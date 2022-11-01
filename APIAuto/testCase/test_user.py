#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/3/24 15:34
# @Author   : yuan yuan

import allure
import pytest
from testC4.baseRequest.grpc_request import *

update_user_data = 'user/update_user_data.json'

@allure.feature("用户管理")
class TestOrg(object):

    @allure.severity("normal")
    # @allure.feature("用户管理")
    @allure.story("列出已启用的群组")
    def test_update_user(self):
        GRpcRequest().send_grpc_request(update_user_data)


if __name__ == '__main__':
    pytest.main(['-s', 'test_user.py'])
