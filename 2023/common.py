import regex as re, numpy as np, sys, os, time, curses
from math import prod, floor, ceil, lcm, inf
from random import randint
from functools import reduce, cache
from itertools import chain, combinations, takewhile, count
from collections import defaultdict, deque
from multiprocessing import Pool
from heapq import heappop, heappush


sys.setrecursionlimit(100000) # heh

def draw_grid(screen, grid, rate, fdraw, *args):
    if rate < 0 and randint(0, -rate-1) != 0: return
    for i, l in enumerate(grid):
        for j, _ in enumerate(l):
            if i < curses.LINES and j < curses.COLS:
                screen.addstr(i, j, fdraw(j, i, grid, *args))
    screen.refresh()
    if rate > 0: time.sleep(rate)

def wrap_in_curses(f, *args):
    def cf(*args):
        curses.use_default_colors()
        f(*args)
    curses.wrapper(cf, *args)
