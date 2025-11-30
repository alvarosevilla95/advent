import re
data = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".strip()

data = open('inputs/day15.txt').read()

sensors = [[*map(int, re.findall(r'(\d+)', line))] for line in data.splitlines()]

def intersect(sensor, line):
    sx, sy = sensor[:2]
    bx, by = sensor[2:]
    # if not (sy<=line<=by or by<=line<=sy): return set()
    dist = abs(sx-bx) + abs(sy-by)
    dist2 = dist - abs(line-sy)
    return set(range(sx - dist2, sx + dist2 + 1))

y = 10
y = 2000000
y = 13
unavailable = set()
for s in sensors: unavailable |= intersect(s, y)

for s in sensors:
    if s[3] == y and s[2] in unavailable: unavailable.remove(s[2])

print(len(unavailable))
# print(unavailable)
print()

maxc = 4000000

total = set()
for y in range(maxc):
    print(y)
    unavailable = set()
    for s in sensors: 
        unavailable |= intersect(s, y)
    available = set(range(maxc)) - unavailable
    if y == 5: 
        pass
        # print(unavailable)
        # print(available)
        # print({(a, y) for a in available})
    total |= { (a, y) for a in available}
    # print(y, total)

for s in sensors:
    if (s[0], s[1]) in total: total.remove((s[0], s[1]))
    if (s[2], s[3]) in total: total.remove((s[2], s[3]))
print(len(total))
# print(total)
