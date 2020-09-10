# encoding: utf-8

import time
import numpy as np
from util import update, drawCurve, testFunc, NDsort
import memory_profiler as mem

class Mopso:
    def __init__(self, num_pop, max_, min_, threshold, grid_div=10):
        self.__grid = grid_div
        self.__num_pop = num_pop  # 种群粒子数量
        self.__threshold = threshold
        self.__max = max_
        self.__min = min_

        # self.max_v = (max_-min_)*0.5  #速度上限
        # self.min_v = (max_-min_)*(-1)*0.5 #速度下限
        self.__max_v = 100 * np.ones(len(max_), )  # 速度上下限,速度不存在上下限，因此设置很大
        self.__min_v = -100 * np.ones(len(min_), )

        self.__pop = None
        self.__v = None
        self.__fit = None
        self.__pop_pbest = None
        self.__fit_pbest = None
        self.__pop_gbest = None
        self.__fit_gbest = None
        self.__archive_pop = None
        self.__archive_fit = None

        self.__draw = drawCurve.DrawParetoCurve()

    def evaluation_fitness(self):
        self.__fit = testFunc.obj_func("value", "DTLZ2", 2, self.__pop)

    def initialize(self):
        """
        初始化粒子群
        :return:
        """
        # 初始化粒子位置 pop[i]
        # self.__num_pop 粒子群数量
        self.__pop = self.__init_loc(self.__num_pop, self.__max, self.__min)
        # 初始化粒子速度 全0
        self.__v = self.__init_v(self.__num_pop, self.__max_v, self.__min_v)
        # 计算适应度
        self.evaluation_fitness()
        # 初始化个体最优
        # TODO 第二个参数应该是速度？
        self.__pop_pbest, self.__fit_pbest = self.__init_pbest(self.__pop, self.__fit)
        # 初始化外部存档
        self.__archive_pop, self.__archive_fit = self.__init_archive(self.__pop, self.__fit)
        # 初始化全局最优
        self.__pop_gbest, self.__fit_gbest = update.update_gbest(self.__archive_pop, self.__archive_fit, self.__grid,
                                                                 self.__num_pop)

    def update(self):
        """
        更新粒子速度、位置、适应度、个体最优、外部存档、全局最优
        :return:
        """
        self.__v = update.update_v(self.__v, self.__min_v, self.__max_v, self.__pop, self.__pop_pbest, self.__pop_gbest)
        self.__pop = update.update_pop(self.__pop, self.__v, self.__min, self.__max)

        self.evaluation_fitness()

        self.__pop_pbest, self.__fit_pbest = update.update_pbest(self.__pop, self.__fit, self.__pop_pbest,
                                                                 self.__fit_pbest)

        self.__archive_pop, self.__archive_fit = update.update_archive(self.__pop, self.__fit, self.__archive_pop,
                                                                       self.__archive_fit,
                                                                       self.__threshold, self.__grid)

        self.__pop_gbest, self.__fit_gbest = update.update_gbest(self.__archive_pop, self.__archive_fit, self.__grid,
                                                                 self.__num_pop)

    def run(self, iterate):
        # 开始时间戳
        beg = time.time()
        print(f'运行前占用内存：{mem.memory_usage()}')
        self.initialize()
        self.__draw.show(self.__pop, self.__fit, self.__archive_pop, self.__archive_fit, -1)
        for i in range(iterate):
            self.update()  # 更新种群
            # numpy.round() 返回浮点数的四舍五入值
            print('第', i+1, '代已完成，耗费时间: ', np.round(time.time() - beg, 2), "s")
            self.__draw.show(self.__pop, self.__fit, self.__archive_pop, self.__archive_fit, i)
        print(f'运行后占用内存：{mem.memory_usage()}')
        return self.__archive_pop, self.__archive_fit

    @staticmethod
    def __init_loc(pop, pop_max, pop_min):
        # 初始化粒子位置
        dim = len(pop_max)  # 输入参数维度
        # numpy.random.uniform(low, high, size) 从均匀分布中随机采样，size是输出样本数量
        return np.random.uniform(0, 1, (pop, dim)) * (pop_max - pop_min) + pop_min

    @staticmethod
    def __init_v(pop, v_max, v_min):
        v_dim = len(v_max)  # 维度
        # v_ = np.random.uniform(0,1,(particals,v_dim))*(v_max-v_min)+v_min
        return np.zeros((pop, v_dim))

    @staticmethod
    def __init_pbest(pop, fit):
        return pop, fit

    @staticmethod
    def __init_archive(pop, fit):
        # NDSort()[0] 取出第一组返回值，如果是1则是第一层的粒子
        front_index = NDsort.NDSort(fit, pop.shape[0])[0] == 1
        front_index = np.reshape(front_index, (-1,)) # 矩阵转成行向量

        # curr_archiving_in = pop[front_index]
        # curr_archiving_fit = fit[front_index]

        # pareto_c = pareto.Pareto_(pop,fitness_)
        # curr_archiving_in_,curr_archiving_fit_ = pareto_c.pareto()
        return pop[front_index], fit[front_index]
