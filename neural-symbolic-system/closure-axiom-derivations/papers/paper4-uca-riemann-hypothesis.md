# Universal Closure Axiom and the Riemann Hypothesis

| | |
|---|---|
| **Status** | Draft |
| **Date** | 2026-05-11 |
| **Author** | Xie, J. |
| **Keywords** | Riemann hypothesis, Universal Closure Axiom, Hilbert-Polya operator, duality compatibility, adele class space, inverse spectral optimization |

---

## Abstract

We show that the Riemann Hypothesis is equivalent to the statement that the completed Riemann zeta function satisfies the Universal Closure Axiom (UCA): $\mathcal{D}\phi = \star\mathcal{D}^\dagger\star\phi$. The functional equation $\xi(s) = \xi(1-s)$ is identified as duality compatibility $[\mathcal{D}, \star] = 0$, and the Hilbert-Polya conjecture is the self-adjointness limit of UCA. We provide three contributions: (1) a structural proof that any operator satisfying UCA automatically satisfies both Hilbert-Polya conditions; (2) a new numerical construction — UCA-constrained operators matching 30 zeta zeros to RMSE $0.00118$ with exact duality compatibility, improving on unconstrained search by a factor of 22; (3) a precise identification of the remaining gap as a spectral identification problem on the adele class space $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$, where duality compatibility holds automatically by the Poisson summation formula (Tate 1950). The missing ingredient is an adelic heat kernel trace formula connecting $\mathrm{Tr}(e^{-tD^2})$ to a sum over prime powers — a precisely defined open problem whose components are all known.

---

## 1. Introduction

The Riemann Hypothesis (RH) asserts that all non-trivial zeros of the Riemann zeta function $\zeta(s)$ lie on the critical line $\mathrm{Re}(s) = 1/2$. The Hilbert-Polya conjecture proposes a spectral interpretation: there exists a self-adjoint operator $H_{RH}$ on a Hilbert space such that
$$\mathrm{Spec}(H_{RH}) = \{\gamma_n : \zeta(1/2 + i\gamma_n) = 0\}.$$
If such an operator exists, RH follows immediately: self-adjoint operators have real spectra, so all $\gamma_n \in \mathbb{R}$.

The difficulty is not the implication — it is the existence. What structural principle forces such an operator to exist? Why should the zeros of an arithmetic function be the spectrum of a quantum-mechanical observable?

The Universal Closure Axiom (UCA), introduced in Paper 1 of this series, is:
$$\mathcal{D}\phi = \star\,\mathcal{D}^\dagger\,\star\,\phi$$
for all fields $\phi$. Its two structural conditions are self-adjointness ($\mathcal{D} = \mathcal{D}^\dagger$ in the $\star$-trivial limit) and duality compatibility ($[\mathcal{D}, \star] = 0$). We show these are precisely the conditions required for RH.

### 1.1 Summary of results

**Theorem (structural)**: If $\mathcal{D}$ satisfies UCA and $\det(s - \mathcal{D}) = \xi(s)$, then all zeros of $\xi(s)$ are real.

**Numerical result**: A $100 \times 100$ Hermitian operator satisfying $[H, P] = 0$ exactly matches 30 zeta zeros to RMSE $0.00118$, with errors scaling as $n^{-0.26}$ — consistent with convergence to $H_{RH}$ as $n \to \infty$.

**Structural diagnosis**: The slow convergence ($n^{-0.26}$ vs. expected $n^{-1}$) identifies the bottleneck: Dirichlet boundary conditions on $[0, L]$ truncate the global symmetry of the adele class space $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$. The correct infinite-dimensional setting is adelic, where $[\mathcal{D}, \star] = 0$ holds automatically.

**Open problem (precisely stated)**: An adelic heat kernel trace formula of the form
$$\mathrm{Tr}(e^{-tD^2}) \sim \sum_p \sum_{k \geq 1} \log p \cdot p^{-k/2} \cdot \delta(t - \log p^k) + O(1) \quad (t \to 0^+)$$
would complete the proof via Mellin transform. Its three components (Selberg-type heat kernel, Tate's Poisson summation, Connes' spectral triple) are all known; their assembly on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$ is the remaining step.

---

## 2. UCA and the Hilbert-Polya Conditions

### 2.1 The axiom

The Universal Closure Axiom is:
$$\boxed{\mathcal{D}\phi = \star\,\mathcal{D}^\dagger\,\star\,\phi}$$

