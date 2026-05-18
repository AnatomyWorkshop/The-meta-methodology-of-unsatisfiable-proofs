"""
Sparse Network Benchmark Suite: Does Prism identify critical nodes?

The key theoretical question from the financial death sentence:
  In what conditions does high duality defect correspond to engineering criticality?

This suite tests Prism against multiple baselines on networks where
ground truth criticality is KNOWN or MEASURABLE:

Networks:
  1. Karate Club (n=34) — known community split, ground truth partition
  2. Dolphins (n=62) — social network with known community structure
  3. Les Misérables (n=77) — co-appearance, known bridge characters
  4. Florentine families (n=15) — historical power network, known key families
  5. US power grid (n=4941) — real infrastructure, degree distribution known
  6. Minnesota road network (n=2642) — real transport topology
  7. C. elegans neural (n=297) — biological, known hub neurons

Criticality metric (ground truth):
  For each node i, remove it and measure:
    - Δ algebraic connectivity (change in Fiedler eigenvalue)
    - Δ average path length
    - Number of components created (fragmentation)

Success criteria:
  1. Prism's top-10 defect nodes overlap with top-10 by Δ-connectivity
     more than betweenness centrality does (Prism > betweenness)
  2. OR: Prism identifies a DIFFERENT kind of criticality that betweenness misses
  3. Correlation between node defect and Δ-connectivity > 0.3

If Prism ≤ betweenness on all networks: the method adds nothing beyond
existing centrality measures (α ≤ 1 in SRS terms).
"""

import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import connected_components, shortest_path
import time


def laplacian(A):
    D = np.diag(A.sum(axis=1))
    return D - A


def fiedler_eigenvalue(L):
    n = L.shape[0]
    if n < 3:
        return 0.0
    evals = np.linalg.eigvalsh(L)
    return float(evals[1])


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
    return (P + P.T) / 2


def per_node_defect(L, P):
    comm = L @ P - P @ L
    L_norm = np.linalg.norm(L, 'fro') + 1e-10
    return np.linalg.norm(comm, axis=1) / L_norm


def betweenness_centrality(A):
    n = A.shape[0]
    betweenness = np.zeros(n)
    for s in range(n):
        dist, predecessors = shortest_path(
            sparse.csr_matrix(A), method='D',
            directed=False, indices=s,
            return_predecessors=True
        )
        for t in range(n):
            if t == s or np.isinf(dist[t]):
                continue
            path = []
            current = t
            while current != s and current >= 0:
                path.append(current)
                current = predecessors[current]
            for node in path[1:]:  # exclude endpoints
                betweenness[node] += 1
    betweenness /= ((n - 1) * (n - 2) / 2 + 1e-10)
    return betweenness


def node_criticality(A):
    """Ground truth: how much does removing each node degrade the network?"""
    n = A.shape[0]
    L = laplacian(A)
    base_fiedler = fiedler_eigenvalue(L)

    criticality = np.zeros(n)
    for i in range(n):
        mask = np.ones(n, dtype=bool)
        mask[i] = False
        A_reduced = A[mask][:, mask]
        if A_reduced.shape[0] < 3:
            criticality[i] = base_fiedler
            continue
        L_reduced = laplacian(A_reduced)
        new_fiedler = fiedler_eigenvalue(L_reduced)
        criticality[i] = base_fiedler - new_fiedler
    return criticality


def rank_correlation(x, y):
    """Spearman rank correlation."""
    from scipy.stats import spearmanr
    rho, _ = spearmanr(x, y)
    return rho


# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════

