import gzip
import os
from collections import defaultdict

# ==========================================================
# Group Parameters (Roll Numbers: 25i-0654, 25i-1047, 25i-0898)
# ==========================================================
R = 2599
PAIR_INDEX = R % 190                  # 129 -> top-20 indices (8, 14)
NUM_RANDOM_NETWORKS = 20 + (R % 31)   # 46
SWAP_MULTIPLIER = 5 + (R % 6)         # 6
SEED = R                              # 2599


def _open_data_file(gz_path):
    """Open either the .txt.gz file or an extracted .txt file if present."""
    if os.path.exists(gz_path):
        return gzip.open(gz_path, "rt", encoding="utf-8")
    txt_path = gz_path[:-3] if gz_path.endswith(".gz") else gz_path
    if os.path.exists(txt_path):
        return open(txt_path, "r", encoding="utf-8")
    raise FileNotFoundError(
        f"Dataset file not found: '{gz_path}' (or '{txt_path}'). "
        "Please place the SNAP email-Eu-core files inside the 'data/' folder."
    )


def load_edges(filepath):
    """Load directed edges, removing self-loops (u == v) and duplicates."""
    edges = set()
    with _open_data_file(filepath) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            u = int(parts[0])
            v = int(parts[1])
            if u != v:
                edges.add((u, v))
    return edges


def load_departments(filepath):
    """Load node-to-department mapping and department-to-nodes grouping."""
    node_to_dept = {}
    dept_to_nodes = defaultdict(set)
    with _open_data_file(filepath) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            node = int(parts[0])
            dept = int(parts[1])
            node_to_dept[node] = dept
            dept_to_nodes[dept].add(node)
    return node_to_dept, dept_to_nodes


def get_top_20_departments(edges, node_to_dept, dept_to_nodes):
    """
    Rank all departments by number of internal edges (both endpoints in same dept).
    Largest first; ties broken by smaller department ID.
    Returns list of (dept_id, internal_edge_count) for indices 0..19.
    """
    internal_edge_counts = {dept: 0 for dept in dept_to_nodes}
    for u, v in edges:
        if u in node_to_dept and v in node_to_dept:
            if node_to_dept[u] == node_to_dept[v]:
                internal_edge_counts[node_to_dept[u]] += 1

    ranked = sorted(
        internal_edge_counts.items(),
        key=lambda item: (-item[1], item[0])
    )
    return ranked[:20]


def get_department_pair(top_20, pair_index):
    """Select the (i, j) pair at pair_index in lexicographic order (0 <= i < j <= 19)."""
    pairs = []
    for i in range(20):
        for j in range(i + 1, 20):
            pairs.append((i, j))
    idx_a, idx_b = pairs[pair_index]
    dept_a = top_20[idx_a][0]
    dept_b = top_20[idx_b][0]
    return idx_a, idx_b, dept_a, dept_b


def build_induced_subgraph(edges, dept_nodes):
    """Build induced subgraph G[V_D] containing only edges with both endpoints in V_D."""
    sub_edges = set()
    for u, v in edges:
        if u in dept_nodes and v in dept_nodes:
            sub_edges.add((u, v))
    return set(dept_nodes), sub_edges


if __name__ == "__main__":
    edges = load_edges("data/email-Eu-core.txt.gz")
    node_to_dept, dept_to_nodes = load_departments("data/email-Eu-core-department-labels.txt.gz")

    top_20 = get_top_20_departments(edges, node_to_dept, dept_to_nodes)
    idx_a, idx_b, dept_a, dept_b = get_department_pair(top_20, PAIR_INDEX)

    nodes_a, edges_a = build_induced_subgraph(edges, dept_to_nodes[dept_a])
    nodes_b, edges_b = build_induced_subgraph(edges, dept_to_nodes[dept_b])

    print("=" * 55)
    print(f"R = {R}")
    print(f"Pair index = {PAIR_INDEX} -> top-20 indices ({idx_a}, {idx_b})")
    print(f"Department A = {dept_a} | Nodes: {len(nodes_a)}, Edges: {len(edges_a)}")
    print(f"Department B = {dept_b} | Nodes: {len(nodes_b)}, Edges: {len(edges_b)}")
    print(f"Random networks = {NUM_RANDOM_NETWORKS}")
    print(f"Swap attempts per network = {SWAP_MULTIPLIER} * |E|")
    print(f"  Dept A swap attempts = {SWAP_MULTIPLIER * len(edges_a)}")
    print(f"  Dept B swap attempts = {SWAP_MULTIPLIER * len(edges_b)}")
    print(f"Random seed = {SEED}")
    print("=" * 55)
