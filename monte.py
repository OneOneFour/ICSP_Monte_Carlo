import time

import numpy as np
import numpy.random as npr

import ProjectFunctions as pf

# sys.stdout = open("output/" + dt.now().ctime().replace(":", " ") + "output.txt", 'w')


#sys.stdout = open("output/" + dt.now().ctime().replace(":", "") + "output.txt", 'w')
debug = False

class World:
    gridsize = 2
    addQueue = None
    t = 1

    def __init__(self, gridsize, seed=None):
        if seed is None:
            seed = int(time.time())
        npr.seed(seed)
        print("SEED - " + str(seed))
        self.gridsize = gridsize
        self.addQueue = []
        self.preyCounter = []
        self.predCounter = []
        self.pos = np.empty((gridsize, gridsize), dtype=Animal)

    def step(self):
        if debug: #debug = true was used to log all animal interactions for troubleshooting purposes
            print("---------- BEGIN STEP " + str(self.t) + " ----------")
        self.addQueue.clear() #creates an empty array newly birthed objects can be stored
        if debug:
            print(
                "Prey count:" + str(self.preyCounter[self.t - 1]) + " Pred count:" + str(self.predCounter[self.t - 1]))
        animals = self.get_objects(Animal) #generates a list of all animals
        for ani in animals: #calls the pred/prey specific processes
            ani.step(self)
        for item in self.addQueue: #adds the newly 'born' animals to the population
            self.birth(item[0], item[1])
        for ani in animals:
            if not ani.alive:
                self.pos[ani.loc[0]][ani.loc[1]] = None  #removes dead animals from the grid
        self.t += 1 #keep track of how many steps the simulation has been running for
        self.preyCounter.append(len(self.get_objects(Prey))) #keeps track of the number of prey
        self.predCounter.append(len(self.get_objects(Predator))) #keeps track of the number of predators
        # self.cap_recap([10, 10], 5) used to test the accuracy of the capture-recapture sampling techinique (DNF)

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
    def cap_recap(self, loc, size):
        animals = [a for a in self.get_objects(Animal) if a.alive]
        for beast in animals:
            if loc[0] - size <= beast.loc[0] <= loc[0] + size and loc[1] - size <= beast.loc[1] <= loc[1] + size:
                beast.tags.append(self.t)

    def on_exit(self):
        animals = [a for a in self.get_objects(Animal) if a.alive]
        for beast in animals:
            pf.savetags("tags.csv", beast.tags)



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
    caughtDiseases = []
    immunities = []
    #pmove = 0
    def __init__(self, meanExpectancey, stdExpectancy, name):
        self.id = Animal.count
        Animal.count += 1
        self.lifeExpect = round(npr.normal(meanExpectancey, stdExpectancy))
        self.name = name
        self.mExpect = meanExpectancey
        self.stdExpect = stdExpectancy
        # self.tags = []
        #self.tags.append(self.name)

    def step(self, world):
        self.age += 1
        if self.age > self.lifeExpect:
            self.kill() #kills the animal if it is older that its specfic, individual lifespan.
            return
        if self.alive:
            self.move(world) #gives the animal the oppurtunity to move.

    def kill(self):
        if debug:
            print(
                "KILL: " + self.name + "_" + str(self.id) + " age:" + str(self.age) + " lexpect:" + str(self.lifeExpect))
        #pf.savetags("tags.csv", self.tags)
        #todo fix me
        self.alive = False


    def move(self, world):

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
        self.eat(world.get_objects(Prey), world)  # generates a list of the prey that could be eaten and passes to Predator.eat

    def eat(self, preytot, world):
        prey = []
        for x in np.arange(-self.killRange, self.killRange + 1):
            for y in np.arange(-self.killRange, self.killRange + 1):
                if isinstance(world.pos[(self.loc[0] + x) % world.gridsize][(self.loc[1] + y) % world.gridsize], Prey): #adds the prey to the list if it is within the kill range.
                    prey.append(world.pos[(self.loc[0] + x) % world.gridsize][(self.loc[1] + y) % world.gridsize])

        for meal in prey: #gives the predator the oppurtunity to kill each prey within its range
            if self.pkill > npr.uniform(): #rolls the dice to see if the prey is caught
                meal.kill()
                if npr.uniform() < self.pbirth: #rolls the dice to see if a new predator is born (if the prey is caught)
                    world.Spawn(Predator(self.mkill, self.stdkill, self.mgrow, self.stdgrow,
                                         self.mExpect, self.stdExpect, self.name, self.killRange), self.loc) # Spawn Baby next step



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


class Disease:
    ptransmit = 0  # if eat probability that transfer to newborn / killer

    pleathality = 0  # probability that disease kills animal each tick
    moveReduction = 1  # reduction is probablity of move

    pmutate = 0  # probability that every symtom will get worse
    mutation = 1
    pimmunity = 0  # probability that animal will become immune to this disease each tick

    def __init__(self, ptransmit, pletahility, pimmunity):
        self.ptransmit = ptransmit
        self.pleathality = pletahility
        self.pimmunity = pimmunity

    def step(self):
        if npr.uniform() < self.pmutate:
            self.pleathality *= self.mutation
            self.moveReduction *= self.mutation
            self.ptransmit *= self.mutation

