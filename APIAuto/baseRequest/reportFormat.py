#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/3/28 11:13
# @Author   : yuan yuan

import allure
from utils.HandleLogging import HandleLogging
logger = HandleLogging(file_name="test").getlog()


def report_format(data, temp_data):
    if data and temp_data:
        with allure.step(f"步骤：{data['step_name']}"):
            if data['step_name'] == '0.登录':
                allure.attach(f"{temp_data.get('login_account')}", "登录账号")
                allure.attach(f"{temp_data.get('header')}", "header")
            elif not data['api_name_grpc']:
                allure.attach(f"{temp_data.get('request')}", "请求参数")
                allure.attach(f"{temp_data.get('response')}", "响应结果")
                allure.attach(f"{data.get('assertions')}", "断言数据")
            else:
                allure.attach(f"{data.get('api_name_grpc')}", "接口名")
                allure.attach(f"{temp_data.get('request')}", "请求参数")
                allure.attach(f"{temp_data.get('response')}", "响应结果")
                allure.attach(f"{data.get('assertions')}", "断言数据")

    else:
        logger.error("数据为空")
