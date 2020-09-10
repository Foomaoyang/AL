from pop import *
import ga as ga
from individual import *
import matplotlib.pyplot as plt


class NSGAII:

    def __init__(self, iterations=100, pop_size=100):
        self.__iterations = iterations  # 种群迭代次数
        self.populations = Pop(pop_size)  # 初始化粒子群
        ga.idv = Individual()
        self.__Qt = []
        self.__Rt = []  # 解集
        self.pareto_f = []
        self.Pop = []

    def fast_nodominate_sort(self, pop):
        """
        快速非支配排序
        :param pop:
        :return: 返回F1层粒子
        """
        # 快速非支配排序
        # 该算法需要计算种群pop中每个粒子i的两个参数Np（种群中支配粒子i的个体数目）和Sp（种群中被粒子i支配的粒子集合）
        # 1. 找出种群中所有Np=0的粒子，保存在集合F1中（也就是第一层）
        # 2. 对F1中的每个粒子i，其所支配的粒子集合为Sp，遍历Sp中每个粒子one，Np=Np-1,若Np=0，将Np保存在集合Q中（第二层)
        # 3. 以Q为当前集合，重复2，直到整个种群被分层
        front = []
        i = 1
        F1 = self.cpt_F1_dominate(pop)
        while len(F1) != 0:
            front.append(F1)
            Q = []
            for pi in F1:
                p = pop[pi]
                for q in p.Sp:  # Sp 种群中被粒子支配的个体集合
                    one_q = pop[q]
                    one_q.Np = one_q.Np - 1
                    if one_q.Np == 0:
                        one_q.p_rank = i + 1
                        Q.append(q)
            i = i + 1
            F1 = Q
            # 最后Q一定是空集合
            # Q为空集合，就表示所有粒子均被划分完毕
        return front

    def cpt_F1_dominate(self, pop):
        """
        计算更新种群支配关系
        :param pop:
        :return: 返回pareto前沿的第一层，数组形式
        """
        F1 = []
        for j, p in enumerate(pop):
            for i, q in enumerate(pop):
                if j != i:
                    if self.is_dominate(p, q):
                        # 如果p支配q，则添加到支配集合
                        if i not in p.Sp:
                            p.Sp.append(i)
                    elif self.is_dominate(q, p):
                        # q支配p，则可以支配p的粒子加一
                        p.Np = p.Np + 1
            if p.Np == 0:  # 为0说明没有粒子可以支配p粒子
                p.p_rank = 1
                F1.append(j)
        return F1

    @staticmethod
    def is_dominate(a, b):
        a_f = a.fit
        b_f = b.fit
        i = 0
        for av, bv in zip(a_f, b_f):
            if av < bv:
                i = i + 1
            if av > bv:
                return False
        if i != 0:
            return True
        return False

    def crowding_dist(self, Fi):
        # 拥挤度计算,只计算P内Fi位置部分的拥挤度
        # 同一层非支配个体集合中，为了保证解的个体能均匀分配在Pareto前沿，就需要使同一层中的非支配个体具有多样性，
        # 否则，个体都在某一处“扎堆”，将无法得到Pareto最优解集。NSGA—II采用了拥挤度策略，
        # 即计算同一非支配层级中某给定个体周围其他个体的密度。
        # ToDo 那个是最大哪个是最小
        f_max = Fi[0].fit[:]
        f_min = Fi[0].fit[:]
        f_size = len(f_max)
        for p in Fi:
            p.dp = 0  # dp 粒子的属性——拥挤度
            for fm in range(f_size):
                if p.fit[fm] > f_max[fm]:
                    f_max[fm] = p.fit[fm]
                if p.fit[fm] < f_min[fm]:
                    f_min[fm] = p.fit[fm]
        for m in range(f_size):
            Fi = self.fit_sorted(Fi, m)
            Fi[0].dp = 1000000
            Fi[len(Fi) - 1].dp = 1000000
            # 每个个体的拥挤距离是通过计算与其相邻的两个个体在每个子目标函数上的距离差之和来求取
            # 上边的m循环是循环是Fi层的粒子，子循环f是该粒子的拥挤度
            for f in range(1, len(Fi) - 1):
                Fi[f].dp = Fi[f].dp + (Fi[f+1].fit[m] - Fi[f-1].fit[m]) / (f_max[m] - f_min[m])

    @staticmethod
    def fit_sorted(Fi, m):
        """
        静态方法，对P中Fi索引对应的个体按照第m个函数排序
        :param Fi:
        :param m:
        :return: 返回支配排序后的pareto前沿
        """
        #
        for i in range(len(Fi) - 1):
            p = Fi[i]
            for j in range(i + 1, len(Fi)):
                q = Fi[j]
                if p != q and p.fit[m] > q.fit[m]:
                    # 前一个粒子的fitness比后一个大，交换两个粒子的位置
                    Fi[i], Fi[j] = Fi[j], Fi[i]
        return Fi

    @staticmethod
    def inv_append(layer, source, destination):
        """
        将第二个参数中的0-layer列的数追加到第三个参数
        :param layer: pareto层数
        :param source:
        :param destination:
        :return:
        """
        for i in layer:
            destination.append(source[i])

    @staticmethod
    def append(source, dist):
        for i in range(len(source)):
            dist.append(source[i])

    def run(self):
        # Pt，Qt父子代种群集,ndarray
        gen = 0
        while gen < self.__iterations:
            # if gen==self.iterations-2:
            #     print(self.pareto_f)
            gen += 1
            self.__Rt = []
            self.__Qt = self.populations.next_Pop(self.Pop)
            self.append(self.Pop, self.__Rt)
            self.append(self.__Qt, self.__Rt)
            # 找到前沿层F1,F2,....
            F = self.fast_nodominate_sort(self.__Rt)
            self.pareto_f = []
            # 保留pareto前沿
            self.inv_append(F[0], self.__Rt, self.pareto_f)
            print('%s th pareto len %s:' % (gen, len(F[0])))
            # 保留前沿层最好的popsize个
            pt_next = []
            i = 0
            while (len(pt_next) + len(F[i])) <= self.populations.pop_size:
                self.inv_append(F[i], self.__Rt, pt_next)
                i += 1
            # self.crowding_dist(Fi)
            Fi = []
            self.inv_append(F[i], self.__Rt, Fi)
            for ip in Fi:
                pt_next.append(ip)
            pt_next = pt_next[0:self.populations.pop_size]
            self.Pop = pt_next

    def draw(self):

        pf1_data = []
        pf2_data = []
        # if len(self.pareto_f)>self.populations.pop_size:
        #     self.pareto_f=self.pareto_f[0:self.populations.pop_size]
        for p in self.pareto_f:
            pf1_data.append(p.fit[0])
            pf2_data.append(p.fit[1])
        f1_data = []
        f2_data = []
        for a in self.__Rt:
            f1_data.append(a.fit[0])
            f2_data.append(a.fit[1])
        plt.xlabel('Function 1', fontsize=15)
        plt.ylabel('Function 2', fontsize=15)
        plt.title('ZDT4')
        # plt.xlim(min(pf1_data), max(pf1_data))
        # plt.ylim(min(pf2_data), max(pf2_data))
        # ToDo: f1_data 解集的解？ pf1_data pareto前沿解？
        plt.scatter(f1_data, f2_data, c='black', s=5)
        plt.scatter(pf1_data, pf2_data, c='red', s=10)
        plt.show()


