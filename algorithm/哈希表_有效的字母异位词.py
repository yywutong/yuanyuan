#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/12/20 10:47
# @Author   : yuanyuan
# @File     : 哈希表_有效的字母异位词.py
# LastEditTime:


# 给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词。
#
# 示例 1: 输入: s = "anagram", t = "nagaram" 输出: true
#
# 示例 2: 输入: s = "rat", t = "car" 输出: false
#
# 说明: 你可以假设字符串只包含小写字母。


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        record = [0] * 26
        for i in s:
            ascii_value = ord(i)
            record[ascii_value - 97] += 1
        for j in t:
            ascii_value = ord(j)
            record[ascii_value - 97] -= 1
        if record == [0] * 26:
            return True
        return False


# （没有使用数组作为哈希表，只是介绍defaultdict这样一种解题思路）
class S:
    def isAnagram(self, s: str, t: str) -> bool:
        from collections import defaultdict
        s_dict = defaultdict(int)
        t_dict = defaultdict(int)
        for i in s:
            s_dict[i] += 1
        for j in t:
            t_dict[j] += 1

        return s_dict == t_dict


# 没有使用数组作为哈希表，只是介绍Counter这种更方便的解题思路
class SS:
    def isAnagram(self, s: str, t: str) -> bool:
        from collections import Counter
        s_count = Counter(s)
        t_count = Counter(t)
        return s_count == t_count


if __name__ == '__main__':
    s = "anagram"
    t = "nagaram"
    # s = "rat"
    # t = "car"
    # res = Solution().isAnagram(s, t)
    # print(res)

    # r = S().isAnagram(s, t)
    # print(r)

    rr = SS().isAnagram(s,t)
    print(rr)
