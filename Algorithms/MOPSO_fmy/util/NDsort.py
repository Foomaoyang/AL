import numpy as np
import pytest


def NDSort(fit, pop_size):
    """
    非劣解的层数排序，根据粒子的pareto层数排序
    :param fit: 种群的fitness矩阵
    :param pop_size: 种群大小
    :return: front_pareto pareto前沿粒子的pareto层数； layer_pareto 曲线最大层数
    """
    size_fit, dim = fit.shape
    front_no = np.inf * np.ones((1, size_fit))
    layer_pareto = 0
    # 返回排好序的矩阵和秩
    fit, rank = matrix_sort(fit)
    while np.sum(front_no < np.inf) < pop_size:
        # front_no 初始化为INF，根据fitness判断是非支配解时，将front_no相应位置赋值为max_fno(层数)
        # 当非支配解个数满足时退出while循环
        layer_pareto += 1  # max_fno代表pareto层数，每次循环层数加1,
        for i in range(size_fit):
            if front_no[0, i] == np.inf:
                dominated = False
                for j in range(i - 1, -1, -1):  # 从i-1到0逆序输出
                    if front_no[0, j] == layer_pareto:
                        m = 2
                        while (m <= dim) and (fit[i, m - 1] >= fit[j, m - 1]):
                            # 后边比前边大，m自加
                            m += 1
                        dominated = m > dim
                        if dominated or (dim == 2):
                            break
                if not dominated:
                    front_no[0, i] = layer_pareto  # 非支配关系就赋值max_no层数
    # temp=np.loadtxt("temp.txt")
    # print((front_no==temp).all())
    front_pareto = np.zeros((1, size_fit))
    front_pareto[0, rank] = front_no
    # front_no[0, rank] = front_no 不能这么操作，因为 FrontNO值在发生改变，会影响后续的结果
    return front_pareto, layer_pareto


def matrix_sort(matrix, order="ascend"):
    """
    按行的顺序排序，返回排好的fitness和排序前对应的秩，方便NDSort()函数调用
    :param matrix: 适应度矩阵
    :param order: ascend升序 descend 降序
    :return:matrix_sorted 排好序的fitness; rank fitness排序前对应的秩
    """
    matrix_row = matrix[:, ::-1].T  # 因为np.lexsort() 默认从最后一行对列开始排序，需要将matrix反向并转置
    if order == "ascend":
        rank = np.lexsort(matrix_row)
    elif order == "descend":
        rank = np.lexsort(-matrix_row)
    matrix_sorted = matrix[rank, :]  # Matrix[rank] 也可以
    return matrix_sorted, rank
    # 关于numpy.lexsort()方法的简介如下：
    # 默认先以第一列值大小对行进行排序，若第一列值相同，则按照第二列值，以此类推,返回排序结果及对应索引
    # Reason: list.sort() 仅仅返回 排序后的结果， np.argsort() 需要多次 排序，其中、
    # np.lexsort()的操作对象等同于sortcols ，先排以最后一行对列进行排序，然后以倒数第二列，
    # 以此类推. np.lexsort((d,c,b,a)来对[a,b,c,d]进行排序、其中 a 为一列向量 ）






