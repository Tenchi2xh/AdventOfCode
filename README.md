# Advent Of Code

- [Requirements](#requirements)
- [Running](#running)
- [Tricks learned](#tricks-learned)

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

### Python

- `2024/01`: I wanted to memoize the counts in `similarity()`, and discovered that instead of doing `{a: l1.count(a) for a in l0}`, `collections` provides a nifty `Counter` class.

### Scala

- `2024/02`: To remove an index from a `List`, instead of `list.take(i) ++ list.drop(i + 1)`, there is `list.patch(i, Nil, 1)`
