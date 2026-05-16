"""
Prism benchmark: compare UCA-constrained spectral analysis against
DOMINANT and Radar-style baselines.

Baselines implemented here (no external deps beyond numpy/scipy):
  - Random Matrix Theory (RMT) threshold: remove eigenvalues below
    Marchenko-Pastur upper edge (standard Radar/DOMINANT approach)
  - Soft threshold: shrink small eigenvalues toward zero
  - Identity baseline: no transformation (raw Laplacian)

Metrics:
  - Duality defect: ||[L, P]||_F  (Prism's native criterion)
  - Spectral RMSE: how much the spectrum shifts from original
  - Symmetry score: how close L is to being P-symmetric
  - Runtime: wall-clock seconds

Test networks:
  - Cycle graph (known ground truth: perfectly symmetric)
  - Path graph (asymmetric, known spectrum)
  - Random Erdos-Renyi (noisy, realistic)
  - Karate Club (real-world, 34 nodes)
  - Stochastic block model (community structure)
"""

import numpy as np
import time
from dataclasses import dataclass
from typing import Callable

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from prism.core import optimize, parity_operator


# ---------------------------------------------------------------------------
# Network generators
# ---------------------------------------------------------------------------

def cycle_graph(n: int) -> np.ndarray:
    A = np.zeros((n, n))
    for i in range(n):
        A[i, (i + 1) % n] = 1
        A[(i + 1) % n, i] = 1
    D = np.diag(A.sum(axis=1))
    return D - A


def path_graph(n: int) -> np.ndarray:
    A = np.zeros((n, n))
    for i in range(n - 1):
        A[i, i + 1] = 1
        A[i + 1, i] = 1
    D = np.diag(A.sum(axis=1))
    return D - A


