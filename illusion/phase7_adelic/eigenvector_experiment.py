"""
Eigenvector experiment: do H_n eigenvectors converge to trivial Hecke character?

The trivial Hecke character phi_0 on C_Q = A_Q^x/Q^x is phi_0(x) = |x|^{1/2}.
In the finite-dimensional Dirichlet basis on [0,L], this corresponds to the
constant function (the norm is quotiented out in H = L^2(C_Q)/V).

In the P-eigenbasis (block-diagonal construction from Phase 6):
- P = parity operator (index reversal)
- phi_0 is even under P (constant function is symmetric)
- So phi_0 projects entirely onto the P=+1 (even) sector

Experiment:
1. Re-run UCA optimizer for n=50 and n=100, saving eigenvectors
2. Compute overlap of each eigenvector with phi_0 (constant vector in even sector)
3. Check if overlap increases with n (convergence to trivial Hecke character)
4. Check orthogonality between eigenvectors (automorphic forms are orthogonal)

Also check: D commutes with Hecke operators T_p?
In the finite-dimensional approximation, T_p acts as multiplication by
the p-th Fourier coefficient. We check [H_n, T_p] numerically.
"""

import numpy as np
from scipy.optimize import minimize
from scipy.linalg import eigh
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'phase6_rh'))


def zeta_zeros(n: int) -> np.ndarray:
    try:
        import mpmath
        mpmath.mp.dps = 25
        return np.array([float(mpmath.im(mpmath.zetazero(k))) for k in range(1, n+1)])
    except ImportError:
        return np.array([
            14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
            37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
            52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
            67.0798, 69.5465, 72.0672, 75.7047, 77.1448,
            79.3374, 82.9104, 84.7357, 87.4253, 88.8091,
            92.4919, 94.6513, 95.8706, 98.8312, 101.318,
        ])[:n]


# ---------------------------------------------------------------------------
# Rebuild UCA optimizer (self-contained, from Phase 6 logic)
# ---------------------------------------------------------------------------

def parity_operator(n: int) -> np.ndarray:
    P = np.zeros((n, n))
    for i in range(n):
        P[i, n - 1 - i] = 1.0
    return P


def build_berry_keating(n: int) -> np.ndarray:
    """Berry-Keating Hamiltonian in Dirichlet sin-basis."""
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            ni, nj = i + 1, j + 1
            if i == j:
                H[i, j] = 0.0
            elif (ni + nj) % 2 == 1:
                H[i, j] = -4.0 * ni * nj / (np.pi * (ni**2 - nj**2))
    return H


def affine_scale(H: np.ndarray, target_zeros: np.ndarray) -> np.ndarray:
    evals = np.sort(np.linalg.eigvalsh(H))
    src_min, src_max = evals[0], evals[-1]
    tgt_min, tgt_max = target_zeros[0], target_zeros[-1]
    if abs(src_max - src_min) < 1e-10:
        return H
    scale = (tgt_max - tgt_min) / (src_max - src_min)
    shift = tgt_min - scale * src_min
    return scale * H + shift * np.eye(len(H))


def parity_eigenbasis(n: int):
    P = parity_operator(n)
    evals, U = np.linalg.eigh(P)
    idx_plus = np.where(evals > 0)[0]
    idx_minus = np.where(evals < 0)[0]
    return U, idx_plus, idx_minus


def params_to_blocks(params, m_plus, m_minus):
    n_plus = m_plus * (m_plus + 1) // 2
    p_plus = params[:n_plus]
    p_minus = params[n_plus:]
    H_plus = np.zeros((m_plus, m_plus))
    idx = np.triu_indices(m_plus)
    H_plus[idx] = p_plus
    H_plus = H_plus + H_plus.T - np.diag(np.diag(H_plus))
    H_minus = np.zeros((m_minus, m_minus))
    idx2 = np.triu_indices(m_minus)
    H_minus[idx2] = p_minus
    H_minus = H_minus + H_minus.T - np.diag(np.diag(H_minus))
    return H_plus, H_minus


def blocks_to_H(H_plus, H_minus, U, idx_plus, idx_minus, n):
    H_block = np.zeros((n, n))
    for i, pi in enumerate(idx_plus):
        for j, pj in enumerate(idx_plus):
            H_block[pi, pj] = H_plus[i, j]
    for i, mi in enumerate(idx_minus):
        for j, mj in enumerate(idx_minus):
            H_block[mi, mj] = H_minus[i, j]
    return U @ H_block @ U.T


