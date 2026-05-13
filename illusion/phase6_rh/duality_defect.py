"""
Duality defect computation for Phase 6: Riemann Hypothesis.

UCA predicts: the perturbation V needed to go from Berry-Keating to H_RH
satisfies [V, star] = -delta_BK, where delta_BK = [D_BK, star] is the
duality defect of the Berry-Keating Hamiltonian.

This module computes delta_BK and analyzes its structure.

The duality map for RH: star implements s -> 1-s (functional equation symmetry).
In the finite-dimensional Dirichlet basis, this is the parity operator P (index reversal).
So: delta_BK = [H_BK, P] = H_BK @ P - P @ H_BK
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inverse_spectral_optimizer import build_base_hamiltonian


def parity_operator(n: int) -> np.ndarray:
    """
    Parity operator P: index reversal.
    Implements the duality s -> 1-s in the Dirichlet sin-basis.
    P_{jk} = delta_{j, n-1-k}
    """
    return np.eye(n)[::-1]


def duality_defect(H: np.ndarray) -> np.ndarray:
    """
    Compute delta = [H, P] = H @ P - P @ H.

    In UCA: delta = [D, star]. For RH, star = P (parity = functional equation).
    A zero defect means H commutes with the functional equation — UCA satisfied.
    """
    n = H.shape[0]
    P = parity_operator(n)
    return H @ P - P @ H


def defect_analysis(n: int = 50, n_zeros: int = None, verbose: bool = True) -> dict:
    """
    Compute and analyze the duality defect of the Berry-Keating Hamiltonian.

    n_zeros: number of zeta zeros to use for affine scaling of H_BK.
             Defaults to n. Pass the optimizer's n_zeros to get a starting
             point scaled to the correct target range.

    Returns a dict with:
      - H_bk: affine-scaled Berry-Keating Hamiltonian
      - defect: the matrix delta_BK = [H_BK, P]
      - defect_norm: Frobenius norm of delta_BK
      - relative_defect: ||delta_BK|| / ||H_BK||
      - singular_values: SVD of delta_BK
      - rank_estimate: effective rank (singular values > 1% of max)
      - V_hermitian: Hermitian operator that exactly cancels the defect
    """
    from l1_rh import zeta_zeros

    if n_zeros is None:
        n_zeros = n

    # Build Berry-Keating in Dirichlet basis, affine-scaled to zeta zero range
    H_bk = build_base_hamiltonian(n)
    base_eigs = np.sort(np.linalg.eigvalsh(H_bk))
    zeros = zeta_zeros(n_zeros)
    target = np.sort(zeros)
    base_min, base_max = base_eigs[0], base_eigs[-1]
    target_min, target_max = target[0], target[-1]
    scale = (target_max - target_min) / (base_max - base_min)
    shift = target_min - base_min * scale
    H_scaled = scale * H_bk + shift * np.eye(n)

    P = parity_operator(n)
    delta = duality_defect(H_scaled)

    # Structural analysis
    defect_norm = np.linalg.norm(delta, 'fro')
    H_norm = np.linalg.norm(H_scaled, 'fro')
    relative_defect = defect_norm / H_norm

    svd_vals = np.linalg.svd(delta, compute_uv=False)
    rank_estimate = int(np.sum(svd_vals > 0.01 * svd_vals[0]))

    # The correction operator: V must satisfy [V, P] = -delta
    # For a Hermitian V, [V, P] = V@P - P@V
    # The antisymmetric part of V under P-conjugation drives the commutator.
    # Minimal-norm solution: V_correction = -delta @ P / 2 (since P^2 = I)
    V_correction = -delta @ P / 2

    # Check: does V_correction cancel the defect?
    residual = duality_defect(H_scaled + V_correction)
    residual_norm = np.linalg.norm(residual, 'fro')

    # Analyze structure of V_correction
    v_diag_fraction = np.sum(np.abs(np.diag(V_correction))**2) / np.sum(np.abs(V_correction)**2)
    v_svd = np.linalg.svd(V_correction, compute_uv=False)
    v_rank = int(np.sum(v_svd > 0.01 * v_svd[0]))
    v_top1_fraction = v_svd[0]**2 / np.sum(v_svd**2)

    # Is V_correction Hermitian? (required for self-adjoint H + V)
    v_herm_error = np.linalg.norm(V_correction - V_correction.conj().T, 'fro') / np.linalg.norm(V_correction, 'fro')

    # Symmetrize V_correction to make it Hermitian
    V_hermitian = (V_correction + V_correction.conj().T) / 2
    residual_herm = duality_defect(H_scaled + V_hermitian)
    residual_herm_norm = np.linalg.norm(residual_herm, 'fro')

    if verbose:
        print("=" * 60)
        print("Duality Defect Analysis: Berry-Keating vs UCA")
        print("=" * 60)
        print()
        print(f"Matrix dimension: {n}")
        print(f"H_BK Frobenius norm: {H_norm:.4f}")
        print()
        print("--- Duality Defect delta = [H_BK, P] ---")
        print(f"  ||delta||_F:          {defect_norm:.4f}")
        print(f"  Relative defect:      {relative_defect:.4f}  ({relative_defect*100:.1f}% of H_BK)")
        print(f"  Effective rank:       {rank_estimate} / {n}")
        print(f"  Top singular value:   {svd_vals[0]:.4f}")
        print(f"  Singular value decay: {svd_vals[:5]}")
        print()
        print("--- Correction operator V = -delta @ P / 2 ---")
        print(f"  ||V_correction||_F:   {np.linalg.norm(V_correction, 'fro'):.4f}")
        print(f"  Hermitian error:      {v_herm_error:.4f}")
        print(f"  Diagonal fraction:    {v_diag_fraction:.3f}")
        print(f"  Effective rank:       {v_rank} / {n}")
        print(f"  Top-1 SVD fraction:   {v_top1_fraction:.3f}")
        print()
        print("--- Defect cancellation check ---")
        print(f"  Residual (raw V):     {residual_norm:.6f}")
        print(f"  Residual (Herm V):    {residual_herm_norm:.6f}")
        print()
        print("--- Interpretation ---")
        if relative_defect < 0.1:
            print("  Berry-Keating is nearly duality-compatible (< 10% defect).")
        elif relative_defect < 0.5:
            print("  Berry-Keating has moderate duality defect — correction is non-trivial.")
        else:
            print("  Berry-Keating has large duality defect — far from UCA satisfaction.")
        print()
        if v_rank < n // 5:
            print(f"  V_correction is low-rank ({v_rank}/{n}) — structured correction.")
        else:
            print(f"  V_correction is full-rank ({v_rank}/{n}) — unstructured correction.")
        print()
        if residual_herm_norm < 1e-10:
            print("  Hermitian V_correction exactly cancels the defect.")
        else:
            print(f"  Hermitian symmetrization introduces residual {residual_herm_norm:.4f}.")
            print("  The exact defect-canceling V is not Hermitian — self-adjointness")
            print("  and duality compatibility cannot both be satisfied by this correction.")

    return {
        "n": n,
        "H_bk": H_scaled,
        "P": P,
        "defect": delta,
        "defect_norm": defect_norm,
        "relative_defect": relative_defect,
        "singular_values": svd_vals,
        "rank_estimate": rank_estimate,
        "V_correction": V_correction,
        "V_hermitian": V_hermitian,
        "residual_norm": residual_norm,
        "residual_herm_norm": residual_herm_norm,
        "v_rank": v_rank,
        "v_top1_fraction": v_top1_fraction,
        "v_herm_error": v_herm_error,
    }


def compare_defect_vs_optimized_V(n: int = 30, verbose: bool = True) -> dict:
    """
    Compare the duality-defect-derived V_correction with the
    inverse-spectral-optimized V from Phase 6.

    Key question: does the optimized V (which matches the spectrum)
    also cancel the duality defect? If yes, UCA and spectral matching
    are consistent. If no, they impose different constraints.
    """
    from inverse_spectral_optimizer import optimize_spectral_match

    if verbose:
        print("=" * 60)
        print("Comparing defect-correction V vs spectral-optimized V")
        print("=" * 60)
        print()

    # Compute duality defect correction
    defect_result = defect_analysis(n=n, verbose=False)
    V_defect = defect_result["V_hermitian"]
    H_bk = defect_result["H_bk"]
    P = defect_result["P"]

    # Run spectral optimization
    if verbose:
        print(f"Running spectral optimization (n={n}, 15 zeros)...")
    opt_result = optimize_spectral_match(n=n, n_zeros=15, max_iter=300,
                                          reg_lambda=0.001, verbose=False)
    V_spectral = opt_result.best_V

    # Compare the two V matrices
    overlap = np.sum(V_defect * V_spectral) / (
        np.linalg.norm(V_defect, 'fro') * np.linalg.norm(V_spectral, 'fro')
    )

    # Does V_spectral cancel the duality defect?
    H_spectral = H_bk + V_spectral
    defect_after_spectral = duality_defect(H_spectral)
    defect_after_spectral_norm = np.linalg.norm(defect_after_spectral, 'fro')
    original_defect_norm = defect_result["defect_norm"]

    # Does V_defect improve spectral match?
    from l1_rh import zeta_zeros
    zeros = zeta_zeros(n)
    target = np.sort(zeros)
    H_defect_corrected = H_bk + V_defect
    eigs_defect = np.sort(np.linalg.eigvalsh(H_defect_corrected))[-15:]
    spectral_error_defect = np.sqrt(np.mean((eigs_defect - np.sort(target[:15]))**2))

    eigs_bk = np.sort(np.linalg.eigvalsh(H_bk))[-15:]
    spectral_error_bk = np.sqrt(np.mean((eigs_bk - np.sort(target[:15]))**2))

    if verbose:
        print(f"  V_defect vs V_spectral cosine similarity: {overlap:.4f}")
        print()
        print(f"  Original duality defect ||delta_BK||:     {original_defect_norm:.4f}")
        print(f"  Defect after spectral V:                  {defect_after_spectral_norm:.4f}")
        print(f"  Defect reduction by spectral V:           {(1 - defect_after_spectral_norm/original_defect_norm)*100:.1f}%")
        print()
        print(f"  Spectral RMSE (bare BK):                  {spectral_error_bk:.4f}")
        print(f"  Spectral RMSE (defect-corrected BK):      {spectral_error_defect:.4f}")
        print(f"  Spectral RMSE (spectral-optimized):       {opt_result.spectral_error:.4f}")
        print()
        if overlap > 0.5:
            print("  HIGH OVERLAP: spectral optimization and defect correction")
            print("  are finding the same V. UCA and spectral matching are consistent.")
        elif overlap > 0.1:
            print("  MODERATE OVERLAP: partial consistency between UCA and spectral matching.")
        else:
            print("  LOW OVERLAP: spectral optimization and defect correction")
            print("  find different V. UCA and spectral matching impose different constraints.")
            print("  The true H_RH must satisfy both simultaneously.")

    return {
        "overlap": overlap,
        "defect_after_spectral_norm": defect_after_spectral_norm,
        "original_defect_norm": original_defect_norm,
        "spectral_error_bk": spectral_error_bk,
        "spectral_error_defect": spectral_error_defect,
        "spectral_error_optimized": opt_result.spectral_error,
    }


if __name__ == "__main__":
    # Main analysis
    result = defect_analysis(n=50, verbose=True)

    print()
    print("=" * 60)
    print("Comparison: defect correction vs spectral optimization")
    print("=" * 60)
    compare_result = compare_defect_vs_optimized_V(n=30, verbose=True)
