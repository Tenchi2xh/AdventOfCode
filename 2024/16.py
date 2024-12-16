from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple
import heapq


Maze = List[List[str]]


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


all_directions = [
    Vec2(0, -1),
    Vec2(0, 1),
    Vec2(-1, 0),
    Vec2(1, 0),
]


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


def get_valid_directions(maze: Maze, p: Vec2, d: Vec2, size: Vec2):
    w, h = size.x, size.y
    x, y = p.x, p.y

    directions = []
    candidates = [dd for dd in all_directions if dd != d.inverse()]

    for dd in candidates:
        xx, yy = x + dd.x, y + dd.y
        if xx < 0 or xx >= w or yy < 0 or yy >= h:
            continue
        if maze[yy][xx] == "#":
            continue
        directions.append(dd)

    return directions


def navigate_dijkstra(maze: Maze, start: Vec2, end: Vec2):
    size = Vec2(len(maze[0]), len(maze))

    visited: Dict[Vec2, int] = {}
    lowest_seats: Set[Vec2] = set()
    min_score = float("inf")

    priority_queue: List[Tuple[int, Vec2, Vec2, List[Vec2]]] = []
    heapq.heappush(priority_queue, (0, start, Vec2(1, 0), [start]))

    while priority_queue:
        score, cur_pos, cur_dir, path = heapq.heappop(priority_queue)

        if score > min_score:
            break

        if cur_pos == end:
            if score < min_score:
                lowest_seats.clear()
                min_score = score
            lowest_seats |= set(path)

        visited[(cur_pos, cur_dir)] = score

        for new_dir in get_valid_directions(maze, cur_pos, cur_dir, size):
            new_score = score + (1001 if new_dir != cur_dir else 1)
            new_pos = cur_pos + new_dir

            if new_score < visited.get((new_pos, new_dir), float("inf")):
                heapq.heappush(priority_queue, (new_score, new_pos, new_dir, path + [new_pos]))

    return min_score, len(lowest_seats)


def lowest_score(s: str):
    maze, start, end = parse_maze(s)
    score, unique_seats = navigate_dijkstra(maze, start, end)
    return score, unique_seats


example_maze = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

example_maze2 = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

def example():
    score1, seats1 = lowest_score(example_maze)
    score2, seats2 = lowest_score(example_maze2)
    assert score1 == 7036
    assert score2 == 11048
    assert seats1 == 45
    assert seats2 == 64


if __name__ == "__main__":
    example()

    with open("2024/16.input", "r") as f:
        maze = f.read()

    score, best_seats = lowest_score(maze)
    print(score)
    print(best_seats)
