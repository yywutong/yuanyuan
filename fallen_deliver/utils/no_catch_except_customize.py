#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2022-04-20 16:57:38
LastEditors: zhoushuke
LastEditTime: 2022-04-20 17:20:37
FilePath: /fallen_deliver/utils/no_catch_except_customize.py
'''

import sys
from loguru import logger as LOGGER
from functools import wraps
from config import cfg as CFG
from utils.func_ops import send_alert


def global_custome_exception(v):
    event = {
        "ifsendalert": True,
        "alerter": ["mail", "wchook"],
        "subject": "[Fallen] 异常崩溃",
        "summary": "Fallen Alert",
        "content": {
            "崩溃原因": v[0:60]
        },
        "sendto": CFG["emailhtml"]["email_to"]
    }
    send_alert(event)


def handle_exception(exc_type, exc_value, exc_traceback):
    LOGGER.critical(exc_value, exc_info=(exc_type, exc_value, exc_traceback))
    # return directly when user ctrl + C
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    # else use custom exception.
    global_custome_exception(exc_value)


def handle_error(func):
    @wraps(func)
    def __inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handle_exception(exc_type, exc_value, exc_tb)
    return __inner


# useage:
# @handle_error
# def main():
#     try:
#         1/0
#     except Exception as e:
#         print("catch exception by handle")
#
#     # 没有catch的异常将被sys._exception捕获
#     # 1/0
#
#     # raise RuntimeError("RuntimeError")
