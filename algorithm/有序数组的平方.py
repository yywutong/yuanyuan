#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 给你一个按 非递减顺序 排序的整数数组 nums，返回 每个数字的平方 组成的新数组，要求也按 非递减顺序 排序。
"""
示例 1：
输入：nums = [-4,-1,0,3,10]
输出：[0,1,9,16,100]
解释：平方后，数组变为 [16,1,0,9,100]
排序后，数组变为 [0,1,9,16,100]
示例 2：
输入：nums = [-7,-3,2,3,11]
输出：[4,9,9,49,121]
"""


# 双指针
# 非递减数组 两侧数乘积大于中间，所以从两侧开始遍历，乘积大的数放在新数组的最后。

class Solution:
    def sortedSquares(self, nums: list[int]) -> list[int]:
        new_nums = [0] * len(nums)  # 需要提前定义列表，存放结果
        k = len(nums) - 1
        i = 0
        j = len(nums) - 1
        while j >= i:
            if nums[j] ** 2 > nums[i] ** 2:
                # new_nums.append(nums[j] * nums[j])
                new_nums[k] = nums[j] ** 2
                k -= 1
                j -= 1
            else:
                # new_nums.append(nums[i] * nums[i])
                new_nums[k] = nums[i] ** 2
                k -= 1
                i += 1
        return new_nums


if __name__ == '__main__':
    nums = [-4, -1, 0, 3, 10]
    # nums = [-7, -3, 2, 3, 11]
    # s = Solution().sortedSquares(nums)
    # print(s)

    print([0] * len(nums))
