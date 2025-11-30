from itertools import count
from visualizer import PyGameVisualizer
from collections import defaultdict

data = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

# data = open('inputs/day17.txt').read().strip()

wind = [-1 if c == '<' else 1 for c in data]

shapes = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(0, 0), (1, 0), (0, 1), (1, 1)},
]

def collides(shape, settled):
    for x, y in shape:
        if (x, y) in settled: return True
        if (y == 0): return True
        if not (0<=x<7): return True
    return False

def settle(shape, settled):
    for s in shape: settled.add(s)
    return max(y for _, y in settled)

hh = 70

t = 1000000000000
cache = set()
with PyGameVisualizer(lines=hh+1, cols=10, cell_size=10, fps=6) as vis:
    vis.palette = {1: (255, 255, 255), 0: (0, 0, 0)}
    wi = 0
    height = 0
    settled = set()
    for i in count():
        shape = shapes[i % len(shapes)]
        h = height + 4  # type: ignore
        dx = 2
        shape = {(x+dx, y+h) for x, y in shape}
        _h = height
        while True:
            # vis.draw_grid(defaultdict(lambda: 0, { (x,hh-y): 1 for (x,y) in settled | shape}), (0, min(0, hh-height-10)))
            # vis.get_frame()
            w, wi = wind[wi], (wi+1) % len(wind)
            next_shape = {(x+w, y) for x, y in shape}
            if not collides(next_shape, settled): shape = next_shape
            next_shape = {(x, y-1) for x, y in shape}
            if collides(next_shape, settled):
                height = settle(shape, settled)
                break
            shape = next_shape
        if i+1 == 2022: 
            print(height)
        sub = tuple({(x, height - y) for (x,y) in settled if height - y <= 30})
        key = (sub, wi, i % len(shapes))
        if key in cache:
            print("FOUND")
            print(i, height)
            print(i, _h)
            print(t//(i+1))
            print(t//(i+1)*_h)
            break
        cache.add(key)




