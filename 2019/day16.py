def value(data, i, pattern):
    actual = []
    for p in pattern: actual += [p for _ in range(i+1)]
    actual = actual[1:] + actual[:1]
    val = 0
    for j, d in enumerate(data): val += d * actual[j%len(actual)]
    return abs(val) % 10

# Part 1
pattern = [0, 1, 0, -1]
raw = open('inputs/day16.txt').read().strip()
data = [int(s) for s in raw]
for _ in range(100): data = [value(data, i, pattern) for i in range(len(data))]
print(data[:8])

# Part 2
raw = open('inputs/day16.txt').read().strip()
data = [int(s) for s in raw] * 10000
offset = int(raw[:7])
assert offset > len(data) // 2 # Method only works on the right half of the data
for _ in range(100):
    rest_sum = sum(data[offset:])
    for i in range(offset, len(data)):
        data[i], rest_sum = abs(rest_sum) % 10, rest_sum - data[i]
print(data[offset: offset+8])
