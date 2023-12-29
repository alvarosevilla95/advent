from intcode import IntcodeVm

program = open('inputs/day21.txt').read()

p1_script = """
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
""".strip()

p2_script = """
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT H T
NOT T T
OR E T
AND T J
RUN
""".strip()

stdin = lambda script: map(ord, script+"\n")

for script in p1_script, p2_script:
    for s in IntcodeVm(program).run(stdin(script)):
        print(chr(s) if s < 256 else s, end='')
    print("\n\n")
