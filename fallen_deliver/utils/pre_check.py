#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2021-06-01 11:56:35
LastEditors: zhoushuke
LastEditTime: 2022-02-07 14:48:06
FilePath: /fallen_deliver/utils/pre_check.py
'''

from config import cfg as CFG
from utils.update_version import Update_Version
from utils.http_ops import Operator_Requests
from utils.func_ops import parse_from_formdata, remove_repeat_str, close_workorder_by_id, send_alert


class PreCheck(object):
    def __init__(self, args, join_flag=True):
        self.Op_Req = Operator_Requests()
        self.subject = "[Fallen] 前置检查失败"
        self.summary = "Fallen Alert"
        self.close_wo = False
        self.apps_info(args, join_flag)

    def _send_alert(self, **kwargs):
        kwargs["工单标题"] = self.title
        kwargs["工单ID"] = self.woid
        event = {
            "ifsendalert": True,
            "alerter": ["mail", "wchook"],
            "subject": self.subject,
            "summary": self.summary,
            "content": kwargs,
            "sendto": self.sendto,
            # "cc": CFG["emailhtml"]["email_cc"]
        }
        send_alert(event)

    def apps_info(self, args, join_flag):
        apps_info = parse_from_formdata(args, join_flag)
        self.apps = apps_info.get("apps")
        self.woid = apps_info.get("woid")
        self.title = apps_info.get("title")
        self.clusters = apps_info.get("clusters")
        self.wotype = apps_info.get("wotype")
        # sendto need to be a list
        self.sendto = remove_repeat_str(
            apps_info.get("order_creator_email") + "," +
            apps_info.get("other_senders_emails"))  # + "," +
        # apps_info.get("creator_leader_email"))  # if need send to leader, drop mark
        # apps_info like: {"order_creator_email": "xxx@sensetime.com", "other_senders_emails": "yyy@sensetime.com", apps: [{"name": "xxx", "version": "yyy"}, {}, ...]}}
        # apps like: [{"name": "xx-test", "version": "oo"}, {"name": "xx-dev", "version": "yy"}, ...]
        # sendto = ["zhoushuke@sensetime.com"]
        # apps = [{
        #     "name": "panorama-backend-test",
        #     "version": "123456"
        # }, {
        #     "name": "panorama-backend-test",
        #     "version": "59b45aa5"
        # }]

    def close_workorder(self):
        close_workorder_by_id(self.woid)

    def check_selected_deploy_cluster(self):
        if len(self.clusters) != 1 or self.clusters[0] not in ("test"):
            content = {"失败原因": "应用提测或者上线时环境只能选择[test],该工单自动关闭"}
            self._send_alert(**content)
            self.close_wo = True
            self.close_workorder()

    def check_same_app_existin_subform(self):
        if len(self.apps) == 0:
            content = {"失败原因": "子表单中未发现应用相关信息,请正确填写,该工单自动关闭"}
            self.close_wo = True
        if len(self.apps) != len(set([d["name"] for d in self.apps])):
            content = {"失败原因": "子表单中发现相同的应用名称,该工单自动关闭"}
            self.close_wo = True
        if self.close_wo:
            self._send_alert(**content)
            self.close_workorder()

    def check_workorder(self):
        uv = Update_Version()
        for app in self.apps:
            real_app = app.get("name").rsplit("-", 1)[0]
            data = uv.query_app_version(real_app)
            if data is False:
                content = {
                    "应用-环境": app.get("name"),
                    "失败原因": "查询app版本时发生异常,请OP确认"
                }
                self._send_alert(**content)
            # if is a bugfix
            elif self.wotype == 2 and len(data) == 0:
                content = {
                    "应用-环境": app.get("name"),
                    "应用版本": app.get("version"),
                    "失败原因": "该应用必须存在提测单才能申请修复单,请去申请提测单,该工单自动关闭"
                }
                self._send_alert(**content)
                self.close_wo = True
                self.close_workorder()
            # if is a test workorder
            elif self.wotype == 1 and len(data) >= 1:
                content = {
                    "应用-环境": app.get("name"),
                    "应用版本": app.get("version"),
                    "失败原因": "该应用已经存在提测单不允许再申请提测单,请去申请修复单,该工单自动关闭"
                }
                self._send_alert(**content)
                self.close_wo = True
                self.close_workorder()
            else:
                pass

    def to_find_arm64_image(self):
        Op_Req = Operator_Requests()
        for app in self.apps:
            name, version = app.get("name"), app.get("version")
            if "test" == name.rsplit("-", 1)[1]:
                url = CFG["registry"]["url"] + name.rsplit("-",
                                                           1)[0] + "/tags/list"
                rnt, res = Op_Req.http_get(
                    url=url,
                    headers={"Content-Type": "applications/json"},
                    data={
                        "user": CFG["registry"]["username"],
                        "password": CFG["registry"]["password"]
                    },
                    timeout=20)
                if rnt > 0:
                    content = {
                        "失败原因":
                        "从镜像仓库返回404,未找到对应的spring-test/arm64/{}".format(
                            name.rsplit("-", 1)[0])
                    }
                    self._send_alert(**content)
                elif version not in res.json().get("tags"):
                    content = {
                        "应用-环境": name,
                        "应用版本": version,
                        "失败原因": "未找到对应ARM64版本的镜像无法提测或上线,该工单自动关闭"
                    }
                    self._send_alert(**content)
                    self.close_wo = True
                    self.close_workorder()
                    break
                else:
                    pass

    def __call__(self, product):
        self.check_selected_deploy_cluster()
        if not self.close_wo:
            self.check_same_app_existin_subform()
        if not self.close_wo and CFG[product]["check_workorder"]:
            self.check_workorder()
        if not self.close_wo and CFG[product]["check_arm64"]:
            self.to_find_arm64_image()
