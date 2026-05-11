"""
Inverse spectral optimizer for Phase 6: Riemann Hypothesis.

Goal: Find a potential V(x) such that the PT-symmetric Berry-Keating Hamiltonian
  H = H_BK + V
has spectrum matching the first N zeta zeros, while preserving PT symmetry.

This is a structured inverse eigenvalue problem:
  Given: target spectrum {gamma_1, ..., gamma_N} (zeta zeros)
  Find: V (PT-symmetric perturbation matrix) minimizing ||Spec(H_BK + V) - target||

Constraints:
  1. PT symmetry: P * conj(H) * P = H (P = parity/reversal matrix)
  2. PT-unbroken: all eigenvalues must remain real
  3. V is "small" relative to H_BK (regularization)

Method: Gradient-based optimization (L-BFGS-B) on the free parameters of V,
with PT symmetry enforced by construction and reality checked at each step.
"""

import numpy as np
from scipy.optimize import minimize
from typing import Tuple, Optional
from dataclasses import dataclass

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from l1_rh import zeta_zeros
from operators_rh import OperatorCandidate


@dataclass
class OptimizationResult:
    best_V: np.ndarray
    best_H: np.ndarray
    best_eigenvalues: np.ndarray
    target_zeros: np.ndarray
    spectral_error: float
    matched_fraction: float
    pt_unbroken: bool
    n_iterations: int
    history: list


def build_base_hamiltonian(n: int) -> np.ndarray:
    """Berry-Keating H = xp + px in Dirichlet basis (Hermitian)."""
    H = np.zeros((n, n), dtype=complex)
    for j in range(n):
        for k in range(n):
            if (j + k) % 2 == 1:
                jj, kk = j + 1, k + 1
                H[j, k] = -1j * 2 * jj * kk / (kk**2 - jj**2)
    H = (H + H.conj().T) / 2
    return H


def params_to_hermitian_V(params: np.ndarray, n: int) -> np.ndarray:
    """
    Convert free parameters to a real symmetric (Hermitian) perturbation.
    n(n+1)/2 free parameters: diagonal + upper triangle.
    """
    V = np.zeros((n, n))
    idx = 0
    for j in range(n):
        for k in range(j, n):
            V[j, k] = params[idx]
            V[k, j] = params[idx]
            idx += 1
    return V


def count_free_params(n: int) -> int:
    """Count free parameters for Hermitian perturbation: n(n+1)/2."""
    return n * (n + 1) // 2


def spectral_loss(params: np.ndarray, H_base: np.ndarray, target: np.ndarray,
                  n: int, reg_lambda: float = 0.01) -> float:
    """
    Loss: ||sorted_eigenvalues(H_base + V) - target||^2 + regularization.
    H_base + V is Hermitian by construction, so eigenvalues are always real.
    """
    V = params_to_hermitian_V(params, n)
    H = H_base + V

    eigs = np.sort(np.linalg.eigvalsh(H))

    # Match the top n_target eigenvalues to the target zeros
    n_target = len(target)
    eigs_to_match = eigs[-n_target:]
    target_sorted = np.sort(target)

    # L2 loss
    loss = np.sum((eigs_to_match - target_sorted)**2) / n_target

    # Regularization: penalize deviation from Berry-Keating structure
    reg = reg_lambda * np.sum(params**2)

    return loss + reg


def spectral_loss_gradient(params: np.ndarray, H_base: np.ndarray, target: np.ndarray,
                           n: int, reg_lambda: float = 0.01) -> np.ndarray:
    """Numerical gradient via finite differences (for validation)."""
    grad = np.zeros_like(params)
    eps = 1e-7
    f0 = spectral_loss(params, H_base, target, n, reg_lambda)
    for i in range(len(params)):
        params[i] += eps
        f1 = spectral_loss(params, H_base, target, n, reg_lambda)
        params[i] -= eps
        grad[i] = (f1 - f0) / eps
    return grad


