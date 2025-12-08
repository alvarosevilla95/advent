from math import prod, dist
from itertools import combinations

data = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""".strip()

data = open('inputs/day8.txt').read()

boxes = list(map(eval, data.splitlines()))
size = len(boxes)
dists = sorted(combinations(range(size), 2), key=lambda ij: dist(boxes[ij[0]], boxes[ij[1]]))

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def unite(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry: return
        self.parent[rx] = ry
        self.size[ry] += self.size[rx]
        self.size[rx] = 0

uf = UnionFind(size)

for step, (i, j) in enumerate(dists, 1):
    uf.unite(i, j)

    if step == 1000:
        print(prod(sorted(uf.size, reverse=True)[:3]))

    if uf.size[uf.find(j)] == size:
        print(boxes[i][0] * boxes[j][0])
        break
