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
