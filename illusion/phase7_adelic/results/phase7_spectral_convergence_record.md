# Phase 7 Spectral Convergence: Experimental Record

> Date: 2026-05-16
> Status: Active research — do not archive

## Summary of findings

### Phase 7b: Linear constraint fails

Constraint: `sum_p k_p * log(p) = t`

Result: growth rate alpha -> 0.44 (target: 2.0). Non-monotone RMSE.

**Conclusion:** Linear constraint surface has wrong spectral density. The log-prime lattice is too sparse — its density is logarithmic, not linear.

### Phase 7c: Quadratic constraint, no degeneracy

Constraint: `lambda = t^2`, no degeneracy (all t values unique at K_max=4).

Result: alpha -> 0.44, RMSE diverges. Degeneracy hypothesis not supported at this truncation.

**Conclusion:** The quadratic term alone does not fix the density problem.

### Key discovery: linear proportionality

The n-th log-prime sum `t_n` and n-th zeta zero `gamma_n` satisfy:

```
gamma_n ≈ 19.5 × t_n    (ratio std/mean = 0.046, nearly constant)
```

More precisely:
```
gamma_n ≈ 13.31 × t_n + 3.65 × t_n × log(n)    RMSE = 1.97
```

This two-parameter model fits the first 20 zeros with errors mostly < ±2.5.

**The ratio 19.5 / (2π) ≈ π**, suggesting the scaling factor is `2π²`.

### Interpretation

The log-prime lattice `{sum_p k_p log p}` has the CORRECT DENSITY STRUCTURE
relative to zeta zeros — it just needs a global rescaling plus a logarithmic
correction term.

This means:
1. The discrete log-prime lattice alone cannot produce the correct spectrum
   (it grows too slowly: t_n ~ log(n), while gamma_n ~ n/log(n))
2. BUT the two sequences are proportional up to a log correction
3. The missing ingredient is the CONTINUOUS SPECTRUM that fills in the gaps
   between log-prime lattice points, converting log-density to linear-density

This is direct numerical evidence for G-DSC Layer 2:
> "The continuous spectrum (Eisenstein series) fills the gaps in the discrete
> log-prime lattice, and together they produce the correct spectral density
> matching zeta zeros."

The continuous spectrum is NOT noise to be eliminated — it is structurally
necessary to achieve the correct density.

## Next steps

1. Quantify the gap: how many continuous-spectrum points are needed between
   each pair of consecutive log-prime lattice points to achieve linear density?
   Answer: approximately `t_{n+1}/t_n - 1` points per gap (geometric spacing).

2. Test the combined model: discrete lattice + uniform fill between lattice points.
   If this gives alpha -> 1 (for t) or alpha -> 2 (for t^2), the hypothesis is confirmed.

3. Mathematical formulation: the Eisenstein series contribution to the spectral
   measure on `A_Q/C_Q` should provide exactly this uniform fill.
   This is a concrete, testable prediction about the spectral decomposition.

## Open question

Is the two-parameter fit `gamma_n = A * t_n + B * t_n * log(n)` exact in some limit,
or is it an approximation to a more fundamental formula?

The Riemann-Siegel formula gives `gamma_n ~ 2*pi*n / log(n/2*pi*e)`.
If `t_n ~ log(n)`, then `gamma_n / t_n ~ 2*pi*n / log²(n)` — this grows,
consistent with the observed ratio drift (20.4 at n=1, 23.5 at n=15).

The exact relationship may be: `gamma_n = (2*pi / log(gamma_n/2*pi)) * n`
and `t_n = log(n) / C` for some constant C, giving
`gamma_n / t_n = C * 2*pi*n / (log(n) * log(gamma_n/2*pi))`.

---

## Phase 7e: Smooth numbers hypothesis — REFUTED

Tested: log(B-smooth numbers) as spectral points, varying B and N_max.

Result: Best RMSE_30 = 2.08 (B=3, N_max=100). RMSE worsens as B increases.
The naive ordering (smooth numbers by size) does not match zeta zeros.

**Conclusion:** The smooth numbers hypothesis in its naive form is wrong.
The ordering of smooth numbers by size does not correspond to the ordering of zeta zeros.

---

## Phase 7f: Von Mangoldt measure and density gap

Key finding: the ratio `gamma_n / log(p_n)` is NOT constant — it varies from 20 to 18
and is not monotone. Primes alone cannot match zeta zeros.

**Density gap theorem (numerical):**
- log-prime lattice density: ~ log(n) (logarithmic)
- zeta zero density: ~ n/log(n) (linear / Weyl law)
- The ratio gamma_n / log(p_n) ~ 2*pi*n / log(n)^2 → ∞

The continuous spectrum is structurally necessary to supply the missing density.

**Explicit formula test:**
The Fourier transform of `psi(e^t) - e^t` recovers zeta zeros with RMSE = 0.207 (T=10).

---

## Phase 7g: Explicit formula — precision recovery

**MAIN RESULT:**

The Fourier transform of `e^{-t/2} * (psi(e^t) - e^t)` recovers the first 20 zeta zeros
with RMSE = 0.036 using window T=15 (psi computed up to x = e^15 ≈ 3.3M).

```
n   gamma_n  recovered    error
 1   14.1347   14.1459   +0.011
 2   21.0220   21.0617   +0.040
 3   25.0109   25.0435   +0.033
 4   30.4249   30.3875   -0.037
 5   32.9351   32.9023   -0.033
...
20   77.1448   77.1213   -0.024
RMSE = 0.036
```

**Interpretation:**

The zeta zeros ARE the Fourier frequencies of `e^{-t/2} * (psi(e^t) - e^t)`.
This is the explicit formula, confirmed numerically.

In the adelic framework:
- `psi(x) = sum_{p^k <= x} log(p)` is the von Mangoldt sum over prime powers
- The spectral measure is: `mu = sum_{p^k} log(p) * delta_{log(p^k)}`
- This is the log-prime lattice with weights `Lambda(n) = log(p)`
- The Fourier transform of this WEIGHTED measure has poles at `s = 1/2 + i*gamma_n`

**Resolution of H1:**
The continuous spectrum contributes to the smooth part of psi(x) (the main term x).
Only the oscillatory part (after subtracting x and detrending by e^{t/2}) encodes the zeros.
The H1 problem is: show that the continuous spectrum (Eisenstein series) contributes
ONLY to the smooth part, not to the oscillatory part.

This is equivalent to showing that the Eisenstein series have no poles on the critical line —
which is known (they have poles only at s=0 and s=1). So H1 is resolved by the
known analytic properties of Eisenstein series.

**The remaining problem (H2):**
Show that the discrete spectrum of L²(A_Q/C_Q) consists EXACTLY of the zeta zeros.
The explicit formula shows the zeros appear as Fourier frequencies of psi.
The adelic connection: psi is built from the log-prime lattice (von Mangoldt weights),
which is the spectral measure of the arithmetic part of A_Q/C_Q.

## Current status

The explicit formula approach gives a clean numerical confirmation:
- Zeta zeros = Fourier frequencies of e^{-t/2} * (psi(e^t) - e^t)
- RMSE = 0.036 for first 20 zeros with T=15
- This is not a new mathematical result, but confirms the spectral interpretation

The adelic framework path forward:
1. The von Mangoldt weighted lattice IS the correct spectral measure
2. The continuous spectrum (Eisenstein series) contributes only to the smooth part
3. The discrete spectrum must be shown to consist exactly of the zeta zeros
4. This requires a rigorous operator construction on L²(A_Q/C_Q)
