import itertools
from collections import namedtuple

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
        self.memory = dict(enumerate(list(map(lambda x: int(x), memory.split(',')))))
        self.ip = 0
        self.r = 0

    def get_mem(self, i, pos=False):
        if pos: return self.get_mem(self.get_mem(i))
        return self.memory[i] #if i < len(self.memory) else 0

    def set_mem(self, i, v):
        # if i >= len(self.memory): self.memory += [0 for _ in range(i - len(self.memory) + 1)]
        self.memory[i] = v

    def parse_instruction(self):
        c = self.get_mem(self.ip) % 100
        v1 = self.get_value_lazy(1, self.get_mem(self.ip) // 100   % 10)
        v2 = self.get_value_lazy(2, self.get_mem(self.ip) // 1000  % 10)
        v3 = self.get_value_lazy(3, self.get_mem(self.ip) // 10000 % 10)
        return c, v1, v2, v3

    def get_value_lazy(self, off, f):
        if f == 0: return lambda l=False: self.get_mem(self.ip+off, True) if not l else self.get_mem(self.ip+off)
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

        elif c == 5: # cmp_neq
            self.ip = v2() if v1() != 0 else self.ip +3

        elif c == 6: # cmp_eq
            self.ip = v2() if v1() == 0 else self.ip +3

        elif c == 7: # jmp_lt
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


with open('./input.txt') as f:
    program = f.read()
    # program = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    vm = IntCodeVm(program)
    vm.run()
    
    # print(test_all(program, range(5)))
    # print(test_all(program, range(5, 10)))

