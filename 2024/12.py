from collections import defaultdict
from copy import deepcopy
from itertools import groupby
from typing import List, Tuple


Map = List[List[str]]
Painted = List[List[bool]]
Edges = List[Tuple[int, int]]


def parse_map(s: str) -> Map:
    return [[c for c in l] for l in s.strip().splitlines()]


def get_neighbors(x: int, y: int, map: Map):
    h = len(map)
    w = len(map[0])
    current = map[y][x]
    # Edges are set at .25 offsets so that in the following shape,
    # the inner left edge and inner right edge at O have distinct x values:
    # aaa
    # aOa
    # aaa
    candidates = [
        (x - 1, y, x - 0.25, y),
        (x + 1, y, x + 0.25, y),
        (x, y - 1, x, y - 0.25),
        (x, y + 1, x, y + 0.25)
    ]
    neighbors = []
    edges = []
    for xx, yy, ex, ey in candidates:
        if xx < 0 or xx >= w or yy < 0 or yy >= h:
            edges.append((ex, ey))
            continue
        if map[yy][xx] == current:
            neighbors.append((xx, yy))
        else:
            edges.append((ex, ey))
    return neighbors, edges



def paint(x: int, y: int, map: Map, painted: Painted) -> Tuple[int, int, Edges]:
    painted[y][x] = True

    neighbors, edges = get_neighbors(x, y, map)
    area = 1
    perimeter = 4 - len(neighbors)
    for xx, yy in neighbors:
        if painted[yy][xx]:
            continue
        new_area, new_perimeter, new_edges = paint(xx, yy, map, painted)
        area += new_area
        perimeter += new_perimeter
        edges += new_edges

    return area, perimeter, edges


def count_sides(edges: List[Tuple[int, int]]) -> int:
    # a. Count all sets of coords that have same x, and y are all within 1 of each other
    #   1. Group by x, keep only y, sort, count sequential subsequences
    #   2. Same with y
    # b. Same with x and y flipped
    # When grouping, only keep values that are offset by .25, which is the common denominator
    # between adjacent points on the same edge
    grouped_by_x = defaultdict(list)
    grouped_by_y = defaultdict(list)
    sides = 0
    for x, y in edges:
        if int(x) != x:
            grouped_by_x[x].append(y)
        if int(y) != y:
            grouped_by_y[y].append(x)
    for d in [grouped_by_x, grouped_by_y]:
        for n in d:
            sides += 1
            l = list(sorted(d[n]))
            for i in range(1, len(l)):
                if l[i] - l[i - 1] > 1:
                    sides += 1

    return sides


def debug(map: Map, painted: Painted):
    h = len(map)
    w = len(map[0])
    for y in range(h):
        l = ""
        for x in range(w):
            l += "#" if painted[y][x] else map[y][x]
        print(l)


def cost(input: str, bulk=False) -> int:
    map = parse_map(input)
    total = 0
    painted = [[False for _ in l] for l in map]
    # debug(map, painted)
    for y in range(len(map)):
        for x in range(len(map[0])):
            if not painted[y][x]:
                area, perimeter, edges = paint(x, y, map, painted)
                # print(f"Adding area {area} * perimeter {perimeter} = {area * perimeter}")
                # debug(map, painted)
                if bulk:
                    total += area * count_sides(edges)
                else:
                    total += area * perimeter
    return total


example_map = """
AAAA
BBCD
BBCC
EEEC
"""

example_map_2 = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

example_map_3 = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

example_map_4 = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""

example_map_5 = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""


def example():
    assert cost(example_map) == 140
    assert cost(example_map_2) == 772
    assert cost(example_map_3) == 1930

    assert cost(example_map, bulk=True) == 80
    assert cost(example_map_4, bulk=True) == 236
    assert cost(example_map_5, bulk=True) == 368
    assert cost(example_map_3, bulk=True) == 1206


if __name__ == "__main__":
    example()

    with open("2024/12.input", "r") as f:
        map = f.read()

    print(cost(map))
    print(cost(map, bulk=True))
