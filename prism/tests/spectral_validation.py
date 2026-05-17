"""
Prism spectral validation: robustness under edge noise.

Task: binary community detection on Karate Club with increasing edge noise.
At each noise level, randomly flip k% of edges (add/remove).
Hypothesis: UCA constraint (learned P) degrades more slowly than raw Laplacian.

Methods compared:
  - Baseline: raw graph Laplacian Fiedler clustering
  - Prism (learned P): UCA constraint with P from Fiedler vector of clean graph
  - RMT: Marchenko-Pastur threshold

Ground truth: Zachary 1977 split.
Metric: accuracy averaged over 50 noise trials per noise level.
"""

import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from prism.core import optimize, learned_parity_operator, optimize_with_P


KARATE_EDGES = [
    (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,10),(0,11),
    (0,12),(0,13),(0,17),(0,19),(0,21),(0,31),(1,2),(1,3),(1,7),(1,13),
    (1,17),(1,19),(1,21),(1,30),(2,3),(2,7),(2,8),(2,9),(2,13),(2,27),
    (2,28),(2,32),(3,7),(3,12),(3,13),(4,6),(4,10),(5,6),(5,10),(5,16),
    (6,16),(8,30),(8,32),(8,33),(9,33),(13,33),(14,32),(14,33),(15,32),
    (15,33),(18,32),(18,33),(19,33),(20,32),(20,33),(22,32),(22,33),
    (23,25),(23,27),(23,29),(23,32),(23,33),(24,25),(24,27),(24,31),
    (25,31),(26,29),(26,33),(27,33),(28,31),(28,33),(29,32),(29,33),
    (30,32),(30,33),(31,32),(31,33),(32,33)
]

KARATE_GROUND_TRUTH = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 1, 1, 0, 0, 1, 0,
    1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1
]


def build_adjacency(n, edges):
    A = np.zeros((n, n))
    for u, v in edges:
        A[u, v] = A[v, u] = 1.0
    return A


def adjacency_to_laplacian(A):
    return np.diag(A.sum(axis=1)) - A


def add_noise(A, noise_rate, rng):
    """Flip each potential edge with probability noise_rate."""
    n = A.shape[0]
    A_noisy = A.copy()
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < noise_rate:
                A_noisy[i, j] = 1.0 - A_noisy[i, j]
                A_noisy[j, i] = A_noisy[i, j]
    return A_noisy


def fiedler_clustering(L):
    _, evecs = np.linalg.eigh(L)
    return (evecs[:, 1] >= 0).astype(int)


def accuracy(pred, truth):
    truth = np.array(truth)
    return max(np.mean(pred == truth), np.mean(1 - pred == truth))


def laplacian_from_result(result, L_original):
    _, evecs = np.linalg.eigh(L_original)
    return evecs @ np.diag(result.constrained_eigenvalues) @ evecs.T


def run_noise_robustness(noise_levels=None, n_trials=50, seed=42):
    if noise_levels is None:
        noise_levels = [0.0, 0.02, 0.05, 0.10, 0.15, 0.20]

    n = 34
    A_clean = build_adjacency(n, KARATE_EDGES)
    L_clean = adjacency_to_laplacian(A_clean)
    truth = KARATE_GROUND_TRUTH

    # Learn P from the clean graph once — this is the "prior knowledge" Prism uses
    P_learned = learned_parity_operator(L_clean)

    print("=" * 65)
    print("Prism Noise Robustness — Karate Club Community Detection")
    print("=" * 65)
    print(f"Network: {n} nodes, {len(KARATE_EDGES)} edges")
    print(f"Trials per noise level: {n_trials}")
    print(f"P learned from: clean graph Fiedler vector")
    print()
    print(f"{'Noise':>8}  {'Baseline':>10}  {'RMT':>10}  {'Prism(learned P)':>18}  {'Prism wins?':>12}")
    print("-" * 65)

    rng = np.random.default_rng(seed)
    summary = []

    for noise in noise_levels:
        acc_baseline_list = []
        acc_rmt_list = []
        acc_prism_list = []

        for _ in range(n_trials):
            A_noisy = add_noise(A_clean, noise, rng)
            L_noisy = adjacency_to_laplacian(A_noisy)

            # Baseline
            pred_b = fiedler_clustering(L_noisy)
            acc_baseline_list.append(accuracy(pred_b, truth))

            # RMT
            evals, evecs = np.linalg.eigh(L_noisy)
            median_ev = np.median(np.abs(evals[evals > 1e-10]))
            filtered = np.where(np.abs(evals) < median_ev * 0.5, 0.0, evals)
            L_rmt = evecs @ np.diag(filtered) @ evecs.T
            pred_rmt = fiedler_clustering(L_rmt)
            acc_rmt_list.append(accuracy(pred_rmt, truth))

            # Prism with learned P (P fixed from clean graph)
            result = optimize_with_P(L_noisy, P_learned)
            pred_prism = fiedler_clustering(result.constrained_matrix)
            acc_prism_list.append(accuracy(pred_prism, truth))

        acc_b = np.mean(acc_baseline_list)
        acc_r = np.mean(acc_rmt_list)
        acc_p = np.mean(acc_prism_list)
        wins = "YES" if acc_p > acc_b + 0.005 else ("tie" if abs(acc_p - acc_b) <= 0.005 else "no")
        summary.append((noise, acc_b, acc_r, acc_p, wins))
        print(f"{noise:>7.0%}  {acc_b:>10.1%}  {acc_r:>10.1%}  {acc_p:>18.1%}  {wins:>12}")

    print("-" * 65)
    print()

    prism_wins = sum(1 for _, _, _, acc_p, w in summary if w == "YES")
    print(f"Prism (learned P) outperforms baseline in {prism_wins}/{len(noise_levels)} noise levels.")

    if prism_wins >= len(noise_levels) // 2:
        print("Result: UCA constraint with learned P provides noise robustness.")
        print("The Fiedler-derived duality acts as a structural prior.")
    else:
        print("Result: UCA constraint does not improve noise robustness here.")
        print("The learned P does not encode information beyond the noisy Fiedler vector.")

    return summary


if __name__ == "__main__":
    run_noise_robustness()
