from intcode import IntcodeVm

program = open('inputs/day23.txt').read()

def pipe_in(i, buf):
    while True: 
        idle[i] = len(buf) == 0
        yield buf.pop(0) if buf else -1

computers = [IntcodeVm(program) for _ in range(50)]
idle = [0 for _ in range(50)]
queues = [[i] for i in range(50)]
pipes = [pipe_in(i, q) for i, q in enumerate(queues)]
outputs = []
nat_queue = []
seen = set()
part1_done = False

while True:
    for i, computer in enumerate(computers):
        add = computer.eval_one(pipes[i])
        if add is not None: 
            x = computer.eval(pipes[i])
            y = computer.eval(pipes[i])
            if add == 255: 
                nat_queue = [x, y]
                if not part1_done:
                    print(y)
                    part1_done = True
            else: queues[add] += [x, y]
    if all(idle) and nat_queue:
            if nat_queue[1] in seen: 
                print(nat_queue[1])
                exit()
            seen.add(nat_queue[1])
            queues[0] += nat_queue # type: ignore
            nat_queue = []
