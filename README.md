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
- `2024/16`: Dijkstra is much easier with a priority queue using `heapq`.
- `2024/18`: Binary search ftw. Discovered that stdlib `bisect.bisect_left` can do a binary search (but manually writing is only 3 lines).
- `2024/21`: When you don't have time to do a smart memoization, spam `functools.cache` everywhere.

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
- `2024/12, 0:38`: Challenging to invent an algorithm for counting distinct edges
- `2024/13, 0:04`
- `2024/14, 0:09`
- `2024/15, 0:22`: Part 2 introduced chain reactions, which needed recursion/stacks.
- `2024/16, 1:26`: Trouble with keeping all the paths in Dijkstra part 2.
    Solution was to also keep both position AND direction in the dictionary of visited positions, and keep track of the current path in the priority queue.
- `2024/17, 1:23`: Another non-bruteforceable part 2, needed to reverse engineer the assembly program.
- `2024/18, 0:13`
- `2024/19, 0:34`: Instead of trying to return all possible arrangements, which made the recursion more complicated, all I needed was to count the successful arrangement (while memoizing).
- `2024/20, 1:20`: Part 2 is weirdly worded, and again it was much easier to only count the good solutions instead of finding them.
- `2024/21, 0:48`: For this one, even part 1 took about two hours. It was hard to exactly implement the problem description and even get the example to be 100% correct. In the end, I think that the part that caused the most bugs was not detecting invalid positions when hovering over an empty square.
- `2024/22, 0:50`: Not particularly a hard part 2, it's just a completely new problem compared to part 1 so it took time to implement.
- `2024/23, 0:23`: Learned and implemented a new graph theory algorithm, the [Bron-Kerbosch algorithm](https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm).
- `2024/24, 2:37`: Fun problem! I don't even know where to start with part 2 programmatically, a brute force would take years. Ended up visualizing the circuit. Since the puzzle says it's a circuit that adds two numbers, I assumed correctly that it would be a chain of [full adders](https://en.wikipedia.org/wiki/Adder_(electronics)#Full_adder). After fiddling a while with [Mermaid](https://mermaid.js.org/), I finally managed to organize the output circuit so that mistakes are obvious to spot.
- `2024/25, 0:01`: Not a puzzle
