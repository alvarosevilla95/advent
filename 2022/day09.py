data = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""".strip()

data = open('inputs/day9.txt').read()

insts = [(line[0], int(line[1:])) for line in data.splitlines()]

dirs = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}

def simulate(rope, insts):
    head, *tail = rope
    visited = {tail[-1]}
    for d, n in insts:
        for i in range(n):
            head = (head[0] + dirs[d][0], head[1] + dirs[d][1])
            prev = head
            for i, t in enumerate(tail):
                t0, t1 = t
                if abs(prev[0]-t[0]) > 1 or abs(prev[1]-t[1]) > 1:
                    if abs(prev[0] - t[0]) >= 1: t0 += 1 if prev[0] > t[0] else -1
                    if abs(prev[1] - t[1]) >= 1: t1 += 1 if prev[1] > t[1] else -1
                    if i == len(tail)-1: visited |= {(t0, t1)}
                tail[i] = (t0, t1)
                prev = tail[i]
    return len(visited)

# part 1
print(simulate([(0, 0)] * 2, insts))

# part 2
print(simulate([(0, 0)] * 10, insts))
