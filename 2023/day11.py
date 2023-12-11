from common import *

data = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".strip().splitlines()

data = open('inputs/day11.txt').read().splitlines()

galaxies = { (r, c) for r in range(len(data)) for c in range(len(data[0])) if data[r][c] == '#' }
empty_rows = { i for i in range(len(data)) } - { r for r, _ in galaxies }
empty_cols = { i for i in range(len(data[0])) } - { c for _, c in galaxies }

axis_d = lambda a, b, g, empty: abs(a - b) + sum(g-1 for r in empty if a<r<b or b<r<a)
distance = lambda a, b, g: axis_d(a[0], b[0], g, empty_rows) + axis_d(a[1], b[1], g, empty_cols)
min_distances = lambda g: sum(distance(a, b, g) for a, b in combinations(galaxies, 2))

# part 1
print(min_distances(2))

# part 2
print(min_distances(1_000_000))
