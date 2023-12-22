from common import *

data = r"""
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
""".strip().splitlines()

data = open('inputs/day22.txt').read().splitlines()

blocks = sorted([[[int(c) for c in line.split(',')] for line in block.split('~')] for block in data], key=lambda b: b[0][2])

# part 1
overlap = lambda s1, e1, s2, e2: s1[0] <= e2[0] and s2[0] <= e1[0] and s1[1] <= e2[1] and s2[1] <= e1[1]

for i, (s1, e1) in enumerate(blocks):
    z = 1 + reduce(max, (e2[2] for (s2, e2) in blocks[:i] if overlap(s1, e1, s2, e2)), 0)
    s1[2], e1[2] = z, z + e1[2] - s1[2]

supports = defaultdict(set)
supported = defaultdict(set)

for i, (s1, e1) in enumerate(blocks):
    for j, (s2, e2) in enumerate(blocks[:i]):
        if e2[2]+1 == s1[2] and overlap(s1, e1, s2, e2):
            supported[i].add(j)
            supports[j].add(i)

alone = {next(iter(s)) for s in supported.values() if len(s) == 1}
print(len(blocks) - len(alone))

# part2
def find_falling(x, falling):
    if x in falling: return falling
    falling.add(x)
    for b in supports[x]:
        if all(c in falling for c in supported[b]):
            falling = find_falling(b, falling)
    return falling

print(sum(len(find_falling(a, set())) - 1 for a in alone))