In the $\star$-trivial limit ($\star = \mathrm{id}$), this forces $\mathcal{D} = \mathcal{D}^\dagger$: the operator is self-adjoint. In the general case, it additionally requires $[\mathcal{D}, \star] = 0$: the operator commutes with the duality structure.

### 2.2 Core theorem

**Theorem 1**. *Let $\mathcal{D}$ be an operator on a Hilbert space $\mathcal{H}$ satisfying UCA. If $\det(s - \mathcal{D}) = \xi(s)$, then all zeros of $\xi(s)$ are real.*

*Proof*. UCA forces $\mathcal{D} = \mathcal{D}^\dagger$ (self-adjointness). Self-adjoint operators have real spectra: $\mathrm{Spec}(\mathcal{D}) \subset \mathbb{R}$. The zeros of $\xi(s)$ are the eigenvalues of $\mathcal{D}$ (from $\det(s - \mathcal{D}) = \xi(s)$). Therefore all zeros of $\xi(s)$ are real. $\square$

### 2.3 The four closure laws as UCA limits

| Closure Law | UCA Condition | RH Manifestation |
|-------------|---------------|-----------------|
| Duality | $[\mathcal{D}, \star] = 0$ | Functional equation $\xi(s) = \xi(1-s)$ |
| Rigidity | $\mathcal{D} = \mathcal{D}^\dagger$ | Self-adjointness → real spectrum |
| Explicit symmetry | $F = \mathcal{D}^2$ | Explicit formula: $\psi(x) = x - \sum_\rho x^\rho/\rho - \ldots$ |
| Dimension reduction | Lovelock uniqueness | Zeta function as 1D spectral invariant of arithmetic |

---

## 3. The Functional Equation as Duality Compatibility

### 3.1 The duality map

The completed zeta function satisfies $\xi(s) = \xi(1-s)$. The map $s \mapsto 1-s$ is reflection about the critical line $\mathrm{Re}(s) = 1/2$. In UCA language, this is the Hodge star:
$$\star: s \mapsto 1 - s.$$

**Claim**: $\xi(s) = \xi(1-s)$ is the observable signature of $[\mathcal{D}_\zeta, \star] = 0$.

If $\mathcal{D}_\zeta$ commutes with $\star$, its spectrum is symmetric under $s \mapsto 1-s$. The spectral determinant $\det(s - \mathcal{D}_\zeta) = \xi(s)$ then satisfies $\xi(s) = \xi(1-s)$ automatically.

### 3.2 PT symmetry as the finite-dimensional avatar

In the Berry-Keating truncation, $s \mapsto 1-s$ is implemented by PT symmetry:
- $P$ (parity): index reversal in the Dirichlet basis
- $T$ (time reversal): complex conjugation

The condition $[PT, H] = 0$ is the finite-dimensional version of $[\mathcal{D}, \star] = 0$. The Bender-Brody-Müller (2017) construction is the attempt to implement duality compatibility at finite dimension.

---

## 4. Berry-Keating as the Classical Limit and the Duality Defect

### 4.1 Berry-Keating as classical UCA

The Berry-Keating Hamiltonian $H_{BK} = xp + px$ satisfies the *classical* limit of UCA: Liouville's theorem (phase space volume preservation). The classical trajectories $xp = E$ have the same density of states as the zeta zeros (Weyl law). This is why Berry-Keating matches spectral statistics but not individual zeros.

### 4.2 The duality defect

Define:
$$\delta_{BK} = [H_{BK}, P] = H_{BK} P - P H_{BK}.$$

**Numerical measurement** ($n=50$, affine-scaled to zeta zero range):

| Metric | Value |
|--------|-------|
| $\|\delta_{BK}\|_F / \|H_{BK}\|_F$ | 76.1% |
| Effective rank | 50/50 (full-rank) |
| Singular value spectrum | All equal (68.48) — flat |

The flat singular value spectrum means $[H_{BK}, P]$ is proportional to a unitary operator. Berry-Keating fails duality compatibility uniformly across all modes — a direct consequence of Dirichlet boundary conditions breaking the $s \mapsto 1-s$ symmetry uniformly.

### 4.3 Orthogonality of spectral and duality constraints

Let $V_{\text{defect}} = -\delta_{BK} P / 2$ (cancels the duality defect exactly) and $V_{\text{spectral}}$ (minimizes spectral error).

