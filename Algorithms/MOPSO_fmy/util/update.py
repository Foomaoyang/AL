# encoding: utf-8
import numpy as np

from util import NDsort


def update_v(v, v_min, v_max, pop, pop_pbest, pop_gbest):
    """
    速度更新公式
    :param v: 粒子pop[i]的上一代速度
    :param v_min: 粒子速度下界
    :param v_max: 粒子速度上界
    :param pop: 粒子pop[i]的位置
    :param pop_pbest: 局部最优粒子位置
    :param pop_gbest: 全局最优粒子位置
    :return: 粒子pop[i]的新速度
    """
    # 更新速度
    # 惯性系数 w
    w = 0.4
    num_pop, dim = v.shape
    r1 = np.tile(np.random.rand(num_pop, 1), (1, dim))
    r2 = np.tile(np.random.rand(num_pop, 1), (1, dim))
    # 更新速度 公式
    v = w * v + r1 * (pop_pbest - pop) + r2 * (pop_gbest - pop)
    # 速度边界处理 列向量
    upper = np.tile(v_max, (num_pop, 1))
    lower = np.tile(v_min, (num_pop, 1))
    v = np.maximum(np.minimum(upper, v), lower)  # v不存在上下限，因此是否有必要进行限制
    return v


def update_pop(pop, v, pop_min, pop_max):
    """
    粒子位置更新公式
    :param pop:粒子pop[i]
    :param v: 粒子pop[i]的新速度
    :param pop_min: 粒子位置下界
    :param pop_max: 粒子位置上界
    :return: 粒子pop[i]的新位置
    """
    num_pop, dim = pop.shape
    # 更新位置
    pop = pop + v
    # 越界处理
    upper = np.tile(pop_max, (num_pop, 1))
    lower = np.tile(pop_min, (num_pop, 1))
    pop = np.maximum(np.minimum(upper, pop), lower)
    return pop


def update_pbest(pop, fitness, in_pbest, out_pbest):
    # TODO
    # in_pbest ???
    # out_pbest ???
    temp = out_pbest - fitness
    # np.any() 判定给定的可迭代参数是否全部为False，如果有一个True，则返回True
    # np.int64(False) 0; np.int64(True) 1.
    dominate = np.int64(np.any(temp < 0, axis=1)) - np.int64(np.any(temp > 0, axis=1))

    # out_pbest 全部大于 fitness
    remained_1 = dominate == -1
    out_pbest[remained_1] = fitness[remained_1]
    in_pbest[remained_1] = pop[remained_1]

    #
    remained_2 = dominate == 0
    remained_temp_rand = np.random.rand(len(dominate), ) < 0.5
    remained_final = remained_2 & remained_temp_rand
    out_pbest[remained_final] = fitness[remained_final]
    in_pbest[remained_final] = pop[remained_final]
    return in_pbest, out_pbest


def update_archive(pop, fit, archive_pop, archive_fitness, threshold, grid):
    """
    更新档案
    :param pop: 种群
    :param fit: fitness
    :param archive_pop: 档案中有的粒子
    :param archive_fitness: 档案中保存的fitness
    :param threshold: 档案数量的限制
    :param grid: 网格等分数量
    :return: 档案保存的粒子和fitness
    """
    # 首先，计算当前粒子群的pareto边界，将边界粒子加入到存档archiving中
    # 沿方向堆叠矩阵，两个矩阵拼一起，注意维度一致
    # archive_pop是存档旧解 pop是新解 组成新的种群
    pop = np.vstack((archive_pop, pop))
    fit = np.vstack((archive_fitness, fit))

    # 非劣解排序 numpy.ndarray
    front_index = NDsort.NDSort(fit, pop.shape[0])[0] == 1
    # 列转行
    front_index = np.reshape(front_index, (-1,))
    # 挑出排序是True的解，取出新解pop和fitness的值
    archive_pop = pop[front_index]
    archive_fitness = fit[front_index]

    # 上一步所挑出存档解的个数
    if archive_pop.shape[0] > threshold:
        # 剔除超出存档数量的解
        del_index = Delete(archive_fitness, archive_pop.shape[0] - threshold, grid)
        # numpy.delete(arr, obj, axis)
        archive_pop = np.delete(archive_pop, del_index, 0)
        archive_fitness = np.delete(archive_fitness, del_index, 0)
    return archive_pop, archive_fitness


