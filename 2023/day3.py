import math, re
from itertools import chain

data = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".strip().splitlines()

data = open('inputs/day3.txt').read().splitlines()

parts = {(r, c): [] for r in range(len(data)) for c in range(len(data[0])) if data[r][c] not in "0123456789."}

for r, row in enumerate(data):
    for n in re.finditer(r'\d+', row):
        edge = {(r, n.start() + c) for r in (r-1, r, r+1) for c in range(-1, len(n.group()) + 1)}
        for o in edge & parts.keys():
            parts[o] += [int(n.group())]

# part 1
print(sum(chain(*parts.values())))

# part 2
print(sum(math.prod(c) for c in parts.values() if len(c)==2))
