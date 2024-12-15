from typing import Callable, List, Tuple


Map = List[List[str]]


cardinals: Callable[[str, int, int], Tuple[int, int]] = lambda d, x, y: {
    "^": (x, y - 1),
    "v": (x, y + 1),
    "<": (x - 1, y),
    ">": (x + 1, y),
}[d]


def widen(s: str):
    return s.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")


def parse_input(s: str, wide=False) -> Tuple[Map, List[str]]:
    raw_map, raw_inputs = s.strip().split("\n\n")
    if wide:
        raw_map = widen(raw_map)

    map = [[c for c in l] for l in raw_map.strip().splitlines()]
    directions = [c for c in "".join(raw_inputs.splitlines())]

    return map, directions


def push(map: Map, d: str, w: int, h: int, x: int, y: int):
    boxes = []
    blocked = False
    pushing = True
    cx, cy = x, y
    while pushing:
        nx, ny = cardinals(d, cx, cy)
        match map[ny][nx]:
            case ".":
                pushing = False
            case "#":
                pushing = False
                blocked = True
            case "O":
                boxes.append((nx, ny))
        cx, cy = nx, ny

    if not blocked:
        for bx, by in boxes:
            nbx, nby = cardinals(d, bx, by)
            map[nby][nbx] = "O"
        nx, ny = cardinals(d, x, y)
        map[ny][nx] = "@"
        map[y][x] = "."
        return nx, ny
    return x, y


def push_wide(map: Map, d: str, w: int, h: int, x: int, y: int):
    boxes_l = []
    boxes_r = []

    blocked = False
    stack = [(x, y)]
    done = set()

    while True:
        if len(stack) == 0:
            break

        cx, cy = stack.pop(0)
        nx, ny = cardinals(d, cx, cy)

        match map[ny][nx]:
            case ".":
                pass
            case "#":
                blocked = True
                break
            case "[":
                boxes_l.append((nx, ny))
                boxes_r.append((nx + 1, ny))
                if (nx, ny) not in done:
                    stack.append((nx, ny))
                    done.add((nx, ny))
                if (nx + 1, ny) not in done:
                    stack.append((nx + 1, ny))
                    done.add((nx + 1, ny))
            case "]":
                boxes_l.append((nx - 1, ny))
                boxes_r.append((nx, ny))
                if (nx, ny) not in done:
                    stack.append((nx, ny))
                    done.add((nx, ny))
                if (nx - 1, ny) not in done:
                    stack.append((nx - 1, ny))
                    done.add((nx - 1, ny))

    if not blocked:
        for bx, by in boxes_l + boxes_r:
            map[by][bx] = "."

        for bx, by in boxes_l:
            nbx, nby = cardinals(d, bx, by)
            map[nby][nbx] = "["
            map[nby][nbx + 1] = "]"

        nx, ny = cardinals(d, x, y)
        map[ny][nx] = "@"
        map[y][x] = "."

        return nx, ny
    return x, y



def debug_print(map: Map):
    for l in map:
        print("".join(l))
    print()


def process(s: str, wide=False, debug=False):
    map, directions = parse_input(s, wide=wide)

    h = len(map)
    w = len(map[0])
    y = next(i for i in range(h) if "@" in map[i])
    x = next(i for i in range(w) if map[y][i] == "@")

    if debug:
        print("Initial state:")
        debug_print(map)

    p = push_wide if wide else push

    for d in directions:
        x, y = p(map, d=d, w=w, h=h, x=x, y=y)
        if debug:
            print("Move " + d + ":")
            debug_print(map)

    total_gps = 0
    for y, l in enumerate(map):
        for x, c in enumerate(l):
            if c not in ["O", "["]:
                continue
            total_gps += 100 * y + x
    return total_gps


example_input = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""

example_input2 = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""


def example():
    assert process(example_input) == 2028
    assert process(example_input2) == 10092
    assert process(example_input2, wide=True) == 9021


if __name__ == "__main__":
    example()

    with open("2024/15.input", "r") as f:
        input = f.read()

    print(process(input))
    print(process(input, wide=True))
