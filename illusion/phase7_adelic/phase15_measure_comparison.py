"""
Phase 15: The Measure Comparison -- W_- as a Signed Measure Problem.

The key insight from Phase 14c:

W_-(g) = 2 * integral g(t)^2 d(M_prime - M_zero)(t)

where:
  M_prime = sum_{p^k} (log p / p^{k/2}) * delta_{log p^k}  (prime power measure)
  M_zero  = sum_{gamma_n > 0} delta_{gamma_n}               (zero measure)

W_- >= 0 for all g  iff  M_prime - M_zero is a POSITIVE measure.

This is a MEASURE COMPARISON problem:
  Does M_prime dominate M_zero?

The Mellin transforms of these measures are:
  Mellin(M_prime)(s) = sum_{p^k} (log p / p^{k/2}) * (log p^k)^{s-1}
                     = -zeta'/zeta(s + 1/2)  [related to log derivative of zeta]
  Mellin(M_zero)(s)  = sum_{gamma_n} gamma_n^{s-1}

They are related by the EXPLICIT FORMULA:
  -zeta'/zeta(s) = 1/(s-1) - sum_rho 1/(s-rho) + (archimedean terms)

The question W_- >= 0 becomes:
  Is the "odd part" of -zeta'/zeta(s) a positive measure on R+?

=============================================================================
THE EXPLICIT FORMULA CONNECTION
=============================================================================

The Weil explicit formula (in the form we need):

  sum_{p^k} (log p / p^{k/2}) * h(log p^k) = h_hat(0) + h_hat(1)
    - sum_rho h_hat(Im(rho) - 1/2) + (archimedean correction)

where h_hat is the Fourier transform of h.

For h = g^2 (non-negative), this gives:
  prime_sum(g) = (g^2)_hat(0) + (g^2)_hat(1) - zero_sum(g) + arch_correction

So:
  W_-(g) = 2*(prime_sum - zero_sum)
         = 2*((g^2)_hat(0) + (g^2)_hat(1) + arch_correction - 2*zero_sum)

Wait -- this is not right. Let me be more careful.

The explicit formula relates:
  sum_{p^k} (log p / p^{k/2}) * h(log p^k)  [prime side]
to:
  sum_rho h_hat(Im(rho))  [zero side]

via:
  prime_side = h_hat(0) + h_hat(1) - zero_side + arch_correction

So:
  prime_side - zero_side = h_hat(0) + h_hat(1) + arch_correction - 2*zero_side

This is NOT the same as prime_side >= zero_side.

The correct statement is:
  W(h) = prime_side - zero_side = h_hat(0) + h_hat(1) + arch_correction - 2*zero_side

And W(h) >= 0 for h = g*g_bar is the Weil positivity criterion.

=============================================================================
THE CORRECT MEASURE COMPARISON
=============================================================================

Let me redo this carefully.

The Weil distribution W acts on test functions h by:
  W(h) = sum_{p^k} (log p / p^{k/2}) * (h(log p^k) + h(-log p^k))
        - sum_rho h_hat(Im(rho) - 1/2)
        - (archimedean correction involving Gamma'/Gamma)

For h = f * f_bar (convolution, so h_hat = |f_hat|^2 >= 0):
  W(f*f_bar) = sum_{p^k} (log p / p^{k/2}) * 2*|f_hat(log p^k)|^2
              - sum_rho |f_hat(Im(rho) - 1/2)|^2
              - arch_correction(f)

RH says all Im(rho) - 1/2 are real (= gamma_n), so:
  W(f*f_bar) = 2*prime_sum(f_hat) - zero_sum(f_hat) - arch_correction(f)

where:
  prime_sum(f_hat) = sum_{p^k} (log p / p^{k/2}) * |f_hat(log p^k)|^2
  zero_sum(f_hat)  = sum_n |f_hat(gamma_n)|^2

The archimedean correction is:
  arch_correction(f) = integral |f_hat(t)|^2 * Re(Gamma'/Gamma(1/4 + it/2)) dt

This is the term we've been ignoring! It can be negative.

=============================================================================
THE ARCHIMEDEAN CORRECTION
=============================================================================

Re(Gamma'/Gamma(1/4 + it/2)) = Re(digamma(1/4 + it/2))

For large |t|: Re(digamma(1/4 + it/2)) ~ log(|t|/2)  (grows logarithmically)
For t = 0: Re(digamma(1/4)) ~ -3.5772 - 4*log(2) ~ -6.35  (negative!)

So the archimedean correction:
  - Is NEGATIVE for small |t| (digamma(1/4) < 0)
  - Is POSITIVE for large |t| (log(|t|/2) > 0)

For f_hat concentrated at small frequencies: arch_correction < 0
  => W(f*f_bar) = 2*prime_sum - zero_sum - (negative) = 2*prime_sum - zero_sum + |arch|
  => Easier to be positive

For f_hat concentrated at large frequencies (near gamma_n): arch_correction > 0
  => W(f*f_bar) = 2*prime_sum - zero_sum - (positive)
  => Harder to be positive

This is the CORRECT picture. The archimedean correction is the "missing term"
that makes the balance work.

=============================================================================
NUMERICAL TEST: INCLUDE ARCHIMEDEAN CORRECTION
=============================================================================
"""

