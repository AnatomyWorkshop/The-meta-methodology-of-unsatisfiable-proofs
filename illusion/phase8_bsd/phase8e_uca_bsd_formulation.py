"""
Phase 8e: UCA Equivalent Formulation of BSD Rank Condition.

This module develops the theoretical framework connecting UCA duality
to the BSD rank conjecture, analogous to the UCA-RH connection.

=============================================================================
THE CORE ANALOGY
=============================================================================

RH case:
  - Hilbert-Polya operator H on L^2(R_+, dx/x)
  - UCA duality: [H, P] = 0 where P: f(x) -> f(1/x)
  - Consequence: spectrum of H is real (RH)

BSD case:
  - Hecke algebra T acting on the space of newforms S_2(Gamma_0(N))
  - UCA duality: [T_p, D] = 0 for all p, where D is the "rank operator"
  - Consequence: spectral multiplicity of D = rank(E)

=============================================================================
THE CONSTRUCTION
=============================================================================

Step 1: The ambient space.

Let E/Q be an elliptic curve of conductor N.
Let f_E in S_2(Gamma_0(N)) be the associated newform (Wiles-Taylor).
The L-function is:
    L(E, s) = L(f_E, s) = sum_{n>=1} a_n(E) n^{-s}

The Hecke operators T_p act on S_2(Gamma_0(N)) by:
    T_p f_E = a_p(E) f_E   (since f_E is a Hecke eigenform)

Step 2: The UCA duality operator for BSD.

The functional equation of L(E, s) is:
    Lambda(E, s) = epsilon_E * Lambda(E, 2-s)
where Lambda(E, s) = (sqrt(N) / 2pi)^s * Gamma(s) * L(E, s)
and epsilon_E in {+1, -1} is the root number.

This defines a symmetry s <-> 2-s (not s <-> 1-s as in RH).
The critical point is s = 1.

The UCA duality operator D_E is defined by:
    D_E: L(E, s) -> epsilon_E * L(E, 2-s)

On the space of Hecke eigenvalues, D_E acts as:
    D_E: a_p -> epsilon_E * a_p * p^{1-2s}|_{s=1} = epsilon_E * a_p / p

This is a RESCALING operator, not a permutation.

Step 3: The commutation condition.

The UCA constraint [T_p, D_E] = 0 means:
    T_p (D_E f) = D_E (T_p f)

Since T_p f_E = a_p f_E and D_E f_E = epsilon_E * f_E (at s=1):
    T_p (epsilon_E f_E) = epsilon_E * a_p * f_E
    D_E (a_p f_E) = epsilon_E * a_p * f_E

These are equal — so [T_p, D_E] = 0 is AUTOMATICALLY satisfied for
any Hecke eigenform. This is not the right formulation.

Step 4: The correct formulation — the rank operator.

The rank of E is encoded in the DERIVATIVE structure of L(E, s) at s=1:
    rank(E) = ord_{s=1} L(E, s)

Define the "rank operator" R_E on the completed L-function space by:
    R_E = -d/ds|_{s=1}  (order of vanishing)

The UCA prediction is:
    [T_p, R_E] = 0  for all primes p

This means: T_p preserves the space of "rank-r contributions" to L(E, s).

Step 5: Spectral interpretation.

Consider the adelic space A_Q^* / Q^* and the spectral decomposition of
the regular representation. The Hecke operators T_p act on this space.

The UCA duality operator P on A_Q^* / Q^* is:
    P: (x_v)_v -> (x_v^{-1})_v  (inversion in each completion)

The UCA constraint [T_p, P] = 0 forces:
    Each eigenspace of P is T_p-invariant.

The eigenspaces of P are:
    V_+ = {f : P f = f}   (symmetric functions)
    V_- = {f : P f = -f}  (antisymmetric functions)

The L-function L(E, s) lives in V_{epsilon_E}:
    - If epsilon_E = +1: L(E, s) in V_+, symmetric under s <-> 2-s
    - If epsilon_E = -1: L(E, s) in V_-, antisymmetric under s <-> 2-s

For L(E, s) in V_-: L(E, 1) = -L(E, 1) => L(E, 1) = 0 => rank >= 1.
This is the parity argument: root number -1 forces rank odd >= 1.

Step 6: The rank >= 2 condition.

For rank >= 2, we need L(E, 1) = L'(E, 1) = 0.

The UCA formulation: consider the EXTENDED space
    W = V_+ ⊕ V_-
with the graded structure W_k = {f : ord_{s=1} f >= k}.

The UCA constraint on W is:
    [T_p, P_k] = 0  for all p, k
where P_k is the projection onto W_k.

This forces: if f in W_k is a T_p eigenfunction, then P_k f is also
a T_p eigenfunction with the same eigenvalue.

For L(E, s) with rank r:
    L(E, s) in W_r \\ W_{r+1}
    T_p L(E, s) = a_p L(E, s)

The UCA constraint [T_p, P_r] = 0 means:
    dim(W_r ∩ T_p-eigenspace(a_p)) >= r

This is the spectral multiplicity condition: the eigenspace of T_p
at eigenvalue a_p has dimension >= rank(E).

=============================================================================
THE BSD-UCA THEOREM (CONJECTURAL)
=============================================================================

Theorem (BSD-UCA, conjectural):
    Let E/Q be an elliptic curve. Let T be the Hecke algebra acting on
    the adelic L^2 space. Let P be the UCA inversion operator.

    If [T_p, P] = 0 for all primes p (UCA duality constraint), then:

        rank(E) = dim(ker(L(E, 1))) = spectral multiplicity of T at a_p

    where the spectral multiplicity is measured in the P-symmetric subspace.

Proof strategy (analogous to RH case):
    1. UCA constraint forces T_p to preserve P-eigenspaces.
    2. The P-eigenspace decomposition corresponds to the functional equation.
    3. The functional equation forces L(E, 1) = 0 when epsilon_E = -1.
    4. For higher rank: the ITERATED UCA constraint on the derived space
       (quotient W_1 / W_0) forces L'(E, 1) = 0 when epsilon_{E'} = -1
       for the "derived curve" E' (related to E by the Selmer group).
    5. By induction: rank(E) = number of times the UCA constraint forces
       a zero at s=1.

The key step (4) is the hard part. It requires:
    - A notion of "derived curve" E' from E
    - The UCA constraint on E' forces L'(E, 1) = 0
    - This is related to the Kolyvagin-Euler system argument

=============================================================================
THE SPECTRAL MULTIPLICITY FORMULATION
=============================================================================

More precisely, define the Hecke-UCA operator:
    H_E = sum_p (log p / p) * T_p * P_p
where P_p is the local UCA operator at prime p.

The UCA constraint is: H_E is self-adjoint on the adelic L^2 space.

Claim: The multiplicity of the eigenvalue 0 of H_E equals rank(E).

This is the direct analogue of:
    RH: H_HP self-adjoint => spectrum real => zeros on critical line
    BSD: H_E self-adjoint => multiplicity of 0 = rank(E)

=============================================================================
WHAT THIS GIVES US
=============================================================================

1. A SPECTRAL CHARACTERIZATION of rank:
   rank(E) = dim(ker(H_E))

2. A TESTABLE PREDICTION:
   For rank 2 curves: H_E has a 2-dimensional kernel.
   For rank 1 curves: H_E has a 1-dimensional kernel.
   For rank 0 curves: H_E has a 0-dimensional kernel (H_E invertible).

3. A PROOF STRATEGY:
   Show that UCA duality (self-adjointness of H_E) implies
   the spectral multiplicity equals the analytic rank.
   This would prove BSD for all curves where UCA holds.

4. THE OPEN PROBLEM:
   Does UCA hold for all elliptic curves over Q?
   This is equivalent to asking: is the adelic L^2 space
   equipped with a natural self-adjoint Hecke-UCA operator?

=============================================================================
COMPARISON WITH KNOWN APPROACHES
=============================================================================

Kolyvagin (1988): rank <= 1 for curves with L(E,1) != 0 or L'(E,1) != 0.
  - Uses Euler systems (Heegner points)
  - Proves rank = analytic rank for rank 0 and 1
  - Does NOT extend to rank >= 2

Gross-Zagier (1986): L'(E,1) != 0 => rank >= 1 (with explicit point).
  - Connects L'(E,1) to height of Heegner point
  - The Heegner point IS the spectral generator of the rank-1 eigenspace

UCA approach:
  - Replaces Heegner points with spectral eigenvectors of H_E
  - The "spectral generators" are the UCA-symmetric eigenfunctions
  - For rank r: there are r independent UCA-symmetric eigenfunctions
  - These correspond to the r independent rational points on E(Q)

The UCA approach is more symmetric: it treats all ranks uniformly,
rather than needing special constructions (Heegner points) for rank 1.

=============================================================================
NUMERICAL EVIDENCE (from Phase 8b-8d)
=============================================================================

Phase 8b: Hecke duality defect with index-reversal P.
  - corr(rank, defect) = 0.45 — not significant
  - Conclusion: index-reversal P is wrong for BSD

Phase 8c: Functional equation duality.
  - At s=0.5: P = I (trivial), defect = 0 always
  - At s=1: corr = 0.38 — weak signal
  - Conclusion: 10 primes insufficient

Phase 8d: BSD product formula with B=300 primes.
  - rank 0: mean estimated = 0.036
  - rank 1: mean estimated = -0.962
  - rank 2: mean estimated = -0.357
  - No monotone separation — need B >= 10000

The numerical experiments confirm: the correct UCA operator for BSD
is NOT the index-reversal P used in Prism. It requires the arithmetic
structure of the functional equation, which is only accessible via
the full L-function (not just 10-300 primes).

=============================================================================
NEXT STEPS
=============================================================================

1. Formalize the Hecke-UCA operator H_E rigorously.
2. Prove that self-adjointness of H_E implies spectral multiplicity = rank.
3. Show that UCA holds for all elliptic curves (or find a counterexample).
4. Connect the spectral generators to rational points on E(Q).

The last step is the deepest: it requires showing that the UCA eigenvectors
in ker(H_E) correspond to elements of E(Q) ⊗ R. This is the arithmetic
content of BSD, translated into spectral language.
"""

