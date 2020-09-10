import numpy as np


def obj_func(operation, test_func, num_obj, num_particle):
    """
    目标函数
    :param operation:
    :param test_func: 测试问题选择 - 文本格式匹配
    :param num_obj: 多目标函数个数
    :param num_particle: 种群粒子数量
    :return: fitness boundary coding
    """
    [fitness, boundary, coding] = select_func(operation, test_func, num_obj, num_particle)
    if boundary == []:
        return fitness
    else:
        return fitness, boundary, coding


def select_func(operation, test_func, num_obj, num_particle):
    """
    测试函数
    :param operation:
    :param test_func: 测试问题选择 - 文本格式匹配
    :param num_obj: 多目标函数个数
    :param num_particle: 种群粒子数量
    :return:
    """
    boundary = []
    coding = ""
    # 指定测试问题的维数 备选
    k_dimension = [5, 10, 10, 10, 10, 10, 20]

    k_select = k_dimension[0]
    if operation == "init":
        # 决策向量维数 dim
        dim = num_obj + k_select - 1
        MaxValue = np.ones((1, dim))
        MinValue = np.zeros((1, dim))
        # 粒子群种群 解集
        pop = np.random.random((num_particle, dim))
        pop = np.multiply(pop, np.tile(MaxValue, (num_particle, 1))) + np.multiply((1 - pop), np.tile(MinValue, (num_particle, 1)))
        boundary = np.vstack((MaxValue, MinValue))
        coding = "Real"
        return pop, boundary, coding
    elif operation == "value":
        pop = num_particle
        fitness = np.zeros((pop.shape[0], num_obj))
        if test_func == "DTLZ1":
            # g = 100*(k_select+np.sum( (pop[:, M-1:] - 0.5)**2
            # - np.cos(20*np.pi*(pop[:, M-1:] - 0.5)), axis=1, keepdims = True))boundary
            # 约束方程
            g = 100 * (k_select + np.sum(
                (pop[:, num_obj - 1:] - 0.5) ** 2 - np.cos(20 * np.pi * (pop[:, num_obj - 1:] - 0.5)), axis=1))
            for i in range(num_obj):
                # np.prod 矩阵一行元素乘积
                fitness[:, i] = 0.5 * np.multiply(np.prod(pop[:, :num_obj - i - 1], axis=1), (1 + g))
                if i > 0:
                    fitness[:, i] = np.multiply(fitness[:, i], 1 - pop[:, num_obj - i - 1])
        elif test_func == "DTLZ2":
            g = np.sum((pop[:, num_obj - 1:] - 0.5) ** 2, axis=1)
            for i in range(num_obj):
                fitness[:, i] = (1 + g) * np.prod(np.cos(0.5 * np.pi * (pop[:, :num_obj - i - 1])), axis=1)
                if i > 0:
                    fitness[:, i] = np.multiply(fitness[:, i],
                                                      np.sin(0.5 * np.pi * (pop[:, num_obj - i - 1])))

        return fitness, boundary, coding
