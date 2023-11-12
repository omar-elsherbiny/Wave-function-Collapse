import pygame as pyg
import json
from random import choice, randint

types=[]
with open("tile_types.json", 'r') as f:
    types = json.load(f)

class Tile:
    def __init__(self, x, y, size, available_types):
        self.x, self.y = x, y
        self.size = size
        self.image = self.format_image('glass.png')
        self.rect = pyg.Rect(self.x*size, self.y*size, size,size)

        self.type = None
        self.available_types=available_types
    
    def remove_availability(self, allowed_types):
        for type in self.available_types:
            if type['name'] not in allowed_types:
                self.available_types.remove(type)
                self.entropy = len(self.available_types)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def collapse(self):
        self.type = choice(self.available_types)
        self.image = self.format_image(self.type['image'])

    def format_image(self, path):
        p=path
        if isinstance(path,list):
            p=choice(path)
        return pyg.transform.rotate(pyg.transform.scale(pyg.image.load(p).convert_alpha(),(self.size,self.size)),choice([0,90,180,270]))
        

class Grid:
    def __init__(self, grid_size, tile_size):
        self.gs = grid_size
        self.ts = tile_size
        self.tiles = []
        self.n_collapsed = 0
        self.init_grid_tiles()

    def init_grid_tiles(self):
        self.tiles = []
        self.n_collapsed = 0
        self.tiles.append((len(self.available_types),Tile(randint(0,self.gs-1),randint(0,self.gs-1),self.ts, types[:])))
    
    def draw_tiles(self, screen):
        for tile in self.drawn_tiles:
            tile.draw(screen)

    def check_full_collapse(self):
        if self.n_collapsed < self.gs**2:
            return False
        return True
    
    def get_neighbours(self,x,y):
        return [(x+a[0], y+a[1]) for a in 
                    [(-1,0), (1,0), (0,-1), (0,1)] 
                    if ( (0 <= x+a[0] < self.gs) and (0 <= y+a[1] < self.gs))]

    def generate(self):
        while self.check_full_collapse() == False:
            self.tiles.sort(key=lambda x: x.entropy)
            selected_tile = self.tiles[0]
            selected_tile.collapse()
            neighbours_index = self.get_neighbours(selected_tile.x,selected_tile.y)
            for neighbour in neighbours_index:
                e,an = self.get_entropy(selected_tile.type['allowed_neighbours']),)
                self.tiles.put((0,Tile(neighbour[0],neighbour[1],self.ts)))