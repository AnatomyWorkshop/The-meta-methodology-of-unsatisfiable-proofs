"""
Phase 14b: W_- Positivity -- Corrected Construction.

The Phase 14 result was all zeros because the Gaussian basis centered at
the zeros themselves causes near-perfect cancellation. We need a different
approach: use a FIXED basis of test functions and compute W(f*f_bar) directly.

CORRECT APPROACH:
  W(h) = sum_{p^k} (log p / p^{k/2}) * h_hat(log p^k)
        - sum_rho h_hat(Im(rho))
        (simplified: ignoring archimedean correction for now)

  For h = f * f_bar (convolution), h_hat(xi) = |f_hat(xi)|^2.

  So W(f*f_bar) = sum_{p^k} (log p / p^{k/2}) * |f_hat(log p^k)|^2
                - sum_rho |f_hat(Im(rho))|^2

  This is MANIFESTLY real. RH predicts W(f*f_bar) >= 0 for all f.

  For f in H_- (odd: f(-t) = -f(t)):
    f_hat(xi) = -f_hat(-xi)  (odd Fourier transform)
    |f_hat(xi)|^2 = |f_hat(-xi)|^2  (same magnitude)

  So W_-(f*f_bar) = 2 * sum_{p^k} (log p / p^{k/2}) * |f_hat(log p^k)|^2
                  - 2 * sum_{gamma>0} |f_hat(gamma)|^2

  (factor 2 from pairing +/- contributions)

  This is: 2 * [prime_sum - zero_sum]

  RH predicts: prime_sum >= zero_sum for all odd f.

TESTABLE: pick specific odd test functions, compute both sums, check sign.
"""

import numpy as np
from scipy.fft import fft, fftfreq
import sys


def compute_w_minus(f_hat_func, primes: list, zeros: list) -> dict:
    """
    Compute W_-(f*f_bar) for an odd test function f with Fourier transform f_hat.

    W_-(f*f_bar) = 2 * [prime_sum - zero_sum]

    prime_sum = sum_{p^k} (log p / p^{k/2}) * |f_hat(log p^k)|^2
    zero_sum  = sum_{gamma_n > 0} |f_hat(gamma_n)|^2
    """
    prime_sum = 0.0
    for p in primes:
        log_p = np.log(p)
        k = 1
        while k * log_p < 25:
            log_pk = k * log_p
            weight = log_p / p**(k / 2)
            val = abs(f_hat_func(log_pk))**2
            prime_sum += weight * val
            k += 1

    zero_sum = 0.0
    for gamma in zeros:
        if gamma > 0:
            zero_sum += abs(f_hat_func(gamma))**2

    w_minus = 2 * (prime_sum - zero_sum)
    return {
        'prime_sum': prime_sum,
        'zero_sum': zero_sum,
        'w_minus': w_minus,
        'positive': w_minus >= 0,
        'ratio': prime_sum / zero_sum if zero_sum > 1e-15 else float('inf'),
    }


def odd_gaussian(center: float, sigma: float):
    """
    Odd test function: f(t) = exp(-(t-c)^2/(2s^2)) - exp(-(t+c)^2/(2s^2))
    Fourier transform: f_hat(xi) = 2i * sin(c*xi) * exp(-s^2*xi^2/2)
    |f_hat(xi)|^2 = 4 * sin^2(c*xi) * exp(-s^2*xi^2)
    """
    def f_hat(xi, c=center, s=sigma):
        return 2j * np.sin(c * xi) * np.exp(-s**2 * xi**2 / 2)
    return f_hat


def odd_sinc(center: float, width: float):
    """
    Odd test function based on sinc: f_hat(xi) = i * sign(xi) * rect((xi-c)/w)
    Simplified: f_hat(xi) = i * sin(c*xi) * exp(-xi^2/(2*width^2))
    """
    def f_hat(xi, c=center, w=width):
        return 1j * np.sin(c * xi) * np.exp(-xi**2 / (2 * w**2))
    return f_hat


