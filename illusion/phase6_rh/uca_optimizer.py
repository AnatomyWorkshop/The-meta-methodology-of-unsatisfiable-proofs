"""
UCA-constrained joint optimizer for Phase 6: Riemann Hypothesis.

Strategy (from duality defect analysis):
  - Spectral matching and duality compatibility are orthogonal constraints.
  - Starting from H_BK + V_defect (which satisfies [H, P] = 0 exactly),
    optimize within the UCA-compatible subspace.

Key insight: [H, P] = 0 iff H is block-diagonal in the P-eigenbasis.
  - P has eigenvalues ±1, splitting the n-dim space into two n/2-dim sectors.
  - Parameterize H by two independent Hermitian blocks (H_+, H_-).
  - This enforces [H, P] = 0 by construction — no soft penalty needed.
  - Free parameters: 2 * (n/2)(n/2+1)/2 = n(n/2+1)/2 (vs n(n+1)/2 unconstrained).

Starting point: project H_BK + V_defect onto the block-diagonal form.
"""

import numpy as np
from scipy.optimize import minimize
from dataclasses import dataclass
from typing import Optional
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from l1_rh import zeta_zeros
from inverse_spectral_optimizer import build_base_hamiltonian
from duality_defect import parity_operator, defect_analysis


@dataclass
class UCAOptResult:
    best_H: np.ndarray
    best_eigenvalues: np.ndarray
    target_zeros: np.ndarray
    spectral_error: float
    duality_defect_norm: float
    n_iterations: int
    history: list
    converged: bool


def build_uca_start(n: int, n_zeros: int) -> np.ndarray:
    """
    Build the UCA-compatible starting point: H_BK + V_defect.
    H_BK is affine-scaled to match the n_zeros target range.
    The result satisfies [H, P] = 0 exactly.
    """
    result = defect_analysis(n=n, n_zeros=n_zeros, verbose=False)
    H_start = result["H_bk"] + result["V_hermitian"]
    # Should be real symmetric — imaginary parts are numerical noise
    H_start = H_start.real
    P = parity_operator(n)
    defect_norm = np.linalg.norm(H_start @ P - P @ H_start, 'fro')
    assert defect_norm < 1e-8, f"Starting point duality defect too large: {defect_norm:.2e}"
    return H_start


def parity_eigenbasis(n: int):
    """
    Compute the eigenbasis of P and return the transformation matrix.
    P = anti-diagonal identity (index reversal).

    Eigenvalues: +1 (even sector) and -1 (odd sector).
    For even n: n/2 each. For odd n: (n+1)/2 even, (n-1)/2 odd.
    Returns: (U, idx_plus, idx_minus) where U diagonalizes P.
    """
    P = parity_operator(n)
    evals, evecs = np.linalg.eigh(P)
    idx_minus = np.where(evals < 0)[0]
    idx_plus = np.where(evals > 0)[0]
    if len(idx_plus) + len(idx_minus) != n:
        raise ValueError(f"Unexpected parity eigenvalues: {evals}")
    return evecs, idx_plus, idx_minus


def H_to_blocks(H: np.ndarray, U: np.ndarray, idx_plus, idx_minus):
    """Project H into P-eigenbasis and extract the two diagonal blocks."""
    H_rot = U.T @ H @ U
    H_plus = H_rot[np.ix_(idx_plus, idx_plus)]
    H_minus = H_rot[np.ix_(idx_minus, idx_minus)]
    return H_plus.real, H_minus.real


def blocks_to_H(H_plus: np.ndarray, H_minus: np.ndarray,
                U: np.ndarray, idx_plus, idx_minus, n: int) -> np.ndarray:
    """Reconstruct full H from two blocks in P-eigenbasis."""
    H_rot = np.zeros((n, n))
    H_rot[np.ix_(idx_plus, idx_plus)] = H_plus
    H_rot[np.ix_(idx_minus, idx_minus)] = H_minus
    return U @ H_rot @ U.T


