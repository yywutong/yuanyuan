#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2021-04-20 15:22:57
LastEditors: zhoushuke
LastEditTime: 2021-09-09 14:03:56
FilePath: /fallen_deliver/fallendeliver/deliver.py
'''
import sys
from utils.pre_check import PreCheck
from utils.func_ops import parse_from_formdata, remove_repeat_str
from utils.argocd_deploy import Argocd_Deploy_By_App


def deliver(args):
    apps_info = parse_from_formdata(args)
    # sendto need to be a list
    sendto = remove_repeat_str(
        apps_info.get("order_creator_email") + "," +
        apps_info.get("other_senders_emails"))
    # apps_info like: {"order_creator_email": "xxx@sensetime.com", "other_senders_emails": "yyy@sensetime.com", apps: [{"name": "xxx", "version": "yyy"}, {}, ...]}}
    apps = apps_info.get("apps")
    # apps like: [{"name": "xx-test", "version": "oo"}, {"name": "xx-dev", "version": "yy"}, ...]
    # multiprocessing
    import multiprocessing
    p = multiprocessing.Pool(processes=len(apps))
    for app in apps:
        adba = Argocd_Deploy_By_App(
            **{
                "woid": apps_info.get("woid"),
                "title": apps_info.get("title"),
                "sendto": sendto
            })
        info = adba.get_app_obj(app.get("name"))
        if info and info["spec"]["source"]:
            if "kustomize" in info["spec"]["source"].keys():
                p.apply_async(adba.deploy_app_by_kustomize,
                              args=(app.get("name"), app.get("version")))
            elif "helm" in info["spec"]["source"].keys():
                p.apply_async(adba.deploy_app_by_helm,
                              args=(app.get("name"), app.get("version")))
            else:
                res = {}
                res["应用-环境"] = app.get("name")
                res["应用版本"] = app.get("version")
                res["失败原因"] = "不支持的发布类型,请OP检查发布平台设置"
                adba._send_alert()
    p.close()
    p.join()


def spring_precheck(args):
    pc = PreCheck(args)
    pc("spring")


def c4_precheck(args):
    pc = PreCheck(args)
    pc("c4")


if __name__ == "__main__":
    # one app and one cluster
    # data = '{"id":75,"title":"deploy","priority":1,"form_data":[{ "input_product_version_id": "v2.0", "select_deploy_cluster_id": ["dev"], "text_1618901016000_73105": "产品线定义版本", "text_1618901008000_76230": "开发在提测时提测环境只能选择【test】", "subform_version_info_id": [ { "input_deploy_app_id": "argocd-kustomize-frontend", "input_deploy_version_id": "e3f5df90", "input_deploy_release_version_id": "e3f5df90", "file_1618901245000_38047": [ { "uid": 1619070456961, "name": "argo-v2021验证.txt", "url": "http://fallen.sensespring.local:8800/static/uploadfile/files/44abad2d0bb541d391e83bac11daee55-argo-v2021验证.txt", "status": "success" } ] } ], "text_1614515214000_50854": " 由QA确认该次提测最终的验收版本，开发在提测时请保持与提测版本相同即可", "input_sep_address": "https://gitlab.bj.sensetime.com/zhoushuke/argocd-kustomize-frontend/pipelines", "textarea_1613635281000_24319": "test", "divider_1614176282000_71093": "分割线", "radio_1613639231000_48190": "是", "radio_1613639268000_11141": "否", "date_1618901410000_45646": "2021-04-22", "input_order_creator_email_id": "zhoushuke@sensetime.com", "input_other_senders_emails_id": "zhoushuke@sensetime.com", "input_1614314798000_68210": "", "input_1614314818000_16911": "", "radio_1614314860000_75631": "否", "radio_1614176251000_48132": "否", "textarea_1614176349000_52899": "", "textarea_remark_id": "" }]}'
    # one app and more cluster
    # data = '{"id":75,"title":"deploy","priority":1,"form_data":[{ "input_product_version_id": "v2.0", "select_deploy_cluster_id": ["dev", "test"], "text_1618901016000_73105": "产品线定义版本", "text_1618901008000_76230": "开发在提测时提测环境只能选择【test】", "subform_version_info_id": [ { "input_deploy_app_id": "argocd-kustomize-frontend", "input_deploy_version_id": "26d5960d", "input_deploy_release_version_id": "26d5960d", "file_1618901245000_38047": [ { "uid": 1619070456961, "name": "argo-v2021验证.txt", "url": "http://fallen.sensespring.local:8800/static/uploadfile/files/44abad2d0bb541d391e83bac11daee55-argo-v2021验证.txt", "status": "success" } ] } ], "text_1614515214000_50854": " 由QA确认该次提测最终的验收版本，开发在提测时请保持与提测版本相同即可", "input_sep_address": "https://gitlab.bj.sensetime.com/zhoushuke/argocd-kustomize-frontend/pipelines", "textarea_1613635281000_24319": "test", "divider_1614176282000_71093": "分割线", "radio_1613639231000_48190": "是", "radio_1613639268000_11141": "否", "date_1618901410000_45646": "2021-04-22", "input_order_creator_email_id": "zhoushuke@sensetime.com", "input_other_senders_emails_id": "zhoushuke@sensetime.com", "input_1614314798000_68210": "", "input_1614314818000_16911": "", "radio_1614314860000_75631": "否", "radio_1614176251000_48132": "否", "textarea_1614176349000_52899": "", "textarea_remark_id": "" }]}'
    # more app and more cluster
    # data = '{"id":75,"title":"ct deploy","priority":1,"form_data":[{ "input_product_version_id": "v2.0", "select_deploy_cluster_id": [ "test", "dev" ], "text_1618901016000_73105": "产品线定义版本", "text_1618901008000_76230": "开发在提测时提测环境只能选择【test】", "subform_version_info_id": [ { "input_deploy_app_id": "argocd-kustomize-frontend", "input_deploy_version_id": "e3f5df90", "input_deploy_release_version_id": "e3f5df90", "file_1618901245000_38047": [ { "uid": 1619090938014, "name": "argo-v2021验证.txt", "url": "http://fallen.sensespring.local:8800/static/uploadfile/files/4e264d89347046a6b3256c9b8f04619c-argo-v2021验证.txt", "status": "success" } ] }, { "input_deploy_app_id": "panorama-backend", "input_deploy_version_id": "727dab32", "input_deploy_release_version_id": "727dab32", "file_1618901245000_38047": [] } ], "text_1614515214000_50854": " 由QA确认该次提测最终的验收版本，开发在提测时请保持与提测版本相同即可", "input_sep_address": "https://gitlab.bj.sensetime.com/zhoushuke/argocd-kustomize-frontend/pipelines", "textarea_1613635281000_24319": "xx", "divider_1614176282000_71093": "分割线", "radio_1613639231000_48190": "是", "radio_1613639268000_11141": "否", "date_1618901410000_45646": "2021-04-22", "input_order_creator_email_id": "zhoushuke@sensetime.com", "input_other_senders_emails_id": "13126604488@sensetime.com,zhoushuke@sensetime.com", "input_1614314798000_68210": "", "input_1614314818000_16911": "", "radio_1614314860000_75631": "否", "radio_1614176251000_48132": "否","textarea_1614176349000_52899": "", "textarea_remark_id": ""}]}'
    # deliver(data)
    deliver(sys.argv[1])
