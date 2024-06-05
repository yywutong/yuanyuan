#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/5/21 18:06
# @Author   : yuanyuan
# @File     : 栈与队列_逆波兰表达式.py
# LastEditTime:
from operator import add, sub, mul


# 根据 逆波兰表示法，求表达式的值。
# 有效的运算符包括 + ,  - ,  * ,  / 。每个运算对象可以是整数，也可以是另一个逆波兰表达式。
# 说明：
# 整数除法只保留整数部分。 给定逆波兰表达式总是有效的。换句话说，表达式总会得出有效数值且不存在除数为 0 的情况。
#
# 示例 1：
# 输入: ["2", "1", "+", "3", " * "]
# 输出: 9
# 解释: 该算式转化为常见的中缀算术表达式为：((2 + 1) * 3) = 9
# 示例 2：
# 输入: ["4", "13", "5", "/", "+"]
# 输出: 6
# 解释: 该算式转化为常见的中缀算术表达式为：(4 + (13 / 5)) = 6
# 示例 3：
# 输入: ["10", "6", "9", "3", "+", "-11", " * ", "/", " * ", "17", "+", "5", "+"]
# 输出: 22
# 解释:该算式转化为常见的中缀算术表达式为：
# ((10 * (6 / ((9 + 3) * -11))) + 17) + 5


def evalRPN(li):
    op_map = {"+": add, "-": sub, "*": mul, "/": lambda x, y: int(x / y)}

    stack = []
    for item in li:
        if item not in ["+", "-", "*", "/"]:
            stack.append(int(item))
        else:
            ele2 = stack.pop()
            ele1 = stack.pop()
            stack.append(op_map[item](ele1, ele2))

    return stack[-1]


li_ele = ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
res = evalRPN(li_ele)
print(res)
