#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/3/23 10:55
# @Author   : yuan yuan

from APIAuto.baseRequest.base_grpc_request import *
from APIAuto.baseRequest.parse_file import *

AddOrg = 'AddOrg'
ListOrgTree = 'ListOrgTree'


class OrgApi(object):
    def __init__(self):
        self.req = BaseGRpcRequest()
        self.cf = GetConfig()
        self.parse = ParseFile()

    def add_org(self, host, token, **request):
        resp = self.req.base_request(api_name=AddOrg, host=host, token=token, **request)
        return resp

    def list_org_tree(self, host, token, **request):
        resp = self.req.base_request(self, api_name=ListOrgTree, token=token, host=host, **request)
        return resp



