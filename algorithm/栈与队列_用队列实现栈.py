#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/6/3 19:16
# @Author   : yuanyuan
# @File     : 栈与队列_用队列实现栈.py
# LastEditTime:

from collections import deque


class MyStack:
    """用2个队列实现"""

    def __init__(self):
        """
        Python普通的Queue或SimpleQueue没有类似于peek的功能
        也无法用索引访问，在实现top的时候较为困难。

        用list可以，但是在使用pop(0)的时候时间复杂度为O(n)
        因此这里使用双向队列，我们保证只执行popleft()和append()，因为deque可以用索引访问，可以实现和peek相似的功能

        que1 - 存所有数据
        que2 - 仅在pop的时候会用到
        """
        self.queue_in = deque()
        self.queue_out = deque()

    def push(self, value):
        self.queue_in.append(value)

    def pop(self):
        """
        1. 首先确认不空
        2. 因为队列的特殊性，FIFO，所以我们只有在pop()的时候才会使用queue_out
        3. 先把queue_in中的所有元素（除了最后一个），依次出列放进queue_out
        4. 交换in和out，此时out里只有一个元素
        5. 把out中的pop出来，即是原队列的最后一个

        tip：这不能像栈实现队列一样，因为另一个queue也是FIFO，如果执行pop()它不能像
        stack一样从另一个pop()，所以干脆in只用来存数据，pop()的时候两个进行交换
        """

        # 写法一：
        # if self.empty():
        #     return None

        # return self.queue_in[-1]    # 这里实际上用到了栈，因为直接获取了queue_in的末尾元素

        # 写法二：
        if self.empy():
            return None
        for i in range(len(self.queue_in) - 1):
            self.queue_out.append(self.queue_in.popleft())

        self.queue_in, self.queue_out = self.queue_out, self.queue_in

        return self.queue_out.pop()

    def top(self):
        res = self.pop()
        if res is not None:
            self.queue_in.append(res)
        return res

    def empy(self):
        return len(self.queue_in) == 0


class MyStack2:
    def __init__(self):
        self.que = deque()

    def push(self, value):
        self.que.append(value)

    def empy(self):
        return len(self.que) == 0

    def pop(self):
        if self.empy():
            return None
        # size = len(self.que) - 1
        for i in range(len(self.que) - 1):
            self.que.append(self.que.popleft())
        self.que.popleft()

    def top(self):
        if self.empy():
            return None
        for i in range(len(self.que) - 1):
            self.que.append(self.que.popleft())
        ele = self.que.popleft()
        self.que.append(ele)
        return ele


if __name__ == '__main__':
    li = [1, 2, 3]
    my_s = MyStack2()
    for i in range(5):
        my_s.push(i)
    print(my_s.que)
    my_s.pop()
    print(my_s.que)
    print(my_s.top())
    print(my_s.empy())
    print(my_s.que)
