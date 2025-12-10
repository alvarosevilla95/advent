import re
import numpy as np
from scipy.optimize import linprog

data = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".strip()

data = open('inputs/day10.txt').read()

def parse(line: str):
    match = re.match(r'\[(.+?)\](.*)\{(.+)\}', line)
    indicator, button_str, joltage_str = match.groups() # pyright: ignore[reportOptionalMemberAccess]
    target: tuple[bool, ...] = tuple(c == '#' for c in indicator)
    buttons: list[tuple[int, ...]] = [tuple(map(int, b[1:-1].split(','))) for b in button_str.split()]
    joltage: list[int] = list(map(int, joltage_str.split(',')))
    return target, buttons, joltage

parsed = list(map(parse, data.splitlines()))

def toggle(state: tuple[bool, ...], button: tuple[int, ...]) -> tuple[bool, ...]:
    return tuple(not s if i in button else s for i, s in enumerate(state))

def solve(target: tuple[bool, ...], buttons: list[tuple[int, ...]]) -> int:
    def search(state: tuple[bool, ...], remaining: list[tuple[int, ...]]) -> int:
        if state == target: return 0
        if not remaining: return 999
        button, *rest = remaining
        return min(search(state, rest), 1 + search(toggle(state, button), rest))
    return search((False,) * len(target), buttons)

print(sum(solve(target, buttons) for target, buttons, _ in parsed))

def solve2(target: list[int], buttons: list[tuple[int, ...]]) -> int:
    A = np.array([[1 if i in b else 0 for b in buttons] for i in range(len(target))])
    result = linprog(np.ones(len(buttons)), A_eq=A, b_eq=target, integrality=1)
    return int(result.fun) if result.success else 999

print(sum(solve2(target, buttons) for _, buttons, target in parsed))
