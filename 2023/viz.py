import sys, curses, time
from random import randint

curses_voff = 0
curses_hoff = 0
curses_counter = 0
curses_window = None

def draw_grid(screen, grid, rate, fdraw, *args):
    global curses_voff, curses_hoff, curses_counter, curses_window
    if (k := curses_window.getch()) > 0: # type: ignore
        match chr(k):
            case 'q': sys.exit()
            case 'j': curses_voff += 1
            case 'J': curses_voff += 10
            case 'k': curses_voff -= 1
            case 'K': curses_voff -= 10
            case 'h': curses_hoff -= 1
            case 'H': curses_hoff -= 10
            case 'l': curses_hoff += 1
            case 'L': curses_hoff += 10
        curses_voff = max(0, min(len(grid) - curses.LINES, curses_voff))
        curses_hoff = max(0, min(len(grid[0]) - curses.COLS, curses_hoff))

    if len(grid) < curses.LINES: curses_voff = (len(grid) - curses.LINES) // 2
    if len(grid[0]) < curses.COLS: curses_hoff = (len(grid[0]) - curses.COLS) // 2

    if rate < 0 and randint(0, -rate-1) != 0: return
    if rate > 0: rate, curses_counter = 0, time.perf_counter() + rate

    for i, l in enumerate(grid):
        for j, _ in enumerate(l):
            if not (curses_voff<= i<curses_voff+curses.LINES and curses_hoff<=j<curses_hoff+curses.COLS): continue
            screen.addstr(i - curses_voff, j - curses_hoff, fdraw(j, i, grid, *args))
    screen.refresh()

    if rate == 0 and time.perf_counter() < curses_counter: draw_grid(screen, grid, rate, fdraw, *args) # type: ignore

def wrap_in_curses(f, *args):
    def cf(*args):
        global curses_window
        curses.use_default_colors()
        curses.curs_set(0)
        curses_window = curses.initscr()
        curses_window.nodelay(True)
        f(*args)
    curses.wrapper(cf, *args)
