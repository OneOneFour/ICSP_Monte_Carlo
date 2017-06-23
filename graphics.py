import matplotlib

matplotlib.use("Agg")

import pygame
import sgc
from sgc.locals import *
import monte
import numpy as np
import time as tme
from abc import ABC, abstractmethod
from datetime import datetime as dt
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import lotkavolterra as lv
import scipy.stats as sps

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Window():
    isRunning = True
    width, height = 1700, 900
    screens = []

    def __init__(self):
        pygame.init()
        screen = sgc.surface.Screen((self.width, self.height))
        pygame.display.set_caption("Monte-Carlo predator prey simulation - Robert King & Matthew Cotton")
        self.font = pygame.font.Font(None, 25)
        self.add_to_stack(MenuScreen(self))
        # (self, size, window, alpha, beta, delta, gamma, s0, scale=1, steps=1):
        while self.isRunning:
            deltaTime = pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                self.get_top_screen().input(event)
            screen.fill(BLACK)
            self.get_top_screen().update(deltaTime / 1000)
            self.get_top_screen().draw(deltaTime / 1000, pygame.display.get_surface())
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
        # TODO add a repeat switch
        self.runButton = sgc.Button(label="Run", pos=(self.window.width / 2, self.window.height - 60))
        self.sizeScale = sgc.Scale(label="Size of the world grid", min=10, max=50, min_step=1, max_step=5, pos=(25, 25))
        self.killRangeSlider = sgc.Scale(label="Predator kill range slider", min=1, max=30, min_step=1, max_step=1,
                                         pos=(25, 25 + width * 6))
        self.initprey = sgc.Scale(label="Initial prey population", min=1, max=10 ** 2, min_step=1, max_step=10,
                                  pos=(25, 25 + width * 7))
        self.initpred = sgc.Scale(label="Initial predator population", min=1, max=10 ** 2, min_step=1, max_step=10,
                                  pos=(25, 25 + width * 8))
        self.alpha = sgc.InputBox(label="Alpha", pos=(25, 75))
        self.beta = sgc.InputBox(label="Beta", pos=(25, 100))
        self.gamma = sgc.InputBox(label="Gamma", pos=(25, 125))
        self.delta = sgc.InputBox(label="Delta", pos=(25, 150))
        self.run_lv_button = sgc.Button(label="Run LV",
                                        pos=(self.runButton.pos[0] + 200, self.runButton.pos[1]))
        self.lv_timelimit = sgc.Scale(label="Time limiter", min=1, max=50, min_step=1, max_step=5,
                                      pos=(400, 25))
        self.lv_scale = sgc.Scale(label="LV SCALE", min=1, max=50, min_step=1, max_step=5, pos=(400, 75))

        self.repeats = sgc.Scale(label="Monte-Carlo Repeats", min=1, max=200, min_step=1, max_step=5, pos=(400, 150))
        self.repeatButtons = sgc.Button(label="Run Fast", pos=(self.run_lv_button.pos[0] + 200, self.runButton.pos[1]))






        self.runButton.add(0)
        self.sizeScale.add(1)
        self.alpha.add(2)
        self.beta.add(3)
        self.gamma.add(4)
        self.delta.add(5)
        self.initprey.add(6)
        self.initpred.add(7)
        self.run_lv_button.add(8)
        self.killRangeSlider.add(9)
        self.lv_timelimit.add(10)
        self.lv_scale.add(11)
        self.repeats.add(12)
        self.repeatButtons.add(13)

    def input(self, event):
        Screen.input(self, event)
        sgc.event(event)
        if self.sizeScale.value != self.lastScaleVal:
            self.initpred.config(max=self.sizeScale.value ** 2)
            self.initprey.config(max=self.sizeScale.value ** 2)
            self.lv_scale.config(max=self.sizeScale.value * 50)
        if event.type == GUI:
            if event.gui_type == "click" and event.widget is self.runButton:
                if self.initprey.value + self.initpred.value > self.sizeScale.value ** 2:
                    print("Population too large for configuration, please select smaller values of predators and prey.")
                else:
                    self.window.add_to_stack(
                        WorldScreen(self.sizeScale.value, self.window, float(self.alpha.text),
                                    float(self.beta.text), float(self.gamma.text), float(self.delta.text),
                                    [self.initprey.value, self.initpred.value], self.killRangeSlider.value))
            elif event.gui_type == "click" and event.widget is self.run_lv_button:
                self.tmp_world = monte.World(self.sizeScale.value)
                self.tmp_world.randSpawnPrey(float(self.alpha.text), 0.1, 50, 1,
                                             self.initprey.value)
                self.tmp_world.randSpawnPredator(float(self.beta.text) / self.initpred.value, 0.1 / self.initpred.value,
                                                 float(self.delta.text) / float(self.beta.text) * (
                                                 self.initpred.value / self.initprey.value),
                                                 0.1 * (self.initpred.value / self.initprey.value),
                                                 1 / float(self.gamma.text), 1, self.initpred.value,
                                                 self.killRangeSlider.value)
                for i in range(self.lv_timelimit.value):
                    self.tmp_world.step()
                s0 = [self.initprey.value / self.lv_scale.value, self.initpred.value / self.lv_scale.value]
                t, ans = lv.lotkavolterragraph(float(self.alpha.text), float(self.beta.text), float(self.gamma.text),
                                               float(self.delta.text), s0, self.lv_timelimit.value + 1)

                ans *= self.lv_scale.value
                fig = plt.figure(figsize=[4.8, 4.8], dpi=100)
                fig.gca().plot(t, ans[:, 0], "g-")
                fig.gca().plot(t[::10], self.tmp_world.preyCounter, "r-")
                fig.savefig("output/" + dt.now().ctime().replace(":", " ") + "output_lvpry.png")
                fig2 = plt.figure(figsize=[4.8, 4.8], dpi=100)
                fig2.gca().plot(t, ans[:, 1], "g-")
                fig2.gca().plot(t[::10], self.tmp_world.predCounter, "r-")
                fig2.savefig("output/" + dt.now().ctime().replace(":", " ") + "output_lvpred.png")
                chi = sps.chisquare(self.tmp_world.preyCounter, ans[::10, 0])
                print(chi)
                plt.close(fig2)
                plt.close(fig)
            elif event.gui_type == "click" and event.widget is self.repeatButtons:
                alp, bet, gam, delt = float(self.alpha.text), float(self.beta.text), float(self.gamma.text), float(
                    self.delta.text)
                mstprey = []
                mstpred = []
                time = tme.time()
                for i in range(self.repeats.value):
                    world = monte.World(self.sizeScale.value, int(time))
                    world.randSpawnPrey(alp, 0.1, 50, 1, self.initprey.value)
                    world.randSpawnPredator(bet, 0.1 / self.initpred.value,
                                            delt / bet * (self.initpred.value / self.initprey.value),
                                            0.1 * self.initprey.value / self.initpred.value,
                                            1 / gam * (self.sizeScale.value / (2 * self.killRangeSlider.value + 1)),
                                            1.0,
                                            self.initpred.value, self.killRangeSlider.value)
                    for t in range(self.lv_timelimit.value):
                        world.step()
                    mstpred.append(world.predCounter)
                    mstprey.append(world.preyCounter)
                    time += 1
                # get median - sort each point in terms of value
                mstprey = np.swapaxes(mstprey, 0, 1)
                mstpred = np.swapaxes(mstpred, 0, 1)
                for t in range(len(mstprey)):
                    mstprey[t] = np.sort(mstprey[t])
                    mstpred[t] = np.sort(mstpred[t])
                # plot median graph and percentiles
                preypercent = plt.figure(figsize=[4.9, 4.9], dpi=100)
                predpercent = plt.figure(figsize=[4.9, 4.9], dpi=100)
                for percentile in np.arange(0.25, 1, 0.25):
                    preypercent.gca().plot(np.arange(0, self.lv_timelimit.value + 1),
                                           mstprey[:, int(percentile * self.repeats.value)])
                    predpercent.gca().plot(np.arange(0, self.lv_timelimit.value + 1),
                                           mstpred[:, int(percentile * self.repeats.value)])
                preypercent.savefig("output/" + dt.now().ctime().replace(":", " ") + "mc_pry_output.png")
                predpercent.savefig("output/" + dt.now().ctime().replace(":", " ") + "mc_pred_output.png")
                plt.close(preypercent)
                plt.close(predpercent)

    '''         
    
    
    def calculateLVconstants(self):
        alpha = self.mGrowSlider.value / (100)
        beta = self.mKillSlider.value / (100)
        delta = beta * (self.mEatSlider.value / (100))
        gamma = 1 / (self.predLifeSlider.value)

        return alpha, beta, delta, gamma
'''
    def draw(self, delta, screen):
        pass

    def update(self, delta):
        sgc.update(delta * 1000)
        self.lastScaleVal = self.sizeScale.value


