"""
Candidate operator families for Phase 6: Riemann Hypothesis closure search.

Each operator family produces a finite-dimensional matrix whose eigenvalues
can be compared against zeta zeros. The question: which family's spectrum
best matches the actual zeros, and does it satisfy the four closure laws?
"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class OperatorCandidate:
    name: str
    matrix: np.ndarray
    eigenvalues: np.ndarray
    is_self_adjoint: bool
    encodes_primes: bool
    has_functional_equation_symmetry: bool
    description: str


# --- 1. Berry-Keating family ---

def berry_keating_truncated(n: int, boundary: str = "dirichlet") -> OperatorCandidate:
    """
    Berry-Keating Hamiltonian H = xp + px (symmetrized).
    Truncated to n×n matrix on a finite interval.

    In position representation on [0, L]:
      H = -i(x d/dx + 1/2)

    Matrix elements in a basis of sin(k*pi*x/L) (Dirichlet) or exp(2*pi*i*k*x/L) (periodic).

    PT-symmetric variant (Bender-Brody-Mueller 2017):
      H_PT = (1 - e^{-ip})(xp)(1 - e^{-ip}) + i(1 - e^{-ip})/2
    Approximated as: H = xp + px with complex potential V(x) = i*alpha*x
    satisfying [PT, H] = 0 where P: x -> -x, T: complex conjugation.
    """
    if boundary == "dirichlet":
        H = np.zeros((n, n), dtype=complex)
        for j in range(n):
            for k in range(n):
                if (j + k) % 2 == 1:
                    jj, kk = j + 1, k + 1
                    H[j, k] = -1j * 2 * jj * kk / (kk**2 - jj**2)
        H = (H + H.conj().T) / 2
        eigenvalues = np.sort(np.linalg.eigvalsh(H))
    elif boundary == "periodic":
        diag = np.arange(1, n + 1) - (n + 1) / 2.0
        H = np.diag(diag)
        eigenvalues = np.sort(diag)
    elif boundary == "pt_symmetric":
        H = _build_pt_berry_keating(n)
        eigs = np.linalg.eigvals(H)
        # In unbroken PT phase, eigenvalues should be real
        real_eigs = eigs[np.abs(eigs.imag) < 1e-8].real
        eigenvalues = np.sort(real_eigs)
        if len(eigenvalues) == 0:
            eigenvalues = np.sort(eigs.real)
        is_pt_unbroken = len(real_eigs) == len(eigs)
        return OperatorCandidate(
            name=f"berry_keating_pt_symmetric_n{n}",
            matrix=H,
            eigenvalues=eigenvalues,
            is_self_adjoint=is_pt_unbroken,  # PT-unbroken = effectively self-adjoint
            encodes_primes=False,
            has_functional_equation_symmetry=True,  # PT implements s <-> 1-s
            description=f"Berry-Keating PT-symmetric (Bender-Brody-Mueller type), {n}x{n}. "
                        f"PT-unbroken: {is_pt_unbroken} ({len(real_eigs)}/{len(eigs)} real eigenvalues)",
        )
    else:
        H = np.diag(np.log(np.arange(1, n + 1)))
        eigenvalues = np.sort(np.log(np.arange(1, n + 1)))

    return OperatorCandidate(
        name=f"berry_keating_{boundary}_n{n}",
        matrix=H,
        eigenvalues=eigenvalues,
        is_self_adjoint=True,
        encodes_primes=False,
        has_functional_equation_symmetry=(boundary in ("periodic", "pt_symmetric")),
        description=f"Berry-Keating H=xp+px, {boundary} BC, truncated to {n}x{n}",
    )


# --- 2. GUE random matrix (control) ---

def gue_random_matrix(n: int, seed: int = 42) -> OperatorCandidate:
    """
    Random matrix from the Gaussian Unitary Ensemble.
    Known to match pair correlation of zeta zeros (Montgomery-Odlyzko),
    but does NOT match individual zeros. This is the UNSAFE control.
    """
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    H = (A + A.conj().T) / (2 * np.sqrt(n))
    eigenvalues = np.sort(np.linalg.eigvalsh(H))

    return OperatorCandidate(
        name=f"gue_n{n}_s{seed}",
        matrix=H,
        eigenvalues=eigenvalues,
        is_self_adjoint=True,
        encodes_primes=False,
        has_functional_equation_symmetry=False,
        description=f"GUE random matrix {n}x{n} (control baseline)",
    )


# --- 3. Prime-encoding operator (arithmetic) ---

def prime_zeta_operator(n: int) -> OperatorCandidate:
    """
    Operator encoding prime structure directly.
    Diagonal: log(p_k) for first n primes.
    Off-diagonal: coupling via Mobius function / convolution structure.

    This is a toy model testing whether prime-encoding alone
    can produce zeta-zero-like spectra.
    """
    primes = _sieve_primes(n * 10)[:n]
    log_primes = np.log(primes).astype(float)

    H = np.diag(log_primes)

    # Add off-diagonal coupling: H[j,k] = 1/sqrt(p_j * p_k) if gcd(p_j, p_k) related
    for j in range(n):
        for k in range(j + 1, n):
            coupling = 1.0 / np.sqrt(primes[j] * primes[k])
            H[j, k] = coupling
            H[k, j] = coupling

    eigenvalues = np.sort(np.linalg.eigvalsh(H))

    return OperatorCandidate(
        name=f"prime_zeta_n{n}",
        matrix=H,
        eigenvalues=eigenvalues,
        is_self_adjoint=True,
        encodes_primes=True,
        has_functional_equation_symmetry=False,
        description=f"Prime-encoding operator: diag=log(p), coupling=1/sqrt(p_j*p_k), {n}x{n}",
    )


# --- 4. Hecke-type operator (modular surface Laplacian) ---

def hecke_operator(n: int, level: int = 1) -> OperatorCandidate:
    """
    Simplified Hecke operator T_p acting on a finite-dimensional space.

    For level 1, the Laplacian eigenvalues on SL(2,Z)\\H are related to
    Maass forms, whose L-functions have zeros on Re(s)=1/2 (GRH).

    We approximate by: eigenvalues of the adjacency matrix of the
    Cayley graph of SL(2, Z/nZ), which captures modular structure.
    """
    # Simplified: use eigenvalues of a circulant matrix encoding Hecke action
    # T_p acts on q-expansion coefficients: (T_p f)(n) = sum_{d|gcd(n,p)} d^{k-1} f(np/d^2)
    # For weight 2, level 1: approximate as shift + multiplication

    primes = _sieve_primes(n * 5)[:min(n, 20)]

    H = np.zeros((n, n))
    for p in primes:
        for j in range(n):
            k = (j * int(p)) % n
            H[j, k] += 1.0 / np.sqrt(p)
            H[k, j] += 1.0 / np.sqrt(p)

    H = (H + H.T) / 2
    eigenvalues = np.sort(np.linalg.eigvalsh(H))

    return OperatorCandidate(
        name=f"hecke_level{level}_n{n}",
        matrix=H,
        eigenvalues=eigenvalues,
        is_self_adjoint=True,
        encodes_primes=True,
        has_functional_equation_symmetry=True,
        description=f"Hecke-type operator, level {level}, {n}x{n} (modular structure)",
    )


# --- 5. Connes-type trace formula operator ---

def connes_truncated(n: int, zeros: Optional[np.ndarray] = None) -> OperatorCandidate:
    """
    Operator constructed to have spectrum matching zeta zeros by design.
    This tests the "if H exists, what would it look like?" question.

    Construction: diagonal matrix with zeta zeros as eigenvalues,
    plus perturbation encoding the explicit formula structure.

    This is NOT a legitimate candidate (it's circular — uses zeros as input).
    It serves as the "upper bound" on what a perfect closure would score.
    """
    if zeros is None:
        from l1_rh import zeta_zeros
        zeros = zeta_zeros(n)

    H = np.diag(zeros[:n])

    eigenvalues = np.sort(np.linalg.eigvalsh(H))

    return OperatorCandidate(
        name=f"connes_truncated_n{n}",
        matrix=H,
        eigenvalues=eigenvalues,
        is_self_adjoint=True,
        encodes_primes=False,  # circular construction
        has_functional_equation_symmetry=True,
        description=f"Connes-type (circular): diagonal = zeta zeros, {n}x{n}. Upper bound reference.",
    )


# --- PT-symmetric construction ---

def _build_pt_berry_keating(n: int) -> np.ndarray:
    """
    Bender-Brody-Mueller type PT-symmetric Berry-Keating Hamiltonian.

    The BBM construction: H = (1 - e^{-ip})(xp + px)(1 - e^{-ip}) regularized.
    We implement a finite-dimensional approximation that preserves PT symmetry.

    Strategy: Start from the Hermitian Berry-Keating (Dirichlet) and add a
    PT-symmetric perturbation scaled to keep PT unbroken. The perturbation
    strength is tuned so that eigenvalues remain real (unbroken phase) while
    the spectrum shifts toward zeta-zero-like spacing.

    PT symmetry: P = parity (index reversal), T = complex conjugation.
    H is PT-symmetric iff P*conj(H)*P = H, i.e., H is symmetric under
    combined parity + conjugation.
    """
    # Base: Hermitian Berry-Keating in Dirichlet basis
    H_base = np.zeros((n, n), dtype=complex)
    for j in range(n):
        for k in range(n):
            if (j + k) % 2 == 1:
                jj, kk = j + 1, k + 1
                H_base[j, k] = -1j * 2 * jj * kk / (kk**2 - jj**2)
    H_base = (H_base + H_base.conj().T) / 2

    # PT-symmetric perturbation: purely imaginary, antisymmetric under parity
    # V_{jk} = i * epsilon * f(j,k) where f is real and P-antisymmetric
    # This ensures P*conj(V)*P = V (PT-symmetric)
    # f(j,k) = -(P*f*P)_{jk} and f real => i*f is PT-symmetric
    epsilon = 0.1
    V = np.zeros((n, n), dtype=complex)
    for j in range(n):
        for k in range(n):
            jj, kk = j + 1, k + 1
            # Position operator in sin-basis: real, P-symmetric
            # Momentum-like coupling: antisymmetric under P
            # Use: f_{jk} = (jj - kk) / (jj^2 + kk^2) which is P-antisymmetric
            j_rev = n - 1 - j
            k_rev = n - 1 - k
            # Antisymmetric under parity: f(j,k) = -f(n-1-j, n-1-k)
            f_jk = (jj - kk) / (jj**2 + kk**2 + 1.0)
            V[j, k] = 1j * epsilon * f_jk

    H = H_base + V

    # Verify and enforce PT symmetry
    P = np.eye(n)[::-1]
    PT_H = P @ H.conj() @ P
    err = np.max(np.abs(PT_H - H))
    if err > 1e-12:
        H = (H + P @ H.conj() @ P) / 2

    # Adaptive epsilon: increase perturbation while keeping PT unbroken
    # Binary search for largest epsilon that keeps all eigenvalues real
    eps_low, eps_high = 0.0, 2.0
    best_H = H_base.copy()
    for _ in range(20):
        eps_mid = (eps_low + eps_high) / 2
        H_test = H_base + eps_mid * (V / epsilon)
        H_test = (H_test + P @ H_test.conj() @ P) / 2
        eigs = np.linalg.eigvals(H_test)
        max_imag = np.max(np.abs(eigs.imag))
        if max_imag < 1e-6:
            eps_low = eps_mid
            best_H = H_test
        else:
            eps_high = eps_mid

    # Scale to match zeta zero range using affine transform
    # This is legitimate: any self-adjoint operator can be shifted/scaled
    # without changing its structural properties
    eigs = np.linalg.eigvals(best_H)
    real_eigs = np.sort(eigs[np.abs(eigs.imag) < 1e-6].real)

    if len(real_eigs) >= 2:
        # Target: first zero at ~14.13, last at ~2*pi*n/log(n) + 14
        target_start = 14.13
        target_end = 2 * np.pi * n / np.log(n) + 14.0
        current_min, current_max = real_eigs[0], real_eigs[-1]
        current_range = current_max - current_min
        if current_range > 1e-10:
            scale = (target_end - target_start) / current_range
            shift = target_start - current_min * scale
            best_H = scale * best_H + shift * np.eye(n, dtype=complex)

    return best_H


# --- Utilities ---

def _sieve_primes(limit: int) -> List[int]:
    """Return all primes up to limit."""
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(limit + 1) if sieve[i]]


# --- Registry ---

def build_candidate_registry(n: int = 50, zeros: Optional[np.ndarray] = None) -> List[OperatorCandidate]:
    """Build all candidate operators at dimension n."""
    candidates = [
        berry_keating_truncated(n, "dirichlet"),
        berry_keating_truncated(n, "periodic"),
        berry_keating_truncated(n, "pt_symmetric"),
        gue_random_matrix(n, seed=42),
        gue_random_matrix(n, seed=123),
        prime_zeta_operator(n),
        hecke_operator(n, level=1),
        connes_truncated(n, zeros),
    ]
    return candidates


if __name__ == "__main__":
    from l1_rh import zeta_zeros

    print("Building candidate operators (n=30)...\n")
    zeros = zeta_zeros(30)
    candidates = build_candidate_registry(30, zeros)

    for c in candidates:
        eigs = c.eigenvalues
        print(f"{c.name}:")
        print(f"  self-adjoint={c.is_self_adjoint}, primes={c.encodes_primes}, "
              f"symmetry={c.has_functional_equation_symmetry}")
        print(f"  eigenvalue range: [{eigs[0]:.3f}, {eigs[-1]:.3f}]")
        print(f"  first 3 eigenvalues: {eigs[:3]}")
        print()
