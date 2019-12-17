def load_program(code):
    return list(map(lambda x: int(x), code.split(',')))

def parse_program(program):
    for i in range(0, len(program), 4):
        if program[i] == 1: op = lambda x, y: x + y
        elif program[i] == 2: op = lambda x, y: x * y
        else: break
        program[program[i+3]] = op(program[program[i+1]], program[program[i+2]])
    return program

with open('./input.txt') as f:
    program = load_program(f.read())

    # Part 1
    program[1] = 12
    program[2] = 2
    print(parse_program(list(program))[0])

    #Part 2
    for i in range(100):
        for j in range(100):
            program[1] = i
            program[2] = j
            if parse_program(list(program))[0] == 19690720:
                print(100*i+j)
                break


