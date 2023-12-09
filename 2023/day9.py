data = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""".strip().splitlines()

data = open('inputs/day9.txt')

values = [[int(c) for c in line.split()] for line in data]

# part 1
predict = lambda s: s[-1] + predict([b - a for a, b in zip(s, s[1:])]) if s else 0
print(sum(map(predict, values)))

# part 2
print(sum(map(lambda v: predict(v[::-1]), values)))
