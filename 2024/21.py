from dataclasses import dataclass
from functools import cache
from itertools import permutations
from typing import Dict, List, Tuple, Union


Keypad = Union[Tuple[str, str, str, str], Tuple[str, str]]


@dataclass(frozen=True)
class Vec2:
    x: int
    y: int

    def __add__(self, other: "Vec2"):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2"):
        return Vec2(self.x - other.x, self.y - other.y)


door_keypad = (
    "789",
    "456",
    "123",
    " 0A"
)

robot_keypad = (
    " ^A",
    "<v>"
)

directions = {
    ">": Vec2( 1, 0),
    "<": Vec2(-1, 0),
    "v": Vec2(0,  1),
    "^": Vec2(0, -1),
}

positions: Dict[Keypad, Dict[str, Vec2]] = {
    door_keypad: {
        "7": Vec2(0, 0), "8": Vec2(1, 0), "9": Vec2(2, 0),
        "4": Vec2(0, 1), "5": Vec2(1, 1), "6": Vec2(2, 1),
        "1": Vec2(0, 2), "2": Vec2(1, 2), "3": Vec2(2, 2),
                         "0": Vec2(1, 3), "A": Vec2(2, 3),
    },
    robot_keypad: {
                         "^": Vec2(1, 0), "A": Vec2(2, 0),
        "<": Vec2(0, 1) ,"v": Vec2(1, 1), ">": Vec2(2, 1),
    }
}


forbidden = {
    robot_keypad: Vec2(0, 0),
    door_keypad: Vec2(0, 3),
}


@cache
def move_to_key(initial_key: str, target_key: str, target_keypad: Keypad) -> Vec2:
    pos0 = positions[target_keypad][initial_key]
    pos1 = positions[target_keypad][target_key]
    dpos = pos1 - pos0

    return dpos


@cache
def is_valid(perm: List[str], pos: Vec2, keypad: Keypad):
    for d in perm:
        pos = pos + directions[d]
        if pos == forbidden[keypad]:
            # print("invalid perm", perm, "forbidden", forbidden[keypad])
            return False

    # print("valid perm", perm, "forbidden", forbidden[keypad])
    return True


@cache
def find_min_movements(pos: Vec2, dpos: Vec2, depth: int, keypad: Keypad) -> int:
    y_inputs = ("^" if dpos.y < 0 else "v") * abs(dpos.y)
    x_inputs = ("<" if dpos.x < 0 else ">") * abs(dpos.x)
    arrows = y_inputs + x_inputs
    perms = set(permutations(arrows, len(arrows)))

    min_movements = float("inf")

    for perm in perms:
        if not is_valid(perm, pos, keypad):
            continue

        result = input_code("".join(perm) + "A", "A", robot_keypad, depth - 1)

        if min_movements is None or result < min_movements:
            min_movements = result

    return min_movements


@cache
def input_code(code: str, initial_key="A", target_keypad=door_keypad, depth=3) -> int:
    if depth == 0:
        return len(code)

    length = 0
    for key in code:
        # print("going from", initial_key, "to", key)
        dpos = move_to_key(initial_key, key, target_keypad)
        length += find_min_movements(positions[target_keypad][initial_key], dpos, depth, target_keypad)

        new_pos = positions[target_keypad][initial_key] + dpos
        initial_key = target_keypad[new_pos.y][new_pos.x]

    return length


def input_all_codes(codes: str, depth=3):
    codes = codes.strip().splitlines()
    complexity = 0
    for code in codes:
        result = input_code(code, depth=depth)
        numeric = int(code[:-1])
        complexity += result * numeric
        # print(result, "*", numeric)

    # print(complexity)
    return complexity


example_codes = """
029A
980A
179A
456A
379A
"""


def example():
    assert input_all_codes(example_codes, depth=3) == 126384


if __name__ == "__main__":
    example()

    with open("2024/21.input", "r") as f:
        codes = f.read()

    print(input_all_codes(codes, depth=3))
    print(input_all_codes(codes, depth=26))
