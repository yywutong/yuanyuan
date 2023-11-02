#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/4/4 13:04
# @Author   : yuan yuan


import base64, ast
import importlib
from utils.HandleGrpcRes import *
from APIAuto.baseRequest.assertions import *
from APIAuto.baseRequest.base_grpc_request import *
from APIAuto.baseRequest.parse_file import *
from APIAuto.baseRequest.reportFormat import *
from lib.request_http import *
from lib.parse_data import *

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
        self.req_h = RequestsHttp()
        self.p = ParseData()

    def send_http_request(self, json_file):

        headers = None
        json_data = self.parse.read_json(json_file)
        global_param = {}
        for case_name, contents in json_data.items():

            logger.info(f"****************************{case_name}-测试开始*********************************")
            loop_num = contents[0].get('loop_num', 1)
            loop_step_index = contents[0].get('loop_step_index', 0)

            system = self.parse.sys_env_param(contents[0])
            host = self.cf.get_param(system, "url_http")
            logger.info(f"=====host: {host}=====")

            for loop_index in loop_num:
                global_param['loop_index'] = loop_index
                for data in contents:
                    temp_data = {}
                    try:
                        # 步骤名
                        step_name = data.get("step_name")
                        if step_name:
                            temp_data.update({"step_name": f"{step_name}"})

                        # 将global_variable参数化并添加到global_param
                        global_variable = data.get('global_variable')
                        return_p = self.p.for_global_variable(global_variable, global_param)
                        global_param.update(return_p)
                        # 登录
                        account = data.get("login_user", [])
                        if account:
                            login_account = GetConfig().get_account(system, account)
                            temp_data.update({f"login_account": f"{login_account}"})
                            headers = self.req_h.get_token_c4(host, login_account[0], login_account[1])  # 这里是写死的C4，后面会改
                            temp_data["header"] = headers

                        # api_name_http = test_data.get('api_name_http')
                        # api_name = self.p.param_relate(api_name_http, global_param)  # 替换api_name参数化的值
                        # method = test_data.get('method')
                        # param = test_data.get('params')
                        # params = self.p.param_relate(param, global_param)  # 替换param参数化的值
                        # body = test_data.get('body')
                        # body = self.p.param_relate(body, global_param)  # 替换body参数化的值
                        # files = test_data.get('files')
                        # files = self.p.param_relate(files, global_param)  # 待优化
                        # url = 'https://' + host + api_name
                        step_loop_num = data.get('loop_num', 1)
                        step_loop_num = self.p.param_relate(step_loop_num, global_param)
                        for index in range(step_loop_num):
                            global_param['loop_index'] = index
                            # 接口请求
                            response, return_data = self.req_h.send_http_request(host, headers, data, global_param)
                            global_param.update(return_data)

                    except Exception as ex:
                        raise ex
                    finally:
                        report_format(data, temp_data)
                        logger.info(f"数据池：{temp_data}")
                        logger.info(f"*************************************************************")

            logger.info(f"****************************{case_name}-测试结束*********************************")


    def http_step_exec(self, origin_data, step_index, host, global_param):

        # 登录
        account = origin_data[step_index].get("login_user", [])
        if account:
            login_account = GetConfig().get_account('c4', account)
            headers = self.req_h.get_token_c4(host, login_account[0], login_account[1])  # 这里是写死的C4，后面会改
            global_param["headers"] = headers

        # 将global_variable参数化并添加到global_param
        global_variable = origin_data[step_index].get('global_variable')
        return_p = self.p.for_global_variable(global_variable, global_param)
        global_param.update(return_p)

        api_name_http = origin_data[step_index].get('api_name_http')
        api_name = self.p.param_relate(api_name_http, global_param)  # 替换api_name参数化的值
        method = origin_data[step_index].get('method')
        param = origin_data[step_index].get('params')
        params = self.p.param_relate(param, global_param)  # 替换param参数化的值
        body = origin_data[step_index].get('body')
        body = self.p.param_relate(body, global_param)  # 替换body参数化的值
        files = origin_data[step_index].get('files')
        files = self.p.param_relate(files, global_param)  # 待优化
        url = 'https://' + host + api_name

        # 执行封装的方法
        resp = {}
        call_classname = origin_data[step_index].get("call_classname", "")
        call_func_name = origin_data[step_index].get("call_func_name", "")
        if call_classname and call_func_name:
            class_obj = eval("module." + call_classname)
            resp = getattr(class_obj, call_func_name)(url=url, headers=global_param['headers'],
                                                      params=params,
                                                      json=body,
                                                      files=files)

        # 接口请求
        if api_name_http and method and host:
            resp = self.req_h.base_http_request(method=method, url=url, headers=global_param['headers'], params=params,
                                                json=body,
                                                files=files)
        else:
            logging.error(f"api_name_http:{api_name_http},method:{method},host:{host}不能为空")
        status_code = resp.status_code
        try:
            response = resp.json()
            response["status_code"] = status_code  # 将status_code写入response
        except:
            response = resp

        # 断言
        assertions = origin_data[step_index].get('assertions')

        # 获取接口返回参数
        return_data = dict()
        extract = origin_data[step_index].get("return_data", {})
        if extract:
            for extract_key, extract_value in extract.items():
                global_param[extract_key] = get_resp_value(response, extract_value)
        return return_data



