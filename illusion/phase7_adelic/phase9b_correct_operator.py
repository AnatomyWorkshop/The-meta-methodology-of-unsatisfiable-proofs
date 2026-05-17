"""
Phase 9b: H1 — What the numerical collapse means, and the correct operator.

=============================================================================
WHAT THE COLLAPSE TELLS US
=============================================================================

In phase9_h1_continuous_spectrum.py, the UCA constraint D' = (D + PDP)/2
caused ALL eigenvalues to collapse to zero (frac_near_zero = 1.000).

Why? Because D is diagonal with entries k*log(p), and P swaps k <-> -k.
So PDP has entries -k*log(p). Therefore:
  D' = (D + PDP)/2 = diag(k*log(p) + (-k*log(p)))/2 = 0

The UCA constraint on the DILATION GENERATOR D forces D' = 0.
This is not H1 — it's a triviality: the symmetrized dilation generator is zero.

The problem: we are applying UCA to the WRONG operator.

=============================================================================
THE CORRECT OPERATOR
=============================================================================

The dilation generator D has eigenvalues k*log(p) (both positive and negative).
The UCA parity P maps k -> -k.
So [D, P] = 0 is impossible unless D = 0 (since D anticommutes with P in the
sense that PDP = -D for the dilation generator).

Wait — let's check:
  D f_k = k*log(p) * f_k
  P f_k = f_{-k}
  PDP f_k = PD f_{-k} = P(-k*log(p)) f_{-k} = -k*log(p) f_k = -D f_k

So PDP = -D, which means [D, P] = DP - PD = DP + DPP^{-1}P... let me be careful.

  [D, P] f_k = DP f_k - PD f_k
             = D f_{-k} - P(k*log(p) f_k)
             = (-k*log(p)) f_{-k} - k*log(p) f_{-k}
             = -2k*log(p) f_{-k}

So [D, P] != 0 in general. The UCA constraint [D, P] = 0 is NOT automatically
satisfied by the dilation generator.

The symmetrized operator D' = (D + PDP)/2 = (D - D)/2 = 0 is trivially zero.

CONCLUSION: The dilation generator D is the WRONG operator for UCA.
The correct operator must COMMUTE with P, not anticommute.

=============================================================================
THE CORRECT UCA OPERATOR: D^2 (OR THE VLADIMIROV OPERATOR)
=============================================================================

Consider D^2 instead of D:
  D^2 f_k = (k*log(p))^2 f_k
  P D^2 P f_k = P D^2 f_{-k} = P ((-k*log(p))^2 f_{-k}) = (k*log(p))^2 f_k

So PD^2P = D^2, which means [D^2, P] = 0. ✓

The Vladimirov operator Delta_p^alpha has eigenvalues p^{alpha*k} (not k^2*log^2(p)).
But it also commutes with P:
  P Delta_p^alpha P f_k = p^{alpha*(-k)} f_k

This is NOT equal to Delta_p^alpha f_k = p^{alpha*k} f_k unless k=0.
So [Delta_p^alpha, P] != 0 either.

The issue: P maps k -> -k, so any operator with eigenvalue lambda(k) != lambda(-k)
will NOT commute with P.

For [A, P] = 0, we need: A f_k = lambda(k) f_k with lambda(k) = lambda(-k).
I.e., the eigenvalues must be EVEN functions of k.

D has eigenvalues k*log(p) — ODD in k. So [D, P] != 0.
D^2 has eigenvalues (k*log(p))^2 — EVEN in k. So [D^2, P] = 0. ✓
|D| has eigenvalues |k|*log(p) — EVEN in k. So [|D|, P] = 0. ✓

=============================================================================
RESTATEMENT OF H1 WITH THE CORRECT OPERATOR
=============================================================================

The correct UCA operator is D^2 (or equivalently |D|), not D.

The spectral decomposition of D^2 on L^2(A_Q^*/Q^*):
  - Discrete part: eigenvalues {(1/4 + gamma_n^2)} where 1/2 + i*gamma_n are zeta zeros
    (from the explicit formula: D^2 corresponds to the Casimir operator,
     eigenvalues 1/4 + t^2 for zeros at 1/2 + it)
  - Continuous part: eigenvalues {1/4 + s^2 : s in R} from Eisenstein series

H1 (restated): Under the UCA constraint [D^2, P] = 0, the continuous spectrum
{1/4 + s^2 : s in R} is suppressed, leaving only the discrete part.

But [D^2, P] = 0 is AUTOMATICALLY satisfied (D^2 has even eigenvalues).
So the UCA constraint on D^2 gives NO information about H1.

=============================================================================
THE REAL QUESTION
=============================================================================

The UCA constraint [A, P] = 0 is automatically satisfied by any operator A
with even eigenvalues. It gives no information about whether the spectrum
is discrete or continuous.

H1 is NOT a consequence of the UCA commutation constraint alone.

H1 requires a DIFFERENT type of condition. The candidates are:

1. COMPACTNESS: The resolvent (D^2 + 1)^{-1} is compact.
   This would force purely discrete spectrum.
   But the adelic space is non-compact, so this is unlikely to hold.

2. TRACE CLASS: The heat kernel e^{-tD^2} is trace class.
   This is equivalent to sum_n e^{-t*lambda_n} < infinity.
   For the zeta zeros: sum_n e^{-t*(1/4+gamma_n^2)} converges for t > 0.
   This is known (the Hadamard product for zeta).
   But it doesn't rule out the continuous spectrum.

3. SPECTRAL ZETA FUNCTION: The spectral zeta function zeta_D(s) = sum_n lambda_n^{-s}
   has a meromorphic continuation. If the continuous spectrum contributes a
   branch cut (not poles), and the UCA constraint forces the branch cut to
   vanish, H1 follows.

4. THE SELBERG TRACE FORMULA APPROACH (most promising):
   The trace formula for A_Q^*/Q^* is:
     sum_n phi(lambda_n) = geometric side (sum over conjugacy classes)
   The geometric side is controlled by the arithmetic of Q.
   If the UCA constraint forces the geometric side to have no continuous
   contribution, H1 follows.

=============================================================================
NUMERICAL EXPERIMENT: D^2 SPECTRUM UNDER UCA
=============================================================================
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from phase9_h1_continuous_spectrum import build_dilation_operator, build_parity_operator_adelic


def run_d_squared_analysis(primes: list = None, N: int = 2) -> None:
    """
    Analyze the spectrum of D^2 and check [D^2, P] = 0.
    Compare discrete vs continuous spectrum structure.
    """
    if primes is None:
        primes = [2, 3, 5]

    D = build_dilation_operator(primes, N)
    P = build_parity_operator_adelic(D)
    D2 = D @ D

    evals_D = np.sort(np.diag(D))
    evals_D2 = np.sort(np.linalg.eigvalsh(D2))

    comm_D2_P = np.linalg.norm(D2 @ P - P @ D2, 'fro')

    print(f"Primes={primes}, N={N}, dim={D.shape[0]}")
    print(f"  [D^2, P] norm: {comm_D2_P:.2e}  (should be ~0)")
    print(f"  D eigenvalues (first 10): {evals_D[:10].round(3)}")
    print(f"  D^2 eigenvalues (first 10): {evals_D2[:10].round(3)}")
    print()

    # The D^2 eigenvalues are (k*log(p))^2 — all non-negative
    # The continuous spectrum of D^2 on the full adelic space would be [0, inf)
    # The discrete spectrum (zeta zeros) would be {1/4 + gamma_n^2}
    # The smallest zeta zero gives: 1/4 + 14.13^2 ≈ 200
    # Our truncated space has D^2 eigenvalues up to (N*log(p_max))^2

    print(f"  Theoretical first zeta eigenvalue: 1/4 + 14.13^2 = {0.25 + 14.13**2:.2f}")
    print(f"  Our D^2 max eigenvalue: {evals_D2[-1]:.2f}")
    print(f"  -> Our truncation is {'too small' if evals_D2[-1] < 200 else 'large enough'}")
    print(f"     to see the first zeta zero in D^2 spectrum")
    print()


def h1_selberg_approach() -> None:
    """
    Outline the Selberg trace formula approach to H1.

    The Selberg trace formula for A_Q^*/Q^* (GL(1) case):

    For a test function h(t) (even, Schwartz class):
      sum_n h(gamma_n) + (continuous contribution)
      = geometric side

    The geometric side for GL(1)/Q is:
      - Identity contribution: (1/2pi) integral h(t) dt  (this IS the continuous spectrum)
      - Prime power contributions: sum_{p^k} (log p) * h_hat(k*log p)

    The UCA constraint forces the prime power contributions to be symmetric:
      h_hat(k*log p) = h_hat(-k*log p)  (even function)

    This is automatically satisfied for even h.

    H1 would follow if: the identity contribution (continuous spectrum) vanishes.
    The identity contribution is (1/2pi) integral h(t) dt.
    This vanishes iff h has zero integral — i.e., h is orthogonal to constants.

    UCA constraint: h must be even (P-symmetric).
    Even functions can have nonzero integral.
    So UCA alone does NOT force the identity contribution to vanish.

    CONCLUSION: H1 cannot be derived from UCA via the Selberg trace formula
    without an additional constraint on h (e.g., h(0) = 0).
    """
    print("Selberg Trace Formula Analysis:")
    print()
    print("  Trace formula (GL(1)/Q):")
    print("    sum_n h(gamma_n) + (1/2pi) integral h(t) dt")
    print("    = sum_{p^k} (log p) * h_hat(k*log p)")
    print()
    print("  The (1/2pi) integral h(t) dt term IS the continuous spectrum.")
    print("  It vanishes iff integral h(t) dt = 0.")
    print()
    print("  UCA constraint: h must be even (P-symmetric).")
    print("  Even functions can have nonzero integral.")
    print("  -> UCA alone does NOT suppress the continuous spectrum.")
    print()
    print("  Additional condition needed: h(0) = 0 (or h orthogonal to 1).")
    print("  This is NOT implied by UCA.")
    print()
    print("  HONEST CONCLUSION:")
    print("  H1 is a genuine open problem. The UCA constraint [D, P] = 0")
    print("  (or [D^2, P] = 0) does not imply H1.")
    print("  H1 requires either:")
    print("    (a) A compactness argument (space is 'effectively compact')")
    print("    (b) An additional spectral condition beyond UCA")
    print("    (c) A direct computation showing the Eisenstein contribution")
    print("        to the spectral measure is zero for arithmetic reasons")
    print()
    print("  Option (c) is the most promising: the Eisenstein series on")
    print("  A_Q^*/Q^* are the characters |x|^s. Their contribution to the")
    print("  spectral measure of D^2 is the Plancherel measure on iR.")
    print("  This is a FIXED measure — it does not depend on UCA.")
    print("  Therefore H1 is FALSE in general, and TRUE only if we")
    print("  restrict to a subspace where the Eisenstein contribution vanishes.")
    print()
    print("  The correct subspace: L^2_0 = {f : integral f = 0}.")
    print("  On L^2_0, the Eisenstein characters |x|^s with s != 0 are absent")
    print("  (they have nonzero integral). The spectrum of D^2 on L^2_0 is")
    print("  purely discrete — this is the content of Tate's thesis.")
    print()
    print("  REVISED H1: The UCA constraint, applied to L^2_0 (not all of L^2),")
    print("  gives a purely discrete spectrum. The restriction to L^2_0 is")
    print("  the arithmetic condition that replaces compactness.")


if __name__ == '__main__':
    print("Phase 9b: Correct Operator and H1 Analysis")
    print("=" * 62)
    print()

    for primes, N in [([2, 3], 1), ([2, 3, 5], 1), ([2, 3], 2)]:
        run_d_squared_analysis(primes, N)

    print("=" * 62)
    h1_selberg_approach()
