import math
from functools import reduce
from itertools import permutations

data = """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""".strip()

data = open('inputs/day18.txt').read()

numbers = [eval(x) for x in data.splitlines()]

def push_left(ns, n):
    if isinstance(ns, int): return ns + n
    return [push_left(ns[0], n), ns[1]]

def push_right(ns, n):
    if isinstance(ns, int): return ns + n
    return [ns[0], push_right(ns[1], n)]

def explode(n, d=0):
    if isinstance(n, int): return 0, n
    if d == 4: return 2, [n[0], n[1]]
    match explode(n[0], d+1):
        case 1, m:    return 1, [m, n[1]]
        case 2, m:     return 3, [0, push_left(n[1], m[1])], m[0]
        case 3, x, m0: return 3, [x, n[1]], m0
        case 4, x, m1: return 1, [x, push_left(n[1], m1)]
    match explode(n[1], d+1):
        case 1, m:    return 1, [n[0], m]
        case 2, m:     return 4, [push_right(n[0], m[0]), 0], m[1]
        case 3, x, m0: return 1, [push_right(n[0], m0), x]
        case 4, x, m1: return 4, [n[0], x], m1
    return 0, n

def split(n):
    if isinstance(n, int): 
        if n < 10: return False, n
        return True, [math.floor(n/2), math.ceil(n/2)]
    m, x = split(n[0])
    if m: return m, [x, n[1]]
    m, x = split(n[1])
    return m, [n[0], x]

def compact(n):
    f, x, *_ = explode(n)
    if f : return True, x
    return split(n)

def add(a, b):
    f, c  = compact([a, b])
    while f: f, c = compact(c)
    return c

def score(n):
    if isinstance(n, int): return n
    return 3*score(n[0]) + 2*score(n[1])

# part 1
print(score(reduce(add, numbers)))

# part 2
print(reduce(max, (score(reduce(add, p)) for p in permutations(numbers, 2)), 0))
