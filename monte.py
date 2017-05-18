import datetime

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr
import scipy.misc as scm

import ProjectFunctions as pf


def culmBinom(p, n):
    if n is 0:
        return 0
    s = 0
    prob = 1
    rand = npr.uniform()  # generates a random number to compare the probability to
    while True:
        prob -= ((1 - p) ** (n - s)) * (p ** s) * (
        scm.comb(n, s))  # adjust the parameters of prob to allow for the new number of events
        if rand > prob:  # see if the randomly generated number lies in the region corresponding to s events
            return s  # if the randomly generated number lies within the section for this area of prob, retun the number of successes
        else:
            s += 1


class World:
    predCounter = []
    preyCounter = []
    population = None
    addQueue = None
    t = 0

    def __init__(self):
        World.population = {}
        World.addQueue = {}

    def step(self):
        self.addQueue.clear()
        self.t += 1
        self.predCounter.append(len(self.population["Predator"]))
        self.preyCounter.append(len(self.population["Prey"]))
        for key in self.population:
            for ani in self.population[key]:
                ani.step(self)
        # cull the old
        for key in self.population:
            if key in self.addQueue:
                self.population[key].extend(self.addQueue[key])
            for ani in self.population[key]:
                if not ani.alive:
                    self.population[key].remove(ani)

    def getPreyCount(self):
        return len(self.getPrey())

    def getPrey(self):
        a = [prey for prey in self.population['Prey'] if prey.alive]
        if 'Prey' in self.addQueue:
            a.extend([prey for prey in self.addQueue['Prey'] if prey.alive])
        return a

    def getPredators(self):
        return self.population['Predator']

    def Spawn(self, animal):
        if animal.name not in self.addQueue:
            self.addQueue[animal.name] = []
        self.addQueue[animal.name].append(animal)

    def SpawnPredator(self, mkill, stdkill, mgrow, stdgrow, mexpect, stdexpect, count):
        self.population['Predator'] = [Predator(mkill, stdkill, mgrow, stdgrow, mexpect, stdexpect, "Predator") for a in
                                       range(count)]

    def SpawnPrey(self, mgrow, stdgrow, mexpext, stdexpect, count):
        self.population['Prey'] = [Prey(mgrow, stdgrow, mexpext, stdexpect, "Prey") for a in range(count)]


class Animal:
    id = 0
    count = 0
    name = "Animal"
    alive = True
    mExpect = 0
    stdExpect = 0
    lifeExpect = 0  # Mean age of death #std dev is 1.5 steps?
    age = 0

    def __init__(self, meanExpectancey, stdExpectancy, name):
        self.id = Animal.count
        Animal.count += 1
        self.lifeExpect = np.floor(npr.normal(meanExpectancey, stdExpectancy))
        self.name = name
        self.mExpect = meanExpectancey
        self.stdExpect = stdExpectancy

    def step(self, world):
        self.age += 1
        if self.age > self.lifeExpect:
            self.kill()
        return

    def kill(self):
        self.alive = False


class Predator(Animal):
    pkill = 0
    mkill = 0
    stdkill = 0
    mgrow = 0
    stdgrow = 0

    def __init__(self, mkill, stdkill, mgrow, stdgrow, mexpect, stdexpect, name):
        Animal.__init__(self, mexpect, stdexpect, name)
        self.mkill = mkill
        self.stdkill = stdkill
        self.mgrow = mgrow
        self.stdgrow = stdgrow
        self.pkill = npr.normal(mkill, stdkill)

    def step(self, world):
        Animal.step(self, world)
        if not self.alive:
            return
        self.eat(world.getPrey())  # get the prey

    def eat(self, prey):
        for meal in range(culmBinom(self.pkill, len(prey))):
            prey[meal].kill()
            for baby in range(round(npr.normal(self.mgrow, self.stdgrow))):
                world.Spawn(Predator(self.mkill, self.stdkill, self.mgrow, self.stdgrow,
                                     self.mExpect, self.stdExpect, self.name))
                # Spawn Baby next step



class Prey(Animal):  # mean number of babies each step
    stdgrow = 0
    mgrow = 0

    def __init__(self, mgrow, stdgrow, mExpect, stdExpect, name):
        Animal.__init__(self, mExpect, stdExpect, name)
        self.mgrow = mgrow
        self.mgrow = mgrow
        self.stdgrow = stdgrow

    def step(self, world):
        if not self.alive:
            return
        self.rollGrow(world)
        Animal.step(self, world)

    def rollGrow(self, world):
        for baby in range(round(npr.normal(self.mgrow, self.stdgrow))):
            world.Spawn(Prey(self.mgrow, self.stdgrow, self.mExpect, self.stdExpect, self.name))


alpha, beta, gamma, delta = 1, 0.2, 0.6, 1
world = World()
world.SpawnPrey(alpha, 0.25, 500, 1.0, 20)
world.SpawnPredator(beta / (alpha + 1), 0.1, gamma / delta, 0.25, 1 / delta, 0.5, 20)

##Remeber p = beta/(alpha+1)
i = 25

for c in range(i):
    world.step()

plt.plot(np.arange(i), world.preyCounter, 'b-', label="prey")
plt.plot(np.arange(i), world.predCounter, 'r-', label="predator")
plt.legend()
filename = (datetime.datetime.now().ctime() + "output").replace(":", "")
plt.gcf().savefig(filename + ".png")
plt.show()
pf.saveValues(alpha, beta, gamma, delta, filename + ".csv")
# Output
