import itertools

def add(ins, outs, p, i, v1, v2):
    p[p[i+3]] = v1() + v2()
    return i + 4

def mul(ins, outs, p, i, v1, v2):
    p[p[i+3]] = v1() * v2()
    return i + 4

def inp(ins, outs, p, i, *_):
    p[p[i+1]] = next(ins)
    return i + 2

def out(ins, outs, p, i, v1, _):
    outs(v1())
    return i + 2

def jmp_neq(ins, outs, p, i, v1, v2):
    return v2() if v1() != 0 else i + 3

def jmp_eq(ins, outs, p, i, v1, v2):
    return v2() if v1() == 0 else i + 3

def cmp_lt(ins, outs, p, i, v1, v2):
    p[p[i+3]] = 1 if v1() < v2() else 0
    return i + 4

def cmp_eq(ins, outs, p, i, v1, v2):
    p[p[i+3]] = 1 if v1() == v2() else 0
    return i + 4

def ret(*_):
    return -1

opcodes = { 1: add, 2: mul, 3: inp, 4: out, 5: jmp_neq, 6: jmp_eq, 7: cmp_lt, 8: cmp_eq, 99: ret }

def load_program(code):
    return list(map(lambda x: int(x), code.split(',')))

# loaded lazyily so only actually accesed if needed,
# preventing access errors
def get_value_lazy(p, i, f):
    return (lambda: p[p[i]]) if f == 0 else lambda: p[i]

def parse_instruction(p, i):
    inst = p[i]
    c = inst  % 100
    f1 = inst // 100   % 10
    f2 = inst // 1000  % 10
    v1 = get_value_lazy(p, i+1, f1)
    v2 = get_value_lazy(p, i+2, f2)
    return c, v1, v2

def std_in():
    while True: yield int(input('input: '))

def std_out():
    return lambda v: print('output: ', str(v))

def eval_program(p):
    i = 0
    while i >= 0:
        c, v1, v2 = parse_instruction(p, i)
        i = opcodes[c](std_in(), std_out(), p, i, v1, v2) 


# Above the solution to Day 5 with minor changes abstract IO
# Below the actual solution to Day 7.

def eval_till_input(p, ins, outs):
    i = 0
    while i >= 0:
        c, v1, v2 = parse_instruction(p, i)
        if c == 3: yield False
        i = opcodes[c](ins, outs, p, i, v1, v2) 
    yield True

    
def pipe_in(buf):
    while True: yield buf.pop(0)

def pipe_out(buf):
    return lambda v: buf.append(v)

def test_perm(program, l):
    bufs = [[x] for x in l]
    bufs[0].append(0)
    runners = []
    for i in range(len(bufs)):
        ins = pipe_in(bufs[i])
        outs = pipe_out(bufs[(i+1)%len(bufs)])
        runners.append(eval_till_input(program.copy(), ins, outs))
    done = False
    while not done:
        for r in runners:
            done = next(r)
    return bufs[0][0]

with open('./input.txt') as f:
    program = load_program(f.read())
    max_l, max_s = [], 0
    for l in itertools.permutations(range(5, 10)):
        s = test_perm(program, l)
        if max_s < s:
            max_s, max_l = s, l
    print(max_s, max_l)
