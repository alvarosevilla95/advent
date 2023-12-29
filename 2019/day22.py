from functools import reduce

data = """
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
""".strip()

data = open('inputs/day22.txt').read()

# part 1
def deal(x):
    return x[::-1]

def cut(x, n):
    return x[n:] + x[:n]

def increment(x, n):
    y = [None] * len(x)
    for i in range(len(x)): y[(i*n) % len(x)] = x[i]
    return y

def parse(data):
    for line in data.splitlines():
        if line.startswith('deal into new stack'): yield deal
        elif line.startswith('deal with increment'): yield lambda c: increment(c, int(line.split()[-1]))
        elif line.startswith('cut'): yield lambda c: cut(c, int(line.split()[-1]))

cards = reduce(lambda x, op: op(x), parse(data), list(range(10007)))
print(cards.index(2019)) # type: ignore

# part 2
m = 119315717514047
n = 101741582076661
a,b = 1,0

deal2 = lambda: (-a %m, (m-1-b)%m)
inc2 = lambda x: (a*x %m, b*x %m)
cut2 = lambda x: (a, (b-x)%m)

for line in data.splitlines():
    if line.startswith('deal with increment'): a, b = inc2(int(line.split()[-1]))
    elif line.startswith('deal into new stack'): a, b = deal2()
    elif line.startswith('cut'): a, b = cut2(int(line.split()[-1]))

r = (b * pow(1-a, m-2, m)) % m
print(((2020 - r) * pow(a, n*(m-2), m) + r) % m)
