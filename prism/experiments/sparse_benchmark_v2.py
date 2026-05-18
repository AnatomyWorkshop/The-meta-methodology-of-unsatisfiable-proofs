"""
Sparse Benchmark v2: What does Prism ACTUALLY measure?

v1 showed Prism loses to betweenness on Δ-algebraic-connectivity.
But Prism's ρ was 0.3-0.55 on most networks — it's measuring SOMETHING.

Hypothesis: Prism measures SYMMETRY-BREAKING criticality, not
path-based criticality. These are different structural properties:

  - Betweenness: "how many shortest paths go through this node?"
    → measures flow/routing importance
  - Degree: "how many connections does this node have?"
    → measures local connectivity
  - Prism defect: "how much does this node break the spectral duality?"
    → measures... what exactly?

This experiment tests multiple alternative ground truths:
  1. Δ algebraic connectivity (v1's metric — betweenness wins)
  2. Δ modularity upon removal (community structure disruption)
  3. Spectral gap sensitivity (how much eigenvalue spacing changes)
  4. Symmetry breaking: does the node sit at a community boundary?
  5. Fiedler cut contribution: is the node on the spectral bisection?

If Prism correlates best with (4) or (5), it's measuring something
genuinely different from betweenness — just not "criticality" in the
engineering sense. That would reframe the product direction.
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


def betweenness_centrality_fast(A):
    """Approximate betweenness using BFS from all nodes."""
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
    betweenness /= ((n - 1) * (n - 2) / 2 + 1e-10)
    return betweenness


# ═══════════════════════════════════════════════════════════════════════════════
# ALTERNATIVE GROUND TRUTHS
# ═══════════════════════════════════════════════════════════════════════════════

def gt_algebraic_connectivity(A):
    """Standard: how much does removing node i reduce λ₂?"""
    n = A.shape[0]
    L = laplacian(A)
    base = np.linalg.eigvalsh(L)[1]
    scores = np.zeros(n)
    for i in range(n):
        mask = np.ones(n, dtype=bool)
        mask[i] = False
        A_r = A[mask][:, mask]
        if A_r.shape[0] < 3:
            scores[i] = base
            continue
        L_r = laplacian(A_r)
        scores[i] = base - np.linalg.eigvalsh(L_r)[1]
    return scores


def gt_fiedler_cut_proximity(A):
    """How close is each node to the Fiedler bisection boundary?
    Nodes near the cut (Fiedler value ≈ 0) are at the community boundary."""
    L = laplacian(A)
    _, evecs = np.linalg.eigh(L)
    fiedler = evecs[:, 1]
    # Proximity to cut = inverse of |fiedler value|
    # Nodes at the boundary have fiedler ≈ 0
    return 1.0 / (np.abs(fiedler) + 0.01)


def gt_cross_cut_edges(A):
    """Number of edges each node has that cross the Fiedler cut.
    Nodes with many cross-cut edges are boundary nodes."""
    L = laplacian(A)
    _, evecs = np.linalg.eigh(L)
    fiedler = evecs[:, 1]
    side = (fiedler >= 0).astype(int)
    n = A.shape[0]
    scores = np.zeros(n)
    for i in range(n):
        for j in range(n):
            if A[i, j] > 0 and side[i] != side[j]:
                scores[i] += 1
    return scores


def gt_spectral_gap_sensitivity(A):
    """How much does removing node i change the spectral gap (λ₃ - λ₂)?"""
    n = A.shape[0]
    L = laplacian(A)
    evals = np.linalg.eigvalsh(L)
    base_gap = evals[2] - evals[1] if n > 2 else 0
    scores = np.zeros(n)
    for i in range(n):
        mask = np.ones(n, dtype=bool)
        mask[i] = False
        A_r = A[mask][:, mask]
        if A_r.shape[0] < 4:
            scores[i] = 0
            continue
        L_r = laplacian(A_r)
        evals_r = np.linalg.eigvalsh(L_r)
        new_gap = evals_r[2] - evals_r[1]
        scores[i] = abs(base_gap - new_gap)
    return scores


def gt_community_boundary(A):
    """Spectral clustering boundary score.
    Use first k eigenvectors, measure how much node i sits between clusters."""
    n = A.shape[0]
    L = laplacian(A)
    _, evecs = np.linalg.eigh(L)
    # Use eigenvectors 1 and 2 for embedding
    k = min(3, n - 1)
    embedding = evecs[:, 1:k+1]
    # For each node, measure variance of neighbor embeddings
    scores = np.zeros(n)
    for i in range(n):
        neighbors = np.where(A[i] > 0)[0]
        if len(neighbors) < 2:
            continue
        neighbor_embeddings = embedding[neighbors]
        # Variance of neighbor positions = how much this node bridges clusters
        scores[i] = np.var(neighbor_embeddings)
    return scores


def gt_pairing_distance(A):
    """How far apart (in graph distance) is each node from its Fiedler pair?
    If the pair is far, the duality is "stretched" at this node."""
    n = A.shape[0]
    L = laplacian(A)
    _, evecs = np.linalg.eigh(L)
    fiedler = evecs[:, 1]
    order = np.argsort(fiedler)
    # Compute graph distances
    dist = sparse.csgraph.shortest_path(sparse.csr_matrix(A), directed=False)
    scores = np.zeros(n)
    for rank, node in enumerate(order):
        partner = order[n - 1 - rank]
        if not np.isinf(dist[node, partner]):
            scores[node] = dist[node, partner]
        else:
            scores[node] = n  # disconnected pair
    return scores


# ═══════════════════════════════════════════════════════════════════════════════
# NETWORKS (reuse from v1)
# ═══════════════════════════════════════════════════════════════════════════════

def karate_club():
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
        A[i, j] = 1; A[j, i] = 1
    return A, "Karate Club"


def florentine():
    edges = [
        (0, 8), (1, 5), (1, 6), (2, 4), (2, 8), (3, 6), (3, 10),
        (3, 13), (4, 10), (4, 13), (6, 7), (6, 13), (8, 11), (8, 12),
        (8, 14), (9, 12), (10, 13), (11, 13), (11, 14),
    ]
    n = 15
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = 1; A[j, i] = 1
    names = ["Acciaiuoli","Albizzi","Barbadori","Bischeri","Castellani",
             "Ginori","Guadagni","Lamberteschi","Medici","Pazzi",
             "Peruzzi","Ridolfi","Salviati","Strozzi","Tornabuoni"]
    return A, "Florentine Families"


def barbell(n1=15, n2=15):
    n = n1 + n2
    A = np.zeros((n, n))
    for i in range(n1):
        for j in range(i+1, n1):
            A[i,j] = 1; A[j,i] = 1
    for i in range(n1, n):
        for j in range(i+1, n):
            A[i,j] = 1; A[j,i] = 1
    A[n1-1, n1] = 1; A[n1, n1-1] = 1
    return A, "Barbell"


def watts_strogatz(n=60, k=4, p=0.1, seed=42):
    np.random.seed(seed)
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(1, k//2 + 1):
            A[i, (i+j)%n] = 1; A[(i+j)%n, i] = 1
    for i in range(n):
        for j in range(1, k//2 + 1):
            if np.random.random() < p:
                target = (i+j) % n
                A[i, target] = 0; A[target, i] = 0
                new_t = np.random.randint(n)
                while new_t == i or A[i, new_t] == 1:
                    new_t = np.random.randint(n)
                A[i, new_t] = 1; A[new_t, i] = 1
    return A, "Watts-Strogatz"


def barabasi_albert(n=60, m=2, seed=42):
    np.random.seed(seed)
    A = np.zeros((n, n))
    for i in range(m+1):
        for j in range(i+1, m+1):
            A[i,j] = 1; A[j,i] = 1
    for new in range(m+1, n):
        deg = A[:new].sum(axis=1)
        probs = deg / deg.sum()
        targets = np.random.choice(new, size=m, replace=False, p=probs)
        for t in targets:
            A[new, t] = 1; A[t, new] = 1
    return A, "Barabási-Albert"


def grid_2d(rows=6, cols=6):
    n = rows * cols
    A = np.zeros((n, n))
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            if c+1 < cols: A[idx, idx+1] = 1; A[idx+1, idx] = 1
            if r+1 < rows: A[idx, idx+cols] = 1; A[idx+cols, idx] = 1
    return A, f"Grid {rows}x{cols}"


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_network(A, name):
    """Test what Prism actually correlates with."""
    n = A.shape[0]
    L = laplacian(A)
    P, fiedler_vec = fiedler_P(L)
    node_d = per_node_defect(L, P)
    betw = betweenness_centrality_fast(A)
    degree = A.sum(axis=1)

    # Compute all ground truths
    gt_names = []
    gt_scores = []

    print(f"\n  Computing ground truths for {name} (n={n})...", end=" ", flush=True)
    t0 = time.time()

    gts = {
        'Δ_connectivity': gt_algebraic_connectivity(A),
        'fiedler_cut_prox': gt_fiedler_cut_proximity(A),
        'cross_cut_edges': gt_cross_cut_edges(A),
        'spectral_gap_Δ': gt_spectral_gap_sensitivity(A),
        'community_boundary': gt_community_boundary(A),
        'pairing_distance': gt_pairing_distance(A),
    }
    print(f"{time.time()-t0:.1f}s")

    # Correlations
    results = {}
    for gt_name, gt_vals in gts.items():
        if np.std(gt_vals) < 1e-10:
            results[gt_name] = {'prism': np.nan, 'betw': np.nan, 'degree': np.nan}
            continue
        rho_p, _ = spearmanr(node_d, gt_vals)
        rho_b, _ = spearmanr(betw, gt_vals)
        rho_d, _ = spearmanr(degree, gt_vals)
        results[gt_name] = {'prism': rho_p, 'betw': rho_b, 'degree': rho_d}

    return results


def run():
    print("=" * 80)
    print("WHAT DOES PRISM ACTUALLY MEASURE?")
    print("=" * 80)
    print("""
  v1 showed Prism loses to betweenness on "criticality" (Δ connectivity).
  But Prism ρ was 0.3-0.55 — it measures SOMETHING structural.

  This experiment tests: what ground truth does Prism correlate with BEST?
  If Prism best correlates with fiedler_cut_proximity or cross_cut_edges,
  it's measuring BOUNDARY position, not criticality.

  That would mean: Prism identifies nodes at community boundaries,
  not nodes whose removal degrades the network. Different product.
