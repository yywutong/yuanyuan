#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/10/24 18:48
# @Author   : yuanyuan
# @File     : 螺旋矩阵.py
# LastEditTime:


class Solution:
    def generateMatrix(self, n: int) -> list[list[int]]:
        nums = [[0] * n for _ in range(n)]
        start_x, start_y = 0, 0  # 起始位置坐标
        loop, mid = n // 2, n // 2  # 循环几圈，中心点位置
        count = 1  # 计数

        for offset in range(1, loop + 1):
            for i in range(start_y, n - offset):
                nums[start_x][i] = count
                count += 1

            for i in range(start_x, n - offset):
                nums[i][n - offset] = count
                count += 1

            for i in range(n - offset, start_y, -1):
                nums[n - offset][i] = count
                count += 1

            for i in range(n - offset, start_x, -1):
                nums[i][start_y] = count
                count += 1

            start_x += 1
            start_y += 1

        if n % 2 != 0:
            nums[mid][mid] = count

        return nums


class S:
    def generateMatrix(self, n: int) -> list[list[int]]:
        nums = [[0] * n for _ in range(n)]
        startx, starty = 0, 0
        loop, mid = n // 2, n // 2
        count = 1

        for offset in range(1, loop + 1):
            for i in range(startx, n - offset):
                nums[startx][i] = count
                count += 1
            for i in range(startx, n - offset):
                nums[i][n - offset] = count
                count += 1
            for i in range(n - offset, startx, -1):
                nums[n - offset][i] = count
                count += 1
            for i in range(n - offset, starty, -1):
                nums[i][starty] = count
                count += 1
            startx += 1
            starty += 1

        if n % 2 != 0:
            nums[mid][mid] = count
        return nums


if __name__ == '__main__':
    n = 5
    s = S().generateMatrix(n)
    print(s)


    # for i in range(4, 0, -1):
    #     print(i)