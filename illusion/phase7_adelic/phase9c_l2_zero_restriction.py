"""
Phase 9c: L^2_0 restriction and Tate's thesis — the correct H1.

=============================================================================
THE KEY INSIGHT FROM PHASE 9b
=============================================================================

H1 is NOT: "UCA forces continuous spectrum to vanish on all of L^2."
H1 IS:     "On L^2_0 (zero-integral functions), the spectrum is discrete,
            and UCA explains WHY the correct subspace is L^2_0."

=============================================================================
TATE'S THESIS (1950) — THE RELEVANT RESULT
=============================================================================

Tate's thesis establishes the spectral decomposition of L^2(A_Q^*/Q^*):

  L^2(A_Q^*/Q^*) = C * 1  ⊕  L^2_0(A_Q^*/Q^*)

where:
  - C * 1 = constant functions (the trivial representation, |x|^0 = 1)
  - L^2_0 = {f in L^2 : integral_{A_Q^*/Q^*} f(x) d*x = 0}

The spectral decomposition of the Hecke algebra on L^2_0:
  - The characters |x|^s for s in iR contribute to the CONTINUOUS spectrum
    of the Hecke algebra on L^2(A_Q^*/Q^*).
  - BUT: on L^2_0, the characters |x|^s with s != 0 are ABSENT.
    (They have nonzero integral: integral |x|^s d*x diverges for s != 0
     on the compact quotient A_Q^1/Q^*, where A_Q^1 = {x : |x|_A = 1}.)

Wait — this needs to be more careful. Let me redo this.

=============================================================================
THE CORRECT SPACE: A_Q^1 / Q^*
=============================================================================

The correct space for the spectral theory is NOT A_Q^*/Q^* but:

  A_Q^1 / Q^*

where A_Q^1 = {x in A_Q^* : |x|_A = 1} is the norm-1 ideles.

This space IS compact (by the product formula and finiteness of class number).

On the compact space A_Q^1/Q^*, the spectral decomposition is:
  L^2(A_Q^1/Q^*) = sum_chi V_chi

where chi ranges over Hecke characters of conductor dividing N.
The spectrum is PURELY DISCRETE.

The Eisenstein series on A_Q^1/Q^* are the characters chi(x) = |x|^s
restricted to A_Q^1. But |x|_A = 1 on A_Q^1, so |x|^s = 1 for all s.
The only Eisenstein contribution is the trivial character.

CONCLUSION: On A_Q^1/Q^* (the COMPACT quotient), the spectrum is
purely discrete. The continuous spectrum lives on A_Q^*/Q^* (non-compact).

=============================================================================
THE UCA OPERATOR ON A_Q^1/Q^*
=============================================================================

The UCA parity operator P on A_Q^1/Q^*:
  P: f(x) -> f(x^{-1})

Since |x^{-1}|_A = |x|_A^{-1} = 1 for x in A_Q^1, P maps A_Q^1 to itself.
So P is well-defined on A_Q^1/Q^*.

The dilation generator D on A_Q^1/Q^*:
  D = -i * d/dt|_{t=0} (x -> e^t x)

But e^t x has norm |e^t x|_A = e^t |x|_A = e^t != 1 for t != 0.
So the dilation group does NOT preserve A_Q^1.

The correct operator on A_Q^1/Q^* is the LAPLACIAN of the compact group,
not the dilation generator.

=============================================================================
RESOLUTION: TWO DIFFERENT SPECTRAL PROBLEMS
=============================================================================

There are TWO different spectral problems, and we have been conflating them:

PROBLEM A (non-compact, GL(1)):
  Space: A_Q^*/Q^*  (non-compact)
  Operator: dilation generator D
  Spectrum: continuous (all of iR) + discrete (zeta zeros, if they exist)
  H1: show discrete spectrum exists and equals zeta zeros
  Status: HARD — requires showing the discrete spectrum is non-empty

PROBLEM B (compact, GL(1)):
  Space: A_Q^1/Q^*  (compact)
  Operator: Laplacian of A_Q^1/Q^*
  Spectrum: purely discrete (by compactness)
  H1: trivially satisfied (compactness gives discrete spectrum)
  Status: EASY — but the spectrum is Hecke characters, not zeta zeros

The zeta zeros appear in PROBLEM A, not PROBLEM B.
The compactness of PROBLEM B does not help with PROBLEM A.

=============================================================================
THE CORRECT FORMULATION OF H1 (FINAL)
=============================================================================

H1 (correct statement):
  On L^2(A_Q^*/Q^*), the operator D^2 has a non-empty discrete spectrum.
  The discrete eigenvalues are {1/4 + gamma_n^2} where 1/2 + i*gamma_n
  are the non-trivial zeros of zeta(s).

This is NOT a consequence of UCA. It is equivalent to the existence of
non-trivial zeros of zeta(s) — which is known (Riemann proved they exist).

H1 is therefore TRIVIALLY TRUE: the discrete spectrum is non-empty
because zeta(s) has non-trivial zeros.

The HARD part is H2: show that the discrete spectrum consists EXACTLY
of the zeta zeros, with no extra eigenvalues.

=============================================================================
REVISED UNDERSTANDING OF THE RH PROBLEM
=============================================================================

The RH problem in the UCA framework is:

  H2 (the real problem): The discrete spectrum of D^2 on L^2(A_Q^*/Q^*)
  consists EXACTLY of {1/4 + gamma_n^2} where gamma_n are the imaginary
  parts of the non-trivial zeros of zeta(s), AND all gamma_n are real
  (i.e., all zeros are on the critical line Re(s) = 1/2).

This is a single statement: RH ↔ the discrete spectrum of D^2 is real
(all eigenvalues are of the form 1/4 + t^2 with t real).

If any zero has Re(s) != 1/2, say s = sigma + it with sigma != 1/2,
then the corresponding "eigenvalue" would be s(1-s) = sigma(1-sigma) - t^2 + i*t(1-2*sigma),
which is COMPLEX — not a real eigenvalue of a self-adjoint operator.

So: RH ↔ D^2 is self-adjoint on L^2(A_Q^*/Q^*) with real spectrum.

The UCA constraint [D^2, P] = 0 is automatically satisfied (D^2 has even eigenvalues).
It does NOT force D^2 to be self-adjoint — D^2 is already self-adjoint by construction.

CONCLUSION: The UCA framework as currently formulated does NOT give a
new proof strategy for RH. The equivalence RH ↔ "D^2 has real spectrum"
is a RESTATEMENT of RH, not a proof.

=============================================================================
WHAT WOULD ACTUALLY WORK
=============================================================================

For UCA to give a proof strategy, we need:

1. A CONSTRUCTION of D^2 that is NOT obviously self-adjoint.
   If D^2 is defined via a non-self-adjoint procedure, and UCA forces
   it to be self-adjoint, then UCA implies RH.

2. The Connes approach (closest to this):
   Connes defines an operator on L^2(A_Q/Q^*) whose spectrum is
   related to zeta zeros. The operator is NOT obviously self-adjoint.
   The question is whether it IS self-adjoint (which would imply RH).
   This is the Hilbert-Polya conjecture in the adelic setting.

3. The UCA contribution:
   UCA provides a SYMMETRY PRINCIPLE ([D, P] = 0 or [D^2, P] = 0)
   that constrains the operator. If this symmetry principle implies
   self-adjointness of D (not D^2), then UCA implies RH.

   But we showed: [D, P] = 0 is IMPOSSIBLE for the dilation generator
   (since PDP = -D, not D). So UCA in the form [D, P] = 0 is
   inconsistent with the dilation generator.

   The correct UCA condition for RH must be formulated differently.

=============================================================================
THE CORRECT UCA CONDITION FOR RH
=============================================================================

Instead of [D, P] = 0 (which is impossible), the correct condition is:

  D P = -P D   (D anticommutes with P)

This IS satisfied by the dilation generator:
  D P f_k = D f_{-k} = -k*log(p) f_{-k}
  -P D f_k = -P(k*log(p) f_k) = -k*log(p) f_{-k}  ✓

So D ANTICOMMUTES with P: {D, P} = DP + PD = 0.

The UCA condition should be: {D, P} = 0 (anticommutation).

Under {D, P} = 0:
  - D maps the +1 eigenspace of P to the -1 eigenspace, and vice versa.
  - The spectrum of D is symmetric about 0 (if lambda is an eigenvalue,
    so is -lambda).
  - This is consistent with the zeta zeros being symmetric about Re(s) = 1/2.

The RH statement in this language:
  The spectrum of D on L^2(A_Q^*/Q^*) is purely imaginary (in iR).
  Equivalently: D is anti-self-adjoint (D* = -D).

UCA ({D, P} = 0) forces the spectrum to be symmetric about 0.
RH requires the spectrum to be ON the imaginary axis (not just symmetric).

The gap: {D, P} = 0 gives symmetry, not reality.
To get reality, we need D to be anti-self-adjoint.
This is the content of the Hilbert-Polya conjecture.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from phase9_h1_continuous_spectrum import build_dilation_operator, build_parity_operator_adelic


def verify_anticommutation(primes: list = None, N: int = 1) -> None:
    """Verify that D anticommutes with P: DP + PD = 0."""
    if primes is None:
        primes = [2, 3]

    D = build_dilation_operator(primes, N)
    P = build_parity_operator_adelic(D)

    anticomm = D @ P + P @ D
    comm = D @ P - P @ D

    print(f"Primes={primes}, N={N}, dim={D.shape[0]}")
    print(f"  ||DP + PD|| (anticommutator) = {np.linalg.norm(anticomm, 'fro'):.2e}  (should be ~0)")
    print(f"  ||DP - PD|| (commutator)     = {np.linalg.norm(comm, 'fro'):.4f}  (should be nonzero)")
    print()


def spectrum_symmetry_check(primes: list = None, N: int = 2) -> None:
    """
    Check that the spectrum of D is symmetric about 0 (consequence of anticommutation).
    """
    if primes is None:
        primes = [2, 3, 5]

    D = build_dilation_operator(primes, N)
    evals = np.sort(np.diag(D))

    # Check symmetry: for each lambda, -lambda should also be present
    symmetric = True
    for lam in evals:
        if not any(abs(evals + lam) < 1e-10):
            symmetric = False
            break

    print(f"Primes={primes}, N={N}")
    print(f"  Spectrum symmetric about 0: {symmetric}")
    print(f"  Eigenvalues: {evals.round(3)}")
    print()


if __name__ == '__main__':
    print("Phase 9c: L^2_0 Restriction and Correct UCA Formulation")
    print("=" * 62)
    print()

    print("1. Verifying D anticommutes with P (not commutes):")
    print()
    for primes, N in [([2, 3], 1), ([2, 3, 5], 1)]:
        verify_anticommutation(primes, N)

    print("2. Spectrum symmetry (consequence of anticommutation):")
    print()
    for primes, N in [([2, 3], 1), ([2, 3, 5], 1)]:
        spectrum_symmetry_check(primes, N)

    print("=" * 62)
    print("SUMMARY OF H1 ANALYSIS (Phases 9, 9b, 9c)")
    print()
    print("  Phase 9:  [D, P] = 0 does not suppress continuous spectrum.")
    print("            The symmetrized D' = (D + PDP)/2 = 0 (trivial).")
    print()
    print("  Phase 9b: [D^2, P] = 0 is automatic (D^2 has even eigenvalues).")
    print("            The Selberg trace formula shows UCA alone cannot")
    print("            suppress the continuous spectrum.")
    print("            H1 is trivially true (zeta zeros exist) but H2 is hard.")
    print()
    print("  Phase 9c: The correct UCA condition is {D, P} = 0 (anticommutation).")
    print("            This forces the spectrum to be symmetric about 0.")
    print("            RH requires the spectrum to be purely imaginary.")
    print("            The gap: symmetry != reality.")
    print("            Closing this gap = proving the Hilbert-Polya conjecture.")
    print()
    print("  OPEN QUESTION: Is there a UCA condition that forces D to be")
    print("  anti-self-adjoint (D* = -D), not just spectrally symmetric?")
    print("  If yes, UCA implies RH. If no, UCA gives only a restatement.")
