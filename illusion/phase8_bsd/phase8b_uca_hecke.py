"""
Phase 8b: UCA constraint on Hecke operators — rank lower bound test.

Core hypothesis (from Deepseek analysis):
  UCA duality constraint forces [T_p, D] = 0 for all Hecke operators T_p,
  where D is the spectral operator on L^2(A_Q/C_Q).

  If [T_p, D] = 0, then T_p preserves each eigenspace of D.
  The eigenspace dimension = spectral multiplicity = (by BSD) rank of E.

  Testable prediction:
    rank(E) = dim(common eigenspace of {T_p : p prime, p <= B})

  For rank 0: all T_p share a 1-dimensional eigenspace (trivial)
  For rank 1: T_p share a 1-dimensional eigenspace (one generator)
  For rank 2: T_p share a 2-dimensional eigenspace (two generators)

Numerical test:
  Build the "Hecke matrix" H_B = sum_{p <= B} T_p (as a matrix on a_p space)
  Compute its eigenvalue structure.
  If rank 2 curves show a 2-dimensional near-zero eigenspace of [H_B, H_B^T],
  this is numerical evidence for the UCA prediction.

Note: we don't have the actual Hecke operators on L^2(A_Q/C_Q).
We approximate them using the a_p data: T_p acts on the space of
modular forms by multiplication by a_p(f). The "eigenspace" is the
space of forms with the same a_p eigenvalues.

For a single elliptic curve E, the Hecke eigenvalues are just {a_p(E)}.
The rank prediction comes from the L-function: ord_{s=1} L(E,s) = rank(E).

What we CAN test numerically:
  The UCA duality defect of the Hecke matrix built from a_p data.
  If rank 2 curves have systematically different duality structure
  than rank 1 curves, this is evidence for the UCA-BSD connection.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from rank_discrimination import (
    RANK_0_CURVES, RANK_1_CURVES, RANK_2_CURVES, kronecker_symbol
)
from prism.core import parity_operator, optimize


# ---------------------------------------------------------------------------
# Build Hecke-like matrix from a_p data
# ---------------------------------------------------------------------------

def build_hecke_matrix(curve: dict, n_primes: int = 10) -> np.ndarray:
    """
    Build an n x n matrix encoding the Hecke action on the a_p space.

    For a curve E with a_p values [a_2, a_3, a_5, ...], we construct
    a matrix H where H[i,j] = a_{p_i} * a_{p_j} / sqrt(p_i * p_j).

    This is the "correlation matrix" of the normalized Hecke eigenvalues.
    Its eigenstructure encodes the multiplicative structure of the L-function.

    For rank r: the L-function has a zero of order r at s=1.
    The Hecke matrix should have r near-zero eigenvalues (in some sense).
    """
    a_p = np.array(curve['a_p'][:n_primes], dtype=float)
    primes = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29][:n_primes], dtype=float)

    # Normalize: a_p / (2 * sqrt(p)) in [-1, 1] by Hasse
    a_norm = a_p / (2 * np.sqrt(primes))

    # Outer product: H[i,j] = a_norm[i] * a_norm[j]
    H = np.outer(a_norm, a_norm)

    # Add diagonal: H[i,i] = a_norm[i]^2 (self-correlation)
    # This makes H positive semi-definite
    return H


def build_twist_matrix(curve: dict, d_values: list = None,
                       n_primes: int = 10) -> np.ndarray:
    """
    Build a matrix encoding the twist structure of the curve.

    For each quadratic twist d, compute the twisted a_p sequence.
    Stack these as rows to get a matrix T where T[d_idx, p_idx] = a_p(E^d).

    The rank of this matrix (or its near-zero singular values) should
    encode the rank of E via the twist formula:
      rank(E^d) = rank(E) + (contribution from d)
    """
    if d_values is None:
        d_values = list(range(-20, 21))
        d_values = [d for d in d_values if d != 0]

    a_p = np.array(curve['a_p'][:n_primes], dtype=float)
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29][:n_primes]

    rows = []
    for d in d_values:
        twisted = np.array([kronecker_symbol(d, p) * a_p[i]
                            for i, p in enumerate(primes)], dtype=float)
        rows.append(twisted)

    return np.array(rows)


# ---------------------------------------------------------------------------
# UCA duality analysis on Hecke matrices
# ---------------------------------------------------------------------------

def hecke_duality_analysis(curve: dict, n_primes: int = 10) -> dict:
    """
    Apply UCA duality analysis to the Hecke matrix of a curve.

    Returns:
      - duality_defect: ||[H, P]||_F where P = index-reversal
      - eigenvalues: sorted eigenvalues of H
      - n_near_zero: number of eigenvalues with |lambda| < threshold
      - spectral_gap: gap between smallest and second-smallest |eigenvalue|
    """
    H = build_hecke_matrix(curve, n_primes)
    n = H.shape[0]
    P = parity_operator(n)

    # Duality defect
    defect = np.linalg.norm(H @ P - P @ H, 'fro')

    # Eigenvalues
    evals = np.sort(np.linalg.eigvalsh(H))

    # Near-zero eigenvalues (threshold = 1% of max)
    threshold = 0.01 * np.max(np.abs(evals))
    n_near_zero = int(np.sum(np.abs(evals) < threshold))

    # Spectral gap
    abs_evals = np.sort(np.abs(evals))
    gap = abs_evals[1] - abs_evals[0] if len(abs_evals) > 1 else 0.0

    return {
        'label': curve['label'],
        'rank': curve['rank'],
        'duality_defect': float(defect),
        'eigenvalues': evals,
        'n_near_zero': n_near_zero,
        'spectral_gap': float(gap),
        'trace': float(np.trace(H)),
        'frobenius_norm': float(np.linalg.norm(H, 'fro')),
    }


def twist_rank_analysis(curve: dict, d_values: list = None,
                        n_primes: int = 10) -> dict:
    """
    Analyze the twist matrix singular value structure.

    The key BSD prediction: for rank r curve E,
    the twist matrix T should have r "large" singular values
    corresponding to the r independent generators of E(Q).

    We test: does the singular value gap between rank r and rank r+1
    singular values discriminate between rank 1 and rank 2 curves?
    """
    T = build_twist_matrix(curve, d_values, n_primes)

    # SVD
    U, s, Vt = np.linalg.svd(T, full_matrices=False)

    # Singular value gaps
    s_sorted = np.sort(s)[::-1]
    gaps = np.diff(s_sorted)

    # Relative gaps
    rel_gaps = gaps / (s_sorted[:-1] + 1e-10)

    return {
        'label': curve['label'],
        'rank': curve['rank'],
        'singular_values': s_sorted[:5],
        'top_gap': float(gaps[0]) if len(gaps) > 0 else 0.0,
        'rel_top_gap': float(rel_gaps[0]) if len(rel_gaps) > 0 else 0.0,
        'effective_rank': float(np.sum(s > 0.1 * s[0])),
    }


# ---------------------------------------------------------------------------
# L-function zero order test (direct BSD test)
# ---------------------------------------------------------------------------

def l_function_zero_order(curve: dict, n_terms: int = 200) -> dict:
    """
    Estimate the order of vanishing of L(E, s) at s=1 numerically.

    L(E, s) = prod_p (1 - a_p p^{-s} + p^{1-2s})^{-1}  (good primes)

    We compute L(E, s) for s near 1 and fit the order of vanishing.
    This is a direct numerical test of BSD.

    Note: this requires more a_p values than we have hardcoded.
    We use the available a_p and extrapolate.
    """
    a_p_data = curve['a_p']
    primes_data = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    # Compute partial L-function using available primes
    def partial_L(s, primes, a_p_vals):
        log_L = 0.0
        for p, ap in zip(primes, a_p_vals):
            # Euler factor: (1 - ap*p^{-s} + p^{1-2s})^{-1}
            factor = 1 - ap * p**(-s) + p**(1 - 2*s)
            if abs(factor) > 1e-10:
                log_L -= np.log(abs(factor))
        return np.exp(log_L)

    # Sample L(E, s) near s=1
    s_vals = np.linspace(1.01, 1.5, 20)
    L_vals = np.array([partial_L(s, primes_data, a_p_data) for s in s_vals])

    # Fit: log|L(E,s)| ~ r * log(s-1) + const near s=1
    # (order of vanishing = r)
    log_s_minus_1 = np.log(s_vals - 1)
    log_L_vals = np.log(L_vals + 1e-10)

    # Linear fit in log-log space
    coeffs = np.polyfit(log_s_minus_1, log_L_vals, 1)
    estimated_order = coeffs[0]

    return {
        'label': curve['label'],
        'rank': curve['rank'],
        'estimated_vanishing_order': float(estimated_order),
        'L_at_1p01': float(partial_L(1.01, primes_data, a_p_data)),
        'L_at_1p1': float(partial_L(1.1, primes_data, a_p_data)),
        'L_at_1p5': float(partial_L(1.5, primes_data, a_p_data)),
    }


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_bsd_uca_experiment(verbose: bool = True) -> None:
    all_curves = RANK_0_CURVES + RANK_1_CURVES + RANK_2_CURVES

    print("Phase 8b: UCA Constraint on Hecke Operators — BSD Rank Test")
    print("=" * 62)
    print()

    # --- Hecke duality analysis ---
    print("1. Hecke Matrix Duality Defect (UCA constraint test)")
    print(f"   {'Label':10s}  {'Rank':>5}  {'Defect':>10}  {'NearZero':>9}  "
          f"{'Gap':>8}  {'Trace':>8}")
    print(f"   {'-'*10}  {'-'*5}  {'-'*10}  {'-'*9}  {'-'*8}  {'-'*8}")

    hecke_results = []
    for curve in all_curves:
        r = hecke_duality_analysis(curve)
        hecke_results.append(r)
        print(f"   {r['label']:10s}  {r['rank']:>5}  {r['duality_defect']:>10.4f}  "
              f"{r['n_near_zero']:>9}  {r['spectral_gap']:>8.4f}  {r['trace']:>8.4f}")

    # Summary by rank
    print()
    for rank in [0, 1, 2]:
        subset = [r for r in hecke_results if r['rank'] == rank]
        if subset:
            mean_defect = np.mean([r['duality_defect'] for r in subset])
            mean_zero = np.mean([r['n_near_zero'] for r in subset])
            mean_gap = np.mean([r['spectral_gap'] for r in subset])
            print(f"   Rank {rank}: mean_defect={mean_defect:.4f}, "
                  f"mean_near_zero={mean_zero:.1f}, mean_gap={mean_gap:.4f}")

    print()

    # --- Twist matrix SVD ---
    print("2. Twist Matrix Singular Value Structure")
    print(f"   {'Label':10s}  {'Rank':>5}  {'SV1':>8}  {'SV2':>8}  "
          f"{'SV3':>8}  {'TopGap':>8}  {'EffRank':>8}")
    print(f"   {'-'*10}  {'-'*5}  {'-'*8}  {'-'*8}  {'-'*8}  {'-'*8}  {'-'*8}")

    twist_results = []
    for curve in all_curves:
        r = twist_rank_analysis(curve)
        twist_results.append(r)
        sv = r['singular_values']
        sv_str = [f"{sv[i]:8.3f}" if i < len(sv) else f"{'N/A':>8}" for i in range(3)]
        print(f"   {r['label']:10s}  {r['rank']:>5}  {''.join(sv_str)}  "
              f"{r['top_gap']:>8.3f}  {r['effective_rank']:>8.1f}")

    print()
    for rank in [0, 1, 2]:
        subset = [r for r in twist_results if r['rank'] == rank]
        if subset:
            mean_sv1 = np.mean([r['singular_values'][0] for r in subset])
            mean_sv2 = np.mean([r['singular_values'][1] for r in subset if len(r['singular_values']) > 1])
            mean_eff = np.mean([r['effective_rank'] for r in subset])
            print(f"   Rank {rank}: mean_SV1={mean_sv1:.3f}, mean_SV2={mean_sv2:.3f}, "
                  f"mean_eff_rank={mean_eff:.1f}")

    print()

    # --- L-function zero order ---
    print("3. L-function Vanishing Order (direct BSD test)")
    print(f"   {'Label':10s}  {'True rank':>10}  {'Est. order':>11}  "
          f"{'L(1.01)':>10}  {'L(1.5)':>8}")
    print(f"   {'-'*10}  {'-'*10}  {'-'*11}  {'-'*10}  {'-'*8}")

    l_results = []
    for curve in all_curves:
        r = l_function_zero_order(curve)
        l_results.append(r)
        print(f"   {r['label']:10s}  {r['rank']:>10}  "
              f"{r['estimated_vanishing_order']:>11.3f}  "
              f"{r['L_at_1p01']:>10.4f}  {r['L_at_1p5']:>8.4f}")

    print()
    print("   Note: estimated order uses only 10 primes — expect noise.")
    print("   Rank 0: L(1) != 0, so order ~ 0")
    print("   Rank 1: L(1) = 0, L'(1) != 0, so order ~ 1")
    print("   Rank 2: L(1) = L'(1) = 0, L''(1) != 0, so order ~ 2")

    print()
    print("=" * 62)
    print("INTERPRETATION")
    print()
    print("UCA prediction: [T_p, D] = 0 forces spectral multiplicity = rank.")
    print("Numerical proxy: Hecke matrix duality defect should correlate with rank.")
    print()

    # Check correlation
    defects = [r['duality_defect'] for r in hecke_results]
    ranks = [r['rank'] for r in hecke_results]
    corr = np.corrcoef(ranks, defects)[0, 1]
    print(f"Correlation(rank, duality_defect) = {corr:.4f}")

    eff_ranks = [r['effective_rank'] for r in twist_results]
    corr2 = np.corrcoef(ranks, eff_ranks)[0, 1]
    print(f"Correlation(rank, twist_eff_rank) = {corr2:.4f}")

    l_orders = [r['estimated_vanishing_order'] for r in l_results]
    corr3 = np.corrcoef(ranks, l_orders)[0, 1]
    print(f"Correlation(rank, L_vanishing_order) = {corr3:.4f}")

    print()
    if abs(corr) > 0.5:
        print("  Hecke duality defect correlates with rank.")
        print("  This is consistent with UCA prediction.")
    else:
        print("  Hecke duality defect does NOT correlate with rank.")
        print("  The index-reversal P is not the right duality operator for BSD.")
        print("  Need: a P that reflects the arithmetic structure of E.")


if __name__ == '__main__':
    run_bsd_uca_experiment()
