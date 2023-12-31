from functools import cache
from itertools import product

p1, p2 = 4, 8
p1, p2 = 5, 9

def part1(pos1, pos2, score1=0, score2=0, i=0):
    if score2 >= 1000: return i*score1
    return part1(pos2, pos1:=(pos1 + 3*i+6) % 10 or 10 , score2, score1+pos1, i+3)

print(part1(p1, p2))

moves = [(i, sum(sum(c) == i for c in product(range(1, 4), repeat=3))) for i in range(3, 10)]

@cache
def part2(pos1, pos2, score1=0, score2=0):
    if score2 >= 21: return 0, 1
    wins1, wins2 = 0, 0
    for move, n in moves:
        npos1 = (pos1 + move) % 10 or 10
        w2, w1 = part2(pos2, npos1, score2, score1 + npos1)
        wins1, wins2 = wins1 + n*w1, wins2 + n*w2
    return wins1, wins2

print(max(part2(p1, p2)))
