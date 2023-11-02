#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/3/23 10:55
# @Author   : yuan yuan

import os
from google.protobuf.json_format import MessageToDict
from client.GrpcClient import GrpcClient
from APIAuto.baseRequest.parse_file import *
from utils.HandleLogging import HandleLogging
logger = HandleLogging(file_name="test").getlog()
import baseconfig
proto_file_path = os.path.join(baseconfig.grpc_proto, "c4_platform.proto")


class BaseGRpcRequest(object):
    def __init__(self):
        self.parse = ParseFile()
        self.cf = GetConfig()

    def base_request(self, host=None, api_name=None, token=None, **kwargs):
        """
        如果传的是testData一个测试步骤的结构体，就不用传host和请求参数
        :param host:
        :param api_name:
        :param token:
        :param kwargs:
        :return:
        """

        logger.info(f"=====request_param: {kwargs}=====\n")

        client = GrpcClient(host, proto_file_path, token)
        res = client.run(api_name, **kwargs)
        resp = MessageToDict(res, including_default_value_fields=True, preserving_proto_field_name=True)

        logger.info(f"=====resp: {resp}=====\n")
        return resp



