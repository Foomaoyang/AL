import numpy as np

dim = 4
bound = [0, 1]


def Func(x):
    if x.shape[0] < 2:
        return -1
    return [f1(x), f2(g(x), x)]


def f1(x):
    return x[0]


def f2(gx, x):
    return gx * (1 - (x[0] / gx)**2)


def g(x):
    g = 1 + 9 * (np.sum(x[1:], axis=0) / (x.shape[0] - 1))
    return g
