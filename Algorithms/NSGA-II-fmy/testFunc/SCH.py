
dim = 1
bound = [-1000, 1000]


def Func(x):
    return [f1(x), f2(x)]


def f1(x):
    return x[0] ** 2


def f2(x):
    return (x[0] - 2) ** 2
