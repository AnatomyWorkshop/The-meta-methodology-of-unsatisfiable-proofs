"""
Local heat kernel trace Tr_p(e^{-t D_p^2}) for prime p.

The conjectured trace formula says:
  Tr(e^{-t D^2}) ~ sum_p sum_{k>=1} log(p) * p^{-k/2} * delta(t - log(p^k)) + O(1)

The local contribution at prime p should be:
  Tr_p(e^{-t D_p^2}) ~ sum_{k>=1} log(p) * p^{-k/2} * delta(t - log(p^k))

This module computes the local trace and checks whether its Laplace/Mellin
transform matches the expected prime power sum.

Key insight: the delta functions in the trace formula are not literal Dirac deltas
in t — they arise from the Mellin transform. The actual local trace is a smooth
function of t whose Mellin transform has poles at s = 1/2 + i*gamma_n.

We compute:
  1. The exact local trace Tr_p(e^{-t D_p^2}) as a function of t
  2. Its Mellin transform M_p(s) = integral_0^inf t^{s/2-1} Tr_p(e^{-t D_p^2}) dt
  3. Compare M_p(s) to the expected -log(p) * p^{-s/2} / (1 - p^{-s/2}) (geometric series)
"""

import numpy as np
from typing import List, Tuple
from vladimirov import eigenvalues_vladimirov


def local_trace(p: int, t: float, N: int = 20, alpha: float = 2.0) -> float:
    """
    Tr_p(e^{-t D_p^alpha}) = sum_k mult_k * e^{-t * lambda_k}

    where lambda_k = p^{alpha*k} and mult_k = p^k - p^{k-1} for k >= 1.

    This is the full trace (not divided by volume), summed over all eigenvalues.
    """
    evals, mults = eigenvalues_vladimirov(p, N, alpha)
    return float(np.sum(mults * np.exp(-t * evals)))


def local_trace_exact(p: int, t: float, alpha: float = 2.0) -> float:
    """
    Exact local trace in the limit N -> infinity.

    Tr_p(e^{-t D_p^alpha}) = 1 + sum_{k=1}^{inf} (p^k - p^{k-1}) * e^{-t * p^{alpha*k}}

    The k=0 term contributes 1 (the constant function eigenspace).
    For k >= 1: mult_k = p^k(1 - 1/p), lambda_k = p^{alpha*k}.

    Truncate when e^{-t * p^{alpha*k}} < 1e-15.
    """
    result = 1.0  # k=0 term
    for k in range(1, 200):
        lam = float(p) ** (alpha * k)
        contrib = (p**k - p**(k-1)) * np.exp(-t * lam)
        result += contrib
        if abs(contrib) < 1e-15:
            break
    return result


def local_trace_array(p: int, t_arr: np.ndarray, alpha: float = 2.0) -> np.ndarray:
    """Vectorized local trace over array of t values."""
    return np.array([local_trace_exact(p, t, alpha) for t in t_arr])


def mellin_transform_numerical(p: int, s: complex, t_max: float = 50.0,
                                n_points: int = 10000, alpha: float = 2.0) -> complex:
    """
    Numerical Mellin transform of the local trace:
      M_p(s) = integral_0^{t_max} t^{s/2 - 1} * Tr_p(e^{-t D_p^alpha}) dt

    Uses log-uniform quadrature (better for power-law integrands).
    """
    t_min = 1e-6
    log_t = np.linspace(np.log(t_min), np.log(t_max), n_points)
    t_arr = np.exp(log_t)
    dt_log = log_t[1] - log_t[0]

    trace_vals = local_trace_array(p, t_arr, alpha)
    # integrand = t^{s/2 - 1} * Tr * t  (the extra t from d(log t) = dt/t)
    integrand = t_arr ** (s / 2) * trace_vals
    return complex(np.trapz(integrand, log_t))


def expected_mellin_local(p: int, s: complex, alpha: float = 2.0) -> complex:
    """
    Expected Mellin transform of the local trace from the trace formula conjecture.

    From the conjectured trace formula:
      Tr_p(e^{-t D_p^2}) ~ sum_{k>=1} log(p) * p^{-k/2} * delta(t - log(p^k))

    Taking Mellin transform (integral t^{s/2-1} dt):
      M_p(s) = sum_{k>=1} log(p) * p^{-k/2} * (log p^k)^{s/2 - 1}
             = log(p) * sum_{k>=1} p^{-k/2} * (k log p)^{s/2 - 1}

    But the more natural form comes from the Euler factor of xi(s):
      -d/ds log(1 - p^{-s/2}) = (log p / 2) * p^{-s/2} / (1 - p^{-s/2})
                               = (log p / 2) * sum_{k>=1} p^{-ks/2}

    This is the logarithmic derivative of the local Euler factor.
    The local trace Mellin transform should equal this.
    """
    # Geometric series: sum_{k>=1} p^{-ks/2} = p^{-s/2} / (1 - p^{-s/2})
    x = float(p) ** (-s / 2)
    if abs(1 - x) < 1e-12:
        return complex(np.inf)
    return complex(np.log(p) / 2 * x / (1 - x))


