import re
from math import prod, lcm
from functools import reduce

data = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".strip()

# data = open('inputs/day11.txt').read()

def parse_monkey(monkey):
    lines = monkey.splitlines()
    items = [int(n) for n in re.findall(r'-?\d+', lines[1])]
    operation = lines[2].split('= ')[1]
    test = int(lines[3].split()[3])
    if_true = int(lines[4].split()[-1])
    if_false = int(lines[5].split()[-1])
    return items, operation, test, if_true, if_false

monkeys = [parse_monkey(monkey) for monkey in data.split('\n\n')]

common = lcm(*[m[2] for m in monkeys])

def round(p1):
    totals = []
    for m in monkeys:
        items, operation, test, if_true, if_false = m
        totals += [len(items)]
        while items:
            old = items.pop(0)
            new = eval(operation)
            new = (new // 3) if p1 else (new % common)
            target = if_true if new % test == 0 else if_false
            monkeys[target][0].append(new)
    return totals

play = lambda rounds, p1: reduce(lambda a, b: [x + y for x, y in zip(a, b)], [round(p1) for _ in range(rounds)])
score = lambda totals: prod(sorted(totals)[-2:])

# part 1
print(score(play(20, 1)))

# part 2
monkeys = [parse_monkey(monkey) for monkey in data.split('\n\n')]
print(score(play(10000, 0)))
