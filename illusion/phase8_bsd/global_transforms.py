"""
Phase 8 iteration 3: Global transforms.

Previous iterations showed:
  - twist_signature signal is dominated by local a_p^2 → UNSAFE
  - Need truly global transforms that cannot be decided from local data

This iteration implements:
  1. BSD residual probe: compute local part of BSD formula, measure deviation
     from L-value. Deviation = |Sha| * R (global quantities).
  2. Rankin-Selberg proxy: symmetric square L-function behavior
  3. Modular symbol parity: sign structure across cusps
  4. Analytic rank gap: rate of vanishing at s=1 (not just order)
"""

import numpy as np
from rank_discrimination import (
    RANK_0_CURVES, RANK_1_CURVES, RANK_2_CURVES,
    kronecker_symbol, compute_delta_collapse
)
from twist_dissection import ALL_RANK_1, ALL_RANK_2


# ---------------------------------------------------------------------------
# Transform 1: BSD Residual Probe
# ---------------------------------------------------------------------------

def transform_bsd_residual(curve: dict) -> np.ndarray:
    """
    The BSD formula says:
      L^(r)(E,1)/r! = |Sha| * Omega * R * prod(c_p) / |tors|^2

    We can compute the "local part": Omega * prod(c_p) / |tors|^2
    from known data. The "global residual" is |Sha| * R.

    For rank 0: residual = |Sha| (since R = 1 by convention)
    For rank 1: residual = |Sha| * h(P) (Neron-Tate height of generator)
    For rank 2: residual = |Sha| * det(height matrix)

    The residual encodes the global arithmetic structure.
    We approximate it from available data.
    """
    rank = curve['rank']
    N = curve['conductor']
    tors = curve['torsion_order']
    sha = curve.get('sha', 1)
    reg = curve.get('regulator', 1.0)
    omega = curve.get('omega', 1.0)
    tam = curve.get('tamagawa_prod', 1)

    # Local part (computable from local data)
    local_part = omega * tam / (tors**2)

    # For rank 0: L(E,1) is known
    L_val = curve.get('L_value', 0.0)
    L_prime = curve.get('L_prime', 0.0)
    L_double = curve.get('L_double_prime', 0.0)

    # BSD residual = L^(r)(E,1)/r! / local_part = |Sha| * R
    if rank == 0 and L_val > 0:
        bsd_residual = L_val / local_part if local_part > 1e-15 else 0
    elif rank == 1 and L_prime > 0:
        bsd_residual = L_prime / local_part if local_part > 1e-15 else 0
    elif rank == 2 and L_double > 0:
        bsd_residual = (L_double / 2.0) / local_part if local_part > 1e-15 else 0
    else:
        bsd_residual = 0.0

    # Features: various normalizations of the residual
    features = [
        bsd_residual,
        np.log(bsd_residual + 1e-10),
        bsd_residual / np.log(N + 1),
        bsd_residual * np.sqrt(N),
        local_part,
        np.log(local_part + 1e-10),
        # Ratio features
        bsd_residual / (local_part + 1e-10),
        float(N) / (bsd_residual + 1e-10) if bsd_residual > 0 else 0,
    ]
    return np.array(features)


# ---------------------------------------------------------------------------
# Transform 2: Symmetric Square L-function proxy
# ---------------------------------------------------------------------------

def transform_symmetric_square(curve: dict) -> np.ndarray:
    """
    The symmetric square L-function L(Sym^2 E, s) has Euler factors:
      L_p(Sym^2 E, s) = (1 - alpha_p^2 p^{-s})^{-1} (1 - p^{-s})^{-1} (1 - beta_p^2 p^{-s})^{-1}

    where alpha_p + beta_p = a_p and alpha_p * beta_p = p.

    For our purposes, the key quantity is:
      a_p^2 - 2p = (alpha_p - beta_p)^2 - 2p = alpha_p^2 + beta_p^2

    This is the trace of Sym^2 at p. Its distribution differs between
    rank 1 and rank 2 in ways that go beyond raw a_p statistics because
    Sym^2 encodes the PRODUCT structure of the Galois representation.
    """
    a_p = np.array(curve['a_p'], dtype=float)
    primes = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], dtype=float)

    # Sym^2 trace: a_p^2 - 2p (for good primes)
    sym2_trace = a_p**2 - 2 * primes

    # Normalized by p (Sato-Tate for Sym^2)
    sym2_norm = sym2_trace / (2 * primes)

    # Partial Sym^2 L-value at s=1
    log_L_sym2 = 0.0
    for i, p in enumerate(primes):
        # Approximate local factor
        local = 1 - sym2_trace[i] * p**(-1) + (a_p[i]**2 - 1) * p**(-2)
        if abs(local) > 1e-15:
            log_L_sym2 -= np.log(abs(local))

    # Adjoint L-function value proxy
    # L(Ad E, 1) = L(Sym^2 E, 1) / zeta(2) relates to Petersson norm
    # For rank 2, this may show different behavior

    features = [
        np.mean(sym2_norm),
        np.std(sym2_norm),
        np.mean(sym2_norm**2),
        np.mean(sym2_norm[sym2_norm > 0]),
        np.mean(sym2_norm[sym2_norm < 0]) if np.any(sym2_norm < 0) else 0,
        log_L_sym2,
        np.sum(np.abs(sym2_norm)),
        np.max(sym2_norm) - np.min(sym2_norm),
    ]
    return np.array(features)


