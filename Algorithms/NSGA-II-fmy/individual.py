import ga


class Individual:

    test_func = ga.test_fun

    def __init__(self):
        self.Np = 0  # 支配当前个体的数量 种群中支配个数
        self.Sp = []  # 当前个体支配的个体集（所在种群编号） 种群中被个体支配的个体集合
        self.p_rank = 0  # 粒子支配个数排序，如果为1，则说明没有粒子可以支配该粒子，是非支配解
        self.dp = 0  # 拥挤度
        self.X = []
        self.fit = []

    def creat_one(self):
        self.X = ga.test_fun.bound[0] + (ga.test_fun.bound[1] - ga.test_fun.bound[0]) * ga.np.random.rand(
            self.test_func.dim)
        self.fit = ga.test_fun.Func(self.X)
        return self

    def reset_one(self):
        self.Np = 0
        self.Sp = []
        self.p_rank = 0
        self.dp = 0
        return self
