import matplotlib

matplotlib.use("Agg")

import pygame
import sgc
from sgc.locals import *
import monte
import numpy as np
from abc import ABC, abstractmethod
from datetime import datetime as dt
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Window():
    isRunning = True
    width, height = 960, 480
    screens = []

    def __init__(self):
        pygame.init()
        screen = sgc.surface.Screen((self.width, self.height))
        font = pygame.font.Font(None, 25)
        self.add_to_stack(MenuScreen(self))
        #(self, size, window, alpha, beta, delta, gamma, s0, scale=1, steps=1):
        while self.isRunning:
            deltaTime = pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                self.get_top_screen().input(event)
            screen.fill(BLACK)
            self.get_top_screen().update(deltaTime)
            self.get_top_screen().draw(deltaTime, pygame.display.get_surface())
            pygame.display.flip()

    def add_to_stack(self, screen):
        self.screens.append(screen)

    def delete_top_stack(self):
        self.pop_stack()

    def pop_stack(self):
        if len(self.screens) < 1:
            return
        return self.screens.pop()

    def get_top_screen(self):
        return self.screens[-1]

    def switch_screen(self, screen):
        self.delete_top_stack()
        self.add_to_stack(screen)


class Screen(ABC):
    window = None

    @abstractmethod
    def input(self, event):  # take user input here
        if event.type == pygame.QUIT:
            self.window.isRunning = False

    @abstractmethod
    def draw(self, delta, screen):  # draw output here
        pass

    @abstractmethod
    def update(self, delta):  # do any animations or other pre-draw calculations here - may not be needed
        pass


class MenuScreen(Screen):
    lastScaleVal = 10

    def __init__(self, window):
        self.window = window
        width = 35
        self.runButton = sgc.Button(label="Run", pos=(self.window.width / 2, self.window.height - 60))
        self.sizeScale = sgc.Scale(label="Size of the world grid", min=10, max=30, min_step=1, max_step=5, pos=(25, 25))
        self.mGrowSlider = sgc.Scale(label="Prey growth probability", min=0, max=100, min_step=1, max_step=10,
                                     pos=(25, 25 + width * 1))
        self.mLifeSlider = sgc.Scale(label="Prey mean life expectancy", min=1, max=20, min_step=0.5, max_step=2,
                                     pos=(25, 25 + width * 2))
        self.mKillSlider = sgc.Scale(label="Predator kill probability", min=0, max=100, min_step=1, max_step=10,
                                     pos=(25, 25 + width * 3))
        self.mEatSlider = sgc.Scale(label="Predator eat given kill probability", min=0, max=100, min_step=1,
                                    max_step=10, pos=(25, 25 + width * 4))
        self.predLifeSlider = sgc.Scale(label="Predator mean life expectancy", min=1, max=20, min_step=0.5, max_step=2,
                                        pos=(25, 25 + width * 5))
        self.killRangeSlider = sgc.Scale(label="Predator kill range slider", min=1, max=5, min_step=1, max_step=1,
                                         pos=(25, 25 + width * 6))
        self.initprey = sgc.Scale(label="Initial prey population", min=0, max=10 ** 2, min_step=1, max_step=10,
                                  pos=(25, 25 + width * 7))
        self.initpred = sgc.Scale(label="Initial predator population", min=0, max=10 ** 2, min_step=1, max_step=10,
                                  pos=(25, 25 + width * 8))

        self.runButton.add(0)
        self.sizeScale.add(1)
        self.mGrowSlider.add(2)
        self.mLifeSlider.add(3)
        self.mKillSlider.add(4)
        self.mEatSlider.add(5)
        self.predLifeSlider.add(6)
        self.killRangeSlider.add(7)
        self.initprey.add(8)
        self.initpred.add(9)

    def input(self, event):
        sgc.event(event)
        if self.sizeScale.value != self.lastScaleVal:
            self.initpred.config(max=self.sizeScale.value ** 2)
            self.initprey.config(max=self.sizeScale.value ** 2)

        if event.type == GUI:
            if event.gui_type == "click" and event.widget is self.runButton:
                if self.initprey.value + self.initpred.value > self.sizeScale.value ** 2:
                    print("Population too large for configuration, please select smaller values of predators and prey.")
                else:
                    self.window.add_to_stack(
                        WorldScreen(self.sizeScale.value, self.window, self.mGrowSlider.value / 100,
                                    self.mLifeSlider.value, self.mKillSlider.value / 100, self.mEatSlider.value / 100,
                                    self.predLifeSlider.value, self.killRangeSlider.value,
                                    [self.initprey.value, self.initpred.value]))

    def draw(self, delta, screen):
        pass

    def update(self, delta):
        sgc.update(delta * 1000)
        self.lastScaleVal = self.sizeScale.value