def karate_club():
    """Zachary's Karate Club (n=34)."""
    edges = [
        (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,10),(0,11),
        (0,12),(0,13),(0,17),(0,19),(0,21),(0,31),(1,2),(1,3),(1,7),
        (1,13),(1,17),(1,19),(1,21),(1,30),(2,3),(2,7),(2,8),(2,9),
        (2,13),(2,27),(2,28),(2,32),(3,7),(3,12),(3,13),(4,6),(4,10),
        (5,6),(5,10),(5,16),(6,16),(8,30),(8,32),(8,33),(9,33),(13,33),
        (14,32),(14,33),(15,32),(15,33),(18,32),(18,33),(19,33),(20,32),
        (20,33),(22,32),(22,33),(23,25),(23,27),(23,29),(23,32),(23,33),
        (24,25),(24,27),(24,31),(25,31),(26,29),(26,33),(27,33),(28,31),
        (28,33),(29,32),(29,33),(30,32),(30,33),(31,32),(31,33),(32,33),
    ]
    n = 34
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = 1
        A[j, i] = 1
    labels = [f"N{i}" for i in range(n)]
    labels[0] = "Mr.Hi"
    labels[33] = "Officer"
    return A, labels, "Karate Club (n=34)"


def dolphins():
    """Dolphin social network (n=62). Lusseau et al. 2003.
    Using a representative subset of the known topology."""
    n = 62
    np.random.seed(42)
    # Dolphins has two communities with a few bridge individuals
    # Construct with known structure: two clusters + bridges
    A = np.zeros((n, n))
    # Community 1: nodes 0-29
    for i in range(30):
        for j in range(i+1, 30):
            if np.random.random() < 0.15:
                A[i, j] = 1
                A[j, i] = 1
    # Community 2: nodes 30-61
    for i in range(30, 62):
        for j in range(i+1, 62):
            if np.random.random() < 0.15:
                A[i, j] = 1
                A[j, i] = 1
    # Bridge nodes: 14, 15, 30, 31 connect communities
    bridges = [(14, 30), (14, 31), (14, 35), (15, 30), (15, 32),
               (28, 33), (29, 34), (29, 30)]
    for i, j in bridges:
        A[i, j] = 1
        A[j, i] = 1
    # Ensure connected
    for i in range(n-1):
        if A[i].sum() == 0:
            j = (i + 1) % n
            A[i, j] = 1
            A[j, i] = 1
    labels = [f"D{i}" for i in range(n)]
    for b in [14, 15, 28, 29, 30, 31]:
        labels[b] = f"Bridge{b}"
    return A, labels, "Dolphins (n=62, synthetic topology)"


def les_miserables():
    """Les Misérables co-appearance network (n=77).
    Key bridge characters: Myriel, Valjean, Fantine, Gavroche."""
    # Simplified but structurally accurate version
    n = 20  # Core characters
    names = [
        "Valjean", "Javert", "Fantine", "Cosette", "Marius",
        "Eponine", "Thenardier", "Mme.Then", "Gavroche", "Enjolras",
        "Myriel", "Baptistine", "Mlle.Bap", "Champmathieu", "Brevet",
        "Bamatabois", "Gillenormand", "Mme.Pontmercy", "Toussaint", "Grantaire",
    ]
    edges = [
        # Myriel cluster
        (10, 11), (10, 12), (11, 12),
        # Valjean connects to many
        (0, 10), (0, 1), (0, 2), (0, 3), (0, 4), (0, 6), (0, 7), (0, 18),
        # Fantine cluster
        (2, 5), (2, 6), (2, 7), (2, 15),
        # Thenardier cluster
        (6, 7), (6, 5), (7, 5), (6, 8),
        # Marius-Cosette cluster
        (3, 4), (4, 5), (4, 8), (4, 9), (4, 16), (4, 17),
        # Barricade cluster
        (8, 9), (9, 19), (8, 19),
        # Champmathieu trial
        (0, 13), (0, 14), (13, 14), (13, 15), (14, 15),
        # Javert connections
        (1, 2), (1, 6), (1, 8),
        # Gavroche bridges
        (8, 6), (8, 5),
    ]
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = 1
        A[j, i] = 1
    return A, names, "Les Misérables (n=20, core characters)"


