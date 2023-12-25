from common import *

data = r"""
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
""".strip().splitlines()

data = open('inputs/day25.txt').read().splitlines()

# part 1
edges = [(a, b) for a, b in map(lambda x: x.split(': '), data) for b in b.split()]
graph = nx.from_edgelist(edges)
partitions = nx.stoer_wagner(graph)[1]
print(prod(map(len, partitions)))

# part 2
print("Merry Christmas!")
