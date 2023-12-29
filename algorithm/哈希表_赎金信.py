#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/12/22 15:48
# @Author   : yuanyuan
# @File     : 哈希表_赎金信.py
# LastEditTime:


# 给定一个赎金信 (ransom) 字符串和一个杂志(magazine)字符串，判断第一个字符串 ransom 能不能由第二个字符串 magazines 里面的字符构成。如果可以构成，返回 true ；否则返回 false。
# (题目说明：为了不暴露赎金信字迹，要从杂志上搜索各个需要的字母，组成单词来表达意思。杂志字符串中的每个字符只能在赎金信字符串中使用一次。)
# 注意：
# 你可以假设两个字符串均只含有小写字母。
#
# canConstruct("a", "b") -> false
# canConstruct("aa", "ab") -> false
# canConstruct("aa", "aab") -> true


from collections import Counter, defaultdict


class Solution:

    def canConstruct(self, ransom, magazine):
        r_count = Counter(ransom)
        m_count = Counter(magazine)

        record = []
        for k, v in r_count.items():
            value = m_count.get(k, 0)
            record.append(value) if value >= v else record.append(0)

        return all(record)


def can_construct(ransom, magazine):
    ransom_count = [0] * 26
    magazine_count = [0] * 26

    for r in ransom:
        ransom_count[ord(r) - ord("a")] += 1
    for m in magazine:
        magazine_count[ord(m) - ord("a")] += 1

    return all(ransom_count[i] <= magazine_count[i] for i in range(26))


def can_construct2(ransom, magazine):
    hashmap = defaultdict(int)
    for i in magazine:
        hashmap[i] += 1

    for j in ransom:
        value = hashmap.get(j)
        if not value:
            return False
        else:
            hashmap[j] -= 1
    return True

    # if hashmap.get(j, 0) <= 0:
    #     return False
    # if j in hashmap:
    #     hashmap[j] -= 1
    # else:
    #     return False


def can_construct3(ransomNote: str, magazine: str) -> bool:
    return not Counter(ransomNote) - Counter(magazine)


def can_construct4(ransomNote: str, magazine: str) -> bool:
    return all(ransomNote.count(c) <= magazine.count(c) for c in set(ransomNote))


if __name__ == '__main__':
    ran = "aa"
    ma = "ab"
    # ran = "aa"
    # ma = "aab"
    ran = "a"
    ma = "b"
    # s = Solution().canConstruct(ran, ma)
    # print(s)

    res = can_construct3(ran, ma)
    print(res)