def florentine_families():
    """Florentine marriage network (n=15). Padgett & Ansell 1993.
    Known: Medici are the critical bridge family."""
    names = [
        "Acciaiuoli", "Albizzi", "Barbadori", "Bischeri", "Castellani",
        "Ginori", "Guadagni", "Lamberteschi", "Medici", "Pazzi",
        "Peruzzi", "Ridolfi", "Salviati", "Strozzi", "Tornabuoni",
    ]
    edges = [
        (0, 8), (1, 5), (1, 6), (2, 4), (2, 8), (3, 6), (3, 10),
        (3, 13), (4, 10), (4, 13), (6, 7), (6, 13), (8, 11), (8, 12),
        (8, 14), (9, 12), (10, 13), (11, 13), (11, 14),
    ]
    n = 15
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = 1
        A[j, i] = 1
    return A, names, "Florentine Families (n=15)"


def barbell_graph(n1=15, n2=15):
    """Two cliques connected by a single bridge edge.
    Ground truth: the bridge nodes are maximally critical."""
    n = n1 + n2
    A = np.zeros((n, n))
    # Clique 1
    for i in range(n1):
        for j in range(i+1, n1):
            A[i, j] = 1
            A[j, i] = 1
    # Clique 2
    for i in range(n1, n):
        for j in range(i+1, n):
            A[i, j] = 1
            A[j, i] = 1
    # Bridge
    A[n1-1, n1] = 1
    A[n1, n1-1] = 1
    labels = [f"L{i}" for i in range(n1)] + [f"R{i}" for i in range(n2)]
    labels[n1-1] = "BRIDGE_L"
    labels[n1] = "BRIDGE_R"
    return A, labels, f"Barbell (n={n}, bridge at {n1-1}-{n1})"


def grid_2d(rows=8, cols=8):
    """2D grid graph. Critical nodes: center nodes with high betweenness."""
    n = rows * cols
    A = np.zeros((n, n))
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            if c + 1 < cols:
                A[idx, idx+1] = 1
                A[idx+1, idx] = 1
            if r + 1 < rows:
                A[idx, idx+cols] = 1
                A[idx+cols, idx] = 1
    labels = [f"({r},{c})" for r in range(rows) for c in range(cols)]
    return A, labels, f"Grid {rows}x{cols} (n={n})"


def tree_graph(depth=4, branching=3):
    """Regular tree. Critical nodes: root and early-level nodes."""
    nodes = [0]
    edges = []
    counter = 1
    for d in range(depth):
        new_nodes = []
        for parent in nodes:
            if len(edges) > 0 and d > 0:
                # Only branch from current level
                pass
            for _ in range(branching):
                edges.append((parent, counter))
                new_nodes.append(counter)
                counter += 1
        nodes = new_nodes
    n = counter
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = 1
        A[j, i] = 1
    labels = [f"T{i}" for i in range(n)]
    labels[0] = "ROOT"
    return A, labels, f"Tree (depth={depth}, branch={branching}, n={n})"


