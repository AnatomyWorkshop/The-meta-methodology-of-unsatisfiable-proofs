"""
Prism core: UCA duality-constrained spectral optimizer for networks.

Given a network's Laplacian L, find L' closest to L such that [L', P] = 0,
where P is the duality operator (index reversal / graph symmetry).

The UCA constraint means: the system's internal evolution (L) must be
self-consistent under duality conjugation. This restricts the admissible
spectrum to a subset of all possible eigenvalue configurations.

Algorithm (adapted from Phase 6 Hilbert-Polya optimizer):
  1. Compute graph Laplacian L = D - A
  2. Define duality operator P (default: index reversal)
  3. Decompose into P-eigenbasis (even/odd sectors)
  4. Optimize L within block-diagonal subspace to minimize ||L' - L||
     while enforcing [L', P] = 0 exactly
  5. Compare original vs constrained spectrum
"""

import numpy as np
from scipy.optimize import minimize
from dataclasses import dataclass


@dataclass
class PrismResult:
    original_eigenvalues: np.ndarray
    constrained_eigenvalues: np.ndarray
    duality_defect_original: float
    duality_defect_constrained: float
    spectral_shift: np.ndarray
    rmse: float
    max_shift: float
    n_iterations: int
    converged: bool
    metadata: dict
    constrained_matrix: np.ndarray = None


def parity_operator(n: int) -> np.ndarray:
    """Index-reversal operator (anti-diagonal identity). Natural duality for networks."""
    return np.eye(n)[::-1]


def parity_eigenbasis(n: int):
    """Compute eigenbasis of P and return transformation matrix + sector indices."""
    P = parity_operator(n)
    evals, evecs = np.linalg.eigh(P)
    idx_minus = np.where(evals < 0)[0]
    idx_plus = np.where(evals >= 0)[0]
    return evecs, idx_plus, idx_minus


def matrix_to_blocks(M: np.ndarray, U: np.ndarray, idx_plus, idx_minus):
    """Project matrix into P-eigenbasis and extract diagonal blocks."""
    M_rot = U.T @ M @ U
    M_plus = M_rot[np.ix_(idx_plus, idx_plus)]
    M_minus = M_rot[np.ix_(idx_minus, idx_minus)]
    return M_plus.real, M_minus.real


def blocks_to_matrix(M_plus: np.ndarray, M_minus: np.ndarray,
                     U: np.ndarray, idx_plus, idx_minus, n: int) -> np.ndarray:
    """Reconstruct full matrix from two blocks in P-eigenbasis."""
    M_rot = np.zeros((n, n))
    M_rot[np.ix_(idx_plus, idx_plus)] = M_plus
    M_rot[np.ix_(idx_minus, idx_minus)] = M_minus
    return U @ M_rot @ U.T


def params_to_blocks(params: np.ndarray, m_plus: int, m_minus: int):
    """Convert flat parameter vector to two symmetric matrices."""
    k_plus = m_plus * (m_plus + 1) // 2

    def fill(p, size):
        M = np.zeros((size, size))
        idx = 0
        for i in range(size):
            for j in range(i, size):
                M[i, j] = p[idx]
                M[j, i] = p[idx]
                idx += 1
        return M

    return fill(params[:k_plus], m_plus), fill(params[k_plus:], m_minus)


def blocks_to_params(M_plus: np.ndarray, M_minus: np.ndarray) -> np.ndarray:
    """Extract upper-triangle parameters from two symmetric blocks."""
    def extract(M):
        size = M.shape[0]
        return np.array([M[i, j] for i in range(size) for j in range(i, size)])
    return np.concatenate([extract(M_plus), extract(M_minus)])


