def split(lst, size):
    return [lst[i:i+size] for i in range(0, len(lst), size)]

def collapse(layers):
    return [next(filter(lambda v: v != 2, lay)) for lay in zip(*layers)]

def draw(img):
    for r in img: print(*['#' if x == 1 else ' ' for x in r])

lenx, leny = 25, 6
data = [int(x) for x in open('./input.txt').read().strip('\n')]
layers = split(data, lenx*leny)


# Part 1
best = min(layers, key=lambda l: l.count(0))
print(best.count(1) * best.count(2))

# Part 2
img = split(collapse(layers), lenx)
draw(img)
