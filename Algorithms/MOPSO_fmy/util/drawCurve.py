# encoding: utf-8
# from mpl_toolkits.mplot3d import Axes3D
# from mpl_toolkits.mplot3d import Axes3D
import time
import numpy as np
import matplotlib.pyplot as plt


class DrawParetoCurve:
    def __init__(self):
        self.start_time = time.time()

    @classmethod
    def show(cls, pop, fit, archive_pop, archive_fit, i):
        """
        打印pareto曲线 蓝色是新粒子 红色点是档案中的粒子
        :param pop: 种群中的粒子
        :param fit: 图中蓝色点是新粒子
        :param archive_pop: 档案中的粒子
        :param archive_fit: 图中红色点是档案中的粒子
        :param i: 迭代第几次
        :return:
        """
        # 共3个子图，第1、2/子图绘制输入坐标与适应值关系，第3图展示pareto边界的形成过程
        fig = plt.figure('第' + str(i + 1) + '次迭代')
        # fig = plt.figure('第'+str(i+1)+'次迭代',figsize = (17,5))
        # ax1 = fig.add_subplot(131, projection='3d')
        # ax1.set_xlabel('input_x1')
        # ax1.set_ylabel('input_x2')
        # ax1.set_zlabel('fitness_y1')
        # ax1.plot_surface(cls.x1,cls.x2,cls.y1,alpha = 0.6)
        # ax1.scatter(pop[:, 0], pop[:, 1], fit[:, 0], s=20, c='blue', marker=".")
        # ax1.scatter(archive_pop[:, 0], archive_pop[:, 1], archive_fit[:, 0], s=50, c='red', marker=".")
        # ax2 = fig.add_subplot(132, projection='3d')
        # ax2.set_xlabel('input_x1')
        # ax2.set_ylabel('input_x2')
        # ax2.set_zlabel('fitness_y2')
        # ax2.plot_surface(cls.x1,cls.x2,cls.y2,alpha = 0.6)
        # ax2.scatter(pop[:, 0], pop[:, 1], fit[:, 1], s=20, c='blue', marker=".")
        # ax2.scatter(archive_pop[:, 0], archive_pop[:, 1], archive_fit[:, 1], s=50, c='red', marker=".")

        ax3 = fig.add_subplot(111)  # 133
        # ax3.set_xlim((0,1))
        # ax3.set_ylim((0,1))
        ax3.set_xlabel('fitness_y1')
        ax3.set_ylabel('fitness_y2')
        ax3.scatter(fit[:, 0], fit[:, 1], s=10, c='blue', marker=".")
        ax3.scatter(archive_fit[:, 0], archive_fit[:, 1], s=30, c='red', marker=".", alpha=1.0)
        # plt.savefig('./img_txt/'+str(i+1)+'.png')  # 打印输出语句要在show()语句前
        plt.show()
        # print('第'+str(i+1)+'次迭代的图片保存于 img_txt 文件夹')
        # print('第'+str(i+1)+'次迭代, time consuming: ',np.round(time.time() - cls.start_time, 2), "s")
        plt.ion()
        # plt.close()