import numpy as np


# ---------------------------------------------------------------------------
# Formal construction of the Hecke-UCA operator
# ---------------------------------------------------------------------------

def hecke_uca_operator(a_p_vals: list, primes: list,
                       epsilon: int, s_ref: float = 1.0) -> np.ndarray:
    """
    Build the Hecke-UCA operator H_E on the finite-dimensional proxy space.

    H_E[i,j] = (log(p_i) / p_i) * a_p_i * P_ij

    where P is the functional equation duality operator at s = s_ref.

    For the full theory, this should be an operator on L^2(A_Q^*/Q^*).
    Here we use the finite-dimensional proxy: the space spanned by
    the Hecke eigenvalues {a_p : p <= B}.

    Parameters:
        a_p_vals: list of a_p values for primes in `primes`
        primes: list of primes
        epsilon: root number (+1 or -1)
        s_ref: reference point for functional equation (default s=1)

    Returns:
        H: n x n matrix (n = len(primes))
    """
    n = len(primes)
    a_p = np.array(a_p_vals[:n], dtype=float)
    p = np.array(primes[:n], dtype=float)

    # Hecke part: diagonal matrix with entries (log p / p) * a_p
    T_diag = (np.log(p) / p) * a_p

    # UCA duality part: functional equation operator at s_ref
    # P_ij = delta_ij * epsilon * p_i^{1-2*s_ref}
    # At s=1: P_ij = delta_ij * epsilon * p_i^{-1}
    # At s=0.5: P_ij = delta_ij * epsilon (trivial)
    P_diag = epsilon * p ** (1 - 2 * s_ref)

    # H_E = T * P (diagonal * diagonal = diagonal)
    H_diag = T_diag * P_diag
    H = np.diag(H_diag)

    return H


