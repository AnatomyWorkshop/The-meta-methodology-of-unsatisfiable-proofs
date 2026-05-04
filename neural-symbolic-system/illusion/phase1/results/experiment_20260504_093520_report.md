# Experiment Report — 2026-05-04 09:35

## Parameters
n=8, depth=3, circuits=50, samples=2000, seed=42
Baseline error on PARITY: 0.499

## Candidates (sorted by collapse score)

| Rank | Transform | Collapse | Error | L3 Verdict | L3 Reason |
|------|-----------|----------|-------|------------|-----------|
| 1 | exhaustive_parity_equivalent_check | 1.000 | 0.500 | **UNSAFE** | deciding PARITY-equivalence requires enumerating all 2^n inp... |
| 2 | random_restriction | 0.969 | 0.503 | **SAFE** | deciding whether a circuit collapses under random restrictio... |
| 3 | random_restriction | 0.940 | 0.500 | **SAFE** | deciding whether a circuit collapses under random restrictio... |
| 4 | input_permutation | 0.892 | 0.500 | **UNSAFE** | the induced property (permutation invariance of f) is decida... |
| 5 | random_restriction | 0.879 | 0.505 | **SAFE** | deciding whether a circuit collapses under random restrictio... |

## Rejected by L2

| Transform | Reason |
|-----------|--------|
| gate_substitution | PARITY affected |
| gate_substitution | PARITY affected |
| depth_reduction | PARITY affected |

## L3 Review Queue

- [x] exhaustive_parity_equivalent_check => UNSAFE
- [o] random_restriction => SAFE
- [o] random_restriction => SAFE
- [x] input_permutation => UNSAFE
- [o] random_restriction => SAFE

## Summary
- Total transforms evaluated: 8
- Candidates passed to L3: 5
- Rejected by L2: 3
- L3 SAFE: 3
- L3 UNSAFE: 2
- L3 UNKNOWN (needs human review): 0
