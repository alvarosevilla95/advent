import numpy as np
from scipy.signal import convolve2d

data = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".strip()

data = open('inputs/day4.txt').read()

grid = np.array([[1 if x == "@" else 0 for x in line] for line in data.splitlines()])

kernel = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]])

removed = 0
prev = grid
while True:
    neighbor_count = convolve2d(prev, kernel, mode='same', boundary='fill')
    after = ((prev == 1) & (neighbor_count >= 4)).astype(int)
    new_removed = np.sum(prev - after)
    if removed == 0: print(new_removed)  # part 1
    if new_removed == 0: break
    removed += new_removed
    prev = after
print(removed)
