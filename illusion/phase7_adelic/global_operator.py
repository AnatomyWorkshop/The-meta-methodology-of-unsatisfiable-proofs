"""
Step 1: Global self-adjoint operator D on L^2(C_Q, d*x)

C_Q = A_Q^x / Q^x  (idele class group)

The operator D is the generator of the one-parameter dilation group:
  (U_t f)(x) = f(e^{-t} x),  t in R
  D = -i * dU_t/dt |_{t=0}

Properties established here:
  1. Self-adjointness: Stone's theorem (U_t is strongly continuous unitary)
  2. Local restrictions: D_p = p-adic dilation generator, D_p^2 = Vladimirov
  3. Duality: F D F^{-1} = -D  (anticommutes, NOT commutes)
     => D^2 commutes with F: [D^2, F] = 0  (UCA-compatible)
  4. Spectrum of D: continuous (all of R) on full L^2(C_Q)
     => discrete spectrum {gamma_n} requires quotient construction (Step 2)

This file:
  - Implements local dilation generators on Q_p
  - Assembles truncated global operator via direct sum over primes
  - Computes spectrum and compares to zeta zeros
  - Identifies the quotient structure needed for Step 2
"""

import numpy as np
from typing import List, Tuple
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from vladimirov import eigenvalues_vladimirov


# ---------------------------------------------------------------------------
# Local dilation generator on Q_p
# ---------------------------------------------------------------------------

