import time
import itertools
import curses
from collections import namedtuple, defaultdict

def std_in():
    while True: yield int(input('input: '))

def std_out():
    return lambda v: print('output: ', str(v))

def pipe_in(buf):
    while True: yield buf.pop(0)

def pipe_out(buf):
    return lambda v: buf.append(v)

class IntCodeVm:

    def __init__(self, memory):
        self.memory = defaultdict(int, dict(enumerate(list(map(lambda x: int(x), memory.split(','))))))
        self.ip = 0
        self.r = 0

    def get_mem(self, i, pos=False):
        if pos: return self.get_mem(self.get_mem(i))
        if i < 0: assert False
        return self.memory[i] 

    def set_mem(self, i, v):
        self.memory[i] = v

    def parse_instruction(self):
        c = self.get_mem(self.ip) % 100
        v1 = self.get_value_lazy(1, self.get_mem(self.ip) // 100   % 10)
        v2 = self.get_value_lazy(2, self.get_mem(self.ip) // 1000  % 10)
        v3 = self.get_value_lazy(3, self.get_mem(self.ip) // 10000 % 10)
        return c, v1, v2, v3

    def get_value_lazy(self, off, f):
        if f == 0: return lambda l=False: self.get_mem(self.ip+off, not l)
        if f == 1: return lambda l=False: self.get_mem(self.ip+off) 
        if f == 2: return lambda l=False: self.get_mem(self.get_mem(self.ip+off) + self.r) if not l else self.get_mem(self.ip+off) + self.r
        return 0

    def eval(self, in_s=std_in()): 
        self.in_s = in_s
        while self.ip >= 0:
            val = self.step()
            if val is not None: return val
        return None

    def run(self, in_s=std_in(), out_s=std_out()): 
        while True:
            val = self.eval(in_s)
            if val is None: break
            out_s(val)

    def step(self):
        c, v1, v2, v3 = self.parse_instruction()
        if c == 1: # add
            self.set_mem(v3(True), v1() + v2())
            self.ip += 4

        elif c == 2: # mul
            self.set_mem(v3(True), v1() * v2())
            self.ip += 4

        elif c == 3: # input
            self.set_mem(v1(True), next(self.in_s))
            self.ip += 2

        elif c == 4: # output
            val = v1()
            self.ip += 2
            return val

        elif c == 5: # jmp_neq
            self.ip = v2() if v1() != 0 else self.ip +3

        elif c == 6: # jmp_eq
            self.ip = v2() if v1() == 0 else self.ip +3

        elif c == 7: # cmp_lt
            self.set_mem(v3(True),  1 if v1() < v2() else 0)
            self.ip += 4

        elif c == 8: # jmp_eq
            self.set_mem(v3(True),  1 if v1() == v2() else 0)
            self.ip += 4

        elif c == 9: # set_r
            self.r += v1()
            self.ip += 2

        elif c == 99: # kill
            self.ip = -1

def run_bot(screen):
    f = open('input.txt').read()
    vm = IntCodeVm(f)

    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    ds = '^>v<'

    max_x, max_y = 50, 12
    grid, i, j, d = defaultdict(int), 00, max_y//2, 0
    frame = [[0 for x in range(max_x)] for y in range(max_y)]
    grid[i,j] = 1

    def grid_in():
        while True:
            yield grid[i, j]
    g_in = grid_in()

    grid[max_x, max_y] = 1

    while True:
        p = vm.eval(g_in)
        if p is None: break
        grid[i, j] = p
        frame[j][i] = p
        p = vm.eval(g_in)
        if p is None: break
        if p == 0: p = -1

        v = frame[j][i]
        frame[j][i] = 2
        draw(screen, frame, (i,j), ds[d])
        frame[j][i] = v
        d = (d+p) % 4
        i += dx[d]
        j += dy[d]
    time.sleep(10)

def render(screen, f, *args):
    curses.curs_set(0)
    f(screen, *args)
    curses.curs_set(1)

def draw(screen, frame, r, d):
    for i, r in enumerate(reversed(frame)):
        screen.addstr(i, 0, ' '.join([d if p == 2 else '#' if p == 1 else ' ' for j, p in enumerate(r)]))
    screen.refresh()
    time.sleep(0.2)

curses.wrapper(lambda s: render(s,run_bot))
