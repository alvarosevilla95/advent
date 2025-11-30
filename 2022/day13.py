from itertools import chain
from functools import cmp_to_key

data = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".strip()

data = open('inputs/day13.txt').read()

pairs = [[*map(eval, pair.splitlines())] for pair in data.split('\n\n')]

def compare(a, b):
    if isinstance(a, int) and isinstance(b, int): return a - b
    if isinstance(a, int): return compare([a], b)
    if isinstance(b, int): return compare(a, [b])
    for (aa, bb) in zip(a, b):
        if (c := compare(aa, bb)) != 0: return c
    return len(a) - len(b)

# part 1
print(sum(i+1 for i, p in enumerate(pairs) if compare(*p) < 0))

# part 2
pairs = list(chain(*pairs)) + [[[2]], [[6]]]
pairs.sort(key=cmp_to_key(compare))
print((pairs.index([[2]])+1) * (pairs.index([[6]])+1))
