import time
import curses 
from intcode import IntcodeVm

mem = open('input.txt').read()

def place_drone(x, y):
    def pipe_pos():
        yield x
        yield y
    return IntcodeVm(mem).eval(pipe_pos()) 

def find_square(size):
    x, y = 0, 0
    for y in range(size*1000):
        if place_drone(x+size-1, y): return x, y
        if not place_drone(x, y+size): x += 1
    return None, None

# Part 1
print(sum(place_drone(x, y) for x in range(50) for y in range(50)))
# Part 2
x, y = find_square(5)
print(x, y)
print(x*10000 + y)

def draw_ray(screen, lenx, leny):
    for i in range(leny):
        r = []
        for j in range(lenx):
            r.append(place_drone(j,i))
        screen.addstr(i, 0, ''.join([str(v) if v == 1 else ' ' for v in r]))
    screen.refresh()
    time.sleep(100)
