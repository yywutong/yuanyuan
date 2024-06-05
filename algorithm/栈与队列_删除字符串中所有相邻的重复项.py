#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/5/13 14:33
# @Author   : yuanyuan
# @File     : 栈与队列_删除字符串中所有相邻的重复项.py
# LastEditTime:


# 给出由小写字母组成的字符串 S，重复项删除操作会选择两个相邻且相同的字母，并删除它们。
# 在 S 上反复执行重复项删除操作，直到无法继续删除。
# 在完成所有重复项删除操作后返回最终的字符串。答案保证唯一。

# 示例：
# 输入："abbaca"
# 输出："ca"
# 解释：例如，在 "abbaca" 中，我们可以删除 "bb" 由于两字母相邻且相同，这是此时唯一可以执行删除操作的重复项。之后我们得到字符串 "aaca"，
# 其中又只有 "aa" 可以执行重复项删除操作，所以最后的字符串为 "ca"。
# 提示：
# 1 <= S.length <= 20000
# S 仅由小写英文字母组成。

def remove_duplicates(s):
    stack = []

    for item in s:
        if stack and item == stack[-1]:
            stack.pop()
        else:
            stack.append(item)

    return "".join(stack)


def remove_duplicates2(s: str):
    slow = 0
    fast = 1
    li = list(s)
    while slow < fast < len(li):
        if li[slow] == li[fast]:
            del li[slow]
            del li[slow]
            if slow > 0:
                slow -= 1
            if fast < len(li):
                fast += 1
        else:
            slow += 1
            fast += 1

    return "".join(li)


if __name__ == '__main__':
    ss = "abbaca"
    res = remove_duplicates2(ss)
    print(res)
