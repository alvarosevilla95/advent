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
        if draw: 
            c = ('#', curses.color_pair(3))
            draw(x, y,c)
            if (i:= i-1) == 0: 
                draw(x, y, c, True)
                i = len(queue)
    return seen

def scan_all_directions(i, draw=None):
    return max(len(scan_light(i, 0, 'S', draw)),
               len(scan_light(i, len(data)-1, 'N', draw)),
               len(scan_light(0, i, 'E', draw)),
               len(scan_light(len(data)-1, i, 'W', draw)))

def viz():
    grid = lambda: [[(c if c != '.' else ' ', curses.color_pair(2)) for c in line] for line in data]
    with Visualiser(0.01, grid) as v: # type: ignore
        def draw(x, y, c, ref=False):
            v.draw_char(x,y,c)
            if ref: 
                v.get_frame()
                v.refresh()

        def viz_scan(x, y, d):
            scan_light(x, y, d, draw)
            v.draw_grid(grid())

        v.draw_grid()
        for i in range(len(data)):
            viz_scan(i, 0, 'S')
            viz_scan(i, len(data)-1, 'N')
            viz_scan(0, i, 'E')
            viz_scan(len(data)-1, i, 'W')

if __name__ == '__main__':
    # part 1
    print(len(scan_light(0, 0, 'E')))

    # part 2
    print(max(Pool().starmap(scan_all_directions, ([i] for i in range(len(data))))))

    # viz()
