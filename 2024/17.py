from typing import List


def parse_program(s: str):
    raw_regs, raw_prog = s.strip().split("\n\n")
    registers = {
        left: int(right)
        for left, right
        in [l.split("Register ")[1].split(": ") for l in raw_regs.splitlines()]
    }
    program = [int(n) for n in raw_prog.split(": ")[1].split(",")]

    return registers, program


def jj(ns: List[int]):
    return ",".join(str(n) for n in ns)


def combo_operands(value, regs):
    if value == 7:
        raise ValueError("Value 7 not expected in a combo operand")
    return {
        0: (0, "0"),
        1: (1, "1"),
        2: (2, "2"),
        3: (3, "3"),
        4: (regs["A"], "A"),
        5: (regs["B"], "B"),
        6: (regs["C"], "C"),
    }[value]


def literal_operand(value):
    return value, str(value)


def execute_program(s: str, verbose=False, override_A=None):
    registers, program = parse_program(s)
    if override_A is not None:
        registers["A"] = override_A
    return run_cpu(registers, program, verbose)


def run_cpu(registers, program, verbose=False):
    ip = 0
    out = []

    def debug(ins, op):
        if verbose:
            print(f"{ip:>4d}: {ins} {op}".ljust(30) + str(registers))

    while ip < len(program):
        instruction, operand = program[ip], program[ip + 1]

        match instruction:
            case 0:  # adv (division: A = A / 2**opc)
                op, op_repr= combo_operands(operand, registers)
                debug("adv", op_repr)
                registers["A"] = int(registers["A"] / 2**op)

            case 1:  # bxl (bitwise XOR: B = B ^ litop)
                op, op_repr = literal_operand(operand)
                debug("bxl", op_repr)
                registers["B"] ^= op

            case 2:  # bst (modulo: B = opc % 8)
                op, op_repr = combo_operands(operand, registers)
                debug("bst", op_repr)
                registers["B"] = op % 8

            case 3:  # jnz (jump if not zero)
                op, op_repr = literal_operand(operand)
                debug("jnz", op_repr)
                if registers["A"] != 0:
                    ip = op - 2

            case 4:  # bxc (bitwise B = XOR: B ^ C)
                op, _ = literal_operand(operand)
                debug("bxc", "")
                registers["B"] ^= registers["C"]

            case 5:  # out (print combo % 8)
                op, op_repr = combo_operands(operand, registers)
                debug("out", op_repr)
                out.append(op % 8)

            case 6:  # bdv (division: B = A / 2**opc)
                op, op_repr= combo_operands(operand, registers)
                debug("bdv", op_repr)
                registers["B"] = int(registers["A"] / 2**op)

            case 7:  # cdv (diviion: C = A / 2**opc)
                op, op_repr= combo_operands(operand, registers)
                debug("cdv", op_repr)
                registers["C"] = int(registers["A"] / 2**op)

        ip += 2

    output = jj(out)
    if verbose:
        print("Program output:")
        print("output")
    return output


# Brute force doesn't work, only for example
def find_quine(s: str):
    registers, program = parse_program(s)
    A = -1

    expected = jj(program)
    result = ""
    while expected != result:
        A += 1
        # print("A", A)
        new_regs = {k: v for k, v in registers.items()}
        new_regs["A"] = A
        result = run_cpu(new_regs, program)

    return(A)


example_program = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""


example_quine = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""


"""
Decompiling the program gives us:

0: bst A
2: bxl 1
4: cdv B
6: adv 3
8: bxc
10: bxl 6
12: out B
14: jnz 0

Which is:
B = A % 8
B = B ^ 1
C = A >> B
A = A >> 3
B = B ^ C
B = B ^ 6

Refactored:
B = (A % 8) ^ 1
C = A >> B
A = A >> 3
B = (B ^ C) ^ 6
out(B)
jnz(0)

Since A is always >> 3 each step, when input A is << 3, it will output the same numbers plus one new one
So we at first just need to find the last expected digit, then shift << 3 before trying to find the next one
"""
def run_re(a):
    b = 0
    c = 0

    out = []
    while a != 0:
        b = (a % 8) ^ 1
        c = a >> b
        a >>= 3
        b = (b ^ c) ^ 6
        out.append(b % 8)
    return out


def find_quine_re(s):
    _, program = parse_program(s)
    out = []
    A = 56 << 3  # Found with a small loop until the result of run is the last two digits of the program
    nth_digit = -3
    while True:
        A += 1
        out = run_re(A)
        # print(nth_digit)
        if str(out) == str(program[nth_digit:]):
            # print(nth_digit, out[nth_digit], program[nth_digit])
            # print(str(out).rjust(50))
            # print(str(program).rjust(50))

            if abs(nth_digit) == len(program):
                return A

            A <<= 3
            nth_digit -= 1

def example():
    assert execute_program(example_program) == "4,6,3,5,6,3,5,2,1,0"
    # assert find_quine(example_quine) == 117440


if __name__ == "__main__":
    example()

    with open("2024/17.input", "r") as f:
        program = f.read()

    registers, pp = parse_program(program)

    part1 = execute_program(program)
    print(part1)
    assert jj(run_re(registers["A"])) == part1
    print(find_quine_re(program))
