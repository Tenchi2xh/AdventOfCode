from dataclasses import dataclass
from typing import Tuple

@dataclass
class Coords:
    x: int
    y: int


@dataclass
class Machine:
    a: Coords
    b: Coords
    p: Coords


def parse_machines(s: str, increase=False):
    i = 10000000000000 if increase else 0
    def parse_machine(m: str):
        lines = m.splitlines()
        return Machine(
            a=Coords(*[int(l.split("+")[1]) for l in lines[0].split(",")]),
            b=Coords(*[int(l.split("+")[1]) for l in lines[1].split(",")]),
            p=Coords(*[int(l.split("=")[1]) + i for l in lines[2].split(",")]),
        )

    machines = [parse_machine(l) for l in s.strip().split("\n\n")]
    return machines


# Na: number of A presses
# Nb: number of B presses
#
# 1. Na * Ax + Nb * Bx = Px
# 2. Na * Ay + Nb * By = Py
#
# (Solve)
#
# Na = (ByPx - BxPy) / (AxBy - AyBx)
# Nb = (AxPy - AyPx) / (AxBy - AyBx)


def process_machines(s: str, increase=False) -> int:
    machines = parse_machines(s, increase)
    tokens = 0

    for m in machines:
        # Na = (ByPx - BxPy) / (AxBy - AyBx)
        # Nb = (AxPy - AyPx) / (AxBy - AyBx)
        denom = m.a.x * m.b.y - m.a.y * m.b.x
        if denom == 0:
            continue
        Na_num = m.b.y * m.p.x - m.b.x * m.p.y
        Nb_num = m.a.x * m.p.y - m.a.y * m.p.x
        Na = Na_num / denom
        Nb = Nb_num / denom
        if Na % 1 != 0 or Nb % 1 != 0 or Na < 0 or Nb < 0:
            continue
        if not increase:
            if Na > 100 or Nb > 100:
                continue

        tokens += Na * 3 + Nb
    return int(tokens)


example_machines = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


def example():
    assert process_machines(example_machines) == 480



if __name__ == "__main__":
    example()

    with open("2024/13.input", "r") as f:
        machines = f.read()

    print(process_machines(machines))
    print(process_machines(machines, increase=True))
