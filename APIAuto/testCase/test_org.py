#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/3/23 10:55
# @Author   : yuan yuan

import pytest
import allure
from testC4.baseRequest.grpc_request import *

org_data_test = 'org/data_org_1.json'
repeat_create_org = 'org/data_org.json'
org_user_group_enabled = 'org/data_org_list_enabled.json'


@allure.feature("组织层级管理")
class TestOrg(object):

    @allure.severity("normal")
    @allure.story("新建-查询-修改-删除")
    def test_list_org_tree(self):
        GRpcRequest().send_grpc_request(org_data_test)

    @allure.severity("normal")
    @allure.story("创建群组-名称重复")
    def test_repeat_create_org(self):
        GRpcRequest().send_grpc_request(repeat_create_org)

    @allure.severity("normal")
    @allure.story("列出已启用的群组")
    def test_list_org_enable(self):
        GRpcRequest().send_grpc_request(org_user_group_enabled)


if __name__ == '__main__':
    pytest.main(['-s', 'test_org.py'])
