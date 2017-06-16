import sys
import time
from datetime import datetime as dt

import numpy as np
import numpy.random as npr

sys.stdout = open("output/" + dt.now().ctime().replace(":", " ") + "output.txt", 'w')
seed = int(time.time())
npr.seed(seed)
print("SEED - " + str(seed))
debug = True

class World:
    gridsize = 2
    predCounter = []
    preyCounter = []
    addQueue = None
    t = 1
    def __init__(self, gridsize):
        self.gridsize = gridsize
        self.addQueue = []
        self.pos = np.empty((gridsize, gridsize), dtype=Animal)

    def step(self):
        if debug:
            print("---------- BEGIN STEP " + str(self.t) + " ----------")
        self.addQueue.clear()
        if debug:
            print(
                "Prey count:" + str(self.preyCounter[self.t - 1]) + " Pred count:" + str(self.predCounter[self.t - 1]))
        animals = self.get_objects(Animal)
        for ani in animals:
            ani.step(self)
        for item in self.addQueue:
            self.birth(item[0], item[1])
        for ani in animals:
            if not ani.alive:
                self.pos[ani.loc[0]][ani.loc[1]] = None  # Hasta la vista
        self.t += 1
        self.preyCounter.append(len(self.get_objects(Prey)))
        self.predCounter.append(len(self.get_objects(Predator)))

    def Spawn(self, animal, ploc):
        if debug:
            print("SPAWN: " + animal.name + "_" + str(animal.id) + " ppos: " + str(ploc))
        self.addQueue.append((animal, ploc))

    def get_objects(self, object):
        objectArray = []
        for x in range(len(self.pos)):
            for y in range(len(self.pos[x])):
                if self.pos[x][y] is None:
                    continue
                if isinstance(self.pos[x][y], object):
                    body = self.pos[x][y]
                    objectArray.append(body)
        return objectArray

    def birth(self, animal, ploc):
        either = [-1, 0, 1]
        dest = []
        for x in either:
            for y in either:
                if self.pos[(ploc[0] + x) % self.gridsize][(ploc[1] + y) % self.gridsize] is None:
                    dest.append((x, y))
        if len(dest) == 0:
            return None
        chosen = npr.randint(len(dest))
        loc = [(ploc[0] + dest[chosen][0]) % self.gridsize, (ploc[1] + dest[chosen][1]) % self.gridsize]
        animal.loc = loc[:]
        self.pos[loc[0]][loc[1]] = animal

    def randSpawnPredator(self, mkill, stdkill, mgrow, stdgrow, mexpect, stdexpect, count, killRange):
        self.predCounter.append(count)
        for a in range(count):
            x = npr.randint(self.gridsize)
            y = npr.randint(self.gridsize)
            s = 0
            while self.pos[x][y] is not None:
                x += 1
                x %= self.gridsize
                s += 1
                if s == (self.gridsize - 1):
                    y += 1
                    y %= self.gridsize
                    s = 0

            self.pos[x][y] = Predator(mkill, stdkill, mgrow, stdgrow, mexpect, stdexpect, "Predator", killRange)
            self.pos[x][y].loc = [x, y]



    def randSpawnPrey(self, mgrow, stdgrow, mexpext, stdexpect, count):
        self.preyCounter.append(count)
        for a in range(count):
            x = npr.randint(self.gridsize)
            y = npr.randint(self.gridsize)
            s = 0
            while self.pos[x][y] is not None:
                x += 1
                x %= self.gridsize
                s += 1
                if s == (self.gridsize - 1):
                    y += 1
                    y %= self.gridsize
                    s = 0

            self.pos[x][y] = Prey(mgrow, stdgrow, mexpext, stdexpect, "Prey")
            self.pos[x][y].loc = [x, y]

    '''
    def showGrid(self):
        for key in self.population:
            print(key)
            gridArray = np.zeros((self.gridsize, self.gridsize))
            for beast in self.population[key]:
                gridArray[beast.loc[0]][beast.loc[1]] += 1
            print (gridArray)

    '''
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

    def __init__(self, meanExpectancey, stdExpectancy, name):
        self.id = Animal.count
        Animal.count += 1
        self.lifeExpect = round(npr.normal(meanExpectancey, stdExpectancy))
        self.name = name
        self.mExpect = meanExpectancey
        self.stdExpect = stdExpectancy

    def step(self, world):
        self.age += 1
        if self.age > self.lifeExpect:
            self.kill()
            return
        if self.alive:
            self.move(world)

    def kill(self):
        if debug:
            print(
                "KILL: " + self.name + "_" + str(self.id) + " age:" + str(self.age) + " lexpect:" + str(self.lifeExpect))
        self.alive = False


    def move(self, world):
        #if self.move > npr.uniform():
        #self.loc = [(elem+(npr.randint(3)-1))%world.gridsize for elem in loc] TODO sort this out, into one line
        #self.loc[1] += (npr.randint(3)-1)
        #self.loc[1] %= world.gridsize
        #self.loc[0] += (npr.randint(3)-1)
        #self.loc[0] %= world.gridsize
        either = [-1, 0, 1]
        dest = [(0, 0)]
        for x in either:
            for y in either:
                if world.pos[(self.loc[0] + x) % world.gridsize][(self.loc[1] + y) % world.gridsize] is None:
                    dest.append((x, y))
        chosen = npr.randint(len(dest))
        world.pos[(self.loc[0] + dest[chosen][0]) % world.gridsize][
            (self.loc[1] + dest[chosen][1]) % world.gridsize] = self
        if dest[chosen][0] != 0 or dest[chosen][1] != 0:
            world.pos[self.loc[0]][self.loc[1]] = None
        self.loc = [(self.loc[0] + dest[chosen][0]) % world.gridsize, (self.loc[1] + dest[chosen][1]) % world.gridsize]



