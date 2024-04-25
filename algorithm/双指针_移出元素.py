#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/1/31 17:31
# @Author   : yuanyuan
# @File     : 双指针_移出元素.py
# LastEditTime:

# 给你一个数组 nums 和一个值 val，你需要 原地 移除所有数值等于 val 的元素，并返回移除后数组的新长度。

# 不要使用额外的数组空间，你必须仅使用 O(1) 额外空间并原地修改输入数组。
# 元素的顺序可以改变。你不需要考虑数组中超出新长度后面的元素。
# 示例 1: 给定 nums = [3,2,2,3], val = 3, 函数应该返回新的长度 2, 并且 nums 中的前两个元素均为 2。 你不需要考虑数组中超出新长度后面的元素。
# 示例 2: 给定 nums = [0,1,2,2,3,0,4,2], val = 2, 函数应该返回新的长度 5, 并且 nums 中的前五个元素为 0, 1, 3, 0, 4。


def delete_val(nums, val):
    i = 0
    j = 0
    while j < len(nums):
        if nums[j] != val:
            nums[i] = nums[j]
            i += 1
        j += 1

    return i


def remove_element(nums, val):
    i = 0
    for num in nums:
        if num != val:
            nums[i] = num
            i += 1
    return i


# 暴力
def remove_element2(nums, val):
    i = 0
    l = len(nums)

    while i < l:
        if nums[i] == val:
            for j in range(i + 1, l):
                nums[j - 1] = nums[j]
            i -= 1  # 后一位移过来的数可能是不需要的数据，所以需要重新判断一下。
            l -= 1  # 新数组长度
        i += 1
        print(nums)
    return l


if __name__ == '__main__':
    n = [0, 1, 2, 2, 2, 3, 0, 4, 2]
    v = 2
    # a = delete_val(n, v)
    # print(a)
    # new_length = remove_element(n, v)
    # print(new_length)

    a = remove_element2(n, v)
    print(a)
