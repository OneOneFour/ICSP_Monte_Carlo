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
debug = False

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
            for ani in self.population[key]:
                if not ani.alive:
                    self.population[key].remove(ani)

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
        print()
    def step(self, world):
        self.age += 1
        if self.age > self.lifeExpect:
            self.kill()
        return

    def kill(self):
        if debug:
            print("KILL: " + self.name + "_" + str(self.id))
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
        self.pbirth = npr.normal(mgrow, stdgrow)
        if debug:
            print("PREDBIRTH: " + " lifeexpect:" + str(self.lifeExpect) + " killprob:" + str(
                self.pkill) + " growProb:" + str(self.pbirth))

    def step(self, world):
        Animal.step(self, world)
        if not self.alive:
            return
        self.eat(world.getPrey(), world)  # get the prey

    def eat(self, prey, world):
        for meal in range(pf.culmBinom(self.pkill, len(prey))):
            if debug:
                print("CATCH: " + self.name + "_" + str(self.id) + " TARGET: " + prey[meal].name + "_" + str(
                    prey[meal].id))
            prey[meal].kill()
            if npr.uniform() < self.pbirth:
                world.Spawn(Predator(self.mkill, self.stdkill, self.mgrow, self.stdgrow,
                                     self.mExpect, self.stdExpect, self.name))
                # Spawn Baby next step


class Prey(Animal):  # mean number of babies each step
    stdgrow = 0
    mgrow = 0
    pgrow = 0
    def __init__(self, mgrow, stdgrow, mExpect, stdExpect, name):
        Animal.__init__(self, mExpect, stdExpect, name)
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
            world.Spawn(Prey(self.mgrow, self.stdgrow, self.mExpect, self.stdExpect, self.name))


def runSim(alpha, beta, gamma, delta, s0, stop=10, steps=10, scale=1):
    alpha1, beta1, gamma1, delta1 = alpha / steps, beta / (scale * s0[1] * steps), gamma / steps, delta / (
        scale * s0[0] * steps)
    world = World()
    if debug:
        print("----- START ----")
        print(
            "alpha = " + str(alpha1) + " beta = " + str(beta1) + " delta = " + str(delta1) + " gamma = " + str(gamma1))
    world.SpawnPrey(alpha1, 0.5 / steps, 500 * steps, 1 * steps, int(s0[0] * scale))
    world.SpawnPredator(beta1 / (alpha1 + 1), 0.01 / steps, delta1 / beta1, 0.1 / steps, 1 / gamma1, 1 * steps,
                        int(s0[1] * scale))
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
