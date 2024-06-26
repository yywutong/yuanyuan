#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/1/10 11:16
# @Author   : yuanyuan
# @File     : 字符串_反转字符串.py
# LastEditTime:


# 编写一个函数，其作用是将输入的字符串反转过来。输入字符串以字符数组 char[] 的形式给出。
# 不要给另外的数组分配额外的空间，你必须原地修改输入数组、使用 O(1) 的额外空间解决这一问题。
# 你可以假设数组中的所有字符都是 ASCII 码表中的可打印字符。
#
# 示例 1：
# 输入：["h","e","l","l","o"]
# 输出：["o","l","l","e","h"]
#
# 示例 2：
# 输入：["H","a","n","n","a","h"]
# 输出：["h","a","n","n","a","H"]

def reverse_string(s: list[str]) -> None:  # 使用range
    for i in range(len(s) // 2):
        s[i], s[len(s) - i - 1] = s[len(s) - i - 1], s[i]
    print(s)


def reverse_string2(s):
    # s[:] = s[:: -1]     # 使用切片
    # s[:] = reversed(s)  # 使用reversed
    # s.reverse()         # 使用reverse()

    s[:] = [s[i] for i in range(len(s) - 1, -1, -1)]  # 使用列表推导
    print(s)


def reverse_string3(s):  # 使用栈
    stack = []
    for i in s:
        stack.append(i)
    for i in range(len(stack)):
        s[i] = stack.pop()
    print(s)


def reverse_string4(s):  # 双指针
    left = 0
    right = len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    print(s)


if __name__ == '__main__':
    ss = ["h", "e", "l", "l", "o"]
    reverse_string3(ss)
