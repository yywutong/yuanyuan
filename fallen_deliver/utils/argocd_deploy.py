#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2021-04-20 15:31:38
LastEditors: zhoushuke
LastEditTime: 2021-12-05 12:29:08
FilePath: /fallen_deliver/utils/argocd_deploy.py
'''

import re
import time
import json
from config import cfg as CFG
from loguru import logger as LOGGER
from utils.func_ops import send_alert, flask_get_oncall_info
from utils.http_ops import Operator_Requests


class Argocd_Deploy_By_App(object):
    def __init__(self, **kwargs):
        self.Op_Req = Operator_Requests()
        self.baseurl = kwargs.get("url", CFG["argocd"]["url"])
        self.subject = "[Fallen] 上线失败"
        self.summary = "Fallen Alert"
        self.sendto = kwargs.get("sendto")
        self.woid = kwargs.get(
            "woid", CFG["fallen"]["missing"])  # set to 0 if no pass.
        self.title = kwargs.get("title", self.summary)

    def _send_alert(self, **kwargs):
        kwargs["工单标题"] = self.title
        kwargs["工单ID"] = self.woid
        event = {
            "ifsendalert":
            True,
            "alerter": ["mail", "wchook"],
            "subject":
            self.subject,
            "summary":
            self.summary,
            "content":
            kwargs,
            "sendto":
            self.sendto if self.sendto else
            [flask_get_oncall_info("op-oncall").get("email")],
            "cc":
            CFG["emailhtml"]["email_cc"]
        }
        send_alert(event)

    def _headers(self):
        headers = {
            "Content-Type": "applications/json",
            "Authorization": "Bearer " + CFG["argocd"]["bearer"]
        }
        return headers

    @staticmethod
    def _update_kustomize_master_img(imgs, app, ver):
        new_imgs = []
        for x in imgs:
            LOGGER.info("kustomize old args: {}, app: {}".format(x, app))
            # in case of multi images name have same prefix, use re to match.
            im = re.findall(r"{{.*/(.*):.*", x)
            if im and app.rsplit("-", 1)[0] == im[0]:
                old = x.split(":")[1]
                LOGGER.info("kustomize new args: {}, app: {}".format(x, im[0]))
                new_imgs.append(x.replace(old, ver))
            else:
                new_imgs.append(x)
        LOGGER.info("update kustomize: {}".format(new_imgs))
        return new_imgs

    '''
    @description: update helm parameters
    @name: _update_helm_img
    @param {*} imgs: app current parameters in argocd like [{"name": "platform.tag", "value": "v2.0.4-55"},{...}]
    @param {*} app: app name in argocd
    @param {*} ver: app new version
    @return {*} return new parameters list like [{"name": "xxx.tag", "version": "yyy"},{...}]
    @author: zhoushuke
    '''

    @staticmethod
    def _update_helm_img(imgs, app, ver):
        new_imgs = []
        for x in imgs:
            if x.get("name") in CFG["c4"]["exclude_apps"]:
                continue
            LOGGER.info("helm old ps: {}, app: {}".format(x, app))
            if app.rsplit("-",
                          1)[0] + CFG["c4"]["key_suffix"] == x.get("name"):
                x["value"] = ver
                LOGGER.info("helm new ps: {}, app: {}".format(x, app))
                new_imgs.append(x)
            else:
                new_imgs.append(x)
        LOGGER.info("update helm: {}".format(new_imgs))
        return new_imgs

    def get_app_obj(self, app):
        headers = self._headers()
        url = self.baseurl + "/api/v1/applications/" + app
        rnt, res = self.Op_Req.http_get(url=url, headers=headers)
        if rnt > 0:
            res["应用-环境"] = app
            res["失败原因"] = "从发布平台获取应用信息失败,请OP检查发布平台设置"
            self._send_alert(**res)
            return None
        else:
            return res.json()

    def set_images_by_kustomize(self, app, ver):
        headers = self._headers()
        url = self.baseurl + "/api/v1/applications/" + app + "/spec"
        info = self.get_app_obj(app)
        if info and "kustomize" in info["spec"]["source"].keys(
        ) and "images" in info["spec"]["source"]["kustomize"].keys():
            # old_imgs is a list
            old_imgs = info["spec"]["source"]["kustomize"]
            # get master image if have one more images
            new_imgs = self._update_kustomize_master_img(
                old_imgs["images"], app, ver)
            # replace images in kustomize use new images
            info["spec"]["source"]["kustomize"]["images"] = new_imgs
            rnt, res = self.Op_Req.http_put(url=url,
                                            data=json.dumps(info["spec"]),
                                            headers=headers)
            if rnt > 0:
                res["应用-环境"] = app
                res["应用版本"] = ver
                res["失败原因"] = "镜像版本更新错误,请检查git下的deploy目录设置"
                self._send_alert(**res)
                return False
        else:
            res = {}
            res["应用-环境"] = app
            res["应用版本"] = "HEAD"
            res["失败原因"] = "未找到对应的kustomize参数,请OP检查发布平台设置"
            self._send_alert(**res)
            return False
        return True

    def set_images_by_helm(self, app, ver):
        headers = self._headers()
        url = self.baseurl + "/api/v1/applications/" + app + "/spec"
        info = self.get_app_obj(app)
        if info and "helm" in info["spec"]["source"].keys(
        ) and "parameters" in info["spec"]["source"]["helm"].keys():
            # parameters old ps, is a list
            old_ps = info["spec"]["source"]["helm"]
            new_ps = self._update_helm_img(old_ps["parameters"], app, ver)
            # replace images in helm use new images
            info["spec"]["source"]["helm"]["parameters"] = new_ps
            rnt, res = self.Op_Req.http_put(url=url,
                                            data=json.dumps(info["spec"]),
                                            headers=headers)
            if rnt > 0:
                res["应用-环境"] = app
                res["应用版本"] = ver
                res["失败原因"] = "镜像版本更新错误,请检查git下的deploy目录设置"
                self._send_alert(**res)
                return False
        else:
            res = {}
            res["应用-环境"] = app
            res["应用版本"] = ver
            res["失败原因"] = "未找到对应的helm参数,请OP检查发布平台设置"
            self._send_alert(**res)
            return False
        return True

    '''
    @description: update helm parameters
    @name: set_images_by_helm_allinone
    @param {*} self
    @param {*} app: app name in argocd
    @param {*} ps: ps is a list like [{"name": "xxx", "version": "yyy"},{...}]
    @return {*} None
    @author: zhoushuke
    '''

    def _sync_app_health(self, app):
        info = self.get_app_obj(app)
        status = info.get("status").get("health").get("status")
        return True if status in ("Healthy", "Missing") else False

    def deploy_app(self,
                   app,
                   rev="HEAD",
                   prune=True,
                   timeout=int(CFG["argocd"]["health_timeout"])):
        # self.set_images_by_kustomize(app, rev)
        headers = self._headers()
        url = self.baseurl + "/api/v1/applications/" + app + "/sync"
        # if app from dev, test, demo, then rev = rev, else reset rev="HEAD"
        env_norev = CFG["spring"]["env_norev"]
        rev = rev if any(env in app for env in env_norev) else "HEAD"
        # todo 这里先写死在deployment中使用了hostNetwork的应用, 需要使用replace --force
        # 目前只有c4的应用里使用到了
        if "camera-backend" in app:
            data = {
                "name": app,
                "prune": prune,
                "revision": rev,
                "strategy": {
                    "hook": {
                        "force": True
                    }
                },
                "syncOptions": {
                    "items": ["Replace=true"]
                }
            }
        else:
            data = {"name": app, "prune": prune, "revision": rev}
        LOGGER.info("POST argocd data: {}".format(data))
        rnt, res = self.Op_Req.http_post(url=url,
                                         data=json.dumps(data),
                                         headers=headers)
        if rnt > 0:
            res["应用-环境"] = app
            res["应用版本"] = rev
            res["失败原因"] = "同步应用失败,请OP检查发布平台设置"
            self._send_alert(**res)
        else:
            # maybe get healthy status after sync right now, so need to wait for a seconds
            time.sleep(5)
            x, healthy = 0, False
            while x < timeout:
                if self._sync_app_health(app):
                    healthy = True
                    break
                else:
                    x += 5
                    time.sleep(5)
                    LOGGER.info(
                        "Still waitting app: {} to be HEALTY status in {}s".
                        format(app, x))
            if not healthy:
                res = {}
                res["应用-环境"] = app
                res["应用版本"] = rev
                res["失败原因"] = "发布应用超时{}s,请登录rancher上查看".format(timeout)
                self._send_alert(**res)

    # for spring
    # app is an app, rev is app's version
    def deploy_app_by_kustomize(self, app, rev):
        if self.set_images_by_kustomize(app, rev):
            self.deploy_app(app, rev)

    # for c4
    # split-out app.
    def deploy_app_by_helm(self, app, rev):
        if self.set_images_by_helm(app, rev):
            self.deploy_app(app, rev)


if __name__ == "__main__":
    adba = Argocd_Deploy_By_App()
    adba.sync_app("this-ia-app", "v1")
