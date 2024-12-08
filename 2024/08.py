from collections import defaultdict
from itertools import combinations
from typing import List, Set, Tuple


def count_antinodes(map: str, resonnant=False) -> int:
    lines = map.strip().splitlines()
    h = len(lines)
    w = len(lines[0])

    antennas_by_type: defaultdict[str, List[Tuple[int, int]]] = defaultdict(list)

    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c != ".":
                antennas_by_type[c].append((x, y))

    antinodes: List[Tuple[int, int]] = set()

    for antenna_type in antennas_by_type.keys():
        antennas = antennas_by_type[antenna_type]
        pairs = combinations(antennas, 2)

        for a, b in pairs:
            dx, dy = b[0] - a[0], b[1] - a[1]

            i = 1
            x0, y0 = a[0] - dx, a[1] - dy
            while x0 >= 0 and x0 < w and y0 >= 0 and y0 < h:
                if resonnant or i == 1:
                    antinodes.add((x0, y0))
                i += 1
                x0, y0 = a[0] - i * dx, a[1] - i * dy

            j = 1
            x1, y1 = b[0] + dx, b[1] + dy
            while x1 >= 0 and x1 < w and y1 >= 0 and y1 < h:
                if resonnant or j == 1:
                    antinodes.add((x1, y1))
                j += 1
                x1, y1 = b[0] + j * dx, b[1] + j * dy

            if resonnant:
                antinodes.add(a)
                antinodes.add(b)

    # for y, l in enumerate(lines):
    #     s = "".join([
    #         "#" if (x, y) in antinodes and c == "." else c
    #         for x, c in enumerate(l)
    #     ])
    #     print(s)

    return len(antinodes)


example_map = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


def example():
    assert count_antinodes(example_map) == 14
    assert count_antinodes(example_map, resonnant=True) == 34


if __name__ == "__main__":
    example()

    with open("2024/08.input", "r") as f:
        map = f.read()

    print(count_antinodes(map))
    print(count_antinodes(map, resonnant=True))
