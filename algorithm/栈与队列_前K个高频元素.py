#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/5/27 18:52
# @Author   : yuanyuan
# @File     : 栈与队列_前K个高频元素.py
# LastEditTime:


# 给定一个非空的整数数组，返回其中出现频率前 k 高的元素。
#
# 示例 1:
# 输入: nums = [1,1,1,2,2,3], k = 2
# 输出: [1,2]
# 示例 2:
# 输入: nums = [1], k = 1
# 输出: [1]
# 提示：
# 你可以假设给定的 k 总是合理的，且 1 ≤ k ≤ 数组中不相同的元素的个数。
# 你的算法的时间复杂度必须优于 $O(n \log n)$ , n 是数组的大小。
# 题目数据保证答案唯一，换句话说，数组中前 k 个高频元素的集合是唯一的。
# 你可以按任意顺序返回答案

import heapq
from collections import Counter, defaultdict


def topKFrequent(li, k):
    map_ = {}
    for i in li:
        map_[i] = map_.get(i, 0) + 1

    pri_que = []

    for key, value in map_.items():
        heapq.heappush(pri_que, (value, key))
        if len(pri_que) > k:
            heapq.heappop(pri_que)

    result = [0] * k
    for i in range(k - 1, -1, -1):
        result[i] = heapq.heappop(pri_que)[1]
    return result


def top_k(li, k):
    li = Counter(li)

    heap_li = []

    for key, value in li.items():
        heapq.heappush(heap_li, (value, key))
        if len(heap_li) > k:
            heapq.heappop(heap_li)

    result = []
    for i in range(k - 1, -1, -1):
        result.append(heap_li[i][1])

    return result


class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        # 使用字典统计数字出现次数
        time_dict = defaultdict(int)
        for num in nums:
            time_dict[num] += 1
        # 更改字典，key为出现次数，value为相应的数字的集合
        index_dict = defaultdict(list)
        for key in time_dict:
            index_dict[time_dict[key]].append(key)
        # 排序
        key = list(index_dict.keys())
        key.sort()
        result = []
        cnt = 0
        # 获取前k项
        while key and cnt != k:
            result += index_dict[key[-1]]
            cnt += len(index_dict[key[-1]])
            key.pop()

        return result[0: k]


if __name__ == '__main__':
    nums = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4]
    n = 2
    # res = topKFrequent(li, k)
    # print(res)

    # res = top_k(nums, n)
    # print(res)

    res = Solution().topKFrequent(nums, n)
    print(res)