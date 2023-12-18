from common import *

data = r"""
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
""".strip().splitlines()

data = open('inputs/day18.txt').read().splitlines()

steps = [re.match(r'(\w) (\d+) \(#(.+)\)', line).groups() for line in data] # type: ignore

dirs = [(1,0), (0,1), (-1,0), (0,-1)]

def _area(steps):
    outer, vs = 0, [(0, 0)]

    # Find perimeter and vertices
    for n, (x,y) in steps: 
        outer += n
        vs += [(vs[-1][0] + x*n, vs[-1][1] + y*n)]

    # https://en.wikipedia.org/wiki/Shoelace_formula
    area = sum(x1*y2 - x2*y1 for (x1,y1), (x2,y2) in zip(vs, vs[1:])) // 2

    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    # area = inner + outer // 2 - 1
    # inner + outer = area + outer // 2 + 1
    return area + outer // 2 + 1

# Alternative implementation, only works for horizontal and vertical lines
# Green's theorem shows that A = ∫x dy = ∫-y dx, so with only horizontal and vertical lines, A = Σx_i * Δy = -Σy_i * Δx
# For more general polygons, this becomes A = Σ(x_i+x_(i+1))/2 * Δy_i (the shoelace trapezoid formula)
def area(steps):
    outer, xpos, area = 0, 0, 0
    for n, (x,y) in steps: 
        outer += n
        # We can keep track of only x position, area += xpos * Δy for each side
        xpos += x*n
        area += xpos * y*n
    # Then apply Pick's theorem as above
    return area + outer // 2 + 1

# part 1
print(_area((int(s), dirs['RDLU'.index(d)]) for d,s,_ in steps))

# part 2
print(area((int(color[:5], 16), dirs[int(color[5])] ) for _,_,color in steps))
