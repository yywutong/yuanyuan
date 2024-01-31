#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/1/19 10:47
# @Author   : yuanyuan
# @File     : 字符串_重复的子字符串.py
# LastEditTime:

# 给定一个非空的字符串，判断它是否可以由它的一个子串重复多次构成。给定的字符串只含有小写英文字母，并且长度不超过10000。
# 示例 1:
# 输入: "abab"
# 输出: True
# 解释: 可由子字符串 "ab" 重复两次构成。
# 示例 2:
# 输入: "aba"
# 输出: False
# 示例 3:
# 输入: "abcabcabcabc"
# 输出: True
# 解释: 可由子字符串 "abc" 重复四次构成。 (或者子字符串 "abcabc" 重复两次构成。)


# kmp算法中next数组为什么遇到字符不匹配的时候可以找到上一个匹配过的位置继续匹配，开始是有计算好的前缀表。
# 前缀表里，统计了各个位置为中点字符串的最长相同前后最的长度。
# 那么 最长相同前后缀和重复子串的关系又有什么关系呢。
# 可能很多录友又忘了 前缀和后缀的定义，再回顾一下：
# 前缀是指不包含最后一个字符的所有以第一个字符开头的连续子串；
# 后缀是指不包含第一个字符的所有以最后一个字符结尾的连续子串


# 移动匹配
def repeatedSubstringPattern(s):
    if len(s) <= 1:
        return False
    ss = s + s
    ss = ss[1:-1]
    # if s in ss:
    #     return True
    # else:
    #     return False
    return ss.find(s) != -1


# 暴力法
def repeatedSubstringPattern2(s):
    if len(s) <= 1:
        return False
    n = len(s)
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            substr = s[:i]
            if substr * (n // i) == s:
                return True
    return False


# KMP算法
class Solution:
    def get_next(self, nxt, s):
        j = 0  # 前缀子串末尾位置
        nxt[0] = 0
        for i in range(1, len(s)):  # i:后缀子串开始位置
            while s[j] != s[i] and j > 0:
                j = nxt[j - 1]
            if s[j] == s[i]:
                j += 1
            nxt[i] = j
        return nxt

    def repeatedSubstringPattern(self, s):
        if len(s) == 0:
            return False
        nxt = [0] * len(s)
        self.get_next(nxt, s)

        if nxt[-1] != 0 and len(s) % (len(s) - nxt[-1]) == 0:
            return True
        return False


class S:

    def get_next(self, nxt, s):
        j = 0
        nxt[0] = 0
        for i in range(1, len(s)):
            while s[i] != s[j] and j > 0:  # 不相等时，j往回退，退到前一个j指向的next位置。直到相等为止。
                j = nxt[j - 1]
            if s[i] == s[j]:
                j += 1
            nxt[i] = j

    def repeated_substr(self, s):
        nxt = [0] * len(s)
        self.get_next(nxt, s)

        # 当s = "abcabcabc", 则next=[0,0,0,1,2,3,4,5,6]
        # next数组最后一个数=0，则说明s数组不是全部由相同子串组成
        # len(s)能被（len(s)-nxt[-1]）整除，则 len(s)-nxt[-1] 就是最小子串的长度。
        # 反过来讲，如果s符合题意，len(最小子串) = len(s)-nxt[-1]，len(s)必须要能被len(最小子串)整除。
        if nxt[-1] != 0 and len(s) % (len(s)-nxt[-1]) == 0:
            return True
        return False


if __name__ == '__main__':
    s = "abcabccbcabcabc"
    # a = repeatedSubstringPattern2(s)
    # print(a)

    a = S().repeated_substr(s)
    print(a)
