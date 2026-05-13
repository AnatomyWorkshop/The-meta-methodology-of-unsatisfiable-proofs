"""
Distribution samplers for algebraic circuit experiments.

D+: matrices where Permanent is "hard" — random matrices over GF(p).
    For random matrices, Permanent is generically nonzero and hard to compute.

D-: matrices where Determinant is "easy" — rank-1 matrices (outer products).
    For rank-1 matrices M = u * v^T, Permanent(M) = product(u) * product(v) * (n-1)!
    and Determinant(M) = 0 (rank 1 ⟹ det = 0 for n > 1).

The key structural difference:
  - D+ matrices: Permanent ≠ 0 with high probability, no algebraic shortcut
  - D- matrices: Determinant = 0 always, Permanent has a closed form

A circuit that can distinguish D+ from D- is detecting the rank-1 structure,
which requires computing something at least as hard as Permanent.
"""

import random
from typing import Tuple


def sample_d_plus(n: int, p: int) -> Tuple[int, ...]:
    """
    D+: uniformly random n×n matrix over GF(p).
    Permanent is generically nonzero; no polynomial-size algebraic shortcut known.
    """
    return tuple(random.randrange(1, p) for _ in range(n * n))


def sample_d_minus(n: int, p: int) -> Tuple[int, ...]:
    """
    D-: rank-1 matrix M = u * v^T over GF(p).
    Determinant = 0 (for n > 1). Permanent = prod(u) * prod(v) * (n-1)! mod p.
    These are "easy" matrices: their algebraic structure is polynomial-time detectable.
    """
    u = [random.randrange(1, p) for _ in range(n)]
    v = [random.randrange(1, p) for _ in range(n)]
    flat = []
    for i in range(n):
        for j in range(n):
            flat.append((u[i] * v[j]) % p)
    return tuple(flat)


def sample_d_minus_low_rank(n: int, p: int, rank: int = 2) -> Tuple[int, ...]:
    """
    D-: rank-r matrix (r < n). Determinant = 0. Permanent has structured form.
    Used for harder negative examples.
    """
    rank = min(rank, n)
    # Build as sum of rank outer products
    matrix = [[0] * n for _ in range(n)]
    for _ in range(rank):
        u = [random.randrange(0, p) for _ in range(n)]
        v = [random.randrange(0, p) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                matrix[i][j] = (matrix[i][j] + u[i] * v[j]) % p
    return tuple(matrix[i][j] for i in range(n) for j in range(n))
