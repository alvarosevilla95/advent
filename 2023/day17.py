from common import *

data = r"""
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
""".strip()

data = open('inputs/day17.txt').read()

grid = [[int(c) for c in line] for line in data.splitlines()]
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def find(mind, maxd):
    start, end = (0, 0), (len(grid)-1, len(grid)-1)
    queue = [(0, start, (-1, -1))]
    dists, seen = defaultdict(lambda: inf), set()
    while queue:
        dist, (x, y), dir = heappop(queue)
        if (x, y) == end: return dist
        if (x, y, dir) in seen: continue
        seen.add((x, y, dir))
        for d in [d for d in dirs if dir not in [d, dirs[dirs.index(d) - 2]]]:
            diff = 0
            for step in range(1, maxd+1):
                nx, ny = x + d[0] * step, y + d[1] * step
                if not(0<=nx<len(grid) and 0<=ny<len(grid)): continue
                diff += grid[nx][ny]
                nc = dist + diff
                if step < mind or dists[(nx, ny, d)] <= nc: continue
                dists[(nx, ny, d)] = nc
                heappush(queue, (nc, (nx, ny), d)) # type: ignore

# part 1
print(find(1, 3))

# part 2
print(find(4, 10))
