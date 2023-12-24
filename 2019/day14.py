import math 
from collections import defaultdict

def parse_input(data):
    recipes = {}
    for l in data.splitlines():
        l = l.replace(' => ', ', ')
        ams = [parse_amount(a) for a in l.split(', ')]
        recipes[ams[-1][0]] = ams[-1][1], ams[:-1]
    return recipes

def parse_amount(data):
    a, e = data.split(' ')
    return e, int(a)

def ore_price(mat, amount, rest=None):
    if mat == 'ORE': return amount
    if not rest: rest = defaultdict(int)
    amount, rest[mat] = amount - rest[mat], max(rest[mat]-amount, 0)
    if amount <= 0: return 0 
    out, ings = recipes[mat]
    need = math.ceil(amount / out)
    cost = sum(map(lambda i: ore_price(i[0], i[1]*need, rest), ings))
    rest[mat] += need * out - amount
    return cost

def max_yield(mat, ore):
    price = ore_price(mat, 1)
    fuel, rest = 0, defaultdict(int)
    while ore > 0:
        # even if we can't make one from scratch, 
        # we may have enough spare ingredientes for it
        f = ore // price if ore > price else 1 
        ore -= ore_price(mat, f, rest)
        if ore > 0: fuel += f
    return fuel

data = open('inputs/day14.txt').read()
recipes = parse_input(data)
# Part 1
print(ore_price('FUEL', 1))
# Part 2
print(max_yield('FUEL', int(1e12)))
