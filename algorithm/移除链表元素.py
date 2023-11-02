#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/10/31 10:39
# @Author   : yuanyuan
# @File     : 移除链表元素.py
# LastEditTime:

# 题意：删除链表中等于给定值 val 的所有节点。
#
# 示例 1： 输入：head = [1,2,6,3,4,5,6], val = 6 输出：[1,2,3,4,5]
# 示例 2： 输入：head = [], val = 1 输出：[]
# 示例 3： 输入：head = [7,7,7,7], val = 7 输出：[]


# （版本一）虚拟头节点法

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# ???
class Solution:
    def removeElements(self, head: ListNode, val: int):
        # 创建虚拟头部节点以简化删除过程
        dummy_head = ListNode(next=head)

        # 遍历列表并删除值为val的节点
        current = dummy_head
        while current.next:
            print(current.next)
            if current.next.val == val:
                current.next = current.next.next
            else:
                current = current.next

        return dummy_head.next


if __name__ == '__main__':
    head = [1, 2, 6, 3, 4, 5, 6]
    val = 6
    # head = []
    # val = 1
    # head = [7, 7, 7, 7]
    # val = 7
    s = Solution().removeElements(head, val)
    print()
