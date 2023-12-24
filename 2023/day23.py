from common import *

data = r"""
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
""".strip().splitlines()

data = open('inputs/day23.txt').read().splitlines()

dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

maze = {(x, y): c for y, line in enumerate(data) for x, c in enumerate(line) if c != '#'}
start = next(k for k in maze if k[1] == 0)
end = next(k for k in maze if k[1] == len(data)-1)

build_edges = lambda neighbors: {(x,y): {(xx, yy, 1) for dx, dy in neighbors((x,y)) if (xx:=x+dx, yy:=y+dy) in maze} for (x, y) in maze}

def dfs(edges, n, d=0, current=set()):
    if n == end: return {d}
    paths = set()
    for xx, yy, l in edges[n]: 
        if (c:=(xx, yy)) not in current: paths |= dfs(edges, c, d+l, current|{c})
    return paths

longest_path = lambda edges: max(*dfs(edges, start))

# part 1
p1_edges = build_edges(lambda n: ([dirs["<>^v".index(maze[n])]] if maze[n] in "<>^v" else dirs))
print(longest_path(p1_edges))

# part 2
p2_edges = build_edges(lambda _: dirs)
while to_remove := next(((n,e) for (n,e) in p2_edges.items() if len(e) == 2), None):
    n, (e1, e2) = to_remove
    p2_edges[e1[:2]].remove((*n, e1[2]))
    p2_edges[e2[:2]].remove((*n, e2[2]))
    p2_edges[e1[:2]].add((*e2[:2], e1[2]+e2[2])) # type: ignore
    p2_edges[e2[:2]].add((*e1[:2], e1[2]+e2[2])) # type: ignore
    del p2_edges[n]
print(longest_path(p2_edges))

# visualisation
def paths_dfs(edges, n, d=0, current=[]):
    if n == end: return [current]
    paths = []
    for xx, yy, l in edges[n]: 
        if (c:=(xx, yy)) not in current: paths += paths_dfs(edges, c, d+l, current+[c])
    return paths

grid = lambda: [[(c, curses.color_pair(4)) for c in line] for line in data]

def on_frame():
    paths = sorted(paths_dfs(p1_edges, start), key=len)
    for path in paths:
        for (x,y) in [start] + path:
            new = [(x, y, ('O', curses.color_pair(1)))]
            yield DrawAction('char', new)
        yield DrawAction('char', [], 0.5)
        yield DrawAction('grid', grid())

# Visualiser(0.01, grid).run(on_frame) # type: ignore
