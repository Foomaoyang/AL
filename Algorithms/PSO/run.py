
import numpy as np
import random
import matplotlib.pyplot as plt
from pso import PSO
# https://blog.csdn.net/qq_43634001/article/details/91398204

my_pso = PSO(pn=30, dim=1, max_iter=100)
my_pso.init_population()                # 初始化种群
fitness = my_pso.iterator()             # 进行迭代训练

plt.figure(1)
plt.title('Figure1')
plt.xlabel('iterators', size=14)
plt.ylabel('fitness', size=14)
t = np.array([t for t in range(0, 100)])
fitness = np.array(fitness)
plt.plot(t, fitness, color='b', linewidth=2)
plt.show()




