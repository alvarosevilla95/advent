import re

monad = open('inputs/day24.txt').read()

def eval_inst(inst, inps):
    match inst.split():
        case ['inp', reg]: vars[reg] = inps.pop(0)
        case ['add', reg, val]: vars[reg] +=  get(val)
        case ['mul', reg, val]: vars[reg] *=  get(val)
        case ['div', reg, val]: vars[reg] //= get(val)
        case ['mod', reg, val]: vars[reg] %=  get(val)
        case ['eql', reg, val]: vars[reg] =  vars[reg] == get(val)
        case _: raise ValueError(f"Unknown instruction: {inst}")

vars = { 'w': 0, 'x': 0, 'y': 0, 'z': 0, }

get = lambda val: vars[val] if val in vars else int(val)

digit_insts = re.split(r'inp w\n', monad)[1:]

for i, d in enumerate(digit_insts):
    for d1 in digit_insts[i+1:]:
        if d == d1: print('matched')

exit()

digits = []
z = 0
pzs = {0}
valid = []
for insts in digit_insts:
    zs = set()
    for pz in pzs:
        for i in range(1,10):
            vars = { 'w': i, 'x': 0, 'y': 0, 'z': pz}
            for j in insts.splitlines(): eval_inst(j, [])
            zs |= {vars['z']}
    print(len(zs))
    pzs = zs

insts = {"w": 0, "x": 0, "y": 0, "z": 0}
print(vars)
print(len(pzs))
