# Experiment Report - 2026-05-04 16:47

## Parameters
n=8, depth=3, circuits=50, samples=2000, seed=42
Baseline error on PARITY: 0.499

## Candidates (sorted by delta-collapse)

| Rank | Transform | Delta | Before | After | Error | L3 Verdict | L3 Reason |
|------|-----------|-------|--------|-------|-------|------------|-----------|
| 1 | exhaustive_parity_equivalent_check | +0.115 | 0.885 | 1.000 | 0.496 | **UNSAFE** | deciding PARITY-equivalence requires enumerating all 2^n inp... |
| 2 | random_restriction | +0.080 | 0.889 | 0.969 | 0.499 | **SAFE** | deciding whether a circuit collapses under random restrictio... |
| 3 | random_restriction | +0.058 | 0.887 | 0.945 | 0.502 | **SAFE** | deciding whether a circuit collapses under random restrictio... |

## Rejected by L2

| Transform | Delta | Reason |
|-----------|-------|--------|
| gate_substitution | +0.113 | PARITY affected |
| gate_substitution | +0.100 | PARITY affected |
| input_negation | +0.008 | low delta-collapse (+0.008) |
| random_restriction | +0.007 | low delta-collapse (+0.007) |
| identity | +0.005 | low delta-collapse (+0.005) |
| input_permutation | -0.002 | low delta-collapse (-0.002) |
| depth_reduction | -0.133 | PARITY affected |

## L3 Review Queue

- [x] exhaustive_parity_equivalent_check => UNSAFE
- [o] random_restriction => SAFE
- [o] random_restriction => SAFE

## Summary
- Total transforms evaluated: 10
- Candidates passed to L3: 3
- Rejected by L2: 7
- L3 SAFE: 2
- L3 UNSAFE: 1
- L3 UNKNOWN (needs human review): 0
