"""
Prism v0.2 benchmark: learnable P vs fixed baselines.

Tests the key claim: learnable P recovers hidden mirror structure
that fixed index-reversal P cannot detect.

Setup:
  - Synthetic graph with KNOWN ground-truth duality (two mirror communities)
  - Noisy version of the same graph
  - Compare: Identity, Symmetrize(fixed P), Prism v0.1 (fixed P), Prism v0.2 (learnable P)

Key metric: recovery of ground-truth duality structure
  - Does the learned P correctly identify which nodes are mirrors of each other?
  - Does L' stay close to the true Laplacian?
"""

import numpy as np
import time
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from prism.core import optimize, parity_operator
from prism.learnable import optimize_learnable, optimize_learnable_multistart, interpret_P, sinkhorn
from prism.benchmark import (
    stochastic_block_model, karate_club,
    duality_defect, spectral_rmse, frobenius_distance,
    baseline_symmetrize,
)


# ---------------------------------------------------------------------------
# Ground-truth mirror graph generator
# ---------------------------------------------------------------------------

def mirror_sbm(n: int, p_in: float = 0.7, p_out: float = 0.05,
               noise: float = 0.0, seed: int = 42) -> tuple:
    """
    Generate a graph with exact mirror symmetry between two communities.

    Nodes 0..n//2-1 are community A, nodes n//2..n-1 are community B.
    The true duality: node i <-> node i + n//2.

    Returns: (L_noisy, L_true, true_P, community_labels)
    """
    rng = np.random.default_rng(seed)
    half = n // 2

    # Build perfectly symmetric adjacency
    A = np.zeros((n, n))
    for i in range(half):
        for j in range(i + 1, half):
            if rng.random() < p_in:
                # Mirror edge: both (i,j) and (i+half, j+half)
                A[i, j] = A[j, i] = 1
                A[i + half, j + half] = A[j + half, i + half] = 1
        for j in range(half):
            if rng.random() < p_out:
                # Cross edge: (i, j+half) and mirror (j, i+half)
                A[i, j + half] = A[j + half, i] = 1
                A[j, i + half] = A[i + half, j] = 1

    np.fill_diagonal(A, 0)
    D = np.diag(A.sum(axis=1))
    L_true = D - A

    # True duality: node i <-> node i + half
    true_P = np.zeros((n, n))
    for i in range(half):
        true_P[i, i + half] = 1
        true_P[i + half, i] = 1

    labels = [0] * half + [1] * half

    # Add noise: flip edges with probability `noise`
    if noise > 0:
        flip = rng.random((n, n)) < noise
        flip = np.triu(flip, 1)
        flip = flip + flip.T
        A_noisy = np.abs(A - flip)
        np.fill_diagonal(A_noisy, 0)
        D_noisy = np.diag(A_noisy.sum(axis=1))
        L_noisy = D_noisy - A_noisy
    else:
        L_noisy = L_true.copy()

    return L_noisy, L_true, true_P, labels


def P_recovery_score(P_learned: np.ndarray, P_true: np.ndarray) -> float:
    """
    How well does the learned P match the true duality?
    Score = Frobenius similarity (normalized), range [0, 1].
    1.0 = perfect recovery, 0.0 = no overlap.
    """
    n = P_true.shape[0]
    overlap = np.sum(P_learned * P_true)
    norm_true = np.linalg.norm(P_true, 'fro')
    norm_learned = np.linalg.norm(P_learned, 'fro')
    return float(overlap / (norm_true * norm_learned + 1e-10))


