#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/12/21 11:08
# @Author   : yuanyuan
# @File     : 哈希表_两数之和.py
# LastEditTime:


# 给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
# 你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。
#
# 示例:
# 给定 nums = [2, 7, 11, 15], target = 9
# 因为 nums[0] + nums[1] = 2 + 7 = 9
# 所以返回 [0, 1]

class Solution:

    def two_sum(self, nums, target):
        n_dict = {}
        for i, n in enumerate(nums):
            if target - n in n_dict:
                return [i, n_dict[target - n]]
            n_dict[n] = i
        return []


class SS:
    def twoSum(self, nums, target):
        left = 0
        right = 1

        while left < right:
            while right < len(nums):
                if nums[left] + nums[right] == target:
                    return [left, right]
                right += 1
            left += 1
            right = left + 1
        return []


if __name__ == '__main__':
    nn = [2, 3, 4, 5]
    t = 9
    # s = Solution().two_sum(nn, t)
    # print(s)

    s = SS().twoSum(nn, t)
    print(s)
