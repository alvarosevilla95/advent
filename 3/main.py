# TODO: change to deltas instead of putting all points
def get_path(insts):
    dx = dict(zip('LRDU', [-1, 1, 0, 0]))
    dy = dict(zip('LRDU', [0, 0, -1, 1]))
    grid, x, y, c = {}, 0, 0 ,0
    for inst in insts:
        for i in range(int(inst[1:])):
            x += dx[inst[0]]
            y += dy[inst[0]]
            c += 1
            if (x, y) not in grid:
                grid[x, y] = c 
    return grid

def distance(point):
    return abs(point[0]) + abs(point[1])

def steps(grid_1, grid_2, point):
    return grid_1[point] + grid_2[point]

with open('./input.txt') as f:
    lines = f.read().splitlines()
    insts_1 = lines[0].split(',')
    insts_2 = lines[1].split(',')
    # insts_1 = 'R8,U5,L5,D3'.split(',')
    # insts_2 = 'U7,R6,D4,L4'.split(',')
    # insts_1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(',')
    # insts_2 = 'U62,R66,U55,R34,D71,R55,D58,R83'.split(',')

    grid_1 = get_path(insts_1)
    grid_2 = get_path(insts_2)

    # Part 1
    union = grid_1.keys() & grid_2.keys()   
    closest = min(union, key=distance)
    print(distance(closest))

    # Part 2
    closest = min(union, key=lambda p: steps(grid_1, grid_2, p))
    print(steps(grid_1, grid_2, closest))


