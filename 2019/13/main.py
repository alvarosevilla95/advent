import time
import curses
from intcode import IntcodeVm, parse_memory
from random import randint

tiles = [(' ', lambda: 1), ('#', lambda: randint(2,4)), ('X', lambda: randint(2,4)), ('_', lambda: 4), ('0', lambda: 4)]

def agent(grid):
    while True: 
        for r in grid:
            for j, p in enumerate(r):
                if p == tiles[3]: px = j
                if p == tiles[4]: bx = j
        yield((px<bx)-(px>bx))
        # time.sleep(0.08)

def run_game(screen, data):
    mem = parse_memory(data)
    mem[0] = 2
    vm = IntcodeVm(mem)

    grid = [[tiles[0] for _ in range(48)] for _ in range(24)]
    score = 0
    ai = agent(grid)

    i = 0
    while True:
        i+=1
        x = vm.eval(ai)
        if x is None: break
        y = vm.eval(ai)
        t = vm.eval(ai)
        if x == -1 and y == 0: score = t
        else: grid[y][x] = tiles[t]
        if i % 1==0: 
            draw(screen, grid, score)
            time.sleep(0.005)
    draw(screen, grid, score)
    time.sleep(10)


def render(screen, f, *args):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    f(screen, *args)
    curses.curs_set(1)

def draw(screen, grid, score):
    for i, r in enumerate(grid):
        for j, p in enumerate(r):
            l, c = p
            screen.addstr(i, j, p[0], curses.color_pair(p[1]()))
    for i in range(44):
        screen.addstr(len(grid)-1, i, '#', curses.color_pair(tiles[1][1]())) 
    screen.addstr(len(grid), 0, "Current Score: " + str(score), curses.A_BOLD)
    screen.refresh()

f = open('space-invaders.intc').read()
curses.wrapper(lambda s: render(s, run_game, f))
