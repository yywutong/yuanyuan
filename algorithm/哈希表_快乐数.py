#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/12/20 16:43
# @Author   : yuanyuan
# @File     : 哈希表_快乐数.py
# LastEditTime:


# 编写一个算法来判断一个数 n 是不是快乐数。

# 「快乐数」定义为：对于一个正整数，每一次将该数替换为它每个位置上的数字的平方和，然后重复这个过程直到这个数变为 1，也可能是 无限循环 但始终变不到 1。如果 可以变为  1，那么这个数就是快乐数。
# 如果 n 是快乐数就返回 True ；不是，则返回 False 。
#
# 示例：
# 输入：19
# 输出：true
# 解释：
# 1^2 + 9^2 = 82
# 8^2 + 2^2 = 68
# 6^2 + 8^2 = 100
# 1^2 + 0^2 + 0^2 = 1


class Solution:

    def isHappy(self, n: int) -> bool:
        record = set()
        while n not in record:
            record.add(n)
            n = self.get_sum(n)
            if n == 1:
                return True
            # if n in record:  # 如果中间结果重复出现，说明陷入死循环了，该数不是快乐数
            #     return False
        return False

    def get_sum(self, n):
        sum_n = int()
        while n:
            n, m = divmod(n, 10)  # 商、余数
            sum_n += m ** 2
        return sum_n


def is_happy(n):
    record = set()
    while n not in record:
        record.add(n)
        n = 0
        str_n = str(n)
        for i in str_n:
            n += int(i) ** 2
        if n == 1:
            return True
    return False





if __name__ == '__main__':
    num = 19
    # s = is_happy(num)
    # print(s)

    s = Solution().isHappy(num)
    print(s)