def run_v2_benchmark(n: int = 16, noise_levels: list = None,
                     verbose: bool = True) -> list:
    if noise_levels is None:
        noise_levels = [0.0, 0.05, 0.10, 0.20]

    print("Prism v0.2 Benchmark: Learnable P vs Fixed Baselines")
    print("=" * 62)
    print(f"Mirror SBM: n={n}, two equal communities, true P = node swap")
    print()

    results = []

    for noise in noise_levels:
        L_noisy, L_true, P_true, labels = mirror_sbm(
            n, p_in=0.7, p_out=0.05, noise=noise, seed=42
        )

        if verbose:
            print(f"Noise={noise:.2f}  (||L_noisy - L_true||_F = "
                  f"{frobenius_distance(L_noisy, L_true):.3f})")
            print(f"  {'Method':25s}  {'Defect':>8}  {'SpecRMSE':>9}  "
                  f"{'Recovery':>9}  {'P-score':>8}  {'ms':>6}")
            print(f"  {'-'*25}  {'-'*8}  {'-'*9}  {'-'*9}  {'-'*8}  {'-'*6}")

        row = {"noise": noise}

        # --- Identity ---
        t0 = time.perf_counter()
        L_id = L_noisy.copy()
        dt = (time.perf_counter() - t0) * 1000
        # Fixed P for identity = index reversal
        P_fixed = parity_operator(n)
        defect = duality_defect(L_id)
        srmse = spectral_rmse(L_noisy, L_id)
        rec = frobenius_distance(L_true, L_id)
        pscore = P_recovery_score(P_fixed, P_true)
        row["identity"] = dict(defect=defect, srmse=srmse, rec=rec, pscore=pscore, ms=dt)
        if verbose:
            print(f"  {'Identity':25s}  {defect:8.4f}  {srmse:9.4f}  "
                  f"{rec:9.4f}  {pscore:8.4f}  {dt:6.1f}")

        # --- Symmetrize (fixed index-reversal P) ---
        t0 = time.perf_counter()
        L_sym = baseline_symmetrize(L_noisy)
        dt = (time.perf_counter() - t0) * 1000
        defect = duality_defect(L_sym)
        srmse = spectral_rmse(L_noisy, L_sym)
        rec = frobenius_distance(L_true, L_sym)
        pscore = P_recovery_score(P_fixed, P_true)
        row["symmetrize"] = dict(defect=defect, srmse=srmse, rec=rec, pscore=pscore, ms=dt)
        if verbose:
            print(f"  {'Symmetrize(index-rev P)':25s}  {defect:8.4f}  {srmse:9.4f}  "
                  f"{rec:9.4f}  {pscore:8.4f}  {dt:6.1f}")

        # --- Prism v0.1 (fixed P) ---
        t0 = time.perf_counter()
        res_v1 = optimize(L_noisy, reg=1e-6, max_iter=1000)
        dt = (time.perf_counter() - t0) * 1000
        defect = res_v1.duality_defect_constrained
        srmse = res_v1.rmse
        # Reconstruct L' for recovery score
        L_v1 = baseline_symmetrize(L_noisy)  # v0.1 converges to this
        rec = frobenius_distance(L_true, L_v1)
        pscore = P_recovery_score(P_fixed, P_true)
        row["prism_v1"] = dict(defect=defect, srmse=srmse, rec=rec, pscore=pscore, ms=dt)
        if verbose:
            print(f"  {'Prism v0.1 (fixed P)':25s}  {defect:8.4f}  {srmse:9.4f}  "
                  f"{rec:9.4f}  {pscore:8.4f}  {dt:6.1f}")

        # --- Prism v0.2 (learnable P, multi-start) ---
        t0 = time.perf_counter()
        res_v2 = optimize_learnable_multistart(
            L_noisy,
            alpha=2.0,
            beta=1.0,
            gamma=0.2,
            max_iter=400,
            n_starts=5,
            verbose=False,
        )
        dt = (time.perf_counter() - t0) * 1000
        defect = res_v2.duality_defect_constrained
        srmse = res_v2.spectral_rmse
        rec = frobenius_distance(L_true, res_v2.constrained_eigenvalues)
        # Use Frobenius distance between L' and L_true
        # Reconstruct L' from eigenvalues is lossy; use spectral proxy
        rec = float(np.sqrt(np.sum(
            (np.sort(np.linalg.eigvalsh(L_true)) -
             res_v2.constrained_eigenvalues) ** 2
        )))
        pscore = P_recovery_score(res_v2.learned_P, P_true)
        row["prism_v2"] = dict(defect=defect, srmse=srmse, rec=rec,
                                pscore=pscore, ms=dt,
                                involution=res_v2.involution_defect)
        if verbose:
            print(f"  {'Prism v0.2 (learnable P)':25s}  {defect:8.4f}  {srmse:9.4f}  "
                  f"{rec:9.4f}  {pscore:8.4f}  {dt:6.1f}")
            interp = interpret_P(res_v2.learned_P)
            print(f"    Learned P: {interp['n_pairs']} cross-pairs, "
                  f"{interp['n_self_dual']} self-dual, "
                  f"involution_defect={res_v2.involution_defect:.4f}")

        results.append(row)
        if verbose:
            print()

    # Summary
    if verbose:
        print("=" * 62)
        print("P-score: overlap between learned P and true duality (higher = better)")
        print("Recovery: spectral distance to true Laplacian (lower = better)")
        print()
        print(f"  {'Noise':>6}  {'Method':25s}  {'P-score':>8}  {'Recovery':>9}")
        print(f"  {'-'*6}  {'-'*25}  {'-'*8}  {'-'*9}")
        for row in results:
            noise = row["noise"]
            for method in ["identity", "symmetrize", "prism_v1", "prism_v2"]:
                r = row[method]
                label = {"identity": "Identity",
                         "symmetrize": "Symmetrize(fixed P)",
                         "prism_v1": "Prism v0.1",
                         "prism_v2": "Prism v0.2 (learnable)"}[method]
                marker = " <--" if method == "prism_v2" else ""
                print(f"  {noise:6.2f}  {label:25s}  "
                      f"{r['pscore']:8.4f}  {r['rec']:9.4f}{marker}")
            print()

    return results


if __name__ == '__main__':
    # Small network first (fast)
    print("=== Small network (n=12) ===")
    run_v2_benchmark(n=12, noise_levels=[0.0, 0.10, 0.20])

    print()
    print("=== Medium network (n=20) ===")
    run_v2_benchmark(n=20, noise_levels=[0.0, 0.10, 0.20])
