import re
data = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

data = open('inputs/day5.txt').read()

state, insts = data.split('\n\n')
state = [list(line[1::4]) for line in state.splitlines()[:-1]]
state = [[x for x in row if x != ' '] for row in [*zip(*state)]]
insts = [list(map(int, re.findall(r'\d+', line))) for line in insts.splitlines()]

def move_boxes(state, by_one=False):
    for (n, f, t) in insts:
        take = state[f-1][:n]
        state[f-1] = state[f-1][n:]
        state[t-1] = take[::by_one or -1] + state[t-1]
    return ''.join([s[0] for s in state])

# part 1
print(move_boxes(state.copy()))

# part 2
print(move_boxes(state, True))

