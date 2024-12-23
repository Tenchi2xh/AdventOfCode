from collections import defaultdict
from typing import Dict, List, Set




def parse_network(s: str):
    raw_links = [l.split("-") for l in s.strip().splitlines()]
    graph: Dict[str, Set[str]] = defaultdict(set)
    for l, r in raw_links:
        graph[l].add(r)
        graph[r].add(l)
    return graph


def count_interconnected(s: str):
    graph = parse_network(s)

    triads = set()

    for a in graph:
        for b in graph[a]:
            common = graph[a].intersection(graph[b])
            for c in common:
                triad = (a, b, c)
                if any(s.startswith("t") for s in triad):
                    triads.add(tuple(sorted(triad)))

    return len(triads)


def bron_kerbosch(
    clique: Set[str],
    candidates: Set[str],
    excluded: Set[str],
    graph: Dict[str, Set[str]],
    valid_cliques: List[Set[str]]
):
    if not candidates and not excluded:
        valid_cliques.append(clique)
        return

    for node in list(candidates):
        new_clique = clique.union({node})
        new_candidates = candidates.intersection(graph[node])
        new_excluded = excluded.intersection(graph[node])
        bron_kerbosch(new_clique, new_candidates, new_excluded, graph, valid_cliques)
        candidates.remove(node)
        excluded.add(node)


def largest_interconnected(s: str):
    graph = parse_network(s)

    valid_cliques = []
    bron_kerbosch(set(), set(graph.keys()), set(), graph, valid_cliques)
    largest = max(valid_cliques, key=len)

    return ",".join(sorted(list(largest)))


example_network = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def example():
    assert count_interconnected(example_network) == 7
    assert largest_interconnected(example_network) == "co,de,ka,ta"


if __name__ == "__main__":
    example()

    with open("2024/23.input", "r") as f:
        network = f.read()

    print(count_interconnected(network))
    print(largest_interconnected(network))
