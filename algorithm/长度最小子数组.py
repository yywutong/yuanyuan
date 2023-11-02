#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/9/26 18:07
# @Author   : yuanyuan
# @File     : 长度最小子数组.py
# LastEditTime:

# 209
# 给定一个含有n个正整数的数组和一个正整数target 。
# 找出该数组中满足其总和大于等于target的长度最小的连续子数组[numsl, numsl + 1, ..., numsr - 1, numsr] ，
# 并返回其长度。如果不存在符合条件的子数组，返回0 。
"""
# 示例1：
# 输入：target = 7, nums = [2, 3, 1, 2, 4, 3]
# 输出：2
# 解释：子数组[4, 3]
# 是该条件下的长度最小的子数组。

# 示例2：
# 输入：target = 4, nums = [1, 4, 4]
# 输出：1

# 示例3：
# 输入：target = 11, nums = [1, 1, 1, 1, 1, 1, 1, 1]
# 输出：0
"""


# 双指针，滑窗原理


class Solution:
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        temp_len = []  # 有效数组长度
        sum_num = 0  # 滑窗数值之和
        i = 0  # 滑窗起始位置

        for j in range(len(nums)):  # 遍历结束位置，
            sum_num += nums[j]

            while sum_num >= target:
                temp_len.append(j - i + 1)
                sum_num -= nums[i]  # 当滑窗数值之和> target时，将i往后移，再将往后移之后的数值与target对比。
                i += 1

        return min(temp_len) if len(temp_len) else 0


class S:
    def mmm(self, target: int, nums: list[int]) -> int:
        i, j = 0, 0
        sum_num = 0
        target_len = []

        while i < len(nums) and j < len(nums):
            sum_num += nums[j]

            while sum_num >= target:
                target_len.append(j-i+1)
                sum_num -= nums[i]
                i += 1

            j += 1

        return min(target_len) if len(target_len) else 0


if __name__ == '__main__':
    target = 7
    nums = [2, 3, 1, 2, 4, 3]  # 2
    # target = 4
    # nums = [1, 4, 4]  # 1
    # target = 11
    # nums = [1, 1, 1, 1, 1, 1, 1, 1]  # 0
    s = Solution().minSubArrayLen(target=target, nums=nums)
    print(s)


