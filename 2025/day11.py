# fmt: off

from functools import cache, reduce

# part 1
data = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""".strip()

# part 2
data = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""".strip()

data = open("inputs/day11.txt").read()

graph = { k: v.split() for k, v in (line.split(":") for line in data.splitlines()) }

add = lambda a, b: tuple(x + y for x, y in zip(a, b))

@cache
def count_paths(node):
  result = reduce(add, ((1, 0, 0, 0) if nxt == "out" else count_paths(nxt) for nxt in graph[node]), (0, 0, 0, 0))
  n, d, f, b = result
  match node:
    case "dac": return (0, n + d, 0, f + b)
    case "fft": return (0, 0, n + f, d + b)
    case _: return result


print(sum(count_paths("you")))

print(count_paths("svr")[-1])
