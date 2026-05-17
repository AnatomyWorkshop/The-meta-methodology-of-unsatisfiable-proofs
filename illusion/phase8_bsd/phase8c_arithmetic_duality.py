"""
Phase 8c: Arithmetic duality operator for BSD.

Finding from Phase 8b:
  Index-reversal P gives corr(rank, defect) = 0.45 — not significant.
  The geometric P has no arithmetic meaning for elliptic curves.

The correct duality for BSD:
  The functional equation of L(E, s):
    L(E, s) = epsilon * N^(1-s) * (2*pi)^(2s-1) * Gamma(s)^2 * L(E, 2-s)
  where epsilon = root number (+1 or -1), N = conductor.

  This says: s <-> 1-s is the symmetry of L(E, s).
  The critical line Re(s) = 1/2 is the fixed point of this symmetry.

  In terms of the Euler product:
    L(E, s) = prod_p (1 - a_p p^{-s} + p^{1-2s})^{-1}
  The substitution s -> 1-s sends:
    p^{-s} -> p^{s-1} = p^{-(1-s)}
    a_p p^{-s} -> a_p p^{-(1-s)}

  So the duality operator P on the a_p space should implement:
    P: a_p(s) -> a_p(1-s)

  For the Hecke matrix H[i,j] = a_norm[i] * a_norm[j] where
  a_norm[i] = a_{p_i} / (2*sqrt(p_i)):

  The functional equation symmetry acts as:
    H[i,j] -> H[i,j] * (p_i * p_j)^{1/2 - s} / (p_i * p_j)^{1/2 - (1-s)}
            = H[i,j] * (p_i * p_j)^{2s-1}

  At s = 1/2 (critical line): (p_i * p_j)^0 = 1, so H is invariant.
  This means: the correct P for BSD is the one that implements s -> 1-s
  on the Hecke matrix, which at s=1/2 is the IDENTITY.

  But the rank information comes from the DERIVATIVE at s=1:
    L(E, 1) = 0 iff rank >= 1
    L'(E, 1) = 0 iff rank >= 2

  The duality s -> 1-s maps s=1 to s=0, not to itself.
  So the functional equation symmetry is NOT the right P for rank detection.

New approach: use the ROOT NUMBER as the duality operator.
  epsilon = +1: L(E, s) is symmetric under s -> 1-s
  epsilon = -1: L(E, s) is antisymmetric under s -> 1-s

  For rank 1 curves: epsilon = -1 (forced by parity of functional equation)
  For rank 2 curves: epsilon = +1 (forced by parity)
  For rank 0 curves: epsilon = +1

  So: epsilon discriminates rank parity, not rank value.
  rank 0 and rank 2 both have epsilon = +1.
  rank 1 has epsilon = -1.

  This is a NECESSARY condition for rank, not sufficient.

Correct BSD approach:
  The rank is encoded in the ANALYTIC RANK = ord_{s=1} L(E, s).
  To detect this numerically, we need to compute L(E, s) near s=1
  with enough precision to see the zero order.

  With only 10 primes, we can't do this accurately.
  We need to use the MODULAR SYMBOL method or the SAGE/PARI L-function.

  Since we don't have SAGE, we use a different approach:
  The Birch-Swinnerton-Dyer conjecture predicts:
    prod_{p <= X} (p / (p - a_p + 1)) ~ C * (log X)^r

  This is the BSD product formula. We can test it numerically.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from rank_discrimination import RANK_0_CURVES, RANK_1_CURVES, RANK_2_CURVES


# ---------------------------------------------------------------------------
# Root number computation
# ---------------------------------------------------------------------------

def root_number_sign(curve: dict) -> int:
    """
    Estimate the root number epsilon from the a_p data.

    For a curve with conductor N, the root number is:
      epsilon = (-1)^(number of prime factors of N with odd exponent)
    times local factors at 2 and 3.

    Simplified: use the parity of the analytic rank.
    rank even -> epsilon = +1
    rank odd  -> epsilon = -1
    """
    return (-1) ** curve['rank']


# ---------------------------------------------------------------------------
# BSD product formula test
# ---------------------------------------------------------------------------

def bsd_product(curve: dict, primes: list = None) -> dict:
    """
    Compute the BSD product: prod_{p <= X} p / (p - a_p + 1).

    BSD predicts: this product ~ C * (log X)^r as X -> infinity.
    So log(product) ~ r * log(log X) + const.

    We fit: log(product(X)) = r * log(log X) + C
    and extract the estimated rank r.
    """
    if primes is None:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    a_p_vals = curve['a_p'][:len(primes)]

    # Compute partial products up to each prime
    log_products = []
    for k in range(1, len(primes) + 1):
        log_prod = 0.0
        for i in range(k):
            p = primes[i]
            ap = a_p_vals[i]
            denom = p - ap + 1
            if denom > 0:
                log_prod += np.log(p / denom)
            # skip bad primes (denom <= 0)
        log_products.append(log_prod)

    log_products = np.array(log_products)
    log_log_primes = np.log(np.log(np.array(primes, dtype=float)))

    # Fit: log_product = r * log_log_p + C
    if len(log_products) >= 3:
        coeffs = np.polyfit(log_log_primes, log_products, 1)
        estimated_rank = coeffs[0]
        intercept = coeffs[1]
    else:
        estimated_rank = float('nan')
        intercept = float('nan')

    return {
        'label': curve['label'],
        'rank': curve['rank'],
        'estimated_rank': float(estimated_rank),
        'intercept': float(intercept),
        'final_log_product': float(log_products[-1]),
        'log_products': log_products,
    }


# ---------------------------------------------------------------------------
# Functional equation duality matrix
# ---------------------------------------------------------------------------

def functional_equation_P(n_primes: int, s_ref: float = 1.0) -> np.ndarray:
    """
    Duality operator implementing s -> 1-s on the Hecke matrix.

    At s = s_ref, the Euler factor for prime p is:
      f_p(s) = 1 - a_p * p^{-s} + p^{1-2s}

    The functional equation maps s -> 1-s, so:
      f_p(s) -> f_p(1-s) = 1 - a_p * p^{-(1-s)} + p^{2s-1}

    The ratio f_p(1-s) / f_p(s) defines how the duality acts on each
    prime's contribution. We use this ratio as the diagonal of P.

    At s = 1: f_p(1) = 1 - a_p/p + 1/p = (p - a_p + 1)/p
              f_p(0) = 1 - a_p*p + p = p(1 - a_p) + 1

    The duality matrix P_ij = delta_ij * f_{p_i}(1-s) / f_{p_i}(s)
    is diagonal, encoding how each prime's contribution transforms.
    """
    primes = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29][:n_primes], dtype=float)

    # Diagonal entries: ratio of Euler factors at s and 1-s
    diag = np.zeros(n_primes)
    for i, p in enumerate(primes):
        f_s = 1 - p**(-s_ref) + p**(1 - 2*s_ref)
        f_1ms = 1 - p**(-(1 - s_ref)) + p**(2*s_ref - 1)
        if abs(f_s) > 1e-10:
            diag[i] = f_1ms / f_s
        else:
            diag[i] = 1.0

    return np.diag(diag)


def hecke_functional_duality(curve: dict, n_primes: int = 10,
                              s_ref: float = 1.0) -> dict:
    """
    Compute duality defect using the functional equation P.

    This tests whether the Hecke matrix commutes with the
    functional equation symmetry — the correct arithmetic duality.
    """
    a_p = np.array(curve['a_p'][:n_primes], dtype=float)
    primes = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29][:n_primes], dtype=float)
    a_norm = a_p / (2 * np.sqrt(primes))

    H = np.outer(a_norm, a_norm)
    P = functional_equation_P(n_primes, s_ref)

    # Duality defect: ||[H, P]||_F
    commutator = H @ P - P @ H
    defect = np.linalg.norm(commutator, 'fro')

    # Since P is diagonal, [H, P]_ij = H_ij * (P_jj - P_ii)
    # This is zero iff H_ij = 0 whenever P_ii != P_jj
    # i.e., iff H is block-diagonal in the P-eigenspaces

    return {
        'label': curve['label'],
        'rank': curve['rank'],
        'defect_functional': float(defect),
        'P_diag': np.diag(P),
    }


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_arithmetic_duality_experiment(verbose: bool = True) -> None:
    all_curves = RANK_0_CURVES + RANK_1_CURVES + RANK_2_CURVES

    print("Phase 8c: Arithmetic Duality Operator for BSD")
    print("=" * 62)
    print()

    # --- BSD product formula ---
    print("1. BSD Product Formula: prod_p p/(p - a_p + 1) ~ C*(log X)^r")
    print(f"   {'Label':10s}  {'True r':>7}  {'Est. r':>8}  {'LogProd':>9}")
    print(f"   {'-'*10}  {'-'*7}  {'-'*8}  {'-'*9}")

    bsd_results = []
    for curve in all_curves:
        r = bsd_product(curve)
        bsd_results.append(r)
        print(f"   {r['label']:10s}  {r['rank']:>7}  "
              f"{r['estimated_rank']:>8.3f}  {r['final_log_product']:>9.4f}")

    print()
    for rank in [0, 1, 2]:
        subset = [r for r in bsd_results if r['rank'] == rank]
        if subset:
            mean_est = np.mean([r['estimated_rank'] for r in subset])
            mean_lp = np.mean([r['final_log_product'] for r in subset])
            print(f"   Rank {rank}: mean_estimated={mean_est:.3f}, "
                  f"mean_log_product={mean_lp:.4f}")

    ranks = [r['rank'] for r in bsd_results]
    est_ranks = [r['estimated_rank'] for r in bsd_results]
    corr = np.corrcoef(ranks, est_ranks)[0, 1]
    print(f"\n   Correlation(true rank, BSD estimated rank) = {corr:.4f}")

    print()

    # --- Functional equation duality ---
    print("2. Functional Equation Duality Defect (s -> 1-s)")
    print(f"   {'Label':10s}  {'Rank':>5}  {'Defect(s=1)':>12}  {'Defect(s=0.5)':>14}")
    print(f"   {'-'*10}  {'-'*5}  {'-'*12}  {'-'*14}")

    fe_results_s1 = []
    fe_results_s05 = []
    for curve in all_curves:
        r1 = hecke_functional_duality(curve, s_ref=1.0)
        r05 = hecke_functional_duality(curve, s_ref=0.5)
        fe_results_s1.append(r1)
        fe_results_s05.append(r05)
        print(f"   {r1['label']:10s}  {r1['rank']:>5}  "
              f"{r1['defect_functional']:>12.6f}  {r05['defect_functional']:>14.6f}")

    print()
    defects_s1 = [r['defect_functional'] for r in fe_results_s1]
    defects_s05 = [r['defect_functional'] for r in fe_results_s05]
    corr_s1 = np.corrcoef(ranks, defects_s1)[0, 1]
    corr_s05 = np.corrcoef(ranks, defects_s05)[0, 1]
    print(f"   Correlation(rank, defect at s=1.0) = {corr_s1:.4f}")
    print(f"   Correlation(rank, defect at s=0.5) = {corr_s05:.4f}")

    print()
    print("=" * 62)
    print("SUMMARY")
    print()
    print(f"  BSD product formula rank estimate: corr = {corr:.4f}")
    print(f"  Functional equation defect (s=1):  corr = {corr_s1:.4f}")
    print(f"  Functional equation defect (s=0.5): corr = {corr_s05:.4f}")
    print()

    best_corr = max(abs(corr), abs(corr_s1), abs(corr_s05))
    if best_corr > 0.7:
        print("  STRONG signal: at least one method correlates with rank.")
        print("  This is numerical evidence for UCA-BSD connection.")
    elif best_corr > 0.4:
        print("  WEAK signal: partial correlation, not conclusive.")
        print("  Need more primes or a different duality construction.")
    else:
        print("  NO signal: none of the methods correlate with rank.")
        print("  The arithmetic duality for BSD requires a fundamentally")
        print("  different construction — not derivable from a_p data alone.")
        print()
        print("  Honest conclusion: with 10 primes and no L-function library,")
        print("  we cannot numerically test the UCA-BSD connection.")
        print("  The BSD product formula needs ~1000 primes to converge.")


if __name__ == '__main__':
    run_arithmetic_duality_experiment()
