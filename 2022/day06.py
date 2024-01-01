data = """
mjqjpqmgbljsphdztnvjfqwrcgsmlb
""".strip()

data = open('inputs/day6.txt').read()

find_marker = lambda l: next(i+l for i in range(len(data)) if len(data[i:i+l]) == len(set(data[i:i+l])))

# part 1
print(find_marker(4))

# part 2
print(find_marker(14))

