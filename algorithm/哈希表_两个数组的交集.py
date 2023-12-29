#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/12/20 14:14
# @Author   : yuanyuan
# @File     : 哈希表_两个数组的交集.py
# LastEditTime:


# 给定两个数组，编写一个函数来计算它们的交集。

# 示例1：
# 输入：nums1 = [1,2,2,1], nums2 = [2,2]
# 输出：[2]
# 示例2：
# 输入：nums1 = [4,9,5], nums2 = [9,4,9,8,4]
# 输出：[9,4]

# 说明：输出结果中的每个元素一定是唯一的。我们可以不考虑输出结果的顺序。


def two_groups_intersection(nums1: list[int], nums2: list[int]):
    return list(set(nums1) & set(nums2))


def intersection2(nums1: list[int], nums2: list[int]):

    set1 = set()
    for i in nums1:
        if i in nums2:
            set1.add(i)
    return list(set1)


class Solution:
    def intersection(self, nums1: list[int], nums2: list[int]) -> list[int]:

        # 使用哈希表存储一个数组中的所有元素
        table = {}
        for num in nums1:
            table[num] = table.get(num, 0) + 1

        # 使用集合存储结果
        res = set()
        for num in nums2:
            if num in table:
                res.add(num)
                del table[num]

        return list(res)


class SS:
    def intersection(self, nums1: list[int], nums2: list[int]) -> list[int]:
        li1 = [0] * 1001
        li2 = [0] * 1001
        result = list()
        for i in nums1:
            li1[i] += 1
        for j in nums2:
            li2[j] += 1
        for k in range(1001):
            if li1[k] != 0 and li2[k] != 0:
                result.append(k)
        return result


if __name__ == '__main__':
    # n1 = [1,2,2,1]
    # n2 = [2,2]
    n1 = [4, 9, 5]
    n2 = [9, 4, 9, 8, 4]
    # res = Solution().intersection(n1, n2)
    # print(res)

    # r = SS().intersection(n1, n2)
    # print(r)

    res = intersection2(n1, n2)
    print(res)

