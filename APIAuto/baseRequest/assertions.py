#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/3/21 10:55
# @Author   : yuan yuan

import unittest


class Assertions(unittest.TestCase):

    def assert_rsp_equal(self, response, expect):
        if expect:
            code = response.get('code', '')
            msg = response.get('msg', '')
            self.assertEqual(code, expect['code'], "返回code不匹配")
            self.assertEqual(msg, expect['msg'], "返回msg不匹配")