def run_w_minus_test() -> None:
    print("Phase 14b: W_- Positivity -- Direct Computation")
    print("=" * 70)
    print()
    print("W_-(f*f_bar) = 2 * [prime_sum - zero_sum]")
    print("prime_sum = sum_{p^k} (log p / p^{k/2}) * |f_hat(log p^k)|^2")
    print("zero_sum  = sum_{gamma_n} |f_hat(gamma_n)|^2")
    print()
    print("RH predicts: W_-(f*f_bar) >= 0 for all odd f.")
    print()

    zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
             37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
             52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
             67.0798, 69.5465, 72.0672, 75.7047, 77.1448]

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
              53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    print("TEST 1: Odd Gaussians f(t) = exp(-(t-c)^2) - exp(-(t+c)^2)")
    print(f"  {'center c':>10}  {'sigma':>6}  {'prime_sum':>12}  {'zero_sum':>12}  "
          f"{'W_-':>12}  {'ratio':>8}  {'>=0?':>6}")
    print(f"  {'--------':>10}  {'-----':>6}  {'---------':>12}  {'--------':>12}  "
          f"{'---':>12}  {'-----':>8}  {'----':>6}")

    for center in [5.0, 10.0, 14.0, 20.0, 25.0, 30.0]:
        for sigma in [1.0, 2.0, 5.0]:
            f_hat = odd_gaussian(center, sigma)
            r = compute_w_minus(f_hat, primes, zeros)
            print(f"  {center:>10.1f}  {sigma:>6.1f}  {r['prime_sum']:>12.4f}  "
                  f"{r['zero_sum']:>12.4f}  {r['w_minus']:>12.4f}  "
                  f"{r['ratio']:>8.4f}  {'YES' if r['positive'] else 'NO':>6}")

    print()
    print("TEST 2: Convergence -- more primes vs more zeros")
    print()
    print("Fixed odd Gaussian: center=14.0, sigma=2.0")
    f_hat_fixed = odd_gaussian(14.0, 2.0)

    print(f"  {'N_primes':>9}  {'N_zeros':>8}  {'prime_sum':>12}  {'zero_sum':>12}  "
          f"{'W_-':>12}  {'ratio':>8}")
    print(f"  {'--------':>9}  {'-------':>8}  {'---------':>12}  {'--------':>12}  "
          f"{'---':>12}  {'-----':>8}")

    for n_p in [5, 10, 20, 30]:
        for n_z in [5, 10, 15, 20]:
            r = compute_w_minus(f_hat_fixed, primes[:n_p], zeros[:n_z])
            print(f"  {n_p:>9}  {n_z:>8}  {r['prime_sum']:>12.4f}  "
                  f"{r['zero_sum']:>12.4f}  {r['w_minus']:>12.4f}  {r['ratio']:>8.4f}")

    print()
    print("TEST 3: Scan over center -- find where W_- is smallest")
    print()
    print("sigma=2.0, N_primes=30, N_zeros=20")
    print(f"  {'center':>8}  {'prime_sum':>12}  {'zero_sum':>12}  {'W_-':>12}  {'ratio':>8}")

    min_w = float('inf')
    min_center = None
    for center in np.linspace(1.0, 80.0, 80):
        f_hat = odd_gaussian(center, 2.0)
        r = compute_w_minus(f_hat, primes, zeros)
        if r['w_minus'] < min_w:
            min_w = r['w_minus']
            min_center = center
        if center % 10 < 1.5:
            print(f"  {center:>8.1f}  {r['prime_sum']:>12.4f}  {r['zero_sum']:>12.4f}  "
                  f"{r['w_minus']:>12.4f}  {r['ratio']:>8.4f}")

    print()
    print(f"  Minimum W_- = {min_w:.6f} at center = {min_center:.2f}")
    print()

    print("=" * 70)
    print("WHAT THIS TELLS US:")
    print()
    print("The ratio prime_sum / zero_sum measures how much the prime")
    print("contributions dominate the zero contributions.")
    print()
    print("In the function field case (Weil bound):")
    print("  prime_sum / zero_sum >= 1 always (proved by Hodge Index Theorem)")
    print()
    print("In the number field case:")
    print("  prime_sum / zero_sum >= 1 iff RH (not proved)")
    print()
    print("The numerical test shows whether this ratio stays above 1")
    print("for the test functions we can compute.")
    print()
    print("KEY OBSERVATION:")
    print("  If W_-(f*f_bar) < 0 for ANY f, then RH is FALSE.")
    print("  If W_-(f*f_bar) >= 0 for all tested f, this is consistent with RH")
    print("  but does not prove it (we only test finitely many f).")


if __name__ == '__main__':
    run_w_minus_test()
