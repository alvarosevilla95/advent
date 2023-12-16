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

def scan_light(x, y, d):
    queue, seen = deque([(x, y, d)]), defaultdict(set)
    while queue:
        x, y, d = queue.pop()
        while 0<=x<len(data) and 0<=y<len(data) and d not in seen[(x, y)]:
            seen[(x, y)].add(d)
            if data[y][x] == '\\': d = 'NESW'[3-'NESW'.index(d)]
            if data[y][x] == '/': d = 'NESW'[1-'NESW'.index(d)]
            if data[y][x] == '|' and d in 'EW': d = 'S'; queue += [(x, y, 'N')]
            if data[y][x] == '-' and d in 'NS': d = 'W'; queue += [(x, y, 'E')]
            x, y = x+dirs[d][0], y+dirs[d][1]
    return seen

def scan_all_directions(i):
    return max(len(scan_light(i, 0, 'S')),
               len(scan_light(i, len(data)-1, 'N')),
               len(scan_light(0, i, 'E')),
               len(scan_light(len(data)-1, i, 'W')))

if __name__ == '__main__':
    # part 1
    print(len(scan_light(0, 0, 'E')))

    # part 2
    print(max(Pool().starmap(scan_all_directions, ([i] for i in range(len(data))))))
