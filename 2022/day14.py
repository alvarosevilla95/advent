import time
start = time.time()
from itertools import count
from collections import defaultdict
from visualizer import PyGameVisualizer

data = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".strip()

data = open('inputs/day14.txt').read()

paths = [line.split(' -> ') for line in data.splitlines()]
paths = [[list(map(int, p.split(','))) for p in ps] for ps in paths]

grid: dict[tuple[int, int], str] = defaultdict(lambda: '.')
for path in paths:
    for pair in zip(path, path[1:]):
        if pair[0][0] == pair[1][0]:
            for y in range(min(pair[0][1], pair[1][1]), max(pair[0][1], pair[1][1])+1):
                grid[pair[0][0], y] = '#'
        else:
            for x in range(min(pair[0][0], pair[1][0]), max(pair[0][0], pair[1][0])+1):
                grid[x, pair[0][1]] = '#'

minx, maxx = min(x for x, _ in grid), max(x for x, _ in grid)
maxy = max(y for _, y in grid)
floor = maxy+2
minx -= 50
maxx += 50

with PyGameVisualizer(fps=0, lines=floor, cols=maxx-minx) as vis:
    p1 = True
    vis.palette = {'o': (255, 255, 255), '#': (0, 0, 0), '.': (0, 0, 255)}
    for i in count():
        pos = (500, 0)
        while True:
            nextpos = pos[0], pos[1]+1
            if nextpos[1] == floor:
                grid[pos] = 'o'
                break
            if p1 and nextpos[1] > maxy: 
                print(i)
                p1 = False
            if grid[nextpos] != '.': 
                nextpos = pos[0]-1, pos[1]+1
                if grid[nextpos] != '.': 
                    nextpos = pos[0]+1, pos[1]+1
                    if grid[nextpos] != '.':
                        if pos == (500, 0): 
                            print(i+1)
                            exit()
                        grid[pos] = 'o'
                        vis.draw_grid(grid, (minx, 0))
                        vis.get_frame()
                        break
            old = grid[pos]
            grid[pos] = 'o'
            # vis.draw_grid(grid, (minx, 0))
            # vis.get_frame()
            grid[pos] = old
            pos = nextpos
