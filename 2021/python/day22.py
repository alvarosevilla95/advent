import re

data = """
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
""".strip()

# data = open('inputs/day22.txt').read()

ranges = [(line.startswith("on"), [(int(x), int(y)) for r in re.findall(r'\d+', line) for x, y in zip(r[::2], r[1::2])]) for line in data.splitlines()]

cubes = []

def find_overlap(cube):
    for i, c in enumerate(cubes):
        if c[0] == cube[0]:
            return i
    return -1


for on, r in ranges:
    if on:
        pass

print(ranges)
