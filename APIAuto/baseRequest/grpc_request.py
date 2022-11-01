#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/3/19 10:55
# @Author   : yuan yuan

import base64, ast
import importlib
from utils.HandleGrpcRes import *
from testC4.baseRequest.assertions import *
from testC4.baseRequest.base_grpc_request import *
from testC4.baseRequest.parse_file import *
from testC4.baseRequest.reportFormat import *

file = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apiCommon'))
for root, dirs, files in os.walk(file):
    for file in files:
        if file.endswith(".py"):
            file_name = os.path.splitext(file)[0]
            name = f"testC4.apiCommon.{file_name}"
            module = importlib.import_module(name)


logger = HandleLogging(file_name="test").getlog()
proto_file_path = os.path.join(baseconfig.grpc_proto, "c4_platform.proto")


class GRpcRequest(object):
    def __init__(self):
        self.req = BaseGRpcRequest()
        self.parse = ParseFile()
        self.cf = GetConfig()

    def get_token(self, host, user, password):
        """登录获取token"""
        passwd = base64.b64encode(password.encode("utf-8"))
        login_user = base64.b64encode(user.encode("utf-8"))
        resp = self.req.base_request(host=host, api_name="Login", user_name=user, user_passwd=passwd,
                                     uiid="njoxO2FK4kz4N9coCcFt", captcha="indplat@c4209")
        msg = get_resp_value(resp, "msg")
        if msg == "success":
            logger.info(f"======{user}，{password} 登录成功：{msg}=====")
            token = get_resp_value(resp, "data.token")
            metadata = [("login-user", login_user), ("token", token)]
            logger.info(f"=====headers: {metadata}=====")
            return metadata
        else:
            logger.error(f"======{user}，{password}登录失败：{msg}=====")
            return None

    def send_grpc_request(self, json_file):

        token = None
        json_data = self.parse.read_json(json_file)

        return_param = {}
        for case_name, contents in json_data.items():
            logger.info(f"****************************{case_name}-测试开始*********************************")
            host = self.cf.get_param(self.parse.sys_env_param(contents[0]), "url_grpc")
            logger.info(f"=====host: {host}=====")

            for data in contents:
                temp_data = {}
                try:
                    # 步骤名
                    step_name = data.get("step_name")
                    if step_name:
                        temp_data.update({"step_name": f"{step_name}"})

                    # 登录
                    account = data.get("login_user", [])
                    if account:
                        login_account = GetConfig().get_account(self.parse.sys_env_param(contents[0]), account)
                        temp_data.update({f"login_account": f"{login_account}"})
                        token = self.get_token(host, login_account[0], login_account[1])
                        temp_data["header"] = token

                    # 关联值替换
                    request = data.get("request", {})
                    request = self.parse.replace_param_value(request, return_param)
                    temp_data.update({"request": f"{request}"})

                    # 执行前置方法
                    resp = {}
                    call_classname = data.get("call_classname", "")
                    call_func_name = data.get("call_func_name", "")
                    if call_classname and call_func_name:
                        class_obj = eval("module."+call_classname)
                        resp = getattr(class_obj, call_func_name)(host=host, token=token, **request)

                    # 接口请求
                    api_name_grpc = data.get("api_name_grpc", '')
                    if api_name_grpc:
                        resp = self.req.base_request(host=host, api_name=api_name_grpc, token=token, **request)
                    temp_data.update({"response": f"{resp}"})

                    # 断言
                    assertions = data.get("assertions", {})
                    Assertions().assert_rsp_equal(resp, assertions)

                    # 获取接口返回参数
                    return_data = data.get("return_data", {})
                    if return_data:
                        for return_key, return_value in return_data.items():
                            return_param[return_key] = get_resp_value(resp, return_value)
                except Exception as ex:
                    raise ex
                finally:
                    report_format(data, temp_data)
                    logger.info(f"数据池：{temp_data}")
                    logger.info(f"*************************************************************")
            logger.info(f"****************************{case_name}-测试结束*********************************")



