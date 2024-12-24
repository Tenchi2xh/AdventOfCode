from collections import defaultdict
from operator import __and__, __or__, __xor__
import os
from pathlib import Path
import tempfile
from typing import Callable, Dict, List, Tuple
import webbrowser


Operator = Callable[[int, int], int]
GateWiring = Tuple[str, str, str, Operator]


operators: Dict[str, Operator] = {
    "AND": __and__,
    "OR": __or__,
    "XOR": __xor__,
}


def parse_circuit(s: str, do_operators=True):
    raw_signals, raw_gates = s.strip().split("\n\n")

    signals: Dict[str, int] = {
        l.split(": ")[0]: int(l.split(": ")[1])
        for l in raw_signals.splitlines()
    }

    gates: List[GateWiring] = []
    for l in raw_gates.splitlines():
        left, right = l.split(" -> ")
        a, gate, b = left.split()
        c = right
        if do_operators:
            gate = operators[gate]
        gates.append((a, b, c, gate))

    return signals, gates


def read_value(signals: Dict[str, int], prefix: str):
    value_keys = list(reversed(sorted([k for k in signals.keys() if k.startswith(prefix)])))
    value_bin = "".join(str(signals[k]) for k in value_keys)
    return int(value_bin, 2)


def write_values(signals: Dict[str, int], values: List[Tuple[str, int]], bits: int):
    new_signals = {k: v for k, v in signals.items()}
    for prefix, value in values:
        value_bin = bin(value)[2:].rjust(bits, "0")[::-1]
        for i, b in enumerate(value_bin):
            new_signals[prefix + str(i).rjust(2, "0")] = int(b)
    return new_signals


def simulate_gates(signals: Dict[str, int], gates: List[GateWiring]):
    new_signals = {k: v for k, v in signals.items()}
    while gates:
        new_gates = []
        for l in gates:
            (a, b, c, gate) = l
            if a in new_signals and b in new_signals:
                new_signals[c] = gate(new_signals[a], new_signals[b])
            else:
                new_gates.append(l)
        gates = new_gates

    return new_signals


def run_circuit(s: str):
    signals, gates = parse_circuit(s)
    new_signals = simulate_gates(signals, gates)
    z = read_value(new_signals, "z")
    return z


def visually_untwist(s: str, twists: List[Tuple[str, str]], name: str):
    # Requirement: npm install -g @mermaid-js/mermaid-cli

    _, gates = parse_circuit(s, do_operators=False)
    for x, y in twists:
        swap_x = next(i for i in range(len(gates)) if gates[i][2] == x)
        swap_y = next(i for i in range(len(gates)) if gates[i][2] == y)
        xx = gates[swap_x]
        yy = gates[swap_y]
        gates[swap_x] = (xx[0], xx[1], y, xx[3])
        gates[swap_y] = (yy[0], yy[1], x, yy[3])

    gate_counters = defaultdict(int)
    lines = []
    for (a, b, c, gate) in gates:
        gid = gate + str(gate_counters[gate]).rjust(3, "0")
        g = gid + "{" + gate + "}"
        fill = {"AND": "red", "OR": "blue", "XOR": "green"}[gate]
        lines.append(f"    style {gid} fill:{fill}")
        lines.append(f"    {a}(({a})) --> {g}")
        lines.append(f"    {b}(({b})) --> {g}")
        lines.append(f"    {g} --> {c}(({c}))")
        gate_counters[gate] += 1

    mermaid = "graph LR\n"
    # Sorting the nodes is important for a consistent layout
    mermaid += "\n".join(sorted(lines, reverse=True))

    fn = f"2024/24_{name}.mmd"
    fn2 = f"2024/24_{name}.svg"
    with open(fn, "w") as f:
        f.write(mermaid)

    with tempfile.NamedTemporaryFile() as f:
        f.write(b'{"maxEdges": 10000}\n')
        f.flush()

        os.system(f"mmdc -q -c {f.name} -i {fn} -o {fn2} 2>/dev/null")

        try:
            browser = webbrowser.get("chrome")
        except:
            browser = webbrowser.get("firefox")
        browser.open_new_tab(Path(fn2).resolve().as_uri())


example_circuit1 = """
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
"""

example_circuit2 = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""


def example():
    assert run_circuit(example_circuit1) == 4
    assert run_circuit(example_circuit2) == 2024


if __name__ == "__main__":
    example()

    with open("2024/24.input", "r") as f:
        circuit = f.read()

    print(run_circuit(circuit))

    # Found manually by analyzing the generated svgs
    twists = [
        ("dkr", "z05"),
        ("htp", "z15"),
        ("hhh", "z20"),
        ("ggk", "rhv"),
    ]

    visually_untwist(circuit, [], name="unsolved")
    visually_untwist(circuit, twists, name="solved")
    print(",".join(sorted([
        n
        for twist in twists
        for n in twist
    ])))

