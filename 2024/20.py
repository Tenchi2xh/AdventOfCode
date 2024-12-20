from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Union
import heapq


Maze = List[List[str]]


# From 16.py
@dataclass(frozen=True)
class Vec2:
    x: int
    y: int

    def inverse(self):
        return Vec2(-self.x, -self.y)

    def __add__(self, other: "Vec2"):
        return Vec2(self.x + other.x, self.y + other.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def manhattan(self, other: "Vec2"):
        return abs(other.x - self.x) + abs(other.y - self.y)

all_directions = [
    Vec2(0, -1),
    Vec2(0, 1),
    Vec2(-1, 0),
    Vec2(1, 0),
]


# From 16.py
def parse_maze(s: str) -> Tuple[Maze, Vec2, Vec2]:
    lines = []
    start = None
    end = None
    for y, l in enumerate(s.strip().splitlines()):
        l = [c for c in l]
        lines.append(l)
        if "S" in l:
            start = Vec2(x=l.index("S"), y=y)
        elif "E" in l:
            end = Vec2(x=l.index("E"), y=y)

    return lines, start, end


def debug_print(scores: List[List[Union[None, int]]]):
    print("---")
    for l in scores:
        ll = ""
        for c in l:
            if c is None:
                ll += "  #  "
            else:
                ll += f"{c:^5d}"
        print(ll)


def count_shortcuts(s: str):
    maze, start, end = parse_maze(s)
    scores = [[None if c == "#" else -1 for c in l] for l in maze]
    pos = start
    score = 0
    scores[pos.y][pos.x] = score
    path = [start]

    # There is only one path possible
    # Flood fill until the end, and mark the distance at each step
    while pos != end:
        for dir in all_directions:
            next_pos = pos + dir
            if scores[next_pos.y][next_pos.x] == -1:
                pos = next_pos
                path.append(pos)
                break
        score += 1
        scores[pos.y][pos.x] = score

    # debug_print(scores)

    simple_shortcuts = 0
    long_shortcuts = 0

    # Navigate through the whole path again
    # For each position i, check the manhattan distance to any next position j in the path
    # If the manhattan distance is smaller than j - a, it's a cheat
    ll = len(path)
    for i in range(ll):
        for j in range(i + 102, ll):
            manhattan = path[i].manhattan(path[j])
            dist = j - i
            # We're only interested in savings of 100 or more
            if dist - manhattan < 100:
                continue

            if manhattan == 2:
                simple_shortcuts += 1
            if manhattan <= 20:
                long_shortcuts += 1

    return simple_shortcuts, long_shortcuts


example_racetrack = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


if __name__ == "__main__":

    with open("2024/20.input", "r") as f:
        racetrack = f.read()

    part1, part2 = count_shortcuts(racetrack)
    print(part1)
    print(part2)
