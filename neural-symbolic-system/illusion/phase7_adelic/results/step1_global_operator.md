# Step 1: Global Operator D on L²(C_Q)

## Definition

Let $C_Q = \mathbb{A}_\mathbb{Q}^\times / \mathbb{Q}^\times$ be the idele class group with Haar measure $d^*x$.

Define the one-parameter unitary group:
$$(U_t f)(x) = f(e^{-t} x), \quad t \in \mathbb{R}$$

By Stone's theorem, the generator
$$D = -i \frac{d}{d(\log|\cdot|)}$$
is self-adjoint on $L^2(C_Q, d^*x)$.

## Properties

**Self-adjoint**: Stone's theorem. ✓

**Local restrictions**: $D_p = -i\,d/d(\log|x|_p)$ on $L^2(\mathbb{Q}_p^\times)$.
The Vladimirov operator satisfies $\Delta_p^\alpha = p^{\alpha D_p / \log p}$ (exponential, not square). ✓

**Duality on full space**: $F D F^{-1} = -D$ (anticommutation).
$[D, F] \neq 0$ on $L^2(C_Q)$. ✗

**Duality on quotient**: Let $V = \ker(|\cdot|: C_Q \to \mathbb{R}_{>0})$ and $H = L^2(C_Q)/V$.
On $H$, the Fourier transform $F$ acts as the identity, so $[D, F] = 0$. ✓ (claimed)

## UCA Selection Principle

UCA requires $[D, \star] = 0$. On the full $L^2(C_Q)$, only $D^2$ satisfies this.
On the quotient $H$, $D$ itself satisfies UCA.

**UCA selects $H$ as the correct domain**: $H$ is the unique subspace of $L^2(C_Q)$
where duality compatibility holds for $D$ (not just $D^2$).

## Remaining Steps

- **Step 2a**: Prove $H$ is well-defined with $D$ self-adjoint on $H$
- **Step 2b**: Prove $[D, F] = 0$ on $H$
- **Step 2c**: Prove $\mathrm{Spec}(D|_H) = \{\gamma_n\}$ — the Hilbert-Polya conjecture
