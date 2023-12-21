import regex as re, numpy as np, sys, os, time, curses
from math import prod, floor, ceil, lcm, inf
from random import randint
from functools import reduce, cache
from itertools import chain, combinations, takewhile, count
from collections import defaultdict, deque
from multiprocessing import Pool
from heapq import heappop, heappush

from viz import draw_grid, wrap_in_curses


sys.setrecursionlimit(100000) # heh

