from common import *

data = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""".strip().splitlines()

data = open('inputs/day16.txt').read().splitlines()

dirs = { 'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0) }

def scan_light(x, y, d, draw=None):
    queue, seen, i = deque([(x, y, d)]), defaultdict(set), 1
    while queue:
        x, y, d = queue.popleft()
        if not(0<=x<len(data) and 0<=y<len(data) and d not in seen[(x, y)]): continue
        seen[(x, y)].add(d)
        if data[y][x] == '\\': d = 'NESW'[3-'NESW'.index(d)]
        if data[y][x] == '/': d = 'NESW'[1-'NESW'.index(d)]
        if data[y][x] == '|' and d in 'EW': d = 'SN'
        if data[y][x] == '-' and d in 'NS': d = 'WE'
        queue += [(x+dirs[i][0], y+dirs[i][1], i) for i in d]
        if draw and (i:= i-1) == 0: 
            draw(data, seen)
            i = len(queue)
    return seen

def scan_all_directions(i, draw=None):
    return max(len(scan_light(i, 0, 'S', draw)),
               len(scan_light(i, len(data)-1, 'N', draw)),
               len(scan_light(0, i, 'E', draw)),
               len(scan_light(len(data)-1, i, 'W', draw)))

def viz(screen):
    draw_char = lambda x, y, grid, seen: grid[y][x] if grid[y][x] != '.' else '#' if (x, y) in seen else ' '
    draw = lambda grid, seen: draw_grid(screen, grid, 0.01, draw_char, seen)
    max(scan_all_directions(i, draw) for i in range(len(data)))

if __name__ == '__main__':
    # part 1
    print(len(scan_light(0, 0, 'E')))

    # part 2
    print(max(Pool().starmap(scan_all_directions, ([i] for i in range(len(data))))))

    # wrap_in_curses(viz)
