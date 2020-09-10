import numpy as np


dim = 30
bound = [0, 1]


def Func(x):
    if x.shape[0] < 2:
        return -1
    return [f1, f2(g(x), x)]


def f1(x):
    return x[0]


def f2(gx, x):
    return gx * (1 - np.sqrt(x[0] / gx))


def g(x):
    return 1 + 9 * (np.sum(x[1:], axis=0) / (x.shape[0] - 1))
