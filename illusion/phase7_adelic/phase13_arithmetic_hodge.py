"""
Phase 13: The Arithmetic Hodge Index Theorem -- Why Faltings Is Not Enough.

=============================================================================
THE QUESTION
=============================================================================

Weil's proof of RH for function fields uses the Hodge Index Theorem on CxC.
Faltings (1984) proved an arithmetic Hodge Index Theorem in Arakelov geometry.

Why is Faltings' theorem not enough to prove RH for number fields?
What is the precise gap?

=============================================================================
WEIL'S HODGE INDEX THEOREM (function field case)
=============================================================================

Setting: C = smooth projective curve over F_q, genus g.
Surface: S = C x C (product surface over F_q).

The Neron-Severi group NS(S) (divisors modulo algebraic equivalence, tensored
with R) has an intersection form (., .) of signature (1, rho-1) where rho is
the Picard number.

The Hodge Index Theorem on S says:
  For any divisor D on S with D . H = 0 (H = ample divisor):
    D . D <= 0
  with equality iff D is numerically trivial.

Weil's application:
  Let Gamma_f = graph of Frobenius f: C -> C (a correspondence on CxC).
  Let Delta = diagonal in CxC.
  Let p1, p2 = projections CxC -> C.

  The "degree" of Gamma_f is:
    deg(Gamma_f) = Gamma_f . Delta = |C(F_q)| = number of fixed points of f

  The Hodge Index Theorem applied to D = Gamma_f - (q+1)/2 * Delta gives:
    (Gamma_f - (q+1)/2 * Delta)^2 <= 0

  Expanding:
    Gamma_f^2 - (q+1) * Gamma_f.Delta + (q+1)^2/4 * Delta^2 <= 0

  Using:
    Gamma_f^2 = 2g - 2 + q(2g-2) = (q+1)(2g-2)  [by Riemann-Roch]
    Delta^2 = 2 - 2g  [self-intersection of diagonal]
    Gamma_f.Delta = |C(F_q)|

  This gives:
    (q+1)(2g-2) - (q+1)|C(F_q)| + (q+1)^2/4 * (2-2g) <= 0

  Simplifying:
    |C(F_q)| >= (q+1) - 2g*sqrt(q)  [Weil bound, lower bound]

  The upper bound comes from applying the same to f^{-1}:
    |C(F_q)| <= (q+1) + 2g*sqrt(q)

  This is the Weil bound: ||C(F_q)| - (q+1)| <= 2g*sqrt(q).

  The Weil bound is EQUIVALENT to RH for C (all |alpha_i| = sqrt(q)).

=============================================================================
THE KEY INGREDIENT: AMPLENESS OF THE DIAGONAL
=============================================================================

The Hodge Index Theorem requires an AMPLE divisor H.
Weil uses H = p1*(point) + p2*(point) (a "polarization" of CxC).

The diagonal Delta is NOT ample in general, but it has positive
self-intersection relative to H:
  Delta . H = 2  (degree of diagonal as a curve)

The AMPLENESS of H is what makes the Hodge Index Theorem work.
H is ample because it comes from a projective embedding of C.

In the number field case:
  - There is no projective embedding of Spec(Z)
  - Spec(Z) is affine, so there is no ample divisor in the usual sense
  - This is the fundamental obstruction

=============================================================================
ARAKELOV GEOMETRY: THE COMPACTIFICATION
=============================================================================

Arakelov (1974) compactified Spec(Z) by adding a "fiber at infinity":
  Spec(Z)_Ar = Spec(Z) union {archimedean place}

The archimedean place corresponds to the embedding Z -> R -> C.
At this place, the "fiber" is the Riemann sphere P^1(C) (or just R for real).

An Arakelov divisor on Spec(Z)_Ar is:
  D = sum_p n_p * [p] + r * [inf]
where n_p are integers (finite part) and r is a real number (infinite part).

The intersection pairing on Arakelov divisors:
  (D1, D2)_Ar = sum_p (D1, D2)_p + (D1, D2)_inf

where (D1, D2)_inf involves the Green's function at the archimedean place.

=============================================================================
FALTINGS' ARITHMETIC HODGE INDEX THEOREM (1984)
=============================================================================

Setting: X = arithmetic surface (proper flat scheme over Spec(Z), relative dim 1)
         with generic fiber X_Q = smooth projective curve over Q.

Faltings proved:
  For any Arakelov divisor D on X with D . H_Ar = 0 (H_Ar = arithmetic ample):
    (D, D)_Ar <= 0

This is the arithmetic analogue of the Hodge Index Theorem.

Faltings used this to prove the Mordell conjecture (Faltings' theorem):
  A curve of genus >= 2 over Q has only finitely many rational points.

=============================================================================
WHY FALTINGS IS NOT ENOUGH FOR RH
=============================================================================

The gap between Faltings and Weil is PRECISE and STRUCTURAL.

In Weil's proof:
  - The surface is CxC (product of the SAME curve with itself)
  - The Frobenius correspondence Gamma_f is a SPECIFIC divisor on CxC
  - The Hodge Index Theorem gives an inequality on Gamma_f . Delta
  - This inequality is EQUIVALENT to the Weil bound (= RH for C)

In Faltings' theorem:
  - The arithmetic surface X is a single curve over Z (not a product)
  - There is no "Frobenius correspondence" in the number field case
  - The Hodge Index Theorem gives inequalities on divisors of X
  - These inequalities are used for Mordell, NOT for RH

The structural gap:
  Weil needs: Hodge Index Theorem on CxC (a PRODUCT surface)
  Faltings has: Hodge Index Theorem on X (a SINGLE arithmetic surface)

To apply Faltings to RH, we would need:
  - An arithmetic surface X = Spec(Z) x_{F_1} Spec(Z) (the "arithmetic CxC")
  - A "Frobenius correspondence" on this product
  - A Hodge Index Theorem on this product

None of these exist in the current mathematical literature.

=============================================================================
THE CONNES-CONSANI ARITHMETIC SITE (2014)
=============================================================================

Connes and Consani constructed the "arithmetic site":
  - Objects: pairs (Spec(Z), Frobenius-like endomorphisms)
  - The "absolute point" Spec(F_1) plays the role of the base field
  - Spec(Z) x_{F_1} Spec(Z) is defined as a topos (not a scheme)

Their construction gives:
  - A "scaling site" that plays the role of CxC
  - A "Frobenius" action on this site
  - A formal analogue of the Weil explicit formula

What they DO NOT have:
  - A concrete intersection form on Spec(Z) x_{F_1} Spec(Z)
  - A Hodge Index Theorem for this intersection form
  - A proof that the intersection form is positive (= RH)

Their work is a FRAMEWORK, not a proof. The positivity question remains open.

=============================================================================
THE PRECISE GAP IN OPERATOR LANGUAGE
=============================================================================

In our UCA framework:
  - {D, P} = 0 is the algebraic skeleton (= functional equation)
  - K = Weil operator (K >= 0 iff RH)
  - K = K_+ + K_- (block diagonal from {D,P}=0)

The Hodge Index Theorem in function field case gives:
  K_+ >= 0  from: Hodge form on EVEN correspondences (symmetric under swap)
  K_- >= 0  from: Hodge form on ODD correspondences (anti-symmetric)

The proof of K_+ >= 0 uses:
  - Riemann-Roch on CxC (gives the self-intersection numbers)
  - Ampleness of H = p1*(pt) + p2*(pt) (gives the positivity)

The proof of K_- >= 0 uses:
  - The same, applied to the anti-symmetric part

In the number field case:
  - We have the algebraic structure ({D,P}=0, K = K_+ + K_-)
  - We do NOT have the geometric input (ampleness, Riemann-Roch on "ZxZ")

=============================================================================
A NEW ANGLE: CAN {D,P}=0 REPLACE AMPLENESS?
=============================================================================

Here is the key question:

In the function field case, ampleness of H is used to prove:
  For any divisor D with D.H = 0: D.D <= 0

In operator language, this is:
  For any f in H with <f, Kf> = 0 (K = "intersection with H"): <f, Kf> <= 0

Wait -- this is circular. Let me restate.

The Hodge Index Theorem says:
  The intersection form (., .) on NS(CxC) has signature (1, rho-1).
  The positive direction is spanned by H.

In operator language:
  K has exactly ONE positive eigenvalue direction (the "H direction").
  All other directions are negative.

But we want K >= 0 (all eigenvalues non-negative)!

WAIT. I have the sign wrong. Let me recheck.

=============================================================================
CORRECTING THE SIGN: WEIL POSITIVITY vs HODGE INDEX
=============================================================================

The Weil distribution W(f) = <f, K f> satisfies:
  W(f * f_bar) >= 0 for all f  iff  RH

This means K >= 0 (positive semi-definite).

The Hodge Index Theorem says the intersection form has signature (1, rho-1),
meaning it has ONE positive direction and many negative directions.

These seem contradictory. Let me resolve this.

The resolution: the Weil distribution W is NOT the intersection form on NS(CxC).
It is a DIFFERENT bilinear form, constructed from the intersection form by:
  W(f) = (Gamma_f, Delta)  [intersection of the f-correspondence with diagonal]

The positivity W(f * f_bar) >= 0 is equivalent to:
  (Gamma_f, Gamma_{f_bar}) >= 0  [Cauchy-Schwarz type inequality]

This follows from the Hodge Index Theorem by:
  (Gamma_f, Gamma_{f_bar})^2 >= (Gamma_f, Gamma_f) * (Gamma_{f_bar}, Gamma_{f_bar})

Wait, that's Cauchy-Schwarz in the WRONG direction for a negative definite form.

Let me look at this more carefully.

=============================================================================
THE CORRECT STATEMENT: WEIL'S POSITIVITY CRITERION
=============================================================================

Weil (1952) showed: RH for all L-functions with Grossencharacter iff
  W(f * f_bar) >= 0 for all Schwartz functions f

where W is the Weil distribution:
  W(f) = sum_p sum_k (log p / p^{k/2}) * (f_hat(k*log p) + f_hat(-k*log p))
        - f(0) * log(pi) - integral f(t) * Re(Gamma'/Gamma(1/4 + it/2)) dt

This is a distribution on R (or on C_Q in the adelic language).

The connection to the Hodge Index Theorem:
  In the function field case, W(f * f_bar) >= 0 follows from:
    sum_n |C(F_{q^n})| * f_hat(n*log q)^2 >= 0  [trivially true]
  combined with the Weil bound |C(F_{q^n})| <= (q^{n/2} + 1)^{2g}.

  The Weil bound comes from the Hodge Index Theorem.
  So: Hodge Index Theorem => Weil bound => W(f*f_bar) >= 0 => RH.

In the number field case:
  W(f * f_bar) >= 0 is EQUIVALENT to RH (Weil 1952).
  But there is no "Weil bound" to use as an intermediate step.
  The Hodge Index Theorem analogue (if it existed) would give the Weil bound.

=============================================================================
WHAT WE ACTUALLY NEED
=============================================================================

The precise missing ingredient is:

  An "arithmetic Weil bound":
    |sum_n a_n * f_hat(n)| <= C * ||f||  for some constant C

  where a_n are the coefficients of the L-function (related to |C(F_{q^n})|
  in the function field case, but for the Riemann zeta function).

  For the Riemann zeta function:
    a_n = Lambda(n) = log p if n = p^k, 0 otherwise (von Mangoldt function)

  The "Weil bound" for zeta would be:
    |sum_{n<=X} Lambda(n) - X| <= C * X^{1/2} * log^2(X)

  This IS the prime number theorem with error term, which is EQUIVALENT to RH.

So the circle closes: the "arithmetic Weil bound" = PNT with RH error term = RH.

=============================================================================
THE HONEST CONCLUSION
=============================================================================

The function field analogy is COMPLETE and PRECISE:

  Function field:
    Hodge Index Theorem on CxC
    => Weil bound: ||C(F_{q^n})| - (q^n+1)| <= 2g * q^{n/2}
    => RH for C

  Number field:
    ??? (missing: arithmetic Hodge Index Theorem on "ZxZ")
    => ??? (missing: arithmetic Weil bound = PNT with RH error)
    => RH for zeta

The UCA framework ({D,P}=0, K = K_+ + K_-) gives the ALGEBRAIC STRUCTURE
of the proof, but not the GEOMETRIC INPUT (ampleness, Riemann-Roch on "ZxZ").

The H_+/H_- decomposition is the correct decomposition, but proving
K_+ >= 0 and K_- >= 0 separately requires the same missing geometric input.

=============================================================================
IS THERE A PURELY ALGEBRAIC PROOF?
=============================================================================

Could {D,P}=0 alone, without geometric input, prove K >= 0?

Answer: NO, for a fundamental reason.

{D,P}=0 is a SYMMETRY condition. It says K = K_+ + K_-.
Symmetry conditions never imply positivity by themselves.

Example: The operator K = diag(1, -1) satisfies [K, P] = 0 where P = diag(1,-1).
K is block diagonal but NOT positive definite.

The positivity of K requires ADDITIONAL INPUT beyond the symmetry.
In the function field case, this input is the ampleness of H (a geometric fact).
In the number field case, this input is unknown.

=============================================================================
WHAT THIS MEANS FOR OUR WORK
=============================================================================

Our UCA framework has:
  1. Correctly identified the algebraic structure ({D,P}=0)
  2. Correctly identified the decomposition (K = K_+ + K_-)
  3. Correctly identified the gap (need K_+ >= 0 and K_- >= 0)
  4. Correctly identified the analogy (function field Hodge Index Theorem)

What we have NOT done (and cannot do with current tools):
  5. Provide the geometric input that makes K_+ >= 0 and K_- >= 0

The honest assessment:
  Our work is a PRECISE FORMULATION of the gap, not a proof.
  The gap is: arithmetic ampleness on "Spec(Z) x Spec(Z)".
  This is the same gap that Connes, Deninger, and others have identified.
  Our contribution: the H_+/H_- decomposition is the CORRECT decomposition
  of this gap, forced by the symmetry {D,P}=0.
"""

