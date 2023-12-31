import numpy as np

data = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""".strip()

data = open('inputs/day25.txt').read()

grid = np.array([[c for c in line] for line in data.splitlines()])

def move_dir(grid, dir):
    axis = dir == '>'
    moves = (grid == dir) & (np.roll(grid, -1, axis) == ".")
    grid[moves] = "."
    grid[np.roll(moves, 1, axis)] = dir
    return np.any(moves)

i = 1
while any([move_dir(grid, '>'), move_dir(grid, 'v')]): i += 1
print(i)
