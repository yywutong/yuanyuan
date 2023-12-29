#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/2 17:52
# @Author   : yuanyuan
# @File     : 快乐数.py
# LastEditTime:


# 编写一个算法来判断一个数 n 是不是快乐数。
#
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


# class Solution:
#     def isHappy(self, n: int) -> bool:
#         num_len = str(n)
#         num_sum = 0
#         if n // 10 >= 1:
#             num_sum += n % 10 ^ 2


# print((23 % 100) // 10)


class Solution:
    def isHappy(self, n: int) -> bool:
        record = set()

        while True:
            n = self.get_sum(n)
            if n == 1:
                return True

            # 如果中间结果重复出现，说明陷入死循环了，该数不是快乐数
            if n in record:
                return False
            else:
                record.add(n)

    def get_sum(self, n: int) -> int:
        new_num = 0
        while n:
            n, r = divmod(n, 10)
            new_num += r ** 2
        return new_num


class S:
    def isHappy(self, n: int) -> bool:
        record = set()
        while n not in record:
            record.add(n)
            new_num = 0
            n_str = str(n)
            for i in n_str:
                new_num += int(i) ** 2
            if new_num == 1:
                return True
            else:
                n = new_num
        return False


if __name__ == '__main__':
    n = 91
    s = Solution().isHappy(n)
    print(s)
