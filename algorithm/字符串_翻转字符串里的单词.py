#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/1/12 17:37
# @Author   : yuanyuan
# @File     : 字符串_翻转字符串里的单词.py
# LastEditTime:


# 给定一个字符串，逐个翻转字符串中的每个单词。
#
# 示例 1：
# 输入: "the sky is blue"
# 输出: "blue is sky the"
#
# 示例 2：
# 输入: "  hello world!  "
# 输出: "world! hello"
# 解释: 输入字符串可以在前面或者后面包含多余的空格，但是反转后的字符不能包括。
#
# 示例 3：
# 输入: "a good   example"
# 输出: "example good a"
# 解释: 如果两个单词间有多余的空格，将反转后单词间的空格减少到只含一个。


class Solution:
    def reverseWords(self, s: str) -> str:
        # 将字符串拆分为单词，即转换成列表类型
        words = s.split()

        # 反转单词
        left, right = 0, len(words) - 1
        while left < right:
            words[left], words[right] = words[right], words[left]
            left += 1
            right -= 1

        # 将列表转换成字符串
        return " ".join(words)


def reverse_words1(s):
    s = s.split()
    s = s[::-1]
    return " ".join(s)


def reverse_words2(s):
    s = s.split()
    left = 0
    right = len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    return " ".join(s)


def reverse_words(s):  # 自己写的太繁琐了
    s = list(s[::-1])

    left = right = 0
    flag = 0
    while right < len(s):
        if s[left] == s[right] == " " and left == 0:
            right += 1
            continue
        if s[right] != " ":
            s[left] = s[right]
            left += 1
            right += 1
        elif s[right] == " " and s[left - 1] != " ":
            s[left] = " "
            s[flag: left] = s[flag: left][::-1]
            flag = left + 1
            left += 1
            right += 1
        else:
            right += 1
    s = "".join(s[0: left - 1])
    return s[0: left - 1]


if __name__ == '__main__':
    s = "  a good   example  "
    ss = reverse_words2(s)
    print(ss)

    # ss = Solution().reverseWords(s)
    # print(ss)