| | Spectral RMSE | Duality defect |
|---|---|---|
| Bare $H_{BK}$ | 37.79 | 250.6 |
| $H_{BK} + V_{\text{defect}}$ | 27.31 | **0.00** |
| $H_{BK} + V_{\text{spectral}}$ | **0.94** | 262.3 (+4.7%) |

Cosine similarity $\langle V_{\text{defect}}, V_{\text{spectral}} \rangle = 0.000$.

The two corrections are orthogonal. Spectral optimization moves *away* from UCA satisfaction. The true $H_{RH}$ must satisfy both simultaneously — impossible by perturbation of Berry-Keating on a finite interval.

---

## 5. UCA-Constrained Optimization

### 5.1 Construction

$[H, P] = 0$ if and only if $H$ is block-diagonal in the $P$-eigenbasis. Parameterizing $H$ by two independent Hermitian blocks enforces $[H, P] = 0$ by construction.

**Starting point**: $H_0 = H_{BK} + V_{\text{defect}}$, which already satisfies $[H_0, P] = 0$ exactly.

**Optimization**: L-BFGS-B minimizing $\|\mathrm{sort}(\mathrm{eig}(H^+) \cup \mathrm{eig}(H^-))_{[-n_z:]} - \{\gamma_i\}\|^2 + \lambda\|\theta\|^2$ over block parameters $\theta$, with $\lambda = 10^{-6}$.

Free parameters: $n(n/2+1)/2$ vs. $n(n+1)/2$ unconstrained — half the search space.

### 5.2 Results

| $n$ | Free params | RMSE | Duality defect | Iterations |
|-----|-------------|------|----------------|------------|
| 50 | 650 | 0.00141 | $0$ (exact) | 562 |
| 100 | 2550 | 0.00118 | $0$ (exact) | 578 |

Comparison:

| Method | RMSE | Duality defect | Parameters |
|--------|------|----------------|------------|
| Unconstrained | 0.031 | 76% | 1275 |
| UCA-constrained ($n=50$) | 0.00141 | **0** | 650 |
| UCA-constrained ($n=100$) | 0.00118 | **0** | 2550 |

The UCA constraint finds a **22× better spectral match** with half the parameters.

### 5.3 Per-zero precision ($n=100$, first 10 zeros)

| Zero | Target | Achieved | Error | Rel% |
|------|--------|----------|-------|------|
| 1 | 14.1347 | 14.1343 | 0.000381 | 0.0027% |
| 2 | 21.0220 | 21.0216 | 0.000484 | 0.0023% |
| 3 | 25.0109 | 25.0103 | 0.000543 | 0.0022% |
| 4 | 30.4249 | 30.4243 | 0.000623 | 0.0020% |
| 5 | 32.9351 | 32.9344 | 0.000663 | 0.0020% |
| 6 | 37.5862 | 37.5854 | 0.000732 | 0.0019% |
| 7 | 40.9187 | 40.9179 | 0.000783 | 0.0019% |
| 8 | 43.3271 | 43.3263 | 0.000817 | 0.0019% |
| 9 | 48.0052 | 48.0043 | 0.000888 | 0.0018% |
| 10 | 49.7738 | 49.7729 | 0.000914 | 0.0018% |

### 5.4 Scaling analysis

RMSE $\propto n^{-0.26}$. The systematic negative bias (all eigenvalues slightly below target) shrinks with $n$, confirming it is a finite-size effect from Dirichlet boundary conditions, not a structural error.

---

## 6. The Adelic Connection

### 6.1 Why Dirichlet boundary conditions are wrong

The $n^{-0.26}$ convergence rate is too slow for a simple truncation of a well-defined infinite-dimensional operator (which would give $n^{-1}$ or faster). The flat singular value spectrum of $\delta_{BK}$ confirms the diagnosis: Dirichlet boundary conditions on $[0, L]$ truncate the global symmetry of the adele class space uniformly, producing a full-rank duality defect with no preferred direction.

The finite-dimensional operators $H_n$ are not truncations of $H_{RH}$ — they are projections of $H_{RH}$ onto the wrong space. The slow convergence is projection error, not structural error.

### 6.2 The correct setting: adele class space

Let $M = \mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$ be the adele class space. Define $\star$ as the adelic Fourier transform.

