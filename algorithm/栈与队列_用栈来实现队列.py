#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/5/31 17:39
# @Author   : yuanyuan
# @File     : 栈与队列_用栈来实现队列.py
# LastEditTime:


class MyQueue:

    def __init__(self):
        """
        in主要负责push，out主要负责pop
        """
        self.stack_in = []  # 用列表来模拟栈
        self.stack_out = []

    def push(self, value):
        self.stack_in.append(value)

    def pop(self):
        """
        删除队首元素
        """
        if self.empty():
            return None

        if self.stack_out:
            return self.stack_out.pop()
        else:
            for i in range(len(self.stack_in)):
                self.stack_out.append(self.stack_in.pop())
            return self.stack_out.pop()

    def peek(self):
        """
        Get the front element.
        """
        ele = self.pop()
        return self.stack_in.append(ele)

    def empty(self):
        """
        只要in或者out有元素，说明队列不为空
        """
        return not (self.stack_in or self.stack_out)
