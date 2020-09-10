import numpy as np
import testFunc.SCH as SCH
import testFunc.ZDT1 as ZDT1
import testFunc.ZDT2 as ZDT2
import testFunc.ZDT4 as ZDT4
from individual import Individual

'''
遗传算法杂交变异选择部分
'''

test_fun = ZDT4

idv = -1


def cross(p1, p2, c_rate=0.8):
    # p1 tp p2
    if np.random.rand() < c_rate:
        p2 = idv.reset_one(p2)
        r1 = 0.7
        r2 = 1 - r1
        x1 = r1 * p1.X + r2 * p2.X
        x2 = r2 * p1.X + r1 * p2.X
        p1.X = x1
        p2.X = x2
        p2.fit = test_fun.Func(p2.X)
        p1.fit = test_fun.Func(p1.X)
    return p2


def mutate(pop, m_rate=0.2):
    # 对p节点变异
    gen_len = len(pop.X)
    if np.random.rand() < m_rate:
        pop = idv.reset_one(pop)
        # 变异5%的基因对
        for l in range(int(gen_len * 0.1)):
            j = np.random.randint(0, gen_len, size=1)[0]
            d = np.random.randint(0, gen_len, size=1)[0]
            pop.X[j], pop.X[d] = pop.X[d], pop.X[j]
            pop.fit = test_fun.Func(pop.X)
    return pop


def select(pop):
    # 洗牌产生新P
    pop_mew = []
    for ip in pop:
        if ip.p_rank <= 3:
            pop_mew.append(ip)
    while len(pop_mew) != len(pop):
        p = idv.creat_one()
        pop_mew.append(p)
    return pop
