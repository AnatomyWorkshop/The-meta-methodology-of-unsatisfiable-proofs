"""
L1 domain model for Phase 6: Riemann Hypothesis.

Provides the ground truth — zeta zeros and their spectral statistics.
This is the "object model" that L2 searches against.
"""

import numpy as np
from typing import List, Tuple


def zeta_zeros(n: int) -> np.ndarray:
    """
    Return the imaginary parts of the first n non-trivial zeros of ζ(s).
    All known zeros lie on Re(s) = 1/2, so we return the γ values where ζ(1/2 + iγ) = 0.
    """
    from mpmath import zetazero
    zeros = np.array([float(zetazero(k).imag) for k in range(1, n + 1)])
    return zeros


def normalized_spacings(zeros: np.ndarray) -> np.ndarray:
    """
    Compute normalized nearest-neighbor spacings.
    Normalize by mean spacing so that <s> = 1.
    """
    spacings = np.diff(zeros)
    mean_spacing = np.mean(spacings)
    return spacings / mean_spacing


def pair_correlation(zeros: np.ndarray, tau_max: float = 3.0, n_bins: int = 50) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the pair correlation function R₂(τ) for a set of spectral values.
    Normalized so that R₂ → 1 for large τ (Poisson baseline).

    For GUE: R₂(τ) = 1 - (sin(πτ)/(πτ))²
    For Poisson: R₂(τ) = 1
    """
    n = len(zeros)
    mean_spacing = (zeros[-1] - zeros[0]) / (n - 1)

    diffs = []
    for i in range(n):
        for j in range(i + 1, min(i + 50, n)):
            diffs.append(abs(zeros[j] - zeros[i]) / mean_spacing)

    diffs = np.array(diffs)
    diffs = diffs[diffs < tau_max]

    bins = np.linspace(0, tau_max, n_bins + 1)
    hist, _ = np.histogram(diffs, bins=bins)

    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_width = bins[1] - bins[0]

    # Normalize: expected count per bin for Poisson = n_pairs * bin_width / tau_max
    n_pairs = n * min(50, n - 1) / 2
    expected = n_pairs * bin_width / tau_max
    r2 = hist / max(expected, 1)

    return bin_centers, r2


def gue_pair_correlation(tau: np.ndarray) -> np.ndarray:
    """Theoretical GUE pair correlation: R₂(τ) = 1 - (sin(πτ)/(πτ))²"""
    with np.errstate(divide='ignore', invalid='ignore'):
        sinc = np.where(tau == 0, 1.0, np.sin(np.pi * tau) / (np.pi * tau))
    return 1.0 - sinc**2


def wigner_surmise(s: np.ndarray) -> np.ndarray:
    """GUE Wigner surmise for nearest-neighbor spacing: P(s) = (32/π²)s² exp(-4s²/π)"""
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)


def poisson_spacing(s: np.ndarray) -> np.ndarray:
    """Poisson spacing distribution: P(s) = exp(-s)"""
    return np.exp(-s)


def spacing_distribution(zeros: np.ndarray, n_bins: int = 30) -> Tuple[np.ndarray, np.ndarray]:
    """Compute the nearest-neighbor spacing distribution."""
    spacings = normalized_spacings(zeros)
    s_max = 4.0
    spacings = spacings[spacings < s_max]

    bins = np.linspace(0, s_max, n_bins + 1)
    hist, _ = np.histogram(spacings, bins=bins, density=True)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    return bin_centers, hist


def explicit_formula_truncated(x: float, zeros: np.ndarray) -> float:
    """
    Riemann explicit formula (truncated):
    ψ(x) ≈ x - Σ_ρ x^ρ/ρ - log(2π) - (1/2)log(1 - x^{-2})

    Simplified: we compute the oscillatory part Σ_γ 2*Re(x^{1/2+iγ}/(1/2+iγ))
    """
    result = x  # main term
    for gamma in zeros:
        rho = 0.5 + 1j * gamma
        term = x**rho / rho
        result -= 2 * term.real
    return result.real if isinstance(result, complex) else result


def prime_counting_exact(n: int) -> int:
    """Exact prime counting function π(n) via sieve."""
    if n < 2:
        return 0
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    return sum(sieve)


# --- Spectral statistics comparison ---

def ks_statistic(empirical: np.ndarray, theoretical_cdf) -> float:
    """Kolmogorov-Smirnov statistic between empirical data and theoretical CDF."""
    sorted_data = np.sort(empirical)
    n = len(sorted_data)
    ecdf = np.arange(1, n + 1) / n
    tcdf = np.array([theoretical_cdf(x) for x in sorted_data])
    return np.max(np.abs(ecdf - tcdf))


def gue_spacing_cdf(s: float) -> float:
    """Approximate CDF of GUE Wigner surmise."""
    from scipy.special import erf
    return 1.0 - np.exp(-4.0 * s**2 / np.pi) + erf(2.0 * s / np.sqrt(np.pi)) * 0  # simplified
    # Use numerical integration for accuracy
    from scipy.integrate import quad
    result, _ = quad(lambda x: wigner_surmise(np.array([x]))[0], 0, s)
    return min(result, 1.0)


def poisson_spacing_cdf(s: float) -> float:
    """CDF of Poisson spacing: 1 - exp(-s)"""
    return 1.0 - np.exp(-s)


if __name__ == "__main__":
    print("Computing first 50 zeta zeros...")
    zeros = zeta_zeros(50)
    print(f"First 5 zeros: {zeros[:5]}")
    print(f"Mean spacing: {np.mean(np.diff(zeros)):.4f}")

    print("\nSpacing statistics:")
    spacings = normalized_spacings(zeros)
    print(f"  Mean normalized spacing: {np.mean(spacings):.4f} (should be ~1)")
    print(f"  Std: {np.std(spacings):.4f}")

    print("\nPair correlation (first 5 bins):")
    tau, r2 = pair_correlation(zeros)
    gue_r2 = gue_pair_correlation(tau)
    for i in range(5):
        print(f"  tau={tau[i]:.2f}: R2={r2[i]:.3f} (GUE: {gue_r2[i]:.3f})")

    print("\nExplicit formula test (x=100):")
    psi_approx = explicit_formula_truncated(100.0, zeros[:20])
    pi_exact = prime_counting_exact(100)
    print(f"  psi(100) ~ {psi_approx:.2f}")
    print(f"  pi(100) = {pi_exact}")
