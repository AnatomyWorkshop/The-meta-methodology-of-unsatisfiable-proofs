"""
Minimal adelic basis experiment.

Target operator: Delta_A (adelic Vladimirov), NOT D (dilation generator).

Delta_A = sum_p Delta_p  on  H = L^2(C_Q)/V

Key distinction from Phase 6:
  Phase 6: H_n approximates D (first-order, eigenvalues ~ k*log(p))
  This:    Delta_n approximates Delta_A (second-order, eigenvalues ~ p^{2k})

Construction:
  p=2, N=3: space Z_2/8Z_2, local dimension 2*2^3 - 1 = 15
  Archimedean: first M Hermite functions (harmonic oscillator eigenstates)
  Tensor product: dimension 15 * M

Checks:
  1. Spec(Delta_n) vs zeta zeros
  2. ||[Delta_n, T_2]|| / ||Delta_n||  (should -> 0 in correct basis)
  3. Overlap of eigenvectors with trivial Hecke character phi_0
"""

import numpy as np
from scipy.linalg import eigh
import sys, os
sys.path.insert(0, os.path.dirname(__file__))


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
# Local Vladimirov operator on Z_p / p^N Z_p
# ---------------------------------------------------------------------------

def vladimirov_local(p: int, N: int, alpha: float = 2.0) -> np.ndarray:
    """
    Vladimirov operator Delta_p^alpha in the eigenbasis.

    Eigenvalues: p^{alpha*k} for k in {-N, ..., N}
    Multiplicity: p^|k| - p^{|k|-1} for k != 0, 1 for k=0

    Returns diagonal matrix (eigenvalue basis).
    """
    diag = []
    for k in range(-N, N + 1):
        lam = float(p) ** (alpha * k)
        if k == 0:
            mult = 1
        else:
            mult = p ** abs(k) - p ** (abs(k) - 1)
        diag.extend([lam] * int(mult))
    return np.diag(diag)


def vladimirov_dim(p: int, N: int) -> int:
    """Dimension of local space Z_p / p^N Z_p."""
    total = 1  # k=0
    for k in range(1, N + 1):
        total += 2 * (p**k - p**(k-1))
    return total


# ---------------------------------------------------------------------------
# Archimedean place: harmonic oscillator (Hermite functions)
# ---------------------------------------------------------------------------

def harmonic_oscillator(M: int) -> np.ndarray:
    """
    Harmonic oscillator Hamiltonian H_inf = -d^2/dx^2 + x^2 in Hermite basis.

    Eigenvalues: 2k+1 for k = 0, 1, ..., M-1.
    In the Hermite function basis, this is diagonal.
    """
    return np.diag([2*k + 1.0 for k in range(M)])


# ---------------------------------------------------------------------------
# Hecke operator T_2 on local p=2 space
# ---------------------------------------------------------------------------

def hecke_T2_local(p: int, N: int) -> np.ndarray:
    """
    Hecke operator T_2 on the local Vladimirov eigenbasis for prime p=2.

    In the p-adic setting, T_2 acts as:
      T_2 f(x) = (1/sqrt(2)) * sum_{a mod 2} f((x+a)/2) + f(2x)

    In the Vladimirov eigenbasis (indexed by level k):
      T_2 maps level k to levels k-1 and k+1 (with appropriate coefficients).

    Matrix element (T_2)_{k', k}:
      = 1/sqrt(2) if k' = k-1 (scaling down by 2)
      = 1/sqrt(2) if k' = k+1 (scaling up by 2)
      = 0 otherwise

    This is the adjacency matrix of the Bruhat-Tits tree for GL(2, Q_2),
    restricted to the diagonal (level) structure.

    Note: In the full eigenbasis with multiplicities, T_2 acts within each
    multiplicity block. We construct the block-diagonal version.
    """
    dim = vladimirov_dim(p, N)

    # Build level -> index mapping
    levels = []
    for k in range(-N, N + 1):
        if k == 0:
            mult = 1
        else:
            mult = p ** abs(k) - p ** (abs(k) - 1)
        levels.extend([k] * int(mult))
    levels = np.array(levels)

    T = np.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            ki, kj = levels[i], levels[j]
            # T_2 connects adjacent levels
            if ki == kj - 1 or ki == kj + 1:
                # Within same "branch" of the tree
                T[i, j] = 1.0 / np.sqrt(2)

    # Symmetrize
    T = (T + T.T) / 2
    return T