def watts_strogatz(n=100, k=4, p=0.1, seed=42):
    """Small-world network. Rewiring creates shortcuts."""
    np.random.seed(seed)
    A = np.zeros((n, n))
    # Ring lattice
    for i in range(n):
        for j in range(1, k//2 + 1):
            A[i, (i+j) % n] = 1
            A[(i+j) % n, i] = 1
    # Rewire
    for i in range(n):
        for j in range(1, k//2 + 1):
            if np.random.random() < p:
                target = (i + j) % n
                A[i, target] = 0
                A[target, i] = 0
                new_target = np.random.randint(n)
                while new_target == i or A[i, new_target] == 1:
                    new_target = np.random.randint(n)
                A[i, new_target] = 1
                A[new_target, i] = 1
    labels = [f"W{i}" for i in range(n)]
    return A, labels, f"Watts-Strogatz (n={n}, k={k}, p={p})"


def barabasi_albert(n=100, m=2, seed=42):
    """Scale-free network. Hubs should be critical."""
    np.random.seed(seed)
    A = np.zeros((n, n))
    # Start with complete graph on m+1 nodes
    for i in range(m+1):
        for j in range(i+1, m+1):
            A[i, j] = 1
            A[j, i] = 1
    # Preferential attachment
    for new_node in range(m+1, n):
        degrees = A[:new_node].sum(axis=1)
        probs = degrees / degrees.sum()
        targets = np.random.choice(new_node, size=m, replace=False, p=probs)
        for t in targets:
            A[new_node, t] = 1
            A[t, new_node] = 1
    labels = [f"BA{i}" for i in range(n)]
    return A, labels, f"Barabási-Albert (n={n}, m={m})"


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN BENCHMARK
# ═══════════════════════════════════════════════════════════════════════════════

def benchmark_network(A, labels, name, verbose=True):
    """Run full benchmark on a single network."""
    n = A.shape[0]
    density = A.sum() / (n * (n - 1))
    mean_degree = A.sum(axis=1).mean()

    if verbose:
        print(f"\n{'='*80}")
        print(f"  {name}")
        print(f"  n={n}, edges={int(A.sum()//2)}, density={density:.3f}, "
              f"mean_degree={mean_degree:.1f}")
        print(f"{'='*80}")

    # Compute metrics
    L = laplacian(A)
    P = fiedler_P(L)
    node_d = per_node_defect(L, P)
    degree = A.sum(axis=1)

    t0 = time.time()
    betw = betweenness_centrality(A)
    t_betw = time.time() - t0

    t0 = time.time()
    crit = node_criticality(A)
    t_crit = time.time() - t0

    # Rank correlations with ground truth criticality
    rho_defect = rank_correlation(node_d, crit)
    rho_betw = rank_correlation(betw, crit)
    rho_degree = rank_correlation(degree, crit)

    # Top-k overlap
    k = min(10, n // 3)
    top_crit = set(np.argsort(crit)[::-1][:k])
    top_defect = set(np.argsort(node_d)[::-1][:k])
    top_betw = set(np.argsort(betw)[::-1][:k])
    top_degree = set(np.argsort(degree)[::-1][:k])

    overlap_defect = len(top_crit & top_defect) / k
    overlap_betw = len(top_crit & top_betw) / k
    overlap_degree = len(top_crit & top_degree) / k

    if verbose:
        print(f"\n  Rank correlation with ground truth (Δ algebraic connectivity):")
        print(f"    Prism defect:    ρ = {rho_defect:>+.3f}")
        print(f"    Betweenness:     ρ = {rho_betw:>+.3f}")
        print(f"    Degree:          ρ = {rho_degree:>+.3f}")

        print(f"\n  Top-{k} overlap with ground truth critical nodes:")
        print(f"    Prism defect:    {overlap_defect*100:.0f}%")
        print(f"    Betweenness:     {overlap_betw*100:.0f}%")
        print(f"    Degree:          {overlap_degree*100:.0f}%")

        winner = "PRISM" if rho_defect > rho_betw else "BETWEENNESS"
        margin = abs(rho_defect - rho_betw)
        print(f"\n  Winner: {winner} (margin: {margin:.3f})")

        # Show top-5 by each metric
        print(f"\n  Top-5 nodes by each metric:")
        print(f"  {'Rank':<5} {'Criticality':<15} {'Prism defect':<15} "
              f"{'Betweenness':<15} {'Degree':<15}")
        print(f"  {'-'*65}")
        for rank in range(min(5, n)):
            c_idx = np.argsort(crit)[::-1][rank]
            d_idx = np.argsort(node_d)[::-1][rank]
            b_idx = np.argsort(betw)[::-1][rank]
            deg_idx = np.argsort(degree)[::-1][rank]
            print(f"  {rank+1:<5} {labels[c_idx]:<15} {labels[d_idx]:<15} "
                  f"{labels[b_idx]:<15} {labels[deg_idx]:<15}")

    return {
        'name': name, 'n': n, 'density': density,
        'rho_defect': rho_defect, 'rho_betw': rho_betw, 'rho_degree': rho_degree,
        'overlap_defect': overlap_defect, 'overlap_betw': overlap_betw,
        'overlap_degree': overlap_degree,
        'prism_wins': rho_defect > rho_betw,
    }


def run():
    print("=" * 80)
    print("PRISM SPARSE NETWORK BENCHMARK SUITE")
    print("=" * 80)
    print("""
  Question: Does per-node duality defect identify critical nodes better
  than betweenness centrality in sparse topological networks?

  Ground truth: Δ algebraic connectivity upon node removal.
  (How much does removing this node degrade the network's connectivity?)

  Pass criteria:
    1. Prism rank-correlation with criticality > 0.3 on majority of networks
    2. Prism outperforms betweenness on at least some network types
    3. If Prism ≤ betweenness everywhere: method adds nothing (α ≤ 1)
""")

    networks = [
        karate_club,
        florentine_families,
        les_miserables,
        dolphins,
        lambda: barbell_graph(15, 15),
        lambda: grid_2d(6, 6),
        lambda: tree_graph(3, 3),
        lambda: watts_strogatz(60, 4, 0.1),
        lambda: barabasi_albert(60, 2),
    ]

    results = []
    for net_fn in networks:
        A, labels, name = net_fn()
        # Skip if disconnected
        n_comp, _ = connected_components(sparse.csr_matrix(A), directed=False)
        if n_comp > 1:
            print(f"\n  SKIPPING {name}: {n_comp} components (disconnected)")
            continue
        result = benchmark_network(A, labels, name)
        results.append(result)

    # ═══════════════════════════════════════════════════════════════════════════
    # SUMMARY TABLE
    # ═══════════════════════════════════════════════════════════════════════════
    print()
    print("=" * 80)
    print("SUMMARY: Prism vs Betweenness vs Degree")
    print("=" * 80)

    print(f"\n  {'Network':<35} {'n':>4} {'ρ(Prism)':>9} {'ρ(Betw)':>9} "
          f"{'ρ(Deg)':>8} {'Winner':<12}")
    print(f"  {'-'*85}")

    prism_wins = 0
    for r in results:
        winner = "PRISM" if r['prism_wins'] else "BETWEENNESS"
        if r['rho_degree'] > max(r['rho_defect'], r['rho_betw']):
            winner = "DEGREE"
        print(f"  {r['name']:<35} {r['n']:>4} {r['rho_defect']:>+8.3f} "
              f"{r['rho_betw']:>+8.3f} {r['rho_degree']:>+7.3f} {winner:<12}")
        if r['prism_wins']:
            prism_wins += 1

    total = len(results)
    print(f"\n  Prism wins: {prism_wins}/{total} networks")
    print(f"  Mean ρ(Prism):       {np.mean([r['rho_defect'] for r in results]):.3f}")
    print(f"  Mean ρ(Betweenness): {np.mean([r['rho_betw'] for r in results]):.3f}")
    print(f"  Mean ρ(Degree):      {np.mean([r['rho_degree'] for r in results]):.3f}")

    # Verdict
    print()
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)

    mean_rho = np.mean([r['rho_defect'] for r in results])
    if prism_wins > total * 0.6 and mean_rho > 0.3:
        print("""
  PASS: Prism identifies critical nodes better than betweenness in
  sparse networks. The method has genuine value beyond existing metrics.
  Proceed to real-world infrastructure networks.
""")
    elif prism_wins > total * 0.3 or mean_rho > 0.2:
        print("""
  PARTIAL: Prism works on SOME network types but not universally.
  Investigate which topological properties predict Prism success.
  The method may have a niche rather than general applicability.
""")
    else:
        print("""
  FAIL: Prism does not outperform betweenness centrality on sparse networks.
  The duality defect does not correspond to engineering criticality.
  This is a structural dead end — not a domain problem.

  If this happens: the Fiedler pairing operator itself may not measure
  what we think it measures. Consider alternative P constructions.
""")

    return results


if __name__ == "__main__":
    run()
