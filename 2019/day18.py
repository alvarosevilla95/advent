data = """
###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############
""".strip().splitlines()

# data = open('inputs/day18.txt').read().splitlines()

maze = {(x,y): c for y, line in enumerate(data) for x, c in enumerate(line) if c != '#'}

start = next(k for k, v in maze.items() if v == '@')
gates = {k: v for k, v in maze.items() if v.isupper()}
keys = {k: v for k, v in maze.items() if v.islower()}

from collections import deque

def bfs(starts, keys):
    queue = deque([(0, starts, set(), [])])
    seen = set()
    while queue:
        steps, poss, collected, hist = queue.popleft()
        key = (tuple(sorted(poss)), tuple(sorted(collected)))
        if key in seen: continue
        seen.add(key)
        n = set()
        for pos in poss:
            if pos in keys: 
                n = {pos}
                if len(collected) == len(keys): 
                    return steps
        for pos in poss:
            nposs = [p for p in poss if p != pos]
            for dx, dy in [(0,1),(1,0),(-1,0),(0,-1)]:
                newpos = (pos[0]+dx, pos[1]+dy)
                if newpos in maze and (newpos not in gates or maze[newpos].lower() in [keys[c] for c in collected]):
                    queue.append((steps+1, nposs + [newpos], collected | n, hist + [newpos])) # type: ignore


bots = []
for i in (-1, 0, 1):
    for j in (-1, 0, 1):
        if i and j:
            maze[(start[0]+i, start[1]+j)] = '@'
            bots.append((start[0]+i, start[1]+j))
        elif (p:=start[0]+i, start[1]+j) in maze: del maze[(start[0]+i, start[1]+j)]

for i in range(len(data)):
    for j in range(len(data[0])):
        print(maze[(j,i)] if (j,i) in maze else '#', end='')
    print()

print(bfs(bots, keys))
