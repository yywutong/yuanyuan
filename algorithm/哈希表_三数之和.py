#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/12/26 12:00
# @Author   : yuanyuan
# @File     : 哈希表_三数之和.py
# LastEditTime:


# 给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有满足条件且不重复的三元组。
# 注意： 答案中不可以包含重复的三元组。
# 示例：
# 给定数组 nums = [-1, 0, 1, 2, -1, -4]，
# 满足要求的三元组集合为： [ [-1, 0, 1], [-1, -1, 2] ]


class Solution:  # 哈希表
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        result = []
        nums.sort()
        # 找出a + b + c = 0
        # a = nums[i], b = nums[j], c = -(a + b)
        for i in range(len(nums)):
            # 排序之后如果第一个元素已经大于零，那么不可能凑成三元组
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i - 1]:  # 三元组元素a去重
                continue
            d = {}
            for j in range(i + 1, len(nums)):
                if j > i + 2 and nums[j] == nums[j - 1] == nums[j - 2]:  # 三元组元素b去重
                    continue
                c = 0 - (nums[i] + nums[j])
                if c in d:
                    result.append([nums[i], nums[j], c])
                    d.pop(c)  # 三元组元素c去重
                else:
                    d[nums[j]] = j
        return result


def three_sum(nums):  # 双指针-复制随想录
    nums.sort()
    result = []
    for i in range(len(nums)):
        left = i + 1
        right = len(nums) - 1

        # 如果第一个元素已经大于0，不需要进一步检查
        if nums[i] > 0:
            return result

        # 跳过相同的元素以避免重复
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        while left < right:
            sum_ = nums[i] + nums[left] + nums[right]
            if sum_ < 0:
                left += 1
            elif sum_ > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])

                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                while left < right and nums[left] == nums[left + 1]:
                    left += 1

                right -= 1
                left += 1

    return result


def three_sum2(nums):  # 双指针自己写的
    nums.sort()

    res = list()
    for i in range(len(nums)):
        if nums[i] > 0:  # 如果第一个元素已经大于0，不需要进一步检查
            return res

        left = i + 1
        right = left + 1
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        while left < right <= len(nums):
            right = left + 1

            if left > i + 1 and nums[left] == nums[left - 1]:
                left += 1
                right = left + 1
                continue

            while left < right < len(nums):
                if right > left + 1 and nums[right] == nums[right - 1]:
                    right += 1
                    continue

                th_sum = nums[i] + nums[left] + nums[right]
                if th_sum > 0:
                    break
                if th_sum == 0 and [nums[i], nums[left], nums[right]] not in res:
                    res.append([nums[i], nums[left], nums[right]])

                right += 1
            left += 1
    return res


def three_sum3(nums):  # 双指针-模仿随想录练习
    nums.sort()
    result = []

    for i in range(len(nums) - 1):
        left = i + 1
        right = len(nums) - 1

        if i > 0 and nums[i] == nums[i - 1]:
            continue

        while left < right:
            sum_ = nums[i] + nums[left] + nums[right]
            if sum_ > 0:
                right -= 1

            elif sum_ < 0:
                left += 1

            else:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1

                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1

    return result


if __name__ == '__main__':
    n = [-1, 0, 0, 1, 2, 2, -4, -1, 1, 0, 6, 9, 10]

    # s = Solution().threeSum(n)
    # print(s)
    #
    # t = three_sum(n)
    # print(t)

    r = three_sum3(n)
    print(r)
