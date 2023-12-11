from common import *

data = """
Time:      7  15   30
Distance:  9  40  200
""".strip().splitlines()

data = open('inputs/day6.txt').read().splitlines()

def possible_ranges(race):
    time, dist = race
    d = (time**2 - 4*dist)**0.5 / 2
    min = ceil(time/2 - d)
    max = floor(time/2 + d)
    return max - min + 1

# part 1
races = list(zip(*[map(int, re.findall(r'\d+', line)) for line in data]))
print(prod(map(possible_ranges, races)))

# part 2
race = [int(line.split(":")[1].replace(" ", "")) for line in data]
print(possible_ranges(race))