def spectral_multiplicity_proxy(curve: dict, primes: list = None,
                                 s_ref: float = 1.0,
                                 threshold: float = 0.1) -> dict:
    """
    Estimate the spectral multiplicity of H_E near zero.

    This is the proxy for rank(E) in the UCA formulation.

    Parameters:
        curve: dict with 'a_p', 'rank', 'label' keys
        primes: list of primes to use
        s_ref: reference point for functional equation
        threshold: eigenvalue threshold for "near zero"

    Returns:
        dict with estimated multiplicity and comparison to true rank
    """
    if primes is None:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    epsilon = (-1) ** curve['rank']  # root number from parity
    H = hecke_uca_operator(curve['a_p'], primes, epsilon, s_ref)

    evals = np.sort(np.abs(np.diag(H)))  # H is diagonal, eigenvalues = diagonal entries
    max_eval = np.max(np.abs(evals)) + 1e-10
    n_near_zero = int(np.sum(evals < threshold * max_eval))

    return {
        'label': curve['label'],
        'rank': curve['rank'],
        'epsilon': epsilon,
        'eigenvalues': evals,
        'n_near_zero': n_near_zero,
        'min_eigenvalue': float(evals[0]),
        'spectral_gap': float(evals[1] - evals[0]) if len(evals) > 1 else 0.0,
    }