# ---------------------------------------------------------------------------
# Global adelic operator: tensor product construction
# ---------------------------------------------------------------------------

def build_adelic_operator(p: int = 2, N: int = 3, M: int = 10,
                           alpha: float = 2.0) -> dict:
    """
    Build the minimal adelic operator Delta_A on Z_p/p^N Z_p x R_M.

    Delta_A = Delta_p (x) I_M + I_d (x) Delta_inf

    where:
      Delta_p: Vladimirov on Z_p/p^N Z_p (dim d)
      Delta_inf: harmonic oscillator on R_M (dim M)

    Returns dict with matrices and metadata.
    """
    d = vladimirov_dim(p, N)

    # Local operators
    D_p = vladimirov_local(p, N, alpha)      # d x d diagonal
    D_inf = harmonic_oscillator(M)            # M x M diagonal

    # Tensor product: Delta_A = D_p (x) I_M + I_d (x) D_inf
    I_d = np.eye(d)
    I_M = np.eye(M)

    Delta_A = np.kron(D_p, I_M) + np.kron(I_d, D_inf)

    # Hecke operator T_2 acts only on the p=2 factor
    T2_local = hecke_T2_local(p, N)
    T2_global = np.kron(T2_local, I_M)

    return {
        'Delta_A': Delta_A,
        'T2': T2_global,
        'D_p': D_p,
        'D_inf': D_inf,
        'dim': d * M,
        'd_local': d,
        'M_inf': M,
        'p': p, 'N': N,
    }


# ---------------------------------------------------------------------------
# Trivial Hecke character in adelic basis
# ---------------------------------------------------------------------------

