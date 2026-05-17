"""
Prism multi-community extension: Z_2^r group action for k-way clustering.

Theory
------
Single-P Prism uses one involution P (Z_2 action) giving a 2-block decomposition.
For k communities, we use r = ceil(log2(k)) commuting involutions P_1,...,P_r
whose joint eigenspaces partition nodes into up to 2^r groups.

The UCA constraint generalizes: [L', P_i] = 0 for all i simultaneously.
This is equivalent to L' being block-diagonal in the joint eigenbasis of
{P_1,...,P_r}, where each block corresponds to a sign pattern (s_1,...,s_r)
with s_i in {+1,-1}.

Joint eigenbasis construction:
  - Each P_i has eigenvalues ±1
  - Since [P_i, P_j] = 0, they share a common eigenbasis
  - The joint eigenbasis diagonalizes all P_i simultaneously
  - Each node gets a binary label (s_1,...,s_r) in {±1}^r
  - Nodes with the same label are in the same block

Optimization:
  Step 1 (fix P_1,...,P_r): project L onto joint commutant (exact, closed-form)
  Step 2 (fix L'): optimize each P_i to minimize sum_i ||[L', P_i]||_F^2
                   subject to P_i^2 = I, P_i = P_i^T, [P_i, P_j] = 0

The commutativity constraint [P_i, P_j] = 0 is enforced by parameterizing
all P_i as functions of a shared orthogonal matrix Q:
  P_i = Q D_i Q^T  where D_i = diag(±1)
This guarantees [P_i, P_j] = 0 automatically (they share eigenbasis Q).

Community assignment:
  Each node gets a binary string label from its joint eigenspace.
  Map binary strings to community indices 0,...,k-1.
  Use k-means on the joint eigenvector embedding to handle k < 2^r.
"""

import numpy as np
from scipy.optimize import minimize
from dataclasses import dataclass
from typing import List, Tuple
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


@dataclass
class MultiPrismResult:
    L_constrained: np.ndarray
    P_list: List[np.ndarray]       # r learned involutions
    Q_shared: np.ndarray           # shared eigenbasis
    original_eigenvalues: np.ndarray
    constrained_eigenvalues: np.ndarray
    duality_defect_original: float
    duality_defect_final: float    # sum of ||[L',P_i]||_F
    rmse: float
    n_outer_iterations: int
    converged: bool
    joint_labels: np.ndarray       # binary string label per node (as int)
    n_blocks: int                  # actual number of non-empty blocks


def commutator_norm_sum(L: np.ndarray, P_list: List[np.ndarray]) -> float:
    """Sum of ||[L, P_i]||_F over all i."""
    return sum(np.linalg.norm(L @ P - P @ L, 'fro') for P in P_list)


def build_P_list(Q: np.ndarray, sign_patterns: np.ndarray) -> List[np.ndarray]:
    """
    Build r involutions from shared eigenbasis Q and sign patterns.
    sign_patterns: (r, n) array of ±1 values, each row is D_i diagonal.
    P_i = Q @ diag(sign_patterns[i]) @ Q.T
    """
    return [Q @ np.diag(sign_patterns[i].astype(float)) @ Q.T
            for i in range(len(sign_patterns))]


