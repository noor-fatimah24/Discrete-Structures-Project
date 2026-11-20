import random
from collections import defaultdict


def get_degrees(edges):
    """Return (in_degree_dict, out_degree_dict) for the given directed edge set."""
    in_deg = defaultdict(int)
    out_deg = defaultdict(int)
    for u, v in edges:
        out_deg[u] += 1
        in_deg[v] += 1
    return in_deg, out_deg


def randomize(edges, attempts, seed):
    """
    Generate a null-model random directed graph via double-edge swaps.
    Each attempt picks two edges (a, b) and (c, d) uniformly at random and replaces
    them with (a, d) and (c, b), rejecting if a == d, c == b, or either new edge
    already exists. Rejected attempts still count toward `attempts`.
    Asserts that every node's in-degree and out-degree remain unchanged.
    """
    rng = random.Random(seed)
    edge_list = list(edges)
    edge_set = set(edges)
    num_edges = len(edge_list)

    orig_in, orig_out = get_degrees(edge_set)

    if num_edges < 2:
        return edge_set

    for _ in range(attempts):
        idx1 = rng.randrange(num_edges)
        idx2 = rng.randrange(num_edges)
        if idx1 == idx2:
            continue

        a, b = edge_list[idx1]
        c, d = edge_list[idx2]

        # Reject self-loops or parallel edges
        if a == d or c == b:
            continue
        if (a, d) in edge_set or (c, b) in edge_set:
            continue

        edge_set.remove((a, b))
        edge_set.remove((c, d))
        edge_set.add((a, d))
        edge_set.add((c, b))

        edge_list[idx1] = (a, d)
        edge_list[idx2] = (c, b)

    new_in, new_out = get_degrees(edge_set)
    assert orig_in == new_in, "In-degree sequence changed after randomization!"
    assert orig_out == new_out, "Out-degree sequence changed after randomization!"

    return edge_set
