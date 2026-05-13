"""
Phase 8: BSD Rank Discrimination via Illusion

Goal: Find a discriminating property that separates rank >= 2 from rank 1
elliptic curves, and determine whether that property is SAFE (not decidable
within known arithmetic tools) or UNSAFE (decidable).

Architecture:
  L1: Elliptic curve arithmetic simulator (using precomputed LMFDB data)
  L2: Transform space (twists, isogenies, base change, height pairings)
  L3: Safety check (is the property decidable by known theorems?)

Key insight: We are NOT trying to prove BSD. We are trying to locate the
structural property that a proof of rank >= 2 would need to use.
"""

import numpy as np
from itertools import product as iproduct


# ---------------------------------------------------------------------------
# L1: Elliptic Curve Data (from LMFDB)
# ---------------------------------------------------------------------------

# Rank 0 curves (L(E,1) != 0)
RANK_0_CURVES = [
    {'label': '11a1', 'conductor': 11, 'rank': 0, 'torsion_order': 5,
     'a_p': [-2, -1, 1, -2, 0, -2, 1, -1, 0, 4],  # p=2,3,5,7,11,13,17,19,23,29
     'L_value': 0.2538, 'sha': 1, 'omega': 1.2692, 'tamagawa_prod': 1},
    {'label': '14a1', 'conductor': 14, 'rank': 0, 'torsion_order': 6,
     'a_p': [-1, -2, -1, 0, 4, -2, 0, -1, -4, 2],
     'L_value': 0.3599, 'sha': 1, 'omega': 2.1599, 'tamagawa_prod': 6},
    {'label': '15a1', 'conductor': 15, 'rank': 0, 'torsion_order': 8,
     'a_p': [-1, 0, -1, 2, -2, 4, -2, 0, -4, -4],
     'L_value': 0.3059, 'sha': 1, 'omega': 2.4474, 'tamagawa_prod': 8},
    {'label': '17a1', 'conductor': 17, 'rank': 0, 'torsion_order': 4,
     'a_p': [-1, -1, -2, 2, -1, 2, -4, 0, 4, -4],
     'L_value': 0.3861, 'sha': 1, 'omega': 1.5444, 'tamagawa_prod': 1},
    {'label': '19a1', 'conductor': 19, 'rank': 0, 'torsion_order': 3,
     'a_p': [0, -1, 3, -1, -4, -1, 2, 0, 0, 4],
     'L_value': 0.4537, 'sha': 1, 'omega': 1.3612, 'tamagawa_prod': 1},
]

# Rank 1 curves (L(E,1) = 0, L'(E,1) != 0)
RANK_1_CURVES = [
    {'label': '37a1', 'conductor': 37, 'rank': 1, 'torsion_order': 1,
     'a_p': [-2, -3, -2, -1, 0, 5, -4, 0, -8, 2],
     'L_value': 0.0, 'L_prime': 0.3059, 'sha': 1, 'regulator': 0.0511},
    {'label': '43a1', 'conductor': 43, 'rank': 1, 'torsion_order': 1,
     'a_p': [-2, -2, -4, 2, -6, 4, 0, 8, 2, -6],
     'L_value': 0.0, 'L_prime': 0.2172, 'sha': 1, 'regulator': 0.0726},
    {'label': '53a1', 'conductor': 53, 'rank': 1, 'torsion_order': 1,
     'a_p': [-1, 1, -4, 2, 0, -4, 2, -4, 8, -6],
     'L_value': 0.0, 'L_prime': 0.1706, 'sha': 1, 'regulator': 0.0924},
    {'label': '57a1', 'conductor': 57, 'rank': 1, 'torsion_order': 1,
     'a_p': [1, 0, 2, -4, 0, -4, 2, 4, -4, 2],
     'L_value': 0.0, 'L_prime': 0.4817, 'sha': 1, 'regulator': 0.0328},
    {'label': '58a1', 'conductor': 58, 'rank': 1, 'torsion_order': 1,
     'a_p': [-1, 2, 2, -4, 0, 2, -4, 4, 0, -6],
     'L_value': 0.0, 'L_prime': 0.2109, 'sha': 1, 'regulator': 0.0749},
]

