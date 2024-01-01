import numpy as np
from math import prod

data = """
30373
25512
65332
33549
35390
""".strip()

data = open('inputs/day8.txt').read()

grid = np.array([[int(x) for x in row] for row in data.splitlines()])

# part 1
def is_visible(i, j):
    paths = [grid[0:i,j], grid[i+1:,j], grid[i,0:j], grid[i,j+1:]]
    return any(all(v < grid[i, j] for v in path) for path in paths)

print(np.sum([is_visible(i, j) for j in range(grid.shape[1]) for i in range(grid.shape[0])]))

def visible_from(i, j):
    paths = [grid[0:i,j][::-1], grid[i+1:,j], grid[i,0:j][::-1], grid[i,j+1:]]
    return [next((n for n,p in enumerate(path, 1) if p >= grid[i,j]), len(path)) for path in paths]

print(max(prod(visible_from(i, j)) for i in range(grid.shape[0]) for j in range(grid.shape[1])))
