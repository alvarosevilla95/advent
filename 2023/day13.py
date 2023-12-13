data = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""".strip()

data = open('inputs/day13.txt').read()

patterns = list(map(str.splitlines, data.split('\n\n')))

sym = lambda pattern, i: sum(a != b for pair in zip(pattern[i-1::-1], pattern[i:]) for a, b in zip(*pair))
find_sym = lambda pattern, smudge: next((i for i in range(len(pattern)) if sym(pattern, i) == smudge), 0)
sym_value = lambda pattern, smudge: 100 * find_sym(pattern, smudge) + find_sym(list(zip(*pattern)), smudge)

# part 1
print(sum(sym_value(pattern, 0) for pattern in patterns))

# part 2
print(sum(sym_value(pattern, 1) for pattern in patterns))
