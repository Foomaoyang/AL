import numpy as np
import random
import matplotlib.pyplot as plt

class PSO():
    def __init__(self, pn, dim, max_iter):
        self.w = 0.8
        self.c1 = 2
        self.c2 = 2
        self.r1 = 0.6
        self.r2 = 0.3
        self.pN = pn  # 粒子数量
        self.dim = dim  # 搜索维度
        self.max_iter = max_iter  # 迭代次数
        self.X = np.zeros((self.pN, self.dim))  # 所有粒子的位置和速度
        self.V = np.zeros((self.pN, self.dim))
        self.pbest = np.zeros((self.pN, self.dim))  # 个体经历的最佳位置和全局最佳位置
        self.gbest = np.zeros((1, self.dim))
        self.p_fit = np.zeros(self.pN)  # 每个个体的历史最佳适应值
        self.fit = 1e10  # 全局最佳适应值

    @staticmethod
    def function(x):                  # 目标函数Sphere函数
        return x**4-2*x+3

    def init_population(self):              # 初始化种群
        for i in range(self.pN):            # 因为要随机生成pN个数据，所以需要循环pN次
            for j in range(self.dim):       # 每一个维度都需要生成速度和位置，故循环dim次
                self.X[i][j] = random.uniform(0, 1)
                self.V[i][j] = random.uniform(0, 1)
            self.pbest[i] = self.X[i]       # 其实是给self.pbest定值
            tmp = self.function(self.X[i])  # 得到现在最优
            self.p_fit[i] = tmp              # 这个个体历史最佳的位置
            if tmp < self.fit:              # 得到现在最优和历史最优比较大小
                self.fit = tmp
                self.gbest = self.X[i]

    def iterator(self):                     # 更新粒子位置
        fitness = []
        for t in range(self.max_iter):      # 迭代次数，不是越多越好
            for i in range(self.pN):        # 更新gbest/pbest
                temp = self.function(self.X[i])
                if temp < self.p_fit[i]:    # 更新个体最优
                    self.p_fit[i] = temp
                    self.pbest[i] = self.X[i]
                    if self.p_fit[i] < self.fit:    # 更新全局最优
                        self.gbest = self.X[i]
                        self.fit = self.p_fit[i]
            for i in range(self.pN):        # 更新速度/位置
                self.V[i] = self.w * self.V[i] + self.c1 * self.r1 * (self.pbest[i] - self.X[i]) + self.c2 * self.r2 *(self.gbest - self.X[i])
                self.X[i] = self.X[i] + self.V[i]
            fitness.append(self.fit)
            print(self.X[0], end=" ")
            print(self.fit)                 # 输出最优值
        return fitness

