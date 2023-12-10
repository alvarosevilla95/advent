from common import *

data = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""".strip().splitlines()

data = open('inputs/day10.txt').read().splitlines()

pipes = { '|': 'NS', '-': 'EW', 'L': 'NE', 'J': 'NW', '7': 'SW', 'F': 'SE', '.': '' }
directions = { 'N': ((0, -1), 'S'), 'E': ((1, 0), 'W'), 'S': ((0, 1), 'N'), 'W': ((-1, 0), 'E') }

iter_grid = lambda: ((x, y, cell) for y, row in enumerate(data) for x, cell in enumerate(row))

# part 1
sx, sy = next((x, y) for x, y, c in iter_grid() if c == 'S')
path, cur, dir = {(sx, sy)}, (sx, sy), ''

for (dx, dy), op in directions.values():
    if op in pipes[data[sy+dy][sx+dx]]:
        if dir:
            shape = next(c for c, ds in pipes.items() if dir in ds and op in ds)
            data[sy] = data[sy].replace('S', shape)
            break
        cur, dir = (sx+dx, sy+dy), op

while cur not in path:
    path.add(cur)
    (dx, dy), dir = directions[pipes[data[cur[1]][cur[0]]].replace(dir, '')]
    cur = cur[0]+dx, cur[1]+dy

print(len(path)//2)
       
# part 2
can_escape = lambda x, y: sum(1 for dx in range(0, x) if (dx, y) in path and data[y][dx] in 'LJ|') % 2
print(sum(1 for x, y, _ in iter_grid() if (x,y) not in path and can_escape(x, y)))
