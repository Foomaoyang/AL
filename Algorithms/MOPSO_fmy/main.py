# encoding: utf-8
from Mopso import *
from util import testFunc
import numpy as np


def main():
    num_pop = 30  # 粒子群的数量
    iterations = 100  # 迭代次数
    grid_div = 10  # 网格等分数量
    threshold = 300  # 外部存档阀值

    test_problem = "DTLZ2"
    num_obj = 2
    # 选择测试集
    # pop, boundary, coding = P_objective.obj_func("init", test_problem, num_obj, num_pop)
    pop, boundary, coding = testFunc.obj_func("init", test_problem, num_obj, num_pop)

    max_ = boundary[0]
    min_ = boundary[1]

    ps = Mopso(num_pop, max_, min_, threshold, grid_div)  # 粒子群实例化
    pareto_pop, pareto_fitness = ps.run(iterations)  # 经过iterations轮迭代后得到存档的粒子，即pareto边界粒子
    np.savetxt("./img_txt/pareto_pop.txt", pareto_pop)  # 保存pareto边界粒子的坐标
    np.savetxt("./img_txt/pareto_fitness.txt", pareto_fitness)  # 打印pareto边界粒子的适应值
    print("\n", "pareto边界的坐标保存于：/img_txt/pareto_pop.txt")
    print("pareto边界的适应值保存于：/img_txt/pareto_fitness.txt")
    print("\n,迭代结束,over")


if __name__ == "__main__":
    main()

