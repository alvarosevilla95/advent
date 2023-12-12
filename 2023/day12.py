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
def count_matches(row, groups):
    count, curr, rest = 0, groups[0], groups[1:]
    for pos in range(len(row) - sum(groups) - len(rest) + 1):
        if '.' not in row[pos:pos+curr]:
            if not rest: count += '#' not in row[pos+curr:]
            elif row[pos+curr] != "#": count += count_matches(row[pos+curr+1:], rest)
        if row[pos] == "#": break
    return count

# part 1
print(sum(count_matches(*r) for r in rows))

#part2
rows = [('?'.join([s]*5), c*5) for s,c in rows]
print(sum(count_matches(*r) for r in rows))
