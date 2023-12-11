data = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".strip().splitlines()

data = open('inputs/day7.txt')

plays = [line.split() for line in data]

# part 1
order = "23456789TJQKA"

def part1_score(play):
    hand, _ = play
    counts = sorted([hand.count(label) for label in set(hand)], reverse=True)
    return [counts, [order.index(c) for c in hand]]

def total_score(plays):
    return sum(int(bid) * (i+1) for i, (_, bid) in enumerate(plays))

print(total_score(sorted(plays, key=part1_score)))

# part 2
order = "J23456789TQKA"

def part2_score(play):
    hand, _ = play
    counts = sorted([hand.count(label) for label in set(hand) - {'J'}], reverse=True)
    if counts: counts[0] += hand.count('J')
    else: counts = [5]
    return [counts, [order.index(c) for c in hand]]

print(total_score(sorted(plays, key=part2_score)))
