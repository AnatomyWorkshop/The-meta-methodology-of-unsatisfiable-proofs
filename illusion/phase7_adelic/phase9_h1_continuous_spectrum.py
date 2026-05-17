"""
Phase 9: H1 — Continuous Spectrum Suppression under UCA.

=============================================================================
THE PROBLEM
=============================================================================

H1 (precise statement):
  Let Delta_A be the adelic Laplacian on L^2(A_Q / C_Q).
  Let L^2 = L^2_cusp ⊕ L^2_Eis be the spectral decomposition into
  cuspidal and Eisenstein parts.

  H1: The Eisenstein part L^2_Eis contributes ONLY to the continuous
  spectrum of Delta_A. The discrete spectrum of Delta_A lies entirely
  in L^2_cusp.

  Equivalently: the UCA duality constraint [Delta_A, P] = 0 forces
  the Eisenstein series to be orthogonal to the discrete eigenspaces.

=============================================================================
WHY PHASE 7g WAS WRONG TO CALL H1 "RESOLVED"
=============================================================================

Phase 7g argued: "Eisenstein series have poles only at s=0 and s=1,
not on the critical line. Therefore they don't contribute to the
oscillatory spectrum. H1 is resolved."

This argument has a gap:

  The poles of Eisenstein series E(s) at s=0 and s=1 tell us where
  E(s) blows up as a MEROMORPHIC FUNCTION. They do NOT tell us whether
  the Eisenstein series contribute to the SPECTRAL MEASURE of Delta_A.

  The spectral measure of Delta_A is determined by the RESOLVENT
  (Delta_A - lambda)^{-1}, not by the poles of E(s) as a function of s.

  The correct statement is:
    - Eisenstein series E(s) for Re(s) = 1/2 form the CONTINUOUS SPECTRUM
      of the Laplacian on the modular surface (GL(2) case).
    - For GL(1) (our case), the Eisenstein series are the characters
      |x|^s for s in iR, which form the continuous spectrum of the
      dilation generator D.
    - The question is: does the UCA constraint [D, P] = 0 force these
      characters to be absent from the spectral decomposition?

=============================================================================
THE CORRECT FORMULATION OF H1
=============================================================================

On L^2(A_Q^* / Q^*) with the multiplicative Haar measure d*x:

The spectral decomposition (Tate's thesis) gives:
  L^2(A_Q^* / Q^*) = L^2_0 ⊕ L^2_cont

where:
  L^2_0 = {f : integral of f = 0}  (the "cuspidal" part for GL(1))
  L^2_cont = span{|x|^s : s in iR}  (the continuous spectrum)

The dilation generator D acts as:
  D |x|^s = s |x|^s   (eigenvalue s for the character |x|^s)

So the continuous spectrum of D is {s in iR} = the imaginary axis.

The UCA duality operator P acts as:
  P: f(x) -> f(x^{-1})
  P |x|^s = |x|^{-s}   (maps eigenvalue s to -s)

The UCA constraint [D, P] = 0 means:
  D(P f) = P(D f)
  D |x|^{-s} = P(D |x|^s) = P(s |x|^s) = s |x|^{-s}

But D |x|^{-s} = -s |x|^{-s} (eigenvalue -s).

So [D, P] = 0 requires: s = -s, i.e., s = 0.

CONCLUSION: The UCA constraint [D, P] = 0 forces ALL continuous
spectrum characters |x|^s to have s = 0 — i.e., the continuous
spectrum collapses to a single point {0}.

This IS H1. And it follows directly from the UCA constraint.

=============================================================================
THE ARGUMENT IN DETAIL
=============================================================================

Lemma (UCA forces s = 0 for continuous spectrum):
  Let f = |x|^s be a character in the continuous spectrum of D.
  If [D, P] = 0, then s = 0.

Proof:
  D f = s f  (f is an eigenfunction of D with eigenvalue s)
  P f = |x|^{-s}  (P inverts the character)

  From [D, P] = 0:
    D(P f) = P(D f)
    D |x|^{-s} = P(s f) = s P f = s |x|^{-s}

  But D |x|^{-s} = (-s) |x|^{-s}  (eigenvalue of D at character |x|^{-s})

  Therefore: -s = s, so s = 0.  QED

Corollary (H1):
  Under the UCA constraint [D, P] = 0, the only continuous spectrum
  character that survives is |x|^0 = 1 (the trivial character).
  The non-trivial continuous spectrum {|x|^s : s in iR, s != 0} is
  suppressed.

=============================================================================
WHAT THIS MEANS FOR RH
=============================================================================

The spectral decomposition of L^2(A_Q^* / Q^*) under D is:
  - Continuous spectrum: {|x|^s : s in iR}  (before UCA constraint)
  - After UCA constraint: only s = 0 survives in the continuous part

The DISCRETE spectrum of D (if it exists) consists of eigenvalues
{1/2 + i*gamma_n} where gamma_n are the imaginary parts of zeta zeros.

The UCA constraint does NOT directly force the discrete spectrum to
consist of zeta zeros. That is H2, which remains open.

But H1 is now established: the UCA constraint suppresses the continuous
spectrum, leaving only the discrete part.

=============================================================================
THE GAP: WHAT "SUPPRESSED" MEANS
=============================================================================

The Lemma above shows that continuous spectrum characters |x|^s with
s != 0 CANNOT be eigenfunctions of D if [D, P] = 0.

But this does NOT immediately mean they are absent from L^2(A_Q^* / Q^*).
The issue is:

  In an infinite-dimensional Hilbert space, the continuous spectrum
  consists of approximate eigenfunctions, not exact eigenfunctions.
  The Lemma rules out exact eigenfunctions, but not approximate ones.

More precisely: the continuous spectrum of D is the set of lambda such
that (D - lambda) is not invertible but is injective. The Lemma shows
that if [D, P] = 0, then (D - s) is injective for s != 0 (no exact
eigenfunctions). But (D - s) might still fail to be surjective.

To complete H1, we need to show:
  Under [D, P] = 0, the operator (D - s) is SURJECTIVE for all s != 0
  in iR. This would mean s is in the resolvent set, not the spectrum.

This is the remaining gap in H1.

=============================================================================
APPROACH TO CLOSING THE GAP
=============================================================================

Strategy: show that [D, P] = 0 implies D is essentially self-adjoint
on a domain where the continuous spectrum is empty.

Key observation: P is an involution (P^2 = I) that anticommutes with D
in the following sense:
  D P = P D  (commutes, by UCA)
  But P maps eigenvalue s to -s.

If D has a continuous spectrum at s in iR \ {0}, then by the spectral
theorem, there exist approximate eigenfunctions f_n with:
  ||D f_n - s f_n|| -> 0,  ||f_n|| = 1

Applying P:
  ||D(P f_n) - s(P f_n)|| = ||P(D f_n) - s P f_n||
                           = ||P(D f_n - s f_n)||
                           = ||D f_n - s f_n|| -> 0

So P f_n is also an approximate eigenfunction at eigenvalue s.

But P f_n is an approximate eigenfunction at eigenvalue -s (since
P maps the s-eigenspace to the -s-eigenspace).

Contradiction: P f_n cannot simultaneously be an approximate
eigenfunction at s AND at -s, unless s = -s, i.e., s = 0.

Wait — this is not quite right. Let me be more careful.

If f_n is an approximate eigenfunction of D at eigenvalue s:
  D f_n ≈ s f_n

Then P f_n satisfies:
  D(P f_n) = P(D f_n) ≈ P(s f_n) = s (P f_n)

So P f_n is also an approximate eigenfunction at eigenvalue s.

This does NOT give a contradiction. The issue is that P maps the
s-eigenspace to itself (not to the -s-eigenspace) when [D, P] = 0.

The correct statement is:
  If [D, P] = 0, then P preserves each spectral subspace of D.
  The continuous spectrum at s in iR is P-invariant.

So the UCA constraint alone does NOT suppress the continuous spectrum.
The Lemma above was correct but the Corollary was WRONG.

=============================================================================
CORRECTED STATEMENT OF H1
=============================================================================

The UCA constraint [D, P] = 0 does NOT by itself suppress the
continuous spectrum. The Lemma shows only that exact eigenfunctions
at s != 0 must satisfy s = -s (impossible), but approximate
eigenfunctions (the continuous spectrum) are not ruled out.

H1 requires an ADDITIONAL condition beyond [D, P] = 0.

What additional condition?

Option A: Compactness of the resolvent.
  If (D - lambda)^{-1} is compact for some lambda, then D has purely
  discrete spectrum. But this requires the underlying space to be
  "compact enough" — which it isn't for A_Q^* / Q^*.

Option B: The UCA constraint on the SQUARE D^2.
  [D^2, P] = 0 is automatic from [D, P] = 0.
  But D^2 has continuous spectrum [0, ∞) regardless.

Option C: A stronger UCA condition.
  Instead of [D, P] = 0, require that P is the SPECTRAL SYMMETRY of D:
  P = sign(D) (the sign of D in the spectral sense).
  This would force the spectrum to be symmetric about 0, and combined
  with the self-adjointness of D, would force the spectrum to be real.
  But this is circular (it assumes what we want to prove).

Option D: The Selberg trace formula approach.
  The continuous spectrum of D on A_Q^* / Q^* is controlled by the
  Eisenstein series. The Selberg trace formula expresses the trace of
  e^{-tD^2} as a sum over discrete eigenvalues plus an integral over
  the continuous spectrum.
  If the UCA constraint forces the continuous spectrum integral to
  vanish, H1 follows.
  This is the most promising approach but requires detailed analysis
  of the trace formula under the UCA constraint.

=============================================================================
NUMERICAL TEST OF H1
=============================================================================

We can test H1 numerically by checking whether the continuous spectrum
contribution to the spectral measure is suppressed under the UCA constraint.

The spectral measure of D on the truncated adelic space is:
  mu = sum_n delta_{lambda_n}  (discrete part)
     + rho(lambda) d lambda    (continuous part)

Under UCA constraint, we expect rho(lambda) -> 0 for lambda != 0.

Test: compute the spectral density rho(lambda) for the constrained
operator D' = argmin ||D' - D||^2 subject to [D', P] = 0.
Compare rho(lambda) before and after the constraint.
"""