def erdos_renyi(n: int, p: float, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    A = rng.random((n, n))
    A = (A + A.T) / 2
    A = (A < p).astype(float)
    np.fill_diagonal(A, 0)
    D = np.diag(A.sum(axis=1))
    return D - A


def stochastic_block_model(n: int, k: int, p_in: float, p_out: float,
                            seed: int = 42) -> np.ndarray:
    """k equal-size communities."""
    rng = np.random.default_rng(seed)
    block_size = n // k
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            same_block = (i // block_size) == (j // block_size)
            p = p_in if same_block else p_out
            if rng.random() < p:
                A[i, j] = 1
                A[j, i] = 1
    D = np.diag(A.sum(axis=1))
    return D - A


def karate_club() -> np.ndarray:
    """Zachary's Karate Club (34 nodes). Hardcoded edge list."""
    edges = [
        (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,10),(0,11),
        (0,12),(0,13),(0,17),(0,19),(0,21),(0,31),(1,2),(1,3),(1,7),(1,13),
        (1,17),(1,19),(1,21),(1,30),(2,3),(2,7),(2,8),(2,9),(2,13),(2,27),
        (2,28),(2,32),(3,7),(3,12),(3,13),(4,6),(4,10),(5,6),(5,10),(5,16),
        (6,16),(8,30),(8,32),(8,33),(9,33),(13,33),(14,32),(14,33),(15,32),
        (15,33),(18,32),(18,33),(19,33),(20,32),(20,33),(22,32),(22,33),
        (23,25),(23,27),(23,29),(23,32),(23,33),(24,25),(24,27),(24,31),
        (25,31),(26,29),(26,33),(27,33),(28,31),(28,33),(29,32),(29,33),
        (30,32),(30,33),(31,32),(31,33),(32,33),
    ]
    n = 34
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = 1
        A[j, i] = 1
    D = np.diag(A.sum(axis=1))
    return D - A


# ---------------------------------------------------------------------------
# Baseline methods
# ---------------------------------------------------------------------------

def baseline_identity(L: np.ndarray) -> np.ndarray:
    """No transformation."""
    return L.copy()


def baseline_rmt_threshold(L: np.ndarray, gamma: float = None) -> np.ndarray:
    """
    Marchenko-Pastur hard threshold on eigenvalues.
    Eigenvalues below the MP upper edge are zeroed out.
    gamma = n/T ratio; if None, use gamma=1 (square case).
    """
    if gamma is None:
        gamma = 1.0
    sigma2 = np.var(np.linalg.eigvalsh(L))
    lambda_plus = sigma2 * (1 + np.sqrt(gamma)) ** 2
    evals, evecs = np.linalg.eigh(L)
    evals_thresh = np.where(np.abs(evals) > lambda_plus, evals, 0.0)
    return evecs @ np.diag(evals_thresh) @ evecs.T


def baseline_soft_threshold(L: np.ndarray, tau: float = None) -> np.ndarray:
    """
    Soft threshold: shrink eigenvalues toward zero by tau.
    tau defaults to median absolute eigenvalue.
    """
    evals, evecs = np.linalg.eigh(L)
    if tau is None:
        tau = np.median(np.abs(evals))
    evals_soft = np.sign(evals) * np.maximum(np.abs(evals) - tau, 0)
    return evecs @ np.diag(evals_soft) @ evecs.T


def baseline_symmetrize(L: np.ndarray) -> np.ndarray:
    """Force P-symmetry by averaging L with P L P."""
    n = L.shape[0]
    P = parity_operator(n)
    return (L + P @ L @ P) / 2


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def duality_defect(L: np.ndarray) -> float:
    n = L.shape[0]
    P = parity_operator(n)
    return float(np.linalg.norm(L @ P - P @ L, 'fro'))


def spectral_rmse(L_orig: np.ndarray, L_new: np.ndarray) -> float:
    e1 = np.sort(np.linalg.eigvalsh(L_orig))
    e2 = np.sort(np.linalg.eigvalsh(L_new))
    return float(np.sqrt(np.mean((e1 - e2) ** 2)))


def frobenius_distance(L_orig: np.ndarray, L_new: np.ndarray) -> float:
    return float(np.linalg.norm(L_orig - L_new, 'fro'))


# ---------------------------------------------------------------------------
# Benchmark runner
# ---------------------------------------------------------------------------

@dataclass
class BenchmarkResult:
    network: str
    method: str
    duality_defect: float
    spectral_rmse: float
    frobenius_dist: float
    runtime_ms: float
    converged: bool = True


def run_one(name: str, L: np.ndarray, method_name: str,
            method_fn: Callable) -> BenchmarkResult:
    t0 = time.perf_counter()
    L_out = method_fn(L)
    dt = (time.perf_counter() - t0) * 1000

    return BenchmarkResult(
        network=name,
        method=method_name,
        duality_defect=duality_defect(L_out),
        spectral_rmse=spectral_rmse(L, L_out),
        frobenius_dist=frobenius_distance(L, L_out),
        runtime_ms=dt,
    )


def run_prism(name: str, L: np.ndarray) -> BenchmarkResult:
    t0 = time.perf_counter()
    result = optimize(L, reg=1e-6, max_iter=2000)
    dt = (time.perf_counter() - t0) * 1000

    L_out = _reconstruct_from_result(L, result)

    return BenchmarkResult(
        network=name,
        method="Prism (UCA)",
        duality_defect=result.duality_defect_constrained,
        spectral_rmse=result.rmse,
        frobenius_dist=frobenius_distance(L, L_out),
        runtime_ms=dt,
        converged=result.converged,
    )


def _reconstruct_from_result(L: np.ndarray, result) -> np.ndarray:
    """Reconstruct constrained Laplacian from PrismResult."""
    from prism.core import (parity_eigenbasis, matrix_to_blocks,
                             params_to_blocks, blocks_to_matrix,
                             blocks_to_params)
    n = L.shape[0]
    L_sym = (L + L.T) / 2
    U, idx_plus, idx_minus = parity_eigenbasis(n)
    m_plus, m_minus = len(idx_plus), len(idx_minus)
    M_plus_0, M_minus_0 = matrix_to_blocks(L_sym, U, idx_plus, idx_minus)
    # Re-run to get the constrained matrix (result stores eigenvalues, not matrix)
    # Use the constrained eigenvalues to reconstruct approximately
    # Actually: re-optimize to get the matrix
    from scipy.optimize import minimize
    from prism.core import proximity_loss, params_to_blocks, blocks_to_matrix
    x0 = blocks_to_params(M_plus_0, M_minus_0)
    res = minimize(proximity_loss, x0,
                   args=(U, idx_plus, idx_minus, n, m_plus, m_minus, L_sym, 1e-6),
                   method='L-BFGS-B',
                   options={'maxiter': 2000, 'ftol': 1e-10, 'gtol': 1e-12})
    M_plus_f, M_minus_f = params_to_blocks(res.x, m_plus, m_minus)
    return blocks_to_matrix(M_plus_f, M_minus_f, U, idx_plus, idx_minus, n)


def run_benchmark(networks: dict = None, verbose: bool = True) -> list:
    if networks is None:
        networks = {
            "Cycle-10":    cycle_graph(10),
            "Path-10":     path_graph(10),
            "ER-20 p=0.3": erdos_renyi(20, 0.3),
            "SBM-20 k=2":  stochastic_block_model(20, 2, 0.6, 0.1),
            "Karate-34":   karate_club(),
        }

    baselines = {
        "Identity":       baseline_identity,
        "Symmetrize(P)":  baseline_symmetrize,
        "RMT-threshold":  baseline_rmt_threshold,
        "Soft-threshold": baseline_soft_threshold,
    }

    all_results = []

    for net_name, L in networks.items():
        if verbose:
            print(f"\n{'='*62}")
            print(f"Network: {net_name}  (n={L.shape[0]})")
            print(f"  Original duality defect: {duality_defect(L):.4f}")
            print()

        # Baselines
        for method_name, fn in baselines.items():
            r = run_one(net_name, L, method_name, fn)
            all_results.append(r)
            if verbose:
                print(f"  {method_name:20s}  defect={r.duality_defect:8.4f}  "
                      f"spec_rmse={r.spectral_rmse:7.4f}  "
                      f"frob={r.frobenius_dist:7.4f}  "
                      f"t={r.runtime_ms:6.1f}ms")

        # Prism
        r = run_prism(net_name, L)
        all_results.append(r)
        if verbose:
            conv = "OK" if r.converged else "FAIL"
            print(f"  {'Prism (UCA)':20s}  defect={r.duality_defect:8.4f}  "
                  f"spec_rmse={r.spectral_rmse:7.4f}  "
                  f"frob={r.frobenius_dist:7.4f}  "
                  f"t={r.runtime_ms:6.1f}ms  {conv}")

    # Summary table
    if verbose:
        print(f"\n{'='*62}")
        print("SUMMARY: Duality Defect (lower = better P-symmetry)")
        print(f"{'Network':20s}  {'Method':20s}  {'Defect':>10}  {'Winner':>6}")
        print(f"{'-'*20}  {'-'*20}  {'-'*10}  {'-'*6}")

        from itertools import groupby
        by_net = {}
        for r in all_results:
            by_net.setdefault(r.network, []).append(r)

        for net_name, results in by_net.items():
            best_defect = min(r.duality_defect for r in results)
            for r in results:
                winner = "<--" if abs(r.duality_defect - best_defect) < 1e-6 else ""
                print(f"  {r.network:20s}  {r.method:20s}  "
                      f"{r.duality_defect:10.4f}  {winner:>6}")
            print()

    return all_results


def run_noise_benchmark() -> None:
    """
    Key benchmark: noisy network where the TRUE graph is known.

    Setup:
      1. Generate a clean SBM (ground truth, P-symmetric by construction)
      2. Add noise: randomly flip edges
      3. Apply each method to the noisy Laplacian
      4. Measure recovery: how close is the output to the CLEAN Laplacian?

    This tests whether each method recovers the true structure,
    not just whether it achieves zero duality defect.

    Prism advantage: it minimizes spectral distortion while enforcing
    duality, so it should stay closer to the true Laplacian than
    Symmetrize(P) which ignores the proximity constraint.
    """
    rng = np.random.default_rng(0)

    print("\n" + "="*62)
    print("NOISE RECOVERY BENCHMARK")
    print("True graph: SBM (2 communities, n=20), known ground truth")
    print("="*62)

    # Ground truth: perfectly P-symmetric SBM
    L_true = stochastic_block_model(20, 2, 0.7, 0.05, seed=1)
    # Force P-symmetry on ground truth
    n = L_true.shape[0]
    P = parity_operator(n)
    L_true = (L_true + P @ L_true @ P) / 2

    noise_levels = [0.05, 0.10, 0.20, 0.30]

    print(f"\n  {'Noise':>6}  {'Method':20s}  {'Defect':>8}  {'Spec-RMSE':>10}  "
          f"{'Recovery':>10}  {'Time(ms)':>9}")
    print(f"  {'-'*6}  {'-'*20}  {'-'*8}  {'-'*10}  {'-'*10}  {'-'*9}")

    for noise in noise_levels:
        # Add noise: flip each edge with probability `noise`
        A_true = np.diag(np.diag(L_true)) - L_true  # adjacency
        flip_mask = rng.random((n, n)) < noise
        flip_mask = np.triu(flip_mask, 1)
        flip_mask = flip_mask + flip_mask.T
        A_noisy = np.abs(A_true - flip_mask)
        np.fill_diagonal(A_noisy, 0)
        D_noisy = np.diag(A_noisy.sum(axis=1))
        L_noisy = D_noisy - A_noisy

        methods = {
            "Identity":       lambda L: baseline_identity(L),
            "Symmetrize(P)":  lambda L: baseline_symmetrize(L),
            "RMT-threshold":  lambda L: baseline_rmt_threshold(L),
        }

        for method_name, fn in methods.items():
            t0 = time.perf_counter()
            L_out = fn(L_noisy)
            dt = (time.perf_counter() - t0) * 1000
            defect = duality_defect(L_out)
            spec_rmse = spectral_rmse(L_noisy, L_out)
            recovery = frobenius_distance(L_true, L_out)
            print(f"  {noise:6.2f}  {method_name:20s}  {defect:8.4f}  "
                  f"{spec_rmse:10.4f}  {recovery:10.4f}  {dt:9.2f}")

        # Prism
        t0 = time.perf_counter()
        res = optimize(L_noisy, reg=1e-6, max_iter=2000)
        dt = (time.perf_counter() - t0) * 1000
        L_prism = _reconstruct_from_result(L_noisy, res)
        defect = duality_defect(L_prism)
        spec_rmse = spectral_rmse(L_noisy, L_prism)
        recovery = frobenius_distance(L_true, L_prism)
        print(f"  {noise:6.2f}  {'Prism (UCA)':20s}  {defect:8.4f}  "
              f"{spec_rmse:10.4f}  {recovery:10.4f}  {dt:9.2f}")
        print()

    print("  Recovery = ||L_output - L_true||_F  (lower = better ground truth recovery)")
    print("  Prism minimizes spectral distortion while enforcing duality.")
    print("  Symmetrize(P) achieves zero defect but ignores proximity to true graph.")


if __name__ == '__main__':
    results = run_benchmark(verbose=True)
    run_noise_benchmark()
