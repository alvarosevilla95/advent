from functools import reduce
from math import prod
from operator import add, mul

data = """
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
""".strip()

data = open('inputs/day6.txt').read()

*number_rows, op_row = data.splitlines()

columns = zip(*[map(int, r.split()) for r in number_rows])
ops = [(sum, prod)[op == "*"] for op in op_row.split()]
print(sum(op(col) for op, col in zip(ops, columns)))

op_pos = [i for i, c in enumerate(op_row) if c in "+*"]
max_len = max(map(len, number_rows))
boundaries = [(op_pos[i], op_pos[i+1] if i+1 < len(op_pos) else max_len) for i in range(len(op_pos))]

def extract_number(col):
    digits = "".join(r[col] for r in number_rows if col < len(r) and r[col] != " ")
    return int(digits) if digits else None

def apply_op(op, start, end):
    nums = [n for col in range(start, end) if (n := extract_number(col)) is not None]
    return reduce(add if op == "+" else mul, nums)

print(sum(apply_op(op_row[start], start, end) for start, end in boundaries))