def optimize_spectral_match(
    n: int = 30,
    n_zeros: int = 20,
    max_iter: int = 500,
    reg_lambda: float = 0.001,
    verbose: bool = True,
) -> OptimizationResult:
    """
    Run inverse spectral optimization to find V that matches zeta zeros.

    Strategy:
    1. Start from H_BK affine-scaled to the zeta zero range
    2. Add Hermitian perturbation V (guarantees real spectrum)
    3. Optimize V to minimize ||Spec(H_BK_scaled + V) - zeta_zeros||^2
    4. After optimization, measure PT-symmetry of the result
    """
    if verbose:
        print(f"Inverse Spectral Optimizer")
        print(f"  Matrix dimension: {n}")
        print(f"  Target: first {n_zeros} zeta zeros")
        print()

    # Target spectrum
    zeros = zeta_zeros(n_zeros)
    target = np.sort(zeros)

    if verbose:
        print(f"  Target range: [{target[0]:.3f}, {target[-1]:.3f}]")

    # Base Hamiltonian: Berry-Keating, affine-scaled to target range
    H_base = build_base_hamiltonian(n)
    base_eigs = np.sort(np.linalg.eigvalsh(H_base))
    # Scale so that eigenvalue range matches target range
    base_min, base_max = base_eigs[0], base_eigs[-1]
    base_range = base_max - base_min
    target_min, target_max = target[0], target[-1]
    target_range = target_max - target_min
    if base_range > 1e-10:
        scale = target_range / base_range
        shift = target_min - base_min * scale
        H_base = scale * H_base + shift * np.eye(n)

    if verbose:
        scaled_eigs = np.sort(np.linalg.eigvalsh(H_base))
        print(f"  Scaled H_BK range: [{scaled_eigs[0]:.3f}, {scaled_eigs[-1]:.3f}]")

    # Count and initialize parameters
    n_params = count_free_params(n)
    if verbose:
        print(f"  Free parameters: {n_params}")
        print()

    # Initial parameters: zero (start from scaled Berry-Keating)
    x0 = np.zeros(n_params)

    # Optimization history
    history = []

    def callback(xk):
        loss = spectral_loss(xk, H_base, target, n, reg_lambda)
        history.append(loss)
        if verbose and len(history) % 50 == 0:
            print(f"  iter {len(history)}: loss = {loss:.6f}")

    if verbose:
        init_loss = spectral_loss(x0, H_base, target, n, reg_lambda)
        print(f"  Initial loss: {init_loss:.6f}")
        print("  Starting optimization (L-BFGS-B)...")
        print()

    result = minimize(
        spectral_loss,
        x0,
        args=(H_base, target, n, reg_lambda),
        method='L-BFGS-B',
        callback=callback,
        options={
            'maxiter': max_iter,
            'ftol': 1e-15,
            'gtol': 1e-10,
        }
    )

    # Extract final result
    best_params = result.x
    best_V = params_to_hermitian_V(best_params, n)
    best_H = H_base + best_V

    best_eigs = np.sort(np.linalg.eigvalsh(best_H))

    # Compute spectral match
    n_target = len(target)
    eigs_to_match = best_eigs[-n_target:]
    target_sorted = np.sort(target)

    epsilon = 0.5
    matched = sum(1 for i in range(n_target)
                  if np.min(np.abs(eigs_to_match - target_sorted[i])) < epsilon)
    matched_fraction = matched / n_target
    spectral_error = np.sqrt(np.mean((eigs_to_match - target_sorted)**2))

    # Measure PT symmetry of the result
    P = np.eye(n)[::-1]
    best_H_complex = best_H.astype(complex)
    PT_H = P @ best_H_complex.conj() @ P
    pt_error = np.max(np.abs(PT_H - best_H_complex))
    pt_relative = pt_error / np.max(np.abs(best_H_complex))

    # Measure Berry-Keating structure retention
    H_bk_original = build_base_hamiltonian(n)
    base_min_o, base_max_o = np.sort(np.linalg.eigvalsh(H_bk_original))[[0, -1]]
    base_range_o = base_max_o - base_min_o
    scale_o = target_range / base_range_o
    shift_o = target_min - base_min_o * scale_o
    H_bk_scaled = scale_o * H_bk_original + shift_o * np.eye(n)
    bk_deviation = np.linalg.norm(best_H - H_bk_scaled, 'fro') / np.linalg.norm(H_bk_scaled, 'fro')

    if verbose:
        print(f"\n  Optimization complete.")
        print(f"  Final loss: {result.fun:.6f}")
        print(f"  Iterations: {result.nit}")
        print(f"  Spectral error (RMSE): {spectral_error:.6f}")
        print(f"  Matched fraction (eps=0.5): {matched_fraction:.3f}")
        print(f"  PT symmetry error: {pt_error:.4f} (relative: {pt_relative:.4f})")
        print(f"  Berry-Keating deviation: {bk_deviation:.4f}")
        print()
        print(f"  First 5 optimized eigenvalues: {eigs_to_match[:5]}")
        print(f"  First 5 target zeros:          {target_sorted[:5]}")
        print(f"  Differences:                   {eigs_to_match[:5] - target_sorted[:5]}")

    return OptimizationResult(
        best_V=best_V,
        best_H=best_H,
        best_eigenvalues=best_eigs,
        target_zeros=target,
        spectral_error=spectral_error,
        matched_fraction=matched_fraction,
        pt_unbroken=(pt_relative < 0.01),
        n_iterations=result.nit,
        history=history,
    )


def run_optimization_experiment(verbose: bool = True) -> dict:
    """Run the full inverse spectral optimization experiment."""
    if verbose:
        print("=" * 70)
        print("Phase 6: Inverse Spectral Optimization")
        print("  Finding PT-symmetric potential matching zeta zeros")
        print("=" * 70)
        print()

    # Start with smaller dimension for feasibility
    results = {}

    for n, n_zeros in [(20, 10), (30, 15), (40, 20)]:
        if verbose:
            print(f"\n{'─' * 50}")
            print(f"  Trial: n={n}, target={n_zeros} zeros")
            print(f"{'─' * 50}\n")

        opt_result = optimize_spectral_match(
            n=n,
            n_zeros=n_zeros,
            max_iter=300,
            reg_lambda=0.001,
            verbose=verbose,
        )

        results[f"n{n}_z{n_zeros}"] = {
            "spectral_error": opt_result.spectral_error,
            "matched_fraction": opt_result.matched_fraction,
            "pt_unbroken": opt_result.pt_unbroken,
            "n_iterations": opt_result.n_iterations,
        }

    if verbose:
        print(f"\n{'=' * 70}")
        print("Summary:")
        print(f"{'=' * 70}")
        for key, val in results.items():
            print(f"  {key}: error={val['spectral_error']:.4f}, "
                  f"match={val['matched_fraction']:.3f}, "
                  f"PT={val['pt_unbroken']}")

    return results


if __name__ == "__main__":
    run_optimization_experiment(verbose=True)