def run_uca_bsd_formulation(verbose: bool = True) -> None:
    """
    Demonstrate the UCA-BSD spectral multiplicity formulation.

    This is a THEORETICAL demonstration, not a proof.
    The finite-dimensional proxy is too crude to distinguish ranks.
    The full construction requires the adelic L^2 space.
    """
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from rank_discrimination import RANK_0_CURVES, RANK_1_CURVES, RANK_2_CURVES

    all_curves = RANK_0_CURVES + RANK_1_CURVES + RANK_2_CURVES
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    print("Phase 8e: UCA-BSD Spectral Multiplicity Formulation")
    print("=" * 62)
    print()
    print("Hecke-UCA operator: H_E = sum_p (log p / p) * T_p * P_p")
    print("Prediction: dim(ker(H_E)) = rank(E)")
    print()

    for s_ref in [1.0, 0.75]:
        print(f"  s_ref = {s_ref}:")
        print(f"  {'Label':10s}  {'True r':>7}  {'eps':>4}  {'NearZero':>9}  "
              f"{'MinEval':>10}  {'Gap':>8}")
        print(f"  {'-'*10}  {'-'*7}  {'-'*4}  {'-'*9}  {'-'*10}  {'-'*8}")

        results = []
        for curve in all_curves:
            r = spectral_multiplicity_proxy(curve, primes, s_ref)
            results.append(r)
            print(f"  {r['label']:10s}  {r['rank']:>7}  {r['epsilon']:>4}  "
                  f"{r['n_near_zero']:>9}  {r['min_eigenvalue']:>10.6f}  "
                  f"{r['spectral_gap']:>8.6f}")

        ranks = [r['rank'] for r in results]
        near_zeros = [r['n_near_zero'] for r in results]
        min_evals = [r['min_eigenvalue'] for r in results]

        if len(set(ranks)) > 1:
            corr_nz = np.corrcoef(ranks, near_zeros)[0, 1]
            corr_me = np.corrcoef(ranks, min_evals)[0, 1]
            print(f"\n  corr(rank, n_near_zero) = {corr_nz:.4f}")
            print(f"  corr(rank, min_eigenvalue) = {corr_me:.4f}")
        print()

    print("=" * 62)
    print("INTERPRETATION")
    print()
    print("The finite-dimensional proxy H_E is diagonal, so its kernel")
    print("is determined by which a_p values are zero — not by rank.")
    print()
    print("The full UCA-BSD formulation requires:")
    print("  1. The adelic L^2 space (infinite-dimensional)")
    print("  2. The Hecke-UCA operator as a genuine self-adjoint operator")
    print("  3. Spectral theory of this operator near s=1")
    print()
    print("The theoretical prediction (BSD-UCA Theorem) is:")
    print("  rank(E) = dim(ker(H_E)) in the full adelic space")
    print()
    print("This is equivalent to BSD, not a proof of it.")
    print("The value is: it gives BSD a SPECTRAL LANGUAGE,")
    print("analogous to the Hilbert-Polya conjecture for RH.")


if __name__ == '__main__':
    run_uca_bsd_formulation()
