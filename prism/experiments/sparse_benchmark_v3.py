"""
Sparse Benchmark v3: Prism as Fault Line Detector

v2 revealed: Prism measures BOUNDARY POSITION (fiedler cut proximity),
not engineering criticality. It identifies nodes sitting at the spectral
bisection — the structural fault line between communities.

This is genuinely different from betweenness (which measures flow) and
degree (which measures local connectivity). The question now:

  Is "fault line detection" a useful product?

Applications where boundary/fault-line nodes matter:
  1. Supply chain: nodes connecting different supplier clusters
     → single points of failure between supply ecosystems
  2. Social networks: bridge individuals between communities
     → influence maximization, information flow control
  3. Infrastructure: interfaces between subsystems
     → where failures cascade across system boundaries
  4. Biological: metabolic pathway junctions
     → drug targets at pathway intersections

This experiment tests on networks with KNOWN community structure:
  - Does Prism correctly identify inter-community bridges?
  - Does it outperform betweenness at finding BOUNDARY nodes specifically?
  - Is the global defect a measure of how "fractured" the network is?

Key insight: if a network has clear communities, the fault line nodes
are WHERE it would break. Prism finds these without knowing the communities.
"""

import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from scipy.stats import spearmanr
import time


def laplacian(A):
    return np.diag(A.sum(axis=1)) - A


def fiedler_P(L):
    n = L.shape[0]
    _, evecs = np.linalg.eigh(L)
    fiedler = evecs[:, 1]
    order = np.argsort(fiedler)
    perm = np.zeros(n, dtype=int)
    for rank, node in enumerate(order):
        perm[node] = order[n - 1 - rank]
    P = np.zeros((n, n))
    for i in range(n):
        P[i, perm[i]] = 1.0
    return (P + P.T) / 2, evecs[:, 1]


def per_node_defect(L, P):
    comm = L @ P - P @ L
    L_norm = np.linalg.norm(L, 'fro') + 1e-10
    return np.linalg.norm(comm, axis=1) / L_norm


def global_defect(L, P):
    comm = L @ P - P @ L
    return np.linalg.norm(comm, 'fro') / (np.linalg.norm(L, 'fro') + 1e-10)


def betweenness_centrality(A):
    from scipy.sparse.csgraph import shortest_path
    n = A.shape[0]
    betweenness = np.zeros(n)
    dist, pred = shortest_path(
        sparse.csr_matrix(A), method='D', directed=False,
        return_predecessors=True
    )
    for s in range(n):
        for t in range(n):
            if t == s or np.isinf(dist[s, t]):
                continue
            path = []
            current = t
            while current != s and current >= 0:
                path.append(current)
                current = pred[s, current]
            for node in path[1:]:
                betweenness[node] += 1
    betweenness /= ((n-1) * (n-2) / 2 + 1e-10)
    return betweenness


# ═══════════════════════════════════════════════════════════════════════════════
# NETWORKS WITH KNOWN COMMUNITY STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

def planted_partition(n_communities=4, community_size=20, p_in=0.3, p_out=0.02, seed=42):
    """Stochastic block model with known ground truth communities."""
    np.random.seed(seed)
    n = n_communities * community_size
    A = np.zeros((n, n))
    communities = np.zeros(n, dtype=int)

    for c in range(n_communities):
        start = c * community_size
        end = start + community_size
        communities[start:end] = c
        # Intra-community edges
        for i in range(start, end):
            for j in range(i+1, end):
                if np.random.random() < p_in:
                    A[i, j] = 1; A[j, i] = 1

    # Inter-community edges
    for i in range(n):
        for j in range(i+1, n):
            if communities[i] != communities[j]:
                if np.random.random() < p_out:
                    A[i, j] = 1; A[j, i] = 1

    # Ground truth: is this node a boundary node?
    is_boundary = np.zeros(n)
    for i in range(n):
        neighbors = np.where(A[i] > 0)[0]
        for nb in neighbors:
            if communities[nb] != communities[i]:
                is_boundary[i] = 1
                break

    # Boundary strength: fraction of edges that cross community
    boundary_strength = np.zeros(n)
    for i in range(n):
        neighbors = np.where(A[i] > 0)[0]
        if len(neighbors) == 0:
            continue
        cross = sum(1 for nb in neighbors if communities[nb] != communities[i])
        boundary_strength[i] = cross / len(neighbors)

    return A, communities, is_boundary, boundary_strength, \
           f"SBM ({n_communities}x{community_size}, p_in={p_in}, p_out={p_out})"


