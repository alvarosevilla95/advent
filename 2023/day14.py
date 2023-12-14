from common import *

data = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""".strip().splitlines()

data = open('inputs/day14.txt').read().splitlines()

# part 1
def tilt(grid, direction):
    grid = grid if direction in 'EW' else [*map(''.join, zip(*grid))]
    pad = str.ljust if direction in 'NW' else str.rjust
    tilt_group = lambda g: pad(g.replace('.', ''), len(g), '.') 
    grid = ['#'.join(map(tilt_group, row.split('#'))) for row in grid]
    return grid if direction in 'EW' else [*map(''.join, zip(*grid))]

total = lambda grid: sum(i*r.count('O') for i, r in enumerate(grid[::-1], 1))

print(total(tilt(data, 'N')))

# part 2
def multispin(grid, spins, grids=[], i=0):
    if (grid := reduce(tilt, 'NWSE', grid)) in grids: 
        return grids[(spins-i-1) % (grids.index(grid)-i)]
    return multispin(grid, spins, grids+[grid], i+1)

print(total(multispin(data, 1000000000)))
