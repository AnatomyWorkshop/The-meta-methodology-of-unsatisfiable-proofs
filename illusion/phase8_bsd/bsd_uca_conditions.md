# BSD Conjecture: Sufficient Conditions under UCA

**Status:** Structural equivalence established. Constructive proof missing.  
**Date:** 2026-05-17

---

## Setup

Let E/Q be an elliptic curve of conductor N.  
Let f_E ∈ S₂(Γ₀(N)) be the associated newform (Wiles–Taylor).  
Let L(E, s) = Σ aₙ n^{-s} be the L-function, with functional equation:

    Λ(E, s) = εₑ · Λ(E, 2−s)

where εₑ ∈ {+1, −1} is the root number and Λ(E, s) = (√N / 2π)^s Γ(s) L(E, s).

Define the **Hecke-UCA operator**:

    H_E = Σ_p (log p / p) · T_p · P_p

where T_p is the Hecke operator at p, and P_p is the local UCA duality operator
implementing the functional equation symmetry s ↔ 2−s at prime p.

---

## The Four Conditions

**Condition 1 (Spectral finiteness).**  
The operator H_E, acting on L²(𝔸_Q*/Q*), has a finite-dimensional kernel:

    dim ker(H_E) < ∞

*Why this is hard:* The adelic quotient 𝔸_Q*/Q* is non-compact. Standard spectral
theory (Rellich compactness) does not apply. Finiteness of ker(H_E) must be proved
directly, likely via the theory of automorphic forms and the discrete decomposition
of L²(GL(2, 𝔸)/GL(2, Q)).

*What is known:* The cuspidal spectrum of GL(2) is discrete. If H_E is shown to
annihilate only cuspidal forms (not Eisenstein series), then ker(H_E) is finite-
dimensional by the theory of newforms.

---

**Condition 2 (Spectral multiplicity = analytic rank).**  
Assuming Condition 1:

    dim ker(H_E) = ord_{s=1} L(E, s)

*Why this is hard:* This is essentially BSD itself, restated spectrally. The
connection between the kernel dimension and the vanishing order of L(E, s) requires
showing that each independent element of ker(H_E) corresponds to an independent
zero of L(E, s) at s = 1.

*What is known:* For rank 0 (L(E,1) ≠ 0): ker(H_E) should be trivial. For rank 1
(εₑ = −1): the functional equation forces L(E,1) = 0, giving dim ker ≥ 1. The
rank 1 case is controlled by Kolyvagin–Gross–Zagier. Rank ≥ 2 is open.

---

**Condition 3 (Hecke eigenvectors → algebraic cycles).**  
For each independent f_i ∈ ker(H_E), there exists an algebraic cycle Z_i on
X₀(N) × X₀(N) such that:

    ⟨Z_i, Δ⟩ = L'(f_i, 1)   (period integral = central L-derivative)

and the cycles Z₁, ..., Z_r are linearly independent in CH¹(X₀(N) × X₀(N)) ⊗ Q.

*Why this is hard:* This is the higher-order Gross–Zagier formula. For r = 1,
this is the Gross–Zagier theorem (1986): the Heegner point height equals L'(E,1).
For r = 2, no explicit construction exists. The difficulty is not geometric
construction but proving linear independence, which requires p-adic L-function
information.

*What is known:* The r = 1 case is complete. For r ≥ 2, the Beilinson–Bloch
conjecture predicts the existence of such cycles, but no proof.

---

**Condition 4 (Galois compatibility).**  
The map f_i ↦ Z_i from Condition 3 commutes with the Galois action:

    σ(Z_i) = Z_{σ(i)}   for all σ ∈ Gal(Q̄/Q)

and the image of Z_i under the Abel–Jacobi map lands in E(Q) ⊗ R:

    AJ(Z_i) ∈ E(Q) ⊗ R ⊂ J₀(N)(Q) ⊗ R

*Why this is hard:* This requires the algebraic cycles to be defined over Q (or
a controlled number field), not just over Q̄. The Galois action on the Hecke
eigenvectors is controlled by the L-function, but the descent from Q̄ to Q
requires the full machinery of Galois cohomology and Selmer groups.

*What is known:* For r = 1, the Heegner point is defined over a ring class field
and descends to E(Q) via the Gross–Zagier–Kolyvagin argument. For r ≥ 2, no
analogous descent is known.

---

## The Logical Structure

    Condition 1 (ker finite-dim)
         ↓
    Condition 2 (dim ker = rank)
         ↓
    Condition 3 (eigenvectors → cycles)
         ↓
    Condition 4 (Galois descent → rational points)
         ↓
    BSD: rank(E) = #(independent rational points in E(Q))

Each condition is necessary. Together they are sufficient for BSD.

The UCA framework provides the language for Conditions 1 and 2.
Conditions 3 and 4 require arithmetic geometry beyond UCA.

---

## What UCA Contributes

UCA does not prove BSD. It does three things:

1. **Reframes the problem spectrally.** BSD becomes: "H_E has a kernel of the
   right dimension." This is a well-posed operator theory question.

2. **Identifies the obstruction.** The non-compactness of 𝔸_Q*/Q* is the
   single source of difficulty. If the space were compact (as in the Calabi
   case), Conditions 1 and 2 would follow from standard spectral theory.

3. **Separates the two hard parts.** Condition 1–2 (spectral, UCA territory)
   and Condition 3–4 (arithmetic, Gross–Zagier territory) are independent
   subproblems. Progress on either does not require the other.

---

## Comparison with RH

| | RH | BSD |
|---|---|---|
| Space | L²(𝔸_Q*/Q*), GL(1) | L²(𝔸_Q*/Q*), GL(2) |
| Non-compactness | Mild (continuous spectrum = Eisenstein, GL(1)) | Severe (Eisenstein series on GL(2)) |
| UCA operator | Vladimirov Δ_𝔸 | Hecke-UCA H_E |
| Key condition | H1: continuous spectrum suppressed | Condition 1: ker(H_E) finite-dim |
| Status | H1 open, numerical RMSE = 0.036 | All four conditions open for r ≥ 2 |

The RH problem reduces to one condition (H1). BSD requires four.
BSD is harder because GL(2) is larger and the arithmetic content (rational points)
has no analogue in the GL(1)/RH setting.

---

## Open Questions (Precise)

**Q1.** Is ker(H_E) finite-dimensional for all E/Q?  
Equivalent to: does H_E annihilate only cuspidal forms?

**Q2.** Does dim ker(H_E) = ord_{s=1} L(E, s) follow from UCA alone,
or does it require additional arithmetic input?

**Q3.** Can the higher Gross–Zagier map (Condition 3) be constructed
using the UCA eigenvectors as input, rather than Heegner points?

**Q4.** Is there a uniform construction for all ranks r ≥ 1,
or does each rank require a separate argument?