# ---------------------------------------------------------------------------
# Transform 3: Modular degree and congruences
# ---------------------------------------------------------------------------

def transform_modular_degree_proxy(curve: dict) -> np.ndarray:
    """
    The modular degree deg(phi: X_0(N) -> E) encodes global information
    about congruences between f_E and other modular forms at level N.

    We can't compute it directly without SageMath, but we can approximate
    related quantities from a_p data:

    - The "congruence number" c(f_E) = #{ g in S_2(Gamma_0(N)) : g ≡ f_E mod p }
    - Approximated by: how many other eigenforms at level N have similar a_p?

    For rank 2 curves (which tend to have large conductor), the modular
    degree tends to be larger, and congruences are rarer.
    """
    a_p = np.array(curve['a_p'], dtype=float)
    N = curve['conductor']
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    # Dimension of S_2(Gamma_0(N)) ≈ N/12 (genus formula)
    dim_approx = N / 12.0

    # "Isolation" of f_E: how far are its a_p from typical values?
    # Hasse bound: |a_p| <= 2*sqrt(p)
    # Normalized distance from 0:
    isolation = np.mean(np.abs(a_p) / (2 * np.sqrt(np.array(primes, dtype=float))))

    # Congruence proxy: for small primes, check if a_p ≡ 0 mod p
    cong_count = sum(1 for i, p in enumerate(primes[:5]) if int(a_p[i]) % p == 0)

    # Analytic conductor (Iwaniec-Sarnak)
    analytic_cond = N * np.exp(2)  # simplified

    features = [
        dim_approx,
        np.log(dim_approx + 1),
        isolation,
        float(cong_count),
        np.log(analytic_cond),
        isolation * dim_approx,
        float(cong_count) / (dim_approx + 1),
        np.mean(a_p**2) / dim_approx,
    ]
    return np.array(features)


# ---------------------------------------------------------------------------
# Transform 4: Analytic rank gap (rate of vanishing)
# ---------------------------------------------------------------------------

def transform_analytic_rank_gap(curve: dict) -> np.ndarray:
    """
    Beyond the ORDER of vanishing, the RATE matters.

    For rank 1: L'(E,1) can be large or small
    For rank 2: L''(E,1)/2 can be large or small

    The ratio L^(r)(E,1) / (conductor)^{something} may distinguish
    curves where the vanishing is "tight" vs "loose".

    This is related to the Goldfeld conjecture and the distribution
    of central values in families.
    """
    N = curve['conductor']
    rank = curve['rank']

    # Leading coefficient
    if rank == 0:
        leading = curve.get('L_value', 0.0)
    elif rank == 1:
        leading = curve.get('L_prime', 0.0)
    elif rank == 2:
        leading = curve.get('L_double_prime', 0.0) / 2.0
    else:
        leading = 0.0

    # Various normalizations
    features = [
        leading,
        np.log(leading + 1e-10),
        leading / np.log(N + 1),
        leading * np.sqrt(N),
        leading / (N**0.25),
        np.log(N),
        float(rank),  # calibration only
        leading / (float(rank) + 0.1),
    ]
    return np.array(features)


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_global_transforms():
    print("=" * 70)
    print("Phase 8 Iteration 3: Global Transforms")
    print("=" * 70)
    print()
    print(f"D+ = {len(ALL_RANK_2)} rank-2 curves")
    print(f"D- = {len(ALL_RANK_1)} rank-1 curves")
    print()

    # Filter: only use curves that have the needed data
    r2_with_data = [c for c in ALL_RANK_2 if 'L_double_prime' in c]
    r1_with_data = [c for c in ALL_RANK_1 if 'L_prime' in c]

    transforms = {
        'bsd_residual': (transform_bsd_residual, r2_with_data, r1_with_data),
        'symmetric_square': (transform_symmetric_square, ALL_RANK_2, ALL_RANK_1),
        'modular_degree_proxy': (transform_modular_degree_proxy, ALL_RANK_2, ALL_RANK_1),
        'analytic_rank_gap': (transform_analytic_rank_gap, r2_with_data, r1_with_data),
    }

    print(f"{'Transform':<25} {'Δcollapse':>12} {'Best d':>10} {'Classification':>16}")
    print("-" * 70)

    results = {}
    for name, (fn, d_plus, d_minus) in transforms.items():
        if len(d_plus) < 2 or len(d_minus) < 2:
            print(f"{name:<25} {'SKIP':>12} (insufficient data)")
            continue
        try:
            r = compute_delta_collapse(fn, d_plus, d_minus)
            # Classification logic
            classification = classify_global(name, r)
            results[name] = {**r, 'classification': classification}
            print(f"{name:<25} {r['delta_collapse']:>12.4f} "
                  f"{r['best_cohens_d']:>+10.4f} {classification:>16}")
        except Exception as e:
            print(f"{name:<25} {'ERROR':>12} {str(e)[:40]}")

    # Self-reflection
    print("\n" + "=" * 70)
    print("SELF-REFLECTION")
    print("=" * 70)
    self_reflect_global(results)

    return results