def params_to_blocks(params: np.ndarray, m_plus: int, m_minus: int):
    """
    Convert flat params to two symmetric matrices (H_plus, H_minus).
    H_plus is m_plus×m_plus, H_minus is m_minus×m_minus.
    """
    k_plus = m_plus * (m_plus + 1) // 2
    params_plus = params[:k_plus]
    params_minus = params[k_plus:]

    def fill(p, size):
        M = np.zeros((size, size))
        idx = 0
        for i in range(size):
            for j in range(i, size):
                M[i, j] = p[idx]
                M[j, i] = p[idx]
                idx += 1
        return M

    return fill(params_plus, m_plus), fill(params_minus, m_minus)


def blocks_to_params(H_plus: np.ndarray, H_minus: np.ndarray) -> np.ndarray:
    """Extract upper-triangle parameters from two symmetric blocks."""
    def extract(M):
        size = M.shape[0]
        p = []
        for i in range(size):
            for j in range(i, size):
                p.append(M[i, j])
        return np.array(p)
    return np.concatenate([extract(H_plus), extract(H_minus)])


def uca_spectral_loss(params: np.ndarray, U: np.ndarray, idx_plus, idx_minus,
                      n: int, m_plus: int, m_minus: int, target: np.ndarray,
                      reg_lambda: float = 1e-5) -> float:
    """
    Loss function for UCA-constrained optimization.
    H is block-diagonal by construction — [H, P] = 0 is exact.
    Loss = ||sorted_eigs[-n_target:] - target||^2 + reg * ||params||^2
    """
    H_plus, H_minus = params_to_blocks(params, m_plus, m_minus)
    eigs_plus = np.linalg.eigvalsh(H_plus)
    eigs_minus = np.linalg.eigvalsh(H_minus)
    all_eigs = np.sort(np.concatenate([eigs_plus, eigs_minus]))

    n_target = len(target)
    eigs_to_match = all_eigs[-n_target:]
    target_sorted = np.sort(target)

    loss = np.sum((eigs_to_match - target_sorted)**2) / n_target
    reg = reg_lambda * np.sum(params**2)
    return loss + reg


