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

def std_in():
    while True: yield int(input('input: '))

def std_out():
    return lambda v: print('output: ', str(v))

def pipe_in(buf):
    while True: yield buf.pop(0)

def pipe_out(buf):
    return lambda v: buf.append(v)

def load_program(code):
    return list(map(lambda x: int(x), code.split(',')))

def parse_instruction(p, i):
    c = p[i] % 100
    v1 = get_value_lazy(p, i+1, p[i] // 100  % 10)
    v2 = get_value_lazy(p, i+2, p[i] // 1000 % 10)
    return c, v1, v2

def get_value_lazy(p, i, f):
    return (lambda: p[p[i]]) if f == 0 else lambda: p[i]

def eval_till_input(p, ins, outs):
    i = 0
    while i >= 0:
        c, v1, v2 = parse_instruction(p, i)
        if c == 3: yield False
        i = opcodes[c](ins, outs, p, i, v1, v2) 
    yield True

def eval_program(p):
    r = eval_till_input(p, std_in(), std_out())
    while not next(r): pass

def test_all(program, values):
    maxs, maxp = 0, []
    for perm in itertools.permutations(values):
        s = test_permutation(program, perm)
        if maxs < s:
            maxs, maxp= s, perm
    return maxs, maxp

def test_permutation(program, perm):
    bufs = [[x] for x in perm]
    bufs[0].append(0)
    runners = []
    for i in range(len(bufs)):
        ins = pipe_in(bufs[i])
        outs = pipe_out(bufs[(i+1)%len(bufs)])
        runners.append(eval_till_input(program.copy(), ins, outs))
    done = False
    while not done:
        for r in runners: done = next(r)
    return bufs[0][0]

with open('./input.txt') as f:
    program = load_program(f.read())
    print(test_all(program, range(5)))
    print(test_all(program, range(5, 10)))
