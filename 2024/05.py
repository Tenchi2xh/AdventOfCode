from typing import List, Tuple


def parse_input(input: str) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    part0, part1 = input.strip().split("\n\n")

    ordering_pairs = [tuple([int(n) for n in l.split("|")]) for l in part0.splitlines()]
    page_numbers = [[int(n) for n in l.split(",")] for l in part1.splitlines()]

    return ordering_pairs, page_numbers


def is_correct_order(pns: List[List[int]], ordering_pairs: List[Tuple[int, int]], flip=False):
    for a, b in ordering_pairs:
        if a in pns and b in pns and pns.index(a) > pns.index(b):
            if flip:
                pns[pns.index(a)], pns[pns.index(b)] = pns[pns.index(b)], pns[pns.index(a)]
            return False
    return True


def process_input(input: str):
    ordering_pairs, page_numbers = parse_input(input)
    result = 0

    for pns in page_numbers:
        if is_correct_order(pns, ordering_pairs):
            result += pns[(len(pns) - 1) // 2]

    return result


def process_input_incorrect(input: str):
    ordering_pairs, page_numbers = parse_input(input)
    result = 0

    for pns in page_numbers:
        if is_correct_order(pns, ordering_pairs, flip=True):
            continue

        while not is_correct_order(pns, ordering_pairs, flip=True):
            pass
        result += pns[(len(pns) - 1) // 2]

    return result


example_input = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

def example():
    assert process_input(example_input) == 143
    assert process_input_incorrect(example_input) == 123


if __name__ == "__main__":
    example()

    with open("2024/05.input", "r") as f:
        input = f.read()

    print(process_input(input))
    print(process_input_incorrect(input))
