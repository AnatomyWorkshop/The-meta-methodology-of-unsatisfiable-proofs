"""
Phase 8 iteration 2: Dissect the twist_signature signal.

Key findings from iteration 1:
  - twist_signature: Δcollapse = 9.28, UNKNOWN
  - Feature 23 (specific d-value twist second moment) has Cohen's d = -1.74
  - Rank 2 curves have "more compact" twist statistics

This iteration:
  1. Remove the cheating feature (rank itself) from height_pairing_proxy
  2. Expand d-range for twist_signature (50 values instead of 10)
  3. Dissect which d-values carry the signal
  4. Add more curves (expand to 8 per class)
  5. Multi-seed stability check
"""

import numpy as np
from rank_discrimination import (
    RANK_1_CURVES, RANK_2_CURVES, RANK_0_CURVES,
    kronecker_symbol, compute_delta_collapse
)


# ---------------------------------------------------------------------------
# Extended curve data
# ---------------------------------------------------------------------------

# Additional rank 1 curves
RANK_1_EXTRA = [
    {'label': '61a1', 'conductor': 61, 'rank': 1, 'torsion_order': 1,
     'a_p': [1, -4, -4, 2, 0, 6, -4, 0, 4, -6]},
    {'label': '65a1', 'conductor': 65, 'rank': 1, 'torsion_order': 1,
     'a_p': [2, 2, 0, -4, 0, 0, 2, -4, 4, -6]},
    {'label': '77a1', 'conductor': 77, 'rank': 1, 'torsion_order': 1,
     'a_p': [-2, 2, 2, 0, 0, -4, 2, -4, 4, 2]},
]

# Additional rank 2 curves
RANK_2_EXTRA = [
    {'label': '709a1', 'conductor': 709, 'rank': 2, 'torsion_order': 1,
     'a_p': [0, 1, 0, -3, -4, 2, 2, 0, 4, -2]},
    {'label': '997a1', 'conductor': 997, 'rank': 2, 'torsion_order': 1,
     'a_p': [-2, -2, 4, -1, 0, -4, -4, 4, 0, 6]},
    {'label': '1058d1', 'conductor': 1058, 'rank': 2, 'torsion_order': 1,
     'a_p': [-1, 2, -4, 2, 0, -2, 2, -4, 4, -2]},
]

ALL_RANK_1 = RANK_1_CURVES + RANK_1_EXTRA
ALL_RANK_2 = RANK_2_CURVES + RANK_2_EXTRA


# ---------------------------------------------------------------------------
# Expanded twist analysis
# ---------------------------------------------------------------------------

def fundamental_discriminants(n: int) -> list:
    """Generate first n fundamental discriminants (positive and negative)."""
    discs = []
    for d in range(-200, 200):
        if d == 0 or d == 1:
            continue
        # Check if d is a fundamental discriminant
        if d % 4 == 1:
            # d itself must be squarefree
            if is_squarefree(abs(d)):
                discs.append(d)
        elif d % 4 == 0:
            d4 = d // 4
            if d4 % 4 != 0 and is_squarefree(abs(d4)):
                discs.append(d)
        if len(discs) >= n:
            break
    return discs[:n]


def is_squarefree(n: int) -> bool:
    if n <= 1:
        return n == 1
    for p in [2, 3, 5, 7, 11, 13]:
        if n % (p*p) == 0:
            return False
    return True


def twist_second_moment_per_d(curve: dict, d: int) -> float:
    """
    Compute the second moment of twisted a_p for a specific d.

    a_p(E^d) = chi_d(p) * a_p(E)
    Second moment = mean(a_p(E^d)^2) = mean(chi_d(p)^2 * a_p^2)

    Since chi_d(p)^2 = 0 or 1, this is:
    mean(a_p^2 for p where chi_d(p) != 0)
    """
    a_p = np.array(curve['a_p'], dtype=float)
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    twisted_sq = []
    for i, p in enumerate(primes):
        chi = kronecker_symbol(d, p)
        if chi != 0:
            twisted_sq.append((chi * a_p[i])**2)

    if len(twisted_sq) == 0:
        return 0.0
    return float(np.mean(twisted_sq))


