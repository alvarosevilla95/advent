import math
from collections import deque

data = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".strip()

data = open('inputs/day12.txt').read()

grid = data.splitlines()

start = next((i, j) for i, row in enumerate(grid) for j, c in enumerate(row) if c == 'S')
end   = next((i, j) for i, row in enumerate(grid) for j, c in enumerate(row) if c == 'E')

def neighbours(i, j):
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if not(0 <= i+di < len(grid) and 0 <= j+dj < len(grid[0])): continue
        v, n = grid[i][j], grid[i+di][j+dj]
        v = 'a' if v == 'S' else 'z' if v == 'E' else v
        n = 'a' if n == 'S' else 'z' if n == 'E' else n
        if ord(n) <= ord(v) + 1: yield i+di, j+dj
        
def dijkstra(start, end):
    q, dist = deque([start]), {start: 0}
    while q:
        (i, j) = q.popleft()
        if (i, j) == end: return dist[end]
        for ni, nj in neighbours(i, j):
            if (ni, nj) not in dist:
                dist[ni, nj] = dist[i, j] + 1
                q += [(ni, nj)]
    return math.inf

# part 1
print(dijkstra(start, end))

# part 2
starts = [(i, j) for i, row in enumerate(grid) for j, c in enumerate(row) if c == 'a' or c == 'S']
print(min(dijkstra(start, end) for start in starts))