class Predator(Animal):
    pkill = 0
    mkill = 0
    stdkill = 0
    mgrow = 0
    stdgrow = 0
    killRange = 0

    def __init__(self, mkill, stdkill, mgrow, stdgrow, mexpect, stdexpect, name, killRange):
        Animal.__init__(self, mexpect, stdexpect, name)
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
        self.eat(world.get_objects(Prey), world)  # get the prey

    def eat(self, preytot, world):
        prey = []
        for x in np.arange(-self.killRange, self.killRange + 1):
            for y in np.arange(-self.killRange, self.killRange + 1):
                if isinstance(world.pos[(self.loc[0] + x) % world.gridsize][(self.loc[1] + y) % world.gridsize], Prey):
                    prey.append(world.pos[(self.loc[0] + x) % world.gridsize][(self.loc[1] + y) % world.gridsize])

        for meal in prey:
            if self.pkill > npr.uniform():
                meal.kill()
                if npr.uniform() < self.pbirth:
                    world.Spawn(Predator(self.mkill, self.stdkill, self.mgrow, self.stdgrow,
                                         self.mExpect, self.stdExpect, self.name, self.killRange), self.loc)
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
            world.Spawn(Prey(self.mgrow, self.stdgrow, self.mExpect, self.stdExpect, self.name), self.loc)


'''
class Disease:  # mean number of babies each step
    pspread = 0
    pdeath0 = 0
    ill = []

    def __init__(self,pspread, pdeath0, loc=None):
        if loc!=None
            for beast in world.population:
                if beast.loc == loc:
                    if npr.rand() < pspread:
                        ill.append(beast)
        self.pspread = pspread
        self.pdeath0 = pdeath0

    def step(self):
        for infected in self.ill:
            for other in world.population:
                if other.loc == infected.loc:
                    if npr.rand() < self.pspread:
                        #effects of infection TODO
                        pass

    def updateIll(self):
        self.ill  = [elem for elem in self.ill if elem.alive == True]



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
'''
def runSim(alpha, beta, gamma, delta, s0, stop=10, steps=10, scale=1):
    world = World(25)
    world.randSpawnPrey(alpha / (steps), 0.1 / (steps), 50 * steps, 1 * steps, int(s0[0] * scale))
    world.randSpawnPredator(world.gridsize * beta / (steps * scale), (0.1 / (steps * scale)), delta / (beta),
                            0.1 / scale, steps / gamma, 1.0 * steps, int(s0[1] * scale), 2)
    for i in range(stop * steps):
        world.step()
    return [world.preyCounter, world.predCounter], np.linspace(0, stop, steps * stop)


alpha, beta, gamma, delta, s0 = 0.67, 1.33, 1, 1, [1, 0.75]

(eq, te) = lv.lotkavolterragraph(alpha, beta, gamma, delta, s0, 20, 10)
(sim, ts) = runSim(alpha, beta, gamma, delta, s0, 20, 10, 100)

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
'''
