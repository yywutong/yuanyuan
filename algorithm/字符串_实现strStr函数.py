#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/1/16 18:10
# @Author   : yuanyuan
# @File     : 字符串_实现strStr函数.py
# LastEditTime:

# 实现 strStr() 函数。
# 给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如果不存在，则返回  -1。
# 示例 1: 输入: haystack = "hello", needle = "ll" 输出: 2
# 示例 2: 输入: haystack = "aaaaa", needle = "bba" 输出: -1
# 说明: 当 needle 是空字符串时，我们应当返回什么值呢？这是一个在面试中很好的问题。 对于本题而言，当 needle 是空字符串时我们应当返回 0 。这与C语言的 strstr() 以及 Java的 indexOf() 定义相符。

# KMP算法
# 前缀是指不包含最后一个字符的所有以第一个字符开头的连续子串；
# 后缀是指不包含第一个字符的所有以最后一个字符结尾的连续子串
# 前缀表：统计了各个位置为终点字符串的最长相同前后缀的长度。


class Solution:
    """
    # 初始化：next数组、j前缀子串末尾位置、i后缀子串起始位置
    # 当前缀末尾！=后缀起始时
    # 当前缀末尾 =后缀起始时
    """

    def get_next(self, next, s):  # 使用KMP算法构建前缀表（next数组）
        """
        next： 前缀表数组
        s： 模式串
        """
        j = 0  # 前缀子串末尾位置
        next[0] = j

        for i in range(1, len(s)):  # i：后缀子串起始位置
            while j > 0 and s[j] != s[i]:  # 当前缀起始！=后缀起始时，j回退到前一位指向的位置，再进行循环比较。
                j = next[j - 1]
            if s[j] == s[i]:  # 当前缀起始=后缀起始时，j往后移一位。
                j += 1
            next[i] = j

    def strStr(self, haystack, needle):
        j = 0  # 指向needle字符位置
        next = [0] * len(needle)
        self.get_next(next, needle)

        if len(needle) == 0:
            return 0
        for i in range(len(haystack)):
            while haystack[i] != needle[j] and j > 0:
                j = next[j - 1]
            if haystack[i] == needle[j]:
                j += 1
            if j == len(needle):
                return i - len(needle) + 1
        return -1


# 暴力解法
def strStr1(haystack, needle):
    for i in range(len(haystack)):
        if haystack[i:i + len(needle)] == needle:
            return i
    return -1


# find
def strStr2(haystack, needle):
    return haystack.find(needle)


# index
def strStr3(haystack, needle):
    try:
        return haystack.index(needle)
    except ValueError:
        return -1


if __name__ == '__main__':
    haystack = "aabaabaaf"
    needle = "aabaaf"

    # n = Solution().strStr(haystack, needle)
    # print(n)

    n = strStr3(haystack, needle)
    print(n)
