"""
Phase 14c: W_- Positivity -- Wide Support Test Functions.

Problem with Phase 14b: Gaussian test functions with sigma=1,2 have
f_hat(gamma_n) ~ exp(-sigma^2 * gamma_n^2 / 2) which is ~0 for gamma_n~14.
The zero contributions vanish, making the test trivial.

Fix: use test functions with WIDE support in frequency space,
so that f_hat is non-negligible at the zeta zeros gamma_n ~ 14-80.

Strategy: use f_hat directly as a compactly supported function in
frequency space, then W_-(f*f_bar) = 2*(prime_sum - zero_sum) where
both sums are computed from f_hat evaluated at the relevant points.

For an odd function f (Pf = -f, i.e., f(-t) = -f(t)):
  f_hat(xi) is purely imaginary and odd: f_hat(-xi) = -f_hat(xi)
  |f_hat(xi)|^2 = |f_hat(-xi)|^2

So we can parametrize by g(xi) = -i * f_hat(xi) (real, odd function of xi).

W_-(f*f_bar) = 2 * [sum_{p^k} (log p / p^{k/2}) * g(log p^k)^2
                   - sum_{gamma_n > 0} g(gamma_n)^2]

This is the CORRECT form. Now we need g to be non-negligible at
both log p^k (small: log 2 ~ 0.69, log 3 ~ 1.1, ...) AND
gamma_n (large: 14.1, 21.0, ...).

The challenge: prime contributions are at log p^k ~ 0.7 to 5,
while zero contributions are at gamma_n ~ 14 to 80.
A function g that is large at BOTH scales will have:
  prime_sum ~ sum_{p^k} (log p / p^{k/2}) * g(log p^k)^2
  zero_sum  ~ sum_n g(gamma_n)^2

The question is whether prime_sum >= zero_sum.

Note: the weights log p / p^{k/2} are DECREASING (larger primes get
smaller weight). The zero contributions have weight 1 each.

This is the CORE TENSION: primes are weighted by log p / sqrt(p) ~ 1/sqrt(p),
while zeros are unweighted. As we go to larger scales, zeros accumulate
faster than prime contributions.

The Weil explicit formula says this balance is EXACTLY maintained (= RH).
"""

import numpy as np


def compute_w_minus_from_g(g_func, primes: list, zeros: list,
                            prime_cutoff: float = 30.0) -> dict:
    """
    Compute W_-(f*f_bar) where g(xi) = -i * f_hat(xi) is real and odd.

    W_-(f*f_bar) = 2 * [prime_sum - zero_sum]
    prime_sum = sum_{p^k, k*log(p) < cutoff} (log p / p^{k/2}) * g(log p^k)^2
    zero_sum  = sum_{gamma_n in zeros} g(gamma_n)^2
    """
    prime_sum = 0.0
    prime_details = []
    for p in primes:
        log_p = np.log(p)
        k = 1
        while k * log_p < prime_cutoff:
            log_pk = k * log_p
            weight = log_p / p**(k / 2)
            val = g_func(log_pk)**2
            prime_sum += weight * val
            if val > 1e-10:
                prime_details.append((p, k, log_pk, weight, val, weight * val))
            k += 1

    zero_sum = 0.0
    zero_details = []
    for gamma in zeros:
        val = g_func(gamma)**2
        zero_sum += val
        if val > 1e-10:
            zero_details.append((gamma, val))

    w_minus = 2 * (prime_sum - zero_sum)
    return {
        'prime_sum': prime_sum,
        'zero_sum': zero_sum,
        'w_minus': w_minus,
        'positive': w_minus >= 0,
        'ratio': prime_sum / zero_sum if zero_sum > 1e-15 else float('inf'),
        'prime_details': prime_details,
        'zero_details': zero_details,
    }


