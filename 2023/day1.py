import regex as re

data = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixtee
""".strip().splitlines()

data = open('inputs/day1.txt').read().splitlines()

# part 1
def first_and_last(line):
    match = re.findall(r'(\d)', line)
    return int(match[0] + match[-1])

print(sum(map(first_and_last, data)))

# part 2
def with_spelled(line):
    spelled = ['zero','one','two','three','four','five','six','seven','eight','nine']
    match = re.findall(fr'(\d|{"|".join(spelled)})', line, overlapped=True)
    match = [str(spelled.index(i)) if i in spelled else i for i in match]
    return int(match[0] + match[-1])

print(sum(map(with_spelled, data)))
