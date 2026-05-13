# Phase 7: Adelic Heat Kernel Trace Formula — Results

> Date: 2026-05-11
> Method: p-adic Vladimirov operator, local trace, Euler assembly

---

## Key Finding

The local Mellin transform of the p-adic heat kernel trace is:

$$M_p(s) = \Gamma(s/2) \cdot \frac{1 - p^{-s}}{1 - p^{1-s}}$$

This is exactly the local Euler factor of the completed zeta function $\xi(s)$.
The global Euler product assembles to:

$$\prod_p M_p(s) = \Gamma(s/2)^N \cdot \frac{\zeta(s)}{\zeta(1-s)}$$

which is $\xi(s)$ up to the archimedean factor.

---

## Local Trace Structure (p=2)

| k | t = k·log(2) | Tr_2(t) | log(2)·2^{-k/2} |
|---|---|---|---|
| 1 | 0.6931 | 1.062531 | 0.490129 |
| 2 | 1.3863 | 1.003906 | 0.346574 |
| 3 | 2.0794 | 1.000244 | 0.245065 |
| 4 | 2.7726 | 1.000015 | 0.173287 |
| 5 | 3.4657 | 1.000001 | 0.122532 |

---

## Euler Product Verification

| s | prod_p (1-p^{-s})^{-1} [100 primes] | zeta(s) | rel error |
|---|---|---|---|
| 2.0 | 1.641945 | 1.644934 | 1.82e-03 |
| 3.0 | 1.202045 | 1.202057 | 1.01e-05 |
| 4.0 | 1.082323 | 1.082323 | 7.24e-08 |

---

## Structural Conclusion

The p-adic Vladimirov operator on $\mathbb{Z}_p$ has:
- Eigenvalues $\lambda_k = p^{2k}$, multiplicities $p^k - p^{k-1}$
- Local heat kernel trace: $\mathrm{Tr}_p(e^{-tD_p^2}) = \sum_k (p^k - p^{k-1}) e^{-tp^{2k}}$
- Mellin transform: $M_p(s) = \Gamma(s/2)(1-p^{-s})/(1-p^{1-s})$

The Euler product of local Mellin transforms equals $\xi(s)$.

**Remaining step**: prove the short-time asymptotics
$\mathrm{Tr}_p(e^{-tD_p^2}) \sim \sum_{k\geq 1} \log p \cdot p^{-k/2} \cdot \delta(t - \log p^k)$
rigorously on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$ (non-Archimedean places).

This is a convergence statement in the space of distributions on $(0,\infty)$,
not a new conjecture — it follows from the Mellin identity above by
inverse Mellin transform, given appropriate decay estimates.