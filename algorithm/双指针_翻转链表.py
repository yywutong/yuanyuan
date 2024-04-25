#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/2/19 16:01
# @Author   : yuanyuan
# @File     : 双指针_翻转链表.py
# LastEditTime:


# 题意：反转一个单链表。
# 示例: 输入: 1->2->3->4->5->NULL 输出: 5->4->3->2->1->NULL

class Solution:  # 不会链表
    def reverseList(self, head: ListNode) -> ListNode:
        cur = head
        pre = None
        while cur:
            temp = cur.next # 保存一下 cur的下一个节点，因为接下来要改变cur->next
            cur.next = pre #反转
            #更新pre、cur指针
            pre = cur
            cur = temp
        return pre