def proximity_loss(params: np.ndarray, U: np.ndarray, idx_plus, idx_minus,
                   n: int, m_plus: int, m_minus: int,
                   L_original: np.ndarray, reg: float = 1e-6) -> float:
    """
    Loss = ||L_constrained - L_original||_F^2 + reg * ||params||^2

    Minimizing this finds the closest UCA-compatible Laplacian to the original.
    """
    M_plus, M_minus = params_to_blocks(params, m_plus, m_minus)
    L_constrained = blocks_to_matrix(M_plus, M_minus, U, idx_plus, idx_minus, n)
    proximity = np.sum((L_constrained - L_original) ** 2)
    regularization = reg * np.sum(params ** 2)
    return proximity + regularization


def optimize(
    L: np.ndarray,
    reg: float = 1e-6,
    max_iter: int = 2000,
    tol: float = 1e-10,
    verbose: bool = False,
) -> PrismResult:
    """
    Find the closest UCA-compatible Laplacian to L.

    The UCA constraint [L', P] = 0 is enforced by construction via
    block-diagonal parameterization in the P-eigenbasis.
    """
    n = L.shape[0]
    assert L.shape == (n, n), f"Expected square matrix, got {L.shape}"

    L_sym = (L + L.T) / 2

    P = parity_operator(n)
    defect_original = np.linalg.norm(L_sym @ P - P @ L_sym, 'fro')

    U, idx_plus, idx_minus = parity_eigenbasis(n)
    m_plus = len(idx_plus)
    m_minus = len(idx_minus)

    M_plus_0, M_minus_0 = matrix_to_blocks(L_sym, U, idx_plus, idx_minus)
    x0 = blocks_to_params(M_plus_0, M_minus_0)

    original_eigs = np.sort(np.linalg.eigvalsh(L_sym))

    if verbose:
        print(f"  Network size: {n} nodes")
        print(f"  Even sector: {m_plus}, Odd sector: {m_minus}")
        print(f"  Free parameters: {len(x0)}")
        print(f"  Original duality defect: {defect_original:.6f}")
        print(f"  Optimizing...")

    result = minimize(
        proximity_loss,
        x0,
        args=(U, idx_plus, idx_minus, n, m_plus, m_minus, L_sym, reg),
        method='L-BFGS-B',
        options={'maxiter': max_iter, 'ftol': tol, 'gtol': 1e-12},
    )

    M_plus_f, M_minus_f = params_to_blocks(result.x, m_plus, m_minus)
    L_constrained = blocks_to_matrix(M_plus_f, M_minus_f, U, idx_plus, idx_minus, n)

    constrained_eigs = np.sort(np.linalg.eigvalsh(L_constrained))

    defect_constrained = np.linalg.norm(L_constrained @ P - P @ L_constrained, 'fro')

    spectral_shift = constrained_eigs - original_eigs
    rmse = np.sqrt(np.mean(spectral_shift ** 2))
    max_shift = np.max(np.abs(spectral_shift))

    return PrismResult(
        original_eigenvalues=original_eigs,
        constrained_eigenvalues=constrained_eigs,
        duality_defect_original=defect_original,
        duality_defect_constrained=defect_constrained,
        spectral_shift=spectral_shift,
        rmse=rmse,
        max_shift=max_shift,
        n_iterations=result.nit,
        converged=result.success,
        metadata={
            "n": n,
            "m_plus": m_plus,
            "m_minus": m_minus,
            "reg": reg,
            "final_loss": float(result.fun),
        },
        constrained_matrix=L_constrained,
    )


