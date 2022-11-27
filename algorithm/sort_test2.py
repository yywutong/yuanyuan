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
    _quick_sort2(li, 0, len(li) - 1)


def sift(li, low, high):
    """
    调整函数
    :param li: 列表
    :param low: 堆的根节点位置
    :param high: 堆的最后一个堆元素的位置
    :return:
    """
    i = low  # i开始指向根节点位置
    j = 2 * i + 1  # j开始指向左孩子
    temp = li[low]  # 把堆顶元素暂存起来
    while j <= high:  # j的位置有数
        if j + 1 <= high and li[j + 1] > li[j]:  # 如果右孩子存在 且右孩子比左孩子大。 使用if li[j+1]:来判断右孩子是否存在会下标越界。
            j = j + 1      # 则j指向右孩子
        if li[j] > temp:   # 如果大的孩子比堆顶大
            li[i] = li[j]  # 则将大的孩子放在i（堆顶）位置。 不能使用li[low] = li[j] 因为循环过程中，堆顶会变
            i = j          # i再向下移动一层，继续下一个循环使用
            j = 2 * i + 1  # j重新指向左孩子，继续下一个循环使用
        else:  # 如果对顶更大
            li[i] = temp  # 则将temp在某一级领导位置上。
            break
    else:
        li[i] = temp  # 把temp放到叶子节点上。


def heap_sort(li):
    n = len(li)
    # 从孩子找父亲：(j-1)//2。len(li)-1是最后一个元素的位置，则(len(li)-2)//2是他父亲的位置。
    for i in range((n - 2) // 2, -1, -1):  # 遍历堆顶的位置，反向遍历，遍历到0
        sift(li, i, n - 1)
    for i in range(n - 1, -1, -1):   # i一直指向堆的最后一个位置。
        li[0], li[i] = li[i], li[0]  # 对顶元素和堆的最后一个元素调换位置。
        sift(li, 0, i - 1)   # i-1是新的high，每次调整后堆的最后一个元素往前移一个。


if __name__ == '__main__':
    li = list(range(100))
    random.shuffle(li)  # 将列表顺序打乱
    # quick_sort2(li)
    # print(li)

    heap_sort(li)
    print(li)
