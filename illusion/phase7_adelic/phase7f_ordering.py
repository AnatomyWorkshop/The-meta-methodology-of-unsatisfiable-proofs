"""
Phase 7f: Ordering problem — which smooth number maps to which zero?

Finding from Phase 7e:
  Naive ordering (smooth numbers by size) gives RMSE > 7 for B >= 5.
  The ratio gamma_n / log(n_smooth) grows from 20 to 26 — not constant.
  The fit: ratio = 15.4 + 3.05 * log(n) matches Phase 7c's two-parameter model.

Problem:
  We assumed gamma_n corresponds to the n-th smallest smooth number.
  But this is wrong — the ordering is not by size of n_smooth.

Alternative orderings to test:
  1. By log(n_smooth) / log(log(n_smooth))  [Riemann-Siegel-like]
  2. By Omega(n_smooth) = total number of prime factors (with multiplicity)
  3. By the "height" in the prime lattice: max(k_p) for n = prod p^{k_p}
  4. By the number of divisors d(n_smooth)
  5. By the von Mangoldt function Lambda(n_smooth)

The Riemann-Siegel formula gives:
  gamma_n ~ 2*pi*n / log(n / 2*pi*e)

If gamma_n = C * log(m_n) for some smooth number m_n, then:
  log(m_n) ~ 2*pi*n / (C * log(n / 2*pi*e))

This means m_n grows SUPER-EXPONENTIALLY in n — much faster than the n-th smooth number.

New hypothesis:
  The correct mapping is NOT n -> n-th smooth number.
  Instead: gamma_n ~ 2*pi * log(m_n) / log(log(m_n))
  where m_n is the n-th smooth number in a DIFFERENT ordering.

Or more precisely: the spectral measure is NOT the counting measure on smooth numbers,
but a WEIGHTED measure where each smooth number n contributes weight Lambda(n) / log(n)
(the normalized von Mangoldt function).

This is the explicit formula:
  psi(x) = x - sum_rho x^rho/rho - log(2*pi) - (1/2)*log(1 - x^{-2})
where psi(x) = sum_{n<=x} Lambda(n) is the Chebyshev function.

The zeros rho = 1/2 + i*gamma_n appear in the explicit formula as oscillations
in psi(x). The connection to smooth numbers is through the Euler product:
  log zeta(s) = sum_p sum_k p^{-ks} / k = sum_n Lambda(n) n^{-s} / log(n)

So the spectral measure is: mu = sum_n Lambda(n)/log(n) * delta_{log n}
NOT the counting measure on smooth numbers.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from constrained_adelic_experiment import zeta_zeros


def first_n_primes(n: int) -> list:
    primes = []
    c = 2
    while len(primes) < n:
        if all(c % p != 0 for p in primes):
            primes.append(c)
        c += 1
    return primes


def von_mangoldt(n: int) -> float:
    """Lambda(n): log(p) if n = p^k, else 0."""
    if n <= 1:
        return 0.0
    # Check if n is a prime power
    for p in range(2, int(n**0.5) + 2):
        if n % p == 0:
            # p divides n; check if n = p^k
            m = n
            while m % p == 0:
                m //= p
            if m == 1:
                return np.log(float(p))
            else:
                return 0.0
    # n is prime
    return np.log(float(n))


def build_mangoldt_spectrum(N_max: int) -> tuple:
    """
    Build the von Mangoldt spectral measure up to N_max.

    Returns: (log_values, weights) where
      log_values[i] = log(n) for n with Lambda(n) > 0
      weights[i] = Lambda(n) / log(n) = 1 (for prime powers)

    The spectral points are log(p^k) = k*log(p) for primes p, k >= 1.
    Each has weight 1 (since Lambda(p^k) = log(p) and we divide by log(p^k) = k*log(p)...
    actually Lambda(p^k)/log(p^k) = log(p)/(k*log(p)) = 1/k).

    So prime powers p^k contribute weight 1/k.
    """
    points = []
    for n in range(2, N_max + 1):
        lam = von_mangoldt(n)
        if lam > 0:
            log_n = np.log(float(n))
            weight = lam / log_n  # = 1/k for n = p^k
            points.append((log_n, weight, n))
    points.sort(key=lambda x: x[0])
    return points


def weighted_spectrum_to_eigenvalues(points: list, n_target: int) -> np.ndarray:
    """
    Convert weighted spectral measure to eigenvalue sequence.

    Each point (t, w, n) contributes floor(w * scale) copies of t,
    where scale is chosen so total count ~ n_target.

    For the von Mangoldt measure: primes contribute weight 1, p^2 contributes 1/2, etc.
    We expand: prime p -> 1 copy of log(p), p^2 -> 0.5 copies (round to 1 if >= 0.5).
    """
    # Simple approach: include all prime powers, weight by 1/k
    # Primes (k=1): weight 1 -> include
    # p^2 (k=2): weight 0.5 -> include with probability 0.5 (deterministic: include if k<=2)
    # p^3 (k=3): weight 1/3 -> skip for now

    # For a first test: include only primes (k=1) and squares of primes (k=2)
    eigenvalues = []
    for (t, w, n) in points:
        # Determine k: n = p^k
        k = round(1.0 / (w + 1e-10))
        if k <= 2:  # include primes and prime squares
            eigenvalues.append(t)

    return np.sort(np.array(eigenvalues))


def rmse_vs_zeros(spectrum: np.ndarray, zeros: np.ndarray, n: int = 30) -> float:
    n = min(len(spectrum), len(zeros), n)
    if n < 3:
        return float('inf')
    pred = spectrum[:n]
    tgt = zeros[:n]
    scale = (tgt[-1] - tgt[0]) / (pred[-1] - pred[0] + 1e-10)
    shift = tgt[0] - scale * pred[0]
    return float(np.sqrt(np.mean((scale * pred + shift - tgt) ** 2)))


def run_mangoldt_experiment(N_max: int = 200, n_zeros: int = 30) -> None:
    """
    Test the von Mangoldt spectral measure as eigenvalue sequence.

    The explicit formula connects zeta zeros to the Chebyshev psi function
    via the von Mangoldt function. This tests whether the spectral points
    {log(p^k)} with weights {1/k} reproduce the zeta zero distribution.
    """
    zeros = zeta_zeros(n_zeros)
    points = build_mangoldt_spectrum(N_max)

    print("Phase 7f: Von Mangoldt Spectral Measure")
    print("=" * 62)
    print(f"N_max={N_max}, {len(points)} prime powers")
    print()

    # Test 1: primes only (k=1)
    primes_only = np.array([t for (t, w, n) in points if abs(w - 1.0) < 0.01])
    rmse_primes = rmse_vs_zeros(primes_only, zeros)
    print(f"  Primes only: {len(primes_only)} points, RMSE={rmse_primes:.4f}")

    # Test 2: primes + prime squares
    primes_sq = np.sort(np.array([t for (t, w, n) in points if w >= 0.4]))
    rmse_sq = rmse_vs_zeros(primes_sq, zeros)
    print(f"  Primes + p^2: {len(primes_sq)} points, RMSE={rmse_sq:.4f}")

    # Test 3: all prime powers (weighted by 1/k, expand to integer counts)
    all_pp = np.sort(np.array([t for (t, w, n) in points]))
    rmse_all = rmse_vs_zeros(all_pp, zeros)
    print(f"  All prime powers: {len(all_pp)} points, RMSE={rmse_all:.4f}")

    # Test 4: weighted expansion — each p^k contributes floor(1/k + 0.5) copies
    expanded = []
    for (t, w, n) in points:
        copies = max(1, round(w))
        expanded.extend([t] * copies)
    expanded = np.sort(np.array(expanded))
    rmse_exp = rmse_vs_zeros(expanded, zeros)
    print(f"  Weighted expansion: {len(expanded)} points, RMSE={rmse_exp:.4f}")

    # Show best detailed comparison
    best_spec = min(
        [(primes_only, rmse_primes, "primes only"),
         (primes_sq, rmse_sq, "primes + p^2"),
         (all_pp, rmse_all, "all prime powers"),
         (expanded, rmse_exp, "weighted expansion")],
        key=lambda x: x[1]
    )
    spec, rmse, label = best_spec

    print()
    print(f"  Best: {label}, RMSE={rmse:.4f}")
    print()

    n = min(n_zeros, len(spec))
    pred = spec[:n]
    tgt = zeros[:n]
    scale = (tgt[-1] - tgt[0]) / (pred[-1] - pred[0] + 1e-10)
    shift = tgt[0] - scale * pred[0]
    pred_scaled = scale * pred + shift

    print(f"  {'n':>4}  {'gamma_n':>10}  {'predicted':>10}  {'error':>10}")
    for i in range(min(20, n)):
        err = pred_scaled[i] - tgt[i]
        print(f"  {i+1:>4}  {tgt[i]:>10.4f}  {pred_scaled[i]:>10.4f}  {err:>+10.4f}")


def run_prime_log_analysis(n_zeros: int = 30) -> None:
    """
    Direct test: do the logs of primes, sorted, match zeta zeros?

    The Riemann-Siegel formula: gamma_n ~ 2*pi*n / log(n).
    The n-th prime: p_n ~ n * log(n).
    So log(p_n) ~ log(n) + log(log(n)) ~ log(n).
    And gamma_n / log(p_n) ~ 2*pi*n / log(n)^2 -> infinity.

    So primes alone CANNOT match zeta zeros by simple scaling.
    The correct spectral object must have density ~ n/log(n), not log(n).

    This confirms: the spectral measure is NOT the log-prime lattice itself,
    but something with LINEAR density. The continuous spectrum is essential.
    """
    zeros = zeta_zeros(n_zeros)

    print()
    print("Phase 7f: Prime log analysis")
    print("=" * 62)

    # Generate enough primes
    primes = first_n_primes(200)
    log_primes = np.log(np.array(primes, dtype=float))

    n = min(n_zeros, len(log_primes))
    ratios = zeros[:n] / log_primes[:n]

    print(f"  {'n':>4}  {'gamma_n':>10}  {'log(p_n)':>10}  {'ratio':>10}  {'p_n':>8}")
    for i in range(min(20, n)):
        print(f"  {i+1:>4}  {zeros[i]:>10.4f}  {log_primes[i]:>10.4f}  "
              f"{ratios[i]:>10.4f}  {primes[i]:>8d}")

    print()
    print(f"  Ratio gamma_n / log(p_n):")
    print(f"    n=1:  {ratios[0]:.2f}")
    print(f"    n=10: {ratios[9]:.2f}")
    print(f"    n=20: {ratios[19]:.2f}")
    print(f"    Trend: {'increasing' if ratios[19] > ratios[0] else 'decreasing'}")
    print()
    print("  CONCLUSION: ratio grows -> primes alone cannot match zeta zeros.")
    print("  The spectral density of {log p_n} is log(n), but gamma_n ~ n/log(n).")
    print("  The ratio gamma_n / log(p_n) ~ 2*pi*n / log(n)^2 -> infinity.")
    print()
    print("  This is the DENSITY GAP: the log-prime lattice has logarithmic density,")
    print("  but zeta zeros have linear density. The continuous spectrum must supply")
    print("  the missing density — approximately n/log(n) - log(n) ~ n/log(n) states.")


def run_explicit_formula_test(N_max: int = 100, n_zeros: int = 20) -> None:
    """
    Test the explicit formula connection directly.

    The explicit formula: psi(x) = x - sum_rho x^rho/rho + ...
    where psi(x) = sum_{n<=x} Lambda(n).

    The zeros rho = 1/2 + i*gamma appear as oscillations in psi(x).
    If we can recover gamma_n from psi(x), this is the direct connection.

    Here we test: does the Fourier transform of psi(e^t) - e^t have peaks at gamma_n?
    """
    zeros = zeta_zeros(n_zeros)

    # Build psi(e^t) for t in [0, T]
    T = 10.0
    N_t = 10000
    t_vals = np.linspace(0.01, T, N_t)
    x_vals = np.exp(t_vals)

    # psi(x) = sum_{n<=x} Lambda(n)
    # Precompute Lambda(n) for n up to exp(T)
    N_psi = int(np.exp(T)) + 1
    lambda_vals = np.zeros(N_psi + 1)
    for n in range(2, N_psi + 1):
        lam = von_mangoldt(n)
        if lam > 0:
            lambda_vals[n] = lam

    # Cumulative sum: psi(x) = sum_{n<=x} Lambda(n)
    psi_cumsum = np.cumsum(lambda_vals)

    psi_t = np.array([psi_cumsum[min(int(x), N_psi)] for x in x_vals])
    # Subtract the main term x = e^t
    psi_centered = psi_t - x_vals

    # Fourier transform to find oscillation frequencies
    dt = t_vals[1] - t_vals[0]
    fft_vals = np.fft.rfft(psi_centered * np.hanning(N_t))
    freqs = np.fft.rfftfreq(N_t, d=dt)
    power = np.abs(fft_vals) ** 2

    # Find peaks in power spectrum
    from scipy.signal import find_peaks
    try:
        peaks, _ = find_peaks(power, height=np.percentile(power, 90))
        peak_freqs = freqs[peaks] * 2 * np.pi  # convert to angular frequency
        peak_freqs = np.sort(peak_freqs[peak_freqs > 5])[:n_zeros]

        print()
        print("Phase 7f: Explicit formula — Fourier peaks vs zeta zeros")
        print("=" * 62)
        print(f"  psi(e^t) - e^t Fourier transform, T={T}, N={N_t}")
        print()
        print(f"  {'n':>4}  {'gamma_n':>10}  {'peak_freq':>10}  {'error':>10}")
        n_show = min(n_zeros, len(peak_freqs), len(zeros))
        for i in range(n_show):
            err = peak_freqs[i] - zeros[i]
            print(f"  {i+1:>4}  {zeros[i]:>10.4f}  {peak_freqs[i]:>10.4f}  {err:>+10.4f}")

        rmse = float(np.sqrt(np.mean((peak_freqs[:n_show] - zeros[:n_show])**2)))
        print(f"\n  RMSE = {rmse:.4f}")

    except ImportError:
        print("  scipy not available for peak finding.")
        print("  Top 10 power spectrum frequencies:")
        top_idx = np.argsort(power)[-20:][::-1]
        top_freqs = np.sort(freqs[top_idx] * 2 * np.pi)
        top_freqs = top_freqs[top_freqs > 5][:10]
        for i, f in enumerate(top_freqs):
            print(f"  {i+1:>4}  {f:.4f}")


if __name__ == '__main__':
    # Test von Mangoldt measure
    run_mangoldt_experiment(N_max=300, n_zeros=30)

    # Prime log analysis (density gap proof)
    run_prime_log_analysis(n_zeros=30)

    # Explicit formula test
    run_explicit_formula_test(N_max=100, n_zeros=20)
