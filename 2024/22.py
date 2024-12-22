
from collections import defaultdict
from itertools import chain
from typing import Dict, List


bits = (1 << 24) - 1


def mix(value: int, secret: int):
    return value ^ secret


def prune(secret: int):
    return secret & bits


def next_prng(secret: int):
    # Non-inline:
    # secret = prune(mix(secret << 6, secret))
    # secret = prune(mix(int(secret / 32), secret))
    # secret = prune(mix(secret << 11, secret))
    # Inline:
    secret = ((secret << 6) ^ secret) & bits
    secret = (int(secret / 32) ^ secret) & bits
    secret = ((secret << 11) ^ secret) & bits

    return secret


def prng(seed: int):
    secret = seed
    while True:
        secret = next_prng(secret)
        yield secret


def add_secrets(s: str):
    secrets = [int(n) for n in s.strip().splitlines()]
    total = 0
    for secret in secrets:
        for _ in range(2000):
            secret = next_prng(secret)
        total += secret
    return total


def find_all_sequences(initial_secret, secrets) -> Dict[str, int]:
    price = initial_secret % 10
    sequences = defaultdict(int)
    sequence = []
    for i, secret in enumerate(secrets):
        new_price = secret % 10
        delta = new_price - price
        price = new_price
        sequence.append(delta)
        if i >= 3:
            seq = ",".join(str(s) for s in sequence)
            if seq not in sequences:
                sequences[seq] = price
            sequence.pop(0)
    return sequences


def buy_bananas(s: str):
    secrets = [int(n) for n in s.strip().splitlines()]
    rnds = [prng(s) for s in secrets]
    lists = [list(next(rnd) for _ in range(2000)) for rnd in rnds]
    all_sequences = [find_all_sequences(secrets[i], lists[i]) for i in range(len(secrets))]

    max_price = 0
    max_k = ""

    all_keys = set(chain(*(seqs.keys() for seqs in all_sequences)))
    l = len(all_keys)
    for i, k in enumerate(all_keys):
        # print(f"{100 * i / l:4.2f}%")
        price = sum(seqs.get(k, 0) for seqs in all_sequences)
        if price > max_price:
            max_price = price
            max_k = k

    # print(max_k, "=", max_price)
    return max_price


example_secrets = """
1
10
100
2024
"""

example_secrets2 = """
1
2
3
2024
"""

def example():
    rnd = prng(123)
    assert list(next(rnd) for i in range(10)) == [
        15887950,
        16495136,
        527345,
        704524,
        1553684,
        12683156,
        11100544,
        12249484,
        7753432,
        5908254,
    ]

    assert add_secrets(example_secrets) == 37327623
    assert buy_bananas(example_secrets2) == 23


if __name__ == "__main__":
    example()

    with open("2024/22.input", "r") as f:
        secrets = f.read()

    print(add_secrets(secrets))
    print(buy_bananas(secrets))
