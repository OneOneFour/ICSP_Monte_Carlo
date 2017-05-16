import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
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
        World.addQueue.clear()
        World.t += 1
        for key in World.population:
            for ani in World.population[key]:
                ani.step()
        #cull the old
        for key in World.population:
            if key in World.addQueue:
                World.population[key].extend(World.addQueue[key])
            for ani in World.population[key]:
                if not ani.alive:
                    World.population[key].remove(ani)
        self.predCounter.append(len(self.population["Predator"]))
        self.preyCounter.append(len(self.population["Prey"]))
    @staticmethod
    def getPrey():
        return World.population['Prey']
    @staticmethod
    def Spawn(animal):
        if animal.name not in World.addQueue:
            World.addQueue[animal.name] = []
        World.addQueue[animal.name].append(animal)


class Animal:
    name = "Animal"
    alive = True
    mExpect = 0
    stdExpect = 0
    lifeExpect = 0 # Mean age of death #std dev is 1.5 steps?
    age = 0

    def __init__(self,meanExpectancey,stdExpectancy,name):
        self.lifeExpect = np.floor(npr.normal(meanExpectancey,stdExpectancy))
        self.name = name
        self.mExpect = meanExpectancey
        self.stdExpect = stdExpectancy

    def step(self):
        self.age+= 1
        if self.age > self.lifeExpect:
            self.kill()
        return

    def kill(self):
        self.alive = False


class Predator(Animal):
    expectedKill = 0
    killDev = 0
    expectedGrowFromKill=0
    growFromKillDev =0

    def __init__(self,killExpect,killDev,expectedGrowFromKill,growFromKillDev,mExpect,stdExpect,name):
        Animal.__init__(self,mExpect,stdExpect,self.name)
        self.expectedKill = killExpect
        self.name = name
        self.killDev = killDev
        self.expectedGrowFromKill = expectedGrowFromKill
        self.growFromKillDev = growFromKillDev

    def step(self):
        self.eat(World.getPrey())#get the prey
        Animal.step(self)

    def eat(self,prey):
        for meal in range(int(npr.normal(self.expectedKill,self.killDev))):
            if meal >= len(prey):
                break
            if not prey[meal].alive:
                continue
            prey[meal].kill()
            for baby in range(int(npr.normal(self.expectedGrowFromKill,self.growFromKillDev))):
                World.Spawn(Predator(self.expectedKill,self.killDev,self.expectedGrowFromKill,self.growFromKillDev,self.mExpect,self.stdExpect,self.name))
                #Spawn Baby next step


class Prey(Animal):
    expectGrow = 0 #mean number of babies each step
    growDev = 0

    def __init__(self,expectGrow,growDev,mExpect,stdExpect,name):
        Animal.__init__(self,mExpect,stdExpect,name)
        self.expectGrow = expectGrow
        self.growDev = growDev

    def step(self):
        self.rollGrow()
        Animal.step(self)

    def rollGrow(self):
        for baby in range(int(npr.normal(self.expectGrow,self.growDev))):
            World.Spawn(Prey(self.expectGrow,self.growDev,self.mExpect,self.stdExpect,self.name))


world = World()
world.population['Predator'] = [Predator(3,0.2,1.5,0.2,10,1,"Predator")]
world.population['Prey'] = [Prey(1.5,0.2,20,1,"Prey")]
for i in range(30):
    world.step()

plt.plot(np.arange(0,30,1),world.preyCounter)
plt.plot(np.arange(0,30,1),world.predCounter)
