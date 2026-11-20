"""
CS1005 - Discrete Structures (Fall 2026) Course Project
Finding Network Motifs in an Email Network

Group Parameters:
  Members: 25i-0654 (Muhammad Abuzar), 25i-1047(Ahmed Basit), 24i-0898(Noor Fatima)
  Group Number R = 654 + 1047 + 898 = 2599
  Pair Index = 2599 mod 190 = 129 -> top-20 indices (8, 14)
  Random Networks = 20 + (2599 mod 31) = 46
  Swap Attempts per Network = (5 + (2599 mod 6)) * |E| = 6 * |E|
  Random Seed = 2599
"""

import math
from src.data_loader import (
    R,
    PAIR_INDEX,
    NUM_RANDOM_NETWORKS,
    SWAP_MULTIPLIER,
    SEED,
    load_edges,
    load_departments,
    get_top_20_departments,
    get_department_pair,
    build_induced_subgraph,
)
from src.motifs import count_triads
from src.randomizer import randomize
from src.plotting import plot_z_scores


def compute_z_scores(real_counts, nodes, edges, num_networks, swap_mult, base_seed):
    """
    Generate `num_networks` randomized graphs (each starting from original `edges`),
    count triads in each, and compute population Z-scores for all 13 classes.
    """
    attempts = swap_mult * len(edges)
    random_counts_all = []

    for i in range(num_networks):
        rand_edges = randomize(edges, attempts, base_seed + i)
        rand_counts = count_triads(nodes, rand_edges)
        random_counts_all.append(rand_counts)

    z_scores = []
    for k in range(13):
        vals = [rc[k] for rc in random_counts_all]
        mean = sum(vals) / num_networks
        variance = sum((v - mean) ** 2 for v in vals) / num_networks
        std = math.sqrt(variance)

        if std == 0:
            z_scores.append(0.0)
        else:
            z_scores.append((real_counts[k] - mean) / std)

    return z_scores


def summarize_motifs(z_scores, dept_label):
    motifs = [f"Class {k + 1} (Z={z:.2f})" for k, z in enumerate(z_scores) if z > 2]
    anti_motifs = [f"Class {k + 1} (Z={z:.2f})" for k, z in enumerate(z_scores) if z < -2]
    print(f"\n{dept_label}:")
    print("  Motifs (Z > 2):      ", ", ".join(motifs) if motifs else "None")
    print("  Anti-motifs (Z < -2):", ", ".join(anti_motifs) if anti_motifs else "None")


def main():
    edges = load_edges("data/email-Eu-core.txt.gz")
    node_to_dept, dept_to_nodes = load_departments("data/email-Eu-core-department-labels.txt.gz")

    top_20 = get_top_20_departments(edges, node_to_dept, dept_to_nodes)
    idx_a, idx_b, dept_a, dept_b = get_department_pair(top_20, PAIR_INDEX)

    nodes_a, edges_a = build_induced_subgraph(edges, dept_to_nodes[dept_a])
    nodes_b, edges_b = build_induced_subgraph(edges, dept_to_nodes[dept_b])

    print("=" * 60)
    print(f"Group Number R:            {R}")
    print(f"Pair Index:                {PAIR_INDEX} -> top-20 indices ({idx_a}, {idx_b})")
    print(f"Department A:              {dept_a} (Nodes: {len(nodes_a)}, Edges: {len(edges_a)})")
    print(f"Department B:              {dept_b} (Nodes: {len(nodes_b)}, Edges: {len(edges_b)})")
    print(f"Random Networks:           {NUM_RANDOM_NETWORKS}")
    print(f"Swap Attempts per Network: {SWAP_MULTIPLIER} * |E|")
    print(f"  Dept A swap attempts:    {SWAP_MULTIPLIER * len(edges_a)}")
    print(f"  Dept B swap attempts:    {SWAP_MULTIPLIER * len(edges_b)}")
    print(f"Random Seed:               {SEED}")
    print("=" * 60)

    counts_a = count_triads(nodes_a, edges_a)
    counts_b = count_triads(nodes_b, edges_b)

    print("\nT4: Real Triad Counts")
    print(f"{'Class':<8} | {'Dept ' + str(dept_a):<12} | {'Dept ' + str(dept_b):<12}")
    print("-" * 38)
    for k in range(13):
        print(f"{k + 1:<8} | {counts_a[k]:<12} | {counts_b[k]:<12}")

    print("\nRunning randomization (with degree-preservation assertions) and computing Z-scores...")
    z_a = compute_z_scores(counts_a, nodes_a, edges_a, NUM_RANDOM_NETWORKS, SWAP_MULTIPLIER, SEED)
    z_b = compute_z_scores(counts_b, nodes_b, edges_b, NUM_RANDOM_NETWORKS, SWAP_MULTIPLIER, SEED)

    print("\nT6: Z-Scores")
    print(f"{'Class':<8} | {'Dept ' + str(dept_a):<12} | {'Dept ' + str(dept_b):<12}")
    print("-" * 38)
    for k in range(13):
        print(f"{k + 1:<8} | {z_a[k]:<12.3f} | {z_b[k]:<12.3f}")

    summarize_motifs(z_a, f"Department {dept_a} (A)")
    summarize_motifs(z_b, f"Department {dept_b} (B)")

    plot_z_scores(z_a, z_b, dept_a, dept_b, R, output_path="motif_zscores.png")


if __name__ == "__main__":
    main()
