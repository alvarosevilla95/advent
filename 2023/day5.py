from common import *

data = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".strip()

data = open('inputs/day5.txt').read()

seeds, *maps = data.split('\n\n')
seeds = [int(i) for i in seeds.split()[1:]]
maps = [[[int(i) for i in line.split()] for line in m.splitlines()[1:]] for m in maps]

# part 1
def map_seed(s, m):
    for md, ms, ml in m:
        if s >= ms and s < ms + ml:
            return s + md - ms
    return s
print(min(reduce(map_seed, maps, s) for s in seeds))

# part 2
ranges = list(zip(seeds[::2], seeds[1::2]))
for m in maps:
    new_ranges = []
    for rs, rl in ranges:
        for md, ms, ml in m:
            if rs < ms + ml and ms < rs + rl:
                os = max(rs, ms)
                ol = min(rs + rl, ms + ml) - os
                new_ranges += [(os - ms + md, ol)]
                if os > rs: ranges += [(rs, os - rs)]
                if os + ol < rs + rl: ranges += [(os + ol, rs + rl - os - ol)]
                break
        else: new_ranges += [(rs, rl)]
    ranges = new_ranges
print(min(r for r, _ in ranges))