def hierarchical_network(seed=42):
    """Two-level hierarchy: 4 groups of 3 clusters.
    Boundary nodes exist at both levels."""
    np.random.seed(seed)
    n = 60  # 4 groups × 3 clusters × 5 nodes
    A = np.zeros((n, n))
    communities_l1 = np.zeros(n, dtype=int)  # 12 clusters
    communities_l2 = np.zeros(n, dtype=int)  # 4 groups

    cluster_size = 5
    clusters_per_group = 3

    for group in range(4):
        for cluster in range(clusters_per_group):
            cluster_id = group * clusters_per_group + cluster
            start = cluster_id * cluster_size
            end = start + cluster_size
            communities_l1[start:end] = cluster_id
            communities_l2[start:end] = group
            # Dense within cluster
            for i in range(start, end):
                for j in range(i+1, end):
                    if np.random.random() < 0.6:
                        A[i, j] = 1; A[j, i] = 1

        # Sparse between clusters within group
        for c1 in range(clusters_per_group):
            for c2 in range(c1+1, clusters_per_group):
                s1 = (group * clusters_per_group + c1) * cluster_size
                s2 = (group * clusters_per_group + c2) * cluster_size
                # 1-2 bridge edges
                for _ in range(2):
                    i = s1 + np.random.randint(cluster_size)
                    j = s2 + np.random.randint(cluster_size)
                    A[i, j] = 1; A[j, i] = 1

    # Very sparse between groups
    for g1 in range(4):
        for g2 in range(g1+1, 4):
            s1 = g1 * clusters_per_group * cluster_size
            s2 = g2 * clusters_per_group * cluster_size
            i = s1 + np.random.randint(clusters_per_group * cluster_size)
            j = s2 + np.random.randint(clusters_per_group * cluster_size)
            A[i, j] = 1; A[j, i] = 1

    # Boundary: nodes with cross-group edges
    is_boundary = np.zeros(n)
    boundary_strength = np.zeros(n)
    for i in range(n):
        neighbors = np.where(A[i] > 0)[0]
        if len(neighbors) == 0:
            continue
        cross = sum(1 for nb in neighbors if communities_l2[nb] != communities_l2[i])
        if cross > 0:
            is_boundary[i] = 1
        boundary_strength[i] = cross / len(neighbors)

    return A, communities_l2, is_boundary, boundary_strength, \
           "Hierarchical (4 groups × 3 clusters × 5 nodes)"


def supply_chain_model(seed=42):
    """Simplified supply chain: 3 tiers (raw → manufacturing → retail).
    Boundary nodes connect tiers. Known bottlenecks."""
    np.random.seed(seed)
    # Tier 1: 10 raw material suppliers (2 clusters)
    # Tier 2: 15 manufacturers (3 clusters)
    # Tier 3: 10 retailers (2 clusters)
    n = 35
    A = np.zeros((n, n))
    tier = np.zeros(n, dtype=int)
    tier[0:10] = 0   # raw
    tier[10:25] = 1  # manufacturing
    tier[25:35] = 2  # retail

    # Within-tier connections (same cluster)
    # Raw: 2 clusters of 5
    for i in range(5):
        for j in range(i+1, 5):
            if np.random.random() < 0.4:
                A[i,j] = 1; A[j,i] = 1
    for i in range(5, 10):
        for j in range(i+1, 10):
            if np.random.random() < 0.4:
                A[i,j] = 1; A[j,i] = 1

    # Manufacturing: 3 clusters of 5
    for c in range(3):
        start = 10 + c*5
        for i in range(start, start+5):
            for j in range(i+1, start+5):
                if np.random.random() < 0.5:
                    A[i,j] = 1; A[j,i] = 1

    # Retail: 2 clusters of 5
    for i in range(25, 30):
        for j in range(i+1, 30):
            if np.random.random() < 0.4:
                A[i,j] = 1; A[j,i] = 1
    for i in range(30, 35):
        for j in range(i+1, 35):
            if np.random.random() < 0.4:
                A[i,j] = 1; A[j,i] = 1

    # Cross-tier connections (the supply chain links)
    # Raw → Manufacturing (sparse, these are the bottlenecks)
    bottleneck_nodes = []
    for _ in range(6):
        i = np.random.randint(10)
        j = 10 + np.random.randint(15)
        A[i,j] = 1; A[j,i] = 1
        bottleneck_nodes.extend([i, j])

    # Manufacturing → Retail
    for _ in range(6):
        i = 10 + np.random.randint(15)
        j = 25 + np.random.randint(10)
        A[i,j] = 1; A[j,i] = 1
        bottleneck_nodes.extend([i, j])

    # Ground truth boundary
    is_boundary = np.zeros(n)
    boundary_strength = np.zeros(n)
    for i in range(n):
        neighbors = np.where(A[i] > 0)[0]
        if len(neighbors) == 0:
            continue
        cross = sum(1 for nb in neighbors if tier[nb] != tier[i])
        if cross > 0:
            is_boundary[i] = 1
        boundary_strength[i] = cross / len(neighbors)

    return A, tier, is_boundary, boundary_strength, \
           "Supply Chain (3-tier, n=35)"


# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL DEFECT vs COMMUNITY CLARITY
# ═══════════════════════════════════════════════════════════════════════════════

def test_defect_vs_modularity():
    """Does global defect correlate with how clearly separated communities are?
    Sweep p_out from 0 (perfect separation) to p_in (random graph)."""
    print("\n" + "=" * 80)
    print("GLOBAL DEFECT vs COMMUNITY SEPARATION")
    print("=" * 80)
    print("""
  Hypothesis: global defect measures how "fractured" the network is.
  As p_out increases (communities blur), defect should change monotonically.
""")

    p_in = 0.3
    p_outs = [0.005, 0.01, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20, 0.25, 0.30]

    print(f"  {'p_out':>6} {'p_out/p_in':>10} {'Global d':>9} {'Modularity':>11} {'Fiedler l2':>11}")
    print(f"  {'-'*55}")

    for p_out in p_outs:
        A, communities, _, _, _ = planted_partition(
            n_communities=4, community_size=15, p_in=p_in, p_out=p_out, seed=42
        )
        n_comp, _ = connected_components(sparse.csr_matrix(A), directed=False)
        if n_comp > 1:
            print(f"  {p_out:>6.3f} {'disconnected':>10}")
            continue

        L = laplacian(A)
        P, _ = fiedler_P(L)
        d = global_defect(L, P)
        lam2 = np.linalg.eigvalsh(L)[1]

        # Simple modularity estimate
        m = A.sum() / 2
        Q = 0
        for i in range(A.shape[0]):
            for j in range(A.shape[0]):
                if communities[i] == communities[j]:
                    ki = A[i].sum()
                    kj = A[j].sum()
                    Q += A[i,j] - ki*kj/(2*m)
        Q /= (2*m)

        print(f"  {p_out:>6.3f} {p_out/p_in:>10.2f} {d:>9.4f} {Q:>11.4f} {lam2:>11.4f}")

    print("""
  If defect decreases as communities blur (p_out → p_in):
    → defect measures community SEPARATION strength
    → high defect = clear communities = network has fault lines
    → low defect = homogeneous = no natural partition

  If defect is non-monotonic or uncorrelated:
    → defect doesn't measure community structure directly
""")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN BENCHMARK
# ═══════════════════════════════════════════════════════════════════════════════

def benchmark_boundary_detection(A, communities, is_boundary, boundary_strength, name):
    """Test: does Prism find boundary nodes better than betweenness?"""
    n = A.shape[0]
    L = laplacian(A)
    P, fiedler_vec = fiedler_P(L)
    node_d = per_node_defect(L, P)
    betw = betweenness_centrality(A)
    degree = A.sum(axis=1)
    d = global_defect(L, P)

    print(f"\n{'='*80}")
    print(f"  {name}")
    print(f"  n={n}, edges={int(A.sum()//2)}, global_defect={d:.4f}")
    print(f"  Boundary nodes: {int(is_boundary.sum())}/{n} "
          f"({is_boundary.sum()/n*100:.0f}%)")
    print(f"{'='*80}")

    # Correlation with boundary strength (continuous)
    if np.std(boundary_strength) > 1e-10:
        rho_prism, _ = spearmanr(node_d, boundary_strength)
        rho_betw, _ = spearmanr(betw, boundary_strength)
        rho_deg, _ = spearmanr(degree, boundary_strength)
    else:
        rho_prism = rho_betw = rho_deg = np.nan

    print(f"\n  Correlation with boundary_strength (fraction of cross-community edges):")
    print(f"    Prism defect:    ρ = {rho_prism:>+.3f}")
    print(f"    Betweenness:     ρ = {rho_betw:>+.3f}")
    print(f"    Degree:          ρ = {rho_deg:>+.3f}")

    # Precision@k: what fraction of top-k by each metric are actual boundary nodes?
    k = min(10, int(is_boundary.sum()))
    if k > 0:
        top_prism = set(np.argsort(node_d)[::-1][:k])
        top_betw = set(np.argsort(betw)[::-1][:k])
        top_deg = set(np.argsort(degree)[::-1][:k])
        actual_boundary = set(np.where(is_boundary > 0)[0])

        prec_prism = len(top_prism & actual_boundary) / k
        prec_betw = len(top_betw & actual_boundary) / k
        prec_deg = len(top_deg & actual_boundary) / k

        print(f"\n  Precision@{k} for boundary node detection:")
        print(f"    Prism defect:    {prec_prism*100:.0f}%")
        print(f"    Betweenness:     {prec_betw*100:.0f}%")
        print(f"    Degree:          {prec_deg*100:.0f}%")

    # Show top-5 by Prism
    top5_idx = np.argsort(node_d)[::-1][:5]
    print(f"\n  Top-5 by Prism defect:")
    print(f"  {'Rank':<5} {'Node':>5} {'Community':>10} {'Boundary?':>10} "
          f"{'BoundStr':>9} {'Defect':>8} {'Betw':>8}")
    print(f"  {'-'*60}")
    for rank, idx in enumerate(top5_idx):
        print(f"  {rank+1:<5} {idx:>5} {communities[idx]:>10} "
              f"{'YES' if is_boundary[idx] else 'no':>10} "
              f"{boundary_strength[idx]:>9.2f} {node_d[idx]:>8.4f} {betw[idx]:>8.4f}")

    winner = "PRISM" if rho_prism > rho_betw else "BETWEENNESS"
    return {
        'name': name, 'n': n, 'global_defect': d,
        'rho_prism': rho_prism, 'rho_betw': rho_betw, 'rho_deg': rho_deg,
        'prism_wins': rho_prism > rho_betw, 'winner': winner,
    }


