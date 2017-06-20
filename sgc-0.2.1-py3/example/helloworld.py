import sgc
from sgc.locals import *

import pygame
from pygame.locals import *

pygame.display.init()
pygame.font.init()

screen = sgc.surface.Screen((640,480))

clock = pygame.time.Clock()

btn = sgc.Button(label="Clicky", pos=(100, 100))
btn.add(0)

while True:
    time = clock.tick(30)

    for event in pygame.event.get():
        sgc.event(event)
        if event.type == QUIT:
            exit()

    screen.fill((0,0,0))
    sgc.update(time)
    pygame.display.flip()