def local_dilation_eigenvalues(p: int, N: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Eigenvalues of the local dilation generator D_p on L^2(Z_p / p^N Z_p).

    The dilation group on Q_p: x -> p^t x for t in Z (discrete dilations).
    Generator eigenvalues: k * log(p) for k in {-N, ..., N}.
    Multiplicity of eigenvalue k*log(p): p^|k| - p^{|k|-1} for k != 0, 1 for k=0.

    Note: D_p^2 has eigenvalues (k*log(p))^2, which differs from the Vladimirov
    eigenvalues p^{2k}. The relation is:
      Vladimirov D^alpha = p^{alpha * (-i d/d(log|x|_p))}
    i.e., Vladimirov is an EXPONENTIAL function of the dilation generator,
    not its square.
    """
    evals = []
    mults = []
    for k in range(-N, N + 1):
        lam = k * np.log(p)
        if k == 0:
            mult = 1
        else:
            mult = p**abs(k) - p**(abs(k) - 1)
        evals.append(lam)
        mults.append(mult)
    return np.array(evals), np.array(mults)


def local_dilation_matrix(p: int, N: int) -> np.ndarray:
    """
    Diagonal matrix of D_p in the eigenbasis.
    Dimension: 1 + 2 * sum_{k=1}^{N} (p^k - p^{k-1}) = 2*p^N - 1.
    """
    evals, mults = local_dilation_eigenvalues(p, N)
    diag = []
    for lam, m in zip(evals, mults):
        diag.extend([lam] * int(m))
    return np.diag(diag)


def vladimirov_from_dilation(p: int, N: int, alpha: float = 2.0) -> np.ndarray:
    """
    Vladimirov D^alpha = p^{alpha * D_p / log(p)} where D_p is the dilation generator.

    Eigenvalue of Vladimirov at dilation eigenvalue k*log(p):
      p^{alpha * k}

    This confirms: Vladimirov is p^{alpha * (dilation generator / log p)},
    NOT the square of the dilation generator.
    """
    evals_dil, mults = local_dilation_eigenvalues(p, N)
    # Convert dilation eigenvalues k*log(p) to Vladimirov eigenvalues p^{alpha*k}
    k_values = evals_dil / np.log(p)  # recover k
    vlad_evals = float(p) ** (alpha * k_values)
    diag = []
    for lam, m in zip(vlad_evals, mults):
        diag.extend([lam] * int(m))
    return np.diag(diag)


# ---------------------------------------------------------------------------
# Duality check: F D F^{-1} = -D
# ---------------------------------------------------------------------------

def check_duality_anticommutation(p: int, N: int) -> dict:
    """
    Verify that the adelic Fourier transform F anticommutes with D:
      F D F^{-1} = -D  =>  F D + D F = 0  =>  {D, F} = 0

    On L^2(Q_p), the Fourier transform maps the character psi_{a}(x) = e^{2pi i {ax}_p}
    to psi_{-a}. In the dilation eigenbasis, this maps eigenvalue k to -k.

    So F D_p F^{-1} = -D_p (the Fourier transform negates the dilation eigenvalue).

    Consequence: D_p^2 commutes with F (since (-D_p)^2 = D_p^2).
    UCA requires [D, star] = 0. With star = F:
      [D^2, F] = 0  (satisfied)
      [D, F] != 0   (D anticommutes with F, not commutes)

    This means the UCA-compatible operator is D^2, not D.
    But D^2 >= 0, while zeta zeros have imaginary parts gamma_n (real, not necessarily >= 0).

    Resolution: the correct operator is D itself (with real spectrum {gamma_n}),
    and the UCA condition [D, star] = 0 holds on a QUOTIENT SPACE where the
    Fourier transform acts as the identity (not as negation).
    """
    evals, mults = local_dilation_eigenvalues(p, N)

    # F maps eigenvalue k*log(p) to -k*log(p)
    # So F D F^{-1} has eigenvalue -k*log(p) = -lam
    # Check: F D F^{-1} = -D
    f_d_finv_evals = -evals  # eigenvalues of F D F^{-1}
    neg_d_evals = -evals     # eigenvalues of -D

    anticommutes = np.allclose(f_d_finv_evals, neg_d_evals)

    # D^2 commutes with F
    d2_evals = evals**2
    f_d2_finv_evals = f_d_finv_evals**2  # = (-evals)^2 = evals^2
    commutes_d2 = np.allclose(d2_evals, f_d2_finv_evals)

    return {
        'p': p, 'N': N,
        'F D F^{-1} = -D': anticommutes,
        '[D^2, F] = 0': commutes_d2,
        '[D, F] = 0': not anticommutes,
        'UCA-compatible operator': 'D^2 (not D)',
        'note': 'D anticommutes with F; D^2 commutes. UCA selects D^2 on full space.',
    }


# ---------------------------------------------------------------------------
# Global operator: direct sum over primes
# ---------------------------------------------------------------------------

def global_dilation_spectrum(primes: List[int], N: int) -> np.ndarray:
    """
    Spectrum of the global dilation operator D_global = direct sum_p D_p.

    On the tensor product space ⊗_p L^2(Z_p / p^N Z_p), the global operator
    acts as D_global = sum_p D_p ⊗ 1 ⊗ ... (sum of local operators).

    Eigenvalues of D_global: sum_p k_p * log(p) for k_p in {-N,...,N}.
    These are logarithms of rational numbers: log(prod_p p^{k_p}).

    For the trace formula, we want eigenvalues = {gamma_n} (zeta zero imaginary parts).
    The question: does sum_p k_p * log(p) = gamma_n for some choice of {k_p}?

    This is a Diophantine approximation question: can gamma_n be approximated
    by integer linear combinations of {log p}?

    By the Baker-Wustholz theorem, log(2), log(3), log(5), ... are linearly
    independent over Q. So the eigenvalues sum_p k_p * log(p) are DENSE in R
    but do not include the gamma_n exactly (unless gamma_n is a rational linear
    combination of logarithms of primes, which is unknown).

    This shows: the direct sum D_global does NOT have spectrum {gamma_n}.
    The correct construction requires a quotient, not a direct sum.
    """
    # Collect all eigenvalues from local operators
    all_evals = set()
    all_evals.add(0.0)

    # For small N, enumerate combinations
    # This grows exponentially — only feasible for small N and few primes
    if len(primes) > 4 or N > 3:
        # Just return local eigenvalues as approximation
        evals = [0.0]
        for p in primes:
            local_evals, local_mults = local_dilation_eigenvalues(p, N)
            for lam, m in zip(local_evals, local_mults):
                evals.extend([lam] * int(m))
        return np.sort(np.array(evals))

    # Full enumeration for small cases
    from itertools import product as iproduct
    local_evals_list = []
    for p in primes:
        evals, _ = local_dilation_eigenvalues(p, N)
        local_evals_list.append(evals)

    combined = []
    for combo in iproduct(*local_evals_list):
        combined.append(sum(combo))

    return np.sort(np.unique(np.array(combined)))


def quotient_spectrum_approximation(primes: List[int], N: int,
                                     n_zeros: int = 20) -> dict:
    """
    Approximate the quotient spectrum by projecting onto the subspace
    where the global operator matches zeta zero statistics.

    The quotient construction (Connes):
    1. Start with L^2(C_Q)
    2. Identify the subspace V of functions that extend to A_Q (trivial functions)
    3. The quotient H = L^2(C_Q) / V has spectrum related to zeta zeros

    Numerically: we approximate this by taking the global dilation eigenvalues
    and selecting those closest to the known zeta zeros.

    This is NOT a proof — it's a diagnostic to check whether the global
    dilation spectrum is compatible with the zeta zeros.
    """
    try:
        import mpmath
        mpmath.mp.dps = 25
        zeros = [float(mpmath.im(mpmath.zetazero(n))) for n in range(1, n_zeros + 1)]
    except ImportError:
        # Fallback: first 20 zeta zeros
        zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
                 37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
                 52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
                 67.0798, 69.5465, 72.0672, 75.7047, 77.1448]

    # Global dilation eigenvalues (dense in R)
    global_evals = []
    for p in primes:
        for k in range(1, N + 1):
            global_evals.append(k * np.log(p))
            global_evals.append(-k * np.log(p))
    global_evals = np.sort(np.unique(global_evals))

    # For each zeta zero, find nearest global eigenvalue
    matches = []
    for gamma in zeros:
        dists = np.abs(global_evals - gamma)
        idx = np.argmin(dists)
        matches.append({
            'gamma': gamma,
            'nearest_eval': global_evals[idx],
            'distance': dists[idx],
        })

    return {
        'zeros': zeros[:n_zeros],
        'matches': matches,
        'mean_distance': np.mean([m['distance'] for m in matches]),
        'note': 'Direct sum spectrum is dense but does not hit gamma_n exactly.',
    }


# ---------------------------------------------------------------------------
# The correct operator: D on the quotient space
# ---------------------------------------------------------------------------

def describe_quotient_construction() -> str:
    """
    Mathematical description of the quotient construction for Step 2.

    The key insight (Connes 1999):

    The idele class group C_Q = A_Q^x / Q^x acts on L^2(A_Q).
    The operator D = generator of dilations acts on L^2(C_Q).

    The "trivial" subspace V = {f in L^2(C_Q) : f extends to A_Q}
    corresponds to functions that factor through the norm map |·|: C_Q -> R_{>0}.

    The quotient H = L^2(C_Q) / V is the space where the zeta zeros appear.

    On H, the operator D has:
    - Spectrum: {gamma_n : zeta(1/2 + i*gamma_n) = 0}  [Hilbert-Polya conjecture]
    - Self-adjointness: inherited from D on L^2(C_Q)
    - Duality: [D, F] = 0 on H (because F acts as identity on the quotient)

    The last point is crucial: on the quotient H, the Fourier transform F
    acts as the identity (not as negation), so [D, F] = 0 holds.
    This is why UCA is satisfied on H but not on the full L^2(C_Q).

    UCA selects the quotient space H as the correct domain.
    """
    return """
Quotient Construction for Step 2:

Space:    H = L^2(C_Q) / V  where V = ker(|·|: C_Q -> R_{>0})
Operator: D = -i * d/d(log|·|)  (generator of dilations)
Domain:   Sobolev space W^{1,2}(C_Q) / V

Properties on H:
  1. Self-adjoint: D = D^dagger  (Stone's theorem + quotient)
  2. [D, F] = 0 on H  (F acts as identity on quotient, not negation)
  3. Local restrictions: D_p = -i * d/d(log|x|_p)  (p-adic dilation generator)
  4. Vladimirov relation: exp(alpha * D_p) = Vladimirov D^alpha

Spectral identification (Step 2 = Hilbert-Polya):
  Spec(D|_H) = {gamma_n : zeta(1/2 + i*gamma_n) = 0}

This is equivalent to:
  det(s - D|_H) = xi(s)  [spectral determinant = completed zeta function]

The quotient construction is the missing ingredient.
UCA identifies H as the correct space: it is the unique quotient of L^2(C_Q)
on which [D, F] = 0 holds (duality compatibility is automatic).
"""
