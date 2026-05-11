"""
Evaluator for Phase 6: measures how well candidate operators match zeta zeros
and satisfy the four closure laws.
"""

import numpy as np
from typing import Tuple
from dataclasses import dataclass

from operators_rh import OperatorCandidate


@dataclass
class ClosureScore:
    name: str
    spectral_match: float       # [0,1] how well eigenvalues match zeta zeros
    pair_correlation_match: float  # [0,1] how well R2 matches GUE
    spacing_match: float        # [0,1] how well spacing matches Wigner surmise
    duality_score: float        # [0,1] zeros <-> spectrum bijection quality
    rigidity_score: float       # [0,1] self-adjointness (binary in practice)
    symmetry_score: float       # [0,1] functional equation symmetry
    reduction_score: float      # [0,1] prime encoding / dimension reduction
    composite_score: float      # weighted average
    description: str


def evaluate_spectral_match(eigenvalues: np.ndarray, zeros: np.ndarray,
                            epsilon: float = 0.5) -> float:
    """
    Measure how well eigenvalues match zeta zeros.
    For each zero, find the closest eigenvalue. Score = fraction matched within epsilon.

    We normalize eigenvalues to the same scale as zeros first.
    """
    if len(eigenvalues) == 0 or len(zeros) == 0:
        return 0.0

    eigs = np.sort(eigenvalues)
    zs = np.sort(zeros)

    # Scale eigenvalues to match zero range
    eig_range = eigs[-1] - eigs[0]
    zero_range = zs[-1] - zs[0]

    if eig_range < 1e-10:
        return 0.0

    # Affine map: eigs -> zeros scale
    scaled_eigs = (eigs - eigs[0]) / eig_range * zero_range + zs[0]

    # For each zero, find closest scaled eigenvalue
    n_match = min(len(scaled_eigs), len(zs))
    matched = 0
    for i in range(n_match):
        min_dist = np.min(np.abs(scaled_eigs - zs[i]))
        if min_dist < epsilon:
            matched += 1

    return matched / n_match


def evaluate_pair_correlation(eigenvalues: np.ndarray) -> float:
    """
    Measure how well the pair correlation matches GUE prediction.
    Returns [0,1] score where 1 = perfect GUE match.
    """
    from l1_rh import pair_correlation, gue_pair_correlation

    if len(eigenvalues) < 10:
        return 0.0

    tau, r2 = pair_correlation(eigenvalues, tau_max=2.0, n_bins=20)
    gue_r2 = gue_pair_correlation(tau)

    # L2 distance, normalized
    diff = np.mean((r2 - gue_r2)**2)
    score = max(0.0, 1.0 - np.sqrt(diff))
    return score


def evaluate_spacing(eigenvalues: np.ndarray) -> float:
    """
    Measure how well nearest-neighbor spacing matches Wigner surmise (GUE).
    Returns [0,1] score.
    """
    from l1_rh import normalized_spacings, wigner_surmise

    if len(eigenvalues) < 5:
        return 0.0

    spacings = normalized_spacings(eigenvalues)
    spacings = spacings[spacings > 0]

    if len(spacings) < 3:
        return 0.0

    # Compare histogram to Wigner surmise
    s_vals = np.linspace(0.01, 3.0, 30)
    wigner = wigner_surmise(s_vals)

    hist, bin_edges = np.histogram(spacings, bins=s_vals, density=True)
    wigner_binned = wigner[:-1]

    diff = np.mean((hist - wigner_binned)**2)
    score = max(0.0, 1.0 - np.sqrt(diff) / 0.5)
    return score


def evaluate_duality(eigenvalues: np.ndarray, zeros: np.ndarray) -> float:
    """
    Duality score: does a bijection exist between eigenvalues and zeros?
    Measures the quality of the best linear mapping eigs -> zeros.
    """
    if len(eigenvalues) < 3 or len(zeros) < 3:
        return 0.0

    eigs = np.sort(eigenvalues)
    zs = np.sort(zeros[:len(eigs)])

    # Best linear fit
    n = min(len(eigs), len(zs))
    eigs_n = eigs[:n]
    zs_n = zs[:n]

    # Correlation coefficient
    if np.std(eigs_n) < 1e-10:
        return 0.0

    corr = np.corrcoef(eigs_n, zs_n)[0, 1]
    return max(0.0, corr)


