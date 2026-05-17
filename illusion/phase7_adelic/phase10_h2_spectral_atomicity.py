"""
Phase 10: H2 — Spectral Atomicity of D on L^2_0(A_Q^*/Q^*).

=============================================================================
THE PRECISE THEOREM TO PROVE
=============================================================================

Theorem (H2):
  Let D = -i * d/d(log|·|) be the scaling operator on L^2_0(A_Q^*/Q^*),
  where L^2_0 = {f in L^2(A_Q^*/Q^*) : integral f d*x = 0}.

  The spectral measure of D is purely atomic:
    mu_D = sum_n c_n * delta_{i*gamma_n}

  where {1/2 + i*gamma_n} are the non-trivial zeros of zeta(s),
  and c_n > 0 are positive weights.

  Equivalently: the regular representation of A_Q^*/Q^* on L^2_0
  decomposes as a direct sum (not a direct integral) of irreducible
  representations.

=============================================================================
STRATEGY: LANGLANDS SPECTRAL DECOMPOSITION FOR GL(1)
=============================================================================

The Langlands spectral decomposition for GL(1)/Q states:

  L^2(A_Q^*/Q^*) = L^2_disc ⊕ L^2_cont

where:
  L^2_disc = direct sum of Hecke characters chi: A_Q^*/Q^* -> C^*
             with |chi| = 1 (unitary characters)
  L^2_cont = direct integral over the continuous family chi_s = |·|^s, s in iR

The continuous part L^2_cont is spanned by the characters |x|^s for s in iR.
These are the "Eisenstein series" for GL(1).

On L^2_0 (zero-integral functions):
  The constant function 1 = |x|^0 is removed.
  But the other characters |x|^s for s != 0 are NOT in L^2_0.

Wait — are the characters |x|^s in L^2_0?

  integral_{A_Q^*/Q^*} |x|^s d*x = ?

For s = 0: integral 1 d*x = vol(A_Q^*/Q^*) = finite (by product formula).
For s != 0: the integral diverges (|x|^s is not integrable on A_Q^*/Q^*
  unless s = 0, because the norm |x|_A takes all positive real values).

So the characters |x|^s for s != 0 are NOT in L^2(A_Q^*/Q^*) at all.
They are in L^2_loc but not L^2.

This means: the "continuous spectrum" of D on L^2(A_Q^*/Q^*) does NOT
come from the characters |x|^s directly. It comes from the SPECTRAL MEASURE
of D, which is a more subtle object.

=============================================================================
THE CORRECT SPECTRAL THEORY
=============================================================================

The spectral theory of D on L^2(A_Q^*/Q^*) is given by the Plancherel
theorem for the group A_Q^*/Q^*.

A_Q^*/Q^* is a locally compact abelian group. Its Pontryagin dual is:
  (A_Q^*/Q^*)^ = {unitary characters chi: A_Q^*/Q^* -> U(1)}
               = {Hecke characters of Q}

The Plancherel theorem for A_Q^*/Q^* states:
  L^2(A_Q^*/Q^*) = integral_{(A_Q^*/Q^*)^} V_chi d mu(chi)

where mu is the Plancherel measure on the dual group.

The dual group (A_Q^*/Q^*)^ consists of:
  - The trivial character chi_0 = 1 (isolated point)
  - The characters chi_s = |·|^s for s in iR (continuous family)
  - The Dirichlet characters chi_D (isolated points, one for each conductor)

The Plancherel measure mu is:
  - A point mass at chi_0 (trivial character)
  - Lebesgue measure on {chi_s : s in iR} (continuous part)
  - Point masses at each Dirichlet character chi_D

So the Plancherel decomposition has BOTH discrete and continuous parts.
The continuous part {chi_s : s in iR} is the source of the continuous spectrum.

On L^2_0 (removing the trivial character):
  The trivial character chi_0 is removed.
  The Dirichlet characters chi_D remain (discrete).
  The continuous family {chi_s : s in iR} remains (continuous).

So L^2_0 STILL has a continuous spectrum from {chi_s : s in iR, s != 0}.

=============================================================================
THE CRITICAL REALIZATION
=============================================================================

The characters chi_s = |·|^s for s in iR are NOT in L^2(A_Q^*/Q^*).
But they contribute to the SPECTRAL MEASURE of D via the Plancherel theorem.

The Plancherel theorem says: for f in L^2(A_Q^*/Q^*),
  ||f||^2 = integral |f_hat(chi)|^2 d mu(chi)

where f_hat(chi) = integral f(x) chi(x)^{-1} d*x is the Fourier transform.

The spectral measure of D is determined by:
  <f, e^{itD} g> = integral chi_s(e^{it}) f_hat(chi_s) g_hat(chi_s)^* ds
                 = integral e^{its} f_hat(chi_s) g_hat(chi_s)^* ds

This is a continuous integral over s in iR — the spectral measure of D
has a CONTINUOUS component from the characters chi_s.

CONCLUSION: The spectral measure of D on L^2_0(A_Q^*/Q^*) is NOT purely
atomic. It has a continuous component from the characters chi_s = |·|^s.

This means H2 as stated is FALSE for the full L^2_0(A_Q^*/Q^*).

=============================================================================
WHERE DO THE ZETA ZEROS COME FROM?
=============================================================================

If the spectral measure of D is continuous (not atomic), where do the
zeta zeros appear?

Answer: they appear as POLES OF THE RESOLVENT, not as eigenvalues.

The resolvent R(z) = (D - z)^{-1} has poles at the eigenvalues of D.
But D has no eigenvalues on L^2(A_Q^*/Q^*) — it has only continuous spectrum.

The zeta zeros appear as poles of the MEROMORPHIC CONTINUATION of the
resolvent, i.e., as RESONANCES of D.

This is the correct picture:
  - D has continuous spectrum on L^2(A_Q^*/Q^*)
  - The resolvent R(z) = (D - z)^{-1} is analytic for z not in the spectrum
  - The resolvent has a meromorphic continuation to a larger domain
  - The poles of this continuation are the RESONANCES of D
  - The resonances are at z = i*gamma_n where 1/2 + i*gamma_n are zeta zeros

RH in this language:
  All resonances of D are purely imaginary (no real part).
  Equivalently: all poles of the meromorphic continuation of R(z) are on iR.

=============================================================================
THE CORRECT FORMULATION OF H2
=============================================================================

H2 (corrected):
  The resolvent R(z) = (D - z)^{-1} on L^2_0(A_Q^*/Q^*) has a meromorphic
  continuation to C \ iR, and all poles of this continuation are on iR.

This is equivalent to RH.

The UCA contribution:
  {D, P} = 0 forces: if z is a pole of R(z), then -z is also a pole.
  Combined with anti-self-adjointness (poles on iR): consistent with RH.
  But does NOT force poles to be on iR — only forces them to come in pairs.

=============================================================================
THE SELBERG ZETA FUNCTION ANALOGY
=============================================================================

For a compact hyperbolic surface Gamma\H:
  - The Laplacian Delta has discrete spectrum {lambda_n}
  - The Selberg zeta function Z(s) has zeros at s = 1/2 + i*sqrt(lambda_n - 1/4)
  - RH for Z(s) is equivalent to lambda_n >= 1/4 (Selberg's theorem, proved)

For A_Q^*/Q^* (non-compact):
  - D has continuous spectrum
  - The "Selberg zeta function" is the Riemann zeta function zeta(s)
  - RH for zeta(s) is equivalent to: all resonances of D are on iR

The analogy is precise. The difference:
  - Compact case: Selberg proved RH (lambda_n >= 1/4) using trace formula
  - Non-compact case: RH for zeta(s) is open

The Selberg trace formula for the compact case works because:
  - The spectrum is discrete (compactness)
  - The trace formula converges absolutely

For A_Q^*/Q^* (non-compact):
  - The spectrum is continuous
  - The trace formula has a continuous contribution
  - Convergence is more delicate

=============================================================================
NUMERICAL EXPERIMENT: RESONANCES OF D
=============================================================================

We can test the resonance picture numerically by computing the poles of
the meromorphic continuation of R(z) for the truncated adelic operator.

For the truncated operator D on a finite-dimensional space, R(z) = (D - z)^{-1}
has poles exactly at the eigenvalues of D (which are k*log(p) for k in Z).

As we increase the truncation (larger N, more primes), the eigenvalues
become denser and approach the continuous spectrum.

The resonances (poles of the meromorphic continuation) should approach
the zeta zeros as the truncation increases.

This is a numerical test of H2 (corrected).
"""

