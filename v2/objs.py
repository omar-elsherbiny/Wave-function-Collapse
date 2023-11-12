import json
from random import choice, randint

f = open('types.json', 'r')
types = json.load(f)
f.close()


class Tile:
    def __init__(self, ix, iy, types):
        self.x = ix
        self.y = iy
        self.available_types = types
        self.entropy = len(self.available_types)
        self.type = None

    def collapse(self):
        self.type = choice(self.available_types)

    def update_availability(self, allowed_types):
        for t in self.available_types:
            if t not in allowed_types:
                self.available_types.remove(t)


class Grid:
    def __init__(self, grid_size, tile_size, types):
        self.gs = grid_size
        self.ts = tile_size
        self.n_collapsed = 0
        self.tiles = [Tile(i, j, list(types.keys())) for i in range(grid_size) for j in range(grid_size)]

    def _index2coords(self, index):
        return [int((index-index % self.gs)/self.gs), index % self.gs]

    def _coords2index(self, x, y):
        return self.gs*y+x

    def get_min_entropy(self):
        min_entropy = min(self.tiles, key=lambda x: x.entropy).entropy
        return choice([i for i, t in enumerate(self.tiles) if t.entropy == min_entropy])
    
    def propagate(self,index):
        x,y=self._index2coords(index)
        tile_type=self.tiles[index].type
        if y>0:
            self.tiles[self._coords2index(x,y-1)].update_availability(types[tile_type]['top'])
        if y<self.gs-1:
            self.tiles[self._coords2index(x,y+1)].update_availability(types[tile_type]['bottom'])
        if x>0:
            self.tiles[self._coords2index(x-1,y)].update_availability(types[tile_type]['left'])
        if x<self.gs-1:
            self.tiles[self._coords2index(x+1,y)].update_availability(types[tile_type]['right'])


if __name__ == '__main__':
    grid = Grid(10, 10, types)
    for i in range(7):
        i=grid.get_min_entropy()
        grid.tiles[i].collapse()
        grid.propagate(i)
        for t in grid.tiles: print(t.type)
        print('\n')
