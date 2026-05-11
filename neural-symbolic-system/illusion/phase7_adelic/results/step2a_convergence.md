# Step 2a: Convergence H_n → D|_H

## Setup

The sequence $H_n$ (Phase 6, UCA-constrained) satisfies:
- $H_n$ self-adjoint (Hermitian matrix)
- $[H_n, P] = 0$ exactly (by block-diagonal construction)
- Eigenvalues of $H_n$ converge to $\{\gamma_k\}_{k=1}^{30}$ with RMSE $\sim n^{-0.26}$
- Systematic negative bias: all eigenvalues below target (monotone from below)

## Trotter-Kato Conditions

| Condition | Status |
|---|---|
| (A) Self-adjoint on common core | ✓ Satisfied (finite-dimensional) |
| (B1) Eigenvalue convergence | ✓ Numerical (RMSE → 0) |
| (B2) Eigenvector convergence | ✗ Missing |
| (C) Range density | ✓ Satisfied (finite-dimensional) |

## Implication: Step 2a ⟹ Step 2b

**Theorem**: If $H_n \to D|_H$ strongly, then $[D|_H, F] = 0$.

**Proof**: For any $\phi \in H$:
$$[D|_H, F]\phi = \lim_n [H_n, P]\phi = \lim_n 0 = 0$$
using $[H_n, P] = 0$ (exact) and $P$ bounded. $\square$

## Missing Piece

The eigenvectors of $D|_H$ are **automorphic forms** on $C_Q$:
- Hecke-Maass cusp forms (discrete spectrum)
- Eisenstein series (continuous spectrum, quotiented out in $H$)

To complete Step 2a: prove that the eigenvectors of $H_n$ (block-diagonal in $P$-basis)
converge to Hecke-Maass forms in $L^2(C_Q)/V$.

This connects the UCA framework to the **Langlands program**.

## Step 2c

$\mathrm{Spec}(D|_H) = \{\gamma_n\}$ requires identifying which automorphic forms
have $L$-functions with zeros at $\{\frac{1}{2} + i\gamma_n\}$.

For $\zeta(s)$: this is the trivial automorphic representation of $GL(1)$.
The statement $\mathrm{Spec}(D|_H) = \{\gamma_n\}$ is equivalent to:
the only automorphic $L$-function contributing to $\mathrm{Spec}(D|_H)$ is $\zeta(s)$.

This is a **uniqueness statement** in the Langlands program.