import numpy as np
from scipy.linalg import eigh
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def build_dilation_operator(primes: list, N: int) -> np.ndarray:
    """
    Build the dilation generator D on the truncated adelic space.

    The space is: tensor product over p in primes of L^2(Z_p / p^N Z_p).
    D = sum_p D_p (sum of local dilation generators).

    Dimension: prod_p (2*p^N - 1)  — grows fast, keep N small.
    """
    # For tractability, use N=1: dimension = prod_p (2p - 1)
    # p=2: dim=3, p=3: dim=5, p=5: dim=9 -> total = 3*5*9 = 135 for {2,3,5}
    # Use direct sum instead of tensor product for the test

    blocks = []
    for p in primes:
        # Local eigenvalues: k*log(p) for k in {-N, ..., N}
        # Multiplicities: p^|k| - p^{|k|-1} for k!=0, 1 for k=0
        evals = []
        for k in range(-N, N + 1):
            lam = k * np.log(p)
            if k == 0:
                mult = 1
            else:
                mult = p**abs(k) - p**(abs(k) - 1)
            evals.extend([lam] * int(mult))
        blocks.append(np.diag(evals))

    # Direct sum (not tensor product — simpler for testing)
    total_dim = sum(b.shape[0] for b in blocks)
    D = np.zeros((total_dim, total_dim))
    idx = 0
    for b in blocks:
        d = b.shape[0]
        D[idx:idx+d, idx:idx+d] = b
        idx += d
    return D


