"""
Prism unsupervised mode: jointly optimize L' and P.

Find the involutory operator P and constrained Laplacian L' that minimize
||L' - L||_F subject to [L', P] = 0, P^2 = I, P = P^T, without any
external reference graph.

Algorithm: alternating optimization
  1. Fix P, optimize L' (closed-form: project L onto commutant of P)
  2. Fix L', optimize P (gradient descent on the Stiefel-like manifold of
     symmetric involutions)
  Repeat until convergence.

The key insight: for fixed P, the optimal L' is the projection of L onto
the subspace of matrices commuting with P. This is the block-diagonalization
step from core.py. For fixed L', the optimal P minimizes ||L' - L||_F
subject to P^2 = I, which we relax to optimizing over symmetric orthogonal
matrices and then snap to the nearest involution.
"""

import numpy as np
from scipy.optimize import minimize
from dataclasses import dataclass
from typing import Optional
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from prism.core import (
    parity_eigenbasis, matrix_to_blocks, blocks_to_matrix,
    blocks_to_params, params_to_blocks, proximity_loss, PrismResult
)


@dataclass
class UnsupervisedResult:
    L_constrained: np.ndarray
    P_learned: np.ndarray
    original_eigenvalues: np.ndarray
    constrained_eigenvalues: np.ndarray
    duality_defect_original: float
    duality_defect_final: float
    rmse: float
    n_outer_iterations: int
    converged: bool
    community_labels: np.ndarray  # Fiedler clustering on L_constrained


def project_onto_commutant(L: np.ndarray, P: np.ndarray) -> np.ndarray:
    """
    Project L onto the commutant of P: find closest L' with [L', P] = 0.

    For a symmetric involution P with eigenvalues ±1, this is exact:
    decompose into P-eigenbasis, zero out off-diagonal blocks, reconstruct.
    """
    evals, evecs = np.linalg.eigh(P)
    idx_minus = np.where(evals < 0)[0]
    idx_plus = np.where(evals >= 0)[0]
    U = evecs

    M_plus, M_minus = matrix_to_blocks(L, U, idx_plus, idx_minus)
    return blocks_to_matrix(M_plus, M_minus, U, idx_plus, idx_minus, L.shape[0])


def commutator_norm(L: np.ndarray, P: np.ndarray) -> float:
    return np.linalg.norm(L @ P - P @ L, 'fro')


def optimize_P_given_L(L_constrained: np.ndarray, n: int,
                        P_init: np.ndarray, reg: float = 1e-4) -> np.ndarray:
    """
    Given fixed L', find P (symmetric involution) minimizing ||[L', P]||_F.

    We parameterize P = Q D Q^T where Q is orthogonal and D = diag(±1).
    For gradient descent, we relax to: minimize over symmetric matrices S
    with ||S||_F = sqrt(n), then snap to nearest involution via eigendecomposition.

    Relaxed objective: minimize ||[L', S]||_F^2 + reg * ||S^T S - I||_F^2
    """
    def loss(params):
        S = params.reshape(n, n)
        S_sym = (S + S.T) / 2
        comm = L_constrained @ S_sym - S_sym @ L_constrained
        comm_loss = np.sum(comm ** 2)
        # Soft orthogonality: S^T S ~ I
        orth_loss = np.sum((S_sym @ S_sym - np.eye(n)) ** 2)
        return comm_loss + reg * orth_loss

    def grad(params):
        S = params.reshape(n, n)
        S_sym = (S + S.T) / 2
        comm = L_constrained @ S_sym - S_sym @ L_constrained
        # Gradient of comm_loss w.r.t. S_sym
        g_comm = 2 * (L_constrained.T @ comm - comm @ L_constrained.T)
        # Gradient of orth_loss w.r.t. S_sym
        g_orth = 4 * S_sym @ (S_sym @ S_sym - np.eye(n))
        g_total = g_comm + reg * g_orth
        # Symmetrize (since S_sym = (S+S^T)/2, chain rule gives factor 1)
        g_sym = (g_total + g_total.T) / 2
        return g_sym.ravel()

    result = minimize(
        loss, P_init.ravel(), jac=grad,
        method='L-BFGS-B',
        options={'maxiter': 200, 'ftol': 1e-10}
    )
    S_opt = result.x.reshape(n, n)
    S_sym = (S_opt + S_opt.T) / 2

    # Snap to nearest symmetric involution: eigendecompose, snap evals to ±1
    evals, evecs = np.linalg.eigh(S_sym)
    evals_snapped = np.where(evals >= 0, 1.0, -1.0)
    P_new = evecs @ np.diag(evals_snapped) @ evecs.T
    return P_new


