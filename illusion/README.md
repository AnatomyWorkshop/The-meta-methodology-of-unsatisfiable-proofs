# Illusion

Computational system for structural diagnosis of proof barriers. Implements the L1/L2/L3 architecture across six mathematical domains.

## Running Experiments

Each phase is self-contained. To run:

```bash
cd phase6_rh
python run_experiment.py
```

## Phases

| Phase | Directory | Domain | Key file |
|-------|-----------|--------|----------|
| 2 | `phase2/` | AC0 circuits / PARITY | `run_experiment.py` |
| 3 | `phase3/` | Monotone circuits / CLIQUE | `run_experiment.py` |
| 4 | `phase4/` | Algebraic circuits / PERMANENT | `run_experiment.py` |
| 5 | `phase5/` | Resolution proof complexity | `run_experiment.py` |
| 5b | `phase5b/` | Frege depth complexity | `run_experiment.py` |
| 5c | `phase5c/` | Frege size complexity | `run_experiment.py` |
| 6 | `phase6_rh/` | Riemann Hypothesis | `run_experiment.py` |

## Architecture

```
L1 (Model)     — Domain-specific evaluator
L2 (Search)    — Finds discriminating transforms / closure operators
L3 (Classify)  — SAFE / UNSAFE / UNKNOWN verdict with structural reasoning
```

## Results

All experiment results are in `<phase>/results/`. Each run produces:
- `.json` — raw data
- `_report.md` — human-readable analysis

Cross-domain summary: [../cross-domain-diagnostic.md](../cross-domain-diagnostic.md)

## Papers

- [manifesto.md](papers/manifesto.md) — Framework overview
- [illusion-proof-complexity.md](papers/illusion-proof-complexity.md) — Proof complexity results
- [illusion-symbol-system.md](papers/illusion-symbol-system.md) — Formal specification
- [illusion-constructive-verification.md](papers/illusion-constructive-verification.md) — Experimental validation

## Dependencies

```
numpy
scipy
mpmath  (Phase 6 only)
```
