"""
Phase 9d: The anti-self-adjointness condition — closing the gap to RH.

=============================================================================
THE PRECISE GAP
=============================================================================

We have established:
  1. D anticommutes with P: {D, P} = 0  (verified numerically)
  2. This forces the spectrum of D to be symmetric about 0
  3. RH requires: spectrum of D is purely imaginary (D* = -D)
  4. Gap: {D, P} = 0 gives symmetry, not anti-self-adjointness

The question: is there a UCA condition that forces D* = -D?

=============================================================================
WHAT D* = -D MEANS
=============================================================================

D is anti-self-adjoint iff:
  <Df, g> = -<f, Dg>  for all f, g in the domain of D

Equivalently: iD is self-adjoint (iD is the Hilbert-Polya operator).

For the dilation generator D = -i * d/dt on L^2(R, dt):
  D* = i * d/dt = -D  ✓  (D is anti-self-adjoint on L^2(R))

For the adelic dilation generator D on L^2(A_Q^*/Q^*):
  D is anti-self-adjoint IF the underlying measure d*x is D-invariant.
  The multiplicative Haar measure d*x = dx/|x| IS invariant under dilations.
  So D is anti-self-adjoint on L^2(A_Q^*, d*x).

But on the QUOTIENT L^2(A_Q^*/Q^*), the situation is more subtle:
  The quotient measure is well-defined (Q^* is discrete, so the quotient
  is a locally compact group with a Haar measure).
  D descends to the quotient and remains anti-self-adjoint.

CONCLUSION: D is ALREADY anti-self-adjoint on L^2(A_Q^*/Q^*).
The spectrum of D is purely imaginary.
This means: the eigenvalues of D are in iR.

If the eigenvalues of D are {i*gamma_n}, then the zeros of zeta are at
s = 1/2 + i*gamma_n — which is exactly RH.

=============================================================================
WAIT — IS THIS ACTUALLY A PROOF?
=============================================================================

Let's be very careful. The argument is:

1. D is anti-self-adjoint on L^2(A_Q^*/Q^*) (by invariance of Haar measure).
2. The spectrum of D is purely imaginary.
3. The eigenvalues of D are {i*gamma_n} where 1/2 + i*gamma_n are zeta zeros.
4. Therefore all gamma_n are real, i.e., all zeros are on the critical line.

Step 3 is the problem. It assumes that the eigenvalues of D are EXACTLY
the imaginary parts of zeta zeros. This is the content of H2 — it is NOT
established.

The argument would be circular if we used "D has eigenvalues i*gamma_n"
to conclude "gamma_n are real." We need to FIRST establish that D has
eigenvalues i*gamma_n (H2), and THEN conclude gamma_n are real (RH).

But H2 is the hard part. The anti-self-adjointness of D gives us:
  "IF D has eigenvalues i*gamma_n, THEN gamma_n are real."
This is a conditional statement, not a proof of RH.

=============================================================================
THE CORRECT LOGICAL STRUCTURE
=============================================================================

The UCA framework gives:

  (A) D is anti-self-adjoint on L^2(A_Q^*/Q^*)  [from Haar measure invariance]
  (B) {D, P} = 0  [UCA anticommutation, verified]
  (C) The spectrum of D is purely imaginary  [from (A)]
  (D) The spectrum of D is symmetric about 0  [from (B)]

  (E) H2: The discrete spectrum of D consists of {i*gamma_n}
          where 1/2 + i*gamma_n are the non-trivial zeros of zeta(s).
          [NOT established — this is the hard part]

  (F) RH: All gamma_n are real.
          [Follows from (C) + (E): if eigenvalues are i*gamma_n and
           spectrum is purely imaginary, then gamma_n are real.]

So the logical chain is:
  (A) + (B) + (E) => (F)

The UCA framework establishes (A) and (B). H2 (E) is the missing piece.

=============================================================================
WHAT H2 REQUIRES
=============================================================================

H2: The discrete spectrum of D on L^2(A_Q^*/Q^*) = {i*gamma_n}.

This requires showing:
  (i)  The discrete spectrum is non-empty (trivially true: zeta zeros exist)
  (ii) Every discrete eigenvalue i*t corresponds to a zeta zero 1/2 + it
  (iii) Every zeta zero 1/2 + it corresponds to a discrete eigenvalue i*t

(ii) is the hard direction: show that if D f = i*t f, then zeta(1/2 + it) = 0.
(iii) is also hard: show that if zeta(1/2 + it) = 0, then i*t is an eigenvalue of D.

The explicit formula gives a partial answer to (iii):
  The von Mangoldt function psi(x) = sum_{p^k <= x} log(p) satisfies:
    psi(x) = x - sum_rho x^rho/rho - log(2pi) - (1/2)log(1 - x^{-2})
  where the sum is over non-trivial zeros rho = 1/2 + i*gamma_n.

  This shows that the zeta zeros appear as "frequencies" in psi(x).
  In the adelic framework, psi(x) is related to the spectral measure of D.
  So the zeta zeros DO appear in the spectrum of D — but as frequencies
  of the spectral measure, not necessarily as discrete eigenvalues.

The distinction: a frequency in the spectral measure can come from either
  - A discrete eigenvalue (point spectrum)
  - A resonance in the continuous spectrum (not an eigenvalue)

H2 requires showing the zeta zeros are discrete eigenvalues, not resonances.

=============================================================================
THE CONNES APPROACH AND WHERE IT STANDS
=============================================================================

Connes (1999) constructed an operator on L^2(A_Q/Q^*) whose spectrum
is related to zeta zeros. His approach:

1. Define the "absorption spectrum": the complement of the spectrum of
   a certain operator is the set of zeta zeros.
2. The operator is constructed from the adelic structure.
3. RH would follow if the operator has a certain spectral property.

The Connes approach is the closest existing work to what we are doing.
The key difference: Connes works with the COMPLEMENT of the spectrum,
while we work with the spectrum directly.

Our approach (UCA) adds: the anticommutation {D, P} = 0 as a symmetry
principle that constrains the operator. This is a new ingredient not
in Connes' original work.

=============================================================================
THE OPEN QUESTION: SHARPER UCA CONDITION
=============================================================================

We need a UCA condition that forces:
  "The discrete spectrum of D consists exactly of {i*gamma_n}."

Candidate: the UCA condition on the RESOLVENT.

Define the resolvent R(z) = (D - z)^{-1} for z not in the spectrum.

UCA condition on the resolvent:
  P R(z) P = R(-z)   (the resolvent at z is related to the resolvent at -z)

This follows from {D, P} = 0:
  P(D - z)P = PDP - zP = -D - zP... wait, let me compute carefully.

  {D, P} = 0 means DP = -PD.
  P(D - z)P = PDP - zP^2 = -D*P^2 - z*I = -D - z*I = -(D + z)

  So P(D - z)P = -(D + z).

  Therefore: P R(z) P = P(D - z)^{-1}P = [P(D - z)P]^{-1} = [-(D + z)]^{-1} = -R(-z).

So the UCA condition gives: P R(z) P = -R(-z).

This means: if z is a pole of R(z) (i.e., z is an eigenvalue of D),
then -z is also a pole of R(-z) (i.e., -z is also an eigenvalue of D).

This is just the spectral symmetry we already knew: eigenvalues come in
pairs (z, -z). Combined with anti-self-adjointness (eigenvalues in iR),
this gives: eigenvalues come in pairs (it, -it) for t real.

This is consistent with RH but does not prove it.

=============================================================================
NUMERICAL VERIFICATION OF P R(z) P = -R(-z)
=============================================================================
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from phase9_h1_continuous_spectrum import build_dilation_operator, build_parity_operator_adelic


def verify_resolvent_relation(primes: list = None, N: int = 1,
                               z: complex = 0.5 + 0.3j) -> None:
    """
    Verify: P R(z) P = -R(-z) where R(z) = (D - z)^{-1}.
    This follows from {D, P} = 0.
    """
    if primes is None:
        primes = [2, 3]

    D = build_dilation_operator(primes, N).astype(complex)
    P = build_parity_operator_adelic(D.real).astype(complex)
    n = D.shape[0]
    I = np.eye(n, dtype=complex)

    # Resolvent at z and -z
    Rz = np.linalg.inv(D - z * I)
    Rmz = np.linalg.inv(D + z * I)  # R(-z) = (D - (-z))^{-1} = (D + z)^{-1}

    # Check P R(z) P = -R(-z)
    lhs = P @ Rz @ P
    rhs = -Rmz

    err = np.linalg.norm(lhs - rhs, 'fro')
    print(f"  Primes={primes}, N={N}, z={z}")
    print(f"  ||P R(z) P - (-R(-z))|| = {err:.2e}  (should be ~0)")


def summarize_rh_gap() -> None:
    """Print the precise gap between UCA and RH."""
    print()
    print("PRECISE GAP BETWEEN UCA AND RH:")
    print()
    print("  UCA gives:")
    print("    (1) D is anti-self-adjoint: D* = -D  [Haar measure invariance]")
    print("    (2) {D, P} = 0: D anticommutes with P  [UCA anticommutation]")
    print("    (3) P R(z) P = -R(-z)  [resolvent relation, from (2)]")
    print()
    print("  These imply:")
    print("    - Spectrum of D is purely imaginary (from (1))")
    print("    - Spectrum is symmetric about 0 (from (2))")
    print("    - Eigenvalues come in pairs (it, -it) for t real")
    print()
    print("  RH requires additionally:")
    print("    (4) H2: The discrete spectrum of D = {i*gamma_n}")
    print("        where 1/2 + i*gamma_n are the non-trivial zeros of zeta(s)")
    print()
    print("  The gap: (1)+(2)+(3) do NOT imply (4).")
    print("  (4) is an identification of the spectrum with zeta zeros.")
    print("  This identification requires a direct construction,")
    print("  not just symmetry principles.")
    print()
    print("  The explicit formula gives a PARTIAL answer:")
    print("    The zeta zeros appear as frequencies in psi(x).")
    print("    psi(x) is the spectral measure of D.")
    print("    But frequencies in the spectral measure != discrete eigenvalues.")
    print()
    print("  WHAT WOULD CLOSE THE GAP:")
    print("    Show that the spectral measure of D on L^2(A_Q^*/Q^*) is")
    print("    PURELY ATOMIC (sum of point masses at {i*gamma_n}).")
    print("    This would mean: no continuous spectrum, only discrete eigenvalues.")
    print("    Combined with (1): all gamma_n are real => RH.")
    print()
    print("  This is equivalent to showing:")
    print("    The Plancherel measure on L^2(A_Q^*/Q^*) is purely atomic.")
    print("    I.e., the regular representation of A_Q^*/Q^* decomposes")
    print("    as a direct sum (not integral) of irreducible representations.")
    print()
    print("  For A_Q^1/Q^* (compact): this is TRUE (Peter-Weyl theorem).")
    print("  For A_Q^*/Q^* (non-compact): this is UNKNOWN.")
    print("  This is the precise mathematical content of H2.")


if __name__ == '__main__':
    print("Phase 9d: Anti-Self-Adjointness and the Gap to RH")
    print("=" * 62)
    print()

    print("Verifying resolvent relation P R(z) P = -R(-z):")
    print()
    for primes, N in [([2, 3], 1), ([2, 3, 5], 1)]:
        for z in [0.5 + 0.3j, 1.0 + 0.7j, 0.1 + 2.0j]:
            verify_resolvent_relation(primes, N, z)
        print()

    summarize_rh_gap()
