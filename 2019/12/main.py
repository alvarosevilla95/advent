import re
import operator
from math import gcd

def reduce(f, v, l):
    for e in l: v = f(v, e)
    return v

def lcm(a,b):
    return a*b//gcd(a,b)

def parse_input(data):
    data = [re.findall(r'-?\d+', l) for l in data.splitlines()]
    data = [[int(v) for v in d] for d in data]
    return [[d, [0,0,0]] for d in data]

def dims():
    return range(3)

def dim(moons, i):
    return [[p[i], v[i]] for p, v in moons]

def evolve_dim(moons):
    for mi, moon in enumerate(moons):
        for other in moons[mi+1:]:
            d = 1 if moon[0] < other[0] else -1 if moon[0] > other[0] else 0
            moon[1], other[1] = moon[1]+d, other[1]-d
    for moon in moons: moon[0] += moon[1]
    return moons

def evolve(moons):
    ds = [evolve_dim(dim(moons, i)) for i in dims()]
    return [[list(v) for v in zip(*d)] for d in zip(*ds)]

def energy(moon):
    return [sum([abs(v) for v in c]) for c in moon]

def total_energy(moon):
    return reduce(operator.mul, 1, energy(moon))

def system_energy(moons):
    return reduce(operator.add, 0, map(total_energy, moons))

def steps_to_loop(dim):
    n = [d[:] for d in dim]
    i = 1
    while evolve_dim(n) != dim: i += 1
    return i


moons = parse_input(open('input.txt').read())
# Part 1
for j in range(1000): 
    moons = evolve(moons)
print(system_energy(moons))

# Part 2
loops = [steps_to_loop(dim(moons, i)) for i in dims()]
print(reduce(lcm, 1, loops))
