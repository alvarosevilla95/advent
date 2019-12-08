with open('./input.txt') as f:
    stars = list(map(lambda x: list(map(int, x.split(','))), f.read().splitlines()))
    constellations = []
    while len(stars) > 0:
        s = stars.pop(0)
        c = [s]
        for i, const in enumerate(constellations):
            if any(map(lambda n: sum([abs(a - b) for a, b in zip(s, n)]) <= 3, const)):
                c += constellations.pop(i)
        constellations.append(c)
    print(len(constellations))
