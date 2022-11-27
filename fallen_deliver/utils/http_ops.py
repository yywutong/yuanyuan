#!/usr/local/bin/python
# # -*- coding: utf-8 -*-
'''
@Author: zhoushuke
@Email: zhoushuke@sensetime.com
@Date: 2020-04-24 14:16:06
LastEditors: zhoushuke
LastEditTime: 2021-04-30 09:50:31
FilePath: /fallen_deliver/utils/http_ops.py
'''

import requests
from requests.packages import urllib3
from loguru import logger as LOGGER
from config import cfg as CFG
from requests.adapters import HTTPAdapter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Operator_Requests(object):
    def __init__(self, **kwargs):
        self.conn = self.req_conn(
            kwargs.get("max_retries", CFG["http"]["http_max_retries"]))

    @staticmethod
    def req_conn(max_retries):
        conn = requests.session()
        conn.verify = False
        conn.mount("http://", HTTPAdapter(max_retries=max_retries))
        conn.mount("https://", HTTPAdapter(max_retries=max_retries))
        return conn

    @staticmethod
    def type_map(url, method, wrong, code, msg, rnt):
        LOGGER.error(url)
        msg = {
            # "ConnUrl": url,
            "请求方法": method,
            "错误类型": wrong,
            "状态码": code,
            "响应数据": msg[0:100],
            "返回码": rnt
        }
        return msg

    def http_get(self,
                 url,
                 data=None,
                 headers=None,
                 timeout=CFG["http"]["http_timeout"]):
        try:
            res = self.conn.get(url=url,
                                params=data,
                                headers=headers,
                                timeout=timeout)
            en_code = res.encoding if res.encoding else "utf-8"
        except (requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError) as e:
            msg = self.type_map(url, "GET", "ConnHTTPError", "NULL", str(e), 3)
            LOGGER.error(msg)
            return 3, msg
        except requests.exceptions.Timeout as e:
            msg = self.type_map(url, "GET", "ConnHTTPTimeout", "NULL", str(e),
                                5)
            LOGGER.error(msg)
            return 5, msg
        else:
            if 200 == res.status_code:
                return 0, res
            else:
                msg = self.type_map(
                    url, "GET", "NOT200",
                    str(res.status_code) if res.status_code else "NULL",
                    res.text.encode(en_code) if res.text else "", 7)
                LOGGER.error(msg)
                return 7, msg

    def http_post(self, url, data, headers=None):
        try:
            res = self.conn.post(url=url, data=data, headers=headers)
            en_code = res.encoding if res.encoding else "utf-8"
        except (requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError) as e:
            msg = self.type_map(url, "POST", "ConnHTTPError", "NULL", str(e),
                                3)
            LOGGER.error(msg)
            return 3, msg
        except requests.exceptions.Timeout as e:
            msg = self.type_map(url, "POST", "ConnHTTPTimeout", "NULL", str(e),
                                5)
            LOGGER.error(msg)
            return 5, msg
        else:
            if 200 == res.status_code:
                return 0, res
            else:
                msg = self.type_map(
                    url, "POST", "NOT200",
                    str(res.status_code) if res.status_code else "NULL",
                    res.text.encode(en_code) if res.text else "", 7)
                LOGGER.error(msg)
                return 7, msg

    def http_delete(self, url, data=None, headers=None):
        try:
            # LOGGER.info("url --> {}, data --> {}".format(url, data))
            res = self.conn.delete(url=url, data=data, headers=headers)
            en_code = res.encoding if res.encoding else "utf-8"
        except (requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError) as e:
            msg = self.type_map(url, "DELETE", "ConnHTTPError", "NULL", str(e),
                                3)
            LOGGER.error(msg)
            return 3, msg
        except requests.exceptions.Timeout as e:
            msg = self.type_map(url, "DELETE", "ConnHTTPTimeout", "NULL",
                                str(e), 5)
            LOGGER.error(msg)
            return 5, msg
        else:
            if 200 == res.status_code:
                return 0, res
            else:
                msg = self.type_map(
                    url, "DELETE", "NOT200",
                    str(res.status_code) if res.status_code else "NULL",
                    res.text.encode(en_code) if res.text else "", 7)
                LOGGER.error(msg)
                return 7, msg

    def http_put(self, url, data=None, headers=None):
        try:
            res = self.conn.put(url=url, data=data, headers=headers)
            en_code = res.encoding if res.encoding else "utf-8"
        except (requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError) as e:
            msg = self.type_map(url, "PUT", "ConnHTTPError", "NULL", str(e), 3)
            LOGGER.error(msg)
            return 3, msg
        except requests.exceptions.Timeout as e:
            msg = self.type_map(url, "PUT", "ConnHTTPTimeout", "NULL", str(e),
                                5)
            LOGGER.error(msg)
            return 5, msg
        else:
            if 200 == res.status_code:
                return 0, res
            else:
                msg = self.type_map(
                    url, "PUT", "NOT200",
                    str(res.status_code) if res.status_code else "NULL",
                    res.text.encode(en_code) if res.text else "", 7)
                LOGGER.error(msg)
                return 7, msg
