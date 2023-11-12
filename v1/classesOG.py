import pygame as pyg
import json
from random import choice

types=[]
with open("tile_types.json", 'r') as f:
    types = json.load(f)

class Tile:
    def __init__(self, x, y, size):
        self.x, self.y = x, y
        self.size = size
        self.image = self.format_image('glass.png')
        self.rect = pyg.Rect(self.x*size, self.y*size, size,size)

        self.type = None
        self.available_types=types[:]
        self.entropy=len(self.available_types)
    
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
        self.tiles = [[None for j in range(grid_size)] for i in range(grid_size)]
        self.init_grid_tiles()
        self.n_collapsed = 0

    def init_grid_tiles(self):
        self.n_collapsed = 0
        for y,r in enumerate(self.tiles):
            for x,c in enumerate(r):
                self.tiles[y][x]=Tile(x,y,self.ts)

    
    def draw_tiles(self, screen):
        for r in self.tiles:
            for tile in r:
                tile.draw(screen)
    
    def get_min_entropy(self):
        min_tile=None
        min_entropy=None
        for r in self.tiles:
            for tile in r:
                if tile.type != None:
                    continue
                if min_tile == None:
                    min_tile = [(tile.x, tile.y)]
                    min_entropy = tile.entropy
                elif min_entropy > tile.entropy:
                    min_tile = [(tile.x, tile.y)]
                    min_entropy = tile.entropy
                elif min_entropy == tile.entropy:
                    min_tile.append((tile.x, tile.y))
        return choice(min_tile)
    
    def check_full_collapse(self):
        if self.n_collapsed < self.gs**2:
            return False
        return True
                
    def get_non_dag_neighbours(self,x,y):
        return [(x+a[0], y+a[1]) for a in 
                    [(-1,0), (1,0), (0,-1), (0,1)] 
                    if ( (0 <= x+a[0] < self.gs) and (0 <= y+a[1] < self.gs))]
    def get_all_neighbours(self,x,y):
        return [(x2, y2) for x2 in range(x-1, x+2)
                               for y2 in range(y-1, y+2)
                               if (-1 < x <= self.gs and
                                   -1 < y <= self.gs and
                                   (x != x2 or y != y2) and
                                   (0 <= x2 <= self.gs) and
                                   (0 <= y2 <= self.gs))]
    ##################################################################
    def generate(self):
        while self.check_full_collapse() == False:
            selected_index = self.get_min_entropy()
            selected_tile = self.tiles[selected_index[1]][selected_index[0]]
            selected_tile.collapse()
            self.n_collapsed += 1
            neighbours_index = self.get_non_dag_neighbours(selected_tile.x,selected_tile.y)
            for neighbour in neighbours_index:
                self.tiles[neighbour[1]][neighbour[0]].remove_availability(selected_tile.type['allowed_neighbours'])