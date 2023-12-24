import sys, curses, time, signal
from dataclasses import dataclass, field

F60 = 0.016

@dataclass
class DrawAction:
    kind: str
    new: list
    delay: float = 0

@dataclass
class Visualiser:
    rate: float = F60
    grid: list = field(default_factory=lambda: [[]])

    def __post_init__(self):
        self.init_with_context = False
        self.last_frame = 0
        self.voff = 0
        self.hoff = 0

    def __enter__(self):
        self.init_with_context = True
        try: self.curses_init()
        except: self.curses_cleanup(); raise
        return self

    def __exit__(self, *_): 
        self.curses_cleanup()

    def curses_init(self):
        self.screen = curses.initscr()
        screen = curses.initscr()
        screen.keypad(True)
        screen.nodelay(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        for i in range(curses.COLORS): curses.init_pair(i, i, -1)
        signal.signal(signal.SIGWINCH, self.resize_handler)
        if callable(self.grid): self.grid = self.grid()
        self.center_grid()

    def curses_cleanup(self):
        if not 'screen' in self.__dict__: return
        self.screen.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        signal.signal(signal.SIGWINCH, signal.SIG_DFL)

    def resize_handler(self, *_):
        curses.endwin()
        self.refresh()
        curses.LINES, curses.COLS = self.screen.getmaxyx()
        self.center_grid()
        self.screen.clear()
        self.draw_grid()

    def center_grid(self):
        if len(self.grid) < curses.LINES: self.voff = (len(self.grid) - curses.LINES) // 2
        if len(self.grid[0]) < curses.COLS: self.hoff = (len(self.grid[0]) - curses.COLS) // 2
        if len(self.grid) >= curses.LINES: self.voff = max(0, self.voff)
        if len(self.grid[0]) >= curses.COLS: self.hoff = max(0, self.hoff)

    def scren_size(self):
        return curses.COLS, curses.LINES

    def get_input(self):
        voff, hoff = self.voff, self.hoff
        if (k := self.screen.getch()) > 0:
            match chr(k):
                case 'q': sys.exit()
                case 'j': self.voff += 1
                case 'J': self.voff += 10
                case 'k': self.voff -= 1
                case 'K': self.voff -= 10
                case 'h': self.hoff -= 1
                case 'H': self.hoff -= 10
                case 'l': self.hoff += 1
                case 'L': self.hoff += 10
                case 'u': self.voff -= curses.LINES // 2
                case 'd': self.voff += curses.LINES // 2
                case 'g': self.voff = 0
                case 'G': self.voff = len(self.grid) - curses.LINES
                case '0': self.hoff = 0
                case '$': self.hoff = len(self.grid[0]) - curses.COLS
            self.voff = max(0, min(len(self.grid) - curses.LINES, self.voff))
            self.hoff = max(0, min(len(self.grid[0]) - curses.COLS+1, self.hoff))
        self.center_grid()
        return voff != self.voff or hoff != self.hoff

    def in_bounds(self, x, y):
        return self.hoff<=x<self.hoff+curses.COLS-1 and self.voff<=y<self.voff+curses.LINES

    def draw_grid(self, grid=None):
        if grid is not None: self.grid = grid
        self.center_grid()
        for i, l in enumerate(self.grid):
            for j, c in enumerate(l):
                if self.in_bounds(j, i): self.screen.addstr(i-self.voff, j-self.hoff, *c)
        self.refresh()

    def draw_char(self, x, y, c):
        self.grid[y][x] = c
        if self.in_bounds(x, y): self.screen.addstr(y-self.voff, x-self.hoff, *c)

    def draw_chars(self, chars):
        for c in chars: self.draw_char(*c)
        self.refresh()

    def refresh(self):
        self.screen.refresh()

    def run(self, draw):
        if not self.init_with_context:
            try: 
                self.curses_init()
                self._run(draw)
            finally: self.curses_cleanup()
        else: self._run(draw)

    def get_frame(self, delay=None):
        rate = delay or self.rate
        while (d := (t:=time.perf_counter()) - self.last_frame) < rate: 
            if self.get_input(): self.draw_grid()
            if d > F60: time.sleep(F60) # 60 fps polling
        self.last_frame = t
        
    def _run(self, draw):
        self.draw_grid()
        for action in draw():
            if self.get_input(): self.draw_grid()
            self.get_frame(action.delay)
            match action.kind:
                case 'grid': self.draw_grid(action.new)
                case 'char': self.draw_chars(action.new)
        self.draw_grid()
        while True: self.draw_grid() if self.get_input() else time.sleep(F60)
