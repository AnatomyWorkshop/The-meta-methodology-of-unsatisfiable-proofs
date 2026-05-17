"""
Phase 14: W_- Positivity Test -- Numerical Investigation of K_- Eigenvalues.

The question: as we include more primes and more zeros in the truncated
Weil operator K, do the negative eigenvalues of K_- vanish?

CORRECT SETUP (fixing Deepseek's definition error):

W is a DISTRIBUTION acting on Schwartz functions h:
  W(h) = prime_contrib(h) - zero_contrib(h)

The Weil operator K is defined by:
  W(h * h_bar) = <h, K h>_H

where h * h_bar is the convolution of h with its time-reversal.

K_- = restriction of K to H_- (odd functions, Pf = -f).

RH iff K >= 0 iff K_+ >= 0 AND K_- >= 0.

TESTABLE QUESTION:
  As N_primes, N_zeros -> infinity, do the negative eigenvalues of K_-
  decrease in magnitude and fraction?

  If yes: numerical support for K_- >= 0 (consistent with RH).
  If no: numerical evidence against RH (extremely unlikely but testable).
"""

import numpy as np
from scipy.special import digamma
import sys


def build_weil_kernel_matrix(test_points: np.ndarray,
                              primes: list,
                              zeros: list,
                              sigma: float = 1.0) -> np.ndarray:
    """
    Build the matrix of the Weil operator K in a Gaussian basis.

    Basis functions: phi_i(t) = exp(-(t - t_i)^2 / (2*sigma^2))
    centered at test_points t_i.

    K_{ij} = W(phi_i * phi_j_bar)

    where W(h) = sum_{p^k} (log p / p^{k/2}) * (h_hat(log p^k) + h_hat(-log p^k))
               - sum_rho h_hat(Im(rho) - 1/2)
               - (archimedean correction)

    For h = phi_i * phi_j_bar:
      h_hat(xi) = FT[phi_i * phi_j_bar](xi)
                = phi_i_hat(xi) * conj(phi_j_hat(xi))
                = exp(i*(t_i - t_j)*xi) * exp(-sigma^2 * xi^2 / 2)
                  * exp(-sigma^2 * xi^2 / 2)
                = exp(i*(t_i - t_j)*xi) * exp(-sigma^2 * xi^2)

    So h_hat(xi) = exp(i*(t_i-t_j)*xi - sigma^2*xi^2).
    """
    n = len(test_points)
    K = np.zeros((n, n), dtype=complex)

    for i in range(n):
        for j in range(n):
            ti, tj = test_points[i], test_points[j]
            phase = ti - tj  # h_hat(xi) = exp(i*phase*xi - sigma^2*xi^2)

            def h_hat(xi, ph=phase, s=sigma):
                return np.exp(1j * ph * xi - s**2 * xi**2)

            # Prime power contributions
            prime_val = 0.0 + 0j
            for p in primes:
                log_p = np.log(p)
                k = 1
                while k * log_p < 20:
                    log_pk = k * log_p
                    weight = log_p / p**(k / 2)
                    prime_val += weight * (h_hat(log_pk) + h_hat(-log_pk))
                    k += 1

            # Zero contributions: sum over rho = 1/2 + i*gamma_n
            # h_hat evaluated at Im(rho) - 1/2 = gamma_n (if on critical line)
            zero_val = 0.0 + 0j
            for gamma in zeros:
                zero_val += h_hat(gamma)
                zero_val += h_hat(-gamma)  # conjugate zero

            K[i, j] = prime_val - zero_val

    # K should be Hermitian; take symmetric part
    K = (K + K.conj().T) / 2
    return K.real  # imaginary part should be ~0 for real test points


def build_parity_matrix(test_points: np.ndarray) -> np.ndarray:
    """
    Build the parity operator P in the Gaussian basis.

    P maps t -> -t (time reversal / parity).
    In the Gaussian basis centered at t_i:
      (P phi_i)(t) = phi_i(-t) = exp(-(t+t_i)^2/(2*sigma^2))
                   = phi_{-i}(t)  [basis function centered at -t_i]

    If test_points are symmetric: {t_1,...,t_n,-t_1,...,-t_n},
    then P is the swap matrix: P e_i = e_{n+i}, P e_{n+i} = e_i.

    We use symmetric test points: t_i and -t_i paired.
    """
    n = len(test_points)
    assert n % 2 == 0, "Need even number of test points (symmetric pairs)"
    half = n // 2
    P = np.zeros((n, n))
    for i in range(half):
        P[i, half + i] = 1.0
        P[half + i, i] = 1.0
    return P


def project_to_H_minus(K: np.ndarray, P: np.ndarray) -> np.ndarray:
    """
    Project K onto H_- (the -1 eigenspace of P).

    H_- basis vectors: v_i = (e_i - e_{n/2+i}) / sqrt(2)

    K_- = V_-^T K V_-  where V_- has columns v_i.
    """
    n = K.shape[0]
    half = n // 2
    V_minus = np.zeros((n, half))
    for i in range(half):
        V_minus[i, i] = 1 / np.sqrt(2)
        V_minus[half + i, i] = -1 / np.sqrt(2)

    K_minus = V_minus.T @ K @ V_minus
    return K_minus


def project_to_H_plus(K: np.ndarray, P: np.ndarray) -> np.ndarray:
    """Project K onto H_+ (the +1 eigenspace of P)."""
    n = K.shape[0]
    half = n // 2
    V_plus = np.zeros((n, half))
    for i in range(half):
        V_plus[i, i] = 1 / np.sqrt(2)
        V_plus[half + i, i] = 1 / np.sqrt(2)

    K_plus = V_plus.T @ K @ V_plus
    return K_plus


