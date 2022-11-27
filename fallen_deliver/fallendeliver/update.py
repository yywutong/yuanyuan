#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2021-04-23 11:01:15
LastEditors: zhoushuke
LastEditTime: 2021-08-19 13:58:50
FilePath: /fallen_deliver/fallendeliver/update.py
'''

import sys
from utils.func_ops import parse_from_formdata, remove_repeat_str
from utils.update_version import Update_Version


def update(args):
    apps_info = parse_from_formdata(args)
    # sendto need to be a list
    sendto = remove_repeat_str(
        apps_info.get("order_creator_email") + "," +
        apps_info.get("other_senders_emails"))
    # apps_info like: {"order_creator_email": "xxx@sensetime.com", "other_senders_emails": "yyy@sensetime.com", apps: [{"name": "xxx", "version": "yyy"}, {}, ...]}}
    # apps like: [{"name": "xx-test", "version": "oo"}, {"name": "xx-dev", "version": "yy"}, ...]
    uv = Update_Version(
        **{
            "woid": apps_info.get("woid"),
            "title": apps_info.get("title"),
            "sendto": sendto
        })
    uv.query_apps_version(apps_info.get("apps"))


if __name__ == "__main__":
    update(sys.argv[1])
    # data = '{"id":75,"title":"xxxdeploy","priority":1,"form_data":[{ "input_product_version_id": "v2.0", "select_deploy_cluster_id": [ "test" ], "text_1618901016000_73105": "产品线定义版本", "text_1618901008000_76230": "开发在提测时提测环境只能选择【test】", "subform_version_info_id": [ { "input_deploy_app_id": "argocd-kustomize-frontend", "input_deploy_release_version_id": "v3.0" } ], "textarea_1613635281000_24319": "resource-manager-backend", "divider_1614176282000_71093": "分割线", "radio_1613639231000_48190": "是", "radio_1613639268000_11141": "是", "input_order_creator_email_id": "zhoushuke@sensetime.com", "input_other_senders_emails_id": "", "radio_1614314860000_75631": "否", "radio_1614176251000_48132": "否", "textarea_1614176349000_52899": "" }]}'
    # update(data)
