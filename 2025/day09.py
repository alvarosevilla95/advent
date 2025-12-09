data = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
""".strip()

data = open('inputs/day9.txt').read()

points = list(map(eval, data.splitlines()))
segments = [(points[i], points[(i+1) % len(points)]) for i in range(len(points))]

def area(a, b):
    return (abs(a[0]-b[0])+1) * (abs(a[1]-b[1])+1)

part1 = max(area(a, b) for i, a in enumerate(points) for b in points[i+1:])
print(part1)

xs = sorted({p[0] for p in points})
ys = sorted({p[1] for p in points})

def point_inside(cx, cy):
    crossings = sum(1 for (x1, y1), (x2, y2) in segments if x1 == x2 and x1 > cx and min(y1, y2) <= cy < max(y1, y2))
    return crossings % 2 == 1

nx, ny = len(xs) - 1, len(ys) - 1
psum = [[0] * (ny+1) for _ in range(nx+1)]
for i in range(nx):
    for j in range(ny):
        cx, cy = (xs[i] + xs[i+1]) / 2, (ys[j] + ys[j+1]) / 2
        val = 1 if point_inside(cx, cy) else 0
        psum[i+1][j+1] = val + psum[i][j+1] + psum[i+1][j] - psum[i][j]

x_idx = {x: i for i, x in enumerate(xs)}
y_idx = {y: j for j, y in enumerate(ys)}

def rect_inside(x1, x2, y1, y2):
    i1, i2 = x_idx[x1], x_idx[x2]
    j1, j2 = y_idx[y1], y_idx[y2]
    total = psum[i2][j2] - psum[i1][j2] - psum[i2][j1] + psum[i1][j1]
    return total == (i2 - i1) * (j2 - j1)

part2 = max(area(a, b) for i, a in enumerate(points) for b in points[i+1:] if rect_inside(min(a[0],b[0]), max(a[0],b[0]), min(a[1],b[1]), max(a[1],b[1])))
print(part2)