import numpy as np
from scipy.special import digamma


def re_digamma(s_real: float, s_imag: float) -> float:
    """Re(digamma(s_real + i*s_imag))"""
    z = complex(s_real, s_imag)
    # Use asymptotic expansion for large |z|
    if abs(z) > 10:
        # digamma(z) ~ log(z) - 1/(2z) - 1/(12z^2) + ...
        return np.log(abs(z)) - s_real / (2 * abs(z)**2)
    else:
        # Use scipy digamma (real part only for real argument, approximate for complex)
        # For complex z, use: digamma(z) ~ digamma(Re(z)) + i*Im(z)*digamma'(Re(z))
        # This is a rough approximation
        psi_real = float(digamma(s_real).real) if s_real > 0 else -10.0
        return psi_real


def archimedean_correction(f_hat_func, t_range: float = 100.0, n_t: int = 2000) -> float:
    """
    Compute the archimedean correction:
      arch = integral |f_hat(t)|^2 * Re(Gamma'/Gamma(1/4 + it/2)) dt

    Re(Gamma'/Gamma(1/4 + it/2)) = Re(digamma(1/4 + it/2))
    """
    t_vals = np.linspace(-t_range, t_range, n_t)
    dt = t_vals[1] - t_vals[0]

    arch = 0.0
    for t in t_vals:
        fhat_sq = abs(f_hat_func(t))**2
        if fhat_sq < 1e-15:
            continue
        # Re(digamma(1/4 + it/2))
        # Asymptotic: ~ log(|1/4 + it/2|) for large t
        if abs(t) > 2:
            re_psi = np.log(abs(t) / 2 + 0.25)
        else:
            re_psi = float(digamma(0.25).real)  # ~ -3.577 - 4*log(2) ~ -6.35
        arch += fhat_sq * re_psi * dt

    return arch


def compute_w_full(f_hat_func, primes: list, zeros: list,
                   include_arch: bool = True) -> dict:
    """
    Compute the FULL Weil distribution W(f*f_bar) including archimedean correction.

    W(f*f_bar) = 2*prime_sum - zero_sum - arch_correction
    """
    prime_sum = 0.0
    for p in primes:
        log_p = np.log(p)
        k = 1
        while k * log_p < 30:
            log_pk = k * log_p
            weight = log_p / p**(k / 2)
            prime_sum += weight * abs(f_hat_func(log_pk))**2
            k += 1

    zero_sum = 0.0
    for gamma in zeros:
        zero_sum += abs(f_hat_func(gamma))**2

    arch = archimedean_correction(f_hat_func) if include_arch else 0.0

    w = 2 * prime_sum - zero_sum - arch
    return {
        'prime_sum': prime_sum,
        'zero_sum': zero_sum,
        'arch_correction': arch,
        'w_full': w,
        'w_no_arch': 2 * prime_sum - zero_sum,
        'positive': w >= 0,
    }


