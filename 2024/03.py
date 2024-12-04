import re


instruction = r"(mul)\((\d{1,3}),(\d{1,3})\)"
instruction_v2 = instruction + r"|(do)\(\)|(don't)\(\)"


def read_memory(input: str):
    for match in re.finditer(instruction, input):
        yield int(match.group(2)), int(match.group(3))


def read_memory_v2(input: str):
    do_yield = True
    for match in re.finditer(instruction_v2, input):
        if match.group(4):
            do_yield = True
        elif match.group(5):
            do_yield = False
        elif do_yield:
            yield int(match.group(2)), int(match.group(3))


example_memory0 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
example_memory1 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def example():
    assert sum(a * b for a, b in read_memory(example_memory0)) == 161
    assert sum(a * b for a, b in read_memory_v2(example_memory1)) == 48


if __name__ == "__main__":
    example()

    with open("2024/03.input", "r") as f:
        memory = f.read()

    print(sum(a * b for a, b in read_memory(memory)))
    print(sum(a * b for a, b in read_memory_v2(memory)))