class WorldScreen(Screen):
    border = 1
    stepTime = 0

    def __init__(self, size, window, prey_grow, prey_life, pred_catch, pred_eat, pred_life, pred_kill_range, s0,
                 scale=1, steps=1):
        self.window = window
        self.__world = monte.World(size)
        self.timeToStep = self.stepTime
        self.steps = steps
        preypop = s0[0] * scale
        predpop = s0[1] * scale
        if size**2 < (predpop + preypop):
            print ("Populations reduced as grid not large enough.")
            excess = predpop + preypop - size**2
            preypop -= np.ceil((s0[0]/(s0[0]+s0[1]))*excess)
            predpop -= np.ceil((s0[1]/(s0[0]+s0[1]))*excess)
            print ("Populations reduced to Prey =", preypop, "Predators =", predpop)
        self.__world.randSpawnPrey(prey_grow, 0.2, prey_life, 1.5, s0[0])  # Input data here
        self.__world.randSpawnPredator(pred_catch, 0.2, pred_eat, 0.2, pred_life, 1.5, s0[1], pred_kill_range)
        self.grphdata = self.get_pop_graph()

    def input(self, event):
        Screen.input(self, event)
        if event.type == pygame.QUIT:
            self.grphdata[2].savefig("output/" + dt.now().ctime().replace(":", " ") + "output.png")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.grphdata[2].savefig("output/" + dt.now().ctime().replace(":", " ") + "output.png")
                self.window.pop_stack()

    def draw(self, delta, screen):
        width = self.window.height / self.__world.gridsize
        for x in range(self.__world.gridsize):
            for y in range(self.__world.gridsize):
                pygame.draw.rect(screen, WHITE,
                                 pygame.Rect(x * width + self.border, y * width + self.border, width - self.border * 2,
                                             width - self.border * 2),
                                 0)  # can change to surface.fill at some point in the future...
                if isinstance(self.__world.pos[x][y], monte.Predator) and self.__world.pos[x][y].alive:
                    pygame.draw.circle(screen, RED, (int(width * (x + 0.5)), int(width * (y + 0.5))), int(width / 2))
                if isinstance(self.__world.pos[x][y], monte.Prey):
                    pygame.draw.circle(screen, GREEN, (int(width * (x + 0.5)), int(width * (y + 0.5))), int(width / 2))
                    # if cell contains predator draw blue dot else draw red4
        if self.grphdata is not None:
            grph = pygame.image.fromstring(self.grphdata[0], self.grphdata[1], 'RGB')
            screen.blit(grph, (self.window.height, 0))

    def get_pop_graph(self):
        fig = plt.figure(figsize=[4.8, 4.8], dpi=100)
        time = np.linspace(0, self.__world.t, self.steps * self.__world.t)
        fig.gca().plot(time, self.__world.preyCounter, "g-")
        fig.gca().plot(time, self.__world.predCounter, "r-")
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        return renderer.tostring_rgb(), canvas.get_width_height(), fig

    def update(self, delta):
        self.timeToStep -= delta

        if self.timeToStep <= 0:
            self.__world.step()
            self.timeToStep = self.stepTime
            if self.grphdata is not None:
                plt.close(self.grphdata[2])
            self.grphdata = self.get_pop_graph()


w = Window()