def optimize_uca(n: int, n_zeros: int = 30, reg: float = 1e-6,
                 max_iter: int = 600, verbose: bool = True):
    """Run UCA-constrained optimizer, return (H_opt, eigenvalues, eigenvectors)."""
    target = zeta_zeros(n_zeros)
    U, idx_plus, idx_minus = parity_eigenbasis(n)
    m_plus, m_minus = len(idx_plus), len(idx_minus)

    # Build starting point
    H_bk = build_berry_keating(n)
    H_bk_scaled = affine_scale(H_bk, target)
    P = parity_operator(n)
    delta = H_bk_scaled @ P - P @ H_bk_scaled
    V_defect = -delta @ P / 2.0
    H0 = H_bk_scaled + V_defect

    # Project to blocks
    H0_rot = U.T @ H0 @ U
    H0_plus = H0_rot[np.ix_(idx_plus, idx_plus)]
    H0_minus = H0_rot[np.ix_(idx_minus, idx_minus)]

    def blocks_to_params(Hp, Hm):
        p = np.concatenate([Hp[np.triu_indices(m_plus)],
                            Hm[np.triu_indices(m_minus)]])
        return p

    params0 = blocks_to_params(H0_plus, H0_minus)

    # Add small noise to escape flat regions (especially for large n)
    rng = np.random.default_rng(42)
    noise_scale = 0.01 * np.std(params0) if np.std(params0) > 0 else 0.01
    params0 = params0 + rng.normal(0, noise_scale, size=params0.shape)

    def loss_and_grad(params):
        Hp, Hm = params_to_blocks(params, m_plus, m_minus)
        evals_p, evecs_p = np.linalg.eigh(Hp)
        evals_m, evecs_m = np.linalg.eigh(Hm)
        all_evals = np.concatenate([evals_p, evals_m])
        sort_idx = np.argsort(all_evals)
        all_evals_sorted = all_evals[sort_idx]
        top_idx_global = sort_idx[-n_zeros:]
        top_evals = all_evals_sorted[-n_zeros:]
        diff = top_evals - target  # shape (n_zeros,)
        loss_val = float(np.sum(diff**2)) + reg * float(np.sum(params**2))

        # Analytical gradient via Hellmann-Feynman
        n_plus = m_plus * (m_plus + 1) // 2
        grad = 2.0 * reg * params.copy()

        for k_rank, k_global in enumerate(top_idx_global):
            coeff = 2.0 * diff[k_rank]
            if k_global < m_plus:
                # eigenvalue from plus block
                u = evecs_p[:, k_global]
                # gradient w.r.t. upper triangle of H_plus
                rows, cols = np.triu_indices(m_plus)
                g_block = np.where(rows == cols,
                                   u[rows] * u[cols],
                                   2.0 * u[rows] * u[cols])
                grad[:n_plus] += coeff * g_block
            else:
                # eigenvalue from minus block
                k_minus = k_global - m_plus
                u = evecs_m[:, k_minus]
                rows, cols = np.triu_indices(m_minus)
                g_block = np.where(rows == cols,
                                   u[rows] * u[cols],
                                   2.0 * u[rows] * u[cols])
                grad[n_plus:] += coeff * g_block

        return loss_val, grad

    if verbose:
        l0, _ = loss_and_grad(params0)
        print(f"  Initial RMSE: {np.sqrt(l0/n_zeros):.4f}")

    result = minimize(loss_and_grad, params0, method='L-BFGS-B', jac=True,
                      options={'maxiter': max_iter, 'ftol': 1e-15, 'gtol': 1e-10})

    Hp_opt, Hm_opt = params_to_blocks(result.x, m_plus, m_minus)
    H_opt = blocks_to_H(Hp_opt, Hm_opt, U, idx_plus, idx_minus, n)

    # Get eigenvalues AND eigenvectors
    evals, evecs = eigh(H_opt)  # evecs[:,i] is i-th eigenvector

    top_idx = np.argsort(evals)[-n_zeros:]
    top_evals = evals[top_idx]
    top_evecs = evecs[:, top_idx]  # shape (n, n_zeros)

    rmse = float(np.sqrt(np.mean((top_evals - target)**2)))
    defect = float(np.linalg.norm(H_opt @ P - P @ H_opt, 'fro'))

    if verbose:
        print(f"  RMSE={rmse:.5f}, defect={defect:.2e}, iters={result.nit}")

    return H_opt, top_evals, top_evecs, U, idx_plus, idx_minus


