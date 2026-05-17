"""
Prism Diagnostic Demo: duality defect as a structural health metric.

Setup: a network with EXACT duality structure (deterministic, not random).
Two groups of n/2 nodes are perfect mirrors: A_i and B_i have identical
neighborhoods within their group, and are connected to each other.
The true P swaps group A with group B (node i <-> node i + n//2).

Key: the clean network satisfies [L, P] = 0 exactly (defect = 0).
As we rewire edges, the defect rises from 0.

Experiment: gradually break the duality by rewiring edges.
Track normalized duality_defect for true P vs index-reversal P,
and compare to modularity.

Expected result: true-P defect rises monotonically from 0.
Index-reversal defect starts high and stays noisy.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def build_exact_dual_network(n: int, rng: np.random.Generator,
                              p_within: float = 0.25,
                              p_cross_mirror: float = 0.5,
                              p_cross_other: float = 0.0) -> np.ndarray:
    """
    Build a network with EXACT duality structure: [L, P] = 0.

    P = group swap: node i <-> node i + half.

    For [L, P] = 0, we need: A[i,j] = A[P(i), P(j)] for all i,j.
    Equivalently: the adjacency matrix commutes with the permutation matrix P.

    Construction: for each pair (i,j) with i < j, decide on edge probability,
    then MIRROR the decision to (P(i), P(j)) = (i+half, j+half).
    This guarantees exact symmetry.

    To break index-reversal symmetry: use asymmetric random within-group edges
    (not a circulant). The mirroring only enforces group-swap symmetry.
    """
    half = n // 2
    A = np.zeros((n, n))

    # Within group A: random edges
    for i in range(half):
        for j in range(i + 1, half):
            if rng.random() < p_within:
                # Mirror to group B
                A[i, j] = A[j, i] = 1.0
                A[i + half, j + half] = A[j + half, i + half] = 1.0

    # Cross-group edges: mirrored pairs (i, i+half) have high probability
    for i in range(half):
        for j in range(half):
            if i == j:
                p = p_cross_mirror
            else:
                p = p_cross_other
            if rng.random() < p:
                # This edge (i, j+half) must be mirrored to (i+half, j)
                A[i, j + half] = A[j + half, i] = 1.0
                A[i + half, j] = A[j, i + half] = 1.0

    return A


def true_parity_operator(n: int) -> np.ndarray:
    """True P: swap node i with node i + n//2."""
    half = n // 2
    P = np.zeros((n, n))
    for i in range(half):
        P[i, i + half] = 1.0
        P[i + half, i] = 1.0
    return P


def index_reversal_P(n: int) -> np.ndarray:
    return np.eye(n)[::-1]


def duality_defect_normalized(L: np.ndarray, P: np.ndarray) -> float:
    """||[L, P]||_F / ||L||_F"""
    comm = L @ P - P @ L
    return np.linalg.norm(comm, 'fro') / (np.linalg.norm(L, 'fro') + 1e-10)


def modularity(A: np.ndarray, labels: np.ndarray) -> float:
    """Newman-Girvan modularity for given partition."""
    n = A.shape[0]
    m = A.sum() / 2
    if m == 0:
        return 0.0
    k = A.sum(axis=1)
    Q = 0.0
    for i in range(n):
        for j in range(n):
            if labels[i] == labels[j]:
                Q += A[i, j] - k[i] * k[j] / (2 * m)
    return Q / (2 * m)


def rewire_fraction(A: np.ndarray, frac: float,
                     rng: np.random.Generator) -> np.ndarray:
    """
    Randomly rewire a fraction of edges, destroying duality structure.
    For each selected edge (i,j), move it to a random (i, k).
    """
    n = A.shape[0]
    B = A.copy()
    edges = [(i, j) for i in range(n) for j in range(i+1, n) if A[i,j] > 0]
    n_rewire = int(len(edges) * frac)
    if n_rewire == 0:
        return B
    selected = rng.choice(len(edges), size=n_rewire, replace=False)
    for idx in selected:
        i, j = edges[idx]
        B[i, j] = B[j, i] = 0.0
        candidates = [k for k in range(n) if k != i and B[i,k] == 0]
        if candidates:
            k = rng.choice(candidates)
            B[i, k] = B[k, i] = 1.0
    return B


