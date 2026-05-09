# Phase 5 Experiment Report: Resolution Proof Complexity

> Timestamp: 20260509_194256
> Domain: Resolution proof system, target: PHP_n (pigeonhole principle)
> Params: width_limit=4, n_formulas=10, n_trials=5, seed=42

---

## Candidates (passed L2 threshold)

| Transform | delta_collapse | Target affected | L3 verdict |
|-----------|---------------|----------------|------------|
| clause_restriction_p0.2 | +0.600 | No | **SAFE** |
| clause_restriction_p0.4 | +0.780 | No | **SAFE** |
| clause_projection_p0.7 | +0.780 | No | **SAFE** |
| clause_projection_p0.8 | +0.780 | No | **SAFE** |
| variable_elimination_p0.2 | +0.640 | No | **UNKNOWN** |
| variable_elimination_p0.3 | +0.780 | No | **UNKNOWN** |

## L3 Summary

- **SAFE**: clause_restriction_p0.2, clause_restriction_p0.4, clause_projection_p0.7, clause_projection_p0.8
- **UNSAFE**: (none)
- **UNKNOWN**: variable_elimination_p0.2, variable_elimination_p0.3

---

## Key Findings

### UNKNOWN verdicts (Phase 5 primary target)

The following transforms have positive delta_collapse but L3 cannot determine decidability within Resolution:

**variable_elimination_p0.2** (delta_collapse=+0.640)

> variable elimination corresponds to existential quantification over proof variables; this relates to Extended Resolution — the separation between Resolution and Extended Resolution is an open problem in proof complexity. Cannot determine decidability within Resolution from current theory.

> Reference: Krajíček 1995, Proof Complexity; Cook & Reckhow 1979, Extended Resolution

**variable_elimination_p0.3** (delta_collapse=+0.780)

> variable elimination corresponds to existential quantification over proof variables; this relates to Extended Resolution — the separation between Resolution and Extended Resolution is an open problem in proof complexity. Cannot determine decidability within Resolution from current theory.

> Reference: Krajíček 1995, Proof Complexity; Cook & Reckhow 1979, Extended Resolution

UNKNOWN is not a failure. It is the system pointing at the boundary of current proof complexity theory.

### SAFE candidates

`clause_restriction` is the core operation of the Ben-Sasson-Wigderson width method: randomly fixing variables preserves the PHP width lower bound. L2 arrived at this without being told about Ben-Sasson-Wigderson.

`clause_projection` is the Resolution analog of subgraph projection: randomly retaining a subset of clauses degrades the proof system's distinguishing power.

---

## Comparison with previous phases

| Phase | Domain | UNKNOWN count | Significance |
|-------|--------|--------------|--------------|
| 1 | AC0 | 0 | Known domain, rule library sufficient |
| 3 | Monotone circuits | 0 | Known domain, rule library sufficient |
| 4d | Algebraic circuits | 0 | Known domain, rule library sufficient |
| **5** | **Resolution** | **2** | **Knowledge boundary reached** |
