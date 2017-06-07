import matplotlib

matplotlib.use("Agg")
import pygame
import monte
import numpy as np
from abc import ABC, abstractmethod
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
        screen = pygame.display.set_mode((self.width, self.height))
        font = pygame.font.Font(None, 25)
        self.add_to_stack(WorldScreen(25, self, 10, 0.6, 1.3, 1, [5.25, 1], 101, 1))
        #(self, size, window, alpha, beta, delta, gamma, s0, scale=1, steps=1):
        while self.isRunning:
            deltaTime = pygame.time.Clock().tick(60) / 1000
            for event in pygame.event.get():
                self.get_top_screen().input(event)
            screen.fill(BLACK)
            self.get_top_screen().update(deltaTime)
            self.get_top_screen().draw(deltaTime, screen)
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


class WorldScreen(Screen):
    border = 2.5
    stepTime = 0

    def __init__(self, size, window, alpha, beta, delta, gamma, s0, scale=1, steps=1):
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
        self.__world.randSpawnPrey(alpha / (self.__world.gridsize * steps), 0.1 / steps, 50 * steps, 1 * steps,
                                   int(preypop))  # Input data here
        self.__world.randSpawnPredator((self.__world.gridsize * beta) / (steps * scale), 0.1 / (steps * scale),
                                       delta / beta, 0.1 / scale, steps / gamma, steps,
                                       int(predpop), 3)
        self.grphdata = self.get_pop_graph()

    def input(self, event):
        Screen.input(self, event)
        if event == pygame.K_SPACE:
            self.__world.step()
            self.grphdata = self.get_pop_graph()

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