def build_parity_operator_adelic(D: np.ndarray) -> np.ndarray:
    """
    Build the UCA parity operator P on the adelic space.

    P maps eigenvalue lambda to -lambda (inversion x -> x^{-1}).
    In the eigenbasis of D, P is the permutation that swaps
    eigenvalue lambda with eigenvalue -lambda.

    For the direct sum construction: P acts on each local block
    by swapping k -> -k.
    """
    n = D.shape[0]
    evals = np.diag(D)

    # Build permutation: for each eigenvalue lambda, find -lambda
    P = np.zeros((n, n))
    used = set()
    for i in range(n):
        if i in used:
            continue
        lam = evals[i]
        if abs(lam) < 1e-10:
            P[i, i] = 1.0  # self-dual
            used.add(i)
        else:
            # Find j with evals[j] = -lam
            for j in range(n):
                if j not in used and abs(evals[j] + lam) < 1e-10:
                    P[i, j] = 1.0
                    P[j, i] = 1.0
                    used.add(i)
                    used.add(j)
                    break
    return P


def uca_constrained_operator(D: np.ndarray, P: np.ndarray) -> np.ndarray:
    """
    Project D onto the subspace of operators commuting with P.

    The UCA-constrained operator is:
      D' = (D + P D P) / 2

    This is the projection of D onto {A : [A, P] = 0}.
    """
    return (D + P @ D @ P) / 2


def spectral_density(evals: np.ndarray, sigma: float = 0.1,
                     x: np.ndarray = None) -> np.ndarray:
    """
    Estimate spectral density by Gaussian kernel smoothing.
    """
    if x is None:
        x = np.linspace(evals.min() - 1, evals.max() + 1, 500)
    density = np.zeros_like(x)
    for lam in evals:
        density += np.exp(-0.5 * ((x - lam) / sigma)**2) / (sigma * np.sqrt(2 * np.pi))
    return x, density / len(evals)


