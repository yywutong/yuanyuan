#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/1/12 10:40
# @Author   : yuanyuan
# @File     : 字符串_替换数字.py
# LastEditTime:


# 输入：一个字符串 s,s 仅包含小写字母和数字字符。
# 输出：打印一个新的字符串，其中每个数字字符都被替换为了number
# 样例输入：a1b2c3
# 样例输出：anumberbnumbercnumber
# 数据范围：1 <= s.length < 10000。

import re


def replace_digit(s):
    return re.sub(r"\d", "number", s)


def main(s):
    s = list(s)

    count = 0
    for l in s:
        if "0" < l < "9":
            count += 1
    i = len(s) - 1
    j = len(s) + count * 5 - 1
    new_s = ["0"] * (j + 1)

    while i >= 0 and j >= 0:
        if '0' <= s[i] <= '9':
            new_s[j] = 'r'
            new_s[j - 1] = 'e'
            new_s[j - 2] = 'b'
            new_s[j - 3] = 'm'
            new_s[j - 4] = 'u'
            new_s[j - 5] = 'n'
            j -= 6
        else:
            new_s[j] = s[i]
            j -= 1
        i -= 1
    return "".join(new_s)


def main2(s):
    new_s = str()
    for i in s:
        if "0" <= i <= "9":
            new_s += "number"
        else:
            new_s += i
    return new_s


if __name__ == '__main__':
    ss = "a1b2c3"
    # numb = replace_digit(ss)
    # print(numb)
    n = main2(ss)
    print(n)
