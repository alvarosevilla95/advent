from common import *

data = r"""
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
""".strip().splitlines()

data = open('inputs/day21.txt').read().splitlines()

size = len(data)
dirs = [(1,0), (0,1), (-1,0), (0,-1)]
pos = {(x,y) for y in range(size) for x in range(size) if data[y][x] == 'S'}
dists = {next(iter(pos)): 0}

new_cell = lambda x, y: 0<=x<size and 0<=y<size and data[y][x] != '#' and (x, y) not in dists
step = lambda pos: {(xx, yy) for x,y in pos for dx,dy in dirs if new_cell(xx:=x+dx, yy:=y+dy)}

for i in range(size):
    pos = step(pos)
    dists.update({p: i+1 for p in pos})

count_squares = lambda p: sum(1 for v in dists.values() if p(v))

# part 1
print(count_squares(lambda v: v % 2 == 0 and v < 65))

# part 2
n = 26501365 // size
full_odd   = count_squares(lambda v: v % 2 == 1)
full_even  = count_squares(lambda v: v % 2 == 0)
outer_odd  = count_squares(lambda v: v % 2 == 1 and v > 65)
outer_even = count_squares(lambda v: v % 2 == 0 and v > 65)
print(full_odd*(n+1)**2 + full_even*n**2 - outer_odd*(n+1) + outer_even*n)

# def viz(screen):
#     global dists
#     pos = {(x,y) for y in range(size) for x in range(size) if data[y][x] == 'S'}
#     dists = {next(iter(pos)): 0}
#     draw_char = lambda x, y, grid, pos: 'O' if (x, y) in pos else grid[y][x]
#     for _ in range(64): draw_grid(screen, data, 0.1, draw_char, pos := step(pos))
# wrap_in_curses(viz)
