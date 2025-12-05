from functools import reduce

data = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
""".strip()

data = open('inputs/day5.txt').read()

ranges, ids = data.split("\n\n")
ranges = [tuple(map(int, r.split("-"))) for r in ranges.splitlines()]
ids = [int(x) for x in ids.splitlines()]

fresh = sum(any(s <= id <= e for s, e in ranges) for id in ids)
print(fresh)

def merge(acc, r):
    if acc and acc[-1][1] >= r[0] - 1:
        return acc[:-1] + [(acc[-1][0], max(acc[-1][1], r[1]))]
    return acc + [r]

ranges = reduce(merge, sorted(ranges), [])

valid = sum(end - start + 1 for start, end in ranges)
print(valid)