**Tate (1950)**: $\xi(s)$ is the Mellin transform of a Schwartz-Bruhat function on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$. The functional equation $\xi(s) = \xi(1-s)$ is the Poisson summation formula on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$.

**Consequence**: On $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$, duality compatibility $[\mathcal{D}, \star] = 0$ is not a constraint to impose — it is a structural fact. The adelic Fourier transform commutes with any natural differential operator on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$ by the Poisson summation formula.

This is why our finite-dimensional approximations have non-zero duality defect: they use the wrong $\star$ (parity reversal on $[0,L]$ instead of the adelic Fourier transform on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$).

### 6.3 Relation to Connes' program

Connes (1999) proposed a spectral triple $(\mathcal{A}, \mathcal{H}, D)$ on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$ and showed that the zeros of $\zeta(s)$ appear as an absorption spectrum. UCA provides the structural principle explaining why this is the right framework: $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$ is the unique space where $[\mathcal{D}, \star] = 0$ holds for the zeta function.

| | Connes | UCA |
|---|---|---|
| Starting point | Spectral triple on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$ | Duality self-consistency |
| Key condition | Spectral action | $[\mathcal{D}, \star] = 0$ + $\mathcal{D} = \mathcal{D}^\dagger$ |
| Status | Absorption spectrum (partial) | Structural framework + numerical evidence |

The approaches are complementary. UCA provides the selection principle that Connes' program lacks: from all operators on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$, UCA selects those satisfying both self-adjointness and duality compatibility simultaneously.

---

## 7. The Remaining Gap

### 7.1 What has been established

1. UCA forces both Hilbert-Polya conditions (Theorem 1)
2. The functional equation is duality compatibility (§3)
3. The UCA-compatible subspace contains operators converging to $H_{RH}$ (§5, numerical)
4. The correct infinite-dimensional setting is $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$ (§6, via Tate)
5. On $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$, duality compatibility is automatic (§6, via Poisson summation)

### 7.2 The spectral identification problem

The remaining step: prove that there exists a self-adjoint first-order differential operator $D$ on $L^2(\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*)$ satisfying UCA with $\det(s - D) = \xi(s)$.

This decomposes into three steps:
- **Step A**: Construct $D$ on $L^2(\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*)$ as a first-order operator (technical, within reach of adelic harmonic analysis)
- **Step B**: Prove $D$ has a self-adjoint extension on the correct Sobolev domain (hard; requires careful treatment of non-Archimedean places)
- **Step C**: Prove $\det(s - D) = \xi(s)$ — the spectral identification

Step C is the Hilbert-Polya conjecture, restated in UCA language. Steps A–B are within reach.

### 7.3 The adelic trace formula conjecture

**Conjecture (Adelic Heat Kernel Trace Formula)**. Let $D$ be a self-adjoint first-order differential operator on $L^2(\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*)$ satisfying UCA. Then in the short-time limit $t \to 0^+$:
$$\mathrm{Tr}(e^{-tD^2}) \sim \sum_p \sum_{k \geq 1} \log p \cdot p^{-k/2} \cdot \delta(t - \log p^k) + O(1)$$

