#Imports
import pygame as pyg
import sys
from classesOG import *

pyg.init()

#Globals
SCREEN_HEIGHT = 640
SCREEN_WIDTH = 640
SCREEN = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pyg.display.set_caption("wave function collapse")
FONT = pyg.font.Font("freesansbold.ttf", 20)

anim=True
gs=20

#Main
def main():
    clock = pyg.time.Clock()

    grid = Grid(gs,round(640/gs))

    #MAIN LOOP
    run = True
    while run:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    grid.init_grid_tiles()
                    grid.generate()

        SCREEN.fill((30, 30, 30))

        grid.draw_tiles(SCREEN)

        clock.tick(30)
        pyg.display.update()

main()