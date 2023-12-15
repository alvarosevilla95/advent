from common import *

data = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
""".strip()

data = open('inputs/day15.txt').read().strip()

groups = data.split(',')

# part 1
hash = lambda s: reduce(lambda h, c: (h + ord(c)) * 17 % 256, s, 0)
print(sum(map(hash, groups)))

# part 2
boxes = defaultdict(dict)

for g in groups:
    b, f = re.split('=|-', g)
    if '=' in g: boxes[hash(b)][b] = int(f)
    if '-' in g: boxes[hash(b)].pop(b, 0)

print(sum((i+1)*j*l for i in boxes for j, l in enumerate(boxes[i].values(), 1)))
