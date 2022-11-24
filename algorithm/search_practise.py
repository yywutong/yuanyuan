
# 顺序查找-效率低
# 内置列表中的index()就是顺序查找。
def linear_search(li, val):
    for ind, v in enumerate(li):
        if v == val:
            return li[ind]


# 二分查找-效率高。只对有序列表有用。
# 思路：取一个中间值将一个列表分为2段，当要查找的值等于中间值时return，否则继续拆分。
def binary_search(li, val):
    left = 0
    right = len(li) - 1

    while right >= left:
        mid = (left + right) // 2
        print(li[mid])
        if li[mid] == val:
            return True
        elif li[mid] < val:  # val 在mid左边
            left = mid + 1
        else:  # val 在mid右边
            right = mid - 1
    else:
        return None


#

