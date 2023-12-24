import re
import operator
from math import gcd
from functools import reduce

def cmp(a, b):
    return (a>b)-(a<b)

def zip_list(l):
    return list(zip(*list(l)))

def lcm(a,b):
    return a*b//gcd(a,b)

def parse_input(data):
    data = [re.findall(r'-?\d+', l) for l in data.splitlines()]
    data = [[int(v) for v in d] for d in data]
    return [[d, [0,0,0]] for d in data]

def dim(moons, i):
    return [[p[i], v[i]] for p, v in moons]

def undim(dims):
    return [zip_list(v) for v in zip_list(dims)]

def dim_map(f, moons):
    return map(lambda d: f(dim(moons,d)), range(3))

def evolve_dim(moons):
    for mi, m in enumerate(moons): 
        for o in moons[mi+1:]:
            d = cmp(o[0], m[0])
            m[1], o[1] = m[1]+d, o[1]-d
    for moon in moons: moon[0] += moon[1]
    return moons

def evolve(moons):
    return undim(dim_map(evolve_dim, moons)) 

def energy(moon):
    return [sum(map(abs, c)) for c in moon]

def total_energy(moon):
    return reduce(operator.mul, energy(moon))

def system_energy(moons):
    return reduce(operator.add, map(total_energy, moons))

def steps_to_loop(dim):
    i, n = 1, [d[:] for d in dim]
    while evolve_dim(n) != dim: i += 1
    return i

moons = parse_input(open('inputs/day12.txt').read())
# Part 1
for j in range(1000): moons = evolve(moons)
print(system_energy(moons))
# Part 2
loops = dim_map(steps_to_loop, moons)
print(reduce(lcm, loops))
