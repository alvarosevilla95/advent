from intcode import IntcodeVm
import time
import curses
import itertools
from collections import Counter


def parse_grid(vm):
    grid = []
    row = []
    for c in vm.run():
        c = str(chr(c))
        if c == '\n':
            if row: grid.append(row)
            if len(grid) == 43: break
            row = []
            continue
        row.append(c)
    return grid

def draw_grid(screen, grid, extra=[]):
    screen.addstr(0,0, '   ' + ' '.join([str((i//10) % 10) for i in range(len(grid[0]))]))
    screen.addstr(1,0, '   ' + ' '.join([str(i % 10) for i in range(len(grid[0]))]))
    for i, r in enumerate(grid):
        screen.addstr(i+2, 0, (' ' if i < 10 else '') + str(i) + ' ' + ' '.join(r))
    if lines:
        for i, l in enumerate(lines):
            screen.addstr(i+len(grid)+2, 0, l)

    screen.refresh()

def find_intersections(grid):
    points = []
    for i, r in enumerate(grid):
        for j, p in enumerate(r):
            if p == '#':
                if (i+1 < len(grid) and grid[i+1][j] == '#' and
                    j+1 < len(r)    and grid[i][j+1] == '#' and
                    i-1 > 0         and grid[i-1][j] == '#' and
                    j-1 > 0         and grid[i][j-1] == '#'):
                    points.append((i,j))
    return points

def find_path(grid):
    for i, r in enumerate(grid):
        for j, p in enumerate(r):
            if p == '^': x, y = j, i
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    dirs = []
    c = -1
    l = 'L'
    d = 3
    while True:
        c+=1
        nx, ny = x + dx[d], y + dy[d]
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] == '#':
            x, y = nx, ny
            continue
        if y+1 < len(grid) and grid[y+1][x] == '#':
            if (x, y+1) != (x-dx[d], y-dy[d]):
                dirs.append((l, c))
                l = 'R' if d == 1 else 'L'
                d = 2
                c = 0
                x, y = x, y + 1
                continue
        if 0 <= y-1 and grid[y-1][x] == '#':
            if (x, y-1) != (x-dx[d], y-dy[d]):
                dirs.append((l, c))
                l = 'L' if d == 1 else 'R'
                d = 0
                c = 0
                x, y = x, y - 1
                continue
        if x+1 < len(grid[0]) and grid[y][x+1] == '#':
            if (x+1, y) != (x-dx[d], y-dy[d]):
                dirs.append((l, c))
                l = 'R' if d == 0 else 'L'
                d = 1
                c = 0
                x, y = x+1, y
                continue
        if 0 <= x-1 and grid[y][x-1] == '#':
            if (x-1, y) != (x-dx[d], y-dy[d]):
                dirs.append((l, c))
                l = 'L' if d == 0 else 'R'
                d = 3
                c = 0
                x, y = x-1, y
                continue
        break
    dirs.append((l, c))
    return ''.join([l+str(d)for l,d in dirs])

def combine(instructions, mins, maxs):
    possible_matches = []
    matches = []
    for start_index in range(0, len(instructions)-3):
        for end_index in range(start_index+1, len(instructions)+1):
            current_string = instructions[start_index:end_index]
            if len(current_string) < mins: continue 
            if len(current_string) > maxs: continue 
            possible_matches.append(instructions[start_index:end_index])

    for possible_match, count in Counter(possible_matches).most_common():
        if count <= 1: break
        matches.append(possible_match)
    return list(filter(lambda m: len(m) <= 10, filter(is_valid_match, matches)))

def is_valid_match(match):
    return ((match[0] == 'L' or match[0] == 'R') and 
            (match[-1] != 'L' and match[-1] != 'R'  and match[-1] != ',') and 
            (match[-1] != '0' and match[-1] != '1'))


def find_strats(grid):
    instructions = find_path(grid)
    cs = combine(instructions, 4, 10)
    for perm in itertools.combinations(cs, 3):
        r = instructions
        for p in perm:
            r = r.replace(p, '')
        if len(r) == 0:
            r = instructions
            for i,p in enumerate(sorted(perm, reverse=True)):
                l = 'A' if i == 0 else 'B' if i ==1 else 'C'
                r = r.replace(p, l)
            return sorted(perm, key=len, reverse=True), r

# exit()
def a_strat():
    return 'L,10,L,10,L,4,L,6\n'

def b_strat():
    return 'L,6,R,12,L,6\n'

def c_strat():
    return 'R,12,L,10,L,4,L,6\n'

def main_strat():
    return 'B,C,B,C,B,A,C,A,B,A\n'

def video_strat():
    return 'y\n'

def start():
    for s in (main_strat() + a_strat() + b_strat() + c_strat() + video_strat()):
        yield ord(s)

def input_line(vm, strat):
    out = ''
    while True:
        c = vm.eval(strat)
        if c is None: assert False
        c = str(chr(c))
        if c == '\n':
            return out # + ''.join([str(chr(s)) for s in strat])
        out += c

def provide_input(vm, s):
    out = ''
    i = False
    while True:
        c = vm.eval()
        if c is None: assert False
        c = str(chr(c))
        if c == '\n':
            if not i: 
                i = True
                out = ''
                continue
            break
        out += c
    lines = []
    lines.append(out + ' ' + main_strat()[:-1])
    lines.append(input_line(vm, s) + ' ' + a_strat()[:-1])
    lines.append(input_line(vm, s) + ' ' + b_strat()[:-1])
    lines.append(input_line(vm, s) + ' ' + c_strat()[:-1])
    lines.append(input_line(vm, s) + ' ' + video_strat()[:-1])
    input_line(vm, s), a_strat()
    return lines

def capture_video(screen, vm, lines):
    prev_grid = []
    curses.curs_set(0)
    grid = []
    row = []
    i = 0
    for c in vm.run():
        if c > 255:
            lines.append("Total Dust: " + str(c))
            draw_grid(screen, prev_grid, lines)
            time.sleep(10)
        c = str(chr(c))
        if c == '\n':
            if row: grid.append(row)
            if len(grid) == 43:
                draw_grid(screen, grid, lines)
                i = 0
                if grid != []: prev_grid = grid
                grid = []
            row = []
            continue
        row.append(c)
        i += 1
    curses.curs_set(1)

# Part 1
mem = IntcodeVm.parse_memory(open('inputs/day17.txt').read())
mem[0] = 2
vm = IntcodeVm(mem)
grid = parse_grid(vm)
print(sum([x * y for x, y in find_intersections(grid)]))

# Part 2
print(find_strats(grid))
lines = provide_input(vm, start())
curses.wrapper(capture_video, vm, lines)