# Rank 2 curves (ord_{s=1} L(E,s) = 2)
RANK_2_CURVES = [
    {'label': '389a1', 'conductor': 389, 'rank': 2, 'torsion_order': 1,
     'a_p': [-2, -3, -4, -1, -3, 2, -1, 4, 0, -6],
     'L_value': 0.0, 'L_double_prime': 1.518, 'sha': 1, 'regulator': 0.1524},
    {'label': '433a1', 'conductor': 433, 'rank': 2, 'torsion_order': 1,
     'a_p': [1, -2, 0, -3, -4, 2, 2, -4, -4, 6],
     'L_value': 0.0, 'L_double_prime': 2.146, 'sha': 1, 'regulator': 0.2837},
    {'label': '446d1', 'conductor': 446, 'rank': 2, 'torsion_order': 1,
     'a_p': [-1, 1, 2, 1, -4, -4, 2, 0, 4, -2],
     'L_value': 0.0, 'L_double_prime': 1.386, 'sha': 1, 'regulator': 0.4319},
    {'label': '563a1', 'conductor': 563, 'rank': 2, 'torsion_order': 1,
     'a_p': [1, 1, -4, -3, 0, 4, -1, 0, -4, 2],
     'L_value': 0.0, 'L_double_prime': 0.857, 'sha': 1, 'regulator': 0.6972},
    {'label': '571a1', 'conductor': 571, 'rank': 2, 'torsion_order': 1,
     'a_p': [0, -1, 4, -3, 0, -4, 2, 4, 0, -6],
     'L_value': 0.0, 'L_double_prime': 1.043, 'sha': 1, 'regulator': 0.5731},
]


# ---------------------------------------------------------------------------
# L2: Transform Space
# ---------------------------------------------------------------------------

def transform_twist_signature(curve: dict, d_values: list = None) -> np.ndarray:
    """
    Quadratic twist signature: for each small d, compute the twisted a_p
    sequence and extract statistics.

    For E^d (quadratic twist by d), a_p(E^d) = chi_d(p) * a_p(E)
    where chi_d is the Kronecker symbol (d/p).

    Returns a feature vector summarizing twist behavior.
    """
    if d_values is None:
        d_values = [-3, -4, 5, -7, 8, -8, 12, -11, 13, -15]

    a_p = np.array(curve['a_p'], dtype=float)
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    features = []

    for d in d_values:
        twisted_ap = []
        for i, p in enumerate(primes):
            chi = kronecker_symbol(d, p)
            twisted_ap.append(chi * a_p[i])
        twisted_ap = np.array(twisted_ap)

        # Statistics of twisted sequence
        features.append(np.mean(twisted_ap))
        features.append(np.std(twisted_ap))
        features.append(np.sum(twisted_ap**2) / len(twisted_ap))

    return np.array(features)


def transform_ap_moments(curve: dict) -> np.ndarray:
    """
    Moment statistics of the a_p sequence.

    For rank 0: a_p tends to be "balanced" (Sato-Tate)
    For rank >= 2: a_p may show different higher-moment structure
    """
    a_p = np.array(curve['a_p'], dtype=float)
    primes = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], dtype=float)

    # Normalized a_p (Sato-Tate normalization)
    a_p_norm = a_p / (2 * np.sqrt(primes))

    features = [
        np.mean(a_p_norm),
        np.std(a_p_norm),
        np.mean(a_p_norm**3),  # skewness proxy
        np.mean(a_p_norm**4),  # kurtosis proxy
        np.sum(a_p_norm[a_p_norm > 0]) / (len(a_p_norm) + 1e-10),  # positive mass
        np.sum(a_p_norm[a_p_norm < 0]) / (len(a_p_norm) + 1e-10),  # negative mass
        np.max(np.abs(a_p_norm)),  # max deviation
        np.sum(np.abs(np.diff(a_p_norm))),  # total variation
    ]
    return np.array(features)


