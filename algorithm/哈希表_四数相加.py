#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/12/22 10:25
# @Author   : yuanyuan
# @File     : 哈希表_四数相加.py
# LastEditTime:


# 给定四个包含整数的数组列表 A , B , C , D ,计算有多少个元组 (i, j, k, l) ，使得 A[i] + B[j] + C[k] + D[l] = 0。
# 为了使问题简单化，所有的 A, B, C, D 具有相同的长度 N，且 0 ≤ N ≤ 500 。所有整数的范围在 -2^28 到 2^28 - 1 之间，最终结果不会超过 2^31 - 1 。
#
# 例如:
# 输入:
# A = [ 1, 2]
# B = [-2,-1]
# C = [-1, 2]
# D = [ 0, 2]
# 输出: 2
#
# 解释:
# 两个元组如下:
# (0, 0, 0, 1) -> A[0] + B[0] + C[0] + D[1] = 1 + (-2) + (-1) + 2 = 0
# (1, 1, 0, 0) -> A[1] + B[1] + C[0] + D[0] = 2 + (-1) + (-1) + 0 = 0


class Solution:

    def four_sum_count(self, nums1, nums2, nums3, nums4):
        hashmap = dict()
        for i in nums2:
            for j in nums1:
                hashmap[i + j] = hashmap.get(i + j, 0) + 1

        count = 0
        for k in nums3:
            for l in nums4:
                count += hashmap.get(-k - l, 0)

        return count


from collections import defaultdict


class SS:

    def four_sum_count(self, nums1, nums2, nums3, nums4):
        rec, cnt = defaultdict(lambda: 0), 0
        print(rec)
        for n1 in nums1:
            for n2 in nums2:
                rec[n1+n2] += 1

        for n3 in nums3:
            for n4 in nums4:
                cnt += rec.get(-n3-n4, 0)

        return cnt


if __name__ == '__main__':
    A = [1, 2]
    B = [-2, -1]
    C = [-1, 2]
    D = [0, 2]
    # s = Solution().four_sum_count(A, B, C, D)
    # print(s)

    ss = SS().four_sum_count(A, B, C, D)
    print(ss)

