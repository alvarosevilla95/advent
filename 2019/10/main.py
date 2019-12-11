from math import inf, gcd, atan2, degrees, pi 
from itertools import groupby
import curses
import time

def asteroids(data):
    asteroids = []
    for i, r in enumerate(data):
        for j, v in enumerate(r):
            if v == '#': asteroids.append((j, i))
    return asteroids

def div_gcd(p):
    x, y = p
    if y == 0: return (1 if x > 0 else 0 if x == 0 else -1), 0
    return x // gcd(x,y), y // gcd(x,y)

def grad(a0, a1):
    return div_gcd([x0 - x1 for x0,x1 in zip(a1, a0)])

def angle(a, b):
    x, y = grad(a,b)
    al = atan2(x, y)
    return (pi-al)%(2*pi)

def distance(a, b):
    return sum([abs(x - y) for x,y in zip(b, a)])

def others(a, bs):
    return [(b, angle(a, b), distance(a,b)) for b in bs if b != a]

def sees(os):
    return set([o[1] for o in os])

def order_by_hit(os):
    os = sorted(os, key=lambda o: o[1:])
    oss = list([list(data) for k, data in groupby(os, key=lambda o: o[1])])
    out = []
    while oss:
        out += [o.pop(0) for o in oss]
        oss = list(filter(lambda x: len(x)>0, oss))
    return out


def draw(pad, lenx, leny, pixels, points, o, k):
    for j in range(leny):
        for i in range(lenx):
            p = (j, i)
            if  p == o: c = 0
            elif p == k: c = 1
            elif p in points: c = 2
            else: c = 3
            pad.addstr(i, j, pixels[c][0], pixels[c][1])
    pad.refresh(0, 0, 0, 0, lenx+1, leny+1)
    time.sleep(0.05)

def render(screen, p, os, points):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    pixels = [
            ('0', curses.color_pair(1) | curses.A_BOLD), 
            ('X', curses.color_pair(2) | curses.A_BOLD), 
            ('#', curses.color_pair(3) | curses.A_BOLD), 
            ('.', curses.color_pair(4))
            ]
    lenx, leny = max(points, key=lambda x:x[0])[0] + 1, max(points, key=lambda x:x[1])[1] + 1
    pad = curses.newpad(lenx+1, leny+1)
    while os:
        killed = os.pop(0)[0]
        points.remove(killed)
        draw(pad, lenx, leny, pixels, points, p, killed)

    curses.curs_set(1)

data = open('input.txt').read().splitlines()
points = asteroids(data)

# Part 1
p, ss = max(([(p, sees(others(p, points))) for p in points]), key=lambda x: len(x[1]))
print(p, len(ss))

# Part 2
os = order_by_hit(others(p, points))
# for i in range(len(os)): print(i+1, os.pop(0))
curses.wrapper(lambda s: render(s, p, os, points))
