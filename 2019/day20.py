data = """
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
""".splitlines()[1:]

_data = """
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               
""".splitlines()[1:]

# data = open('inputs/day20.txt').read().splitlines()

maze = {(x, y) for y in range(len(data)) for x in range(len(data[y])) if data[y][x] not in ' #'}
portals = {}
for i, line in enumerate(data[:-1]):
    for j, c in enumerate(line[:-1]):
        if c.isupper():
            if data[i+1][j].isupper():
                name = c + data[i+1][j]
                if i == 0 or i > len(data) // 2: portals[(j, i+2)] = name
                else: portals[(j, i-1)] = name
            if data[i][j+1].isupper():
                name = c + data[i][j+1]
                if j == 0 or j > len(data[0]) // 2: portals[(j+2, i)] = name
                else: portals[(j-1, i)] = name
import heapq

def neighbors(p, maze, portals):
    x, y = p
    for dx, dy in [(1,0), (0,1), (-1,0), (0,-1)]:
        xx, yy = x+dx, y+dy
        np = (xx, yy)
        if np in portals and portals[np] != 'AA' and portals[np] != 'ZZ':
            yield next(p2 for p2 in portals if portals[p2] == portals[np] and p2 != np), 1
        elif np in maze: yield np, 0
        if np in portals and portals[np] == 'ZZ': yield np, 1

def dijkstra(start, end, maze, portals):
    q = [(0, start, [])]
    seen = set()
    while q:
        d, p, h = heapq.heappop(q)
        if p == end: 
            print()
            print(h)
            for p in h:
                if p in portals: print(portals[p], end=' ')
            print()
            return d
        if p in seen: continue
        seen.add(p)
        for n, _p in neighbors(p, maze, portals): 
            heapq.heappush(q, (d+(1 if not _p else -1 if p == 1 else 0), n, h + [n])) # type: ignore

start = next(p for p in portals if portals[p] == 'AA')
end = next(p for p in portals if portals[p] == 'ZZ')
for i in range(len(data)):
    for j in range(len(data[i])):
        print(portals[(j, i)][0] if (j, i) in portals else '.' if (j, i) in maze else '#', end='')
    print()

print(dijkstra(start, end, maze, portals))
