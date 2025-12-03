data = """
987654321111111
811111111111119
234234234234278
818181911112111
""".strip().splitlines()

data = open('inputs/day3.txt').read().splitlines()

bats = [[int(c) for c in line] for line in data]

def battery_power(bat, n, p=0):
    if n == 0: return 0
    best = bat[m := max(range(p, len(bat)-n+1), key=bat.__getitem__)]
    return best * 10**(n-1) + battery_power(bat, n-1, m+1)

def total_power(bats: list[list[int]], n: int):
    return sum(battery_power(b, n) for b in bats)

print(total_power(bats, 2))
print(total_power(bats, 12))
