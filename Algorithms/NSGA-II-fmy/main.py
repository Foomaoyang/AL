from pop import *
import ga as ga
from individual import *
import matplotlib.pyplot as plt
from nsgaii import *


def main():
    nsga_ii = NSGAII(100)
    nsga_ii.Pop = nsga_ii.populations.creat_pop()
    nsga_ii.run()
    nsga_ii.draw()


if __name__ == '__main__':
    main()









