"""
Phase 7e: Smooth numbers hypothesis.

Finding from Phase 7d decoding:
  Each zeta zero gamma_n corresponds to a smooth number n via gamma_n ~ C * log(n).
  The log-prime lattice has 95 points in the range of 30 zeros — too dense.
  The continuous spectrum must PROJECT OUT the excess lattice points, not fill gaps.

Hypothesis:
  The surviving lattice points (after projection) are exactly the B-smooth numbers:
  integers whose prime factors are all <= B for some smoothness bound B.

  This is structurally motivated by the Euler product:
    zeta(s) = prod_p (1 - p^{-s})^{-1}
  The zeros of zeta encode the distribution of primes, and smooth numbers
  are the integers "generated" by a finite set of primes.

Test:
  1. Generate all B-smooth numbers up to some bound N_max
  2. Take their logarithms as the spectral points
  3. Compare to zeta zeros via affine scaling + RMSE
  4. Vary B (smoothness bound) and N_max to find optimal parameters

If RMSE drops significantly below Phase 7d's best (1.27), the hypothesis is confirmed.
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


def is_b_smooth(n: int, primes: list) -> bool:
    """Check if n is smooth with respect to the given prime set."""
    if n <= 1:
        return False
    for p in primes:
        while n % p == 0:
            n //= p
    return n == 1


def generate_smooth_numbers(primes: list, N_max: int) -> np.ndarray:
    """All B-smooth numbers up to N_max (B = max(primes))."""
    smooth = [n for n in range(2, N_max + 1) if is_b_smooth(n, primes)]
    return np.array(smooth)


def generate_smooth_logs(primes: list, N_max: int) -> np.ndarray:
    """Log of all B-smooth numbers up to N_max, sorted."""
    smooth = generate_smooth_numbers(primes, N_max)
    return np.log(smooth.astype(float))


def rmse_vs_zeros(spectrum: np.ndarray, zeros: np.ndarray, n: int = 30) -> float:
    """RMSE after affine scaling."""
    n = min(len(spectrum), len(zeros), n)
    if n < 3:
        return float('inf')
    pred = spectrum[:n]
    tgt = zeros[:n]
    scale = (tgt[-1] - tgt[0]) / (pred[-1] - pred[0] + 1e-10)
    shift = tgt[0] - scale * pred[0]
    return float(np.sqrt(np.mean((scale * pred + shift - tgt) ** 2)))


def fit_growth_rate(vals: np.ndarray, n_fit: int = 30) -> float:
    """Fit lambda_n ~ C * n^alpha in log-log space."""
    vals = vals[:n_fit]
    if len(vals) < 3:
        return float('nan')
    ns = np.arange(1, len(vals) + 1)
    coeffs = np.polyfit(np.log(ns), np.log(vals + 1e-10), 1)
    return coeffs[0]


def run_smooth_experiment(
    max_primes: int = 8,
    N_max_values: list = None,
    n_zeros: int = 50,
    verbose: bool = True,
) -> list:
    zeros = zeta_zeros(n_zeros)

    if N_max_values is None:
        N_max_values = [100, 200, 500, 1000, 2000, 5000]

    print("Phase 7e: Smooth Numbers Hypothesis")
    print("=" * 62)
    print(f"Testing: log(B-smooth numbers) as spectral points")
    print(f"Comparing to first {n_zeros} zeta zeros")
    print()

    results = []

    for n_primes in range(2, max_primes + 1):
        primes = first_n_primes(n_primes)
        B = primes[-1]

        for N_max in N_max_values:
            logs = generate_smooth_logs(primes, N_max)
            if len(logs) < 5:
                continue

            rmse_30 = rmse_vs_zeros(logs, zeros, n=30)
            rmse_50 = rmse_vs_zeros(logs, zeros, n=50)
            alpha = fit_growth_rate(logs, n_fit=min(50, len(logs)))

            entry = {
                'n_primes': n_primes,
                'primes': primes,
                'B': B,
                'N_max': N_max,
                'n_smooth': len(logs),
                'alpha': alpha,
                'rmse_30': rmse_30,
                'rmse_50': rmse_50,
            }
            results.append(entry)

            if verbose:
                print(f"  B={B:3d} (primes={str(primes):18s}), N_max={N_max:5d}: "
                      f"{len(logs):5d} smooth | alpha={alpha:.3f} | "
                      f"RMSE_30={rmse_30:.4f} | RMSE_50={rmse_50:.4f}")

        if verbose:
            print()

    # Summary: best RMSE_30 and RMSE_50
    valid = [r for r in results if r['rmse_30'] < float('inf')]
    if valid:
        best_30 = min(valid, key=lambda r: r['rmse_30'])
        best_50 = min(valid, key=lambda r: r['rmse_50'])
        print("--- Best results ---")
        print(f"  Best RMSE_30: {best_30['rmse_30']:.4f} "
              f"(B={best_30['B']}, N_max={best_30['N_max']}, "
              f"n_smooth={best_30['n_smooth']})")
        print(f"  Best RMSE_50: {best_50['rmse_50']:.4f} "
              f"(B={best_50['B']}, N_max={best_50['N_max']}, "
              f"n_smooth={best_50['n_smooth']})")

    return results


def run_detailed_comparison(
    n_primes: int = 6,
    N_max: int = 1000,
    n_zeros: int = 30,
) -> None:
    """Show detailed comparison for the best smooth number model."""
    zeros = zeta_zeros(n_zeros)
    primes = first_n_primes(n_primes)
    B = primes[-1]
    logs = generate_smooth_logs(primes, N_max)

    n = min(n_zeros, len(logs))
    pred = logs[:n]
    tgt = zeros[:n]
    scale = (tgt[-1] - tgt[0]) / (pred[-1] - pred[0] + 1e-10)
    shift = tgt[0] - scale * pred[0]
    pred_scaled = scale * pred + shift

    smooth_nums = generate_smooth_numbers(primes, N_max)

    print()
    print(f"Phase 7e: Detailed comparison (B={B}, N_max={N_max})")
    print(f"  Primes: {primes}")
    print(f"  {len(logs)} smooth numbers in range")
    print()
    print(f"  {'n':>4}  {'gamma_n':>10}  {'predicted':>10}  {'error':>10}  {'smooth_n':>10}  {'factored':>15}")
    print(f"  {'-'*4}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*15}")

    for i in range(n):
        err = pred_scaled[i] - tgt[i]
        sn = int(smooth_nums[i]) if i < len(smooth_nums) else -1
        # Factor the smooth number
        factored = _factor_str(sn, primes) if sn > 0 else "?"
        print(f"  {i+1:>4}  {tgt[i]:>10.4f}  {pred_scaled[i]:>10.4f}  "
              f"{err:>+10.4f}  {sn:>10d}  {factored:>15s}")

    rmse = float(np.sqrt(np.mean((pred_scaled - tgt[:n]) ** 2)))
    alpha = fit_growth_rate(logs)
    print()
    print(f"  RMSE = {rmse:.4f}")
    print(f"  alpha(log n_smooth) = {alpha:.4f}  (target: 1.0 for gamma_n ~ n)")


def _factor_str(n: int, primes: list) -> str:
    """Return factorization string like '2^3 * 3'."""
    if n <= 1:
        return str(n)
    parts = []
    for p in primes:
        exp = 0
        while n % p == 0:
            n //= p
            exp += 1
        if exp == 1:
            parts.append(str(p))
        elif exp > 1:
            parts.append(f"{p}^{exp}")
    return " * ".join(parts) if parts else str(n)


def run_scaling_analysis(n_zeros: int = 50) -> None:
    """
    Analyze the scaling constant C in gamma_n ~ C * log(n_smooth).

    If C is related to 2*pi or other fundamental constants, this is
    a structural connection to the Riemann-Siegel formula.
    """
    zeros = zeta_zeros(n_zeros)
    primes = first_n_primes(6)
    N_max = 2000
    logs = generate_smooth_logs(primes, N_max)
    smooth_nums = generate_smooth_numbers(primes, N_max)

    n = min(n_zeros, len(logs))
    ratios = zeros[:n] / (logs[:n] + 1e-10)

    print()
    print("Phase 7e: Scaling analysis gamma_n / log(n_smooth)")
    print(f"  Primes: {primes}, N_max={N_max}")
    print()
    print(f"  {'n':>4}  {'gamma_n':>10}  {'log(n_s)':>10}  {'ratio':>10}  {'n_smooth':>10}")
    for i in range(min(25, n)):
        sn = int(smooth_nums[i]) if i < len(smooth_nums) else -1
        print(f"  {i+1:>4}  {zeros[i]:>10.4f}  {logs[i]:>10.4f}  "
              f"{ratios[i]:>10.4f}  {sn:>10d}")

    mean_ratio = np.mean(ratios)
    std_ratio = np.std(ratios)
    print()
    print(f"  Mean ratio: {mean_ratio:.4f}")
    print(f"  Std ratio:  {std_ratio:.4f}  (relative: {std_ratio/mean_ratio:.4f})")
    print(f"  2*pi = {2*np.pi:.4f}")
    print(f"  pi^2 = {np.pi**2:.4f}")
    print(f"  2*pi^2 = {2*np.pi**2:.4f}")
    print(f"  ratio / (2*pi) = {mean_ratio / (2*np.pi):.4f}")
    print(f"  ratio / pi^2 = {mean_ratio / np.pi**2:.4f}")

    # Check if ratio grows with n (log correction)
    if n >= 10:
        ns = np.arange(1, n + 1)
        # Fit: ratio = A + B * log(n)
        coeffs = np.polyfit(np.log(ns), ratios, 1)
        print()
        print(f"  Fit: ratio = {coeffs[1]:.4f} + {coeffs[0]:.4f} * log(n)")
        print(f"  Log correction coefficient: {coeffs[0]:.4f}")
        if abs(coeffs[0]) < 0.5 * abs(coeffs[1]):
            print("  Ratio is approximately constant — pure scaling.")
        else:
            print("  Ratio grows with log(n) — logarithmic correction needed.")


if __name__ == '__main__':
    # Main experiment: vary B and N_max
    results = run_smooth_experiment(
        max_primes=7,
        N_max_values=[100, 300, 1000, 3000],
        n_zeros=50,
    )

    # Detailed comparison for best candidate
    print()
    print("=" * 62)
    run_detailed_comparison(n_primes=6, N_max=1000, n_zeros=30)

    # Scaling analysis
    print()
    print("=" * 62)
    run_scaling_analysis(n_zeros=30)
