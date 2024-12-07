from functools import reduce
from itertools import product
from operator import add, mul
from typing import List, Tuple


def concat_num(a: int, b: int) -> int:
    return int(f"{a}{b}")


operators = [add, mul]
operators_v2 = operators + [concat_num]


def parse_equations(input: str) -> List[Tuple[int, List[int]]]:
    lines = [l.split(": ") for l in input.strip().splitlines()]
    return [(int(l[0]), [int(i) for i in l[1].split()]) for l in lines]


def process_equations(input: str, operators=operators) -> int:
    eqs = parse_equations(input)
    total = 0
    for result, operands in eqs:
        operations = product(operators, repeat=len(operands) - 1)
        for ops in operations:
            iops = iter(ops)
            # Could break out of current calculation earlier if actual alredy exceeds
            # expected result before calculation is over if we did it manually in a for loop
            actual = reduce(lambda a, b: next(iops)(a, b), operands)
            if actual == result:
                # print(result, list(chain(*zip_longest(operands, ops))))
                total += result
                break
    return total


example_equations = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def example():
    assert process_equations(example_equations) == 3749
    assert process_equations(example_equations, operators=operators_v2) == 11387


if __name__ == "__main__":
    example()

    with open("2024/07.input", "r") as f:
        equations = f.read()

    print(process_equations(equations))
    print(process_equations(equations, operators=operators_v2))
