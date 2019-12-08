import numpy as np

num_players = 404
scores = list(map(lambda x: int(x), np.zeros(num_players)))
marbles = list(range(71853))

circle = [marbles.pop(0)]

i = 0
player = 0
while len(marbles) > 0:
    m = marbles.pop(0)
    if m % 23 == 0:
        i = (i - 7) % len(circle)
        scores[player] += m + circle.pop(i)
        continue
    i = (i + 2) % len(circle)
    if i == 0: i = len(circle)
    circle.insert(i, m)
    player = (player + 1) % num_players

print(max(scores))
