from typing import List, Set, Tuple

Map = List[List[int]]
Visited = List[List[bool]]
UniqueCoords = Set[Tuple[int, int]]


def parse_map(s: str) -> Map:
    return [[int(c) for c in l] for l in s.strip().splitlines()]


def get_valid_neighbors(map, x, y, visited):
    h = len(map)
    w = len(map[0])
    current = map[y][x]
    candidates = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    neighbors = []
    for xx, yy in candidates:
        if xx < 0 or xx >= w or yy < 0 or yy >= h:
            continue
        if visited[yy][xx]:
            continue
        if map[yy][xx] - current == 1:
            neighbors.append((xx, yy))
    return neighbors


def trail_score_dfs(map: Map, x: int, y: int, visited: Visited=None) -> Tuple[UniqueCoords, int]:
    if map[y][x] == 9:
        return {(x, y)}, 1

    h = len(map)
    w = len(map[0])
    tops = set()
    score = 0

    if visited is None:
        visited = [[False for _ in range(w)] for _ in range(h)]

    valid_neighbors = get_valid_neighbors(map, x, y, visited)

    for xx, yy in valid_neighbors:
        visited = [[v for v in l] for l in visited]
        visited[y][x] = True
        new_tops, new_score = trail_score_dfs(map, xx, yy, visited)
        tops |= new_tops
        score += new_score

    return tops, score


def process(s: str):
    map = parse_map(s)
    total_score = 0
    total_score_distinct = 0
    for y, l in enumerate(map):
        for x, n in enumerate(l):
            if n == 0:
                tops, score = trail_score_dfs(map, x, y)
                # print(x, y, tops)
                total_score += len(tops)
                total_score_distinct += score

    return total_score, total_score_distinct


example_map = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


def example():
    a, b = process(example_map)
    assert a == 36
    assert b == 81


if __name__ == "__main__":
    example()

    with open("2024/10.input", "r") as f:
        map = f.read()

    a, b = process(map)
    print(a)
    print(b)
