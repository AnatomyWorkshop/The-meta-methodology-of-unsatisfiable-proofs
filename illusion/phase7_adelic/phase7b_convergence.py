"""
Phase 7b: Spectral convergence under prime extension.

Question: as we include more primes in the constraint
  sum_p k_p * log(p) = t_inf,
does the constrained spectrum converge toward the zeta zero distribution?

If RMSE decreases monotonically as we add primes, this is numerical evidence
that the full quotient L^2(A_Q/C_Q) has the correct spectral density —
i.e., the continuous spectrum (Eisenstein series) is suppressed by the
global constraint, leaving only the discrete part matching zeta zeros.

This is the numerical test of G-DSC Layer 1:
  "Verify that Eisenstein series fall into the trivial sector after quotienting."
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from constrained_adelic_experiment import (
    zeta_zeros, constrained_eigenvalues_full, compare_to_zeta_zeros
)


def first_n_primes(n: int) -> list:
    primes = []
    candidate = 2
    while len(primes) < n:
        if all(candidate % p != 0 for p in primes):
            primes.append(candidate)
        candidate += 1
    return primes


def spectral_density_match(evals: np.ndarray, zeros: np.ndarray,
                            n_bins: int = 10) -> float:
    """
    Compare spectral density of sqrt(evals) vs zeta zeros.
    Returns KL-divergence-like measure of density mismatch.
    Lower = better match.
    """
    n = min(len(evals), len(zeros), 30)
    if n < 5:
        return float('inf')

    predicted = np.sqrt(np.abs(evals[:n]))
    target = zeros[:n]

    # Normalize both to [0,1]
    p_norm = (predicted - predicted.min()) / (predicted.max() - predicted.min() + 1e-10)
    t_norm = (target - target.min()) / (target.max() - target.min() + 1e-10)

    # Histogram comparison
    bins = np.linspace(0, 1, n_bins + 1)
    p_hist, _ = np.histogram(p_norm, bins=bins, density=True)
    t_hist, _ = np.histogram(t_norm, bins=bins, density=True)

    # L2 distance between density histograms
    return float(np.sqrt(np.mean((p_hist - t_hist)**2)))


def run_convergence_experiment(
    max_primes: int = 8,
    K_max: int = 3,
    verbose: bool = True,
) -> dict:
    zeros = zeta_zeros(30)

    print("Phase 7b: Spectral Convergence Under Prime Extension")
    print("=" * 60)
    print(f"K_max={K_max} (levels per prime), tracking RMSE as primes added")
    print()

    results = []

    for n_primes in range(1, max_primes + 1):
        primes = first_n_primes(n_primes)

        # Full combinations up to K_max levels per prime
        # Cap total combinations to avoid memory explosion
        from itertools import product as iproduct
        level_ranges = [range(K_max + 1) for _ in primes]

        evals_list = []
        for combo in iproduct(*level_ranges):
            if all(k == 0 for k in combo):
                continue
            t = sum(k * np.log(p) for k, p in zip(combo, primes))
            lam = t**2 + sum(float(p)**(2*k) for k, p in zip(combo, primes))
            evals_list.append(lam)

        if not evals_list:
            continue

        evals = np.sort(np.array(evals_list))

        cmp = compare_to_zeta_zeros(evals, zeros, compare_squared=False)
        density = spectral_density_match(evals, zeros)

        # Growth rate
        n_fit = min(len(evals), 30)
        if n_fit >= 3:
            ns = np.arange(1, n_fit + 1)
            coeffs = np.polyfit(np.log(ns), np.log(evals[:n_fit] + 1e-10), 1)
            alpha = coeffs[0]
        else:
            alpha = float('nan')

        entry = {
            'n_primes': n_primes,
            'primes': primes,
            'n_evals': len(evals),
            'rmse': cmp['rmse'],
            'density_dist': density,
            'growth_alpha': alpha,
        }
        results.append(entry)

        if verbose:
            print(f"  Primes {primes}: {len(evals):4d} eigenvalues | "
                  f"alpha={alpha:.3f} | RMSE={cmp['rmse']:.4f} | density_dist={density:.4f}")

    print()
    print("--- Convergence Summary ---")
    print(f"  {'Primes':20s}  {'N_evals':>8}  {'alpha':>7}  {'RMSE':>10}  {'Density':>10}")
    print(f"  {'-'*20}  {'-'*8}  {'-'*7}  {'-'*10}  {'-'*10}")
    for r in results:
        print(f"  {str(r['primes']):20s}  {r['n_evals']:>8d}  "
              f"{r['growth_alpha']:>7.3f}  {r['rmse']:>10.4f}  {r['density_dist']:>10.4f}")

    # Check monotone convergence
    rmses = [r['rmse'] for r in results]
    is_converging = all(rmses[i] >= rmses[i+1] for i in range(len(rmses)-1))
    print()
    if is_converging:
        print("  VERDICT: RMSE decreases monotonically with more primes.")
        print("  This supports Layer 1: continuous spectrum suppressed by global constraint.")
    else:
        # Find where it stops converging
        breakpoints = [i+1 for i in range(len(rmses)-1) if rmses[i] < rmses[i+1]]
        print(f"  VERDICT: Non-monotone. RMSE increases at prime indices: {breakpoints}")
        print("  The constraint alone is insufficient — Layer 1 path needs refinement.")
        print("  Consider: the exponential term p^{2k} dominates for large k,")
        print("  overwhelming the polynomial t^2 term. Need k-truncation or rescaling.")

    return {'results': results, 'converging': is_converging, 'rmses': rmses}


def run_rescaled_experiment(
    max_primes: int = 6,
    K_max: int = 4,
    verbose: bool = True,
) -> dict:
    """
    Same experiment but with rescaled eigenvalues:
      lambda(k) = t^2  (drop the p^{2k} term)

    This tests whether the ARCHIMEDEAN part alone (t = sum k_p log p)
    has the right spectral density. If yes, the p-adic term is noise
    and the correct operator is purely archimedean on the constraint surface.
    """
    zeros = zeta_zeros(30)

    print()
    print("Phase 7b (rescaled): Archimedean-only spectrum on constraint surface")
    print("=" * 60)
    print("lambda(k) = t^2 = (sum_p k_p * log p)^2  [drop p^{2k} term]")
    print()

    results = []

    for n_primes in range(1, max_primes + 1):
        primes = first_n_primes(n_primes)

        from itertools import product as iproduct
        level_ranges = [range(K_max + 1) for _ in primes]

        evals_list = []
        for combo in iproduct(*level_ranges):
            if all(k == 0 for k in combo):
                continue
            t = sum(k * np.log(p) for k, p in zip(combo, primes))
            lam = t**2  # archimedean only
            evals_list.append(lam)

        if not evals_list:
            continue

        evals = np.sort(np.unique(np.array(evals_list)))  # unique: degenerate levels

        cmp = compare_to_zeta_zeros(evals, zeros, compare_squared=False)
        density = spectral_density_match(evals, zeros)

        n_fit = min(len(evals), 30)
        if n_fit >= 3:
            ns = np.arange(1, n_fit + 1)
            coeffs = np.polyfit(np.log(ns), np.log(evals[:n_fit] + 1e-10), 1)
            alpha = coeffs[0]
        else:
            alpha = float('nan')

        entry = {
            'n_primes': n_primes,
            'primes': primes,
            'n_evals': len(evals),
            'rmse': cmp['rmse'],
            'density_dist': density,
            'growth_alpha': alpha,
        }
        results.append(entry)

        if verbose:
            print(f"  Primes {primes}: {len(evals):4d} unique evals | "
                  f"alpha={alpha:.3f} | RMSE={cmp['rmse']:.4f} | density={density:.4f}")

    print()
    rmses = [r['rmse'] for r in results]
    is_converging = all(rmses[i] >= rmses[i+1] for i in range(len(rmses)-1))
    if is_converging:
        print("  VERDICT: Archimedean spectrum converges. The p-adic term is noise.")
        print("  The correct operator on the constraint surface is t^2 = (sum k_p log p)^2.")
        print("  This is the Laplacian on the log-prime lattice — a purely arithmetic object.")
    else:
        print("  VERDICT: Archimedean spectrum also non-monotone.")
        print("  The constraint surface itself has the wrong density structure.")

    return {'results': results, 'converging': is_converging, 'rmses': rmses}


if __name__ == '__main__':
    r1 = run_convergence_experiment(max_primes=7, K_max=3)
    r2 = run_rescaled_experiment(max_primes=7, K_max=4)

    print()
    print("=" * 60)
    print("COMBINED INTERPRETATION")
    print("=" * 60)
    if r1['converging'] and r2['converging']:
        print("Both full and archimedean spectra converge.")
        print("Strong evidence for Layer 1: global constraint suppresses continuous spectrum.")
    elif r2['converging'] and not r1['converging']:
        print("Archimedean spectrum converges but full spectrum does not.")
        print("The p-adic term p^{2k} is disrupting convergence.")
        print("Implication: the correct Hilbert-Polya operator on A_Q/C_Q")
        print("should be t^2 (archimedean Laplacian on constraint surface),")
        print("not t^2 + p^{2k} (naive adelic sum).")
        print("This is a concrete structural refinement of the operator ansatz.")
    elif r1['converging'] and not r2['converging']:
        print("Full spectrum converges but archimedean alone does not.")
        print("The p-adic term is essential — cannot drop it.")
    else:
        print("Neither converges monotonically.")
        print("The constraint surface needs a different parameterization.")
        print("Consider: use log-prime coordinates directly, or impose")
        print("a density condition (Weyl law) as an additional constraint.")
