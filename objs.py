import pygame as pyg
import json
from random import choice, randint, choices

f = open('types.json', 'r')
types = json.load(f)
max_entropy = len(list(types.keys()))+1
f.close()


def format_img(path, size):
    return pyg.transform.rotate(pyg.transform.scale(pyg.image.load(path).convert_alpha(), (size, size)), choice([0, 90, 180, 270]))


class Tile:
    def __init__(self, ix, iy, types, size):
        self.x = ix
        self.y = iy
        self.s = size
        self.available_types = types
        self.type_probabilities={t:1 for t in types}
        self.entropy = len(self.available_types)
        self.type = None
        self.image = None

    def collapse(self):
        if self.entropy > 0:
            self.type = choices(self.available_types,weights=[self.type_probabilities[t] for t in self.available_types],k=1)[0]
            self.image = format_img(f"assets/{self.type}.png", self.s)
        self.entropy = max_entropy

    def update_availability(self, allowed_types):
        if self.type == None:
            type_names=[t[0] for t in allowed_types]
            new_types = []
            for t in self.available_types:
                if t in type_names:
                    new_types.append(t)
                    self.type_probabilities[t] += allowed_types[type_names.index(t)][1]
            self.available_types = new_types
            if len(self.available_types) > 0:
                self.entropy = len(self.available_types)
            else:
                self.entropy = max_entropy


class Grid:
    def __init__(self, grid_size, tile_size, types, n_nodes=1):
        self.gs = grid_size
        self.ts = tile_size
        self.n_collapsed = 0
        self.tiles = [Tile(i, j, list(types.keys()), tile_size)
                      for i in range(grid_size) for j in range(grid_size)]
        for i in range(n_nodes):
            ind = randint(0, grid_size**2-1)
            self.tiles[ind].collapse()
            self.propagate(ind)
            self.n_collapsed += 1

        self.default_tile = format_img('assets/glass.png', tile_size)

    def _index2coords(self, index):
        return [int((index-index % self.gs)/self.gs), index % self.gs]

    def _coords2index(self, x, y):
        return self.gs*x+y

    def get_min_entropy(self):
        min_entropy = min(self.tiles, key=lambda x: x.entropy).entropy
        if min_entropy >= max_entropy:
            return None
        return choice([i for i, t in enumerate(self.tiles) if t.entropy == min_entropy])

    def propagate(self, index):
        x, y = self._index2coords(index)
        tile_type = self.tiles[index].type
        if tile_type != None:
            if y > 0: self.tiles[self._coords2index(x, y-1)].update_availability(types[tile_type]['top'])
            if y < self.gs-1: self.tiles[self._coords2index(x, y+1)].update_availability(types[tile_type]['bottom'])
            if x > 0: self.tiles[self._coords2index(x-1, y)].update_availability(types[tile_type]['left'])
            if x < self.gs-1: self.tiles[self._coords2index(x+1, y)].update_availability(types[tile_type]['right'])

    def draw(self, screen):
        for tile in self.tiles:
            if tile.type == None:
                screen.blit(self.default_tile,
                            (tile.x*self.ts, tile.y*self.ts))
            else:
                screen.blit(tile.image, (tile.x*self.ts, tile.y*self.ts))

    def check_full_collapse(self):
        if self.n_collapsed < self.gs**2:
            return False
        return True


if __name__ == '__main__':
    pyg.init()
    pyg.display.set_mode((500, 500))
    grid = Grid(10, 10, types)
    for i, tile in enumerate(grid.tiles):
        print(i, grid._coords2index(tile.x, tile.y),
              grid._index2coords(i), (tile.x, tile.y))
    # for i in range(7):
    #     i = grid.get_min_entropy()
    #     grid.tiles[i].collapse()
    #     grid.propagate(i)
    #     for t in grid.tiles:
    #         print(t.type)
    #     print('\n')
