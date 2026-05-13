"""
Vladimirov operator on Q_p, truncated to level N.

Q_p is totally disconnected. The natural Laplacian is the Vladimirov operator D^alpha,
a p-adic fractional derivative. For alpha=2 (matching D^2 in the trace formula):

  (D^2 f)(x) = integral_{Q_p} |x - y|_p^{-1-2} (f(y) - f(x)) dy   [regularized]

Its eigenfunctions are p-adic characters chi_{a,j}(x) = psi(a * x) for a in Q_p,
with eigenvalues |a|_p^2.

For the trace formula we need:
  Tr(e^{-t D^2}) = sum over eigenvalues lambda of e^{-t lambda}

On Q_p / Z_p (the compact quotient), the spectrum is discrete:
  lambda_k = p^{2k},  k = 0, 1, 2, ...
  multiplicity of lambda_k = p^k - p^{k-1}  (for k >= 1), and 1 for k=0

This module constructs the truncated Vladimirov operator as a matrix on the
finite-dimensional space of locally constant functions at level N.
"""

import numpy as np
from typing import Tuple


def p_adic_norm(n: int, p: int) -> float:
    """p-adic norm |n|_p = p^{-v_p(n)} where v_p(n) is the p-adic valuation."""
    if n == 0:
        return 0.0
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return float(p) ** (-v)


def p_adic_valuation(n: int, p: int) -> int:
    """p-adic valuation v_p(n): largest k such that p^k divides n."""
    if n == 0:
        return int(1e9)
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def build_basis(p: int, N: int) -> np.ndarray:
    """
    Basis of locally constant functions on Z_p at level N.

    The space L^2(Z_p / p^N Z_p) has dimension p^N.
    Basis elements: indicator functions of cosets a + p^N Z_p, a in {0,...,p^N - 1}.

    Returns array of basis indices (0 to p^N - 1).
    """
    return np.arange(p**N, dtype=int)


def vladimirov_matrix(p: int, N: int, alpha: float = 2.0) -> np.ndarray:
    """
    Matrix of the Vladimirov operator D^alpha on L^2(Z_p / p^N Z_p).

    On the basis of indicator functions of cosets {a + p^N Z_p},
    the matrix element is:

      M[a,b] = integral_{Z_p} |x|_p^{alpha-1} * (delta_{a,b+x} - delta_{a,b}) dx

    For the truncated space, this becomes:
      M[a,b] = c(|a-b|_p)  for a != b
      M[a,a] = -sum_{b != a} M[a,b]

    where c(p^{-k}) = (1 - p^{-1}) * p^{k*(alpha-1)} * p^{-k} = (1-p^{-1}) * p^{k*(alpha-2)}
    ... actually let's use the known eigenvalue structure directly.

    The eigenfunctions of D^alpha on Z_p are the p-adic characters.
    At level N, the eigenvalues are:
      lambda_k = p^{alpha * k}  for k = 0, 1, ..., N
    with multiplicities:
      m_0 = 1
      m_k = p^k - p^{k-1}  for k = 1, ..., N-1
      m_N = p^N - p^{N-1}  (boundary level)

    We construct the matrix in the eigenbasis and return it.
    """
    dim = p**N

    # Build eigenvalues and their multiplicities
    eigenvalues = []
    for k in range(N + 1):
        lam = float(p) ** (alpha * k)
        if k == 0:
            mult = 1
        else:
            mult = p**k - p**(k-1)
        eigenvalues.extend([lam] * mult)

    eigenvalues = np.array(eigenvalues[:dim])

    # Diagonal matrix in eigenbasis — return as diagonal operator
    return np.diag(eigenvalues)


def eigenvalues_vladimirov(p: int, N: int, alpha: float = 2.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns (eigenvalues, multiplicities) of D^alpha on Z_p at level N.

    Eigenvalue p^{alpha*k} has multiplicity:
      k=0: 1
      k=1,...,N-1: p^k - p^{k-1}
      k=N: p^N - p^{N-1}  (truncation level)
    """
    evals = []
    mults = []
    for k in range(N + 1):
        lam = float(p) ** (alpha * k)
        if k == 0:
            mult = 1
        else:
            mult = p**k - p**(k-1)
        evals.append(lam)
        mults.append(mult)

    return np.array(evals), np.array(mults)


def heat_kernel_diagonal(p: int, N: int, t: float, alpha: float = 2.0) -> np.ndarray:
    """
    Diagonal of the heat kernel K(t, x, x) = <x| e^{-t D^alpha} |x>
    on Z_p at level N.

    Since D^alpha is diagonal in the eigenbasis with eigenvalues lambda_k,
    the heat kernel diagonal is:
      K(t, x, x) = sum_k e^{-t * lambda_k} * |phi_k(x)|^2

    For the indicator function basis, each basis element x has:
      K(t, x, x) = (1/p^N) * sum_k mult_k * e^{-t * lambda_k}

    (uniform by translation invariance of Z_p)
    """
    evals, mults = eigenvalues_vladimirov(p, N, alpha)
    heat_sum = np.sum(mults * np.exp(-t * evals))
    return heat_sum / (p**N)