import numpy as np


def weil_bound_function_field(q: int, g: int, n: int) -> tuple:
    """
    Compute the Weil bound for |C(F_{q^n})| for a curve of genus g over F_q.

    Weil bound: ||C(F_{q^n})| - (q^n + 1)| <= 2g * q^{n/2}

    This is equivalent to RH for C (all |alpha_i| = q^{1/2}).
    """
    center = q**n + 1
    bound = 2 * g * q**(n / 2)
    return center, bound


def prime_counting_rh_bound(x: float) -> tuple:
    """
    The number field analogue of the Weil bound.

    RH implies: |pi(x) - li(x)| <= C * sqrt(x) * log(x)

    where pi(x) = number of primes <= x
    and li(x) = integral_2^x dt/log(t) (logarithmic integral).

    This is the "arithmetic Weil bound" -- equivalent to RH.
    """
    import math
    # Approximate li(x)
    li_x = x / math.log(x) * (1 + 1/math.log(x) + 2/math.log(x)**2)
    # RH bound on error
    rh_bound = math.sqrt(x) * math.log(x)
    return li_x, rh_bound


def run_analogy_comparison() -> None:
    print("Phase 13: Arithmetic Hodge Index Theorem -- The Precise Gap")
    print("=" * 70)
    print()
    print("COMPARISON: Function field Weil bound vs Number field RH bound")
    print("-" * 60)
    print()
    print("Function field (curve C/F_q, genus g=1, q=2):")
    print(f"  {'n':>4}  {'center q^n+1':>14}  {'Weil bound 2g*q^{n/2}':>22}  {'ratio':>8}")
    print(f"  {'--':>4}  {'------------':>14}  {'--------------------':>22}  {'-----':>8}")
    for n in [1, 2, 3, 4, 5]:
        center, bound = weil_bound_function_field(q=2, g=1, n=n)
        print(f"  {n:>4}  {center:>14.1f}  {bound:>22.4f}  {bound/center:>8.4f}")
    print()
    print("  The Weil bound says: |C(F_{q^n})| is within 2g*q^{n/2} of q^n+1.")
    print("  This is O(q^{n/2}) error on a O(q^n) main term -- square root savings.")
    print()

    print("Number field (Riemann zeta, analogue):")
    print(f"  {'x':>10}  {'li(x) approx':>14}  {'RH bound sqrt(x)*log(x)':>24}  {'ratio':>8}")
    print(f"  {'--':>10}  {'------------':>14}  {'-----------------------':>24}  {'-----':>8}")
    import math
    for x in [100, 1000, 10000, 100000]:
        li_x, rh_bound = prime_counting_rh_bound(x)
        print(f"  {x:>10.0f}  {li_x:>14.2f}  {rh_bound:>24.2f}  {rh_bound/x:>8.4f}")
    print()
    print("  The RH bound says: |pi(x) - li(x)| is within sqrt(x)*log(x).")
    print("  This is O(sqrt(x)*log(x)) error on O(x/log(x)) main term.")
    print()

    print("=" * 70)
    print("THE PRECISE ANALOGY:")
    print()
    print("  Function field:  Hodge Index on CxC  =>  Weil bound  =>  RH")
    print("  Number field:    ???                 =>  RH bound    =>  RH")
    print()
    print("  The '???' is the missing arithmetic Hodge Index Theorem.")
    print("  It would need to live on 'Spec(Z) x Spec(Z)'.")
    print()
    print("  Connes-Consani (2014): constructed the FRAMEWORK for this object")
    print("  (the 'arithmetic site' / 'scaling site').")
    print("  Status: intersection form and Hodge Index Theorem NOT YET PROVED.")
    print()
    print("=" * 70)
    print("WHAT {D,P}=0 CONTRIBUTES (honest assessment):")
    print()
    print("  1. Algebraic structure: K = K_+ + K_- (block diagonal)")
    print("  2. Correct decomposition of the positivity problem")
    print("  3. Precise analogy with function field (Poincare duality = P)")
    print()
    print("  What {D,P}=0 CANNOT contribute:")
    print("  4. The geometric input (ampleness, Riemann-Roch on 'ZxZ')")
    print("  5. The positivity K_+ >= 0 and K_- >= 0")
    print()
    print("  Symmetry does not imply positivity. This is a fundamental barrier.")
    print()
    print("=" * 70)
    print("THE OPEN QUESTION (precisely stated):")
    print()
    print("  Does there exist a bilinear form B on L^2_0(A_Q^*/Q^*) such that:")
    print("  (a) B is the 'arithmetic intersection form' on 'Spec(Z) x Spec(Z)'")
    print("  (b) B satisfies an arithmetic Hodge Index Theorem: B(D,D) <= 0")
    print("      for D orthogonal to an 'arithmetic ample class'")
    print("  (c) B implies the Weil positivity K >= 0")
    print()
    print("  If yes: RH follows.")
    print("  If no: the function field analogy breaks down at this step,")
    print("         and a fundamentally different approach is needed.")
    print()
    print("  Current status: OPEN. Neither Connes-Consani nor anyone else")
    print("  has constructed B with properties (a)-(c).")


if __name__ == '__main__':
    run_analogy_comparison()
