"""
Phase 7d: Hybrid spectrum — discrete log-prime lattice + continuous fill.

Hypothesis from Phase 7b/7c:
  The continuous spectrum (Eisenstein series) fills the gaps between
  log-prime lattice points, converting log-density to linear-density.

Test: construct a hybrid spectral measure:
  1. Discrete part: log-prime lattice points t_n = sum_p k_p * log(p)
  2. Continuous fill: uniform points between consecutive lattice points
     with density proportional to the gap size

If the hybrid spectrum gives alpha -> 1 (for t) matching gamma_n,
this confirms that continuous + discrete together produce the correct density.

The number of fill points between t_n and t_{n+1} is chosen so that
the total density becomes LINEAR (uniform in t), not logarithmic.
"""

import numpy as np
from itertools import product as iproduct
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from constrained_adelic_experiment import zeta_zeros, compare_to_zeta_zeros


def first_n_primes(n: int) -> list:
    primes = []
    c = 2
    while len(primes) < n:
        if all(c % p != 0 for p in primes):
            primes.append(c)
        c += 1
    return primes


def build_log_prime_lattice(primes: list, K_max: int) -> np.ndarray:
    """All values of sum_p k_p * log(p), sorted."""
    t_vals = set()
    for combo in iproduct(*[range(K_max + 1) for _ in primes]):
        if all(k == 0 for k in combo):
            continue
        t = sum(k * np.log(p) for k, p in zip(combo, primes))
        t_vals.add(round(t, 10))
    return np.sort(list(t_vals))


def hybrid_spectrum(lattice: np.ndarray, fill_density: float) -> np.ndarray:
    """
    Hybrid spectrum: lattice points + uniform fill between them.

    fill_density: average number of continuous points per unit interval.
    Between lattice[i] and lattice[i+1], insert floor(gap * fill_density) points
    uniformly distributed in the gap.

    This models the Eisenstein series contribution as a uniform continuous measure.
    """
    points = list(lattice)

    for i in range(len(lattice) - 1):
        gap = lattice[i+1] - lattice[i]
        n_fill = max(0, int(round(gap * fill_density)))
        if n_fill > 0:
            fill = np.linspace(lattice[i], lattice[i+1], n_fill + 2)[1:-1]
            points.extend(fill.tolist())

    return np.sort(np.array(points))


def fit_growth_rate(vals: np.ndarray, n_fit: int = 30) -> float:
    """Fit lambda_n ~ C * n^alpha in log-log space."""
    vals = vals[:n_fit]
    if len(vals) < 3:
        return float('nan')
    ns = np.arange(1, len(vals) + 1)
    coeffs = np.polyfit(np.log(ns), np.log(vals + 1e-10), 1)
    return coeffs[0]


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


def run_hybrid_experiment(
    n_primes: int = 7,
    K_max: int = 4,
    fill_densities: list = None,
    verbose: bool = True,
) -> dict:
    zeros = zeta_zeros(30)
    primes = first_n_primes(n_primes)
    lattice = build_log_prime_lattice(primes, K_max)

    if fill_densities is None:
        # Try a range: 0 (pure discrete) to high density (nearly continuous)
        fill_densities = [0, 0.5, 1, 2, 5, 10, 20, 50, 100]

    print("Phase 7d: Hybrid Spectrum (Discrete + Continuous Fill)")
    print("=" * 62)
    print(f"Primes: {primes}")
    print(f"Lattice: {len(lattice)} points, range [{lattice[0]:.3f}, {lattice[min(20,len(lattice)-1)]:.3f}]")
    print()

    results = []

    for fd in fill_densities:
        spectrum = hybrid_spectrum(lattice, fill_density=fd)
        alpha_t = fit_growth_rate(spectrum, n_fit=30)
        alpha_t2 = fit_growth_rate(spectrum**2, n_fit=30)
        rmse = rmse_vs_zeros(spectrum, zeros)

        entry = {
            'fill_density': fd,
            'n_points': len(spectrum),
            'alpha_t': alpha_t,
            'alpha_t2': alpha_t2,
            'rmse': rmse,
        }
        results.append(entry)

        if verbose:
            print(f"  fill={fd:6.1f}: {len(spectrum):6d} pts | "
                  f"alpha(t)={alpha_t:.3f} | alpha(t^2)={alpha_t2:.3f} | "
                  f"RMSE={rmse:.4f}")

    print()
    print("--- Summary ---")
    print(f"  {'fill':>8}  {'n_pts':>7}  {'alpha(t)':>9}  {'alpha(t^2)':>11}  {'RMSE':>8}")
    print(f"  {'-'*8}  {'-'*7}  {'-'*9}  {'-'*11}  {'-'*8}")
    for r in results:
        marker = ""
        if abs(r['alpha_t'] - 1.0) < 0.1:
            marker = " <-- alpha(t)~1"
        elif abs(r['alpha_t2'] - 2.0) < 0.2:
            marker = " <-- alpha(t^2)~2"
        print(f"  {r['fill_density']:>8.1f}  {r['n_points']:>7d}  "
              f"{r['alpha_t']:>9.3f}  {r['alpha_t2']:>11.3f}  "
              f"{r['rmse']:>8.4f}{marker}")

    # Find best RMSE
    best = min(results, key=lambda r: r['rmse'])
    print()
    print(f"  Best RMSE: {best['rmse']:.4f} at fill_density={best['fill_density']}")

    # Find where alpha(t) crosses 1.0
    alphas = [r['alpha_t'] for r in results]
    crossings = [i for i in range(len(alphas)-1)
                 if (alphas[i] - 1.0) * (alphas[i+1] - 1.0) < 0]
    if crossings:
        i = crossings[0]
        fd_cross = (fill_densities[i] + fill_densities[i+1]) / 2
        print(f"  alpha(t) crosses 1.0 between fill={fill_densities[i]} and fill={fill_densities[i+1]}")
        print(f"  Estimated crossing: fill_density ~ {fd_cross:.1f}")
        print()
        print("  INTERPRETATION: at this fill density, the hybrid spectrum")
        print("  has the same growth rate as zeta zeros (gamma_n ~ n).")
        print("  This is the density of continuous spectrum needed to")
        print("  complement the discrete log-prime lattice.")
    elif alphas[-1] > 1.0:
        print("  alpha(t) never reaches 1.0 — need higher fill density.")
    else:
        print("  alpha(t) already below 1.0 at lowest fill — lattice too dense.")

    return results


