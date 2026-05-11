"""
Global trace via Euler product assembly.

The global adelic trace is:
  Tr(e^{-t D^2}) = prod_p Tr_p(e^{-t D_p^2})  [schematically]

More precisely, the LOGARITHM of the global spectral determinant is:
  log det(s - D) = sum_p log det_p(s - D_p)

And the Mellin transform of the global trace gives:
  -d/ds log xi(s) = sum_p -d/ds log(local Euler factor at p)
                  = sum_p (log p / 2) * p^{-s/2} / (1 - p^{-s/2})
                  = sum_p sum_{k>=1} (log p / 2) * p^{-ks/2}

This is the explicit formula for xi(s).

The global trace formula conjecture says:
  Tr(e^{-t D^2}) ~ sum_p sum_{k>=1} log(p) * p^{-k/2} * delta(t - log(p^k)) + O(1)

This module:
1. Assembles the global Mellin transform from local factors
2. Compares to the known -xi'/xi(s)
3. Verifies the Euler product structure numerically
"""

import numpy as np
from typing import List, Tuple
from local_trace import local_trace_exact, exact_mellin_local


def primes_up_to(n: int) -> List[int]:
    """Sieve of Eratosthenes."""
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]


def global_trace_truncated(t: float, primes: List[int], alpha: float = 2.0) -> float:
    """
    Truncated global trace: product of local traces over given primes.

    Note: the true global trace is a sum (not product) of local contributions
    in the additive (log) sense. The product structure is for the spectral determinant.

    For the trace formula, the global trace is:
      Tr_global(t) = sum_p Tr_p^{(connected)}(t)

    where Tr_p^{(connected)} is the "connected" part of the local trace
    (subtracting the k=0 constant term).
    """
    # The global trace formula is additive in the connected local traces
    # Tr_p^{conn}(t) = Tr_p(t) - 1  (subtract the constant eigenspace)
    result = 1.0  # global constant term
    for p in primes:
        local = local_trace_exact(p, t, alpha)
        result += (local - 1.0)  # connected contribution
    return result


def global_mellin_truncated(s: complex, primes: List[int],
                             alpha: float = 2.0) -> complex:
    """
    Global Mellin transform assembled from local Euler factors.

    M_global(s) = sum_p M_p^{conn}(s)
                = sum_p [M_p(s) - Gamma(s/2)]  [connected part]

    The full global Mellin transform is:
      M_global(s) = Gamma(s/2) * prod_p F_p(s)

    where F_p(s) = (1 - p^{-s}) / (1 - p^{1-s}) is the local Euler factor.
    """
    from scipy.special import gamma as gamma_func
    g = gamma_func(s / 2)

    # Product of local Euler factors
    euler_product = complex(1.0)
    for p in primes:
        x = float(p) ** (-s)
        y = float(p) ** (1 - s)
        if abs(1 - y) < 1e-12:
            continue
        F_p = (1 - x) / (1 - y)
        euler_product *= F_p

    return g * euler_product


def log_derivative_xi(s: complex, primes: List[int]) -> complex:
    """
    Numerical approximation to -xi'(s)/xi(s) via truncated Euler product.

    -xi'/xi(s) = sum_p sum_{k>=1} log(p) * p^{-ks/2}
               = sum_p log(p) * p^{-s/2} / (1 - p^{-s/2})

    This is the Dirichlet series for the von Mangoldt function Lambda(n).
    """
    result = complex(0.0)
    for p in primes:
        x = float(p) ** (-s / 2)
        if abs(1 - x) < 1e-12:
            continue
        result += np.log(p) * x / (1 - x)
    return result


def prime_power_sum(s: complex, primes: List[int], k_max: int = 30) -> complex:
    """
    Direct sum: sum_p sum_{k=1}^{k_max} log(p) * p^{-ks/2}

    This is the explicit form of -xi'/xi(s) as a Dirichlet series.
    Should match log_derivative_xi(s, primes) for large k_max.
    """
    result = complex(0.0)
    for p in primes:
        for k in range(1, k_max + 1):
            contrib = np.log(p) * float(p) ** (-k * s / 2)
            result += contrib
            if abs(contrib) < 1e-15:
                break
    return result


def verify_euler_product(primes: List[int], s_values: List[complex]) -> dict:
    """
    Verify that the truncated Euler product matches the known zeta function.

    For Re(s) > 1:
      prod_p (1 - p^{-s})^{-1} = zeta(s)

    We check: |prod_p (1-p^{-s})^{-1} - zeta(s)| / |zeta(s)|
    """
    try:
        import mpmath
        mpmath.mp.dps = 25
    except ImportError:
        return {'error': 'mpmath not available'}

    results = {}
    for s in s_values:
        # Truncated Euler product
        product = complex(1.0)
        for p in primes:
            product *= 1.0 / (1.0 - float(p) ** (-s))

        # True zeta value
        zeta_true = complex(mpmath.zeta(s))

        rel_error = abs(product - zeta_true) / abs(zeta_true)
        results[s] = {
            'truncated': product,
            'true': zeta_true,
            'rel_error': rel_error,
        }
    return results


def trace_formula_check(primes: List[int], t_range: np.ndarray,
                         alpha: float = 2.0) -> dict:
    """
    Check the trace formula: does the global trace have peaks at t = k*log(p)?

    For each prime p and power k, the trace formula predicts a contribution
    of weight log(p) * p^{-k/2} near t = k * log(p).

    We compute the global trace and check for these peaks.
    """
    trace_vals = np.array([global_trace_truncated(t, primes, alpha) for t in t_range])

    # Expected peak locations and weights
    peaks = []
    for p in primes:
        for k in range(1, 6):
            t_peak = k * np.log(p)
            if t_peak > t_range[-1]:
                break
            weight = np.log(p) * float(p) ** (-k / 2)
            peaks.append({'p': p, 'k': k, 't': t_peak, 'weight': weight})

    # Sort by t
    peaks.sort(key=lambda x: x['t'])

    return {
        't_range': t_range,
        'trace': trace_vals,
        'predicted_peaks': peaks,
    }
