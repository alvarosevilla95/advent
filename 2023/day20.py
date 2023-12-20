from common import *

data = r"""
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
""".strip().splitlines()

data = open('inputs/day20.txt').read().splitlines()

mods = {}
sources = defaultdict(dict)

for line in data:
    mod, targets = line.split(' -> ')
    targets = targets.split(', ')
    if mod[0] == '%': mod, value = mod[1:], ['flip', targets, 0]
    elif mod[0] == '&': mod, value = mod[1:], ['conj', targets, sources[mod[1:]]]
    else: value = ['broad', targets]
    for target in targets: sources[target][mod] = 0
    mods[mod] = value

def press_button(i):
    highs, lows = 0, 0 
    queue = [('button', 'broadcaster', 0)] 
    while queue:
        source, name, value = queue.pop(0)
        highs, lows = highs + value, lows + (not value)
        if source in triggers and not triggers[source] and value: triggers[source] = i
        if name not in mods: continue
        mod = mods[name]
        if mod[0] == 'flip':
            if value: continue
            mod[2] = not mod[2]
            send = mod[2]
        elif mod[0] == 'conj':
            mod[2][source] = value
            send = not all(mod[2].values())
        else:
            send = value
        queue += [(name, t, send) for t in mod[1]]
    return highs, lows

highs, lows = 0, 0
triggers = {k: 0 for k in mods[next(iter(sources['rx']))][2]}
for i in count(1):
    h, l = press_button(i)
    highs, lows = highs + h, lows + l
    # part 1
    if i == 1000: 
        print(highs  * lows)
    # part 2
    if all(triggers.values()):
        print(lcm(*triggers.values()))
        break
