# Phase 4d Experiment Report - 2026-05-09

## Parameters
Domain: algebraic circuits over GF(7), target: 3x3 Permanent over GF(7)
n=3, p=7, depth=3, circuits=20, samples=300, seed=42

## Candidates (sorted by delta-collapse)

| Rank | Transform | Delta | Before | After | Perm Affected | L3 Verdict |
|------|-----------|-------|--------|-------|---------------|------------|

## Rejected by L2

| Transform | Delta | Reason |
|-----------|-------|--------|
| degree_truncation_d2 | +0.029 | low delta (+0.029) |
| degree_truncation_d1 | +0.027 | permanent affected |
| monomial_elimination_p0.5 | +0.020 | permanent affected |
| monomial_elimination_p0.7 | +0.012 | permanent affected |
| algebraic_restriction_p0.7 | +0.008 | permanent affected |
| field_reduction_q2 | +0.006 | low delta (+0.006) |
| identity | +0.004 | low delta (+0.004) |
| algebraic_restriction_p0.5 | +0.003 | low delta (+0.003) |
| scalar_multiplication | +0.000 | low delta (+0.000) |
| input_permutation | -0.004 | low delta (-0.004) |
| algebraic_restriction_p0.3 | -0.010 | low delta (-0.010) |

## L3 Verdicts


## Summary
- Transforms evaluated: 11
- L2 candidates: 0
- L2 rejected: 11
- L3 SAFE: 0
- L3 UNSAFE: 0
- L3 UNKNOWN: 0

## Framework Interpretation

The algebraic restriction transform (if SAFE) is the algebraic analog of:
- Phase 1: Håstad's random restriction (AC⁰ lower bounds)
- Phase 3: Razborov's approximation method (monotone circuit lower bounds)
- Phase 4d: Razborov-Smolensky method (algebraic circuit lower bounds)

If `algebraic_restriction` is SAFE and `field_reduction`/`scalar_multiplication` are UNSAFE,
this confirms the SRS framework's prediction: the discriminating property for Permanent
is not decidable within algebraic P/poly — consistent with Valiant's 1979 hardness result.