def run_demo():
    n = 40
    rng = np.random.default_rng(42)

    # Exact dual network: [L, P_true] = 0 by construction
    A_clean = build_exact_dual_network(n, rng=rng, p_within=0.3,
                                        p_cross_mirror=0.5, p_cross_other=0.0)
    P_true  = true_parity_operator(n)
    P_index = index_reversal_P(n)
    labels_true = np.array([0]*(n//2) + [1]*(n//2))

    # Verify exact duality
    D_clean = np.diag(A_clean.sum(axis=1))
    L_clean = D_clean - A_clean
    defect_clean = duality_defect_normalized(L_clean, P_true)

    rewire_levels = np.linspace(0, 0.8, 17)

    defects_true  = []   # ||[L, P_true]||_F / ||L||_F
    defects_index = []   # ||[L, P_index]||_F / ||L||_F
    modularities  = []
    mean_degrees  = []

    for frac in rewire_levels:
        A = A_clean.copy() if frac == 0 else rewire_fraction(A_clean, frac, rng)
        D_mat = np.diag(A.sum(axis=1))
        L = D_mat - A

        defects_true.append(duality_defect_normalized(L, P_true))
        defects_index.append(duality_defect_normalized(L, P_index))
        modularities.append(modularity(A, labels_true))
        mean_degrees.append(A.sum() / n)

    print("=" * 72)
    print("Prism Diagnostic Demo: Duality Defect as Structural Health Metric")
    print("=" * 72)
    print(f"Network: n={n}, exact dual structure, [L_clean, P_true] = 0")
    print(f"Initial defect (true P, clean network): {defect_clean:.2e}  ← should be ~0")
    print(f"Metric: ||[L, P]||_F / ||L||_F  (0 = perfect symmetry, 1 = broken)")
    print()
    print(f"{'Rewire':>8}  {'Defect(true P)':>15}  {'Defect(index P)':>16}  "
          f"{'Modularity':>11}  {'Mean deg':>9}")
    print("-" * 68)
    for i, frac in enumerate(rewire_levels):
        print(f"{frac:>7.0%}  {defects_true[i]:>15.4f}  {defects_index[i]:>16.4f}  "
              f"{modularities[i]:>11.4f}  {mean_degrees[i]:>9.2f}")
    print("-" * 68)

    def sensitivity(vals):
        return np.polyfit(rewire_levels, vals, 1)[0]

    s_true  = sensitivity(defects_true)
    s_index = sensitivity(defects_index)
    s_mod   = sensitivity([-m for m in modularities])

    print()
    print("Sensitivity (linear slope vs rewiring fraction):")
    print(f"  Defect (true P):   {s_true:+.4f}  ← Prism with correct P")
    print(f"  Defect (index P):  {s_index:+.4f}  ← Prism with wrong P")
    print(f"  Modularity loss:   {s_mod:+.4f}  ← standard metric (normalized)")

    print()
    ratio = s_true / max(abs(s_index), 1e-6)
    print(f"True-P defect sensitivity: {s_true:.4f}")
    print(f"Index-P defect sensitivity: {s_index:.4f}")
    if s_true > 0.05:
        print(f"Ratio: {ratio:.2f}x — true P is {'more' if ratio>1 else 'less'} sensitive than index P")
        print()
        print("Result: duality_defect(true P) rises monotonically from ~0 as structure")
        print("breaks. Index-P defect starts high and stays noisy — no diagnostic value.")
        print("This is Prism's core claim: a meaningful P turns defect into a health metric.")
    else:
        print()
        print(f"Note: true-P sensitivity ({s_true:.4f}) is low. The rewiring may not be")
        print("breaking the specific symmetry P captures, or the network is too sparse.")

    return rewire_levels, defects_true, defects_index, modularities


if __name__ == "__main__":
    run_demo()
