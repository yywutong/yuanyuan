#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/12/29 11:47
# @Author   : yuanyuan
# @File     : 哈希表_四数之和.py
# LastEditTime:


# 题意：给定一个包含 n 个整数的数组 nums 和一个目标值 target，判断 nums 中是否存在四个元素 a，b，c 和 d ，
# 使得 a + b + c + d 的值与 target 相等？找出所有满足条件且不重复的四元组。
# 注意：
# 答案中不可以包含重复的四元组。
#
# 示例： 给定数组 nums = [1, 0, -1, 0, -2, 2]，和 target = 0。
# 满足要求的四元组集合为： [ [-1, 0, 0, 1], [-2, -1, 1, 2], [-2, 0, 0, 2] ]


def four_sum(nums, target):
    nums.sort()

    result = []
    s = set()
    for i in range(len(nums)):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        for j in range(i + 1, len(nums)):
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue
            for k in range(j + 1, len(nums)):
                if k > j + 1 and nums[k] == nums[k - 1]:
                    continue
                if k < len(nums) - 1:
                    s.add(nums[k + 1])
                l = target - (nums[i] + nums[j] + nums[k])
                if l in s:
                    result.append([nums[i], nums[j], nums[k], l])
                    s.pop()
    return result


def four_sum2(nums, target):
    nums.sort()
    result = []

    for i in range(len(nums)):
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        for j in range(i + 1, len(nums)):
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue

            left = j + 1
            right = len(nums) - 1

            while left < right:
                sum_ = nums[i] + nums[j] + nums[left] + nums[right]
                if sum_ > target:
                    right -= 1
                elif sum_ < target:
                    left += 1
                else:
                    result.append([nums[i], nums[j], nums[left], nums[right]])
                    right -= 1
                    left += 1

                    while j + 1 < left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right < len(nums) - 1 and nums[right] == nums[right + 1]:
                        right -= 1
    return result


if __name__ == '__main__':
    n = [1, 0, -1, 0, -2, 2]
    f = four_sum2(n, 0)
    print(f)
