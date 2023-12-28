def calc_fuel(mass):
    return max(mass // 3 - 2, 0)

def calc_fuel_full(mass):
    if mass == 0: return 0
    fuel = calc_fuel(mass)
    return fuel + calc_fuel_full(fuel)

with open('inputs/day01.txt') as f:
    modules = [int(m) for m in f.read().splitlines()]
    total = sum(map(calc_fuel_full, modules))
    print(total)