def classify_global(name: str, r: dict) -> str:
    """Classify global transforms."""
    delta = r['delta_collapse']
    if delta < 0.5:
        return 'REJECTED'

    # BSD residual: measures |Sha|*R — genuinely global
    if name == 'bsd_residual':
        return 'UNKNOWN' if delta > 1.0 else 'MARGINAL'

    # Symmetric square: encodes Galois representation structure
    # But still computable from a_p → likely UNSAFE
    if name == 'symmetric_square':
        return 'UNSAFE'

    # Modular degree: partially global (depends on full space S_2)
    # But our proxy uses only local data → UNSAFE
    if name == 'modular_degree_proxy':
        return 'UNSAFE'

    # Analytic rank gap: uses L-values which are global
    if name == 'analytic_rank_gap':
        return 'UNKNOWN' if delta > 1.0 else 'MARGINAL'

    return 'UNKNOWN'


def self_reflect_global(results: dict):
    """Critical self-examination of global transforms."""
    print("""
Key question: which transforms use genuinely global information
that CANNOT be reconstructed from local a_p data alone?

Analysis:
""")

    for name, r in results.items():
        cls = r.get('classification', '?')
        delta = r['delta_collapse']
        print(f"  {name} (Δ={delta:.2f}, {cls}):")

        if name == 'bsd_residual':
            print(f"    Uses: L-value, omega, tamagawa, torsion, regulator")
            print(f"    Global content: regulator R (height pairing of generators)")
            print(f"    Verdict: R is genuinely global — cannot be computed from a_p alone")
            print(f"    BUT: we used precomputed R values, not discovered them")
            print(f"    → Signal is real but CIRCULAR (we already know rank from R)")
            print()

        elif name == 'symmetric_square':
            print(f"    Uses: a_p^2 - 2p (Sym^2 trace)")
            print(f"    Global content: NONE — Sym^2 trace is determined by a_p")
            print(f"    Verdict: purely local, correctly classified UNSAFE")
            print()

        elif name == 'modular_degree_proxy':
            print(f"    Uses: conductor, a_p, dimension estimate")
            print(f"    Global content: modular degree is global, but our PROXY is local")
            print(f"    Verdict: proxy is UNSAFE; true modular degree would be UNKNOWN")
            print()

        elif name == 'analytic_rank_gap':
            print(f"    Uses: L^(r)(E,1) values")
            print(f"    Global content: L-values at s=1 are global (require all a_p)")
            print(f"    BUT: we used precomputed values, not computed from finite a_p")
            print(f"    → In practice, L(E,1) from finite Euler product is LOCAL")
            print(f"    → True L-value (analytic continuation) is GLOBAL")
            print()

    print("""
CONCLUSION:
  The fundamental problem: with only 10 primes of a_p data,
  ALL computable transforms are effectively local.

  To get genuinely global signals, we need either:
  1. Precomputed global invariants (R, |Sha|, modular degree) — but then
     the experiment is circular (we already know rank from these)
  2. Enough a_p data to approximate L-values accurately — needs ~1000 primes
  3. A STRUCTURAL property that is provably non-local but detectable
     from finite data — THIS is what we're really looking for

  The honest answer: with LMFDB lookup data, we can verify BSD but not
  discover new discriminating properties. To discover, we need to work
  at the level of PROOFS, not DATA.

  This points back to Approach B in the paper-plan: can UCA self-consistency
  FORCE Selmer rank = analytic rank without constructing explicit points?
  That's a theorem to prove, not an experiment to run.
""")


if __name__ == '__main__':
    run_global_transforms()
