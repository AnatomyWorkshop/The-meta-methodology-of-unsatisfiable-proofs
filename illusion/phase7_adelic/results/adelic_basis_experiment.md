# Minimal Adelic Basis Experiment

> Date: 2026-05-11
> Operator: $\Delta_\mathbb{A} = \Delta_2 \otimes I + I \otimes \Delta_\infty$
> Basis: $p=2$, $N=3$ (Vladimirov eigenbasis) $\times$ Hermite functions

## Key distinction from Phase 6

Phase 6 approximated $D$ (dilation generator, first-order, continuous spectrum).
This experiment approximates $\Delta_\mathbb{A}$ (adelic Vladimirov, second-order).
The relation is $\Delta_\mathbb{A} = e^{2D}$.

## Results

| M | dim | RMSE | Rel. Hecke commutator | Mean overlap |
|---|---|---|---|---|
| 5 | 75 | 12.10415 | 0.959540 | 0.050000 |
| 10 | 150 | 12.10415 | 0.869445 | 0.050000 |
| 20 | 300 | 12.10415 | 0.714914 | 0.050000 |

## Comparison with sin-basis (Phase 6, n=100)

| Metric | Sin-basis | Adelic (M=10) |
|---|---|---|
| RMSE | 0.00011 | 12.10415 |
| Rel. Hecke commutator | 1.446 | 0.869445 |
| Mean overlap with $\phi_0$ | 0.077 | 0.050000 |

## Interpretation

If the adelic basis gives rel. commutator $\ll 1$ and mean overlap $\gg 0.077$:
→ Confirms sin-basis is the wrong function space
→ $\Delta_\mathbb{A}$ in the correct basis satisfies Hecke commutativity
→ Supports Proposition 1 and Theorem 2 numerically

If not: the minimal adelic model needs refinement (larger $N$, better $\Delta_\infty$).