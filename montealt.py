import numpy as np
import numpy.random as npr


class Grid:
    X, Y = None
    __grid = None
    t = 0

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.__grid = [[[] for y in range(Y)] for x in range(X)]

    def step(self):  # step simulation by one
        self.t += 1
        for x in range(self.X):
            for y in range(self.Y):
                if self.__grid[x][y] is None:  # not interesting if no animal present
                    continue
                for animal in self.__grid[x][y]:
                    animal.age += 1


class Animal:
    pos = None
    __pmove = 0  # Probabilty of moving from square this step
    __pbirth = 0  # Probability of giving birth this step
    __pdie = 0  # Probability of dieing
    __pcatch = 0  # Probability of catching if in same cell
    __pabsorb = 0  # Probability of growing given a catch (Quite high)
    age = 0

    def __init__(self, pmove, pbirth, pdie, pcatch, pabsord, x, y):
        self.pos = np.array([x, y])
        self.__pmove = pmove
        self.__pbirth = pbirth
        self.__pdie = pdie
        self.__pcatch = pcatch
        self.__pabsorb = pabsord

    def getPMove(self):
        return self.__pmove
