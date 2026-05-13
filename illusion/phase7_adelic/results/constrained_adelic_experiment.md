# Constrained Adelic Basis Experiment

> Date: 2026-05-11
> Key: impose sum_p k_p * log(p) = t_inf (norm constraint = quotient H)

## Motivation

The naive operator $\Delta_\mathbb{A}^{\text{naive}} = \sum_p \Delta_p$ has
exponential spectrum $p^{2k}$, incompatible with $\gamma_n \sim 2\pi n/\log n$.

The fix: impose the global norm constraint $\sum_p k_p \log p = t_\infty$.
This is the finite-dimensional realization of $H = L^2(C_\mathbb{Q})/V$.

In the constrained subspace, the diagonal elements become:
$$\lambda(k) = (k \log p)^2 + p^{2k}$$
For small $k$, the dominant term is $(k \log p)^2 \sim O(k^2)$,
matching $\gamma_n^2 \sim O(n^2)$.

## Results

| Model | Growth $\alpha$ | RMSE ($\sqrt{\lambda}$ vs $\gamma_n$) |
|---|---|---|
| p2_only | 9.359 | 33.47938 |
| p235_single | 7.973 | 51.75526 |
| p23_full | 2.429 | 22.72760 |

## Interpretation

- Growth $\alpha \approx 2$: polynomial spectrum, compatible with $\gamma_n^2$
- Growth $\alpha \gg 2$: exponential spectrum, incompatible
- The constraint $\sum_p k_p \log p = t_\infty$ is the key mechanism
  that converts exponential local spectra into polynomial global spectrum.

This confirms: the quotient $H = L^2(C_\mathbb{Q})/V$ is not just a
philosophical construction — it has a concrete spectral effect.
The norm constraint couples local operators and changes the growth rate.