import sys
import time
from datetime import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr

import ProjectFunctions as pf
import lotkavolterra as lv

sys.stdout = open("output/" + dt.now().ctime().replace(":", "") + "output.txt", 'w')
seed = int(time.time())
npr.seed(seed)
print("SEED - " + str(seed))
debug = True

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
        if debug:
            print("---------- BEGIN STEP " + str(self.t) + " ----------")
        self.addQueue.clear()
        self.predCounter.append(len(self.population["Predator"]))
        self.preyCounter.append(len(self.population["Prey"]))
        if debug:
            print("Prey count:" + str(self.preyCounter[self.t]) + " pred count:" + str(self.predCounter[self.t]))
        self.t += 1
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
                beast.move(self)

    def getPreyCount(self):
        return len(self.getPrey())

    def getPrey(self):
        a = [prey for prey in self.population['Prey'] if prey.alive]
        return a

    def getPredators(self):
        return self.population['Predator']

    def Spawn(self, animal):
        if debug:
            print("SPAWN: " + animal.name + "_" + str(animal.id))
        if animal.name not in self.addQueue:
            self.addQueue[animal.name] = []
        self.addQueue[animal.name].append(animal)

    def randSpawnPredator(self, mkill, stdkill, mgrow, stdgrow, mexpect, stdexpect, count, killRange):
        loc = [npr.randint(self.gridsize), npr.randint(self.gridsize)]
        self.population['Predator'] = [Predator(mkill, stdkill, mgrow, stdgrow, mexpect, stdexpect, "Predator", loc, killRange) for a in
                                       range(count)]

    def randSpawnPrey(self, mgrow, stdgrow, mexpext, stdexpect, count):
        loc = [npr.randint(self.gridsize), npr.randint(self.gridsize)]
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
        if debug:
            print("KILL: " + self.name + "_" + str(self.id))
        self.alive = False

    def move(self, world):
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
        self.pbirth = npr.normal(mgrow, stdgrow)
        if debug:
            print("PREDBIRTH: " + " lifeexpect:" + str(self.lifeExpect) + " killprob:" + str(
                self.pkill) + " growProb:" + str(self.pbirth))

    def step(self, world):
        Animal.step(self, world)
        if not self.alive:
            return
        self.eat(world.getPrey(), world)  # get the prey

    def eat(self, preytot, world):
        min1 = self.loc[1] - self.killRange
        max1 = self.loc[1] + self.killRange
        min0 = self.loc[0] - self.killRange
        max0 = self.loc[0] + self.killRange
        prey = [food for food in preytot if min1 <= food.loc[1] <= max1 and min0 <= food.loc[0] <= max0]
        for meal in range(pf.culmBinomNew(self.pkill, len(prey))):
            prey[meal].kill()
            if npr.uniform() < self.pbirth:
                world.Spawn(Predator(self.mkill, self.stdkill, self.mgrow, self.stdgrow,
                                     self.mExpect, self.stdExpect, self.name, self.loc, self.killRange))
                # Spawn Baby next step



class Prey(Animal):  # mean number of babies each step
    stdgrow = 0
    mgrow = 0
    pgrow = 0

    def __init__(self, mgrow, stdgrow, mExpect, stdExpect, name,loc):
        Animal.__init__(self, mExpect, stdExpect, name,loc)
        self.mgrow = mgrow
        self.stdgrow = stdgrow
        self.pgrow = npr.normal(self.mgrow, self.stdgrow)
        if debug:
            print("PREYBIRTH:" + "lifeexpect:" + str(self.lifeExpect) + " growProb: " + str(self.pgrow))

    def step(self, world):
        if not self.alive:
            return
        self.rollGrow(world)
        Animal.step(self, world)

    def rollGrow(self, world):
        roll = npr.uniform()
        if roll < self.pgrow:
            world.Spawn(Prey(self.mgrow, self.stdgrow, self.mExpect, self.stdExpect, self.name,self.loc))


'''
tscale = 1
killRange = 1
prey0, pred0 = 50, 75
alpha, beta, delta, gamma = 0.67,1.33,1,1
alpha1, beta1, delta1, gamma1 = alpha / tscale, beta / (pred0 * tscale), delta / (prey0 * tscale), gamma / tscale
world = World(10)
world.randSpawnPrey(alpha1, 0.05 / (alpha1 * tscale), 5 * tscale, tscale, prey0)
world.randSpawnPredator(beta1 / (alpha1 + 1), 0.01 / tscale, delta1 / (beta1), beta1 / (delta1 * tscale), 1 / gamma1,
                    tscale, pred0, killRange)
'''

##Remeber p = beta/(alpha+1)
#i = 20 * tscale

#for c in range(i):
#    world.step()
#    world.showGrid()

#plt.plot(np.arange(i), world.preyCounter, 'b-', label="prey")
#plt.plot(np.arange(i), world.predCounter, 'r-', label="predator")
#plt.legend()
#filename = "output/" + (datetime.datetime.now().ctime() + "output").replace(":", "")
#plt.gcf().savefig(filename + ".png")
#plt.show()
#pf.saveValues(alpha, beta, gamma, delta, prey0, pred0, filename + ".csv")
# Output

def runSim(alpha, beta, gamma, delta, s0, stop=10, steps=10, scale=1):
    world = World(25)
    world.randSpawnPrey(alpha / (steps), 0.1 / (steps), 50 * steps, 1 * steps, int(s0[0] * scale))
    world.randSpawnPredator(world.gridsize * beta / (steps * scale), (0.1 / (steps * scale)), delta / (beta),
                            0.1 / scale, steps / gamma, 1.0 * steps, int(s0[1] * scale), 2)
    for i in range(stop * steps):
        world.step()
    return [world.preyCounter, world.predCounter], np.linspace(0, stop, steps * stop)


alpha, beta, gamma, delta, s0 = 0.67, 1.33, 1, 1, [1, 0.75]

(eq, te) = lv.lotkavolterragraph(alpha, beta, gamma, delta, s0, 10, 10)
(sim, ts) = runSim(alpha, beta, gamma, delta, s0, 10, 10, 100)

fig, axes = plt.subplots(nrows=2, figsize=(20, 10))

axes[0].plot(te, eq[:, 0], linewidth=1, label="prey")
axes[0].plot(te, eq[:, 1], linewidth=1, label="pred")

axes[1].plot(ts, sim[0], linewidth=1, label="prey")
axes[1].plot(ts, sim[1], linewidth=1, label="pred")

for ax in range(2):
    axes[ax].set_xlabel("Time")
    axes[ax].set_ylabel("Species Count")
    axes[ax].legend()

plt.show()
