#Imports
import pygame as pyg
from sys import exit as syexit
from objs import *

pyg.init()

#Globals
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BG_COLOR=(20,20,20)
SCREEN = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pyg.font.Font("freesansbold.ttf", 20)

#Main
def main():
    clock = pyg.time.Clock()

    #MAIN LOOP
    run = True
    while run:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                syexit()
            elif event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass

        SCREEN.fill(BG_COLOR)

        

        clock.tick(60)
        pyg.display.set_caption(f"Rendering--{int(clock.get_fps())}")
        pyg.display.update()

def unpyg():
    pass

if __name__=='__main__':
    unpyg()