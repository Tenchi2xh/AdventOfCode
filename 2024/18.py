from dataclasses import dataclass
import heapq
from typing import Dict, List, Tuple
from bisect import bisect_left


@dataclass(frozen=True)
class Vec2:
    x: int
    y: int

    def __add__(self, other: "Vec2"):
        return Vec2(self.x + other.x, self.y + other.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)


all_directions = [
    Vec2(0, -1),
    Vec2(0, 1),
    Vec2(-1, 0),
    Vec2(1, 0),
]


def parse_bytes(s: str):
    return [[int(n) for n in l.split(",")] for l in s.strip().splitlines()]


def debug_print(memory):
    for l in memory:
        print("".join(l))


def get_valid_directions(memory, p: Vec2, size: Vec2):
    w, h = size.x, size.y
    x, y = p.x, p.y

    directions = []

    for dd in all_directions:
        xx, yy = x + dd.x, y + dd.y
        if xx < 0 or xx >= w or yy < 0 or yy >= h:
            continue
        if memory[yy][xx] == "#":
            continue
        directions.append(dd)

    return directions


def dijkstra(memory, start: Vec2, end: Vec2):
    size = Vec2(len(memory[0]), len(memory))

    visited: Dict[Vec2] = {}

    priority_queue: List[Tuple[int, Vec2]] = []
    heapq.heappush(priority_queue, (0, start))

    while priority_queue:
        score, cur_pos = heapq.heappop(priority_queue)

        if cur_pos in visited and visited[cur_pos] <= score:
            continue

        visited[(cur_pos)] = score

        if cur_pos == end:
            return score

        for new_dir in get_valid_directions(memory, cur_pos, size):
            new_score = score + 1
            new_pos = cur_pos + new_dir

            heapq.heappush(priority_queue, (new_score, new_pos))

    return float("inf")


def process(s: str, nanoseconds, w=71):
    bytes = parse_bytes(s)
    start, end = Vec2(0, 0), Vec2(w - 1, w - 1)

    def fill(nanoseconds):
        memory = [["." for _ in range(w)] for _ in range(w)]
        for x, y in bytes[:nanoseconds]:
            memory[y][x] = "#"
        return memory

    part1 = dijkstra(fill(nanoseconds), start, end)

    # binary search
    left, right = nanoseconds, 1_000_000_000
    while left < right:
        mid = (left + right) // 2
        if dijkstra(fill(mid), start, end) != float("inf"):
            left = mid + 1
        else:
            right = mid

    part2 = ",".join(str(n) for n in bytes[left - 1])

    return part1, part2


example_bytes = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


def example():
    part1, part2 = process(example_bytes, nanoseconds=12, w=7)
    assert part1 == 22
    assert part2 == "6,1"


if __name__ == "__main__":
    example()

    with open("2024/18.input", "r") as f:
        bytes = f.read()

    part1, part2 = process(bytes, nanoseconds=1024, w=71)
    print(part1)
    print(part2)