def evaluate_rigidity(candidate: OperatorCandidate) -> float:
    """Rigidity = self-adjointness. Binary: 1.0 if self-adjoint, 0.0 if not."""
    return 1.0 if candidate.is_self_adjoint else 0.0


def evaluate_symmetry(candidate: OperatorCandidate, eigenvalues: np.ndarray) -> float:
    """
    Symmetry score: does the operator have functional equation symmetry?
    Check if spectrum is symmetric around its center (s <-> 1-s maps gamma <-> -gamma).
    """
    base_score = 0.5 if candidate.has_functional_equation_symmetry else 0.0

    # Check spectral symmetry
    eigs = np.sort(eigenvalues)
    center = (eigs[0] + eigs[-1]) / 2
    reflected = 2 * center - eigs[::-1]

    if len(eigs) < 3:
        return base_score

    # How symmetric is the spectrum?
    diff = np.mean(np.abs(eigs - reflected)) / (np.std(eigs) + 1e-10)
    symmetry_empirical = max(0.0, 1.0 - diff)

    return 0.5 * base_score + 0.5 * symmetry_empirical


def evaluate_reduction(candidate: OperatorCandidate) -> float:
    """
    Dimension reduction score: does the operator encode prime structure compactly?
    """
    score = 0.0
    if candidate.encodes_primes:
        score += 0.5
    if candidate.is_self_adjoint:
        score += 0.25
    if candidate.has_functional_equation_symmetry:
        score += 0.25
    return score


def evaluate_candidate(candidate: OperatorCandidate, zeros: np.ndarray) -> ClosureScore:
    """Full evaluation of a candidate operator against zeta zeros."""
    eigs = candidate.eigenvalues

    spectral = evaluate_spectral_match(eigs, zeros)
    pair_corr = evaluate_pair_correlation(eigs)
    spacing = evaluate_spacing(eigs)
    duality = evaluate_duality(eigs, zeros)
    rigidity = evaluate_rigidity(candidate)
    symmetry = evaluate_symmetry(candidate, eigs)
    reduction = evaluate_reduction(candidate)

    # Composite: weighted by importance for closure validity
    # Structural properties (rigidity, symmetry, reduction) determine whether
    # a closure PATH is valid. Spectral match determines how far along that path
    # the candidate has progressed. Both matter, but structural validity is primary.
    composite = (
        0.20 * spectral +
        0.10 * pair_corr +
        0.05 * spacing +
        0.20 * duality +
        0.20 * rigidity +
        0.15 * symmetry +
        0.10 * reduction
    )

    return ClosureScore(
        name=candidate.name,
        spectral_match=spectral,
        pair_correlation_match=pair_corr,
        spacing_match=spacing,
        duality_score=duality,
        rigidity_score=rigidity,
        symmetry_score=symmetry,
        reduction_score=reduction,
        composite_score=composite,
        description=candidate.description,
    )


if __name__ == "__main__":
    from l1_rh import zeta_zeros
    from operators_rh import build_candidate_registry

    print("Evaluating candidates against first 30 zeta zeros...\n")
    zeros = zeta_zeros(30)
    candidates = build_candidate_registry(30, zeros)

    scores = []
    for c in candidates:
        score = evaluate_candidate(c, zeros)
        scores.append(score)

    scores.sort(key=lambda s: s.composite_score, reverse=True)

    print(f"{'Name':<30} {'Composite':>9} {'Spectral':>9} {'Duality':>8} "
          f"{'Rigid':>6} {'Symm':>6} {'Reduce':>7}")
    print("-" * 85)
    for s in scores:
        print(f"{s.name:<30} {s.composite_score:>9.3f} {s.spectral_match:>9.3f} "
              f"{s.duality_score:>8.3f} {s.rigidity_score:>6.1f} "
              f"{s.symmetry_score:>6.3f} {s.reduction_score:>7.2f}")