class WorldScreen(Screen):
    border = 1
    stepTime = 0

    def __init__(self, size, window, alpha, beta, gamma, delta, s0, killrange,
                 scale=1, steps=1):
        self.window = window
        self.__world = monte.World(size)
        self.timeToStep = self.stepTime
        self.steps = steps
        preypop = s0[0] * scale
        predpop = s0[1] * scale
        if size ** 2 < (predpop + preypop):
            print("Populations reduced as grid not large enough.")
            excess = predpop + preypop - size ** 2
            preypop -= np.ceil((s0[0] / (s0[0] + s0[1])) * excess)
            predpop -= np.ceil((s0[1] / (s0[0] + s0[1])) * excess)
            print("Populations reduced to Prey =", preypop, "Predators =", predpop)
        self.__world.randSpawnPrey(alpha, 0.1, 50, 1.0, s0[0])
        self.__world.randSpawnPredator(beta, 0.1, (delta / beta), 0.1, 1 / gamma * (size / (2 * killrange + 1)), 1.0,
                                       s0[1], killrange)
        self.grphdata = self.get_pop_graph()

    def input(self, event):
        Screen.input(self, event)
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.grphdata[2].savefig("output/" + dt.now().ctime().replace(":", " ") + "output.png")
            plt.close(self.grphdata[2])
            self.window.pop_stack()
            #self.world.on_exit()

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
        fig = plt.figure(figsize=[8.5, 9], dpi=100)
        time = np.linspace(0, self.__world.t, self.steps * self.__world.t)
        fig.gca().plot(time, self.__world.preyCounter, "g-")
        fig.gca().plot(time, self.__world.predCounter, "r-")
        fig.gca().set_xlabel("Time")
        fig.gca().set_ylabel("Population")
        if self.__world.t > 50:
            fig.gca().set_xlim([self.__world.t - 50, self.__world.t])
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        return renderer.tostring_rgb(), canvas.get_width_height(), fig

    def update(self, delta):
        self.timeToStep -= delta
        #self.__world.cap_recap([self.__world.gridsize / 2, self.__world.gridsize / 2], 2)


        if self.timeToStep <= 0:
            self.__world.step()
            self.timeToStep = self.stepTime
            if self.grphdata is not None:
                plt.close(self.grphdata[2])
            self.grphdata = self.get_pop_graph()


w = Window()
