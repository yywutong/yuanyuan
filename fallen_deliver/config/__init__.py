#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: zhoushuke
@Email: zhoushuke@sensetime.com
@Date: 2020-04-29 11:33:35
LastEditors: zhoushuke
LastEditTime: 2021-06-01 17:14:58
FilePath: /fallen_deliver/config/__init__.py
'''

import os
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Get_Config(object):
    def __init__(self, path="config.yml", mode="default"):
        self.path = path
        self.mode = mode
        self.cfg = None

    def parse_conf(self):
        if os.path.exists(self.path):
            with open(self.path, "rt") as fh:
                config = load(fh, Loader=Loader)
                cfg = config[self.mode]
        else:
            raise ValueError("CONFIG FILE NOT FOUND")
            os._exit(1)
        return cfg


# CONF_PATH = os.path.dirname(os.path.abspath(__file__))
CONF_PATH = "/etc/fallendeliver"
cfg = Get_Config(path="{}/config.yml".format(CONF_PATH),
                 mode="default").parse_conf()
