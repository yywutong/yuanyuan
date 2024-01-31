#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/1/10 14:29
# @Author   : yuanyuan
# @File     : 字符串_反转字符串2.py
# LastEditTime:

# 给定一个字符串 s 和一个整数 k，从字符串开头算起, 每计数至 2k 个字符，就反转这 2k 个字符中的前 k 个字符。
# 如果剩余字符少于 k 个，则将剩余字符全部反转。
# 如果剩余字符小于 2k 但大于或等于 k 个，则反转前 k 个字符，其余字符保持原样。
#
# 示例:
# 输入: s = "abcdefg", k = 2
# 输出: "bacdfeg"

def main(s, k):  # 自己写的

    def reverse_substring(text):
        left, right = 0, len(text) - 1
        while left < right:
            text[left], text[right] = text[right], text[left]
            left += 1
            right -= 1
        return text

    s = list(s)
    n = len(s) // (2 * k)
    for i in range(n + 1):
        start = i * 2 * k
        end = start + k
        s[start: end] = reverse_substring(s[start: end])
    return "".join(s)


def reserve_str(s, k):
    def reverse_substring(text):
        left, right = 0, len(text) - 1
        while left < right:
            text[left], text[right] = text[right], text[left]
            left += 1
            right -= 1
        return text

    s = list(s)
    for cur in range(0, len(s), 2 * k):
        s[cur: cur + k] = reverse_substring(s[cur:cur + k])
    return "".join(s)


def reserve_str2(s, k):
    s = list(s)
    t = 0
    for i in range(len(s)):
        s[t:t + k] = s[t:t + k][::-1]
        t += 2 * k
    return "".join(s)


if __name__ == '__main__':
    sss = "abcdefg"
    # ss = main(sss, 2)
    # print(ss)
    ss = reserve_str2(sss, 2)
    print(ss)