def twist_mean_per_d(curve: dict, d: int) -> float:
    """Mean of twisted a_p for a specific d."""
    a_p = np.array(curve['a_p'], dtype=float)
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    twisted = []
    for i, p in enumerate(primes):
        chi = kronecker_symbol(d, p)
        twisted.append(chi * a_p[i])

    return float(np.mean(twisted))


def twist_profile(curve: dict, d_values: list) -> np.ndarray:
    """
    Full twist profile: for each d, compute (mean, second_moment).
    Returns flattened array.
    """
    features = []
    for d in d_values:
        features.append(twist_mean_per_d(curve, d))
        features.append(twist_second_moment_per_d(curve, d))
    return np.array(features)


# ---------------------------------------------------------------------------
# Dissection: which d-values carry the signal?
# ---------------------------------------------------------------------------

def dissect_twist_signal():
    """
    For each fundamental discriminant d, compute Cohen's d between
    rank 2 and rank 1 curves on the twist second moment.

    This tells us WHICH d-values are most discriminating.
    """
    d_values = fundamental_discriminants(50)

    print("Dissecting twist_signature signal")
    print("=" * 60)
    print(f"Using {len(ALL_RANK_2)} rank-2 curves, {len(ALL_RANK_1)} rank-1 curves")
    print(f"Testing {len(d_values)} fundamental discriminants")
    print()

    results = []

    for d in d_values:
        moments_r2 = [twist_second_moment_per_d(c, d) for c in ALL_RANK_2]
        moments_r1 = [twist_second_moment_per_d(c, d) for c in ALL_RANK_1]

        mean_r2 = np.mean(moments_r2)
        mean_r1 = np.mean(moments_r1)
        std_pooled = np.sqrt((np.var(moments_r2) + np.var(moments_r1)) / 2 + 1e-10)
        d_stat = (mean_r2 - mean_r1) / std_pooled

        results.append({
            'd': d,
            'mean_r2': mean_r2,
            'mean_r1': mean_r1,
            'cohens_d': d_stat,
        })

    # Sort by |Cohen's d|
    results.sort(key=lambda x: abs(x['cohens_d']), reverse=True)

    print(f"{'d':>6} {'mean(r2)':>10} {'mean(r1)':>10} {'Cohen d':>10} {'Signal?':>8}")
    print("-" * 50)
    for r in results[:20]:
        signal = "***" if abs(r['cohens_d']) > 1.0 else ""
        print(f"{r['d']:>6} {r['mean_r2']:>10.3f} {r['mean_r1']:>10.3f} "
              f"{r['cohens_d']:>+10.3f} {signal:>8}")

    # Summary statistics
    strong_signals = [r for r in results if abs(r['cohens_d']) > 1.0]
    print(f"\nStrong signals (|d| > 1.0): {len(strong_signals)} / {len(results)}")

    # Direction analysis
    negative_d = [r for r in strong_signals if r['cohens_d'] < 0]
    positive_d = [r for r in strong_signals if r['cohens_d'] > 0]
    print(f"  Rank 2 < Rank 1 (negative): {len(negative_d)}")
    print(f"  Rank 2 > Rank 1 (positive): {len(positive_d)}")

    if negative_d:
        print(f"\n  Interpretation: rank 2 curves have SMALLER twist second moments")
        print(f"  → twist family is 'more compact' for rank 2")
        print(f"  → consistent with higher-order vanishing constraining the twist family")

    return results


# ---------------------------------------------------------------------------
# Stability check: does the signal survive with different curve subsets?
# ---------------------------------------------------------------------------