def check_local_trace_asymptotics(p: int, t_values: np.ndarray,
                                   alpha: float = 2.0) -> dict:
    """
    Check whether the local trace matches the expected prime power contributions.

    The trace formula predicts that near t = log(p^k) = k * log(p),
    the local trace has a peak whose integral equals log(p) * p^{-k/2}.

    We check this by integrating the trace in windows around each t = k*log(p).
    """
    results = {}
    log_p = np.log(p)

    for k in range(1, 6):
        t_center = k * log_p
        expected_weight = np.log(p) * float(p) ** (-k / 2)

        # Find t values near t_center
        window = log_p * 0.4
        mask = np.abs(t_values - t_center) < window
        if not np.any(mask):
            continue

        t_window = t_values[mask]
        trace_window = local_trace_array(p, t_window, alpha)

        # The "weight" is the integral of the trace in this window
        # (rough proxy for the delta function coefficient)
        if len(t_window) > 1:
            integral = np.trapz(trace_window, t_window)
        else:
            integral = 0.0

        results[k] = {
            't_center': t_center,
            'expected_weight': expected_weight,
            'integral_in_window': integral,
            'ratio': integral / expected_weight if expected_weight > 0 else np.nan,
        }

    return results


def local_trace_mellin_residues(p: int, alpha: float = 2.0) -> List[Tuple[float, float]]:
    """
    Exact Mellin transform of the local trace via term-by-term integration.

    Tr_p(e^{-t D_p^alpha}) = sum_{k=0}^{inf} mult_k * e^{-t * p^{alpha*k}}

    Mellin transform of e^{-lambda*t} is Gamma(s/2) * lambda^{-s/2}.

    So M_p(s) = sum_{k=0}^{inf} mult_k * Gamma(s/2) * (p^{alpha*k})^{-s/2}
              = Gamma(s/2) * [1 + sum_{k=1}^{inf} (p^k - p^{k-1}) * p^{-alpha*k*s/2}]
              = Gamma(s/2) * [1 + (1 - 1/p) * sum_{k=1}^{inf} p^{k(1 - alpha*s/2)}]

    For alpha=2: exponent = k(1 - s), geometric series converges for Re(s) > 1:
      sum_{k=1}^{inf} p^{k(1-s)} = p^{1-s} / (1 - p^{1-s})

    So M_p(s) = Gamma(s/2) * [1 + (1-1/p) * p^{1-s} / (1 - p^{1-s})]

    The poles of the geometric series are at p^{1-s} = 1, i.e., s = 1 + 2*pi*i*n/log(p).
    These are NOT the zeta zeros. The zeta zeros come from the GLOBAL trace.

    Returns list of (s_real, s_imag) for poles in the strip 0 < Re(s) < 2.
    """
    log_p = np.log(p)
    poles = []
    # Poles at s = 1 + 2*pi*i*n / log(p) for n in Z
    for n in range(-20, 21):
        s_real = 1.0
        s_imag = 2 * np.pi * n / log_p
        poles.append((s_real, s_imag))
    return poles


def exact_mellin_local(p: int, s: complex, alpha: float = 2.0,
                        n_terms: int = 100) -> complex:
    """
    Exact Mellin transform M_p(s) = Gamma(s/2) * F_p(s) where:

    For alpha=2:
      F_p(s) = 1 + (1 - 1/p) * p^{1-s} / (1 - p^{1-s})
             = (1 - p^{1-s} + (1-1/p)*p^{1-s}) / (1 - p^{1-s})
             = (1 - p^{-s}) / (1 - p^{1-s})

    This is the local Euler factor of the completed zeta function!
    xi(s) = prod_p (1 - p^{-s})^{-1} / (1 - p^{1-s})^{-1} * [archimedean factor]

    The local Mellin transform is:
      M_p(s) = Gamma(s/2) * (1 - p^{-s}) / (1 - p^{1-s})
    """
    from scipy.special import gamma as gamma_func
    g = gamma_func(s / 2)
    x = float(p) ** (-s)
    y = float(p) ** (1 - s)
    if abs(1 - y) < 1e-12:
        return complex(np.inf)
    F = (1 - x) / (1 - y)
    return complex(g * F)
