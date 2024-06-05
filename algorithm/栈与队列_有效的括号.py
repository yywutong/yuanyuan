#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/4/29 11:21
# @Author   : yuanyuan
# @File     : 栈与队列_有效的括号.py
# LastEditTime:


# 仅使用栈，更省空间
def is_valid(ss):
    stack = []

    for item in ss:
        if item == "{":
            stack.append("}")
        elif item == "[":
            stack.append("]")
        elif item == "(":
            stack.append(")")
        elif not stack or stack[-1] != item:
            return False
        else:
            stack.pop()

    return True if not stack else False


def is_valid2(ss):
    stack = []
    mapping = {
        "{": "}",
        "[": "]",
        "(": ")"
    }
    for item in ss:
        if item in mapping:
            stack.append(mapping[item])
        elif not stack or stack[-1] != item:
            return False
        else:
            stack.pop()

    return len(stack) == 0


if __name__ == '__main__':
    s = "()[]{}"
    result = is_valid2(s)
    print(result)
