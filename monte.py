import numpy as np
import numpy.random as npr
import matthew as mc

class Grid:
    X, Y = None
    population = None
    grid = None
    t = 0

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.population = []

    def append(self, obj, x, y):
        self.population.append(obj)

    def step(self):  # step simulation by one
        self.t += 1
        # Moving - Loop through pop find beas
        predList = [beast for beast in self.population if isinstance(beast, Predator)][:]# <- Maybe not needed
        # for x in range(self.X):
        #   for y in range(self.Y):
        #      # find the beasts here
        #       cell = [beast for beast in copyList if beast.pos == (x, y)]
        #       predNo = sum([1 for beast in copyList if isinstance(beast, Predator)])
        #       preyNo = len(cell) - predNo
        #  for 
        for pred in predList:
            # generate a list of prey
            ani = [beast for beast in self.population if
                   isinstance(beast, Prey) and beast.pos == pred.pos and beast.alive]
            cull = mc.culmBinom(pred.eat, len(ani), npr.uniform())
            for die in range(cull):
                pred.eat(die)

class Animal:
    pos = None
    alive = True
    _pmove = 0  # Probabilty of moving from square this step
    #  Probability of growing given a catch (Quite high)
    age = 0

    def __init__(self, pmove, pos):
        self.pos = pos
        self._pmove = pmove
        Grid.population.append(self)  # I don't like this - Rob

    def move(self):
        if npr.uniform() <= self._pmove:
            self.pos += npr.randint(0, 1, (1, 2))[0] * 2 - 1
            self.pos[0] %= Grid.X
            self.pos[1] %= Grid.Y
        else:
            return

    def kill(self):
        self.alive = False
        Grid.population.remove(self)

    def checkStatus(self):
        return self.alive


class Predator(Animal):
    pdie = 0
    pabsorb = 0
    peat = 0

    def __init__(self, pmove, pdie, pabsorb, peat, pos):
        Animal.__init__(self, pmove, pos)
        self.pdie = pdie
        self.pabsorb = pabsorb
        self.peat = peat

    def eat(self, culling):
        culling.kill()
        if npr.uniform() <= self.pabsorb:
            Grid.population.append(Predator(self._pmove, self.pdie, self.pabsorb, self.peat, self.pos))


class Prey(Animal):
    __pbirth = 0

    def __init__(self, pmove, pbirth, pos):
        Animal.__init__(self, pmove, pos)
        self.__pbirth = pbirth

    def birth(self):
        if npr.uniform() <= self.__pbirth:
            Grid.population.append(Prey(self._pmove, self.__pbirth, self.pos))
        else:
            return
