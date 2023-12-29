from intcode import IntcodeVm

program = open('inputs/day25.txt').read()

for s in IntcodeVm(program).run(IntcodeVm.stdin_ascii()):
    print(chr(s), end='')