def trivial_hecke_character_adelic(d: int, M: int) -> np.ndarray:
    """
    Trivial Hecke character phi_0 in the adelic tensor product basis.

    phi_0(x) = |x|^{1/2} on C_Q.

    In the local Vladimirov eigenbasis:
      - p-adic factor: phi_0 is the k=0 eigenstate (constant on Z_p)
      - Archimedean factor: phi_0 is the ground state of the harmonic oscillator

    So phi_0 = e_0^{(p)} (x) e_0^{(inf)} in the tensor product basis,
    where e_0^{(p)} is the first basis vector (k=0 level) and
    e_0^{(inf)} is the ground state (k=0 Hermite function).
    """
    v = np.zeros(d * M)
    # k=0 level is the first index in our eigenbasis (k goes from -N to N)
    # The k=0 state is at index N (since we go -N, ..., 0, ..., N)
    # But with multiplicities, k=0 has mult=1 and is at position sum_{k=-N}^{-1} mult(k)
    # = sum_{k=1}^{N} (p^k - p^{k-1}) = p^N - 1
    # For p=2, N=3: 2^3 - 1 = 7, so k=0 is at index 7
    # Archimedean ground state is at index 0 in the M-dim space
    # Tensor product index: i_p * M + i_inf
    p_ground_idx = 0  # will be computed properly below
    inf_ground_idx = 0

    # Recompute: levels go -N, ..., N with multiplicities
    # k=0 is at cumulative position sum_{k=-N}^{-1} mult(k)
    # mult(k) = p^|k| - p^{|k|-1} for k != 0
    p_val = 2  # hardcoded for now, generalize later
    N_val = 3
    cum = 0
    for k in range(-N_val, 0):
        cum += p_val**abs(k) - p_val**(abs(k)-1)
    p_ground_idx = cum  # index of k=0 in local basis

    tensor_idx = p_ground_idx * M + inf_ground_idx
    v[tensor_idx] = 1.0
    return v


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_adelic_experiment(p: int = 2, N: int = 3, M: int = 10,
                           n_zeros: int = 20, verbose: bool = True) -> dict:
    """
    Run the minimal adelic basis experiment.

    Checks:
    1. Eigenvalues of Delta_A vs zeta zeros (after affine scaling)
    2. ||[Delta_A, T_2]|| / ||Delta_A||
    3. Overlap of eigenvectors with phi_0
    """
    target = zeta_zeros(n_zeros)

    ops = build_adelic_operator(p=p, N=N, M=M)
    Delta_A = ops['Delta_A']
    T2 = ops['T2']
    dim = ops['dim']

    if verbose:
        print(f"  Adelic basis: p={p}, N={N}, M={M}, dim={dim}")
        print(f"  Delta_A eigenvalue range: [{Delta_A.min():.2f}, {Delta_A.max():.2f}]")

    # Eigendecomposition
    evals, evecs = eigh(Delta_A)

    # Delta_A has eigenvalues p^{2k} (exponential), starting from small values.
    # The zeta zeros gamma_n are the LOWEST non-trivial eigenvalues of the
    # correct operator. We take the SMALLEST n_match eigenvalues (low energy).
    # Skip the zero eigenvalue (ground state of harmonic oscillator at k=0).
    n_match = min(n_zeros, dim)

    # Sort ascending, take first n_match
    sort_idx = np.argsort(evals)
    evals_sorted = evals[sort_idx]
    evecs_sorted = evecs[:, sort_idx]

    # Skip near-zero eigenvalues (they correspond to the trivial sector)
    nonzero_mask = evals_sorted > 1e-6
    evals_nz = evals_sorted[nonzero_mask]
    evecs_nz = evecs_sorted[:, nonzero_mask]

    n_match = min(n_zeros, len(evals_nz))
    bot_evals = evals_nz[:n_match]
    bot_evecs = evecs_nz[:, :n_match]

    # Affine scale to match zeta zero range
    if n_match >= 2:
        src_min, src_max = bot_evals[0], bot_evals[-1]
        tgt_min, tgt_max = target[0], target[n_match-1]
        if abs(src_max - src_min) > 1e-10:
            scale = (tgt_max - tgt_min) / (src_max - src_min)
            shift = tgt_min - scale * src_min
            evals_scaled = scale * bot_evals + shift
        else:
            evals_scaled = bot_evals.copy()
    else:
        evals_scaled = bot_evals.copy()

    rmse = float(np.sqrt(np.mean((evals_scaled - target[:n_match])**2)))

    if verbose:
        print(f"\n  Eigenvalue match (lowest {n_match} non-zero):")
        print(f"  {'k':>4}  {'gamma_k':>10}  {'eval_k':>10}  {'error':>10}")
        for k in range(min(10, n_match)):
            err = evals_scaled[k] - target[k]
            print(f"  {k+1:>4}  {target[k]:>10.4f}  {evals_scaled[k]:>10.4f}  {err:>+10.4f}")
        print(f"\n  RMSE: {rmse:.5f}")

    # Hecke commutativity
    comm = Delta_A @ T2 - T2 @ Delta_A
    comm_norm = float(np.linalg.norm(comm, 'fro'))
    delta_norm = float(np.linalg.norm(Delta_A, 'fro'))
    rel_comm = comm_norm / delta_norm if delta_norm > 1e-10 else float('inf')

    if verbose:
        print(f"\n  [Delta_A, T_2] Frobenius norm: {comm_norm:.4f}")
        print(f"  ||Delta_A||_F:                 {delta_norm:.4f}")
        print(f"  Relative commutator:           {rel_comm:.6f}")

    # Overlap with trivial Hecke character
    phi0 = trivial_hecke_character_adelic(ops['d_local'], M)
    overlaps = np.abs(bot_evecs.T @ phi0)

    if verbose:
        print(f"\n  Overlap |<v_k, phi_0>| for lowest eigenvectors:")
        print(f"  {'k':>4}  {'gamma_k':>10}  {'overlap':>10}")
        for k in range(min(10, n_match)):
            print(f"  {k+1:>4}  {target[k]:>10.4f}  {overlaps[k]:>10.6f}")
        print(f"\n  Mean overlap: {np.mean(overlaps):.6f}")
        print(f"  Max overlap:  {np.max(overlaps):.6f}")

    return {
        'evals_scaled': evals_scaled,
        'rmse': rmse,
        'rel_commutator': rel_comm,
        'overlaps': overlaps,
        'mean_overlap': float(np.mean(overlaps)),
        'dim': dim,
    }


