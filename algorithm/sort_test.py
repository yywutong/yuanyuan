#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/7/28 19:39
# @Author   : yuan yuan

# 快速排序
def quick_sort(list1: list):
    if len(list1) < 2:
        return list1
    else:
        middle_index = len(list1) // 2
        n = list1[middle_index]
        list2 = quick_sort([i for i in list1 if i < n])
        list3 = quick_sort([i for i in list1 if i > n])

        return list2 + [n] + list3


# 冒泡排序
def sort_test(list1: list):
    for i in range(1, len(list1)):
        for j in range(i, 0, -1):
            if list1[j] < list1[j - 1]:
                list1[j], list1[j - 1] = list1[j - 1], list1[j]
    return list1


# 递归求x的n次方
def s_test1(x, n):
    if n == 0:
        return 1
    else:
        return x * s_test1(x, n - 1)


if __name__ == '__main__':
    list1 = [4, 3, 5, 1, 9, 8, 7, 2, 1]
    list4 = sort_test(list1)
    print(list4)
    # a = sorted(list1)
    # print(a)

# from mmap import mmap
#
#
# def get_lines(fp):
#     with open(fp, "r+") as f:
#         m = mmap(f.fileno(), 0)
#
#     tmp = 0
#     for i, char in enumerate(m):
#         if char == b"\n":
#             yield m[tmp:i + 1].decode()
#         tmp = i + 1
#
#
# if __name__ == "__main__":
#     for i in get_lines("fp_some_huge_file"):
#         print(i)
