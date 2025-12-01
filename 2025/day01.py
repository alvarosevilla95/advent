test_input = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
""".strip()

data = open('inputs/day1.txt').read().splitlines()
# data = test_input.splitlines()

insts = [[x[0], int(x[1:])] for x in data]

x = 50
p1 = p2 = 0
d = 'R'
for i in insts:
    if i[0] != d: x, d = 100 -x, i[0]
    x = (x % 100) + i[1]
    if not x % 100: p1+=1
    p2 += x // 100

print(p1, p2)
