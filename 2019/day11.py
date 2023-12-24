import time
import itertools
import curses
from intcode import IntcodeVm

def run_bot(screen):
    f = open('inputs/day11.txt').read()
    vm = IntcodeVm(f)

    ds = '^>v<'
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    max_x, max_y = 50, 12
    i, j, d = 0, max_y//2, 0
    grid = [[0 for x in range(max_x)] for y in range(max_y)]

    grid[j][i] = 1

    def grid_in():
        while True:
            yield grid[j][i]
    g_in = grid_in()

    while True:
        p = vm.eval(g_in)
        if p is None: break
        grid[j][i] = p
        p = vm.eval(g_in)
        if p is None: break
        if p == 0: p = -1
        d = (d+p) % 4
        i += dx[d]
        j += dy[d]

        v = grid[j][i]
        grid[j][i] = 2
        draw(screen, grid, (i,j), ds[d])
        grid[j][i] = v
    time.sleep(10)

def render(screen, f, *args):
    curses.curs_set(0)
    f(screen, *args)
    curses.curs_set(1)

def draw(screen, grid, r, d):
    for i, r in enumerate(reversed(grid)):
        for j, p in enumerate(r):
            screen.addstr(i, j, d if p == 2 else '#' if p == 1 else ' ')
    screen.refresh()
    time.sleep(0.02)

curses.wrapper(lambda s: render(s,run_bot))
