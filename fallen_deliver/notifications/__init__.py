#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2021-04-20 15:50:58
LastEditors: zhoushuke
LastEditTime: 2021-04-21 17:09:49
FilePath: /fallen_deliver/notifications/__init__.py
'''

from notifiers import get_notifier
from config import cfg as CFG
# from notifiers.logging import NotificationHandler


class Notification(object):
    def __init__(self):
        self.sendto = self.mail_sender()

    @staticmethod
    def mail_sender(self):
        params = {}
        params["host"] = CFG["emailhtml"]["smtp_host"]
        params["port"] = int(CFG["emailhtml"]["smtp_port"])
        params["username"] = CFG["emailhtml"]["username"]
        params["password"] = CFG["emailhtml"]["password"]
        params["from"] = CFG["emailhtml"]["from_add"]
        # to can be list, to = ["foo@foo.com", "bar@foo.com"]
        params["to"] = CFG["emailhtml"]["to"]
        return params

    def mail_notify(self, others=[]):
        if others and isinstance(others, list):
            defaults = self.sendto
            defaults["to"].extend(others)
        email = get_notifier("email")
        email.notify(**defaults)
        # handler = NotificationHandler("email", defaults=defaults)
        # logger.add(handler, level="ERROR")
        # use like this, then will send email auto
        # logger.error("this is a error message")
        return handler

    # support more handler in future


handler = Notification(["zhoushuke@sensetime.com"])
