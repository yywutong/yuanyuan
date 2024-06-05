#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/5/22 19:27
# @Author   : yuanyuan
# @File     : 栈与队列_滑动窗口最大值.py
# LastEditTime:


# 给定一个数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 k 个数字。滑动窗口每次只向右移动一位。
# 返回滑动窗口中的最大值。
# 进阶：
# 你能在线性时间复杂度内解决此题吗？

from collections import deque


class MyQueue:

    def __init__(self):
        self.queue = deque()

    def pop(self, value):
        if self.queue and self.queue[0] == value:
            self.queue.popleft()

    def push(self, value):
        while self.queue and value > self.queue[-1]:
            self.queue.pop()
        self.queue.append(value)

    def front(self):
        return self.queue[0]


class Solution:

    def maxSlidingWindow(self, nums, k):
        que = MyQueue()
        result = []

        for i in range(k):
            que.push(nums[i])
        result.append(que.front())

        for i in range(k, len(nums)):
            que.pop(i - k)
            que.push(i)
            result.append(que.front())

        return result


if __name__ == '__main__':
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    re = Solution().maxSlidingWindow(nums, k)
    print(re)

