from collections import Counter


# 统计一个列表中出现次数大于1半的数据。
# from collections import Counter，转换为字典，value为出现的次数。
def count_test():
    a = [1, 3, 2, 3, 3, 1, 3, 3]
    b = Counter(a)
    b1 = dict(b)
    for k, v in b1.items():
        if v >= len(a) / 2:
            print(k)


# 深拷贝，浅拷贝
# deepcopy是真正意义上的复制，深拷贝，被复制对象完全复制一遍作为独立的新个体，新开辟一块空间。
# 浅拷贝，不会产生独立对象，只是对原有数据块打上新标签，其中一个标签改变，数据块就会变化。
# copy仅拷贝对象本身，浅拷贝不会对其中的子对象进行拷贝，对子对象进行修改也会随着修改
# 对于不可变类型(元组、数值，字符串等)为浅拷贝,对象的id值与浅复制原来的值相同
# 对于可变类型(列表、字典等)为深拷贝，
# 1、复制的对象中无复杂子对象，即列表中不嵌套列表，原来值的改变并不会影响浅复制的值，同时浅复制的值改变也并不会影响原来的值。原来值的id值与浅复制原来的值不同。
# 2、复制的对象中有复杂子对象 （例如列表中的一个子元素是一个列表）如果改变复杂子对象的值（列表中的值）会影响浅复制的值。
def copy_test():
    a = [1, 2, 3, 4, ["a", "b"]]  # id =2812314355072
    b = a  # id =2812314355072
    c = copy.copy(a)  # id =2812314318912
    d = copy.deepcopy(a)  # id =2812314318656

    a.append(5)

    a[4].append("c")

    print(a, id(a))  # [1, 2, 3, 4, ['a', 'b', 'c'], 5]
    print(b, id(b))  # [1, 2, 3, 4, ['a', 'b', 'c'], 5]
    print(c, id(c))  # [1, 2, 3, 4, ['a', 'b', 'c']]
    print(d, id(d))  # [1, 2, 3, 4, ['a', 'b']]

    x = 'Hello World'
    y = x
    z = copy.copy(x)
    w = copy.deepcopy(x)
    print(id(x))  # 4617118576
    print(id(y))  # 4617118576
    print(id(z))  # 4617118576
    print(id(w))  # 4617118576


from time import time


# 时间统计装饰器
def time_cost(func):
    def func_wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        time_spend = end_time - start_time
        print('\n{0} cost time:{1}s\n'.format(func.__name__, time_spend))
        return result

    return func_wrapper


@time_cost
def func():
    i = list(range(1000))
    print(i)
    return i


if __name__ == '__main__':
    # func()
    import copy
