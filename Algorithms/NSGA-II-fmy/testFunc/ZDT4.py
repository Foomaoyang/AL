import numpy as np

# 解的维数
dim = 30
# 解的定义域
bound = [0, 1]


def Func(x):
    """
    ZDT4测试函数
    :param x: 输入的解集
    :return: 返回两个优化目标f1和f2
    """
    if x.shape[0] < 2:
        return -1
    return [f1(x), f2(g(x), x)]


def f1(x):
    return x[0]


def f2(gx, x):
    return gx * (1 - np.sqrt(f1(x) / gx))


def g(x):
    return 1 + 10 * (x.shape[0] - 1) + (np.sum(x[1:] ** 2 - 10 * np.cos(4 * np.pi * x[1:]), axis=0))
