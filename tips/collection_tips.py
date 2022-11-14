from collections import Counter

# 统计一个列表中出现次数大于1半的数据。
# from collections import Counter，转换为字典，value为出现的次数。
a = [1, 3, 2, 3, 3, 1, 3, 3]
b = Counter(a)
b1 = dict(b)
for k, v in b1.items():
    if v >= len(a) / 2:
        print(k)
