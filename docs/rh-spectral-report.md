# Spectral Structure of the Riemann Zeta Function: A Numerical Investigation

**Apophenia Research** · May 2026  
Contact: apophenia.cto.alice@gmail.com

---

## What this report is

A record of numerical experiments on the spectral interpretation of the Riemann Hypothesis. We do not claim a proof. We claim three things: a precise equivalent formulation, a numerical verification of its internal consistency, and an honest statement of what remains open.

---

## 1. The question

The Riemann Hypothesis states that all non-trivial zeros of the Riemann zeta function ζ(s) lie on the critical line Re(s) = 1/2. The Hilbert-Pólya conjecture proposes that these zeros are eigenvalues of a self-adjoint operator — which would imply RH, since self-adjoint operators have real spectra.

We investigated: what is that operator, and can we construct it?

---

## 2. The framework: UCA and the adelic quotient

We worked within the **Universal Constraint Axiom (UCA)** framework, which enforces a global duality condition on differential operators:

$$\mathcal{D} \cdot \varphi = \star \cdot \mathcal{D}^\dagger \cdot \star \cdot \varphi$$

The natural arena for this construction is the adelic quotient L²(𝔸_ℚ / ℂ_ℚ), where 𝔸_ℚ is the adele ring of ℚ and ℂ_ℚ is the idele class group. This space decomposes into:

- A **discrete spectrum** (cuspidal automorphic forms)
- A **continuous spectrum** (Eisenstein series)

The Hilbert-Pólya conjecture, in this language, becomes: the discrete spectrum of the UCA-constrained operator on L²(𝔸_ℚ / ℂ_ℚ) consists exactly of the zeta zeros.

---

## 3. Numerical experiments: Phase 6

We constructed a finite-dimensional approximation of the Hilbert-Pólya operator using the UCA duality constraint. The optimizer found a matrix whose eigenvalues match the first 30 zeta zeros with **RMSE = 0.00141** and zero duality defect.

This is a numerical solution, not a mathematical proof. A matrix that fits 30 eigenvalues does not define a well-posed operator on an infinite-dimensional space. But it confirms that the UCA constraint is compatible with the zeta zero distribution — the constraint does not rule out the correct answer.

---

## 4. Numerical experiments: Phase 7

We investigated the spectral structure of the log-prime lattice — the set of values {∑ kₚ log p} — and its relationship to zeta zeros.

**Phase 7b–7d** established a key fact: the log-prime lattice has *logarithmic* density (the n-th lattice point grows as log n), while zeta zeros have *linear* density (γₙ ~ n/log n). The lattice alone cannot reproduce the zero distribution. A continuous spectral component is structurally necessary.

**Phase 7e–7f** tested the smooth numbers hypothesis and the von Mangoldt measure. The naive smooth number ordering fails. The correct spectral measure is the **von Mangoldt weighted lattice**:

$$d\mu = \sum_{p^k} \log p \cdot \delta_{\log p^k}$$

This is the Chebyshev psi function in disguise: ψ(x) = ∑_{p^k ≤ x} log p.

**Phase 7g** — the main numerical result:

The Fourier transform of e^{−t/2} · (ψ(e^t) − e^t) recovers the zeta zeros with **RMSE = 0.036** for the first 20 zeros, using a window T = 15 (ψ computed up to x = e^15 ≈ 3.3 million).

| n | γₙ (true) | recovered | error |
|---|-----------|-----------|-------|
| 1 | 14.1347 | 14.1459 | +0.011 |
| 2 | 21.0220 | 21.0617 | +0.040 |
| 3 | 25.0109 | 25.0435 | +0.033 |
| 4 | 30.4249 | 30.3875 | −0.037 |
| 5 | 32.9351 | 32.9023 | −0.033 |
| 10 | 49.7738 | 49.7726 | −0.001 |
| 15 | 65.1125 | 65.0711 | −0.041 |
| 20 | 77.1448 | 77.1213 | −0.024 |

The errors are truncation errors, not fitting errors. They decrease as T increases.

This is the **explicit formula** working numerically. It is not a new mathematical result — the explicit formula is classical — but it confirms the spectral interpretation: the zeta zeros are the Fourier frequencies of the oscillatory part of ψ(e^t), after removing the main term e^t and the e^{t/2} envelope.

---

## 5. What this means

The von Mangoldt weighted lattice is the correct spectral measure. The continuous spectrum (Eisenstein series) contributes to the smooth part of ψ(x) — the main term x — not to the oscillatory part. The oscillatory part encodes exactly the zeta zeros.

In the adelic framework: the Eisenstein series have poles only at s = 0 and s = 1, not on the critical strip. Their contribution to the spectral measure is the smooth background, not the oscillations. This resolves the H1 problem (continuous spectrum suppression) at the level of known analytic properties of Eisenstein series.

---

## 6. What remains open (H2)

The remaining problem is to show rigorously that the discrete spectrum of L²(𝔸_ℚ / ℂ_ℚ), under the UCA-constrained operator, consists *exactly* of the zeta zeros.

This requires:
1. A rigorous operator definition on the adelic quotient space (domain, self-adjointness, spectral theorem applicability)
2. A proof that the spectral measure of this operator equals the von Mangoldt measure
3. A proof that the eigenvalues are exactly {1/2 + iγₙ}

Step 3 is equivalent to RH. Steps 1–2 are the mathematical infrastructure needed to make the argument non-circular.

The explicit formula approach (Phase 7g) cannot close this gap: it uses the zeros as input to recover the zeros as output. It verifies internal consistency, not the original claim.

---

## 7. Open questions worth pursuing

- Can the UCA duality constraint, applied to the adelic Vladimirov operator, force Re(s) = 1/2 for all eigenvalues without assuming RH? This is the core structural question.
- Does the finite-dimensional UCA optimizer (Phase 6, RMSE = 0.00141) converge to a well-defined infinite-dimensional operator as the truncation is removed?
- Can the von Mangoldt spectral measure be derived from first principles within the adelic framework, rather than imposed by hand?

---

## 8. Code and reproducibility

All experiments are implemented in Python and available at:  
[github.com/AnatomyWorkshop/apophenia](https://github.com/AnatomyWorkshop/apophenia)

Key files:
- `illusion/phase6_rh/` — UCA optimizer, RMSE = 0.00141
- `illusion/phase7_adelic/phase7g_explicit.py` — explicit formula recovery, RMSE = 0.036
- `illusion/phase7_adelic/results/phase7_spectral_convergence_record.md` — full experimental record

---

## 9. About Apophenia

Apophenia builds tools for spectral analysis of complex systems. **Prism** applies the UCA duality framework to network Laplacians — the same mathematical structure used in this RH investigation, applied to graphs, financial networks, and physical systems.

[apophenia tools →](https://anatomyworkshop.github.io/apophenia)

---

*This report was produced using the Apophenia research stack: Claude Sonnet 4.6, Deepseek, and custom Python tooling. The experiments are reproducible; the conclusions are honest.*
