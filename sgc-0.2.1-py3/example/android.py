"""
This example is a modification of the helloworld.py example to work with
Android using PS4A.

To use this, you should create a directory structure like this:
+-project/
  +-external/
  | +-arial.ttf
  | +-cour.ttf
  +-internal/
    +-sgc/ (the sgc subfolder for the toolkit)
    +-main.py (this file; must rename to main.py)

Default system fonts are not currently supported, so you need to provide some
fonts in the 'external' directory ('arial.ttf' and 'cour.ttf' in this example).

"""

import sys

import sgc
from sgc.locals import *

import pygame
from pygame.locals import *

pygame.display.init()
pygame.font.init()

# Android initialisation
import android
android.init()
# Used to exit the application, see below
android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

# Setup fonts, as PGS4A can't use default system fonts
# Font files should be located in 'external' directory
fonts = {"widget": "arial.ttf", "title": "arial.ttf", "mono": "cour.ttf"}
sgc.Font.set_fonts(fonts)

screen = sgc.surface.Screen((400,480))

clock = pygame.time.Clock()

btn = sgc.Button(label="Clicky", pos=(100, 100))
btn.add(0)

# Need a main() function in pgs4a
def main():
    while True:
        # A PGS4A program must include these two lines
        if android.check_pause():
            android.wait_for_resume()
        
        time = clock.tick(30)

        for event in pygame.event.get():
            sgc.event(event)
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                # Alternate way to exit the program in Android - back button
                sys.exit()
                
        screen.fill((0,0,0))
        sgc.update(time)
        pygame.display.flip()
