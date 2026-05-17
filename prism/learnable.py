"""
Prism v0.2: Learnable duality operator.

Problem with v0.1: for index-reversal P, the optimal L' = (L + PLP)/2
has a closed-form solution. Prism's optimizer just rediscovers it —
no advantage over a one-line baseline.

Fix: make P learnable. Instead of fixing P = index-reversal, we learn
a permutation matrix P(Z) from node embeddings Z, jointly with L'.

The duality operator P should satisfy:
  - P^2 = I  (involution: applying duality twice returns to start)
  - P^T = P  (symmetric, since P is a permutation)
  - [L', P] = 0  (duality constraint)

We relax P to a doubly-stochastic matrix via Sinkhorn normalization,
then penalize deviation from P^2 = I. This makes the problem differentiable.

Joint loss:
  L(L', Z) = ||L' - L||_F^2          # proximity: stay close to original
            + alpha * ||[L', P(Z)]||_F^2  # duality: L' commutes with P
            + beta  * ||P(Z)^2 - I||_F^2  # involution: P is its own inverse
            + gamma * R_community(Z)       # community: P reveals structure

The community regularizer R encourages P to be a block permutation
(nodes in one community map to nodes in another), not a random shuffle.
We use: R = -||P(Z) - P(Z)^T||_F^2 / n  (penalize asymmetry in P,
since a block permutation between two equal communities is symmetric).

Output:
  - L': UCA-constrained Laplacian
  - P*: learned duality operator (reveals hidden mirror structure)
  - duality_defect: ||[L', P*]||_F (how well constraint is satisfied)
  - involution_defect: ||P*^2 - I||_F (how close P* is to true involution)
"""

import numpy as np
from scipy.optimize import minimize
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LearnableResult:
    original_eigenvalues: np.ndarray
    constrained_eigenvalues: np.ndarray
    learned_P: np.ndarray
    duality_defect_original: float
    duality_defect_constrained: float
    involution_defect: float          # ||P^2 - I||_F
    spectral_rmse: float
    frobenius_dist: float
    n_iterations: int
    converged: bool
    loss_history: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Sinkhorn normalization: Z -> doubly-stochastic matrix
# ---------------------------------------------------------------------------

def sinkhorn(Z: np.ndarray, n_iter: int = 20) -> np.ndarray:
    """
    Sinkhorn normalization: turn any matrix into a doubly-stochastic matrix.
    Alternately normalize rows and columns to sum to 1.
    """
    P = np.exp(Z - Z.max())  # softmax-style stability
    for _ in range(n_iter):
        P = P / (P.sum(axis=1, keepdims=True) + 1e-10)
        P = P / (P.sum(axis=0, keepdims=True) + 1e-10)
    return P


def sinkhorn_grad(Z: np.ndarray, n_iter: int = 20) -> np.ndarray:
    """Same as sinkhorn but returns the matrix (for use in loss computation)."""
    return sinkhorn(Z, n_iter)


# ---------------------------------------------------------------------------
# Block-diagonal parameterization for L' given P
# ---------------------------------------------------------------------------

def commutant_projection(L: np.ndarray, P: np.ndarray) -> np.ndarray:
    """
    Project L onto the commutant of P: {M : [M, P] = 0}.

    For a general (non-involution) P, the commutant projection is:
      L' = (1/k) * sum_{j=0}^{k-1} P^j L P^{-j}
    For an involution P (P^2 = I), this simplifies to:
      L' = (L + P L P) / 2
    We use the general form with k=2 (works well for near-involutions).
    """
    P2 = P @ P
    return (L + P @ L @ P.T + P2 @ L @ P2.T) / 3


# ---------------------------------------------------------------------------
# Joint loss function
# ---------------------------------------------------------------------------

