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

grid = [[1 if x == "@" else 0 for x in line] for line in data.splitlines()]

xt = len(grid[0])
yt = len(grid)

def neighbors(grid, x, y):
  return sum(grid[i][j] for i in range(x-1, x+2) for j in range(y-1, y+2) if 0 <= i < xt and 0 <= j < yt and (i, j) != (x, y))

removed = 0
prev = grid
while True:
    after = [[ 1 if prev[x][y] == 1 and neighbors(prev, x, y) >= 4 else 0 for x in range(xt)] for y in range(yt)]
    new_removed = sum(prev[x][y] - after[x][y] for x in range(xt) for y in range(yt))
    if removed == 0: print(new_removed) # part 1
    if new_removed == 0: break
    removed += new_removed
    prev = after
print(removed)