def fiedler_clustering(L: np.ndarray) -> np.ndarray:
    _, evecs = np.linalg.eigh(L)
    return (evecs[:, 1] >= 0).astype(int)


def unsupervised_prism(
    adjacency: np.ndarray,
    n_outer: int = 15,
    reg_L: float = 1e-6,
    reg_P: float = 1e-3,
    tol: float = 1e-6,
    verbose: bool = True,
) -> UnsupervisedResult:
    """
    Jointly optimize L' and P without any reference graph.

    Args:
        adjacency: n×n adjacency matrix
        n_outer: max alternating optimization iterations
        reg_L: regularization for L' optimization
        reg_P: regularization for P optimization (orthogonality penalty)
        tol: convergence tolerance on ||[L', P]||_F
        verbose: print iteration progress
    """
    A = np.asarray(adjacency, dtype=float)
    n = A.shape[0]
    D = np.diag(A.sum(axis=1))
    L = D - A
    L = (L + L.T) / 2

    original_eigs = np.sort(np.linalg.eigvalsh(L))
    defect_original = commutator_norm(L, np.eye(n)[::-1])

    # Initialize P from the graph's own Fiedler vector — no external reference.
    # This is the key difference from supervised mode: we use the noisy graph's
    # own spectral structure as the starting point for P.
    from prism.core import learned_parity_operator
    P = learned_parity_operator(L)

    if verbose:
        print(f"  Unsupervised Prism: n={n}, max_outer={n_outer}")
        print(f"  Initial duality defect (index-reversal P): {defect_original:.4f}")
        print(f"  {'Iter':>5}  {'||[L\',P]||':>12}  {'RMSE':>8}  {'Acc':>6}")

    L_constrained = L.copy()
    prev_defect = np.inf

    for it in range(n_outer):
        # Step 1: fix P, project L onto commutant of P
        L_constrained = project_onto_commutant(L, P)

        # Step 2: fix L', optimize P
        P = optimize_P_given_L(L_constrained, n, P, reg=reg_P)

        defect = commutator_norm(L_constrained, P)
        spectral_shift = np.sort(np.linalg.eigvalsh(L_constrained)) - original_eigs
        rmse = np.sqrt(np.mean(spectral_shift ** 2))

        if verbose:
            labels = fiedler_clustering(L_constrained)
            # Can't compute accuracy without ground truth here; show defect
            print(f"  {it+1:>5}  {defect:>12.6f}  {rmse:>8.4f}")

        if abs(prev_defect - defect) < tol and defect < 1e-4:
            if verbose:
                print(f"  Converged at iteration {it+1}")
            break
        prev_defect = defect

    constrained_eigs = np.sort(np.linalg.eigvalsh(L_constrained))
    spectral_shift = constrained_eigs - original_eigs
    rmse = np.sqrt(np.mean(spectral_shift ** 2))
    labels = fiedler_clustering(L_constrained)

    return UnsupervisedResult(
        L_constrained=L_constrained,
        P_learned=P,
        original_eigenvalues=original_eigs,
        constrained_eigenvalues=constrained_eigs,
        duality_defect_original=defect_original,
        duality_defect_final=commutator_norm(L_constrained, P),
        rmse=rmse,
        n_outer_iterations=it + 1,
        converged=defect < 1e-3,
        community_labels=labels,
    )