def joint_loss(
    params: np.ndarray,
    L_orig: np.ndarray,
    n: int,
    alpha: float = 1.0,
    beta: float = 0.5,
    gamma: float = 0.1,
    sinkhorn_iters: int = 20,
) -> float:
    """
    Joint loss over (L'_params, Z_params).

    params layout:
      - first n*n entries: Z (node embedding matrix for P)
      - remaining entries: upper triangle of L' (symmetric)
    """
    # Unpack
    Z = params[:n * n].reshape(n, n)
    n_L = n * (n + 1) // 2
    L_params = params[n * n: n * n + n_L]

    # Reconstruct L' (symmetric)
    L_prime = np.zeros((n, n))
    idx = 0
    for i in range(n):
        for j in range(i, n):
            L_prime[i, j] = L_params[idx]
            L_prime[j, i] = L_params[idx]
            idx += 1

    # Compute P via Sinkhorn
    P = sinkhorn(Z, sinkhorn_iters)

    # Loss terms
    # 1. Proximity
    proximity = np.sum((L_prime - L_orig) ** 2)

    # 2. Duality: [L', P] = L'P - PL'
    commutator = L_prime @ P - P @ L_prime
    duality = np.sum(commutator ** 2)

    # 3. Involution: P^2 ~ I
    P2 = P @ P
    involution = np.sum((P2 - np.eye(n)) ** 2)

    # 4. Community regularizer: encourage P to be symmetric (block structure)
    community = -np.sum((P - P.T) ** 2) / n  # negative: penalize asymmetry

    loss = proximity + alpha * duality + beta * involution + gamma * community
    return float(loss)


def joint_loss_and_grad(
    params: np.ndarray,
    L_orig: np.ndarray,
    n: int,
    alpha: float,
    beta: float,
    gamma: float,
    sinkhorn_iters: int,
    eps: float = 1e-5,
) -> tuple:
    """Numerical gradient for joint loss (finite differences)."""
    f0 = joint_loss(params, L_orig, n, alpha, beta, gamma, sinkhorn_iters)
    grad = np.zeros_like(params)
    for i in range(len(params)):
        params_p = params.copy()
        params_p[i] += eps
        grad[i] = (joint_loss(params_p, L_orig, n, alpha, beta, gamma, sinkhorn_iters) - f0) / eps
    return f0, grad


# ---------------------------------------------------------------------------
# Main optimizer
# ---------------------------------------------------------------------------

def optimize_learnable(
    L: np.ndarray,
    alpha: float = 1.0,
    beta: float = 0.5,
    gamma: float = 0.1,
    max_iter: int = 500,
    tol: float = 1e-8,
    sinkhorn_iters: int = 20,
    verbose: bool = False,
    random_seed: int = 42,
) -> LearnableResult:
    """
    Joint optimization of L' and learnable duality operator P.

    Args:
        L: graph Laplacian (n x n symmetric)
        alpha: weight for duality constraint ||[L', P]||^2
        beta: weight for involution constraint ||P^2 - I||^2
        gamma: weight for community regularizer
        max_iter: maximum optimizer iterations
        tol: convergence tolerance
        sinkhorn_iters: Sinkhorn normalization iterations
        verbose: print progress
        random_seed: for reproducibility

    Returns:
        LearnableResult with learned P and constrained L'
    """
    n = L.shape[0]
    L_sym = (L + L.T) / 2
    rng = np.random.default_rng(random_seed)

    # Initial P: random initialization to avoid identity local minimum
    # Use a random doubly-stochastic matrix as starting point
    Z0 = rng.standard_normal((n, n))

    # Initial L': start at L itself
    n_L = n * (n + 1) // 2
    L0_params = np.array([L_sym[i, j] for i in range(n) for j in range(i, n)])

    x0 = np.concatenate([Z0.ravel(), L0_params])

    original_eigs = np.sort(np.linalg.eigvalsh(L_sym))
    P0 = sinkhorn(Z0, sinkhorn_iters)
    defect_original = np.linalg.norm(L_sym @ P0 - P0 @ L_sym, 'fro')

    if verbose:
        print(f"  n={n}, params={len(x0)}, alpha={alpha}, beta={beta}, gamma={gamma}")
        print(f"  Initial duality defect (with P~I): {defect_original:.4f}")

    loss_history = []

    def callback(xk):
        loss_history.append(joint_loss(xk, L_sym, n, alpha, beta, gamma, sinkhorn_iters))

    result = minimize(
        joint_loss,
        x0,
        args=(L_sym, n, alpha, beta, gamma, sinkhorn_iters),
        method='L-BFGS-B',
        jac=None,  # numerical gradient via scipy
        options={'maxiter': max_iter, 'ftol': tol, 'gtol': 1e-8},
        callback=callback,
    )

    # Extract results
    Z_final = result.x[:n * n].reshape(n, n)
    L_params_final = result.x[n * n: n * n + n_L]

    P_final = sinkhorn(Z_final, sinkhorn_iters)

    L_prime = np.zeros((n, n))
    idx = 0
    for i in range(n):
        for j in range(i, n):
            L_prime[i, j] = L_params_final[idx]
            L_prime[j, i] = L_params_final[idx]
            idx += 1

    constrained_eigs = np.sort(np.linalg.eigvalsh(L_prime))
    defect_final = np.linalg.norm(L_prime @ P_final - P_final @ L_prime, 'fro')
    involution_defect = np.linalg.norm(P_final @ P_final - np.eye(n), 'fro')
    spectral_rmse = float(np.sqrt(np.mean((constrained_eigs - original_eigs) ** 2)))
    frob_dist = float(np.linalg.norm(L_prime - L_sym, 'fro'))

    if verbose:
        print(f"  Final duality defect: {defect_final:.6f}")
        print(f"  Involution defect ||P^2-I||: {involution_defect:.6f}")
        print(f"  Spectral RMSE: {spectral_rmse:.6f}")
        print(f"  Frobenius dist: {frob_dist:.6f}")
        print(f"  Converged: {result.success}, iterations: {result.nit}")

    return LearnableResult(
        original_eigenvalues=original_eigs,
        constrained_eigenvalues=constrained_eigs,
        learned_P=P_final,
        duality_defect_original=defect_original,
        duality_defect_constrained=defect_final,
        involution_defect=involution_defect,
        spectral_rmse=spectral_rmse,
        frobenius_dist=frob_dist,
        n_iterations=result.nit,
        converged=result.success,
        loss_history=loss_history,
        metadata={
            "n": n,
            "alpha": alpha,
            "beta": beta,
            "gamma": gamma,
            "final_loss": float(result.fun),
        },
    )


