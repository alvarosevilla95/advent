from common import *

data = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""".strip().splitlines()

data = open('inputs/day12.txt').read().splitlines()

rows = [(s, tuple(map(int, c.split(',')))) for s, c in (line.split() for line in data)]

@cache
def count_matches(r, g, s=0):
    if not g: return '#' not in r
    if not r: return (s,) == g
    if r[0] == '.': return 0 if s and s != g[0] else count_matches(r[1:], g[s or 0:]) 
    if r[0] == "#": return 0 if s == g[0] else count_matches(r[1:], g, s+1)
    if s: return count_matches(r[1:], *(g, s+1) if s != g[0] else (g[1:], 0))
    return count_matches(r[1:], g) + count_matches(r[1:], g, 1)


all_possible = lambda rows: sum(count_matches(*r) for r in rows)

# part 1
print(all_possible(rows))

#part2
print(all_possible(('?'.join([s]*5), c*5) for s, c in rows))
