from collections import defaultdict
from typing import Dict, List


# map of stone number to map of blink score per iteration for that stone number
memo: Dict[int, Dict[int, int]] = defaultdict(dict)

def blink_stone(stone: int, steps: int) -> int:
    if steps in memo[stone]:
        return memo[stone][steps]

    if steps == 0:
        return 1

    result = 0

    if stone == 0:
        result += blink_stone(1, steps - 1)
    else:
        l = len(str(stone))
        if l % 2 == 0:
            half_len = l // 2
            divisor = 10 ** half_len
            result += blink_stone(stone // divisor, steps - 1)
            result += blink_stone(stone % divisor, steps - 1)
        else:
            result += blink_stone(stone * 2024, steps - 1)

    memo[stone][steps] = result

    return result


def process(input: str, blinks=25):
    stones = [blink_stone(int(n), blinks) for n in input.split()]
    return sum(stones)


example_stones = "125 17"


def example():
    assert process(example_stones, 25) == 55312


if __name__ == "__main__":
    example()

    with open("2024/11.input", "r") as f:
        stones = f.read()

    print(process(stones, 25))
    print(process(stones, 75))
