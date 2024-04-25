#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/2/20 17:22
# @Author   : yuanyuan
# @File     : 双指针_四数之和.py
# LastEditTime:

# 题意：给定一个包含 n 个整数的数组 nums 和一个目标值 target，判断 nums 中是否存在四个元素 a，b，c 和 d ，使得 a + b + c + d 的值与 target 相等？找出所有满足条件且不重复的四元组。
# 注意：
# 答案中不可以包含重复的四元组。
# 示例： 给定数组 nums = [1, 0, -1, 0, -2, 2]，和 target = 0。 满足要求的四元组集合为： [ [-1, 0, 0, 1], [-2, -1, 1, 2], [-2, 0, 0, 2] ]


def four_sum(nums, target):
    result = []
    nums.sort()

    for i in range(len(nums)):

        if i > 0 and nums[i] == nums[i - 1]:  # 去重
            continue

        for j in range(i + 1, len(nums)):

            if j < len(nums) - 1 and nums[j] == nums[j - 1]:  # 去重
                continue

            left = j + 1
            right = len(nums) - 1

            while left < right:
                s = nums[i] + nums[j] + nums[left] + nums[right]
                if s > target:
                    right -= 1
                elif s < target:
                    left += 1
                else:
                    result.append([nums[i], nums[j], nums[left], nums[right]])

                    while left < right and nums[left] == nums[left + 1]:  # 去重
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:  # 去重
                        right -= 1

                    left += 1
                    right -= 1
    return result


n = [1, 0, -1, 0, -2, 2]
t = 0
r = four_sum(n, t)
print(r)
