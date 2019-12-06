def add(p, i, v1, v2):
    p[p[i+3]] = v1() + v2()
    return i + 4

def mul(p, i, v1, v2):
    p[p[i+3]] = v1() * v2()
    return i + 4

def inp(p, i, *_):
    p[p[i+1]] = int(input('input: '))
    return i + 2

def out(p, i, v1, _):
    print('output: ' + str(v1()))
    return i + 2

def jmp_neq(p, i, v1, v2):
    return v2() if v1() != 0 else i + 3

def jmp_eq(p, i, v1, v2):
    return v2() if v1() == 0 else i + 3

def cmp_lt(p, i, v1, v2):
    p[p[i+3]] = 1 if v1() < v2() else 0
    return i + 4

def cmp_eq(p, i, v1, v2):
    p[p[i+3]] = 1 if v1() == v2() else 0
    return i + 4

def ret(*_):
    return -1

opcodes = { 1: add, 2: mul, 3: inp, 4: out, 5: jmp_neq, 6: jmp_eq, 7: cmp_lt, 8: cmp_eq, 99: ret }

# loaded lazyily so only actually accesed if needed,
# preventing access errors
def get_value_lazy(p, i, f):
    if f == 0:
        return lambda: p[p[i]]
    return lambda: p[i]

def parse_instruction(inst):
    c = inst  % 100
    f1 = inst // 100   % 10
    f2 = inst // 1000  % 10
    f3 = inst // 10000 % 10
    return c, f1, f2, f3

def eval_program(p):
    i = 0
    while i >= 0:
        c, f1, f2, _ = parse_instruction(p[i])
        v1 = get_value_lazy(p, i+1, f1) 
        v2 = get_value_lazy(p, i+2, f2)
        i = opcodes[c](p, i, v1, v2) 
    return program

def load_program(code):
    return list(map(lambda x: int(x), code.split(',')))

with open('./input.txt') as f:
    program = load_program(f.read())
    # program = load_program('3,3,1105,-1,9,1101,0,0,12,4,12,99,1')
    eval_program(list(program))
