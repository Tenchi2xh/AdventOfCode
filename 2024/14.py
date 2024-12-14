from dataclasses import dataclass
from functools import reduce
from operator import mul
import time
from typing import List


@dataclass
class Vec2:
    x: int
    y: int


@dataclass
class Robot:
    p: Vec2
    v: Vec2


def parse_robots(s: str):
    def parse_robot(r: str):
        parts = r.split(" ")
        return Robot(
            p=Vec2(*[int(p) for p in parts[0].split("p=")[1].split(",")]),
            v=Vec2(*[int(p) for p in parts[1].split("v=")[1].split(",")]),
        )

    robots = [parse_robot(l) for l in s.strip().splitlines()]
    return robots


def debug_print(robots: List[Robot], w: int, h: int):
    for y in range(h):
        l = ""
        for x in range(w):
            rs = 0
            for r in robots:
                if r.p.x == x and r.p.y == y:
                    rs += 1
            l += "." if rs == 0 else str(rs)
        print(l)


def simulate_floor(input: str, w=101, h=103, max=100, slow=False) -> int:
    robots = parse_robots(input)

    for i in range(max):
        for r in robots:
            r.p.x = (r.p.x + r.v.x) % w
            r.p.y = (r.p.y + r.v.y) % h

        if slow:
            positions = set()
            for r2 in robots:
                positions.add((r2.p.x, r2.p.y))
            if len(positions) != len(robots):
                continue
            print(i + 1)
            debug_print(robots, w, h)
            time.sleep(1)


    quadrants = [0, 0, 0, 0]
    hw = w // 2
    hh = h // 2

    for r in robots:
        x, y = r.p.x, r.p.y
        if x == hw or y == hh:
            continue

        quadrant_index = ((y < hh) << 1) | (x < hw)
        quadrants[quadrant_index] += 1

    return reduce(mul, quadrants)


example_robots = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


def example():
    assert simulate_floor(example_robots, w=11, h=7) == 12


if __name__ == "__main__":
    example()

    with open("2024/14.input", "r") as f:
        robots = f.read()

    print(simulate_floor(robots))
    simulate_floor(robots, max=10000, slow=True)