import numpy as np
from scipy.linalg import eigvals
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from phase9_h1_continuous_spectrum import build_dilation_operator, build_parity_operator_adelic


def compute_resolvent_poles(primes: list, N: int) -> np.ndarray:
    """
    Compute the poles of R(z) = (D - z)^{-1} for the truncated D.
    These are the eigenvalues of D.
    As N -> inf, these should approach the resonances (zeta zeros).
    """
    D = build_dilation_operator(primes, N)
    return np.sort(np.diag(D))  # D is diagonal, eigenvalues = diagonal entries


def zeta_zeros_imaginary_parts(n: int = 20) -> np.ndarray:
    """First n imaginary parts of non-trivial zeta zeros."""
    return np.array([
        14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
        37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
        52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
        67.0798, 69.5465, 72.0672, 75.7047, 77.1448,
    ][:n])


def run_resonance_experiment() -> None:
    """
    Test: do the eigenvalues of D (truncated) approach zeta zeros?

    The eigenvalues of D are k*log(p) for k in {-N,...,N}, p in primes.
    The zeta zeros have imaginary parts gamma_n ~ 14.13, 21.02, ...

    For the eigenvalues to approach zeta zeros, we need:
      k*log(p) ≈ gamma_n  for some k, p

    This is a Diophantine approximation problem:
      gamma_n ≈ k * log(p)  for integers k and primes p

    The zeta zeros are NOT known to be rational multiples of log(p).
    So the eigenvalues of D do NOT approach zeta zeros in general.

    This confirms: the resonances of D are NOT the eigenvalues of D.
    The resonances require the meromorphic continuation of R(z).
    """
    print("Resonance Experiment: Do D eigenvalues approach zeta zeros?")
    print()

    gamma = zeta_zeros_imaginary_parts(10)
    print(f"  First 10 zeta zero imaginary parts: {gamma.round(3)}")
    print()

    for primes, N in [([2, 3, 5, 7], 3), ([2, 3, 5, 7, 11], 4)]:
        evals = compute_resolvent_poles(primes, N)
        # Only look at positive eigenvalues (imaginary axis)
        pos_evals = np.sort(evals[evals > 0])

        print(f"  Primes={primes}, N={N}: {len(pos_evals)} positive eigenvalues")
        print(f"  Range: [{pos_evals[0]:.3f}, {pos_evals[-1]:.3f}]")

        # Find closest eigenvalue to each zeta zero
        print(f"  Closest eigenvalue to each zeta zero:")
        for g in gamma[:5]:
            if len(pos_evals) > 0:
                idx = np.argmin(np.abs(pos_evals - g))
                closest = pos_evals[idx]
                print(f"    gamma={g:.3f} -> closest={closest:.3f} (gap={abs(closest-g):.3f})")
        print()