def optimize_uca_constrained(
    n: int = 50,
    n_zeros: int = 30,
    max_iter: int = 2000,
    reg_lambda: float = 1e-5,
    verbose: bool = True,
) -> UCAOptResult:
    """
    Optimize within the UCA-compatible subspace.

    The UCA constraint [H, P] = 0 is enforced by construction via
    block-diagonal parameterization in the P-eigenbasis.

    Starting point: H_BK + V_defect (already satisfies [H, P] = 0).
    """
    if verbose:
        print("=" * 65)
        print("UCA-Constrained Joint Optimizer")
        print(f"  n={n}, zeros={n_zeros}, reg={reg_lambda}")
        print("  Constraint: [H, P] = 0 enforced by block-diagonal structure")
        print("=" * 65)
        print()

    target = np.sort(zeta_zeros(n_zeros))
    U, idx_plus, idx_minus = parity_eigenbasis(n)
    m_plus = len(idx_plus)
    m_minus = len(idx_minus)
    n_params = m_plus * (m_plus + 1) // 2 + m_minus * (m_minus + 1) // 2

    if verbose:
        print(f"  Target range: [{target[0]:.3f}, {target[-1]:.3f}]")
        print(f"  Even sector: {m_plus}×{m_plus}, Odd sector: {m_minus}×{m_minus}")
        print(f"  Free parameters: {n_params} (vs {n*(n+1)//2} unconstrained)")
        print()

    # Starting point: H_BK + V_defect, scaled to n_zeros target range
    if verbose:
        print("  Building UCA-compatible starting point (H_BK + V_defect)...")
    H_start = build_uca_start(n, n_zeros)

    # Project to blocks
    H_plus_0, H_minus_0 = H_to_blocks(H_start, U, idx_plus, idx_minus)
    x0 = blocks_to_params(H_plus_0, H_minus_0)

    # Check starting spectral error
    eigs_plus_0 = np.linalg.eigvalsh(H_plus_0)
    eigs_minus_0 = np.linalg.eigvalsh(H_minus_0)
    eigs_start = np.sort(np.concatenate([eigs_plus_0, eigs_minus_0]))
    start_rmse = np.sqrt(np.mean((eigs_start[-n_zeros:] - np.sort(target))**2))

    if verbose:
        print(f"  Starting spectral RMSE: {start_rmse:.4f}")
        init_loss = uca_spectral_loss(x0, U, idx_plus, idx_minus, n, m_plus, m_minus, target, reg_lambda)
        print(f"  Starting loss: {init_loss:.6f}")
        print()
        print("  Starting L-BFGS-B optimization in UCA subspace...")
        print()

    history = []

    def callback(xk):
        loss = uca_spectral_loss(xk, U, idx_plus, idx_minus, n, m_plus, m_minus, target, reg_lambda)
        history.append(loss)
        if verbose and len(history) % 100 == 0:
            Hp, Hm = params_to_blocks(xk, m_plus, m_minus)
            ep = np.linalg.eigvalsh(Hp)
            em = np.linalg.eigvalsh(Hm)
            eigs = np.sort(np.concatenate([ep, em]))
            rmse = np.sqrt(np.mean((eigs[-n_zeros:] - np.sort(target))**2))
            print(f"  iter {len(history):4d}: loss={loss:.6f}  RMSE={rmse:.6f}")

    result = minimize(
        uca_spectral_loss,
        x0,
        args=(U, idx_plus, idx_minus, n, m_plus, m_minus, target, reg_lambda),
        method='L-BFGS-B',
        callback=callback,
        options={
            'maxiter': max_iter,
            'ftol': 1e-18,
            'gtol': 1e-12,
            'maxfun': 10_000_000,
        }
    )

    # Extract final result
    H_plus_f, H_minus_f = params_to_blocks(result.x, m_plus, m_minus)
    best_H = blocks_to_H(H_plus_f, H_minus_f, U, idx_plus, idx_minus, n)

    eigs_plus_f = np.linalg.eigvalsh(H_plus_f)
    eigs_minus_f = np.linalg.eigvalsh(H_minus_f)
    best_eigs = np.sort(np.concatenate([eigs_plus_f, eigs_minus_f]))

    spectral_error = np.sqrt(np.mean((best_eigs[-n_zeros:] - np.sort(target))**2))

    # Verify [H, P] = 0
    P = parity_operator(n)
    defect = best_H @ P - P @ best_H
    defect_norm = np.linalg.norm(defect, 'fro')

    if verbose:
        print()
        print("  Optimization complete.")
        print(f"  Iterations: {result.nit}")
        print(f"  Final loss: {result.fun:.8f}")
        print(f"  Spectral RMSE: {spectral_error:.8f}")
        print(f"  Duality defect ||[H,P]||_F: {defect_norm:.2e}  (should be ~0)")
        print()
        print(f"  First 5 optimized eigenvalues: {best_eigs[-n_zeros:][:5]}")
        print(f"  First 5 target zeros:          {np.sort(target)[:5]}")
        print(f"  Differences:                   {best_eigs[-n_zeros:][:5] - np.sort(target)[:5]}")
        print()

        # Per-zero table (first 10)
        print("  Per-zero precision (first 10):")
        print(f"  {'Zero':>4}  {'Target':>10}  {'Achieved':>10}  {'Error':>10}  {'Rel%':>8}")
        for i in range(min(10, n_zeros)):
            t = np.sort(target)[i]
            a = best_eigs[-n_zeros:][i]
            err = abs(a - t)
            rel = err / t * 100
            print(f"  {i+1:>4}  {t:>10.4f}  {a:>10.4f}  {err:>10.6f}  {rel:>8.4f}%")

        if spectral_error < 1e-4:
            print()
            print("  *** CONVERGENCE: RMSE < 1e-4 ***")
            print("  A finite-dimensional Hilbert-Polya operator satisfying UCA has been found.")
        elif spectral_error < 0.01:
            print()
            print("  Near-convergence: RMSE < 0.01. Increase max_iter or n.")
        else:
            print()
            print("  Not converged. Consider: larger n, more iterations, or different reg.")

    return UCAOptResult(
        best_H=best_H,
        best_eigenvalues=best_eigs,
        target_zeros=target,
        spectral_error=spectral_error,
        duality_defect_norm=defect_norm,
        n_iterations=result.nit,
        history=history,
        converged=(spectral_error < 1e-4),
    )


if __name__ == "__main__":
    result = optimize_uca_constrained(
        n=50,
        n_zeros=30,
        max_iter=2000,
        reg_lambda=1e-5,
        verbose=True,
    )