def learned_parity_operator(L: np.ndarray) -> np.ndarray:
    """
    Learn the intrinsic duality operator P from the network's spectral structure.

    Strategy: find the permutation matrix P that maximizes the block-diagonal
    structure of L in the P-eigenbasis, i.e., minimizes ||[L, P]||_F over all
    involutory permutation matrices P (P^2 = I, P != I).

    For a network with true community structure, the natural duality pairs nodes
    across communities. This is found by looking at the Fiedler vector: nodes
    with opposite signs in the Fiedler vector are natural duality partners.

    Returns an involutory symmetric matrix P with P^2 = I.
    """
    n = L.shape[0]
    eigenvalues, eigenvectors = np.linalg.eigh(L)

    # Fiedler vector: second eigenvector (first non-trivial)
    fiedler = eigenvectors[:, 1]

    # Sort nodes by Fiedler value
    order = np.argsort(fiedler)

    # Pair node i (low Fiedler) with node n-1-i (high Fiedler)
    # This creates a natural duality: nodes on opposite sides of the cut
    perm = np.zeros(n, dtype=int)
    for rank, node in enumerate(order):
        perm[node] = order[n - 1 - rank]

    # Build permutation matrix
    P = np.zeros((n, n))
    for i in range(n):
        P[i, perm[i]] = 1.0

    # Make it symmetric (average with transpose to handle non-involutory cases)
    P = (P + P.T) / 2
    # Re-normalize rows to keep it close to involutory
    # For a true pairing perm[perm[i]] = i, P is already symmetric and P^2 = I
    return P


def optimize_with_P(
    L: np.ndarray,
    P: np.ndarray,
    reg: float = 1e-6,
    max_iter: int = 2000,
    tol: float = 1e-10,
) -> PrismResult:
    """
    Find the closest UCA-compatible Laplacian to L using a given P operator.
    Same as optimize() but accepts an arbitrary P instead of index-reversal.
    """
    n = L.shape[0]
    L_sym = (L + L.T) / 2

    defect_original = np.linalg.norm(L_sym @ P - P @ L_sym, 'fro')

    # Compute P-eigenbasis
    evals, evecs = np.linalg.eigh(P)
    idx_minus = np.where(evals < 0)[0]
    idx_plus = np.where(evals >= 0)[0]
    U = evecs
    m_plus = len(idx_plus)
    m_minus = len(idx_minus)

    M_plus_0, M_minus_0 = matrix_to_blocks(L_sym, U, idx_plus, idx_minus)
    x0 = blocks_to_params(M_plus_0, M_minus_0)
    original_eigs = np.sort(np.linalg.eigvalsh(L_sym))

    result = minimize(
        proximity_loss,
        x0,
        args=(U, idx_plus, idx_minus, n, m_plus, m_minus, L_sym, reg),
        method='L-BFGS-B',
        options={'maxiter': max_iter, 'ftol': tol, 'gtol': 1e-12},
    )

    M_plus_f, M_minus_f = params_to_blocks(result.x, m_plus, m_minus)
    L_constrained = blocks_to_matrix(M_plus_f, M_minus_f, U, idx_plus, idx_minus, n)
    constrained_eigs = np.sort(np.linalg.eigvalsh(L_constrained))
    defect_constrained = np.linalg.norm(L_constrained @ P - P @ L_constrained, 'fro')
    spectral_shift = constrained_eigs - original_eigs
    rmse = np.sqrt(np.mean(spectral_shift ** 2))

    return PrismResult(
        original_eigenvalues=original_eigs,
        constrained_eigenvalues=constrained_eigs,
        duality_defect_original=defect_original,
        duality_defect_constrained=defect_constrained,
        spectral_shift=spectral_shift,
        rmse=rmse,
        max_shift=np.max(np.abs(spectral_shift)),
        n_iterations=result.nit,
        converged=result.success,
        metadata={"n": n, "m_plus": m_plus, "m_minus": m_minus,
                  "reg": reg, "final_loss": float(result.fun)},
        constrained_matrix=L_constrained,
    )


def analyze_network(adjacency: np.ndarray, **kwargs) -> PrismResult:
    """
    Main entry point: analyze a network's spectral structure under UCA constraints.

    Args:
        adjacency: n×n adjacency matrix (symmetric for undirected graphs)
        **kwargs: passed to optimize() (reg, max_iter, tol, verbose)

    Returns:
        PrismResult with original vs constrained spectrum comparison
    """
    A = np.asarray(adjacency, dtype=float)
    n = A.shape[0]
    D = np.diag(A.sum(axis=1))
    L = D - A
    return optimize(L, **kwargs)