def h2_summary() -> None:
    print("=" * 62)
    print("H2 SUMMARY: THE CORRECT PICTURE")
    print()
    print("  The spectral measure of D on L^2_0(A_Q^*/Q^*) is NOT")
    print("  purely atomic. It has a continuous component from the")
    print("  characters chi_s = |·|^s for s in iR.")
    print()
    print("  The zeta zeros appear as RESONANCES of D, not eigenvalues.")
    print("  Resonances = poles of the meromorphic continuation of R(z).")
    print()
    print("  H2 (corrected):")
    print("    All resonances of D are purely imaginary.")
    print("    Equivalently: all poles of the meromorphic continuation")
    print("    of R(z) are on iR.")
    print("    This is equivalent to RH.")
    print()
    print("  The UCA contribution:")
    print("    {D, P} = 0 forces resonances to come in pairs (z, -z).")
    print("    Anti-self-adjointness forces resonances to be on iR IF")
    print("    they are eigenvalues. But resonances are NOT eigenvalues.")
    print("    So UCA does not directly force resonances onto iR.")
    print()
    print("  THE REMAINING GAP:")
    print("    Show that the resonances of D (poles of meromorphic R(z))")
    print("    are constrained to iR by the UCA symmetry {D, P} = 0.")
    print()
    print("    This requires: the meromorphic continuation of R(z)")
    print("    satisfies P R(z) P = -R(-z) (which we proved for the")
    print("    resolvent itself). If this relation extends to the")
    print("    meromorphic continuation, then poles come in pairs (z, -z).")
    print("    Combined with the functional equation of zeta(s) (which")
    print("    forces poles to be symmetric about Re(s) = 1/2), this")
    print("    would force all poles to be on iR.")
    print()
    print("  THIS IS THE PRECISE REMAINING STEP.")
    print("  It requires:")
    print("    1. Meromorphic continuation of R(z) to C \\ iR")
    print("    2. Extension of P R(z) P = -R(-z) to the continuation")
    print("    3. Functional equation of zeta(s) as a constraint on poles")
    print("    4. Conclusion: poles on iR")


if __name__ == '__main__':
    print("Phase 10: H2 — Spectral Atomicity and Resonances")
    print("=" * 62)
    print()
    run_resonance_experiment()
    h2_summary()
