# fmt: off

data = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
""".strip()

data = open("inputs/day12.txt").read()

*blocks, specs = data.split("\n\n")
blocks = [b.splitlines()[1:] for b in blocks]
specs = [(tuple(map(int, k.split("x"))), list(map(int, v.split()))) for k, v in (line.split(":") for line in specs.splitlines())]

block_sizes = [sum(c == '#' for c in ''.join(block)) for block in blocks]

# lol
def check_spec(spec):
    (w, h), counts = spec
    return w*h >= sum(c * s for c, s in zip(counts, block_sizes))

print(sum(map(check_spec, specs)))
print("Merry Christmas!")
