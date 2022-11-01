#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/3/20 10:55
# @Author   : yuan yuan

import configparser
import os

config_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini'))


class GetConfig(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding='utf-8')

    def get_env(self, _env):
        """
        获取config.ini中[ENV] _env参数对应的值
        :param _env: [ENV]中的参数名，如："EVN_C4"
        :return: [ENV]中参数值
        """
        return self.config.get("ENV", _env)

    def get_account(self, _env, user):
        """
        获取用户名密码
        :param _env: [ENV]中环境参数名，如："EVN_C4"
        :param user: 账号参数名
        :return: ['test_admin', 'Admin_2020']
        """
        user = self.config.get(self.get_env(_env), user).split('/')
        return user

    def get_param(self, _env, param):
        """
        获取对应环境中的参数值
        :param _env: [ENV]中环境参数名，如："EVN_C4"
        :param param: 如："url_grpc"
        :return:
        """
        return self.config.get(self.get_env(_env), param)

