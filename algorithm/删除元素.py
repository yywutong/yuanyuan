# leetcode27
"""
给你一个数组 nums 和一个值 val，你需要 原地 移除所有数值等于 val 的元素，并返回移除后数组的新长度。
不要使用额外的数组空间，你必须仅使用 O(1) 额外空间并 原地 修改输入数组。
元素的顺序可以改变。你不需要考虑数组中超出新长度后面的元素。
"""


# 双指针思想
# 删除元素的底层是原理，后面的元素覆盖前面的元素。

class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != val:
                nums[slow] = nums[fast]
                slow +=1
        return slow  # 慢指针指向的位置就是新数组的长度。


if __name__ == '__main__':
    nums = [0,1,2,2,3,0,4,2]
    val = 2
    s = Solution().removeElement(nums=nums, val=val)
    print(s)