# ---------------------------------------------------------------------------
# Interpret the learned P
# ---------------------------------------------------------------------------

def optimize_learnable_multistart(
    L: np.ndarray,
    alpha: float = 1.0,
    beta: float = 0.5,
    gamma: float = 0.1,
    max_iter: int = 500,
    tol: float = 1e-8,
    n_starts: int = 5,
    verbose: bool = False,
) -> LearnableResult:
    """
    Multi-start version of optimize_learnable.
    Runs n_starts random initializations and returns the best result
    (lowest final loss). Avoids identity local minimum.
    """
    best_result = None
    best_loss = float('inf')

    for seed in range(n_starts):
        result = optimize_learnable(
            L, alpha=alpha, beta=beta, gamma=gamma,
            max_iter=max_iter, tol=tol, verbose=False,
            random_seed=seed * 17 + 3,
        )
        loss = result.metadata.get("final_loss", float('inf'))
        if loss < best_loss:
            best_loss = loss
            best_result = result
        if verbose:
            print(f"  Start {seed+1}/{n_starts}: loss={loss:.6f}, "
                  f"defect={result.duality_defect_constrained:.4f}, "
                  f"involution={result.involution_defect:.4f}")

    return best_result


def interpret_P(P: np.ndarray, threshold: float = 0.3) -> dict:
    """
    Interpret the learned duality operator P.

    For each node i, find its 'dual' node: argmax_j P[i,j].
    If P is a near-permutation, this gives a node pairing.
    If P is block-structured, this reveals community mirror structure.

    Returns:
        - node_pairs: list of (i, j) pairs where j = argmax P[i,:]
        - is_involution: whether the pairing is self-consistent (i->j->i)
        - block_structure: detected block assignments
    """
    n = P.shape[0]
    dual_of = [int(np.argmax(P[i])) for i in range(n)]

    # Check involution: i -> j -> i?
    involution_pairs = [(i, dual_of[i]) for i in range(n) if dual_of[dual_of[i]] == i]
    is_involution = len(involution_pairs) == n

    # Detect block structure: nodes that map to themselves vs others
    self_dual = [i for i in range(n) if dual_of[i] == i]
    cross_dual = [(i, dual_of[i]) for i in range(n) if dual_of[i] != i]

    # Deduplicate cross pairs
    seen = set()
    unique_pairs = []
    for i, j in cross_dual:
        key = (min(i, j), max(i, j))
        if key not in seen:
            seen.add(key)
            unique_pairs.append((i, j))

    return {
        "dual_of": dual_of,
        "is_involution": is_involution,
        "self_dual_nodes": self_dual,
        "cross_dual_pairs": unique_pairs,
        "n_pairs": len(unique_pairs),
        "n_self_dual": len(self_dual),
    }
