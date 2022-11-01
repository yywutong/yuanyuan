#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/3/20 10:55
# @Author   : yuan yuan

import json
import re
from testC4.baseRequest.get_config import *
from testC4.pre_func import *
from utils.HandleLogging import *
logger = HandleLogging(file_name="test").getlog()


class ParseFile(object):

    def json_file_path(self, file_path):
        """testC4/testData下的文件路径"""
        return os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testData', file_path))

    def read_json(self, file_path):
        file = self.json_file_path(file_path)
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def sys_env_param(self, data):
        """
        根据testData-json文件中system值，返回config.ini对应环境配置名称
        :param data: json文件每个测试步骤的结构体{}
        :return: C4 - EVN_C4
        """
        system = data.get("system").lower()
        if system == 'c4':
            return "EVN_C4"
        elif system == 'spring':
            return "ENV_SPRING"

    def get_value(self, contents, input_key):
        """
        获取参数的值
        """
        for content_key, content_value in contents.items():
            if content_key == input_key:
                return content_value
            elif isinstance(content_value, dict) and content_value:  # 有bug
                result = self.get_value(content_value, input_key)
                if result:
                    return result

    def replace_param_value(self, request, return_param):
        """
        1. request里面的请求参数参数参数化时，将return_param里面的值替换进去
        2. request里面的请求参数调用一个函数时，执行函数值赋值给参数
        :param request: json文件里面的request请求参数体{}
        :param return_param: 上一个测试步骤返回的值放在这里
        :return:
        """
        if request:
            for request_key, request_value in request.items():
                # 替换前置步骤返回的值
                if isinstance(request_value, str) and request_value.startswith("{{") and return_param:
                    value = re.findall("{{(.*?)}}", request_value)[0]
                    request[request_key] = return_param[value]
                # 替换参数值为一个函数的值
                if isinstance(request_value, str) and request_value.startswith("&{"):
                    value = re.findall("&{(.*?)}", request_value)[0]
                    request[request_key] = eval(value)
        return request

    def check_exit(self, step_sequence, loop_step):
        """判断某个step是否在step_sequence列表中存在"""
        flag = 1
        for step_seq in step_sequence:
            if isinstance(step_seq, int):
                if loop_step == step_seq:
                    flag = 0
            # elif isinstance(step_seq, dict):
            #     for step_key, step_value in step_seq.items():
            #         if loop_step in step_value or step_seq == step_key:
            #             flag = 0
            elif isinstance(step_seq, list):
                if loop_step in step_seq:
                    flag = 0
        return flag

    def check_loop_exit(self, step_sequence, loop_step):
        """判断step列表是否在step_sequence中存在"""
        flag = 1
        for step_seq in step_sequence:
            # if isinstance(step_seq, dict):
            #     for step_value in step_seq.values():
            #         if loop_step == step_value:  # 如果loop step已存在则不添加
            #             flag = 0
            if isinstance(step_seq, list):
                if loop_step == step_seq:  # 如果loop step已存在则不添加
                    flag = 0
        return flag

    def get_step_index(self, loop_step, loop_num, step_sequence, index, case_name):
        """
        loop_num是定量情况下，根据loop_num将step index添加到step_sequence
        :param loop_step: json文件中配置的 - 循环步骤，需要包含当前步骤，
                          如果是列表则循环规则例如loop_num: 2,loop_step：[2,3]，则执行step2-step3,再step2-step3
        :param loop_num: json文件中配置的 - 循环次数
        :param step_sequence: 步骤列表
        :param index: json文件中case step index
        :param case_name:
        :return: step_sequence
        """
        if isinstance(loop_step, list):
            if len(loop_step) == 1 or len(loop_step) == 0:  # loop_step只能配置当前步骤或者包含当前步骤
                flag = self.check_exit(step_sequence, index)
                if flag:
                    for i in range(loop_num):
                        step_sequence.append(index)
            else:   # 循环步骤多于1步时，则顺序循环测试步骤。例如loop_num: 2,loop_step：[2,3]，则执行step2-step3,再step2-step3
                flag_1 = self.check_exit(step_sequence, loop_step[0])
                flag_2 = self.check_exit(step_sequence, loop_step[-1])
                if flag_1 and flag_2:
                    if index in loop_step:
                        for i in range(loop_num):
                            for step in loop_step:
                                step_sequence.append(step)
                    else:
                        raise logger.error(f"用例{case_name}第{index}步的loop_step配置错误，循环步骤中没有包含当前步骤")

        else:  # loop_step为int 或不写时，只能循环当前步骤
            flag = self.check_exit(step_sequence, index)
            if flag:
                for i in range(loop_num):
                    step_sequence.append(index)

        #
        #
        # if len(loop_step) == 0:  # json中循环步骤没有写时，则循环当前步骤
        #     flag = self.check_exit(step_sequence, index)
        #     for i in range(loop_num):
        #         if flag:
        #             step_sequence.append(index)
        #
        # elif len(loop_step) == 1:
        #     if isinstance(loop_step, int):
        #         loop_step = loop_step
        #     elif isinstance(loop_step, list):
        #         loop_step = loop_step[0]
        #     else:
        #         loop_step = index  # 如果loop_step不是int或list时，则loop_step=当前步骤
        #
        #     flag = self.check_exit(step_sequence, loop_step)
        #     if flag:
        #         if loop_step == index:  # 循环步骤等于当前步骤
        #             for i in range(loop_num):
        #                 step_sequence.append(index)
        #         else:
        #             raise logger.error(f"用例{case_name}第{index}步的loop_step配置错误，应该等于当前步骤或不写，实际为：{loop_step}")
        #
        # else:  # 循环步骤多于1步时，则顺序循环测试步骤。例如loop_num: 2,loop_step：[2,3]，则执行step2-step3,再step2-step3
        #     flag = self.check_loop_exit(step_sequence, loop_step)
        #     if flag:
        #         if index in loop_step:
        #             for i in range(loop_num):
        #                 for step in loop_step:
        #                     step_sequence.append(step)
        #         else:
        #             raise logger.error(f"用例{case_name}第{index}步的loop_step配置错误，循环步骤中没有包含当前步骤")
        return step_sequence

    def step_exec_sequence(self, case_name, origin_data):
        step_sequence = list()  # 用例执行步骤[1,2,{3:[4,5]},6]
        variable_keys = {}  # key:步骤，value输出的变量名

        for index in range(len(origin_data)):
            loop_num = origin_data[index].get("loop_num", 1)
            loop_step = origin_data[index].get("loop_step", [])
            if isinstance(loop_num, int):
                # loop_num是定量时，添加测试步骤执行顺序到step_sequence
                self.get_step_index(loop_step, loop_num, step_sequence, index, case_name)

                # # 将每个步骤要输出的参数暂存，用来判断是否输出了循环次数变量
                # global_variable = origin_data[index].get("global_variable", "")
                # var_key = []
                # if global_variable:
                #     if isinstance(global_variable, list):
                #         for variable in global_variable:
                #             var_key += list(variable.keys())
                #     else:
                #         var_key += list(global_variable.keys())
                # return_data = origin_data[index].get("return_data", {})
                # if return_data:
                #     var_key += list(return_data.keys())
                # if var_key:
                #     variable_keys[index] = var_key

            # 循环次数是变量，则需要根据前面的接口来获取执行次数
            elif isinstance(loop_num, str) and loop_num.startswith("{{"):
                loop_str = re.findall("{{+(.*?)}+}", loop_num)[0]
                # temp = {}
                # judge_step = int()  # 判断循环次数的步骤
                # for key, value in variable_keys.items():
                #     if loop_str in value:
                #         judge_step = key
                # if loop_step:
                #     if isinstance(loop_step, int):
                #         if loop_step == index:
                #             loop_step = [loop_step]
                #         else:
                #             raise logger.error(f"用例【{case_name}】第【{index}】步的loop_step配置错误，循环步骤中没有包含当前步骤")
                #     elif isinstance(loop_step, list):
                #         if index in loop_step:
                #             loop_step = loop_step
                #         else:
                #             raise logger.error(f"用例【{case_name}】第【{index}】步的loop_step配置错误，循环步骤中没有包含当前步骤")
                #     else:
                #         loop_step = [index]
                # else:
                #     loop_step = [index]
                # temp[judge_step] = loop_step

                temp = []
                if loop_step:
                    if isinstance(loop_step, int):
                        if loop_step == index:
                            temp = [loop_step]
                        else:
                            raise logger.error(f"用例【{case_name}】第【{index}】步的loop_step配置错误，循环步骤中没有包含当前步骤")
                    elif isinstance(loop_step, list):
                        if index in loop_step:
                            temp = loop_step
                        else:
                            raise logger.error(f"用例【{case_name}】第【{index}】步的loop_step配置错误，循环步骤中没有包含当前步骤")
                    # else:
                    #     temp = [index]
                else:
                    temp = [index]

                # 判断循环步骤不在step_sequence则添加
                flag = self.check_loop_exit(step_sequence, loop_step)
                if flag:
                    step_sequence.append(temp)
                    # if judge_step in step_sequence:
                    #     step_sequence.remove(judge_step)

        return step_sequence


if __name__ == '__main__':

    # dd = [1,2,{3:[4,5]},6]
    # for s in dd:
    #     if isinstance(s, int):
    #         pass  # 执行接口请求
    #     elif isinstance(s, dict):
    #         for s_key, s_value in s.items():
    #             pass  # 执行s的接口请求，获取循环次数（if输出参数=loop_str）
    #             # [4,5]的循环步骤--》
    #             sss = [4,5,4,5]
    #             for v in sss:
    #                 pass  # 执行v的接口
    p = ParseFile()
    file_path = r"D:\00code\qa_auto\testC4\testData\spring_upload.json"
    data = p.read_json(file_path)
    for case_name, origin_data in data.items():
        l = p.step_exec_sequence(case_name, origin_data)
        print(l)
    # ff = [0, 0, 1, {2: [3, 4]}]
    # gg = [0,1]
    # if gg in ff:
    #     print("yes")
    # else:
    #     print("no")
    # step_sequence = [0, 0, 1, {2: [3, 4]}, {2: [4, 5]}]
    # loop_step = [1,2]
    # flag = p.check_loop_exit(step_sequence, loop_step)
    # print(flag)