def project_onto_joint_commutant(L: np.ndarray,
                                  Q: np.ndarray,
                                  sign_patterns: np.ndarray) -> np.ndarray:
    """
    Project L onto the joint commutant of all P_i.

    Since all P_i share eigenbasis Q, the joint commutant consists of
    matrices that are block-diagonal in the Q basis, where blocks are
    defined by joint eigenspace (same sign pattern across all P_i).

    Algorithm:
      1. Rotate L into Q basis: L_rot = Q^T L Q
      2. For each pair (i,j), zero out L_rot[i,j] if nodes i,j have
         different joint eigenspace labels
      3. Rotate back: L' = Q L_rot Q^T
    """
    n = L.shape[0]
    r = len(sign_patterns)

    # Joint label for each basis vector: integer encoding of sign pattern
    # sign_patterns: (r, n), each column is the sign vector for that basis vector
    # Label = binary encoding: +1 -> 1, -1 -> 0
    labels = np.zeros(n, dtype=int)
    for i in range(r):
        bit = (sign_patterns[i] > 0).astype(int)
        labels += bit * (2 ** i)

    # Rotate L into Q basis
    L_rot = Q.T @ L @ Q

    # Zero out off-block entries
    L_block = np.zeros_like(L_rot)
    for a in range(n):
        for b in range(n):
            if labels[a] == labels[b]:
                L_block[a, b] = L_rot[a, b]

    # Rotate back
    return Q @ L_block @ Q.T