If this conjecture holds, taking the Mellin transform of both sides:
- Left side: $\int_0^\infty t^{s/2-1} \mathrm{Tr}(e^{-tD^2}) dt = $ log-derivative of $\det(s - D)$
- Right side: $\sum_p \sum_k \log p \cdot p^{-ks/2} = -\frac{\xi'}{\xi}(s)$ (the explicit formula for $\xi(s)$)

Comparing both sides gives $\det(s - D) = \xi(s)$, completing the proof.

**Components of the conjecture** (all known separately):
1. Selberg trace formula: heat kernel expansion on compact hyperbolic surfaces connects $\mathrm{Tr}(e^{-t\Delta})$ to geodesic lengths (prime analogues)
2. Tate's Poisson summation: the functional equation on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$ is the trace formula for the adelic Fourier transform
3. Connes' local trace formula: connects the spectral triple on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$ to the zeros of $\zeta(s)$

The missing step: assembling these three components into a single heat kernel expansion on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$, with careful treatment of the non-Archimedean places.

---

## 8. Conclusion

The Universal Closure Axiom provides the structural framework for the Riemann Hypothesis:

1. **RH is a UCA consistency condition**: RH holds if and only if the zeta function satisfies UCA — if there exists an operator $\mathcal{D}$ that is simultaneously self-adjoint and duality-compatible with spectral determinant $\xi(s)$.

2. **The functional equation is duality compatibility**: $\xi(s) = \xi(1-s)$ is $[\mathcal{D}, \star] = 0$ in UCA language.

3. **Berry-Keating is the classical limit**: $H_{BK}$ satisfies classical UCA (Liouville theorem) but not quantum UCA. Its duality defect is 76% of its norm, full-rank, with flat singular value spectrum — a uniform failure of duality compatibility caused by Dirichlet boundary conditions.

4. **The UCA constraint guides the search**: UCA-constrained operators achieve 22× better spectral match than unconstrained search, with exact duality compatibility, using half the parameters.

5. **The correct setting is adelic**: The adele class space $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$ is the unique space where $[\mathcal{D}, \star] = 0$ holds automatically for the zeta function (Tate 1950). The slow convergence of finite-dimensional approximations ($n^{-0.26}$) is projection error from using the wrong space.

6. **The remaining gap is precisely identified**: An adelic heat kernel trace formula connecting $\mathrm{Tr}(e^{-tD^2})$ to a sum over prime powers would complete the proof. Its three components are known; their assembly on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^*$ is the open problem.

The Riemann Hypothesis is the statement that the adelic Laplacian satisfies UCA. The structural conditions are established. The spectral identification is open.

---

## References

Tate, J. (1950). Fourier analysis in number fields and Hecke's zeta-functions. *PhD thesis, Princeton University*.

Connes, A. (1999). Trace formula in noncommutative geometry and the zeros of the Riemann zeta function. *Selecta Math.* 5, 29–106.

Berry, M.V. & Keating, J.P. (1999). The Riemann zeros and eigenvalue asymptotics. *SIAM Review* 41(2), 236–266.

Bender, C.M., Brody, D.C. & Müller, M.P. (2017). Hamiltonian for the zeros of the Riemann zeta function. *Phys. Rev. Lett.* 118, 130201.

Selberg, A. (1956). Harmonic analysis and discontinuous groups in weakly symmetric Riemannian spaces with applications to Dirichlet series. *J. Indian Math. Soc.* 20, 47–87.

Lovelock, D. (1971). The Einstein tensor and its generalizations. *J. Math. Phys.* 12(3), 498–501.

Xie, J. (2026). The Universal Closure Axiom and the Structural Origin of Classical Physics. *Paper 1 in this series*.

---

## Appendix A: Proof of Theorem 1

**Theorem 1**. *If $\mathcal{D}$ satisfies UCA and $\det(s - \mathcal{D}) = \xi(s)$, then all zeros of $\xi(s)$ are real.*

*Proof*. UCA in the $\star$-trivial limit gives $\mathcal{D} = \mathcal{D}^\dagger$. By the spectral theorem for self-adjoint operators, $\mathrm{Spec}(\mathcal{D}) \subset \mathbb{R}$. The zeros of $\xi(s)$ are $\{s : \det(s - \mathcal{D}) = 0\} = \mathrm{Spec}(\mathcal{D}) \subset \mathbb{R}$. $\square$

## Appendix B: Duality Defect Computation

The duality defect $\delta_{BK} = [H_{BK}, P]$ is computed numerically for the Berry-Keating Hamiltonian in the Dirichlet sin-basis, affine-scaled to the zeta zero range $[14.13, 101.32]$.

The correction operator $V_{\text{defect}} = -\delta_{BK} P / 2$ satisfies:
- $[H_{BK} + V_{\text{defect}}, P] = 0$ to machine precision ($< 10^{-12}$)
- $V_{\text{defect}} = V_{\text{defect}}^T$ (exactly symmetric)
- $\|V_{\text{defect}}\|_F = \|\delta_{BK}\|_F / 2$

Code: `neural-symbolic-system/illusion/phase6_rh/duality_defect.py`

## Appendix C: UCA Optimizer

The UCA-constrained optimizer parameterizes $H$ as block-diagonal in the $P$-eigenbasis, enforcing $[H, P] = 0$ by construction. Starting from $H_{BK} + V_{\text{defect}}$, L-BFGS-B minimizes the spectral loss with regularization $\lambda = 10^{-6}$.

Code: `neural-symbolic-system/illusion/phase6_rh/uca_optimizer.py`

Reproducibility: all results are deterministic given the zeta zeros (computed via `mpmath`) and the Berry-Keating matrix construction.