# ---------------------------------------------------------------------------
# Trivial Hecke character in finite-dimensional basis
# ---------------------------------------------------------------------------

def trivial_hecke_character(n: int, U: np.ndarray, idx_plus: np.ndarray) -> np.ndarray:
    """
    The trivial Hecke character phi_0 in the n-dimensional Dirichlet sin-basis.

    phi_0(x) = constant on C_Q (norm quotiented out).
    In the sin-basis phi_k(x) = sqrt(2/L)*sin(k*pi*x/L), the constant function
    has Fourier coefficients:
      <1, phi_k> = sqrt(2/L) * integral_0^L sin(k*pi*x/L) dx
                 = sqrt(2/L) * L/(k*pi) * (1 - cos(k*pi))
                 = sqrt(2/L) * 2L/(k*pi)  for k odd
                 = 0                       for k even

    So v_0[k-1] = 2*sqrt(2/L)*L/(k*pi) for k odd, 0 for k even.
    With L=1 (normalized): v_0[k-1] = 2*sqrt(2)/(k*pi) for k odd.

    phi_0 is even under parity (constant = symmetric), so it projects
    entirely onto the P=+1 (even) sector.
    """
    v_const = np.zeros(n)
    for k in range(1, n + 1):
        if k % 2 == 1:  # odd k only
            v_const[k - 1] = 2.0 * np.sqrt(2.0) / (k * np.pi)
    # Normalize
    norm = np.linalg.norm(v_const)
    if norm > 1e-10:
        v_const /= norm
    # Rotate to P-eigenbasis
    v_rot = U.T @ v_const
    # Project onto even sector
    v_even = np.zeros(n)
    v_even[idx_plus] = v_rot[idx_plus]
    norm2 = np.linalg.norm(v_even)
    if norm2 > 1e-10:
        v_even /= norm2
    return v_even


