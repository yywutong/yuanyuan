# 快速排序
# 这个生成了新列表空间复杂度没那么好
import random
import sys

sys.setrecursionlimit(100000)  # 限制最大递归深度为10万层


def quick_sort(list1: list):
    if len(list1) < 2:
        return list1
    else:
        # middle_index = len(list1) // 2
        # n = list1[middle_index]
        n = list1[0]
        list2 = quick_sort([i for i in list1 if i < n])
        list3 = quick_sort([i for i in list1 if i > n])

        return list2 + [n] + list3


# 快速排序-原地排序
# 倒叙
# 思路：随机取一个值，将列表中小于它的值放在列表左边，大于它的值放在列表右边，它放在中间
# 时间复杂度O(nlogn)。最坏的情况复杂度是O(n^2)但是出现的概率很少。
# 问题：当10000个数正序排列计算成倒叙，1.时间复杂度为O(n^2)，解决方案随机取值，或者先打乱列表。 2.可能会超出最大递归深度。
def partition(li, left, right):
    # tmp_index = random.randint(0,len(li)-1)  # 随机取值
    # tmp = li[tmp_index]
    # li[tmp_index] = li[left]
    tmp = li[left]  # 取左边的值临时存放
    while left < right:
        while li[right] < tmp and left < right:  # li[right]<tmp 则li[right]不用交换位置.因为left right位置是变化的所以需要再次判断left<right
            right -= 1  # right-1 对下一个数据进行对比
        li[left] = li[right]  # 将大于tmp的值放在左边
        while li[left] > tmp and left < right:
            left += 1
        li[right] = li[left]
    li[left] = tmp  # 将临时取的值放回到中间位置
    return left


def _quick_sort2(li, left, right):
    if left < right:
        mid = partition(li, left, right)
        _quick_sort2(li, left, mid - 1)
        _quick_sort2(li, mid + 1, right)


def quick_sort2(li):
    _quick_sort2(li, 0, len(li)-1)


if __name__ == '__main__':

    li = list(range(10000))
    # random.shuffle(li)  # 将列表顺序打乱
    # quick_sort2(li)
    # print(li)

    tmp_index = random.randint(0,len(li)-1)
    print(tmp_index)