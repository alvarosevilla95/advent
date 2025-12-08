import curses, time
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import NamedTuple

class Pt(NamedTuple):
    r: int; c: int
    def down(self): return Pt(self.r + 1, self.c)
    def split(self): return Pt(self.r, self.c - 1), Pt(self.r, self.c + 1)

@dataclass(frozen=True)
class State:
    beams: frozenset[Pt]; splits: frozenset[Pt]; breaks: int
    def step(self, grid):
        moved = frozenset(b.down() for b in self.beams)
        hits = frozenset(p for p in moved if grid[p.r][p.c] == "^")
        return State((moved - hits) | frozenset(s for p in hits for s in p.split()), hits, self.breaks + len(hits))

THEME = {"beam": (1, "|"), "split": (2, "^"), "active": (3, "^"), "start": (4, "S"), "empty": (5, "."), "border": (6, "|")}

def load(path):
    grid = Path(path).read_text().splitlines()
    return grid, next(Pt(i, j) for i, row in enumerate(grid) for j, c in enumerate(row) if c == "S")

def simulate(grid, start):
    return reduce(lambda acc, _: acc + [acc[-1].step(grid)], range(len(grid) - 1), [State(frozenset([start]), frozenset(), 0)])

def cell_style(p, c, state):
    if p in state.splits: return THEME["active"][1], THEME["active"][0], curses.A_BOLD
    if p in state.beams:  return THEME["beam"][1], THEME["beam"][0], curses.A_BOLD
    if c == "S": return THEME["start"][1], THEME["start"][0], curses.A_BOLD
    if c == "^": return THEME["split"][1], THEME["split"][0], 0
    return THEME["empty"][1], THEME["empty"][0], 0

def render(scr, grid, state, scroll):
    max_y, max_x = scr.getmaxyx(); view_h = max_y - 4; scr.erase()
    grid_w = len(grid[0]) if grid else 0; off = max(0, (max_x - grid_w) // 2)
    header = f" * Breaks: {state.breaks:4d}  |  Beams: {len(state.beams):3d}  |  Depth: {scroll}/{len(grid)} "
    hdr_off = max(0, (max_x - len(header)) // 2)
    scr.addstr(0, hdr_off, "-" * len(header), curses.color_pair(6))
    scr.addstr(1, hdr_off, header, curses.color_pair(6) | curses.A_BOLD)
    scr.addstr(2, hdr_off, "-" * len(header), curses.color_pair(6))
    for sr, gr in enumerate(range(scroll, min(scroll + view_h, len(grid)))):
        if sr + 3 >= max_y - 1: break
        for j, c in enumerate(grid[gr][:max_x - off]):
            ch, pair, attr = cell_style(Pt(gr, j), c, state)
            scr.addstr(sr + 3, off + j, ch, curses.color_pair(pair) | attr)
    scr.refresh()

def main(stdscr):
    curses.curs_set(0); curses.start_color(); curses.use_default_colors()
    for i, (fg, bg) in enumerate([(curses.COLOR_YELLOW, -1), (curses.COLOR_CYAN, -1), (curses.COLOR_RED, -1), (curses.COLOR_GREEN, -1), (238, -1), (curses.COLOR_BLUE, -1)], 1):
        curses.init_pair(i, fg, bg)
    grid, start = load("inputs/day7.txt"); view_h = stdscr.getmaxyx()[0] - 4
    for state in simulate(grid, start):
        scroll = min(max(0, max((b.r for b in state.beams), default=0) - view_h * 2 // 3), max(0, len(grid) - view_h))
        render(stdscr, grid, state, scroll); time.sleep(0.03)
    msg = f">> Complete: {state.breaks} breaks  [press any key]"  # pyright: ignore[reportPossiblyUnboundVariable]
    stdscr.addstr(stdscr.getmaxyx()[0] - 1, (stdscr.getmaxyx()[1] - len(msg)) // 2, msg, curses.color_pair(4) | curses.A_BOLD)
    stdscr.refresh(); stdscr.getch()

if __name__ == "__main__": curses.wrapper(main)
