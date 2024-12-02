# Advent Of Code

## Tricks learned

### Python

- `2024/01`: I wanted to memoize the counts in `similarity()`, and discovered that instead of doing `{a: l1.count(a) for a in l0}`, `collections` provides a nifty `Counter` class.

### Scala

- `2024/02`: To remove an index from a `List`, instead of `list.take(i) ++ list.drop(i + 1)`, there is `list.patch(i, Nil, 1)`
