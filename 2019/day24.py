import numpy as np
from collections import defaultdict
from scipy.signal import convolve2d

data = """
....#
#..#.
#..##
..#..
#....
""".strip()

data = open('inputs/day24.txt').read()

grid = np.array([[1 if c == '#' else 0 for c in line] for line in data.splitlines()])

kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])

def life_score(grid):
    return convolve2d(grid, kernel, boundary="fill", mode='same')

def life(grid, score=None):
    if score is None: score = life_score(grid)
    return (grid > 0) & (score == 1) | (grid == 0) & np.isin(score, [1,2])

def recursive_life(grid, outer, inner):
    score = life_score(grid)

    score[0,:] += outer[1,2]
    score[4,:] += outer[3,2]
    score[:,0] += outer[2,1]
    score[:,4] += outer[2,3]

    score[1,2] += inner[0,:].sum()
    score[2,1] += inner[:,0].sum()
    score[2,3] += inner[:,4].sum()
    score[3,2] += inner[4,:].sum()

    score[2,2] = 0

    return life(grid, score)

# part 1
history = set()
p1_grid = grid.copy()
while True:
    p1_grid = life(p1_grid)
    rating = sum(2**(i*len(p1_grid)+j) for i, row in enumerate(p1_grid) for j, c in enumerate(row) if c)
    if rating in history: break
    history.add(rating)
print(rating)

# part 2
defdict = lambda d: defaultdict(lambda: np.zeros((5,5)).astype(int), d)
stack = defdict({0: grid})
min_level, max_level = 0, 0
for _ in range(200):
    stack = defdict({
        level: recursive_life(stack[level], stack[level-1], stack[level+1])
        for level in range(min_level-1, max_level+2)
    })
    min_level, max_level = min_level-1, max_level+1
print(sum(grid.sum() for grid in stack.values()))
