#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/2/20 16:21
# @Author   : yuanyuan
# @File     : 双指针_三数之和.py
# LastEditTime:

# 给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有满足条件且不重复的三元组。
# 注意： 答案中不可以包含重复的三元组。

# 示例：
# 给定数组 nums = [-1, 0, 1, 2, -1, -4]，
# 满足要求的三元组集合为： [ [-1, 0, 1], [-1, -1, 2] ]

def three_sum(nums):
    li = []
    nums = sorted(nums)

    for idx, num in enumerate(nums):
        if idx > 0 and nums[idx - 1] == nums[idx]:  # 去重
            continue
        i = idx + 1
        j = len(nums) - 1
        while i < j:
            if nums[i] + nums[j] + num > 0 and i < j:
                j -= 1
            elif nums[i] + nums[j] + num < 0 and i < j:
                i += 1
            else:
                li.append([num, nums[i], nums[j]])

                while i < j and nums[i] == nums[i + 1]:  # 去重
                    i += 1
                while i < j and nums[j] == nums[j - 1]:
                    j -= 1

                i += 1
                j -= 1
    return li


n = [-1, 0, 1, 2, -1, -4, 2, 2, 2, 2, 4]
l = three_sum(n)
print(l)
