from typing import List, Tuple


Key = Tuple[int, int, int, int, int]
Lock = Key


def parse_schematics(s: str):
    parts = [p.splitlines() for p in s.strip().split("\n\n")]

    locks: List[Lock] = []
    keys: List[Key] = []

    for p in parts:
        is_lock = p[0][0] == "#"
        if not is_lock:
            p = p[::-1]

        component = [0] * 5

        for l in p[1:]:
            for j, c in enumerate(l):
                if c == "#":
                    component[j] += 1

        # print("lock" if is_lock else "key", tuple(component))

        (locks if is_lock else keys).append(tuple(component))

    return locks, keys


def fit(lock: Lock, key: Key):
    for i in range(5):
        if lock[i] + key[i] > 5:
            return False
    return True


def count_fitting_keys(s: str):
    locks, keys = parse_schematics(s)

    fitting = 0
    for lock in locks:
        for key in keys:
            if fit(lock, key):
                fitting += 1

    return fitting


example_schematics = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""


def example():
    assert count_fitting_keys(example_schematics) == 3


if __name__ == "__main__":
    example()

    with open("2024/25.input", "r") as f:
        schematics = f.read()

    print(count_fitting_keys(schematics))
