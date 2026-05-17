"""
Phase 8d: Generate a_p data for more primes using the curve equation.

For elliptic curves in Weierstrass form y^2 = x^3 + ax + b,
we can compute a_p = p + 1 - #E(F_p) by counting points mod p.

This gives us a_p for all primes up to any bound B,
enabling the BSD product formula to converge.

Curves used (Cremona labels, Weierstrass coefficients from LMFDB):
  389a1: y^2 + y = x^3 + x^2 - 2x  [rank 2]
  37a1:  y^2 + y = x^3 - x          [rank 1]
  11a1:  y^2 + y = x^3 - x^2 - 10x - 10  [rank 0]
  433a1: y^2 + y = x^3 + x^2 - 12x + 3  [rank 2]
  571a1: y^2 + y = x^3 - x^2 - 3x + 2  [rank 2]
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))


# ---------------------------------------------------------------------------
# Elliptic curve point counting mod p
# ---------------------------------------------------------------------------

def weierstrass_to_short(a1, a2, a3, a4, a6):
    """Convert general Weierstrass to short form y^2 = x^3 + Ax + B."""
    # Standard transformation
    b2 = a1**2 + 4*a2
    b4 = a1*a3 + 2*a4
    b6 = a3**2 + 4*a6
    b8 = a1**2*a6 - a1*a3*a4 + 4*a2*a6 + a2*a3**2 - a4**2
    return b2, b4, b6, b8


def count_points_mod_p(a1, a2, a3, a4, a6, p):
    """
    Count #E(F_p) for y^2 + a1*x*y + a3*y = x^3 + a2*x^2 + a4*x + a6 mod p.

    Uses brute force: for each x in F_p, count y solutions.
    O(p^2) but fine for p < 1000.
    """
    if p == 2:
        # Special handling for p=2
        count = 1  # point at infinity
        for x in range(2):
            for y in range(2):
                lhs = (y*y + a1*x*y + a3*y) % 2
                rhs = (x*x*x + a2*x*x + a4*x + a6) % 2
                if lhs == rhs:
                    count += 1
        return count

    count = 1  # point at infinity
    for x in range(p):
        # RHS = x^3 + a2*x^2 + a4*x + a6 mod p
        rhs = (x**3 + a2*x**2 + a4*x + a6) % p
        # LHS = y^2 + (a1*x + a3)*y mod p
        # Complete the square: (y + (a1*x+a3)/2)^2 = rhs + ((a1*x+a3)/2)^2
        # For odd p: count y solutions
        c = (a1 * x + a3) % p
        # y^2 + c*y = rhs  =>  (y + c*inv2)^2 = rhs + c^2*inv4
        inv2 = pow(2, p - 2, p)
        disc = (rhs + c * c * pow(inv2, 2, p)) % p
        # Count solutions to z^2 = disc mod p
        if disc == 0:
            count += 1
        else:
            # Euler criterion: disc^((p-1)/2) = 1 iff disc is QR
            if pow(disc, (p - 1) // 2, p) == 1:
                count += 2
    return count


def compute_ap_sequence(a1, a2, a3, a4, a6, primes):
    """Compute a_p = p + 1 - #E(F_p) for each prime in list."""
    ap_vals = []
    for p in primes:
        n_pts = count_points_mod_p(a1, a2, a3, a4, a6, p)
        ap = p + 1 - n_pts
        ap_vals.append(ap)
    return ap_vals