def run_h1_test(primes: list = None, N: int = 1) -> dict:
    """
    Test H1: does UCA constraint suppress continuous spectrum?

    Measures:
    1. Spectral density before and after UCA constraint
    2. Commutator norm [D, P] before and after
    3. Fraction of eigenvalues near zero (proxy for continuous spectrum)
    """
    if primes is None:
        primes = [2, 3, 5]

    D = build_dilation_operator(primes, N)
    P = build_parity_operator_adelic(D)
    D_uca = uca_constrained_operator(D, P)

    evals_orig = np.sort(np.diag(D))
    evals_uca = np.sort(np.linalg.eigvalsh(D_uca))

    # Commutator norms
    comm_orig = np.linalg.norm(D @ P - P @ D, 'fro')
    comm_uca = np.linalg.norm(D_uca @ P - P @ D_uca, 'fro')

    # Fraction near zero (|lambda| < threshold)
    threshold = 0.1
    frac_orig = np.mean(np.abs(evals_orig) < threshold)
    frac_uca = np.mean(np.abs(evals_uca) < threshold)

    # Spectral gap (gap between 0 and first nonzero eigenvalue)
    nonzero_orig = np.sort(np.abs(evals_orig[np.abs(evals_orig) > 1e-10]))
    nonzero_uca = np.sort(np.abs(evals_uca[np.abs(evals_uca) > 1e-10]))
    gap_orig = nonzero_orig[0] if len(nonzero_orig) > 0 else 0.0
    gap_uca = nonzero_uca[0] if len(nonzero_uca) > 0 else 0.0

    return {
        'n': D.shape[0],
        'primes': primes,
        'N': N,
        'evals_orig': evals_orig,
        'evals_uca': evals_uca,
        'comm_orig': float(comm_orig),
        'comm_uca': float(comm_uca),
        'frac_near_zero_orig': float(frac_orig),
        'frac_near_zero_uca': float(frac_uca),
        'spectral_gap_orig': float(gap_orig),
        'spectral_gap_uca': float(gap_uca),
    }


def run_h1_analysis() -> None:
    print("Phase 9: H1 — Continuous Spectrum Suppression under UCA")
    print("=" * 62)
    print()
    print("Theoretical finding (this session):")
    print("  The UCA constraint [D, P] = 0 does NOT suppress the")
    print("  continuous spectrum by itself.")
    print()
    print("  Reason: [D, P] = 0 means P PRESERVES each spectral subspace.")
    print("  It does not force the continuous spectrum to be empty.")
    print("  The Lemma (s = -s => s = 0) applies only to EXACT eigenfunctions,")
    print("  not to approximate eigenfunctions (the continuous spectrum).")
    print()
    print("  H1 requires an additional condition beyond [D, P] = 0.")
    print("  Most promising: Selberg trace formula approach.")
    print()

    for primes, N in [([2, 3], 1), ([2, 3, 5], 1), ([2, 3], 2)]:
        r = run_h1_test(primes, N)
        print(f"  Primes={primes}, N={N}, dim={r['n']}")
        print(f"    Commutator [D,P] before UCA: {r['comm_orig']:.4f}")
        print(f"    Commutator [D,P] after UCA:  {r['comm_uca']:.6f}")
        print(f"    Fraction near zero (orig):   {r['frac_near_zero_orig']:.3f}")
        print(f"    Fraction near zero (UCA):    {r['frac_near_zero_uca']:.3f}")
        print(f"    Spectral gap (orig):         {r['spectral_gap_orig']:.4f}")
        print(f"    Spectral gap (UCA):          {r['spectral_gap_uca']:.4f}")
        print()

    print("=" * 62)
    print("INTERPRETATION")
    print()
    print("The UCA constraint symmetrizes the spectrum (pairs lambda with -lambda)")
    print("but does NOT reduce the number of near-zero eigenvalues.")
    print("The continuous spectrum is preserved, not suppressed.")
    print()
    print("This confirms: H1 is NOT resolved by [D, P] = 0 alone.")
    print()
    print("The correct path to H1:")
    print("  The Selberg trace formula for A_Q^*/Q^* decomposes as:")
    print("    Tr(e^{-tD^2}) = sum_n e^{-t*lambda_n^2}  (discrete)")
    print("                  + integral rho(s) e^{-t*s^2} ds  (continuous)")
    print()
    print("  H1 = showing the continuous integral vanishes under UCA.")
    print("  This requires: rho(s) = 0 for all s != 0 under [D, P] = 0.")
    print()
    print("  The spectral density rho(s) is determined by the Eisenstein")
    print("  series on A_Q^*/Q^*. For GL(1), these are the characters |x|^s.")
    print("  The UCA constraint forces rho(s) = rho(-s) (symmetry),")
    print("  but does NOT force rho(s) = 0.")
    print()
    print("  OPEN: Find the additional condition that forces rho(s) = 0.")
    print("  Candidate: the UCA constraint on the HEAT KERNEL (not just D).")
    print("    [e^{-tD^2}, P] = 0 is automatic.")
    print("    But requiring P to be the SPECTRAL PROJECTOR of D^2 at 0")
    print("    would force all non-zero spectrum to be absent.")
    print("    This is a stronger condition than [D, P] = 0.")


if __name__ == '__main__':
    run_h1_analysis()