def compare_with_sinbasis(verbose: bool = True) -> None:
    """
    Compare adelic basis results with sin-basis results from Phase 6.
    """
    print("\n--- Comparison: adelic basis vs sin-basis ---")
    print(f"  {'Metric':30s}  {'Sin-basis (n=100)':>20s}  {'Adelic (p=2,N=3,M=10)':>22s}")
    print(f"  {'-'*30}  {'-'*20}  {'-'*22}")
    print(f"  {'RMSE':30s}  {'0.00011':>20s}  {'(see above)':>22s}")
    print(f"  {'Mean overlap with phi_0':30s}  {'0.077':>20s}  {'(see above)':>22s}")
    print(f"  {'Rel. Hecke commutator':30s}  {'1.446':>20s}  {'(see above)':>22s}")
    print(f"\n  Key: if adelic basis gives rel. commutator << 1 and overlap >> 0.077,")
    print(f"  this confirms the sin-basis is the wrong function space.")


def main():
    print("Minimal Adelic Basis Experiment")
    print("=" * 60)
    print("\nTarget: Delta_A = Delta_2 (x) I + I (x) Delta_inf")
    print("(adelic Vladimirov, NOT dilation generator D)")

    results = {}

    for M in [5, 10, 20]:
        print(f"\n--- M={M} (Archimedean truncation) ---")
        r = run_adelic_experiment(p=2, N=3, M=M, n_zeros=20, verbose=True)
        results[M] = r

    compare_with_sinbasis()

    print("\n--- Convergence with M ---")
    print(f"  {'M':>4}  {'dim':>6}  {'RMSE':>10}  {'rel_comm':>12}  {'mean_overlap':>14}")
    for M, r in results.items():
        print(f"  {M:>4}  {r['dim']:>6}  {r['rmse']:>10.5f}  "
              f"{r['rel_commutator']:>12.6f}  {r['mean_overlap']:>14.6f}")

    # Save results
    output_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(output_dir, exist_ok=True)

    lines = [
        "# Minimal Adelic Basis Experiment",
        "",
        "> Date: 2026-05-11",
        "> Operator: $\\Delta_\\mathbb{A} = \\Delta_2 \\otimes I + I \\otimes \\Delta_\\infty$",
        "> Basis: $p=2$, $N=3$ (Vladimirov eigenbasis) $\\times$ Hermite functions",
        "",
        "## Key distinction from Phase 6",
        "",
        "Phase 6 approximated $D$ (dilation generator, first-order, continuous spectrum).",
        "This experiment approximates $\\Delta_\\mathbb{A}$ (adelic Vladimirov, second-order).",
        "The relation is $\\Delta_\\mathbb{A} = e^{2D}$.",
        "",
        "## Results",
        "",
        f"| M | dim | RMSE | Rel. Hecke commutator | Mean overlap |",
        "|---|---|---|---|---|",
    ]
    for M, r in results.items():
        lines.append(f"| {M} | {r['dim']} | {r['rmse']:.5f} | "
                     f"{r['rel_commutator']:.6f} | {r['mean_overlap']:.6f} |")

    lines += [
        "",
        "## Comparison with sin-basis (Phase 6, n=100)",
        "",
        "| Metric | Sin-basis | Adelic (M=10) |",
        "|---|---|---|",
        f"| RMSE | 0.00011 | {results[10]['rmse']:.5f} |",
        f"| Rel. Hecke commutator | 1.446 | {results[10]['rel_commutator']:.6f} |",
        f"| Mean overlap with $\\phi_0$ | 0.077 | {results[10]['mean_overlap']:.6f} |",
        "",
        "## Interpretation",
        "",
        "If the adelic basis gives rel. commutator $\\ll 1$ and mean overlap $\\gg 0.077$:",
        "→ Confirms sin-basis is the wrong function space",
        "→ $\\Delta_\\mathbb{A}$ in the correct basis satisfies Hecke commutativity",
        "→ Supports Proposition 1 and Theorem 2 numerically",
        "",
        "If not: the minimal adelic model needs refinement (larger $N$, better $\\Delta_\\infty$).",
    ]

    path = os.path.join(output_dir, 'adelic_basis_experiment.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"\nReport saved: {path}")


if __name__ == '__main__':
    main()
