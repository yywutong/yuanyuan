#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2021-06-01 13:13:29
LastEditors: zhoushuke
LastEditTime: 2021-06-01 23:18:29
FilePath: /fallen_deliver/fallendeliver/standardops.py
'''

from utils.standard_ops import Standard_Ops


def standardops(args):
    so = Standard_Ops(args)
    so()


if __name__ == "__main__":
    data = "{\"id\":266,\"title\":\"更新op-service\",\"priority\":3,\"form_data\":[{\"divider_1614176282000_71093\":\"分割线\",\"input_order_creator_email_id\":\"duguangjun_vendor@sensetime.com\",\"input_other_senders_emails_id\":\"\",\"input_product_version_id\":\"v3.2\",\"input_wotype_id\":\"修复单\",\"radio_1613639231000_48190\":\"是\",\"radio_1613639268000_11141\":\"否\",\"radio_1614176251000_48132\":\"是\",\"radio_1614314860000_75631\":\"否\",\"select_deploy_cluster_id\":[\"3s\",\"demo\",\"test\"],\"subform_version_info_id\":[{\"input_deploy_app_id\":\"op-service\",\"input_deploy_release_version_id\":\"v0.4.0\"}],\"text_1618901008000_76230\":\"开发在提测时提测环境只能选择【test】\",\"text_1618901016000_73105\":\"产品线定义版本\",\"textarea_1613635281000_24319\":\"修复vid为空的问题\",\"textarea_1614176349000_52899\":\"更新 配置文件  op-procession版本为 0.1.18\"}]}"
    standardops(data)
