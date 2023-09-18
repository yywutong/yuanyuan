# 704。给定一个 n 个元素有序的（升序）整型数组 nums 和一个目标值 target  ，写一个函数搜索 nums 中的 target，如果目标值存在返回下标，否则返回 -1。

# 注意：判断left <= right是否需要=号，left = mid + 1，right = mid - 1是否需要+1 -1，
# 需要看这个数组是开区间还是闭区间，常用的有[],[)。
# [1,1]是成立的，那么left<=right就要加=号，[1,1）是不成立的就不能加=号

class Solution:
    def search(self, nums: list[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1  # 左闭右闭区间，nums[mid]已经被比较一次了，所以新的区间就不需要再把mid加到新的区间里面去比较了。就需要+1
            elif nums[mid] > target:
                right = mid - 1  # 左闭右闭区间同上需要-1。
                # 左闭右开区间，右边是不包含边界值的[left，mid)不包含mid，mid不会被重新比较一次，所以不需要-1。
            else:
                return mid
        return -1


if __name__ == '__main__':
    # nums = [-1,0,3,5,9,12]
    # target = 9

    nums = [-1, 0, 3, 5, 9, 12]
    target = 2
    s = Solution().search(nums=nums, target=target)
    print(s)
