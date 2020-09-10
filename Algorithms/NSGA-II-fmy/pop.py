from ga import *
import ga as ga


class Pop:
    idv = Individual()

    def __init__(self, pop_size=100):
        self.pop_size = pop_size

    def creat_pop(self):
        pop = []
        for i in range(self.pop_size):
            pop.append(self.idv.creat_one())
        return pop

    def next_Pop(self, pop):
        fit = []
        idv = self.idv
        P = pop
        p_size = len(P)
        for p in P:
            p = idv.reset_one(p)
            cp = idv.creat_one()
            cp.X[:] = p.X[:]
            cp.fit[:] = p.fit[:]
            fit.append(cp)
        # 产生下一代
        select(fit)
        for i in range(p_size):
            j = np.random.randint(0, p_size, size=1)[0]
            cross(fit[i], fit[j])
            fit[j] = mutate(fit[j])
        return fit

