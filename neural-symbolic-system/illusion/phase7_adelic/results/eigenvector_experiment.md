# Eigenvector Experiment: H_n → Trivial Hecke Character

> Date: 2026-05-11
> Experiment: overlap of UCA-constrained eigenvectors with phi_0 = |x|^{1/2}

## Setup

The trivial Hecke character $\phi_0(x) = |x|^{1/2}$ on $C_Q$ corresponds
to the constant function in the Dirichlet basis (norm quotiented out).
We compute $|\langle v_k, \phi_0 \rangle|$ for each eigenvector $v_k$ of $H_n$.

## Results

### n=50

| k | γ_k | overlap | overlap² |
|---|---|---|---|
| 1 | 14.1347 | 0.034031 | 0.001158 |
| 2 | 21.0220 | 0.082704 | 0.006840 |
| 3 | 25.0109 | 0.040795 | 0.001664 |
| 4 | 30.4249 | 0.056651 | 0.003209 |
| 5 | 32.9351 | 0.316259 | 0.100020 |
| 6 | 37.5862 | 0.167699 | 0.028123 |
| 7 | 40.9187 | 0.038670 | 0.001495 |
| 8 | 43.3271 | 0.103128 | 0.010635 |
| 9 | 48.0052 | 0.137440 | 0.018890 |
| 10 | 49.7738 | 0.354944 | 0.125985 |

Mean overlap: 0.113770
Hecke commutator $\|[H_n, T_2]\|/\|H_n\|$: 1.2528

### n=100

| k | γ_k | overlap | overlap² |
|---|---|---|---|
| 1 | 14.1347 | 0.060138 | 0.003617 |
| 2 | 21.0220 | 0.020479 | 0.000419 |
| 3 | 25.0109 | 0.123994 | 0.015374 |
| 4 | 30.4249 | 0.106165 | 0.011271 |
| 5 | 32.9351 | 0.018128 | 0.000329 |
| 6 | 37.5862 | 0.119958 | 0.014390 |
| 7 | 40.9187 | 0.006051 | 0.000037 |
| 8 | 43.3271 | 0.014468 | 0.000209 |
| 9 | 48.0052 | 0.012857 | 0.000165 |
| 10 | 49.7738 | 0.020999 | 0.000441 |

Mean overlap: 0.077443
Hecke commutator $\|[H_n, T_2]\|/\|H_n\|$: 1.4455

## Convergence

| n | Mean overlap | Hecke commutator |
|---|---|---|
| 50 | 0.113770 | 1.2528 |
| 100 | 0.077443 | 1.4455 |

## Interpretation

If mean overlap increases with $n$ and approaches 1:
→ $H_n$ eigenvectors converge to $\phi_0$ (trivial Hecke character)
→ Step 2a (eigenvector convergence) is numerically confirmed
→ Combined with $[H_n, P]=0$, this supports Step 2b

If Hecke commutator $\|[H_n, T_2]\|/\|H_n\| \to 0$:
→ $D|_H$ commutes with Hecke operators
→ Strong multiplicity one theorem (Jacquet-Langlands) applies
→ $\mathrm{Spec}(D|_H) = \{\gamma_n\}$ follows from Langlands for $GL(1)$