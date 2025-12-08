import curses
import time

data = open('inputs/day7.txt').read()
grid = [list(line) for line in data.splitlines()]
S = next((i, j) for i, row in enumerate(grid) for j, c in enumerate(row) if c == "S")

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # beams
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)    # splitters
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # active split
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)   # start

    max_y, max_x = stdscr.getmaxyx()
    view_h = max_y - 3  # leave room for header/footer

    def draw_grid(beams, splits, breaks, scroll_y):
        stdscr.clear()
        stdscr.addstr(0, 0, f"Breaks: {breaks}  Beams: {len(beams)}  Row: {scroll_y}/{len(grid)}", curses.A_BOLD)

        for screen_row in range(view_h):
            i = scroll_y + screen_row
            if i >= len(grid):
                break
            row = grid[i]
            for j, c in enumerate(row):
                if j + 2 >= max_x - 1:
                    break

                if (i, j) in splits:
                    stdscr.addstr(screen_row + 1, j + 2, "^",
                                  curses.color_pair(3) | curses.A_BOLD)
                elif (i, j) in beams:
                    stdscr.addstr(screen_row + 1, j + 2, "*",
                                  curses.color_pair(1) | curses.A_BOLD)
                elif c == "S":
                    stdscr.addstr(screen_row + 1, j + 2, "S",
                                  curses.color_pair(4) | curses.A_BOLD)
                elif c == "^":
                    stdscr.addstr(screen_row + 1, j + 2, "^",
                                  curses.color_pair(2))
                else:
                    stdscr.addstr(screen_row + 1, j + 2, ".")

        stdscr.refresh()

    beams, breaks, scroll_y = {S}, 0, 0
    draw_grid(beams, set(), breaks, scroll_y)
    time.sleep(0.5)

    for _ in range(len(grid) - 1):
        moved = {(r + 1, c) for r, c in beams}
        splits = {p for p in moved if grid[p[0]][p[1]] == "^"}
        beams = (moved - splits) | {(r, c + d) for r, c in splits for d in (-1, 1)}
        breaks += len(splits)

        beam_rows = {r for r, _ in beams}
        if beam_rows:
            max_beam_row = max(beam_rows)
            target_scroll = max(0, max_beam_row - view_h * 2 // 3)
            scroll_y = min(target_scroll, len(grid) - view_h)

        draw_grid(beams, splits, breaks, scroll_y)
        time.sleep(0.03)

    stdscr.addstr(max_y - 2, 0, f"Final: {breaks} breaks", curses.A_BOLD)
    stdscr.addstr(max_y - 1, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