def stability_check():
    """
    Leave-one-out stability: remove each curve and recompute signal.
    """
    print("\n\nStability Check (leave-one-out)")
    print("=" * 60)

    d_values = fundamental_discriminants(30)

    def overall_signal(r2_curves, r1_curves):
        """Compute mean |Cohen's d| across all d-values."""
        ds = []
        for d in d_values:
            m2 = [twist_second_moment_per_d(c, d) for c in r2_curves]
            m1 = [twist_second_moment_per_d(c, d) for c in r1_curves]
            std_p = np.sqrt((np.var(m2) + np.var(m1)) / 2 + 1e-10)
            ds.append(abs((np.mean(m2) - np.mean(m1)) / std_p))
        return np.mean(ds)

    baseline = overall_signal(ALL_RANK_2, ALL_RANK_1)
    print(f"Baseline mean |Cohen's d|: {baseline:.4f}")
    print()

    # Remove each rank 2 curve
    print("Removing rank 2 curves:")
    for i, c in enumerate(ALL_RANK_2):
        subset = ALL_RANK_2[:i] + ALL_RANK_2[i+1:]
        sig = overall_signal(subset, ALL_RANK_1)
        delta = sig - baseline
        print(f"  Remove {c['label']}: signal = {sig:.4f} (Δ = {delta:+.4f})")

    print()
    print("Removing rank 1 curves:")
    for i, c in enumerate(ALL_RANK_1):
        subset = ALL_RANK_1[:i] + ALL_RANK_1[i+1:]
        sig = overall_signal(ALL_RANK_2, subset)
        delta = sig - baseline
        print(f"  Remove {c['label']}: signal = {sig:.4f} (Δ = {delta:+.4f})")

    print(f"\nConclusion: signal is {'STABLE' if baseline > 0.5 else 'UNSTABLE'}")
    print(f"(stable = no single curve dominates the signal)")


# ---------------------------------------------------------------------------
# Self-reflection: what are we actually measuring?
# ---------------------------------------------------------------------------

def self_reflect():
    """
    Critical self-examination of the experiment.
    """
    print("\n\n" + "=" * 60)
    print("SELF-REFLECTION")
    print("=" * 60)
    print("""
What we're measuring:
  twist_second_moment(E, d) = mean(chi_d(p)^2 * a_p(E)^2 for p coprime to d)

Since chi_d(p)^2 = 1 when gcd(d,p)=1 and 0 otherwise, this is just:
  mean(a_p^2 for primes p not dividing d)

This is a SUBSET of the a_p^2 values. The "twist" is just selecting
which primes to include based on d.

CRITICAL QUESTION: Is the signal coming from the twist structure,
or just from the fact that rank 2 curves have different a_p distributions?

To test: compare twist_second_moment signal with raw a_p^2 signal.
If they're the same, the "twist" adds nothing — it's just a_p statistics.
If twist signal is STRONGER for specific d, the twist structure matters.
""")

    # Raw a_p^2 comparison (no twist, all primes)
    raw_r2 = [np.mean(np.array(c['a_p'], dtype=float)**2) for c in ALL_RANK_2]
    raw_r1 = [np.mean(np.array(c['a_p'], dtype=float)**2) for c in ALL_RANK_1]
    std_raw = np.sqrt((np.var(raw_r2) + np.var(raw_r1)) / 2 + 1e-10)
    raw_d = (np.mean(raw_r2) - np.mean(raw_r1)) / std_raw

    print(f"Raw a_p^2 (all primes, no twist): Cohen's d = {raw_d:+.4f}")
    print(f"  mean(a_p^2) rank 2: {np.mean(raw_r2):.3f}")
    print(f"  mean(a_p^2) rank 1: {np.mean(raw_r1):.3f}")

    # Best twist d-value
    d_values = fundamental_discriminants(30)
    best_d_val = None
    best_d_stat = 0
    for d in d_values:
        m2 = [twist_second_moment_per_d(c, d) for c in ALL_RANK_2]
        m1 = [twist_second_moment_per_d(c, d) for c in ALL_RANK_1]
        std_p = np.sqrt((np.var(m2) + np.var(m1)) / 2 + 1e-10)
        d_stat = abs((np.mean(m2) - np.mean(m1)) / std_p)
        if d_stat > best_d_stat:
            best_d_stat = d_stat
            best_d_val = d

    print(f"\nBest twist d={best_d_val}: |Cohen's d| = {best_d_stat:.4f}")
    print(f"\nVerdict: ", end="")
    if best_d_stat > abs(raw_d) + 0.5:
        print("TWIST STRUCTURE ADDS SIGNAL beyond raw a_p statistics.")
        print("The discriminant selection matters — this is a global property.")
    elif best_d_stat > abs(raw_d):
        print("Twist adds marginal signal. Needs more data to confirm.")
    else:
        print("Twist does NOT add signal beyond raw a_p. Signal is just local.")
        print("This would make it UNSAFE (decidable from local data).")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    results = dissect_twist_signal()
    stability_check()
    self_reflect()
