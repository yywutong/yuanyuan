#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2021-04-25 10:40:59
LastEditors: zhoushuke
LastEditTime: 2021-09-24 11:16:12
FilePath: /fallen_deliver/utils/update_version.py
'''

import re
import time
from config import cfg as CFG
from loguru import logger as LOGGER
from utils.func_ops import DataBaseHandle, send_alert


class Update_Version(object):
    def __init__(self, **kwargs):
        self.DbHandle = DataBaseHandle()
        self.subject = "[Fallen] 更新失败"
        self.summary = "Fallen Alert"
        self.sendto = kwargs.get("sendto")
        self.title = kwargs.get("title", self.summary)
        self.woid = kwargs.get("woid")
        self.STATUS = "QATesting"

    def _send_alert(self, **kwargs):
        kwargs["工单标题"] = self.title
        kwargs["工单ID"] = self.woid
        event = {
            "ifsendalert": True,
            "alerter": ["mail", "wchook"],
            "subject": self.subject,
            "summary": self.summary,
            "content": kwargs,
            "sendto": CFG["emailhtml"]["email_to"]
        }
        send_alert(event)

    def update_app_release_version(self, id, app, version, remark, inx):
        sql = "UPDATE p_work_order_tpl_data a SET form_data = JSON_REPLACE ( form_data, '$.subform_version_info_id[{}].input_deploy_release_version_id','{}', '$.textarea_remark_id', '{}' ) WHERE a.wotype = 1  AND work_order = {}".format(
            inx, version, remark, id)
        LOGGER.info("update sql: {}".format(sql))
        if not self.DbHandle.updateDB(sql):
            res = {}
            res["应用-环境"] = app
            res["应用版本"] = version
            res["失败原因"] = "在数据库中更新应用版本失败,请联系OP"
            self._send_alert(**res)

    def query_app_in_json_index(self, app, id):
        # query app index in result
        sql = "SELECT JSON_UNQUOTE(JSON_SEARCH(a.form_data ->> '$.subform_version_info_id[*]', 'one', '{}' )) inx FROM p_work_order_tpl_data a WHERE a.wotype=1 and work_order={}".format(
            app, id)
        LOGGER.info("query index sql: {}".format(sql))
        # like {["inx": "$[0].input_deploy_app_id"]}
        return self.DbHandle.selectDB(sql)

    def query_app_version(self, app):
        # sql = SELECT a.work_order id, jt.app, jt.version, a.form_data ->> '$.textarea_remark_id' textarea_remark FROM p_work_order_tpl_data a, p_work_order_info b, JSON_TABLE (form_data, '$.subform_version_info_id[*]' COLUMNS (app VARCHAR (50) PATH '$.input_deploy_app_id', version VARCHAR (50) PATH '$.input_deploy_release_version_id')) AS jt WHERE a.wotype = 1 AND a.work_order = b.id AND b.is_end = 0 AND b.delete_time is null AND JSON_CONTAINS (b.state, '{"label": "QATesting"}') AND jt.app = 'sensebee-frontend'
        # use mysql v8, json_table
        sql = "SELECT a.work_order id, jt.app, jt.version, a.form_data ->> '$.textarea_remark_id' textarea_remark FROM p_work_order_tpl_data a, p_work_order_info b, JSON_TABLE (form_data, '$.subform_version_info_id[*]' COLUMNS (app VARCHAR (50) PATH '$.input_deploy_app_id', version VARCHAR (50) PATH '$.input_deploy_release_version_id')) AS jt WHERE a.wotype = 1 AND a.work_order = b.id AND b.is_end = 0 AND b.delete_time is null AND JSON_CONTAINS (b.state, '{" + "\"label\": \"" + self.STATUS + "\"}') AND jt.app = '" + app + "'"
        LOGGER.info("query version sql: {}".format(sql))
        # like [{'id': 110, 'app': 'resource-manager-backend', 'version': '74b0fb5b', 'textarea_remark': '[Fallen Operator]: update app: resource-manager-backend version from: 3a2dead3 to: 74b0fb5b'}]
        return self.DbHandle.selectDB(sql)

    # apps like: [{"name": "xx-test", "version": "oo"}, {"name": "xx-dev", "version": "yy"}, ...]
    def query_apps_version(self, apps):
        for app in apps:
            real_app = app.get("name").rsplit("-", 1)[0]
            data = self.query_app_version(real_app)
            if data is False:
                res = {}
                res["应用-环境"] = app.get("name")
                res["应用版本"] = app.get("version")
                res["失败原因"] = "查询数据库时发生网络异常,请联系OP"
                self._send_alert(**res)
            # have one work-order in processing
            elif len(data) == 1:
                if data[0].get("version") != app.get("version"):
                    old_remark = data[0].get("textarea_remark")
                    if "Fallen Operator" in old_remark:
                        new_remark = old_remark + ",update app {} version from {} to {}".format(
                            real_app, data[0].get("version"),
                            app.get("version"))
                    else:
                        new_remark = " [Fallen Operator]: update app {} version from {} to {} ".format(
                            real_app, data[0].get("version"),
                            app.get("version"))
                    LOGGER.info(new_remark)
                    # query app index in result
                    _inx = self.query_app_in_json_index(
                        real_app, data[0].get("id"))[0]
                    inx = re.findall(r"\d+", _inx.get("inx"))[0]
                    self.update_app_release_version(data[0].get("id"),
                                                    real_app,
                                                    app.get("version"),
                                                    new_remark, inx)
                    time.sleep(2)
            elif len(data) == 0:
                LOGGER.info("NotFound need to modify app version, Just deploy")
            else:
                res = {}
                res["应用-环境"] = app.get("name")
                res["应用版本"] = app.get("version")
                res["失败原因"] = "该应用同时存在多个处于{}状态的提测单,请联系QA/OP".format(
                    self.STATUS)
                self._send_alert(**res)
