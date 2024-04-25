#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/2/2 15:17
# @Author   : yuanyuan
# @File     : 双指针_替换数字.py
# LastEditTime:

# 给定一个字符串 s，它包含小写字母和数字字符，请编写一个函数，将字符串中的字母字符保持不变，而将每个数字字符替换为number。
# 例如，对于输入字符串 "a1b2c3"，函数应该将其转换为 "anumberbnumbercnumber"。
# 对于输入字符串 "a5b"，函数应该将其转换为 "anumberb"
# 输入：一个字符串 s,s 仅包含小写字母和数字字符。
# 输出：打印一个新的字符串，其中每个数字字符都被替换为了number
#
# 样例输入：a1b2c3
# 样例输出：anumberbnumbercnumber
# 数据范围：1 <= s.length < 10000


def replace_element(s):
    s = list(s)
    count = 0
    for sss in s:
        if "0" <= sss <= "9":
            count += 1
    ss = s + ["0"] * (5 * count)

    i = len(s) - 1
    j = len(ss) - 1
    while i >= 0 and j >= 0:
        if "0" <= ss[i] <= "9":
            ss[j] = "r"
            ss[j - 1] = "e"
            ss[j - 2] = "b"
            ss[j - 3] = "m"
            ss[j - 4] = "u"
            ss[j - 5] = "n"
            j -= 6
        else:
            ss[j] = ss[i]
            j -= 1
        i -= 1
    return "".join(ss)


# number
s = "a1b2c3"
a = replace_element(s)
print(a)