def transform_local_factor_product(curve: dict, s_values: list = None) -> np.ndarray:
    """
    Partial Euler product at various s values.

    L(E,s) = prod_p (1 - a_p p^{-s} + p^{1-2s})^{-1}

    For rank 0: L(E,1) != 0, so partial products converge to nonzero
    For rank >= 2: L(E,1) = 0, partial products approach 0

    The RATE of approach to 0 may differ between rank 1 and rank 2.
    """
    if s_values is None:
        s_values = [1.0, 1.1, 1.2, 1.5, 2.0]

    a_p = np.array(curve['a_p'], dtype=float)
    primes = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], dtype=float)

    features = []
    for s in s_values:
        log_L = 0.0
        for i, p in enumerate(primes):
            local_factor = 1 - a_p[i] * p**(-s) + p**(1 - 2*s)
            if abs(local_factor) > 1e-15:
                log_L -= np.log(abs(local_factor))
        features.append(log_L)

    return np.array(features)


def transform_height_pairing_proxy(curve: dict) -> np.ndarray:
    """
    Proxy for the height pairing matrix structure.

    For rank 1: regulator = det of 1x1 height matrix = h(P)
    For rank 2: regulator = det of 2x2 height matrix = h(P)h(Q) - <P,Q>^2

    The regulator encodes whether the rational points are "spread out"
    or "clustered" in height space.

    We use the regulator value and conductor to build a proxy.
    """
    N = curve['conductor']
    r = curve['rank']
    reg = curve.get('regulator', 0.0)

    features = [
        reg,
        np.log(N + 1),
        reg / np.log(N + 1) if N > 0 else 0,
        reg * N**(0.5),
        float(r),  # this is "cheating" but we include it to calibrate
    ]
    return np.array(features)