def initialize_Q_and_signs(L: np.ndarray, r: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Initialize shared eigenbasis Q and sign patterns from spectral structure of L.

    Strategy: use the first r+1 non-trivial eigenvectors of L to define
    r binary splits. Each split i uses eigenvector i+1: sign = sign(v_{i+1}).
    Q is initialized as the full eigenbasis of L.
    """
    n = L.shape[0]
    eigenvalues, eigenvectors = np.linalg.eigh(L)

    # Q = full eigenbasis of L (orthogonal by construction)
    Q = eigenvectors.copy()

    # Sign patterns: for each of r involutions, use eigenvector i+1
    # sign_patterns[i, j] = sign of eigenvector i+1 at position j
    sign_patterns = np.ones((r, n))
    for i in range(r):
        ev_idx = min(i + 1, n - 1)  # eigenvector index (skip trivial)
        v = eigenvectors[:, ev_idx]
        sign_patterns[i] = np.where(v >= 0, 1.0, -1.0)

    return Q, sign_patterns


def optimize_signs_given_Q_and_L(L_constrained: np.ndarray,
                                   Q: np.ndarray,
                                   sign_patterns: np.ndarray,
                                   r: int) -> np.ndarray:
    """
    Given fixed Q and L', optimize sign patterns to minimize
    sum_i ||[L', P_i]||_F^2.

    Since P_i = Q D_i Q^T, we have:
    [L', P_i] = L' Q D_i Q^T - Q D_i Q^T L'
    Let M = Q^T L' Q (L' in Q basis). Then:
    Q^T [L', P_i] Q = M D_i - D_i M

    ||[L', P_i]||_F^2 = ||M D_i - D_i M||_F^2
                      = sum_{a!=b} (D_i[a] - D_i[b])^2 * M[a,b]^2
                      = 4 * sum_{a!=b, sign_i[a]!=sign_i[b]} M[a,b]^2

    To minimize: for each involution i, we want to assign signs so that
    large |M[a,b]| entries have the same sign (same block).
    This is a graph partitioning problem: minimize cut weight where
    edge weight = M[a,b]^2.

    Greedy approach: for each involution i independently, find the
    binary partition of {0,...,n-1} minimizing sum of cross-partition
    M[a,b]^2. This is the minimum bisection problem (NP-hard in general),
    but we use spectral relaxation: sign of leading eigenvector of M^2.
    """
    n = Q.shape[0]
    M = Q.T @ L_constrained @ Q  # L' in Q basis

    new_signs = sign_patterns.copy()
    for i in range(r):
        # Weight matrix: W[a,b] = M[a,b]^2 (cost of putting a,b in different blocks)
        W = M ** 2
        np.fill_diagonal(W, 0)
        # Spectral bisection: sign of Fiedler vector of W's Laplacian
        D_w = np.diag(W.sum(axis=1))
        L_w = D_w - W
        _, evecs_w = np.linalg.eigh(L_w)
        fiedler_w = evecs_w[:, 1]  # second eigenvector
        new_signs[i] = np.where(fiedler_w >= 0, 1.0, -1.0)

    return new_signs


def multi_prism(
    adjacency: np.ndarray,
    k: int,
    n_outer: int = 20,
    tol: float = 1e-5,
    verbose: bool = True,
) -> MultiPrismResult:
    """
    Multi-community Prism: jointly optimize L' and r commuting involutions.

    Args:
        adjacency: n×n adjacency matrix
        k: number of communities
        n_outer: max alternating optimization iterations
        tol: convergence tolerance
        verbose: print iteration progress
    """
    A = np.asarray(adjacency, dtype=float)
    n = A.shape[0]
    D = np.diag(A.sum(axis=1))
    L = D - A
    L = (L + L.T) / 2

    r = int(np.ceil(np.log2(k)))  # number of involutions needed
    original_eigs = np.sort(np.linalg.eigvalsh(L))

    # Initial duality defect with index-reversal P
    P_init = np.eye(n)[::-1]
    defect_original = np.linalg.norm(L @ P_init - P_init @ L, 'fro')

    if verbose:
        print(f"  Multi-Prism: n={n}, k={k}, r={r} involutions")
        print(f"  Initial duality defect (single index-reversal P): {defect_original:.4f}")
        print(f"  {'Iter':>5}  {'sum||[L,Pi]||':>15}  {'RMSE':>8}")

    # Initialize
    Q, sign_patterns = initialize_Q_and_signs(L, r)
    L_constrained = L.copy()
    prev_defect = np.inf

    for it in range(n_outer):
        # Step 1: fix Q and sign_patterns, project L onto joint commutant
        L_constrained = project_onto_joint_commutant(L, Q, sign_patterns)

        # Step 2: fix L', optimize sign patterns
        sign_patterns = optimize_signs_given_Q_and_L(
            L_constrained, Q, sign_patterns, r)

        # Compute metrics
        P_list = build_P_list(Q, sign_patterns)
        defect = commutator_norm_sum(L_constrained, P_list)
        spectral_shift = np.sort(np.linalg.eigvalsh(L_constrained)) - original_eigs
        rmse = np.sqrt(np.mean(spectral_shift ** 2))

        if verbose:
            print(f"  {it+1:>5}  {defect:>15.6f}  {rmse:>8.4f}")

        if abs(prev_defect - defect) < tol:
            if verbose:
                print(f"  Converged at iteration {it+1}")
            break
        prev_defect = defect

    # Compute joint labels: each node gets an integer label from sign pattern
    # sign_patterns[i, j] = ±1 for involution i, basis vector j
    # But we need node labels, not basis vector labels.
    # Node j's label in the Q basis is sign_patterns[:, j].
    # Map to integer: +1 -> 1, -1 -> 0, binary encoding.
    joint_labels = np.zeros(n, dtype=int)
    for i in range(r):
        bit = (sign_patterns[i] > 0).astype(int)
        joint_labels += bit * (2 ** i)

    # Remap to 0,...,n_blocks-1
    unique_labels = np.unique(joint_labels)
    n_blocks = len(unique_labels)
    label_map = {old: new for new, old in enumerate(unique_labels)}
    joint_labels = np.array([label_map[l] for l in joint_labels])

    constrained_eigs = np.sort(np.linalg.eigvalsh(L_constrained))
    spectral_shift = constrained_eigs - original_eigs
    rmse = np.sqrt(np.mean(spectral_shift ** 2))
    P_list = build_P_list(Q, sign_patterns)
    defect_final = commutator_norm_sum(L_constrained, P_list)

    return MultiPrismResult(
        L_constrained=L_constrained,
        P_list=P_list,
        Q_shared=Q,
        original_eigenvalues=original_eigs,
        constrained_eigenvalues=constrained_eigs,
        duality_defect_original=defect_original,
        duality_defect_final=defect_final,
        rmse=rmse,
        n_outer_iterations=it + 1,
        converged=defect_final < 1e-3,
        joint_labels=joint_labels,
        n_blocks=n_blocks,
    )
