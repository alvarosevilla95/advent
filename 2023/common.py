import regex as re, numpy as np, networkx as nx, sys, os, time, curses
from math import prod, floor, ceil, lcm, inf
from random import randint
from functools import reduce, cache
from itertools import chain, combinations, takewhile, count
from collections import defaultdict, deque
from multiprocessing import Pool
from heapq import heappop, heappush
from sympy import Symbol, symbols, solve_poly_system

from viz import Visualiser, DrawAction


sys.setrecursionlimit(100000) # heh

