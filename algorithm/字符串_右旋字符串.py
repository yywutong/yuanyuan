#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/1/16 16:42
# @Author   : yuanyuan
# @File     : 字符串_右旋字符串.py
# LastEditTime:


# 字符串的右旋转操作是把字符串尾部的若干个字符转移到字符串的前面。给定一个字符串 s 和一个正整数 k，请编写一个函数，将字符串中的后面 k 个字符移到字符串的前面，实现字符串的右旋转操作。
# 例如，对于输入字符串 "abcdefg" 和整数 2，函数应该将其转换为 "fgabcde"。
# 输入：输入共包含两行，第一行为一个正整数 k，代表右旋转的位数。第二行为字符串 s，代表需要旋转的字符串。
# 输出：输出共一行，为进行了右旋转操作后的字符串。
# 不能申请额外空间，只能在本串上操作


def reverse_str(s, k):  # 按解题思路写的。
    s = list(s[::-1])
    s[:k] = reversed(s[:k])
    s[k:] = reversed(s[k:])
    return "".join(s)


def main():  # 按自己的意思写的。
    s = list(input("请输入字符串s："))
    k = int(input("请输入数字k: "))

    k_list = s[-k:]
    for t in range(len(k_list)):
        s.insert(t, k_list[t])
    ss = s[:-k]
    return "".join(ss)


if __name__ == '__main__':
    sss = "abcdefg"
    kk = 2
    ss = reverse_str(sss, kk)
    print(ss)