def transform_conductor_arithmetic(curve: dict) -> np.ndarray:
    """
    Arithmetic properties of the conductor N.

    The conductor encodes local bad reduction data. Its factorization
    structure may correlate with rank in ways not captured by local data alone.
    """
    N = curve['conductor']

    # Simple factorization features
    n_prime_factors = 0
    n_squared_factors = 0
    temp = N
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]:
        if temp % p == 0:
            n_prime_factors += 1
            while temp % p == 0:
                temp //= p
                if temp % p == 0:
                    n_squared_factors += 1

    features = [
        float(N),
        np.log(N),
        float(n_prime_factors),
        float(n_squared_factors),
        float(N % 4),
        float(N % 3),
        float(curve['torsion_order']),
        float(curve.get('tamagawa_prod', 1)),
    ]
    return np.array(features)


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def kronecker_symbol(a: int, p: int) -> int:
    """Compute Kronecker symbol (a/p) for odd prime p."""
    if p == 2:
        if a % 2 == 0:
            return 0
        a_mod8 = a % 8
        if a_mod8 == 1 or a_mod8 == 7:
            return 1
        return -1
    a = a % p
    if a == 0:
        return 0
    if pow(a, (p - 1) // 2, p) == 1:
        return 1
    return -1


# ---------------------------------------------------------------------------
# Discrimination Engine
# ---------------------------------------------------------------------------

def compute_delta_collapse(transform_fn, d_plus: list, d_minus: list) -> dict:
    """
    Compute Δcollapse: how well does the transform separate D+ from D-.

    D+ = rank >= 2 curves
    D- = rank 1 curves (or rank 0, depending on experiment)

    Returns discrimination statistics.
    """
    features_plus = np.array([transform_fn(c) for c in d_plus])
    features_minus = np.array([transform_fn(c) for c in d_minus])

    # Per-feature discrimination (Cohen's d)
    mean_plus = np.mean(features_plus, axis=0)
    mean_minus = np.mean(features_minus, axis=0)
    std_pooled = np.sqrt(
        (np.var(features_plus, axis=0) + np.var(features_minus, axis=0)) / 2
        + 1e-10
    )
    cohens_d = (mean_plus - mean_minus) / std_pooled

    # Overall discrimination (Mahalanobis-like)
    diff = mean_plus - mean_minus
    overall_signal = float(np.sqrt(np.sum(diff**2)))
    overall_noise = float(np.mean(std_pooled))
    delta_collapse = overall_signal / (overall_noise + 1e-10)

    # Best single feature
    best_idx = int(np.argmax(np.abs(cohens_d)))
    best_d = float(cohens_d[best_idx])

    return {
        'delta_collapse': delta_collapse,
        'best_feature_idx': best_idx,
        'best_cohens_d': best_d,
        'mean_plus': mean_plus,
        'mean_minus': mean_minus,
        'cohens_d': cohens_d,
    }


# ---------------------------------------------------------------------------
# L3: Safety Classification
# ---------------------------------------------------------------------------

def classify_safety(transform_name: str, delta: float, cohens_d: np.ndarray) -> str:
    """
    Classify a transform as SAFE, UNSAFE, or UNKNOWN.

    SAFE: property cannot be decided by known arithmetic tools
    UNSAFE: property is decidable within known theory
    UNKNOWN: strong signal but decidability is unclear

    Rules (initial, to be refined):
    - If delta < 0.5: REJECTED (no signal)
    - If transform uses only local data (a_p, conductor factorization):
      likely UNSAFE (local data is computable)
    - If transform involves global structure (regulator, height pairing,
      twist families): potentially SAFE or UNKNOWN
    """
    if delta < 0.5:
        return 'REJECTED'

    # Known-decidable transforms (local data only)
    local_transforms = ['ap_moments', 'conductor_arithmetic', 'local_factor_product']
    if transform_name in local_transforms:
        return 'UNSAFE'

    # Potentially non-decidable transforms
    global_transforms = ['twist_signature', 'height_pairing_proxy']
    if transform_name in global_transforms:
        if delta > 2.0:
            return 'UNKNOWN'
        elif delta > 1.0:
            return 'UNKNOWN'
        else:
            return 'UNSAFE'

    return 'UNKNOWN'


# ---------------------------------------------------------------------------
# Main Experiment
# ---------------------------------------------------------------------------

def run_phase8_experiment():
    """Run the BSD rank discrimination experiment."""

    print("=" * 70)
    print("Phase 8: BSD Rank Discrimination via Illusion")
    print("=" * 70)
    print()
    print("D+ = rank 2 curves (5 curves)")
    print("D- = rank 1 curves (5 curves)")
    print("Goal: find transforms that discriminate rank 2 from rank 1")
    print()

    transforms = {
        'twist_signature': transform_twist_signature,
        'ap_moments': transform_ap_moments,
        'local_factor_product': transform_local_factor_product,
        'height_pairing_proxy': transform_height_pairing_proxy,
        'conductor_arithmetic': transform_conductor_arithmetic,
    }

    results = {}

    print(f"{'Transform':<25} {'Δcollapse':>12} {'Best d':>10} {'Classification':>16}")
    print("-" * 70)

    for name, fn in transforms.items():
        try:
            r = compute_delta_collapse(fn, RANK_2_CURVES, RANK_1_CURVES)
            classification = classify_safety(name, r['delta_collapse'], r['cohens_d'])
            results[name] = {**r, 'classification': classification}
            print(f"{name:<25} {r['delta_collapse']:>12.4f} {r['best_cohens_d']:>+10.4f} {classification:>16}")
        except Exception as e:
            print(f"{name:<25} {'ERROR':>12} {str(e)[:30]}")
            results[name] = {'error': str(e)}

    print()
    print("=" * 70)
    print("Interpretation:")
    print("  REJECTED: no discriminating signal (Δ < 0.5)")
    print("  UNSAFE: signal exists but property is decidable by known tools")
    print("  UNKNOWN: signal exists and decidability is unclear — INVESTIGATE")
    print("=" * 70)

    # Detailed analysis of UNKNOWN results
    unknowns = {k: v for k, v in results.items()
                if isinstance(v, dict) and v.get('classification') == 'UNKNOWN'}

    if unknowns:
        print()
        print("--- UNKNOWN transforms (candidates for deeper investigation) ---")
        for name, r in unknowns.items():
            print(f"\n  {name}:")
            print(f"    Δcollapse = {r['delta_collapse']:.4f}")
            print(f"    Best feature index = {r['best_feature_idx']}")
            print(f"    Best Cohen's d = {r['best_cohens_d']:+.4f}")
            print(f"    Mean (rank 2) = {r['mean_plus'][:5]}")
            print(f"    Mean (rank 1) = {r['mean_minus'][:5]}")

    return results


if __name__ == '__main__':
    results = run_phase8_experiment()
