from collections import defaultdict
from itertools import permutations

# Sorted ascending canonical codes for the 13 connected triad classes (Class 1 to Class 13)
CANONICAL_CODES = [3, 6, 7, 10, 11, 15, 21, 23, 25, 27, 30, 31, 63]
CODE_TO_CLASS = {code: idx + 1 for idx, code in enumerate(CANONICAL_CODES)}


def triad_class(a, b, c, edges):
    """
    Return the triad class (1..13) of connected 3-node subset {a, b, c}
    using the fixed 6-bit canonical encoding minimized over all 6 permutations.

    Bit mapping for ordering (x0, x1, x2):
      Bit 0: x0 -> x1   Bit 1: x0 -> x2   Bit 2: x1 -> x0
      Bit 3: x1 -> x2   Bit 4: x2 -> x0   Bit 5: x2 -> x1
    """
    nodes = (a, b, c)
    min_code = 64

    for x0, x1, x2 in permutations(nodes):
        code = 0
        if (x0, x1) in edges:
            code |= (1 << 0)
        if (x0, x2) in edges:
            code |= (1 << 1)
        if (x1, x0) in edges:
            code |= (1 << 2)
        if (x1, x2) in edges:
            code |= (1 << 3)
        if (x2, x0) in edges:
            code |= (1 << 4)
        if (x2, x1) in edges:
            code |= (1 << 5)

        if code < min_code:
            min_code = code

    return CODE_TO_CLASS[min_code]


def count_triads(nodes, edges):
    """
    Compute the triad census N(G) = [N_1, ..., N_13] for all connected 3-subsets.
    Every connected triad contains a node adjacent to the other two, so we enumerate
    pairs of undirected neighbors of each node and deduplicate via a set.
    """
    undirected_adj = defaultdict(set)
    for u, v in edges:
        undirected_adj[u].add(v)
        undirected_adj[v].add(u)

    seen_triads = set()
    counts = [0] * 13

    for center in nodes:
        neighbors = list(undirected_adj[center])
        n = len(neighbors)
        for i in range(n):
            for j in range(i + 1, n):
                u = neighbors[i]
                v = neighbors[j]
                triad = tuple(sorted((center, u, v)))
                if triad not in seen_triads:
                    seen_triads.add(triad)
                    cls = triad_class(triad[0], triad[1], triad[2], edges)
                    counts[cls - 1] += 1

    return counts


if __name__ == "__main__":
    # Hand-worked example verification: Feed-Forward Loop (a -> b, a -> c, b -> c)
    # Minimum 6-bit code over all 6 permutations is 11 -> Class 5
    sample_edges = {("a", "b"), ("a", "c"), ("b", "c")}
    cls = triad_class("a", "b", "c", sample_edges)
    print(f"Hand-worked example (a->b, a->c, b->c) classified as: Class {cls} (expected Class 5)")
    assert cls == 5
