from typing import List, Tuple


def parse_towels(s: str) -> Tuple[List[str], List[str]]:
    raw_patterns, raw_designs = s.strip().split("\n\n")
    patterns = raw_patterns.split(", ")
    designs = raw_designs.splitlines()
    return patterns, designs


def is_possible(design: str, patterns: List[str], memo=None):
    if memo is None:
        memo = {}

    if design == "":
        return 1

    if design in memo:
        return memo[design]

    possible = 0
    for p in patterns:
        if design.startswith(p):
            possible += is_possible(design[len(p):], patterns, memo)

    memo[design] = possible
    return possible


def process(s):
    patterns, designs = parse_towels(s)
    part1 = 0
    part2 = 0
    for d in designs:
        possible = is_possible(d, patterns)
        if possible > 0:
            part1 += 1
            part2 += possible

    return part1, part2


example_towels = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def example():
    part1, part2 = process(example_towels)
    assert part1 == 6
    assert part2 == 16


if __name__ == "__main__":
    example()

    with open("2024/19.input", "r") as f:
        towels = f.read()

    part1, part2 = process(towels)
    print(part1)
    print(part2)
