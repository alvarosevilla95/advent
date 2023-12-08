from common import *

data = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".strip().splitlines()

data = open('inputs/day2.txt')

games = [[{c: int(v) for v, c in re.findall(r'(\d+) (\w+)', game)} for game in line.split(';')] for line in data]

# part 1
possible = { "red": 12, "green": 13, "blue": 14 }
is_possible = lambda game: all(r.get(c, 0) <= v for r in game for c,v in possible.items())
print(sum(i + 1 for i, game in enumerate(games) if is_possible(game)))

# part 2
score = lambda g: prod(max(r.get(c, 0) for r in g) for c in {c for r in g for c in r}) # type: ignore
print(sum(map(score, games)))
