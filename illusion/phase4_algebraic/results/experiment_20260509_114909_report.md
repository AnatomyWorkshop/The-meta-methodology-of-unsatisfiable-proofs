# Phase 4d Experiment Report - 2026-05-09

## Parameters
Domain: algebraic circuits over GF(7), target: 3x3 Permanent over GF(7)
n=3, p=7, depth=3, circuits=20, samples=300, seed=42

## Candidates (sorted by delta-collapse)

| Rank | Transform | Delta | Before | After | Perm Affected | L3 Verdict |
|------|-----------|-------|--------|-------|---------------|------------|
| 1 | algebraic_restriction_p0.5 | +0.115 | 0.864 | 0.979 | False | **SAFE** |
| 2 | field_reduction_q2 | +0.105 | 0.859 | 0.964 | False | **UNSAFE** |
| 3 | algebraic_restriction_p0.3 | +0.104 | 0.866 | 0.970 | False | **SAFE** |

## Rejected by L2

| Transform | Delta | Reason |
|-----------|-------|--------|
| degree_truncation_d1 | +0.141 | permanent affected |
| algebraic_restriction_p0.7 | +0.132 | permanent affected |
| monomial_elimination_p0.5 | +0.128 | permanent affected |
| monomial_elimination_p0.7 | +0.098 | permanent affected |
| scalar_multiplication | +0.004 | low delta (+0.004) |
| identity | -0.008 | low delta (-0.008) |
| input_permutation | -0.008 | low delta (-0.008) |
| degree_truncation_d2 | -0.038 | low delta (-0.038) |

## L3 Verdicts

- **algebraic_restriction_p0.5**: SAFE (high) - random algebraic restriction (p ≤ 0.6) preserves the Permanent structure but degrades circuit distinguishing power; deciding whether a circuit loses distinguishing advantage under random variable fixing requires evaluating the circuit on exponentially many restricted inputs — this is the algebraic analog of the Razborov-Smolensky method
- **field_reduction_q2**: UNSAFE (high) - reducing inputs modulo q is a local operation on each variable; deciding whether a circuit's output changes under field reduction is decidable by an algebraic circuit of polynomial size
- **algebraic_restriction_p0.3**: SAFE (high) - random algebraic restriction (p ≤ 0.6) preserves the Permanent structure but degrades circuit distinguishing power; deciding whether a circuit loses distinguishing advantage under random variable fixing requires evaluating the circuit on exponentially many restricted inputs — this is the algebraic analog of the Razborov-Smolensky method

## Summary
- Transforms evaluated: 11
- L2 candidates: 3
- L2 rejected: 8
- L3 SAFE: 2
- L3 UNSAFE: 1
- L3 UNKNOWN: 0

## Framework Interpretation

The algebraic restriction transform (if SAFE) is the algebraic analog of:
- Phase 1: Håstad's random restriction (AC⁰ lower bounds)
- Phase 3: Razborov's approximation method (monotone circuit lower bounds)
- Phase 4d: Razborov-Smolensky method (algebraic circuit lower bounds)

If `algebraic_restriction` is SAFE and `field_reduction`/`scalar_multiplication` are UNSAFE,
this confirms the SRS framework's prediction: the discriminating property for Permanent
is not decidable within algebraic P/poly — consistent with Valiant's 1979 hardness result.
