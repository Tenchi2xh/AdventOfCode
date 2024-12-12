# Advent Of Code

- [Requirements](#requirements)
- [Running](#running)
- [Tricks learned](#tricks-learned)
- [Part 2 times](#part-2-times)

## Requirements

- Python 3
- Scala 3, [Scala CLI](https://scala-cli.virtuslab.org/install/)
- Pyth:
    - `cd <somewhere> && git clone git@github.com:isaacg1/pyth.git`
    - Add `alias pyth="python3 <somewhere>/pyth.py"` to `~/.bash_profile` or `~/.bashrc`

## Running

- Python: run `python 202X/YY.py`
- Scala: run `scala-cli 202X/YY.sc`
- Pyth: run `pyth -dm 202X/YY.pyth < 202X/YY.input`

## Tricks learned

### General

- `2024/11`: Read and analyze the problems carefully (order doesn't matter, even though they say it does), and also memoization is your friend

### Python

- `2024/01`: I wanted to memoize the counts in `similarity()`, and discovered that instead of doing `{a: l1.count(a) for a in l0}`, `collections` provides a nifty `Counter` class.
- `2024/07`: How to `reduce` with an operator that changes each time it's called:
    ```py
    operands = ...         # [1, 2, 3, 4]
    operators = iter(...)  # ("*", "+", "/")
    result = reduce(lambda a, b: next(operators)(a, b), operands)
    ```

### Scala

- `2024/02`: To remove an index from a `List`, instead of `list.take(i) ++ list.drop(i + 1)`, there is `list.patch(i, Nil, 1)`

## Part 2 times

Format: `yyyy/dd, h:mm`. For times lnger than 15 minutes, an explanation on why.

- `2024/01, 0:08`
- `2024/02, 0:05`
- `2024/03, 0:15`: Straight forward, but had an issue with regexes
- `2024/04, 0:08`
- `2024/05, 0:07`
- `2024/06, 0:20`: Mistake was overwriting the same map with walls
- `2024/07, 0:03`
- `2024/08, 0:10`
- `2024/09, 1:44`: Tried to write a different approach with classes, went back to just blocks
- `2024/10, 0:03`
- `2024/11, 1:00`: Brute force part 1 didn't work for part 2, needed refactoring and memoization
- `2024/12, 0.38`: Challenging to invent an algorithm for counting distinct edges