""")

    networks = [
        karate_club,
        florentine,
        lambda: barbell(12, 12),
        lambda: grid_2d(6, 6),
        lambda: watts_strogatz(50, 4, 0.1),
        lambda: barabasi_albert(50, 2),
    ]

    all_results = {}
    for net_fn in networks:
        A, name = net_fn()
        n_comp, _ = connected_components(sparse.csr_matrix(A), directed=False)
        if n_comp > 1:
            print(f"\n  SKIP {name}: disconnected")
            continue
        results = analyze_network(A, name)
        all_results[name] = results

    # ═══════════════════════════════════════════════════════════════════════════
    # RESULTS TABLE
    # ═══════════════════════════════════════════════════════════════════════════
    print()
    print("=" * 80)
    print("CORRELATION MATRIX: What does each metric measure?")
    print("=" * 80)

    gt_names = ['Δ_connectivity', 'fiedler_cut_prox', 'cross_cut_edges',
                'spectral_gap_Δ', 'community_boundary', 'pairing_distance']

    for net_name, results in all_results.items():
        print(f"\n  {net_name}:")
        print(f"  {'Ground Truth':<22} {'ρ(Prism)':>9} {'ρ(Betw)':>9} {'ρ(Deg)':>8}  Best")
        print(f"  {'-'*65}")
        for gt in gt_names:
            if gt not in results:
                continue
            r = results[gt]
            vals = {'Prism': r['prism'], 'Betw': r['betw'], 'Deg': r['degree']}
            valid_vals = {k: v for k, v in vals.items() if not np.isnan(v)}
            best = max(valid_vals, key=lambda k: abs(valid_vals[k])) if valid_vals else "N/A"
            print(f"  {gt:<22} {r['prism']:>+8.3f} {r['betw']:>+8.3f} "
                  f"{r['degree']:>+7.3f}  {best}")

    # ═══════════════════════════════════════════════════════════════════════════
    # AGGREGATE: Where does Prism win?
    # ═══════════════════════════════════════════════════════════════════════════
    print()
    print("=" * 80)
    print("AGGREGATE: On which ground truth does Prism perform best?")
    print("=" * 80)

    gt_prism_avg = {gt: [] for gt in gt_names}
    gt_betw_avg = {gt: [] for gt in gt_names}
    gt_prism_wins = {gt: 0 for gt in gt_names}

    for net_name, results in all_results.items():
        for gt in gt_names:
            if gt not in results:
                continue
            r = results[gt]
            if not np.isnan(r['prism']):
                gt_prism_avg[gt].append(abs(r['prism']))
            if not np.isnan(r['betw']):
                gt_betw_avg[gt].append(abs(r['betw']))
            if not np.isnan(r['prism']) and not np.isnan(r['betw']):
                if abs(r['prism']) > abs(r['betw']):
                    gt_prism_wins[gt] += 1

    print(f"\n  {'Ground Truth':<22} {'Mean|ρ|(Prism)':>15} {'Mean|ρ|(Betw)':>15} "
          f"{'Prism wins':>11}")
    print(f"  {'-'*70}")
    for gt in gt_names:
        p_avg = np.mean(gt_prism_avg[gt]) if gt_prism_avg[gt] else np.nan
        b_avg = np.mean(gt_betw_avg[gt]) if gt_betw_avg[gt] else np.nan
        total = len(gt_prism_avg[gt])
        marker = " ← PRISM NICHE" if gt_prism_wins[gt] > total * 0.5 else ""
        print(f"  {gt:<22} {p_avg:>14.3f} {b_avg:>14.3f} "
              f"{gt_prism_wins[gt]}/{total:<8}{marker}")

    # ═══════════════════════════════════════════════════════════════════════════
    # VERDICT
    # ═══════════════════════════════════════════════════════════════════════════
    print()
    print("=" * 80)
    print("INTERPRETATION")
    print("=" * 80)
    print("""
  If Prism best correlates with fiedler_cut_proximity or cross_cut_edges:
    → Prism measures BOUNDARY POSITION (nodes between communities)
    → Product: community boundary detection, not criticality
    → Reframe: "structural fault line identifier"

  If Prism best correlates with pairing_distance:
    → Prism measures DUALITY STRETCH (how far apart paired nodes are)
    → This is tautological — defect IS the commutator of L and P
    → No independent product value

  If Prism best correlates with spectral_gap_sensitivity:
    → Prism measures SPECTRAL STRUCTURE sensitivity
    → Potentially useful for detecting phase transitions
    → Product: early warning for structural regime change

  If Prism doesn't clearly win on ANY ground truth:
    → The per-node decomposition is a noisy, inferior version of betweenness
    → Structural dead end for per-node attribution
    → Only the GLOBAL defect (scalar) has value
""")


if __name__ == "__main__":
    run()
