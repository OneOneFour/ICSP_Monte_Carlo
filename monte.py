import numpy as np
import random as rn
import pygame
class Grid:
    X,Y = None
    t = 0
    def __init__(self,X,Y,):
        self.X = X
        self.Y = Y
    def step(self): #step simulation by one
        self.t+=1
        #Tell visual to update
    def showGrid(self):
        for x in range(self.X):
            for y in range(self.Y):

class Animal:
    x,y = None
    __pmove = 0 #Probabilty of moving from square this step
    __pbirth = 0 #Probability of giving birth this step
    __pdie = 0 #Probability of dieing
    __pcatch = 0 #Probability of catching if in same cell
    __pabsorb= 0 # Probability of growing given a catch (Quite high)
    __age = 0
    def __init__(self):
        