from typing import List


def parse_reports(s: str) -> List[List[int]]:
    return [[int(n) for n in l.split()] for l in s.strip().splitlines()]


def is_safe(r: List[int]) -> bool:
    pairs = [(r[i], r[i + 1]) for i in range(len(r) - 1)]
    offsets = [a - b for a, b in pairs]

    if all(o > 0 for o in offsets) or all(o < 0 for o in offsets):
        if all(abs(o) <= 3 for o in offsets):
            return True

    return False


def is_safe_dampened(r: List[int]) -> bool:
    if is_safe(r):
        return True

    for i in range(len(r)):
        if is_safe(r[:i] + r[i + 1:]):
            return True

    return False


example_reports = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def example():
    reports = parse_reports(example_reports)
    assert sum(is_safe(r) for r in reports) == 2
    assert sum(is_safe_dampened(r) for r in reports) == 4


if __name__ == "__main__":
    example()

    with open("02.input", "r") as f:
        reports = parse_reports(f.read())
    print(sum(is_safe(r) for r in reports))
    print(sum(is_safe_dampened(r) for r in reports))