def run():
    print("=" * 80)
    print("PRISM AS FAULT LINE DETECTOR")
    print("=" * 80)
    print("""
  Reframed hypothesis: Prism identifies nodes at COMMUNITY BOUNDARIES
  (structural fault lines), not nodes whose removal degrades connectivity.

  This is a different product:
    - NOT "which node is most critical to remove"
    - YES "where are the structural seams in this network"

  Test: on networks with known community structure, does Prism find
  boundary nodes better than betweenness?
""")

    # Test networks with known communities
    networks = [
        lambda: planted_partition(4, 15, 0.3, 0.02),
        lambda: planted_partition(3, 20, 0.25, 0.03),
        lambda: planted_partition(6, 10, 0.35, 0.03),
        lambda: hierarchical_network(),
        lambda: supply_chain_model(),
    ]

    results = []
    for net_fn in networks:
        A, communities, is_boundary, boundary_strength, name = net_fn()
        n_comp, _ = connected_components(sparse.csr_matrix(A), directed=False)
        if n_comp > 1:
            print(f"\n  SKIP {name}: disconnected ({n_comp} components)")
            continue
        r = benchmark_boundary_detection(A, communities, is_boundary, boundary_strength, name)
        results.append(r)

    # Global defect vs modularity test
    test_defect_vs_modularity()

    # Summary
    print()
    print("=" * 80)
    print("SUMMARY: Prism as Boundary Detector")
    print("=" * 80)

    if results:
        print(f"\n  {'Network':<45} {'ρ(Prism)':>9} {'ρ(Betw)':>9} {'Winner':<12}")
        print(f"  {'-'*80}")
        for r in results:
            print(f"  {r['name']:<45} {r['rho_prism']:>+8.3f} "
                  f"{r['rho_betw']:>+8.3f} {r['winner']:<12}")

        prism_wins = sum(1 for r in results if r['prism_wins'])
        print(f"\n  Prism wins: {prism_wins}/{len(results)} networks")
        print(f"  Mean ρ(Prism): {np.mean([r['rho_prism'] for r in results if not np.isnan(r['rho_prism'])]):.3f}")
        print(f"  Mean ρ(Betw):  {np.mean([r['rho_betw'] for r in results if not np.isnan(r['rho_betw'])]):.3f}")

    print()
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)

    if results:
        prism_wins = sum(1 for r in results if r['prism_wins'])
        if prism_wins > len(results) * 0.6:
            print("""
  PASS: Prism outperforms betweenness at BOUNDARY DETECTION.
  The correct product framing is "fault line identifier":
    - Supply chain: where are the inter-tier bottlenecks?
    - Social: who bridges communities?
    - Infrastructure: where do subsystems interface?

  This is NOT criticality (betweenness wins there).
  This IS structural boundary detection (Prism wins here).
  Different product, different market, genuine value.
""")
        else:
            print("""
  FAIL: Prism does not reliably outperform betweenness even at
  boundary detection. The per-node decomposition may be fundamentally
  limited as a practical tool.

  Remaining value: GLOBAL defect as a scalar health metric.
  Per-node attribution does not have a viable product direction.
""")


if __name__ == "__main__":
    run()
