from math import inf

def get_tree(edges):
    orbits = {}
    for o in edges:
        orbits.setdefault(o[0], []).append(o[1]) 
    return orbits

def get_graph(edges):
    graph = {}
    for o in edges:
        graph.setdefault(o[0], []).append(o[1]) 
        graph.setdefault(o[1], []).append(o[0]) 
    return graph

def total_orbits(tree, node, c=0):
    return c if node not in tree else c + sum(map(lambda n: total_orbits(tree, n, c + 1), tree[node])) 

def dijkstra(graph, a, b):
    unvisited = list(graph.keys())
    distances = { u : inf for u in unvisited }
    distances[a] = 0
    while len(unvisited) > 0:
        curr = min(unvisited, key=lambda x: distances[x])
        for c in graph[curr]:
            distances[c] = min(distances[c], distances[curr] + 1)
        unvisited.remove(curr)
    return distances[b]

data = open('./input.txt').read()
edges = list(map(lambda l: l.split(')'), data.splitlines()))
# Part 1
print(total_orbits(get_tree(edges), 'COM'))
# Part 2
print(dijkstra(get_graph(edges), 'YOU', 'SAN') - 2) # subtract 2 as the 'YOU' and 'SAN' edges don't count
