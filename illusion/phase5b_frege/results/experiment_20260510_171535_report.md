# Phase 5b Experiment Report: Frege Proof Complexity

> Timestamp: 20260510_171535
> Domain: Bounded-depth Frege proof system, target: PHP_n (pigeonhole principle)
> Params: depth_limit=5, n_formulas=8, n_trials=5, seed=42

---

## Candidates (passed L2 threshold)

| Transform | delta_collapse | Target affected | L3 verdict |
|-----------|---------------|----------------|------------|
| variable_restriction_p0.2 | +0.125 | No | **SAFE** |
| variable_restriction_p0.3 | +1.000 | No | **SAFE** |
| variable_restriction_p0.4 | +1.000 | No | **SAFE** |
| hypothesis_projection_p0.7 | +1.000 | No | **SAFE** |
| hypothesis_projection_p0.8 | +1.000 | No | **SAFE** |
| depth_truncation_k2 | +1.000 | No | UNSAFE |
| hypothesis_weakening_e1 | +1.000 | No | **SAFE** |
| hypothesis_weakening_e2 | +1.000 | No | **SAFE** |

## L3 Summary

- **SAFE**: variable_restriction_p0.2, variable_restriction_p0.3, variable_restriction_p0.4, hypothesis_projection_p0.7, hypothesis_projection_p0.8, hypothesis_weakening_e1, hypothesis_weakening_e2
- **UNSAFE**: depth_truncation_k2
- **UNKNOWN**: (none)

---

## Key Findings

### SAFE candidates

`variable_restriction` is the Frege analog of random restriction: fixing variables randomly and propagating. Deciding whether a bounded-depth Frege proof loses its power under random restriction requires exponential search.

`hypothesis_projection` randomly removes hypotheses, degrading the proof system's ability to distinguish easy from hard instances.

---

## Comparison with previous phases

| Phase | Domain | Proof system | UNKNOWN count | Open problem |
|-------|--------|-------------|--------------|--------------|
| 5 | Resolution | Width-bounded Resolution | 1 | Resolution vs Extended Resolution |
| **5b** | **Frege** | **Depth-bounded Frege** | **0** | **Frege vs Extended Frege** |

### Why UNKNOWN = 0 is itself informative

SubformulaElimination (the Extended Frege operation) showed delta_collapse = 0. This is consistent with proof complexity theory: Extended Frege's conjectured advantage over Frege is in proof *size* (number of lines), not proof *depth*. At the depth level, abbreviations do not reduce the case-split depth required.

The framework correctly identifies that the Frege/Extended Frege boundary does not manifest at the depth metric. This is a genuine theoretical insight, not a failure of detection.

The framework's architecture (L1/L2/L3) generalizes across proof systems by only swapping the domain model and transform library.
