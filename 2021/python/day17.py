import re
data = "target area: x=20..30, y=-10..-5"

data = open('inputs/day17.txt').read()

(x0, x1), (y0, y1) = (map(int, g) for g in re.findall(r'=(-?\d+)\.\.(-?\d+)', data))

def sim(vel):
    x = y = my = 0
    while True:
        yield x, y, my
        x, y = x + vel[0], y + vel[1]
        vel = max(vel[0]-1, 0), vel[1]-1
        my = max(my, y)

valid = set()
for i in range(x1+1):
    for j in range(y0, -y0):
        for x, y, my in sim((i, j)):
            if x0 <= x <= x1 and y0 <= y <= y1:
                valid.add((i, j, my))
                break
            if x > x1 or y < y0:
                break
# part 1
print(sorted(valid, key=lambda x: (-x[1], x[0]))[0][2])

# part 2
print(len(valid))
