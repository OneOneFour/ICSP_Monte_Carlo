import datetime

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr
import scipy.misc as scm

import ProjectFunctions as pf

print ("I made it here")


def culmBinom(p, n):
    if n is 0:
        return 0
    s = 0
    prob = 1
    rand = npr.uniform()  # generates a random number to compare the probability to
    while True:
        prob -= ((1 - p) ** (n - s)) * (p ** s) * (scm.comb(n, s))  # adjust the parameters of prob to allow for the new number of events
        if rand > prob:  # see if the randomly generated number lies in the region corresponding to s events
            return s  # if the randomly generated number lies within the section for this area of prob, retun the number of successes
        else:
            s += 1


class World:
    gridsize = 2
    predCounter = []
    preyCounter = []
    population = None
    addQueue = None
    t = 0

    def __init__(self, gridsize):
        self.gridsize = gridsize
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
            for ani in self.population[key][:]:
                if not ani.alive:
                    self.population[key].remove(ani)
        for key in self.population:
            for beast in self.population[key]:
                beast.move()

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

    def randSpawnPredator(self, mkill, stdkill, mgrow, stdgrow, mexpect, stdexpect, count, killRange):
        loc = [npr.uniform(self.gridsize), npr.uniform(self.gridsize)]
        self.population['Predator'] = [Predator(mkill, stdkill, mgrow, stdgrow, mexpect, stdexpect, "Predator", loc, killRange) for a in
                                       range(count)]

    def randSpawnPrey(self, mgrow, stdgrow, mexpext, stdexpect, count):
        loc = [npr.uniform(self.gridsize), npr.uniform(self.gridsize)]
        self.population['Prey'] = [Prey(mgrow, stdgrow, mexpext, stdexpect, "Prey", loc) for a in range(count)]

    def showGrid(self):
        for key in self.population:
            print(key)
            gridArray = np.zeros((self.gridsize, self.gridsize))
            for beast in self.population[key]:
                gridArray[beast.loc[0]][beast.loc[1]] += 1
            print (gridArray)


class Animal:
    id = 0
    count = 0
    name = "Animal"
    alive = True
    mExpect = 0
    stdExpect = 0
    lifeExpect = 0  # Mean age of death #std dev is 1.5 steps?
    age = 0
    loc = []
    #pmove = 0

    def __init__(self, meanExpectancey, stdExpectancy, name, loc):
        self.id = Animal.count
        Animal.count += 1
        self.lifeExpect = round(npr.normal(meanExpectancey, stdExpectancy))
        self.name = name
        self.mExpect = meanExpectancey
        self.stdExpect = stdExpectancy
        self.loc = loc[:]

    def step(self, world):
        self.age += 1
        if self.age > self.lifeExpect:
            self.kill()
        return

    def kill(self):
        self.alive = False

    def move(self):
        #if self.move > npr.uniform():
        #self.loc = [(elem+(npr.randint(3)-1))%world.gridsize for elem in loc] TODO sort this out, into one line
        self.loc[1] += (npr.randint(3)-1)
        self.loc[1] %= world.gridsize
        self.loc[0] += (npr.randint(3)-1)
        self.loc[0] %= world.gridsize

class Predator(Animal):
    pkill = 0
    mkill = 0
    stdkill = 0
    mgrow = 0
    stdgrow = 0
    killRange = 0

    def __init__(self, mkill, stdkill, mgrow, stdgrow, mexpect, stdexpect, name, loc, killRange):
        Animal.__init__(self, mexpect, stdexpect, name, loc)
        self.mkill = mkill
        self.stdkill = stdkill
        self.mgrow = mgrow
        self.stdgrow = stdgrow
        self.pkill = npr.normal(mkill, stdkill)
        self.killRange = killRange

    def step(self, world):
        Animal.step(self, world)
        if not self.alive:
            return
        self.eat(world.getPrey())  # get the prey

    def eat(self, preytot):
        prey = [food for food in preytot if food.loc == self.loc]
        for meal in range(culmBinom(self.pkill, len(prey))):
            prey[meal].kill()
            for baby in range(round(npr.normal(self.mgrow, self.stdgrow))):
                world.Spawn(Predator(self.mkill, self.stdkill, self.mgrow, self.stdgrow,
                                     self.mExpect, self.stdExpect, self.name, self.loc))
                # Spawn Baby next step



class Prey(Animal):  # mean number of babies each step
    stdgrow = 0
    mgrow = 0

    def __init__(self, mgrow, stdgrow, mExpect, stdExpect, name, loc):
        Animal.__init__(self, mExpect, stdExpect, name, loc)
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
            world.Spawn(Prey(self.mgrow, self.stdgrow, self.mExpect, self.stdExpect, self.name, self.loc))


tscale = 1
killRange = 1
prey0, pred0 = 50, 75
alpha, beta, delta, gamma = 0.5, 0.5, 1.5, 0.7
alpha1, beta1, delta1, gamma1 = alpha / tscale, beta / (pred0 * tscale), delta / (prey0 * tscale), gamma / tscale
world = World(2)
world.randSpawnPrey(alpha1, 0.05 / (alpha1 * tscale), 5 * tscale, tscale, prey0)
world.randSpawnPredator(beta1 / (alpha1 + 1), 0.01 / tscale, delta1 / (beta1), beta1 / (delta1 * tscale), 1 / gamma1,
                    tscale, pred0, killRange)


##Remeber p = beta/(alpha+1)
i = 20 * tscale

for c in range(i):
    world.step()
    world.showGrid()

plt.plot(np.arange(i), world.preyCounter, 'b-', label="prey")
plt.plot(np.arange(i), world.predCounter, 'r-', label="predator")
plt.legend()
filename = "output/" + (datetime.datetime.now().ctime() + "output").replace(":", "")
#plt.gcf().savefig(filename + ".png")
plt.show()
#pf.saveValues(alpha, beta, gamma, delta, prey0, pred0, filename + ".csv")
# Output