def primes_up_to(B):
    """Sieve of Eratosthenes."""
    sieve = [True] * (B + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(B**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, B + 1, i):
                sieve[j] = False
    return [i for i in range(2, B + 1) if sieve[i]]


# ---------------------------------------------------------------------------
# Curve definitions (Weierstrass coefficients [a1, a2, a3, a4, a6])
# ---------------------------------------------------------------------------

CURVES_WEIERSTRASS = {
    # rank 0
    '11a1':  {'coefs': (0, -1, 1, -10, -10), 'rank': 0, 'conductor': 11},
    '37b1':  {'coefs': (0, 1, 1, -23, -50),  'rank': 0, 'conductor': 37},
    # rank 1
    '37a1':  {'coefs': (0, 0, 1, -1, 0),     'rank': 1, 'conductor': 37},
    '43a1':  {'coefs': (0, 1, 1, 0, 0),      'rank': 1, 'conductor': 43},
    '57a1':  {'coefs': (0, -1, 1, 0, 0),     'rank': 1, 'conductor': 57},
    # rank 2
    '389a1': {'coefs': (0, 1, 1, -2, 0),     'rank': 2, 'conductor': 389},
    '433a1': {'coefs': (0, 1, 1, -12, 3),    'rank': 2, 'conductor': 433},
    '571a1': {'coefs': (0, -1, 1, -3, 2),    'rank': 2, 'conductor': 571},
}


# ---------------------------------------------------------------------------
# BSD product formula with many primes
# ---------------------------------------------------------------------------

def bsd_product_many_primes(label: str, B: int = 500) -> dict:
    """
    Compute BSD product prod_{p <= B, p good} p/(p - a_p + 1)
    and fit log(product) ~ r * log(log B) + C.
    """
    curve = CURVES_WEIERSTRASS[label]
    a1, a2, a3, a4, a6 = curve['coefs']
    rank = curve['rank']
    N = curve['conductor']

    primes = [p for p in primes_up_to(B) if N % p != 0]  # good primes only

    print(f"  Computing a_p for {label} (rank {rank}), {len(primes)} good primes up to {B}...")
    ap_vals = compute_ap_sequence(a1, a2, a3, a4, a6, primes)

    # Cumulative log product
    log_prods = []
    running = 0.0
    for p, ap in zip(primes, ap_vals):
        denom = p - ap + 1
        if denom > 0:
            running += np.log(p / denom)
        log_prods.append(running)

    log_prods = np.array(log_prods)
    log_log_p = np.log(np.log(np.array(primes, dtype=float)))

    # Fit over last half (converged region)
    n_fit = len(log_prods) // 2
    coeffs = np.polyfit(log_log_p[n_fit:], log_prods[n_fit:], 1)
    estimated_rank = coeffs[0]

    return {
        'label': label,
        'rank': rank,
        'estimated_rank': float(estimated_rank),
        'final_log_product': float(log_prods[-1]),
        'n_primes': len(primes),
        'log_prods': log_prods,
        'log_log_p': log_log_p,
    }


def run_bsd_many_primes(B: int = 300, verbose: bool = True) -> None:
    print("Phase 8d: BSD Product Formula with Many Primes")
    print("=" * 62)
    print(f"Computing a_p by point counting up to B={B}")
    print()

    results = []
    for label in CURVES_WEIERSTRASS:
        r = bsd_product_many_primes(label, B=B)
        results.append(r)

    print()
    print(f"  {'Label':10s}  {'True r':>7}  {'Est. r':>8}  {'LogProd':>9}  {'N_primes':>9}")
    print(f"  {'-'*10}  {'-'*7}  {'-'*8}  {'-'*9}  {'-'*9}")
    for r in results:
        print(f"  {r['label']:10s}  {r['rank']:>7}  "
              f"{r['estimated_rank']:>8.3f}  {r['final_log_product']:>9.4f}  "
              f"{r['n_primes']:>9}")

    print()
    ranks = [r['rank'] for r in results]
    est = [r['estimated_rank'] for r in results]
    if len(set(ranks)) > 1:
        corr = np.corrcoef(ranks, est)[0, 1]
        print(f"  Correlation(true rank, BSD estimated rank) = {corr:.4f}")

        if corr > 0.7:
            print()
            print("  STRONG: BSD product formula discriminates rank with many primes.")
            print("  This confirms the UCA spectral multiplicity prediction:")
            print("  the rank is encoded in the growth rate of the Euler product.")
        elif corr > 0.4:
            print()
            print("  PARTIAL: some signal, but B is still too small.")
            print(f"  Try B=1000 for cleaner convergence.")
        else:
            print()
            print("  WEAK: even with many primes, the product formula is noisy.")
            print("  The BSD constant C varies too much between curves.")

    # Show rank-by-rank summary
    print()
    for rank in [0, 1, 2]:
        subset = [r for r in results if r['rank'] == rank]
        if subset:
            mean_est = np.mean([r['estimated_rank'] for r in subset])
            print(f"  Rank {rank}: mean estimated = {mean_est:.3f}")


if __name__ == '__main__':
    run_bsd_many_primes(B=300)