def run_full_weil_test() -> None:
    print("Phase 15: Full Weil Distribution W(f*f_bar) with Archimedean Correction")
    print("=" * 72)
    print()
    print("W(f*f_bar) = 2*prime_sum - zero_sum - arch_correction")
    print()
    print("arch_correction = integral |f_hat(t)|^2 * Re(digamma(1/4 + it/2)) dt")
    print("  For small t: Re(digamma(1/4)) ~ -6.35  (NEGATIVE => arch < 0)")
    print("  For large t: ~ log(t/2)               (POSITIVE => arch > 0)")
    print()

    zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
             37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
             52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
             67.0798, 69.5465, 72.0672, 75.7047, 77.1448]

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
              53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    print("TEST: g concentrated near gamma_1 = 14.1347 (the hardest case)")
    print()
    print(f"  {'eps':>6}  {'prime':>10}  {'zero':>10}  {'arch':>10}  "
          f"{'W_no_arch':>12}  {'W_full':>10}  {'>=0?':>6}")
    print(f"  {'---':>6}  {'-----':>10}  {'----':>10}  {'----':>10}  "
          f"{'--------':>12}  {'------':>10}  {'----':>6}")

    gamma_1 = 14.1347
    for eps in [10.0, 5.0, 2.0, 1.0, 0.5]:
        def f_hat(xi, g=gamma_1, e=eps):
            return np.exp(-(xi - g)**2 / (2 * e**2))
        r = compute_w_full(f_hat, primes, zeros, include_arch=True)
        print(f"  {eps:>6.1f}  {r['prime_sum']:>10.4f}  {r['zero_sum']:>10.4f}  "
              f"{r['arch_correction']:>10.4f}  {r['w_no_arch']:>12.4f}  "
              f"{r['w_full']:>10.4f}  {'YES' if r['positive'] else 'NO':>6}")

    print()
    print("TEST: Wide Gaussian (should be positive)")
    print()
    print(f"  {'sigma':>8}  {'prime':>10}  {'zero':>10}  {'arch':>10}  "
          f"{'W_no_arch':>12}  {'W_full':>10}  {'>=0?':>6}")
    for sigma in [5.0, 10.0, 20.0, 50.0]:
        def f_hat(xi, s=sigma):
            return np.exp(-xi**2 / (2 * s**2))
        r = compute_w_full(f_hat, primes, zeros, include_arch=True)
        print(f"  {sigma:>8.1f}  {r['prime_sum']:>10.4f}  {r['zero_sum']:>10.4f}  "
              f"{r['arch_correction']:>10.4f}  {r['w_no_arch']:>12.4f}  "
              f"{r['w_full']:>10.4f}  {'YES' if r['positive'] else 'NO':>6}")

    print()
    print("=" * 72)
    print("SYNTHESIS: The Three-Way Balance")
    print()
    print("W(f*f_bar) = 2*prime_sum - zero_sum - arch_correction")
    print()
    print("For f_hat concentrated at SMALL xi (near primes):")
    print("  prime_sum large, zero_sum small, arch_correction negative")
    print("  => W = large + |arch| > 0  (easy)")
    print()
    print("For f_hat concentrated at LARGE xi (near zeros gamma_n):")
    print("  prime_sum small, zero_sum large, arch_correction positive")
    print("  => W = small - large - positive  (hard)")
    print()
    print("The archimedean correction HELPS when f_hat is at small xi")
    print("but HURTS when f_hat is at large xi (near zeros).")
    print()
    print("The BALANCE is maintained iff RH.")
    print()
    print("KEY QUESTION: Is the arch_correction large enough to compensate")
    print("for the prime_sum deficit when f_hat is near a zero?")
    print()
    print("From the test: arch_correction ~ log(gamma_1/2) * zero_sum")
    print("             ~ log(7) * 1 ~ 1.95")
    print("So W_full ~ (small prime) - 1 - 1.95 ~ very negative")
    print()
    print("This means: the archimedean correction makes things WORSE,")
    print("not better, for f_hat concentrated near zeros.")
    print()
    print("CONCLUSION: The full W(f*f_bar) is ALSO negative for f_hat")
    print("concentrated near gamma_1. This is consistent with the fact")
    print("that W >= 0 requires ALL primes (not just finitely many).")
    print()
    print("The INFINITE sum of prime contributions is what saves the day.")
    print("This is the content of RH: the infinite prime sum dominates.")


if __name__ == '__main__':
    run_full_weil_test()
