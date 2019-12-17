from collections import defaultdict

class IntcodeVm:

    @staticmethod
    def parse_memory(mem):
        return list(map(lambda x: int(x), mem.split(',')))

    @staticmethod
    def std_in():
        while True: yield int(input('input: '))

    @staticmethod
    def pipe_one(val):
        yield val

    @staticmethod
    def pipe_many(values):
        for v in iter(values): yield v

    def __init__(self, memory):
        if isinstance(memory, str): memory = IntcodeVm.parse_memory(memory)
        self.memory = defaultdict(int, dict(enumerate(memory)))
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

    def eval(self, in_s=None): 
        if in_s is None: in_s = IntcodeVm.std_in()
        self.in_s = in_s
        while self.ip >= 0:
            val = self.step()
            if val is not None: return val
        return None

    def run(self, in_s=None): 
        if in_s is None: self.in_s = IntcodeVm.std_in()
        self.in_s = in_s
        while True: 
            o = self.eval(in_s)
            if o is None: break
            yield o

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


