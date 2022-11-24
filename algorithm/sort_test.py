#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/7/28 19:39
# @Author   : yuan yuan

# 电脑的计算速度差不多是1秒完成10^7次计算
# 若对10000个数的列表进行冒泡排序，时间复杂度是O(n^2)，大概估算计算时间是10000*10000/10^7 = 10秒左右。可以验证一下。

# 原地排序


# 冒泡排序
def sort_test(list1: list):
    for i in range(1, len(list1)):
        for j in range(i, 0, -1):
            if list1[j] < list1[j - 1]:
                list1[j], list1[j - 1] = list1[j - 1], list1[j]
    return list1


def bubble_sort(list1: list):
    for i in range(len(list1) - 1):
        flag = 0
        for j in range(len(list1) - i - 1):
            if list1[j] > list1[j + 1]:
                list1[j], list1[j + 1] = list1[j + 1], list1[j]
                flag = 1
        if not flag:  # 当一个循环里面没有位置交换时，就证明排序结束。
            return


# 查找排序简单版
# 每次查找最小值，再按顺序存放
# 时间复杂度O(n^2) 不是O(n^3)，因为查找最小值和删除0（n)+0（n)=0（n)
def search_sort_simple(li):
    li2 = []  # 新的列表，空间复杂度不是最优
    for i in range(len(li) - 1):
        min_var = min(li)  # 找到列表最小值，时间复杂度是O(n)
        li2.append(min_var)
        li.remove(min_var)  # 删除最小的值，时间复杂度是O(n)
    return li2


# 查找一个列表中最小的值，放在首位
# 时间复杂度O(n^2)
def search_sort(li):
    for i in range(len(li) - 1):
        min_loc = i
        for j in range(i + 1, len(li)):
            if li[min_loc] > li[j]:
                min_loc = j
        if min_loc != i:
            li[min_loc], li[i] = li[i], li[min_loc]
    return li


# 插入排序
# 时间复杂度O(n^2)
def insert_sort(li):
    for i in range(1, len(li)):
        tmp = i
        j = i - 1
        while j >= 0 and li[j] > li[tmp]:
            li[j + 1] = li[j]
        li[j] = li[tmp]


# 递归求x的n次方
def s_test1(x, n):
    if n == 0:
        return 1
    else:
        return x * s_test1(x, n - 1)


if __name__ == '__main__':
    list1 = [4, 3, 5, 1, 9, 8, 9, 10, 11]
    insert_sort(list1)
    print(list1)
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