def run_wide_support_test() -> None:
    print("Phase 14c: W_- Positivity -- Wide Support Test Functions")
    print("=" * 70)
    print()

    zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
             37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
             52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
             67.0798, 69.5465, 72.0672, 75.7047, 77.1448]

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
              53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    print("KEY INSIGHT: prime contributions are at xi ~ 0.7-5 (log p^k),")
    print("             zero contributions are at xi ~ 14-80 (gamma_n).")
    print("These are DIFFERENT scales. A test function g(xi) that is")
    print("large at BOTH scales is needed to make the test non-trivial.")
    print()

    # Test 1: g(xi) = 1 for all xi (constant -- not in L^2, but illustrative)
    # This gives: prime_sum = sum (log p / p^{k/2}), zero_sum = N_zeros
    print("TEST 1: g(xi) = 1 (constant, illustrative)")
    def g_const(xi): return 1.0
    r = compute_w_minus_from_g(g_const, primes, zeros)
    print(f"  prime_sum = {r['prime_sum']:.4f}")
    print(f"  zero_sum  = {r['zero_sum']:.4f}  (= N_zeros = {len(zeros)})")
    print(f"  W_-       = {r['w_minus']:.4f}  ({'POSITIVE' if r['positive'] else 'NEGATIVE'})")
    print(f"  ratio     = {r['ratio']:.4f}")
    print()

    # Test 2: g(xi) = exp(-xi^2 / (2*sigma^2)) with large sigma
    print("TEST 2: g(xi) = exp(-xi^2 / (2*sigma^2)) -- wide Gaussian")
    print(f"  {'sigma':>8}  {'prime_sum':>12}  {'zero_sum':>12}  {'W_-':>12}  {'ratio':>8}  {'>=0?':>6}")
    for sigma in [5.0, 10.0, 20.0, 50.0, 100.0]:
        def g_gauss(xi, s=sigma): return np.exp(-xi**2 / (2 * s**2))
        r = compute_w_minus_from_g(g_gauss, primes, zeros)
        print(f"  {sigma:>8.1f}  {r['prime_sum']:>12.6f}  {r['zero_sum']:>12.6f}  "
              f"{r['w_minus']:>12.6f}  {r['ratio']:>8.4f}  {'YES' if r['positive'] else 'NO':>6}")
    print()

    # Test 3: g(xi) = sin(a*xi) / xi -- sinc-like, wide support
    print("TEST 3: g(xi) = sin(a*xi) / (xi+eps) -- oscillating wide support")
    print(f"  {'a':>8}  {'prime_sum':>12}  {'zero_sum':>12}  {'W_-':>12}  {'ratio':>8}  {'>=0?':>6}")
    for a in [1.0, 2.0, 5.0, 10.0, 20.0]:
        def g_sinc(xi, aa=a): return np.sin(aa * xi) / (xi + 1e-10) if abs(xi) > 1e-10 else aa
        r = compute_w_minus_from_g(g_sinc, primes, zeros)
        print(f"  {a:>8.1f}  {r['prime_sum']:>12.6f}  {r['zero_sum']:>12.6f}  "
              f"{r['w_minus']:>12.6f}  {r['ratio']:>8.4f}  {'YES' if r['positive'] else 'NO':>6}")
    print()

    # Test 4: g(xi) = 1 / (1 + (xi/scale)^2) -- Lorentzian, heavy tail
    print("TEST 4: g(xi) = 1 / (1 + (xi/scale)^2) -- Lorentzian")
    print(f"  {'scale':>8}  {'prime_sum':>12}  {'zero_sum':>12}  {'W_-':>12}  {'ratio':>8}  {'>=0?':>6}")
    for scale in [1.0, 5.0, 10.0, 20.0, 50.0]:
        def g_lor(xi, s=scale): return 1.0 / (1 + (xi / s)**2)
        r = compute_w_minus_from_g(g_lor, primes, zeros)
        print(f"  {scale:>8.1f}  {r['prime_sum']:>12.6f}  {r['zero_sum']:>12.6f}  "
              f"{r['w_minus']:>12.6f}  {r['ratio']:>8.4f}  {'YES' if r['positive'] else 'NO':>6}")
    print()

    # Test 5: The CRITICAL test -- g concentrated near a zero
    # If g(xi) = delta(xi - gamma_1), then prime_sum ~ 0, zero_sum ~ 1
    # => W_- < 0. But delta is not in L^2.
    # Approximate: g(xi) = exp(-(xi - gamma_1)^2 / (2*eps^2)) with small eps
    print("TEST 5: g concentrated near first zero gamma_1 = 14.1347")
    print("  (This is the HARDEST test -- zero contribution dominates)")
    print(f"  {'eps':>8}  {'prime_sum':>12}  {'zero_sum':>12}  {'W_-':>12}  {'ratio':>8}  {'>=0?':>6}")
    gamma_1 = 14.1347
    for eps in [5.0, 2.0, 1.0, 0.5, 0.2]:
        def g_near_zero(xi, g=gamma_1, e=eps):
            return np.exp(-(xi - g)**2 / (2 * e**2))
        r = compute_w_minus_from_g(g_near_zero, primes, zeros)
        print(f"  {eps:>8.2f}  {r['prime_sum']:>12.6f}  {r['zero_sum']:>12.6f}  "
              f"{r['w_minus']:>12.6f}  {r['ratio']:>8.4f}  {'YES' if r['positive'] else 'NO':>6}")
    print()

    print("=" * 70)
    print("CRITICAL ANALYSIS:")
    print()
    print("Test 5 is the key: when g is concentrated near a zero gamma_n,")
    print("  zero_sum ~ g(gamma_n)^2 ~ 1")
    print("  prime_sum ~ sum_{p^k near gamma_n} (log p / p^{k/2}) * g(log p^k)^2")
    print()
    print("For gamma_1 = 14.1347: the nearest prime power is p^k = e^14.1 ~ 1.3e6")
    print("  = 2^20 ~ 1e6, log(2^20) = 20*log(2) = 13.86 (close!)")
    print("  weight = log(2) / 2^10 = 0.693 / 1024 ~ 0.00068")
    print()
    print("So prime_sum near gamma_1 is TINY (weight ~ 1/1000),")
    print("while zero_sum ~ 1.")
    print()
    print("This means: for g concentrated near gamma_1, W_- < 0 !")
    print()
    print("BUT WAIT: this is a TRUNCATION artifact.")
    print("The full prime sum includes ALL prime powers, not just those near gamma_1.")
    print("The Weil explicit formula says the FULL sum (all primes) balances the zeros.")
    print()
    print("This is the PRECISE statement of RH in this language:")
    print("  For any g, sum_{ALL p^k} (log p / p^{k/2}) * g(log p^k)^2")
    print("           >= sum_{ALL gamma_n} g(gamma_n)^2")
    print()
    print("The left side is a sum over a DENSE set (log p^k are dense in R+).")
    print("The right side is a sum over a SPARSE set (gamma_n ~ n*log(n)/2pi).")
    print()
    print("The inequality holds iff the prime powers are 'spread out enough'")
    print("to dominate the zeros -- which is exactly the prime number theorem")
    print("with the RH error bound.")


if __name__ == '__main__':
    run_wide_support_test()
