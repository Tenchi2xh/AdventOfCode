from typing import List, Tuple
from collections import Counter


def parse_lists(s: str) -> Tuple[List[int], List[int]]:
    raw_pairs = [t.split() for t in s.strip().splitlines()]
    int_pairs = [[int(a), int(b)] for a, b in raw_pairs]
    return zip(*int_pairs)


def distance(l0: List[int], l1: List[int]) -> int:
    pairs = zip(sorted(l0), sorted(l1))
    distances = [abs(a - b) for a, b in pairs]
    return sum(distances)


def similarity(l0: List[int], l1: List[int]) -> int:
    l1_counts = Counter(l1)
    return sum(a * l1_counts[a] for a in l0)


example_lists = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


def example():
    l0, l1 = parse_lists(example_lists)
    assert distance(l0, l1) == 11
    assert similarity(l0, l1) == 31


if __name__ == "__main__":
    example()

    with open("2024/01.input", "r") as f:
        l0, l1 = parse_lists(f.read())

    print(distance(l0, l1))
    print(similarity(l0, l1))
