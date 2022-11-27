#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2022-01-28 13:11:55
LastEditors: zhoushuke
LastEditTime: 2022-02-01 14:11:47
FilePath: /fallen_deliver/utils/app_check_in_backend.py
'''

import jsonpath
from config import cfg as CFG
from loguru import logger as LOGGER
from utils.func_ops import send_alert
from utils.sqlalchemy_db import update_apps_status_by_fallen_subform, get_db_structure_by_tpl_id, update_db_form_structure, get_apps_list_by_status
"""
# 判断传过来的工单类型，如果是提测单，走下面逻辑，不是提测单，直接跳过， 可以将工单类型放入配置文件中
# 对于提测单，在创建工单时，会调用以下逻辑:
# 	1. 获取到子表单数据后拿到应用信息，判断是否在app_lists表中
#		如果存在: 则将应用的状态修改为提测中
#		如果不存在，则整段逻辑跳过
#	2. 根据传过来的模板id，获取到模板数据，并解析模板数据中的组件是否绑定有特定的远端方法(以约定的字符串开头)
#		如果绑定: 则调用远端方法获取数据，将返回数据插回至组件的values
#		如果没有绑定: 直接跳过
"""


class AppCheckInBackend(object):
    def __init__(self, form_data, form_structure):
        self.form_data = form_data
        self.form_structure = form_structure

    # 根据form_structure中获取模板id
    # 更新数据库应用状态
    # todo 优化可自定义字段
    def update_apps_to_status_by_key(self, key, status):
        apps = jsonpath.jsonpath(
            self.form_data, "$..subform_version_info_id..input_deploy_app_id")
        # 返回 ['argo-engine', 'op-service']
        # self.apps = apps
        # 根据应用名设置表apps_list的ckkey标志
        s = {key: status}
        try:
            LOGGER.info("update app status by ckkey: {}".format(apps))
            update_apps_status_by_fallen_subform(apps, s)
        except Exception:
            event = {
                "ifsendalert": True,
                "alerter": ["wchook"],
                "subject": "[Fallen] 设置应用状态失败",
                "summary": "Fallen Alert",
                "content": {
                    "应用列表": apps
                },
                "sendto": CFG["emailhtml"]["email_to"]
            }
            send_alert(event)

    # 根据form_structure中获取模板id
    @staticmethod
    def get_tpl_id_from_extract_from_structure(st):
        tpl_id = jsonpath.jsonpath(st, "$.id")
        # 返回的tpl_id为一维数组
        return tpl_id[0]

    # 从模板中获取应用信息
    # todo.优化可自定义字段
    @staticmethod
    def update_form_structure_into_db_by_tplid(tpl_id, apps):
        db_structure = get_db_structure_by_tpl_id(tpl_id)
        # 如果存在，以防万一
        if db_structure:
            db_structure = db_structure[0]
            # 从form_structure中获取数据库已存在的静态数据
            all_models = jsonpath.jsonpath(db_structure,
                                           "$..model",
                                           result_type=None)
            # todo model一定存在,获取以input_deploy_app_id开头的即可
            for x in all_models:
                if jsonpath.jsonpath(db_structure,
                                     x)[0].startswith('input_deploy_app_id'):
                    # 从前端传过来的表单数据获取model对应的xpath,需要去掉$
                    # $['list'][2]['columns'][0]['list'][0]['options']
                    models_pos = x.replace("['model']", "['options']")
                    # 根据apps_list获取应用列表
                    if apps:
                        # 将apps调整成相对的格式
                        # apps 原始的格式 ['argo-engine', 'op-service']
                        # 需要的格式: [{'value': 'argo-engine'}, {'value': 'op-service'}]
                        tmp_apps = {"options": [{"value": x} for x in apps]}
                        # todo eval的作用是使db_structure能够通过路径进行key更新,maybe有更好的方式
                        eval("db_structure" + models_pos[1:] +
                             ".update(tmp_apps)")
                        # models_values_af = jsonpath.jsonpath(
                        #     db_structure,
                        #     "$['list'][2]['columns'][0]['list'][0]['options']['options']"
                        # )[0]
                        # print(models_values_af)
                        # 使用替换之后的structure替换数据库模板对应的form_structure
                        try:
                            update_db_form_structure(tpl_id, db_structure)
                        except Exception:
                            event = {
                                "ifsendalert": True,
                                "alerter": ["wchook"],
                                "subject": "[Fallen] 更新模板json失败",
                                "summary": "Fallen Alert",
                                "content": {
                                    "模板ID": tpl_id
                                },
                                "sendto": CFG["emailhtml"]["email_to"]
                            }
                            send_alert(event)

    def todo_with_remoteFunc():
        pass
        """
        # todo 使用远端方法
        # all_remotefunc = (jsonpath.jsonpath(d, "$..remoteFunc", result_type=None))
        # if all_remotefunc:
        #     for x in all_remotefunc:
        #         if jsonpath.jsonpath(d, x)[0].startswith('Fallen'):
        #             # 需要先获取remoteFunc对应的函数，进行http get, 获取到相应的数据
        #             # 再通过remoteFunc来定位remoteOptions
        #             y = x.replace("['remoteFunc']", "['remoteOptions']")
        #             # y的值无所谓，最终会被远端方法返回的值给覆盖掉
        #             print(jsonpath.jsonpath(d, y)[0])
        #             # 最终将更新之后的字典覆盖数据库中的模板数据
        #             #
        #             # todo 扩展 为什么要从直接修改静态数据扩展到调用远端方法，是因为:
        #                 # 1. 可以直接修改静态数据，会简单一些，但是不够通用
        #                 # 2. 修改静态数据还是需要判断要修改哪个控件的静态数据，这个最复杂的逻辑还是无法省略
        #     #print(fallen_remotefunc)
        # print(all_remotefunc)
        """

    # 根据tpl_id来区别业务的逻辑关系,关联提测单及修复单
    def update_tpls(self, tpl_id):
        LOGGER.info("update tpls id: {}".format(tpl_id))
        relations = {
            # 深泉
            24: {
                # 对应的所属产品线
                "product": 1,
                # 关联的修复单
                "relation": 26
            },
            # 巡检
            18: {
                "product": 2,
                "relation": 17
            },
            # 质检
            33: {
                "product": 3,
                "relation": 37
            }
        }

        # 如果存在关联的修复单,则也一起更新
        if relations.get(tpl_id, None):
            tc_apps, sx_apps = get_apps_list_by_status(
                relations.get(tpl_id).get("product"))
            LOGGER.info("tiche apps: {}, shangxian apps: {}".format(
                tc_apps, sx_apps))
            # 如果tpl_id一定存在, 则 tc_apps, sx_apps也一定存在
            # 更新提测单, 提测单只显示还没有提测的应用
            self.update_form_structure_into_db_by_tplid(tpl_id, sx_apps)
            # 更新关联的修复单, 修复单只显示已经提测的应用
            self.update_form_structure_into_db_by_tplid(
                relations.get(tpl_id).get("relation"), tc_apps)

    def __call__(self, status):
        self.update_apps_to_status_by_key("ckkey", status)
        tpl_id = self.get_tpl_id_from_extract_from_structure(
            self.form_structure)
        self.update_tpls(tpl_id)
