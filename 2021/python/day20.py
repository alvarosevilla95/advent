import numpy as np
from functools import reduce
from scipy.ndimage import convolve

data = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""".strip()

data = open('inputs/day20.txt').read()

algo, _, *img = data.splitlines()
algo = np.array([int(x=='#') for x in algo])
img = np.pad([[int(p=="#") for p in row] for row in img], (50,50))

kernel = 2**np.arange(9).reshape(3,3)
iterate = lambda n: reduce(lambda b,_: algo[convolve(b, kernel)], range(n), img).sum() # type: ignore

# part 1
print(iterate(2))

# part 2
print(iterate(50))