def run_optimal_fill_detail(
    n_primes: int = 7,
    K_max: int = 4,
    verbose: bool = True,
) -> None:
    """
    Find the optimal fill density and show detailed comparison to zeta zeros.
    """
    zeros = zeta_zeros(30)
    primes = first_n_primes(n_primes)
    lattice = build_log_prime_lattice(primes, K_max)

    # Fine scan around the crossing point
    fine_densities = np.linspace(0, 30, 61)
    best_rmse = float('inf')
    best_fd = 0
    best_spectrum = None

    for fd in fine_densities:
        spectrum = hybrid_spectrum(lattice, fill_density=fd)
        rmse = rmse_vs_zeros(spectrum, zeros)
        if rmse < best_rmse:
            best_rmse = rmse
            best_fd = fd
            best_spectrum = spectrum

    print()
    print(f"Phase 7d: Optimal fill density scan (0 to 30, step 0.5)")
    print(f"  Best fill_density = {best_fd:.1f}, RMSE = {best_rmse:.6f}")
    print(f"  Spectrum size: {len(best_spectrum)} points")

    # Show comparison
    n_show = min(20, len(best_spectrum), len(zeros))
    n = n_show
    pred = best_spectrum[:n]
    tgt = zeros[:n]
    scale = (tgt[-1] - tgt[0]) / (pred[-1] - pred[0] + 1e-10)
    shift = tgt[0] - scale * pred[0]
    pred_scaled = scale * pred + shift

    print()
    print(f"  {'n':>4}  {'gamma_n':>10}  {'predicted':>10}  {'error':>10}")
    for i in range(n_show):
        err = pred_scaled[i] - tgt[i]
        print(f"  {i+1:>4}  {tgt[i]:>10.4f}  {pred_scaled[i]:>10.4f}  {err:>+10.4f}")

    alpha_t = fit_growth_rate(best_spectrum)
    alpha_t2 = fit_growth_rate(best_spectrum**2)
    print()
    print(f"  Growth rate alpha(t) = {alpha_t:.4f}  (target: 1.0)")
    print(f"  Growth rate alpha(t^2) = {alpha_t2:.4f}  (target: 2.0)")

    if best_rmse < 2.0:
        print()
        print("  *** RMSE < 2.0: hybrid spectrum closely matches zeta zeros ***")
        print("  The continuous fill density needed is approximately:")
        print(f"  {best_fd:.1f} points per unit interval in log-prime space.")
        print()
        print("  Physical interpretation:")
        print("  The Eisenstein series contribution to the spectral measure")
        print(f"  on A_Q/C_Q provides ~{best_fd:.0f} states per unit log-interval,")
        print("  complementing the discrete log-prime lattice to produce")
        print("  the correct zeta zero density.")


if __name__ == '__main__':
    # Coarse scan
    results = run_hybrid_experiment(
        n_primes=7,
        K_max=4,
        fill_densities=[0, 1, 2, 5, 10, 20, 50, 100, 200],
    )

    # Fine scan for best fit
    run_optimal_fill_detail(n_primes=7, K_max=4)