def Delete(arr, num, num_grid):
    rows = arr.shape[0]
    # %% Calculate the grid location of each solution
    upper, lower = np.max(arr, axis=0), np.min(arr, axis=0)
    # 获得网格间隔距离
    div = (upper - lower) / num_grid
    lower = np.tile(lower, (rows, 1))
    div = np.tile(div, (rows, 1))
    # 根据距离计算在哪个网格中
    # numpy.floor 向下取整
    grid_loc = np.floor((arr - lower) / div)
    grid_loc[grid_loc >= num_grid] = num_grid - 1
    # numpy.isnan 判断是否空值
    grid_loc[np.isnan(grid_loc)] = 0

    # Detect the grid of each solution belongs to
    # numpy.unique()去除重复元素，并按照由大到小返回一个新列表
    # return_index=True 表示返回新列表元素在旧列表中的位置
    # TODO site是什么
    _, _, site = np.unique(grid_loc, return_index=True, return_inverse=True, axis=0)
    # Calculate the crowd degree of each grid
    dist_crowd_grid = np.histogram(site, np.max(site) + 1)[0]
    del_index = np.zeros(rows, ) == 1
    while np.sum(del_index) < num:
        # 输出满足条件的坐标
        max_grid = np.where(dist_crowd_grid == max(dist_crowd_grid))[0]
        temp = np.random.randint(0, len(max_grid))
        grid = max_grid[temp]

        in_grid = np.where(site == grid)[0]

        temp = np.random.randint(0, len(in_grid))
        p = in_grid[temp]
        del_index[p] = True
        site[p] = -100
        dist_crowd_grid[grid] = dist_crowd_grid[grid] - 1

    return np.where(del_index == 1)[0]


def update_gbest(archive_pop, archiving_fit, num_grid, pop):
    rows = archive_pop.shape[0]
    # %% Calculate the grid location of each solution
    upper, lower = np.max(archive_pop, axis=0), np.min(archive_pop, axis=0)
    # 获得网格间隔距离
    div = (upper - lower) / num_grid
    lower = np.tile(lower, (rows, 1))
    div = np.tile(div, (rows, 1))
    # 根据距离计算在哪个网格中
    # numpy.floor 向下取整
    grid_loc = np.floor((archive_pop - lower) / div)
    grid_loc[grid_loc >= num_grid] = num_grid - 1
    # numpy.isnan 判断是否空值
    grid_loc[np.isnan(grid_loc)] = 0

    # Detect the grid of each solution belongs to
    # numpy.unique()去除重复元素，并按照由大到小返回一个新列表
    # return_index=True 表示返回新列表元素在旧列表中的位置
    # TODO site是什么
    _, _, site = np.unique(grid_loc, return_index=True, return_inverse=True, axis=0)
    # Calculate the crowd degree of each grid
    dist_crowd_grid = np.histogram(site, np.max(site) + 1)[0]

    #  Roulette-wheel 1/Fitnessselection
    the_grid = roulette_wheel_selection(pop, dist_crowd_grid)

    ReP = np.zeros(pop, )
    for i in range(pop):
        InGrid = np.where(site == the_grid[i])[0]
        temp = np.random.randint(0, len(InGrid))
        ReP[i] = InGrid[temp]
    ReP = np.int64(ReP)
    return archive_pop[ReP], archiving_fit[ReP]


def roulette_wheel_selection(size, fit):
    """
    轮盘赌选择算法
    :param size: 种群大小
    :param fit:
    :return:
    """
    # 轮盘赌选择算法
    # 基本思想是各个个体被选中的概率与其适应度大小成正比
    # 这段程序不是标准轮盘赌算法
    # 传入的fit值全为1，个数不定
    # numpy.reshape() -1：行数自动给定
    fit = np.reshape(fit, (-1,))
    fit = fit + np.minimum(np.min(fit), 0)
    # numpy.cumsum() 将数组当做一维数组累加
    fit = np.cumsum(1 / fit)
    fit = fit / np.max(fit)
    # n行1列随机数,fit是1行多列，两者比较得到矩阵，矩阵元素是0或1
    # 使用0值表示沿着每一列或行标签\索引值向下执行方法
    # 使用1值表示沿着每一行或者列标签模向执行对应的方法
    index = np.sum(np.int64(~(np.random.rand(size, 1) < fit)), axis=1)
    return index