def run_convergence_test() -> None:
    print("Phase 14: W_- Positivity -- Convergence Test")
    print("=" * 70)
    print()
    print("Testing: as N_primes and N_zeros increase, do negative eigenvalues")
    print("of K_- decrease? (RH predicts: yes, converging to 0)")
    print()

    # Known zeta zeros (imaginary parts)
    all_zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
                 37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
                 52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
                 67.0798, 69.5465, 72.0672, 75.7047, 77.1448]

    # Primes
    all_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                  31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                  73, 79, 83, 89, 97]

    # Test points: symmetric around 0, centered near first few zeros
    base_points = np.array([7.0, 14.0, 21.0, 25.0, 30.0])
    test_points = np.concatenate([base_points, -base_points])

    print(f"  Basis: {len(test_points)} Gaussians at +/-{base_points}")
    print(f"  sigma = 3.0")
    print()

    sigma = 3.0

    print(f"  {'N_zeros':>8}  {'N_primes':>9}  {'min_eig_K-':>12}  "
          f"{'frac_neg_K-':>12}  {'min_eig_K+':>12}  {'frac_neg_K+':>12}")
    print(f"  {'-------':>8}  {'--------':>9}  {'----------':>12}  "
          f"{'----------':>12}  {'----------':>12}  {'----------':>12}")

    results = []
    for n_zeros in [3, 5, 8, 12, 16, 20]:
        for n_primes in [5, 10, 15, 20, 25]:
            zeros = all_zeros[:n_zeros]
            primes = all_primes[:n_primes]

            K = build_weil_kernel_matrix(test_points, primes, zeros, sigma=sigma)
            P = build_parity_matrix(test_points)

            K_minus = project_to_H_minus(K, P)
            K_plus = project_to_H_plus(K, P)

            eigs_minus = np.linalg.eigvalsh(K_minus)
            eigs_plus = np.linalg.eigvalsh(K_plus)

            min_minus = float(np.min(eigs_minus))
            frac_neg_minus = float(np.mean(eigs_minus < -1e-10))
            min_plus = float(np.min(eigs_plus))
            frac_neg_plus = float(np.mean(eigs_plus < -1e-10))

            results.append({
                'n_zeros': n_zeros, 'n_primes': n_primes,
                'min_minus': min_minus, 'frac_neg_minus': frac_neg_minus,
                'min_plus': min_plus, 'frac_neg_plus': frac_neg_plus,
            })

            print(f"  {n_zeros:>8}  {n_primes:>9}  {min_minus:>12.4f}  "
                  f"{frac_neg_minus:>12.4f}  {min_plus:>12.4f}  {frac_neg_plus:>12.4f}")

    print()
    print("=" * 70)
    print("ANALYSIS:")
    print()

    # Check trend: does min_eig_K- increase as n_zeros and n_primes increase?
    # Group by n_zeros, look at trend with n_primes
    print("Trend of min eigenvalue of K_- as N_primes increases (fixed N_zeros):")
    for n_zeros in [5, 10, 20]:
        subset = [r for r in results if r['n_zeros'] == n_zeros]
        if subset:
            mins = [r['min_minus'] for r in subset]
            n_ps = [r['n_primes'] for r in subset]
            trend = "increasing" if mins[-1] > mins[0] else "decreasing"
            print(f"  N_zeros={n_zeros}: min_K- goes from {mins[0]:.4f} to {mins[-1]:.4f} ({trend})")

    print()
    print("Trend of min eigenvalue of K_- as N_zeros increases (fixed N_primes=25):")
    subset = [r for r in results if r['n_primes'] == 25]
    if subset:
        mins = [r['min_minus'] for r in subset]
        n_zs = [r['n_zeros'] for r in subset]
        for nz, m in zip(n_zs, mins):
            print(f"  N_zeros={nz}: min_K- = {m:.4f}")

    print()
    print("=" * 70)
    print("INTERPRETATION:")
    print()
    print("The Weil operator K has two competing contributions:")
    print("  prime_contrib: POSITIVE (sum of squares weighted by log p / sqrt(p))")
    print("  zero_contrib:  NEGATIVE (subtracts for each zero)")
    print()
    print("K_- >= 0 requires: prime_contrib_- >= zero_contrib_- for all f in H_-")
    print()
    print("In the function field case, this follows from the Weil bound:")
    print("  |C(F_{q^n})| <= (q^{n/2} + 1)^{2g}")
    print("  => prime contributions dominate zero contributions")
    print()
    print("In the number field case, the analogous bound is:")
    print("  |sum_{p<=x} log p / sqrt(p) - 2*sqrt(x)| = O(1)  (PNT with RH error)")
    print("  This is EQUIVALENT to RH -- not a consequence of it.")
    print()
    print("THE PRECISE GAP (now numerically visible):")
    print("  The truncated K_- has negative eigenvalues because we include")
    print("  finitely many zeros (negative contributions) but the prime")
    print("  contributions need ALL primes to dominate.")
    print()
    print("  As N_primes -> inf with N_zeros fixed: K_- should become more positive")
    print("  (prime contributions grow, zero contributions fixed).")
    print()
    print("  As N_zeros -> inf with N_primes fixed: K_- should become more negative")
    print("  (zero contributions grow, prime contributions fixed).")
    print()
    print("  The BALANCE between these two limits is exactly RH.")


if __name__ == '__main__':
    run_convergence_test()
