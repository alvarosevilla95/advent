from intcode import IntcodeVm
import sys
import time
import curses
from math import inf

def closest(points):
    closest = min(points, key=lambda p: abs(sy - p[0]) + abs(sx - p[1]))
    return closest[2]+1, closest[1], closest[0]

def choose_next(grid, x,y):
    dirs = list(zip([1, -1, 0, 0],[0, 0, 1, -1]))
    neighbors = map(lambda d: [y+d[0],x+d[1], dirs.index(d)], dirs)
    valid = [n for n in neighbors if grid[n[0]][n[1]] >= 0]
    new = [n for n in valid if grid[n[0]][n[1]] == 0]
    if new: return closest(new)
    grid[y][x] = -grid[y][x]
    if not valid: return  -1, -1, -1
    return closest(valid)

def map_ship(screen=None):
    grid = [[0 for _ in range(lenx)] for _ in range(leny)]
    x, y = sx, sy
    # grid[y][x] = 8
    while True:
        if grid[y][x] == 0: grid[y][x] = 1
        d, nx, ny = choose_next(grid, x, y)
        if d == -1: # done
            break
        out = vm.eval(IntcodeVm.pipe_one(d))
        if out == 0:
            grid[ny][nx] = -3
            continue
        x, y = nx, ny
        if screen: draw(screen, grid)
        if out == 2:
            # time.sleep(10)
            grid[y][x] = 2
            # break
    grid = [[-p if p < 0  else p if p != 0 else -3 for p in r] for r in grid]
    if screen: 
        draw(screen, grid)
        time.sleep(0.5)
    fill(screen, grid)
    return grid

def dijkstra(grid):
    unvisited = [(y,x) for x in range(lenx) for y in range(leny) if grid[y][x] < 3]
    distances = { u : inf for u in unvisited }
    distances[sy,sx] = 0
    while len(unvisited) > 0:
        curr = min(unvisited, key=lambda x: distances[x])
        dirs = list(zip([1, -1, 0, 0],[0, 0, 1, -1]))
        neighbors = map(lambda d: (curr[0]+d[0],curr[1]+d[1]), dirs)
        for n in neighbors:
            if n[0] < 0 or n[1] < 0: continue
            if n[0] >= leny or n[1] >= lenx: continue
            if grid[n[0]][n[1]] < 3: 
                distances[n] = min(distances[n], distances[curr] + 1)
        unvisited.remove(curr)
    return distances[35,31]

def is_full(grid):
    for r in grid:
        for p in r:
            if p == 1: return False
    return True

def fill(screen, grid):
    sx, sy = 31, 35
    grid[sy][sx] = 4
    i = 0
    while not is_full(grid):
        i += 1
        draw(screen, grid)
        time.sleep(0.2)
        for y, r in enumerate(grid):
            for x, p in enumerate(r):
                if p == 4: 
                    dirs = list(zip([1, -1, 0, 0],[0, 0, 1, -1]))
                    neighbors = map(lambda d: (y+d[0],x+d[1]), dirs)
                    for n in neighbors:
                        if grid[n[0]][n[1]] == 1: grid[n[0]][n[1]] = -4
        for y, r in enumerate(grid):
            for x, p in enumerate(r):
                if p == -4: 
                    r[x] = 4

    return i

def render(screen, f, *args):
    curses.use_default_colors()
    curses.curs_set(0)
    f(screen, *args)
    curses.curs_set(1)

def draw(screen, grid):
    for i, r in enumerate(reversed(grid)):
        for j, p in enumerate(r):
            if p == 0: p = ' '
            elif abs(p) == 1: p = ' '
            elif p == -1: p = ' '
            elif abs(p) == 2: p = '0'
            elif abs(p) == 3: p = '#'
            elif abs(p) == 4: p = '0'
            screen.addstr(i, j, str(p))
    screen.refresh()

lenx, leny = 41, 41
sx, sy = lenx//2-1, leny//2-1

f = open('input.txt').read()
vm = IntcodeVm(f)

# lab = map_ship()
# dijkstra(lab)
# print(dijkstra(lab))
curses.wrapper(render, map_ship)
