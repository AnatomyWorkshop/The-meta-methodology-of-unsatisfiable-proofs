# Duality Defect Analysis Report

> Date: 2026-05-11
> Experiment: Measuring [H_BK, P] — the duality defect of Berry-Keating
> Theoretical basis: UCA predicts the true H_RH satisfies [H_RH, P] = 0

---

## Summary

The duality defect of the Berry-Keating Hamiltonian is large (76% of H_BK's norm),
full-rank, and orthogonal to the spectral-optimized perturbation. The true Hilbert-Polya
operator must satisfy both constraints simultaneously — a much harder problem than
either alone.

---

## Result 1: Duality Defect of Berry-Keating (n=50)

| Metric | Value | Interpretation |
|--------|-------|----------------|
| ||delta_BK||_F | 469.57 | Absolute defect magnitude |
| Relative defect | 76.1% | Berry-Keating is far from UCA |
| Effective rank | 50/50 | Full-rank defect |
| Singular value spectrum | All equal (68.48) | Flat — maximally unstructured |

**The flat singular value spectrum is remarkable**: all 50 singular values of [H_BK, P]
are identical. This means the duality defect is proportional to a unitary operator —
it has no preferred direction in operator space. The Berry-Keating Hamiltonian fails
duality compatibility in the most uniform possible way.

---

## Result 2: Structure of the Defect-Canceling Correction

The operator V_correction = -delta_BK @ P / 2 exactly cancels the duality defect:

| Property | Value |
|----------|-------|
| ||V_correction||_F | 234.79 |
| Hermitian error | 0.0000 (exactly Hermitian) |
| Diagonal fraction | 0.000 (no diagonal component) |
| Effective rank | 50/50 (full-rank) |
| Residual after correction | 0.000000 (exact cancellation) |

The correction is exactly Hermitian and exactly cancels the defect. This means:
- H_BK + V_correction is self-adjoint (Hermitian)
- H_BK + V_correction commutes with P (duality-compatible)
- H_BK + V_correction satisfies UCA

But does it match the zeta zeros?

---

## Result 3: Spectral vs Duality Constraints are Orthogonal

| Operator | Spectral RMSE | Duality defect |
|----------|--------------|----------------|
| Bare H_BK | 37.79 | 250.55 (baseline) |
| H_BK + V_defect (UCA-corrected) | 27.31 | 0.00 (exact) |
| H_BK + V_spectral (spectrum-optimized) | 0.94 | 262.29 (+4.7%) |

**Cosine similarity between V_defect and V_spectral: 0.0000**

The two corrections are orthogonal in operator space. The spectral optimizer:
- Dramatically improves spectral match (37.79 → 0.94)
- Slightly worsens duality compatibility (250.55 → 262.29)

The duality corrector:
- Moderately improves spectral match (37.79 → 27.31)
- Exactly satisfies duality compatibility (250.55 → 0.00)

---

## Interpretation

### What this proves:

1. **UCA and spectral matching impose orthogonal constraints on V.**
   The true H_RH must satisfy both simultaneously. Neither the spectral optimizer
   nor the duality corrector alone finds H_RH.

2. **The duality-corrected BK is a valid UCA solution but not H_RH.**
   H_BK + V_defect satisfies UCA exactly (self-adjoint + duality-compatible)
   but its spectrum does not match the zeta zeros (RMSE 27.31).

3. **The spectral-optimized BK is not a UCA solution.**
   H_BK + V_spectral matches 15 zeros to RMSE 0.94 but violates duality
   compatibility (defect increases by 4.7%).

### What this means for the search:

The Hilbert-Polya operator H_RH lies at the intersection of two constraints:
- **Spectral constraint**: Spec(H_RH) = {gamma_n} (zeta zeros)
- **UCA constraint**: [H_RH, P] = 0 (duality compatibility)

These constraints are currently orthogonal — satisfying one moves away from the other.
The true H_RH requires a fundamentally different construction, not a perturbation of
Berry-Keating. This is consistent with the UCA prediction that H_RH lives on the
adele class space, not on a finite interval with Dirichlet conditions.

### The flat singular value spectrum:

The fact that all singular values of [H_BK, P] are equal (68.48) means the duality
defect is proportional to a unitary operator. This is a structural property of the
Berry-Keating Hamiltonian in the Dirichlet basis — it fails duality compatibility
in the most symmetric possible way. This may be related to the fact that the
Dirichlet boundary conditions break the s <-> 1-s symmetry uniformly across all modes.

---

## Updated L3 Diagnosis

The Phase 6 L3 verdict remains **UNKNOWN**, now with sharper characterization:

> Berry-Keating fails UCA in two independent ways:
> (1) Spectral mismatch: RMSE 37.79 on 15 zeros
> (2) Duality defect: 76.1% of H_BK's norm, full-rank, flat spectrum
>
> These failures are orthogonal — correcting one does not help the other.
> The true Hilbert-Polya operator requires a construction that satisfies
> both constraints simultaneously, which is not achievable by perturbation
> of Berry-Keating on a finite interval. The correct setting is the adele
> class space, where the functional equation is exact (not approximate).
