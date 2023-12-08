from common import *

data = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".strip()

data = open('inputs/day8.txt').read()

steps = data.splitlines()[0]
nodes = {m[0]: m[1:] for m in re.findall(r'(\w+) = \((\w+), (\w+)\)', data)}

# part 1
find = lambda node, pred, i=0: i if pred(node) else find(nodes[node][steps[i%len(steps)] == 'R'], pred, i+1)
print(find('AAA', lambda n: n == 'ZZZ'))

# part 2
print(reduce(lcm, (find(n, lambda p: p[-1] == 'Z') for n in nodes if n[-1] == 'A')))
