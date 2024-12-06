from typing import Set, Tuple


directions_map = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}

directions = list(directions_map.values())


def debug_print(lines, x, y):
    print("---")
    for i, l in enumerate(lines):
        ll = [c for c in l]
        if i == y:
            ll[x] = "x"
        print("".join(ll))


def turn_right(direction: Tuple[int, int]):
    i = directions.index(direction)
    return directions[(i + 1) % 4]


def navigate_map(map: str, detect_loops=False):
    lines = map.strip().splitlines()
    lines = [list(l) for l in lines]

    h = len(lines)
    w = len(lines[0])
    y = next(y for y in range(len(lines)) if list(filter(lambda c: c not in (".", "#"), lines[y])))
    x = next(x for x in range(len(lines[y])) if lines[y][x] not in (".", "#"))

    direction = directions_map[lines[y][x]]
    lines[y][x] = "."

    stepped: Set[Tuple[int, int]] = set([(x, y)])
    previous_states: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set()
    while True:
        # debug_print(lines, x, y)

        state = ((x, y), direction)
        if state in previous_states and detect_loops:
            return None
        previous_states.add(state)

        x1, y1 = x + direction[0], y + direction[1]
        if x1 < 0 or x1 >= w or y1 < 0 or y1 >= h:
            break
        elif lines[y1][x1] == "#":
            direction = turn_right(direction)
        else:
            x, y = x1, y1
            stepped.add((x, y))

    return stepped


def find_loops(map: str):
    lines = map.strip().splitlines()
    stepped = navigate_map(map)
    loops = 0

    for x, y in stepped:
        if lines[y][x] != ".":
            continue

        new_lines = [list(l) for l in lines]
        new_lines[y][x] = "#"

        result = navigate_map("\n".join("".join(l) for l in new_lines), detect_loops=True)
        if result is None:
            loops += 1

    return loops


example_map = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


def example():
    assert len(navigate_map(example_map)) == 41
    assert find_loops(example_map) == 6


if __name__ == "__main__":
    example()

    with open("2024/06.input", "r") as f:
        map = f.read()

    print(len(navigate_map(map)))
    print(find_loops(map))