def hecke_operator_T2(n: int) -> np.ndarray:
    """
    Hecke operator T_2 in the Dirichlet sin-basis on [0, L].

    T_2 f(x) = (1/sqrt(2)) * [f(2x) + f(x/2)]  (symmetrized)

    In the sin-basis phi_k(x) = sqrt(2/L) sin(k*pi*x/L):
      T_2 phi_k = (1/sqrt(2)) * [phi_{2k} + (1/2)*phi_{k/2}]
    where phi_{k/2} = 0 if k is odd.

    Matrix element: (T_2)_{ij} = <phi_i | T_2 | phi_j>
    """
    T = np.zeros((n, n))
    for j in range(1, n + 1):
        # T_2 phi_j has component at 2j (if 2j <= n)
        if 2 * j <= n:
            T[2*j - 1, j - 1] += 1.0 / np.sqrt(2)
            T[j - 1, 2*j - 1] += 1.0 / np.sqrt(2)  # Hermitian
        # T_2 phi_j has component at j/2 (if j even)
        if j % 2 == 0:
            T[j//2 - 1, j - 1] += 1.0 / (2.0 * np.sqrt(2))
            T[j - 1, j//2 - 1] += 1.0 / (2.0 * np.sqrt(2))
    return T


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_eigenvector_experiment():
    print("Eigenvector Experiment: H_n -> trivial Hecke character")
    print("=" * 60)

    results = {}

    for n in [50, 100]:
        print(f"\n--- n={n} ---")
        max_iter = 800 if n <= 50 else 1200
        H_opt, top_evals, top_evecs, U, idx_plus, idx_minus = optimize_uca(
            n, n_zeros=30, reg=1e-6, max_iter=max_iter, verbose=True)

        # Trivial Hecke character
        v0 = trivial_hecke_character(n, U, idx_plus)

        # Overlap of each eigenvector with phi_0
        overlaps = np.abs(top_evecs.T @ v0)  # shape (30,)

        print(f"\n  Overlap |<v_k, phi_0>| for first 10 eigenvectors:")
        print(f"  {'k':>4}  {'gamma_k':>10}  {'overlap':>10}  {'overlap^2':>10}")
        target = zeta_zeros(30)
        for k in range(min(10, len(overlaps))):
            print(f"  {k+1:>4}  {target[k]:>10.4f}  {overlaps[k]:>10.6f}  "
                  f"{overlaps[k]**2:>10.6f}")

        mean_overlap = float(np.mean(overlaps))
        max_overlap = float(np.max(overlaps))
        print(f"\n  Mean overlap: {mean_overlap:.6f}")
        print(f"  Max overlap:  {max_overlap:.6f}")

        # Hecke operator T_2 commutativity check
        T2 = hecke_operator_T2(n)
        P = parity_operator(n)
        commutator = H_opt @ T2 - T2 @ H_opt
        comm_norm = float(np.linalg.norm(commutator, 'fro'))
        H_norm = float(np.linalg.norm(H_opt, 'fro'))
        print(f"\n  [H_n, T_2] Frobenius norm: {comm_norm:.4f}")
        print(f"  ||H_n||_F:                 {H_norm:.4f}")
        print(f"  Relative commutator:       {comm_norm/H_norm:.4f}")

        results[n] = {
            'evals': top_evals,
            'overlaps': overlaps,
            'mean_overlap': mean_overlap,
            'max_overlap': max_overlap,
            'hecke_commutator': comm_norm / H_norm,
        }

    # Convergence: does overlap increase from n=50 to n=100?
    print("\n--- Convergence of overlaps n=50 -> n=100 ---")
    print(f"  Mean overlap n=50:  {results[50]['mean_overlap']:.6f}")
    print(f"  Mean overlap n=100: {results[100]['mean_overlap']:.6f}")
    delta = results[100]['mean_overlap'] - results[50]['mean_overlap']
    print(f"  Delta:              {delta:+.6f}  "
          f"({'increasing -> converging to phi_0' if delta > 0 else 'decreasing'})")

    print(f"\n  Hecke commutator [H_n, T_2]/||H_n||:")
    print(f"  n=50:  {results[50]['hecke_commutator']:.4f}")
    print(f"  n=100: {results[100]['hecke_commutator']:.4f}")

    return results


def save_results(results: dict, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    target = zeta_zeros(30)

    lines = [
        "# Eigenvector Experiment: H_n → Trivial Hecke Character",
        "",
        "> Date: 2026-05-11",
        "> Experiment: overlap of UCA-constrained eigenvectors with phi_0 = |x|^{1/2}",
        "",
        "## Setup",
        "",
        "The trivial Hecke character $\\phi_0(x) = |x|^{1/2}$ on $C_Q$ corresponds",
        "to the constant function in the Dirichlet basis (norm quotiented out).",
        "We compute $|\\langle v_k, \\phi_0 \\rangle|$ for each eigenvector $v_k$ of $H_n$.",
        "",
        "## Results",
        "",
    ]

    for n, r in results.items():
        lines += [
            f"### n={n}",
            "",
            f"| k | γ_k | overlap | overlap² |",
            "|---|---|---|---|",
        ]
        for k in range(min(10, len(r['overlaps']))):
            lines.append(
                f"| {k+1} | {target[k]:.4f} | {r['overlaps'][k]:.6f} | "
                f"{r['overlaps'][k]**2:.6f} |")
        lines += [
            "",
            f"Mean overlap: {r['mean_overlap']:.6f}",
            f"Hecke commutator $\\|[H_n, T_2]\\|/\\|H_n\\|$: {r['hecke_commutator']:.4f}",
            "",
        ]

    lines += [
        "## Convergence",
        "",
        f"| n | Mean overlap | Hecke commutator |",
        "|---|---|---|",
    ]
    for n, r in results.items():
        lines.append(f"| {n} | {r['mean_overlap']:.6f} | {r['hecke_commutator']:.4f} |")

    lines += [
        "",
        "## Interpretation",
        "",
        "If mean overlap increases with $n$ and approaches 1:",
        "→ $H_n$ eigenvectors converge to $\\phi_0$ (trivial Hecke character)",
        "→ Step 2a (eigenvector convergence) is numerically confirmed",
        "→ Combined with $[H_n, P]=0$, this supports Step 2b",
        "",
        "If Hecke commutator $\\|[H_n, T_2]\\|/\\|H_n\\| \\to 0$:",
        "→ $D|_H$ commutes with Hecke operators",
        "→ Strong multiplicity one theorem (Jacquet-Langlands) applies",
        "→ $\\mathrm{Spec}(D|_H) = \\{\\gamma_n\\}$ follows from Langlands for $GL(1)$",
    ]

    path = os.path.join(output_dir, 'eigenvector_experiment.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"\nReport saved: {path}")


if __name__ == '__main__':
    results = run_eigenvector_experiment()
    output_dir = os.path.join(os.path.dirname(__file__), 'results')
    save_results(results, output_dir)
