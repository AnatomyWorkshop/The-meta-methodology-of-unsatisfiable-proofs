以下是论文的 **Table of contents** 和 **Appendix I, II, III** 的完整内容。

---

## Table of contents

Introduction.

I Quantum chaos and the hypothetical Riemann flow.  
II Algebraic Geometry and global fields of non zero characteristic.  
III Spectral interpretation of critical zeros.  
IV The distribution trace formula for flows on manifolds.  
V The action \((\lambda ,x)\to \lambda x\) of \(K^{*}\) on a local field \(K\) .  
VI The global case, and the formal trace computation.  
VII Proof of the trace formula in the \(S\) - local case.  
VIII The trace formula in the global case, and elimination of \(\delta\) .  
Appendix I, Proof of theorem 1.  
Appendix II, Explicit formulas.  
Appendix III, Distribution trace formulas.

---

## Appendix I, Proof of theorem 1

In this appendix we give the proof of theorem 1. Let us first recall as a preliminary the results of Tate an Iwasawa as interpreted in [W 2] \(L\) functions and homogeneous distributions on \(A\)

In general for a non archimedean local field \(K\) we use the notations \(R\) for the maximal compact subring, \(P\) for the maximal ideal of \(R\) , \(\pi\) for a generator of the ideal \(P\) (i.e. \(P = \pi R\) ).

Let \(k\) be a global field and \(A\) the ring of Adeles of \(k\) . It is the restricted product of the local fields \(k_{v}\) indexed by the set of places \(v\) of \(k\) , with respect to the maximal compact subrings \(R_{v}\) . Similarly, the Bruhat- Schwartz space \(S(A)\) is the restricted tensor product of the local Bruhat- Schwartz spaces \(S(k_{v})\) , with respect to the vectors \(1_{R_{v}}\) .

\(L\) functions on \(k\) are associated to Grossencharakters, i.e. to characters of the Idele class group,

\[C_{k} = J_{k} / k^{*}. \quad (1)\]

Let \(\mathcal{X}\) be a character of the idele class group, we consider \(\mathcal{X}\) as a character of \(J_{k}\) which is 1 on \(k^{*}\) . As such it can be written as a product,

\[\mathcal{X}(j) = \Pi \mathcal{X}_{v}(j_{v})\qquad j = (j_{v})\in J_{k}. \quad (2)\]

\[G_{0} = \Pi R_{v}^{*}\times 1\subset J_{k},\]

it follows that for all finite \(v\) but a finite number, one has

\[\mathcal{X}_v / R_v^* = 1.\]

One says that \(\mathcal{X}\) is unramified at \(v\) when this holds.

Then \(\mathcal{X}_v(x)\) only depends upon the module \(|x|\) , since

\[k_v^* /R_v^* = \mathrm{mod}(k_v).\]

Thus \(\mathcal{X}_v\) is determined by

\[\mathcal{X}_v(\pi_v) \quad (6)\]

which does not depend upon the choice of \(\pi_v\) (mod \(R_v^*\) ).

Let \(\mathcal{X}\) be a quasi- character of \(C_k\) , it is of the form,

\[\mathcal{X}(x) = \mathcal{X}_0(x)|x|^s \quad (7)\]

where \(s \in \mathbb{C}\) and \(\mathcal{X}_0\) is a character of \(C_k\) . The real part \(\sigma\) of \(s\) is uniquely determined by

\[|\mathcal{X}(x)| = |x|^{\sigma}. \quad (8)\]

Let \(P\) be the finite set of finite places where \(\mathcal{X}_0\) is ramified. The \(L\) function \(L(\mathcal{X}_0, s)\) is defined for \(\sigma = Re(s) > 1\) as

\[L(\mathcal{X}_0,s) = \left(\prod_{\substack{v\mathrm{finite}\\v\notin P}}(1 - \mathcal{X}_{0,v}(\pi_v)q_v^{-s})^{-1}\right) = \left(\prod_{\substack{v\mathrm{finite}\\v\notin P}}(1 - \mathcal{X}_v(\pi_v))^{-1}\right) \quad (9)\]

where

\[|\pi_v| = q_v^{-1}. \quad (10)\]

Let us now recall from [W 2] how \(L(\mathcal{X}_0, s)\) appears as a normalization factor for homogeneous distributions on \(A\) .

\[\mathcal{X}(x) = \mathcal{X}_0(x)|x|^s,\quad \mathcal{X}_0:K^*\to U(1).\]

A distribution \(D\) on \(K\) is homogeneous of weight \(\mathcal{X}\) iff one has

\[\langle f^a,D\rangle = \mathcal{X}(a)^{-1}\langle f,D\rangle\]

for all test functions \(f\) and all \(a\) in \(K^{*}\) , where by definition

\[f^{a}(x) = f(ax)\]

When \(\sigma = Re(s) > 0\) , there exists up to normalization only one homogeneous distribution of weight \(\mathcal{X}\) on \(K\) , (cf [W 2]). It is given by the absolutely convergent integral,

\[\int_{K^{*}}f(x)\mathcal{X}(x)d^{*}x = \Delta_{\mathcal{X}}(f)\]

In particular, let \(K\) be non archimedean, then, for any compactly supported locally constant function \(f\) on \(K\) one has,

\[f(x) - f(\pi^{-1}x) = 0\quad \forall x,|x|\leq \delta\]

thus, for any \(s\in \mathbb{C}\) the integral

\[\int_{K^{*}}(f(x) - f(\pi^{-1}x))|x|^{s}d^{*}x = \Delta_{s}^{\prime}(f)\]

with the multiplicative Haar measure \(d^{*}x\) normalized by

\[\langle 1_{R^{*}},d^{*}x\rangle = 1.\]

defines a distribution on \(K\) with the properties,

\[\langle 1_{R},\Delta_{s}^{\prime}\rangle = 1\]

\[\langle f^{a},\Delta_{s}^{\prime}\rangle = |a|^{-s}\langle f,\Delta_{s}^{\prime}\rangle\]

and

\[\Delta_{s}^{\prime} = (1 - q^{-s})\Delta_{s},\]

\[\left|\pi \right| = q^{- 1} . \quad (20)\]

Let then \(\mathcal{X}\) be a quasi- character of \(C_{k}\) and write as above

\[\mathcal{X} = \Pi \mathcal{X}_{v},\qquad \mathcal{X}(x) = \mathcal{X}_{0}(x)\left|x\right|^{s} \quad (21)\]

where \(s\in \mathbb{C}\) and \(\mathcal{X}_0\) is a character. Let \(P\) be the finite set of finite places where it is ramified. For any finite place \(v\notin P\) , let \(\Delta_v^{\prime}(s)\) be the unique homogeneous distribution of weight \(\mathcal{X}_v\) normalized by

\[\langle \Delta_v^{\prime}(s),1_{R_v}\rangle = 1. \quad (22)\]

For any \(v\in P\) or any infinite place, let, for \(\sigma = Re(s) > 0\) \(\Delta_v^{\prime}\) be given by (14) which is homogeneous of weight \(\mathcal{X}_v\) but unnormalized. Then the infinite tensor product,

\[\Delta_s^{\prime} = \Pi \Delta_v^{\prime}(s) \quad (23)\]

makes sense as a continuous linear form on \(S(A)\) and is homogeneous of weight \(\mathcal{X}\) .

This solution is not equal to 0 since \(\Delta_v^{\prime}\neq 0\) for any \(v\in P\) and any infinite place also. It is finite by construction of the space \(S(A)\) of test functions as an infinite tensor product

\[\mathcal{S}(A) = \otimes (\mathcal{S}(k_v),1_{R_v}). \quad (24)\]

Lemma 1. (cf [W 2]) For \(\sigma = Re(s) > 1\) , the following integral converges absolutely

\[\int f(x)\mathcal{X}_0(x)\left|x\right|^s d^* x = \Delta_s(f)\qquad \forall f\in \mathcal{S}(A)\]

and \(\Delta_s(f) = L(\mathcal{X}_0,s)\Delta_s'(f)\)

Proof. To get the absolute convergence one can assume that \(f = 1_{R}\) and \(\mathcal{X}_0 = 1\) . Then one has to control an infinite product of local terms, given locally for the Haar measure \(d^{*}x\) on \(k_{v}^{*}\) such that \(\int_{R_{v}^{*}}d^{*}x = 1\) , by

\[\int_{R\cap k_{v}^{*}}\left|x\right|^{s}d^{*}x\qquad (s\mathrm{real}) \quad (25)\]

which is \(1 + q_v^{- s} + q_v^{- 2s} + \ldots = (1 - q_v^{- s})^{- 1}\) . Thus the convergence for \(\sigma > 1\) is the same as for the zeta function.

To prove the second equality one only needs to consider the infinite tensor product for finite places \(v \notin P\) . Then by (20) one has \(\Delta_v' = (1 - q_v^{-\alpha_v}) \Delta_v\) where

\[q_v^{-\alpha_v} = \mathcal{X}_v(\pi) = \mathcal{X}_{0,v}(\pi)q_v^{-s} \quad (26)\]

with \(|\pi | = q_v^{- 1}\) .

\[\mathrm{Thus~one~gets~}\Delta_{s} = \left(\prod_{\substack{v\mathrm{~finite~}}}\\ \mathrm{~with~}\pi \mathrm{~finite~}}\left(1 - \mathcal{X}_{0,v}(\pi)q_{v}^{-s}\right)^{-1}\right)\Delta_{s}^{\prime} = L(\mathcal{X}_{0},s)\Delta_{s}^{\prime}.\right.\]

By construction \(\Delta_{s}^{\prime}\) makes sense whenever \(\sigma > 0\) and is a holomorphic function of \(s\) (for fixed \(f\) ). Let us review briefly (cf [W2]) how to extend the definition of \(\Delta_{s}\) .

We let as above \(k\) be a global field, we fix a non trivial additive character \(\alpha\) of \(A\) , trivial on \(k\) ,

\[\alpha (x + y) = \alpha (x)\alpha (y)\in U(1), \alpha (q) = 1 \quad \forall q\in k. \quad (27)\]

We then identify the dual of the locally compact additive group \(A\) with \(A\) itself by the pairing,

\[\langle x,y\rangle = \alpha (xy). \quad (28)\]

One shows (cf.[W 1]) that the lattice \(k\subset A\) , i.e. the discrete and cocompact additive subgroup \(k\) , is its own dual,

\[\langle x,q\rangle = 1\qquad \forall q\in k\qquad \Leftrightarrow \qquad x\in k. \quad (29)\]

Since \(A\) is the restricted product of the local fields \(k_{v}\) one can write \(\alpha\) as an infinite product,

\[\alpha = \Pi \alpha_{v} \quad (30)\]

where for almost all \(v\) one has \(\alpha_{v} = 1\) on \(R_{v}\) . Let us recall the definition of the space \(\mathcal{S}(A)_{0}\) ,

\[\mathcal{S}(A)_0 = \{f\in \mathcal{S}(A);f(0) = 0,\int f dx = 0\} \quad (31)\]

Lemma 2. Let \(f \in \mathcal{S}(A)_0\) , then the series

\[E(f)(g) = |g|^{1 / 2}\sum_{q\in k^{*}}f(qg)\qquad \forall g\in C_{k}\]

converges absolutely and one has

\[\forall n,\exists c,\qquad |E(f)(g)|\leq c e^{-n|\log |g||}\qquad \forall g\in C_{k}\]

and \(E(\widehat{f})(g) = E(f)(g^{- 1})\)

Proof. Let us first recall the formal definition ([Br]) of the Bruhat- Schwartz space \(\mathcal{S}(G)\) for an arbitrary locally compact abelian group \(G\) . One considers all pairs of subgroups \(G_{1},G_{2}\) of \(G\) such that \(G_{1}\) is generated by a compact neighborhood of 0 in \(G\) , while \(G_{2}\) is a compact subgroup of \(G_{1}\) such that the quotient group is elementary, i.e. is of the form \(\mathbb{R}^{a}\mathbb{T}^{b}\mathbb{Z}^{c}F\) for \(F\) a finite group. By definition the Bruhat- Schwartz space \(\mathcal{S}(G)\) is the inductive limit of the Schwartz spaces \(\mathcal{S}(G_{1} / G_{2})\) where the latter have the usual definition in terms of rapid decay of all derivatives. Since \(G_{1}\) is open in \(G\) , any element of \(\mathcal{S}(G_{1} / G_{2})\) extended by 0 outside \(G_{1}\) defines a continuous function on \(G\) . By construction \(\mathcal{S}(G)\) is the union of the subspaces \(\mathcal{S}(G_{1} / G_{2})\) and it is endowed with the inductive limit topology.

Let \(\hat{G}\) be the Pontrjagin dual of \(G\) , then the Fourier transform, which depends upon the normalization of the Haar measure on \(G\) , gives an isomorphism of \(\mathcal{S}(G)\) with \(\mathcal{S}(\hat{G})\) .

Let \(\Gamma\) be a lattice in the locally compact abelian group \(G\) . Then any function \(f \in \mathcal{S}(G)\) is admissible for the pair \(G, \Gamma\) in the sense of [W 1], and the Poisson summation formula (cf [W 1]) is the equality,

\[\mathrm{Covol}(\Gamma)\sum_{\gamma \in \Gamma}f(\gamma) = \sum_{\beta \in \Gamma^{\perp}}\widehat{f} (\beta) \quad (32)\]

where \(\Gamma^{\perp}\) is the dual of the lattice \(\Gamma\) , and

\[\widehat{f} (\beta) = \int f(a)\beta (a)da. \quad (33)\]

Both sides of (32) depend upon the normalization of the Haar measure on \(G\) .

In our case we let \(A\) be as above the additive group of Adeles on \(k\) . We normalize the additive Haar measure \(dx\) on \(A\) by

\[\mathrm{Covol}(k) = 1. \quad (34)\]

We then take \(\Gamma = xk\) , for some \(x \in A^{- 1}\) . One has

\[\mathrm{Covol}(xk) = |x|\]

The dual \(\Gamma^{\perp}\) of the lattice \(xk\) , for \(x\) invertible in \(A\) , is the lattice \(\Gamma^{\perp} = x^{- 1}k\) . Thus the Poisson formula (32) reads, for any \(f \in \mathcal{S}(A)\) ,

\[\left|x\right|\sum_{q\in k}f(xq) = \sum_{q\in k}\widehat{f} (x^{-1}q). \quad (36)\]

Which we can rewrite as,

\[\left|x\right|\sum_{k^{*}}f(xq) = \sum_{k^{*}}\widehat{f} (x^{-1}q) + \delta \quad (37)\]

\[\delta = -|x|f(0) + \int f(y)dy.\]

We can then rewrite (37) as the equality, valid for all \(f \in \mathcal{S}(A)_0\)

\[E(f)(x) = E(\widehat{f})\left(\frac{1}{x}\right)\qquad f\in \mathcal{S}(A)_0. \quad (38)\]

It remains to control the growth of \(E(f)(x)\) on \(C_k\) , but by (38), it is enough to understand what happens for \(|x|\) large.

We only treat the case of number fields, the general case is similar. Let \(A = A_{f} \times A_{\infty}\) be the decomposition of the ring of Adeles corresponding to finite and infinite places, thus \(A_{\infty} = \prod_{S_{\infty}}k_{v}\) where \(S_{\infty}\) is the set of infinite places.

Any element of \(\mathcal{S}(A)\) is a finite linear combination of test functions of the form,

\[f = f_{0}\otimes f_{1} \quad (39)\]

where \(f_{0} \in \mathcal{S}(A_{f})\) , \(f_{1} \in \mathcal{S}(A_{\infty})\) (cf [W 5] 39), thus it is enough to control the growth of \(E(f)(x)\) for such \(f\) and \(|x|\) large.

Let \(J_{k,1} = \{x \in J_k; |x| = 1\}\) be the group of Ideles of module one, since \(J_{k,1} / k^{*}\) is compact (cf [W 1]), we shall fix a compact subset \(K_1\) of \(J_{k,1}\) whose image in \(J_{k,1} / k^{*}\) is this compact group.

Let \(\mu\) be the diagonal embedding:

\[\lambda \in \mathbb{R}_{+}^{*}\xrightarrow{\mu}(\lambda ,\ldots,\lambda)\in\prod_{S_{\infty}}k_{v}^{*} \quad (40)\]

which yields an isomorphism

\[J_{k} = J_{k,1}\times \operatorname {Im}\mu .\]

One has \(f_{0}\in \mathcal{S}(A_{f})\) , hence (cf [W 5]), \(f_{0}\in C_{c}(A_{f})\) and we let \(K_{0} =\) Support \(f_{0}\) . Since \(K_{0}\) is compact, one can find a finite subset \(P\) of the set of finite places and \(C< \infty\) such that:

\[y\in K = (K_{f})^{-1}K_{0}\Rightarrow |y_{v}|\leq 1\quad \forall v\notin P\qquad ,\qquad |y_{v}|\leq C\quad \forall v.\]

where \(K_{f}\) is the projection of \(K_{1}\) on \(A_{f}\) .

We let \(\Omega\) be the compact open subgroup of \(A_{f}\) determined by

\[|a_{v}|\leq 1\quad \forall v\notin P\qquad ,\qquad |a_{v}|\leq C\quad \forall v.\]

By construction \(E(f)(x)\) only depends upon the class of \(x\) in \(J_{k} / k^{*}\) . Thus, to control the behaviour of \(E(f)(x)\) for \(|x|\to \infty\) , we can take \(x = (x_{f},x_{\infty})\in\) \(K_{1}\) and consider \(E(f)(\lambda x)\) for \(\lambda \in \mathbb{R}_{+}^{*}\) \(\lambda \to \infty\) . Now let \(q = (q_{f},q_{\infty})\in k\) then,

\[f(q\lambda x) = f_{0}(q_{f}x_{f})f_{1}(q_{\infty}\lambda x_{\infty}) \quad (44)\]

and this vanishes unless \(q_{f}x_{f}\in K_{0}\) , i.e. unless \(q_{f}\in K\) . But then by (42) one has \(q_{f}\in \Omega\) . Let \(\Gamma\) be the lattice in \(\prod_{S_{\infty}}k_{v}\) determined by

\[\Gamma = \{q_{\infty};q\in k,q_{f}\in \Omega ,\} \quad (45)\]

The size of \(E(f)(\lambda x)\) is thus controlled ( up to the square root of \(|\lambda x|\) ) by

\[C\sum_{n\in \Gamma^{*}}|f_{1}(\lambda x_{\infty}n)| \quad (46)\]

where \(x_{\infty}\) varies in the projection \(K_{\infty}\) of \(K_{1}\) on \(\prod_{S_{\infty}}k_{v}^{*}\) .

Since \(f_{1}\in \mathcal{S}(A_{\infty})\) , this shows that \(E(f)(x)\) decays faster than any power of \(|x|\) for \(|x|\to \infty\) .

We have shown that \(E(f)\) has rapid decay in terms of \(|x|\) , for \(|x|\to \infty\) . Using (38) and the stability of \(\mathcal{S}(A)_{0}\) under Fourier, we see that it also has exponential decay in terms of \(|\log |x||\) when \(|\log |x||\to \infty\) .

We then get,

Lemma 3. (cf [W 2]) For \(\sigma = Re(s) > 0\) , and any character \(\mathcal{X}_0\) of \(C_k\) , one has

\[\int E(f)(x)\mathcal{X}_0(x)|x|^{s - 1 / 2}d^* x = cL(\mathcal{X}_0,s)\Delta_s'(f)\qquad \forall f\in \mathcal{S}(A)_0\]

where the non zero constant \(c\) depends upon the normalization of the Haar measure \(d^* x\) on \(C_k\) .

Proof. For \(\sigma = Re(s) > 1\) , the equality follows from lemma 1, but since both sides are analytic in \(s\) it holds in general.

As in lemma 1, we shall continue to use the notation \(\Delta_s(f)\) for \(\sigma = Re(s) > 0\) .

Approximate units in the Sobolev spaces \(L_{\delta}^{2}(C_{k})\)

We first consider, for \(\delta > 1\) , the Hilbert space \(L_{\delta}^{2}(\mathbb{R})\) of functions \(\xi (u)\) , \(u \in \mathbb{R}\) with square norm given by

\[\int_{\mathbb{R}}|\xi (u)|^{2}(1 + u^{2})^{\delta /2}du. \quad (1)\]

We let \(\rho (u) = (1 + u^{2})^{\delta /2}\) . It is comparable to \((1 + |u|)^{\delta}\) and in particular,

\[\frac{\rho(u + a)}{\rho(u)}\leq c\rho (a)\qquad \forall u\in \mathbb{R},a\in \mathbb{R} \quad (2)\]

with \(c = 2^{\delta /2}\) .

We then let \(V(v)\) be the translation operator,

\[(V(v)\xi)(u) = \xi (u - v)\qquad \forall u,v\in \mathbb{R}. \quad (3)\]

One has \(\int_{\mathbb{R}}|\xi (u - v)|^{2}\rho (u)du = \int_{\mathbb{R}}|\xi (u)|^{2}\rho (u + v)du\) so that by (2) it is less than \(c\int_{\mathbb{R}}|\xi (u)|^{2}\rho (u)\rho (v)du = c\rho (v)\| \xi \|^{2}\)

\[\| V(v)\| \leq (c\rho (v))^{1 / 2}. \quad (4)\]

This shows that \(V(f) = \int f(v)V(v)dv\) makes sense as soon as

\[\int |f(v)|\rho (v)^{1 / 2}dv< \infty . \quad (5)\]

4. There exists an approximate unit \(f_{n} \in \mathcal{S}(\mathbb{R})\) , such that \(\widehat{f}_{n}\) has compact support, \(\| V(f_{n})\| \leq C \quad \forall n\) , and

\[V(f_{n})\to 1 \text{strongly in} L_{\delta}^{2}(\mathbb{R}).\]

Proof. Let \(f\) be a function, \(f \in \mathcal{S}(\mathbb{R})\) , whose Fourier transform \(\hat{f}\) has compact support, and such that \(\int f dx = 1\) (i.e. \(\hat{f}(0) = 1\) ). Let then

\[f_{n}(v) = n f(n v)\qquad n = 1,2,\ldots \quad (6)\]

One has \(\begin{array}{r}{\int |f_{n}(v)|\rho (v)^{1 / 2}d v = \int |f(u)|\rho \left(\frac{u}{n}\right)^{1 / 2}d u\leq \int |f(u)|\rho (u)^{1 / 2}d u} \end{array}\) Thus \(\| V(f_{n})\|\) is uniformly bounded.

We can assume that \(\hat{f}\) is equal to 1 on \([- 1,1]\) , then \(\hat{f}_{n}\) is equal to 1 on \([- n,n]\) and \(V(f_{n})\xi = \xi\) for any \(\xi\) with \(\operatorname {Supp}\hat{\xi}\subset [- n,n]\) . By uniformity one gets that \(V(f_{n})\to 1\) strongly.

Let us now identify the dual \((L_{\delta}^{2})^{*}\) of the Hilbert space \(L_{\delta}^{2}\) with \(L_{-\delta}^{2}\) by means of the pairing,

\[\langle \xi ,\eta \rangle_{0} = \int_{\mathbb{R}}\xi (u)\eta (u)d u. \quad (7)\]

Since \(L_{\delta}^{2}\) is a Hilbert space, it is its own dual using the pairing,

\[\langle \xi ,\eta_{1}\rangle = \int_{\mathbb{R}}\xi (u)\eta_{1}(u)(1 + u^{2})^{\delta /2}d u. \quad (8)\]

If we let \(\eta (u) = \eta_{1}(u)(1 + u^{2})^{\delta /2}\) , then

\[\int |\eta_{1}(u)|^{2}(1 + u^{2})^{\delta /2}d u = \int |\eta (u)|^{2}(1 + u^{2})^{-\delta /2}d u\]

which is the natural norm square for \(L_{-\delta}^{2}\) .

Given a quasicompact group such as \(C_{k}\) with module,

\[\mid \mid :C_{k}\to \mathbb{R}_{+}^{*} \quad (9)\]

we let \(d^{*}g\) be the Haar measure on \(C_{k}\) normalized by

\[\int_{|g|\in [1,\Lambda]}d^{*}g\sim \log \Lambda \qquad \Lambda \to \infty \quad (10)\]

\[\int_{C_k}|\xi (g)|^2 (1 + \log |g|^2)^{\delta /2}d^* g.\]

It is, when the module of \(k\) is \(\mathbb{R}_{+}^{*}\) , a direct sum of spaces (1), labelled by the characters \(\mathcal{X}_0\) of the compact group

\[C_{k,1} = \mathrm{Ker~mod}.\]

The pairing between \(L_{\delta}^{2}(C_{k})\) and \(L_{- \delta}^{2}(C_{k})\) is given by

\[\langle \xi ,\eta \rangle = \int \xi (g)\eta (g)d^{*}g. \quad (13)\]

The natural representation \(V\) of \(C_{k}\) by translations is given by

\[(V(a)\xi)(g) = \xi (a^{-1}g)\qquad \forall g,a\in C_{k}. \quad (14)\]

It is not unitary but by (4) one has,

\[\| V(g)\| = 0|\log |g||^{\delta /2},|\log |g||\to \infty . \quad (15)\]

Finally, one has, using lemma 4 and the decomposition \(C_{k} = C_{k,1} \times N\) ,

Lemma 5. There exists an approximate unit \(f_{n} \in \mathcal{S}(C_{k})\) , such that \(\hat{f}_{n}\) has compact support, \(\| V(f_{n})\| \leq C \quad \forall n\) , and

\[V(f_{n})\to 1 \text{strongly in} L_{\delta}^{2}(C_{k}).\]

## Proof of theorem III 1

We first consider the subspace of codimension 2 of \(\mathcal{S}(A)\) given by

\[f(0) = 0, \int f dx = 0. \quad (1)\]

On this subspace \(\mathcal{S}(A)_{0}\) we put the inner product,

\[\int_{C_k}|E(f)(x)|^2 (1 + \log |x|^2)^{\delta /2}d^* x. \quad (2)\]

\[(U(a)\xi)(x) = \xi (a^{-1}x)\qquad \forall a\in C_k,x\in A.\]

We let \(L_{\delta}^{2}(X)_{0}\) be the separated completion of \(\mathcal{S}(A)_{0}\) for the inner product given by (2). The linear map \(E:\mathcal{S}(A)_{0}\to L_{\delta}^{2}(C_{k})\) satisfies

\[\| E(f)\|_{\delta}^{2} = \| f\|_{\delta}^{2} \quad (4)\]

by construction. Thus it extends to an isometry, still noted \(E\)

\[E:L_{\delta}^{2}(X)_{0}\hookrightarrow L_{\delta}^{2}(C_{k}). \quad (5)\]

One has

\[\begin{array}{l}{E(U(a)f)(g) = |g|^{1 / 2}\sum_{k^{*}}(U(a)f)(q g) = |g|^{1 / 2}\sum_{k^{*}}f(a^{-1}q g)}\\ {= |g|^{1 / 2}\sum_{k^{*}}f(q a^{-1}g) = |a|^{1 / 2}|a^{-1}g|^{1 / 2}\sum_{k^{*}}f(q a^{-1}g) = \vert a\vert^{1 / 2}(V(a)E(f))(g)} \end{array} \quad (6)\]

\[E U(a) = |a|^{1 / 2}V(a)E. \quad (6)\]

The equality (6) shows that the natural representation \(U\) of \(C_{k}\) on \(L_{\delta}^{2}(X)_{0}\) corresponds by the isometry \(E\) to the restriction of \(|a|^{1 / 2}V(a)\) to the invariant subspace given by the range of \(E\) .

In order to understand \(\operatorname{Im}E\) we consider its orthogonal in the dual space \(L_{-\delta}^{2}(C_{k})\) .

The compact subgroup

\[C_{k,1} = \{g\in C_k;|g| = 1\} \quad (7)\]

acts by the representation \(V\) which is unitary when restricted to \(C_{k,1}\) . Thus one can decompose \(L_{\delta}^{2}(C_{k})\) and its dual \(L_{-\delta}^{2}(C_{k})\) , in the direct sum of the subspaces,

\[L_{\delta ,\chi_0}^2 = \{\xi \in L_\delta^2 (C_k);\xi (a^{-1}g) = \chi_0(a)\xi (g)\qquad \forall g\in C_k,a\in C_{k,1}\} \quad (8)\]

and,

\[L_{-\delta ,\chi_0}^2 = \{\xi \in L_{-\delta}^2 (C_k);\xi (a g) = \chi_0(a)\xi (g)\qquad \forall g\in C_k,a\in C_{k,1}\} \quad (9)\]

which corresponds to the projections \(P_{\mathcal{X}_0} = \int \overline{\mathcal{X}_0} (a)V(a)d_1a\) for \(L_{\delta}^2\) and \(P_{\mathcal{X}_0}^t = \int \overline{\mathcal{X}_0} (a)V(a)^t d_1a\) for the dual space \(L_{-\delta}^2\) .

In (9) we used the formula

\[(V(g)^t\eta)(x) = \eta (gx)\]

which follows from the definition of the transpose, \(\langle V(g)\xi ,\eta \rangle = \langle \xi ,V(g)^t\eta \rangle\) using

\[\int \xi (g^{-1}x)\eta (x)d^{*}x = \int \xi (y)\eta (gy)d^{*}y\]

In these formulas one only uses the character \(\mathcal{X}_0\) as a character of the compact subgroup \(C_{k,1}\) of \(C_k\) . One now chooses, non canonically, an extension \(\tilde{\mathcal{X}}_0\) of \(\mathcal{X}_0\) as a character of \(C_k\)

\[\tilde{\mathcal{X}}_0(g) = \mathcal{X}_0(g)\qquad \forall g\in C_{k,1}. \quad (11)\]

This choice is not unique but any two such extensions differ by a character which is principal, i.e. of the form: \(g \to |g|^{is_0}\) , \(s_0 \in \mathbb{R}\) .

Let us fix a factorization \(C_k = C_{k,1} \times \mathbb{R}_+^*\) , and fix \(\tilde{\mathcal{X}}_0\) as being equal to 1 on \(\mathbb{R}_+^*\) .

We then write any element of \(L_{-\delta ,\mathcal{X}_0}^2 (C_k)\) in the form

\[g\in C_k\to \eta (g) = \tilde{\mathcal{X}}_0(g)\psi (|g|) \quad (12)\]

where

\[\int |\psi (|g|)^2 (1 + (\log |g|)^2)^{-\delta /2}d^* g< \infty \quad (13)\]

This vector is in the orthogonal of \(\operatorname {Im}E\) iff

\[\int E(f)(x)\tilde{\mathcal{X}}_0(x)\psi (|x|)d^* x = 0\qquad \forall f\in \mathcal{S}(A)_0. \quad (14)\]

We first proceed formally and write \(\psi (|x|) = \int \tilde{\psi} (t)|x|^{it}dt\) so that the left hand side of (14) becomes,

\[\int \int E(f)(x)\tilde{\mathcal{X}}_0(x)|x|^{it}\tilde{\psi} (t)d^* xdt = \int \Delta_{1 / 2 + it}(f)\tilde{\psi} (t)dt \quad (15)\]

(using the notations of lemmas 1 and 3).

Let us justify this formal manipulation; since we deal with the orthogonal of an invariant subspace, we can assume that

\[V^{t}(h)\eta = \eta ,\]

for some \(h\) such that \(\hat{h}\) has compact support. Indeed we can use lemma 5 to only consider vectors which belong to the range of

\[V^{t}(h) = \int h(g)V(g)^{t}d^{*}g,\hat{h}\mathrm{~with~compact~support}.\]

Then, using (16), the Fourier transform of the tempered distribution \(\psi\) on \(\mathbb{R}_{+}^{*}\) has compact support in \(\mathbb{R}\) . Thus, since \(E(f)(x)\) has rapid decay, the equality between (14) and (15) follows from the definition of the Fourier transform of the tempered distribution \(\psi\) on \(\mathbb{R}_{+}^{*}\) .

Let us now describe suitable test functions \(f\in \mathcal{S}(A)_0\) in order to test the distribution,

\[\int \Delta_{\frac{1}{2} +it}\widehat{\psi} (t)dt \quad (17)\]

We treat the case of characteristic zero, the general case is similar. For the finite places we take,

\[f_{0} = \otimes_{v\notin P}1_{R_{v}}\otimes f_{\chi_{0}} \quad (18)\]

where \(f_{\chi_0}\) is the tensor product over ramified places of the functions equal to 0 outside \(R_{v}^{*}\) and to \(\overline{\mathcal{X}}_{0,v}\) on \(R_{v}^{*}\) . It follows then by the definition of \(\Delta_{s}^{\prime}\) that,

\[\langle \Delta_{s}^{\prime},f_{0}\otimes f\rangle = \int f(x)\mathcal{X}_{0,\infty}(x)|x|^{s}d^{*}x \quad (19)\]

for any \(f\in \mathcal{S}(A_{\infty})\)

Moreover if the set \(P\) of finite ramified places is not empty one has,

\[f_{0}(0) = 0,\int_{A_{f}}f_{0}(x)dx = 0 \quad (20)\]

so that \(f_{0}\otimes f\in \mathcal{S}(A)_{0}\qquad \forall f\in \mathcal{S}(A_{\infty})\)

Now let \(\ell\) be the number of infinite places of \(k\) and consider the map \(\rho :(\mathbb{R}_{+}^{*})^{\ell}\to \mathbb{R}_{+}^{*}\) given by

\[\rho (\lambda_{1},\ldots ,\lambda_{\ell}) = \lambda_{1}\ldots \lambda_{\ell}.\]

As soon as \(\ell >1\) this map is not proper. Given a smooth function with compact support, \(b\in C_{c}^{\infty}(\mathbb{R}_{+}^{*})\) we need to find \(a\in C_{c}^{\infty}((\mathbb{R}_{+}^{*})^{\ell})\) such that the direct image of the measure \(a(x)d^{*}x\) is \(b(y)d^{*}y\) where \(d^{*}x = \Pi d^{*}x_{i}\) is the product of the multiplicative Haar measures.

Equivalently one is dealing with a finite dimensional vector space \(E\) and a linear form \(L:E\to \mathbb{R}\) . One is given \(b\in C_{c}^{\infty}(\mathbb{R})\) and asked to lift it. One can write \(E = \mathbb{R}\times E_{1}\) and the lift can be taken as \(a = b\otimes b_{1}\) where \(b_{1}\in C_{c}^{\infty}(E_{1})\) \(\int b_{1}dx = 1\) .

Thus we can in (19) take a function \(f\) of the form,

\[f(x) = g(x)\overline{{X}}_{0,\infty}(x)\]

where the function \(g\in C_{c}^{\infty}(A_{\infty})\) only depends upon \((|x|_{v})\) \(v\in S_{\infty}\) and is smooth with compact support, disjoint from the closed set

Thus, to any function \(b\in C_{c}^{\infty}(\mathbb{R}_{+}^{*})\) we can assign a test function \(f = f_{b}\) such that for any \(s\) (Re \(s > 0\) )

\[\langle \Delta_{s}^{\prime},f_{0}\otimes f_{b}\rangle = \int_{\mathbb{R}_{+}^{*}}b(x)|x|^{s}d^{*}x.\]

By lemma 3, we get,

\[\left\langle \int \Delta_{\frac{1}{2} +it}\widehat{\psi} (t)d t,f_{0}\otimes f_{b}\right\rangle = \left\langle \int L(\mathcal{X}_{0},\frac{1}{2} +it)\Delta_{\frac{1}{2} +it}^{\prime}\widehat{\psi} (t)d t,f_{0}\otimes f_{b}\right\rangle\] \[\qquad = \int \int L(\mathcal{X}_{0},\frac{1}{2} +it)\widehat{\psi} (t)b(x)|x|^{\frac{1}{2} +it}d^{*}x d t.\]

Thus, from (14) and (15) we conclude, using arbitrary test functions \(b\) that the Fourier transform of the distribution \(L(\mathcal{X}_{0},1 / 2 + it)\widehat{\psi} (t)\) actually vanishes,

\[L(\mathcal{X}_{0},\frac{1}{2} +it)\widehat{\psi} (t) = 0 \quad (24)\]

To justify the above equality, we need to control the growth of the \(L\) function in the variable \(t\) . One has,

\[|L(\frac{1}{2} +it)| = 0(|t|^{N}) \quad (25)\]

In particular, since \(L\left(\frac{1}{2} + it\right)\) is an analytic function of \(t\) we see that it is a multiplier of the algebra \(\mathcal{S}(\mathbb{R})\) of Schwartz functions in the variable \(t\) . Thus the product \(L\left(\frac{1}{2} + it\right)\hat{\psi} (t)\) is still a tempered distribution, and so is its Fourier transform. To say that the latter vanishes when tested on arbitrary functions which are smooth with compact support implies that it vanishes.

The above argument uses the hypothesis \(\mathcal{X}_0 / C_{k,1} \neq 1\) .

In the case \(\mathcal{X}_0 / C_{k,1} = 1\) we need to impose to the test function \(f\) used in (22) the condition \(\int f dx = 0\) which means

\[\int b(x)|x|d^{*}x = 0. \quad (26)\]

But the space of functions \(b(x)|x|^{1 / 2}\in C_{c}^{\infty}(\mathbb{R}_{+}^{*})\) such that (26) holds is still dense in the Schwartz space \(\mathcal{S}(\mathbb{R}_{+}^{*})\) .

To understand the equation (24), let us consider an equation for distributions \(\alpha (t)\) of the form

\[\phi (t)\alpha (t) = 0 \quad (27)\]

where we first work with distributions \(\alpha\) on \(S^{1}\) and we assume that \(\phi \in C^{\infty}(S^{1})\) has finitely many zeros \(x_{i}\in Z(\phi)\) , of finite order \(n_{i}\) . Let \(J\) be the ideal of \(C^{\infty}(S^{1})\) generated by \(\phi\) . One has \(\psi \in J\Leftrightarrow\) order of \(\psi\) at \(x_{i}\) is \(\geq n_{i}\) .

Thus the distributions \(\delta_{x_{i}}\) \(\delta_{x_{i}}^{\prime},\ldots ,\delta_{x_{i}}^{(n_{i} - 1)}\) form a basis of the space of solutions of (27).

Now \(\hat{\psi} (t)\) is, for \(\eta\) orthogonal to \(\operatorname {Im}(E)\) and satisfying (16), a distribution with compact support, and \(L\left(\mathcal{X}_0,\frac{1}{2} +it\right)\hat{\psi} (t) = 0\) . Thus by the above argument we get that \(\hat{\psi}\) is a finite linear combination of the distributions,

\[\delta_{t}^{(k)},L\left(\mathcal{X}_{0},\frac{1}{2} +it\right) = 0,k< \mathrm{order~of~the~zero},k< \frac{\delta - 1}{2}. \quad (28)\]

The condition \(k< \mathrm{order}\) of the zero is necessary and sufficient to get the vanishing on the range of \(E\) . The condition \(k< \frac{\delta - 1}{2}\) is necessary and sufficient to ensure that \(\psi\) belongs to \(L_{- \delta}^{2}\) , i.e. that

\[\int (\log |x|)^{2k}(1 + |\log |x||^{2})^{-\delta /2}d^{*}x< \infty \quad (29)\]

which is \(2k + \delta < - 1\) , i.e. \(k< \frac{\delta - 1}{2}\) .

Conversely, let \(s\) be a zero of \(L(\mathcal{X}_0,s)\) and \(k > 0\) its order. By lemma 3 and the finiteness and analyticity of \(\Delta_{s}^{\prime}\) (for \(\mathrm{Re}s > 0\) ) we get

\[\left(\frac{\partial}{\partial s}\right)^{a}\Delta_{s}(f) = 0\qquad \forall f\in \mathcal{S}(A)_{0},a = 0,1,\ldots ,k - 1. \quad (30)\]

We can differentiate the equality of lemma 3 and get,

\[\left(\frac{\partial}{\partial s}\right)^{a}\Delta_{s}(f) = \int_{C_{k}}E(f)(x)\mathcal{X}_{0}(x)|x|^{s - 1 / 2}(\log |x|)^{a}d^{*}x. \quad (31)\]

Thus \(\eta\) belongs to the orthogonal of \(\operatorname {Im}(E)\) and satisfies (16) iff it is a finite linear combination of functions of the form,

\[\eta_{t,a}(x) = \mathcal{X}_0(x)|x|^{it}(\log |x|)^a, \quad (32)\]

where,

\[L\left(\mathcal{X}_0,\frac{1}{2} +it\right) = 0,\quad a< \mathrm{order~of~the~zero},a< \frac{\delta - 1}{2}.\]

The restriction to the subgroup \(\mathbb{R}_{+}^{*}\) of \(C_{k}\) of the transposed of \(W\) is thus given in the above basis by:

\[W(\lambda)^{t}\eta_{t,a} = \sum_{b = 0}^{a}C_{a}^{b}\lambda^{it}(Log(\lambda))^{b}\eta_{t,a - b}.\]

The multiplication operator by a function with bounded derivatives is a bounded operator in any Sobolev space thus one checks directly, using the density in the orthogonal of \(\operatorname {Im}(E)\) of vectors satisfying (16), that if \(L\left(\mathcal{X}_0,\frac{1}{2} +is\right)\neq 0\) then \(is\) does not belong to the spectrum of \(D_{\mathcal{X}_0}^{t}\)

This determines the spectrum of the operator \(D_{\mathcal{X}_0}^{t}\) and hence of its transpose \(D_{\mathcal{X}_0}\) as indicated in Theorem 1 and ends the proof of theorem 1.

Let us now prove the corollary. Let us fix \(h_0\in \mathcal{S}(C_k)\) such that \(\hat{h}_0\) has compact support contained in \(\{\mathcal{X}_0\} \times \mathbb{R}\) and \(\hat{h}_0(\mathcal{X}_0,s) = 1\) for \(s\) small.

Let then \(h_s\) be given by \(h_s(g) = h_0(g)|g|^{is}\) . The Fourier transform \(\hat{h}_s\) is then the translate of \(\hat{h}_0\) , and one can choose \(h_0\) such that,

\[\sum_{n\in \mathbb{Z}}\hat{h}_n(\mathcal{X}_0,u) = 1\qquad u\in \mathbb{R} \quad (35)\]

When |s| →∞, the dimension of the range of W t(hs) is of the order of Log|s| as is the number of zeros of the L function in the translates of a fixed interval (cf [W 3]).
Let h ∈S(Ck). One has W t(h) = ∑_{n∈Z} W t(h ∗hn).
It follows then from the polynomial growth of the norm of W t(g) that the operator
∫ h(g) W(g)^t d∗g
is of trace class for any h ∈S(Ck).
Moreover using the triangular form given by (34) we get its trace, and hence the trace of its transpose W(h) as,
Trace W(h) = ∑_{L(X, 1/2 +ρ)=0, ρ∈iR} ĥ(X , ρ)
where the multiplicity is counted as in Theorem 1 and where the Fourier transform ĥ of h is defined by,
ĥ(X , ρ) = ∫_{Ck} h(u) X(u) |u|^ρ d∗u .

---

## Appendix II. Explicit formulas

Let us first recall the Weil explicit formulas ([W3]). One lets k be a global field. One identifies the quotient Ck/Ck,1 with the range of the module,
N = { |g| ; g ∈ Ck } ⊂ R∗_+ .
One endows N with its normalized Haar measure d∗x. Given a function F on N such that, for some b > 1/2,
|F(ν)| = 0(ν^b) (ν→0), |F(ν)| = 0(ν^{−b}) (ν→∞),
one lets,
Φ(s) = ∫_N F(ν) ν^{1/2−s} d∗ν .

Given a Grossencharakter X , i.e. a character of Ck and any ρ in the strip 0 < Re(ρ) < 1 , one lets N(X, ρ) be the order of L(X, s) at s = ρ . One lets,
S(X, F) = ∑_ρ N(X, ρ) Φ(ρ)
where the sum takes place over ρ's in the above open strip. One then defines a distribution Δ on Ck by,
Δ = log |d^{−1}| δ_1 + D − ∑_v D_v,
where δ_1 is the Dirac mass at 1 ∈ Ck , where d is a differential idele of k so that |d|^{−1} is up to sign the discriminant of k when char(k)=0 and is q^{2g−2} when k is a function field over a curve of genus g with coefficients in the finite field F_q.

The distribution D is given by,
D(f) = ∫_{Ck} f(w) (|w|^{1/2} + |w|^{−1/2}) d∗w
where the Haar measure d∗w is normalized (cf. IIb). The distributions D_v are parametrized by the places v of k and are obtained as follows. For each v one considers the natural proper homomorphism,
k_v^* → C_k, x → class of (1,…, x, 1…)
of the multiplicative group of the local field k_v in the idele class group C_k.

One then has,
D_v(f) = Pfw ∫_{k_v^*} \frac{f(u)}{|1-u|} |u|^{1/2} d∗u
where the Haar measure d∗u is normalized (cf. IIb), and where the Weil Principal value Pfw of the integral is obtained as follows, for a local field K = k_v,
Pfw ∫_{k_v^*} 1_{R_v^*} \frac{1}{|1-u|} d∗u = 0,
if the local field k_v is non Archimedean, and otherwise:
Pfw ∫_{k_v^*} φ(u) d∗u = Pf_0 ∫_{R_+^*} ψ(ν) d∗ν ,
where Pf_0 is defined by,
PF_0∫ ψ(ν)d∗ν = 2log(2π)c + lim_{t→∞} ( ∫ (1 − f_0^{2t}) ψ(ν) d∗ν − 2c log t ),
where one assumes that ψ − c f_1^{−1} is integrable on R_+^* , and
f_0(ν) = inf(ν^{1/2}, ν^{−1/2}) ∀ν∈R_+^*, f_1 = f_0^{-1} − f_0.

The Weil explicit formula is then,

Theorem 1. ([W]) With the above notations one has S(X,F) = Δ( F(|w|) X(w) ).

We shall now elaborate on this formula and in particular compare the principal values Pfw with those of theorem V.3.

Let us make the following change of variables,
|g|^{-1/2} h(g^{-1}) = F(|g|) X_0(g),
and rewrite the above equality in terms of h.

By (3) one has,
Φ(1/2 + is) = ∫_{C_k} F(|g|) |g|^{-is} d∗g,
thus, in terms of h
∫ h(g) X_1(g) |g|^{1/2 + is} d∗g = ∫ F(|g^{-1}|) X_0(g^{-1}) X_1(g) |g|^{is} d∗g,
which is equal to 0 if X_1/C_{k,1} ≠ X_0/C_{k,1} and for X_1 = X_0
∫ h(g) X_0(g) |g|^{1/2 + is} d∗g = Φ(1/2 + is).

Thus, with our notations we see that,
Supp ĥ ⊂ X_0 × R, ĥ(X_0, ρ) = Φ(ρ).

Thus we can write,
S(X_0,F) = ∑_{L(X,ρ)=0, X∈\hat{C}_{k,1}, 0<Reρ<1} ĥ(X, ρ)
using a fixed decomposition Ck = C_{k,1} × N.

Let us now evaluate each term in (5).
The first gives (log |d^{-1}|) h(1). One has, using (6) and (12),
⟨D, F(|g|) X_0(g)⟩ = ∫_{C_k} |g|^{-1/2} h(g^{-1}) (|g|^{1/2} + |g|^{-1/2}) d∗g = ∫_{C_k} h(u) (1 + |u|) d∗u = ĥ(0) + ĥ(1),
where for the trivial character of C_{k,1} one uses the notation
ĥ(z) = ĥ(1, z) ∀z∈C.
Thus the first two terms of (5) give
(log |d^{-1}|) h(1) + ĥ(0) + ĥ(1).

Let then v be a place of k, one has by (8) and (12),
⟨D_v, F(|g|) X_0(g)⟩ = Pfw ∫_{k_v^*} \frac{h(u^{-1})}{|1-u|} d∗u.
We can thus write the contribution of the last term of (5) as,
− ∑_v Pfw ∫_{k_v^*} \frac{h(u^{-1})}{|1-u|} d∗u.

Thus the equality of Weil can be rewritten as,
ĥ(0) + ĥ(1) − ∑_{L(X,ρ)=0, X∈\hat{C}_{k,1}, 0<Reρ<1} ĥ(X, ρ) = (log |d|) h(1) + ∑_v Pfw ∫_{k_v^*} \frac{h(u^{-1})}{|1-u|} d∗u.
Which now holds for finite linear combinations of functions h of the form (12). This is enough to conclude when h(1) = 0.

Let us now compare the Weil Principal values, with those dictated by theorem V.3. We first work with a local field K and compare (9), (10) with our prescription. Let first K be non Archimedean. Let α be a character of K such that,
α/R = 1, α/π^{-1}R ≠ 1.
Then, for the Fourier transform given by,
(Ff)(x) = ∫ f(y) α(y) dy,
with dy the selfdual Haar measure, one has
F(1_R) = 1_R.

Lemma 2. With the above choice of α one has
∫′ \frac{h(u^{-1})}{|1-u|} d∗u = Pfw ∫ \frac{h(u^{-1})}{|1-u|} d∗u
with the notations of theorem 3.

Proof. By construction the two sides can only differ by a multiple of h(1). Let us recall from theorem 3 that the left hand side is given by
⟨ L, \frac{h(u^{-1})}{|u|} ⟩,
where L is the unique extension of ρ^{-1} \frac{du}{|1-u|} whose Fourier transform vanishes at 1, \hat{L}(1)=0. Thus from (9) we just need to check that (25) vanishes for h = 1_{R^*}, i.e. that
⟨L, 1_{R^*}⟩ = 0.
Equivalently, if we let Y = { y∈K ; |y-1| = 1 } we just need to show, using Parseval, that,
⟨ log |u|, \hat{1}_Y ⟩ = 0.
One has \hat{1}_Y(x) = ∫_Y α(xy) dy = α(x) \hat{1}_{R^*}(x), and 1_{R^*} = 1_R − 1_P, \hat{1}_{R^*} = 1_R − |π| 1_{π^{-1}R}, thus, with q^{-1}=|π|
\hat{1}_Y(x) = α(x) (1_R − \frac{1}{q} 1_{π^{-1}R})(x).

A = −\frac{1}{q} ∫_{π^{-1}R^*} α(x) (log q) dx, B = (1−\frac{1}{q}) ∫_R log|x| dx.
Let us show that A+B = 0. One has ∫_R dx = 1, and
A = −∫_{R^*} α(π^{-1}y) (log q) dy = −log q (∫_R α(π^{-1}y) dy − ∫_P dy) = \frac{1}{q} log q, since ∫_R α(π^{-1}y) dy = 0 as α/π^{-1}R ≠ 1.
To compute B, note that ∫_{π^n R^*} dy = q^{-n}(1−1/q) so that
B = (1−1/q)^2 ∑_{n=0}^∞ (−n log q) q^{-n} = −q^{-1} log q.
and A+B=0.

Let us now treat the case of Archimedean fields. We take K = R first, and we normalize the Fourier transform as,
(Ff)(x) = ∫ f(y) e^{-2π i x y} dy
so that the Haar measure dx is selfdual.

With the notations of (10) one has,
Pfw ∫_{R^*} f_0^3(|u|) \frac{|u|^{1/2}}{|1-u|} d∗u = log π + γ
where γ is Euler's constant, γ = −Γ'(1). Indeed integrating over the fibers gives f_0^4 × (1−f_0^4)^{-1}, and one gets,
PF_0 ∫_{R_+^*} f_0^4 (1−f_0^4)^{-1} d∗u = log(2π) + lim_{t→∞} ( ∫_{R_+^*} (1−f_0^{2t}) f_0^4 (1−f_0^4)^{-1} d∗u − log t ) = log2π + γ − log2.

Now let φ(u) = −log|u|, it is a tempered distribution on R and one has,
⟨φ, e^{-π u^2}⟩ = \frac{1}{2} log π + \frac{γ}{2} + log 2,
as one obtains from ∂/∂s ∫ |u|^{-s} e^{-π u^2} du = ∂/∂s (π^{(s-1)/2} Γ((1−s)/2)) evaluated at s=0, using Γ'(1/2)/Γ(1/2) = −γ −2log2.
Thus by the Parseval formula one has,
⟨\hat{φ}, e^{-π x^2}⟩ = \frac{1}{2} log π + \frac{γ}{2} + log 2,
which gives, for any test function f,
⟨\hat{φ}, f⟩ = lim_{ε→0} ( ∫_{|x|≥ε} f(x) d∗x + (log ε) f(0) ) + λ f(0)
where λ = log(2π) + γ. In order to get (34) one uses the equality,
lim_{ε→0} ( ∫_{|x|≥ε} f(x) d∗x + (log ε) f(0) ) = lim_{ε→0} ( ∫ f(x) |x|^ε d∗x − \frac{1}{ε} f(0) ),
which holds since both sides vanish for f(x)=1 if |x|≤1, f(x)=0 otherwise.
Thus from (34) one gets,
∫′_R f(u) \frac{1}{|1-u|} d∗u = λ f(1) + lim_{ε→0} ( ∫_{|1-u|≥ε} \frac{f(u)}{|1-u|} d∗u + (log ε) f(1) ).
Taking f(u) = |u|^{1/2} f_0^3(|u|), the right hand side of (36) gives λ − log2 = log π + γ, thus we conclude using (31) that for any test function f,
∫′_R f(u) \frac{1}{|1-u|} d∗u = Pfw ∫_R f(u) \frac{1}{|1-u|} d∗u.

Let us finally consider the case K = C. We choose the basic character α as
α(z) = exp 2πi(z + \bar{z}),
the selfdual Haar measure is dz d\bar{z} = |dz∧d\bar{z}|, and the function f(z) = exp −2π|z|^2 is selfdual.
The normalized multiplicative Haar measure is
d∗z = \frac{|dz∧d\bar{z}|}{2π|z|^2}.
Let us compute the Fourier transform of the distribution
φ(z) = −log|z|_C = −2 log|z|.

One has
⟨φ, exp −2π|z|^2⟩ = log 2π + γ,
as is seen using ∂/∂ε ( ∫ e^{-2π|z|^2} |z|^{-2ε} |dz∧d\bar{z}| ) = ∂/∂ε ( (2π)^ε Γ(1−ε) ).
Thus ⟨\hat{φ}, exp −2π|u|^2⟩ = log 2π + γ and one gets,
⟨\hat{φ}, f⟩ = lim_{ε→0} ( ∫_{|u|≥ε} f(u) d∗u + log ε f(0) ) + λ′ f(0)
where λ′ = 2(log 2π + γ).
To see this one uses the analogue of (35) for K=C, to compute the right hand side of (42) for f(z)=exp −2π|z|^2.

Thus, for any test function f, one has,
∫′_C f(u) \frac{1}{|1-u|_C} d∗u = λ′ f(1) + lim_{ε→0} ( ∫_{|1-u|_C ≥ ε} \frac{f(u)}{|1-u|_C} d∗u + (log ε) f(1) ).

Let us compare it with Pfw. When one integrates over the fibers of C^* → R_+^* the function |1−z|_C^{-1} one gets,
\frac{1}{2π} ∫_0^{2π} \frac{1}{|1−e^{iθ}z|^2} dθ = \frac{1}{1−|z|^2} if |z|<1, and \frac{1}{|z|^2−1} if |z|>1.
Thus for any test function f on R_+^* one has, by (10),
Pfw ∫ f(|u|_C) \frac{1}{|1-u|_C} d∗u = PF_0 ∫ f(ν) \frac{1}{|1−ν|} d∗ν
with the notations of (11). With f_2(ν) = ν^{1/2} f_0(ν) we thus get, using (11),
Pfw ∫ f_2(|u|_C) \frac{1}{|1-u|_C} d∗u = PF_0 ∫ f_0 f_1^{-1} d∗ν = 2(log 2π + γ).
We shall now show that,
lim_{ε→0} ( ∫_{|1-u|_C ≥ ε} \frac{f_2(|u|_C)}{|1-u|_C} d∗u + log ε ) = 0,
it will then follow that, using (43),
∫′_C f(u) \frac{1}{|1-u|_C} d∗u = Pfw ∫_C f(u) \frac{1}{|1-u|_C} d∗u.

To prove (47) it is enough to investigate the integral,
∫_{|z|≤1, |1−z|≥ε} ((1−z)(1−\bar{z}))^{-1} |dz∧d\bar{z}| = j(ε)
and show that j(ε) = α log ε + o(1) for ε→0. A similar statement then holds for ∫_{|z|≤1, |1−z^{-1}|≥ε} ... .
One has j(ε) = ∫_D |dZ∧d\bar{Z}|, where Z = log(1−z) and the domain D is contained in the rectangle,
{ Z = (x+iy); log ε ≤ x ≤ log 2, −π/2 ≤ y ≤ π/2 } = R_ε
and bounded by the curve x = log(2 cos y) which comes from the equation of the circle |z|=1 in polar coordinates centered at z=1. One thus gets,
j(ε) = 4 ∫_{log ε}^{log 2} Arc cos(e^x/2) dx,
when ε→0 one has j(ε) ∼ 2π log(1/ε), which is the area of the following rectangle (in the measure |dz∧d\bar{z}|)
{ Z = (x+iy); log ε ≤ x ≤ 0, −π/2 ≤ y ≤ π/2 }
One has |R_ε| − 2π log 2 = 2π log(1/ε). When ε→0 the area of R_ε \ D converges to
4 ∫_{-∞}^{log 2} Arc sin(e^x/2) dx = −4 ∫_0^{π/2} log(sin u) du = 2π log 2,
so that j(ε) = 2π log(1/ε) + o(1) when ε→0.

Thus we can assert that with the above choice of basic characters for local fields one has, for any test function f
∫_K′ f(u) \frac{1}{|1-u|} d∗u = Pfw ∫_K f(u) \frac{1}{|1-u|} d∗u.

Lemma 3. Let K be a local field, α_0 a normalized character as above and α(x)=α_0(λx) an arbitrary character of K. Let ∫′ be defined as in theorem V.3 relative to α, then, for any test function f
∫_K′ f(u) \frac{1}{|1-u|} d∗u = log |λ| f(1) + Pfw ∫_K f(u) \frac{1}{|1-u|} d∗u.

Proof. The new selfdual Haar measure is da = |λ|^{1/2} d_0 a with d_0 selfdual for α_0. Similarly the new Fourier transform is given by
\hat{f}(x) = ∫ α(xy) f(y) dy = ∫ α_0(λ x y) f(y) |λ|^{1/2} d_0 y,
thus \hat{f}(x) = |λ|^{1/2} \hat{f}^0(λ x).
Let then φ(u) = −log|u|. Its Fourier transform as a distribution is given by,
⟨\hat{φ}, f⟩ = ∫ (−log|u|) \hat{f}(u) du.
One has
∫ (−log|u|) \hat{f}(u) du = ∫ (−log|u|) \hat{f}^0(λ u) |λ| d_0 u = ∫ (−log|v|) \hat{f}^0(v) d_0 v + ∫ log|λ| \hat{f}^0(v) d_0 v = ∫ (−log|v|) \hat{f}^0(v) d_0 v + log|λ| f(0).
Thus the lemma follows from (54).

Let us now pass to the global case, recall that if α, α≠1, is a character of A such that α/k=1, there exists a differential idele d = (d_v) such that, (cf. [W1])
α_v(x) = α_{0,v}(d_v x)
where α = Π α_v and each local character α_{0,v} is normalized as above.

We can thus rewrite the Weil formula (theorem 1) as,

Theorem 6. Let k be a global field, α a non trivial character of A/k and α = Π α_v its local factors. Let h ∈ S(C_k) have compact support, then
ĥ(0) + ĥ(1) − ∑_{L(X,ρ)=0, 0<Reρ<1} ĥ(X,ρ) = ∑_v ∫_{k_v^*}′ \frac{h(u^{-1})}{|1-u|} d∗u
where the normalization of ∫′ is given by α_v as in theorem V.3, and ĥ(X,z) = ∫ h(u) X(u) |u|^z d∗u.

Proof. This follows from formula (21), lemma 3 and the equality log|d| = ∑_v log|d_v|.

## Normalization of Haar measure on modulated group

We let G be a locally compact abelian group with a proper morphism,
g → |g|, G → R_+^*
whose range is cocompact in R_+^*.

There exists a unique Haar measure d∗g on G such that
∫_{|g|∈[1,Λ]} d∗g ∼ log Λ when Λ → +∞.

Let G_0 = Ker mod = { g∈G ; |g|=1 }. It is a compact group by hypothesis, and one can identify G/G_0 with the range N of the module. Let us determine the measure d∗n on N ⊂ R_+^* such that (2) holds for
∫ f d∗g = ∫ (∫ f(n g_0) dg_0) d∗n
where the Haar measure dg_0 is normalized by
∫_{G_0} dg_0 = 1.

We let ρ_Λ be the function on G given by
ρ_Λ(g) = 0 if |g|∉[1,Λ], ρ_Λ(g) = 1/log Λ if g∈[1,Λ].
The normalization (2) means that ∫ ρ_Λ d∗g → 1 when Λ→∞.

Let first N = R_+^* then the unique measure satisfying (2) is
d∗λ = dλ/λ.

Let then N = μ^Z for some μ>1. Let us consider the measure
∫ f d∗g = α ∑ f(μ^n).
We take f = ρ_Λ, then the right hand side is α N/log Λ where N is the number of μ^n∈[1,Λ], i.e. ∼ log Λ/log μ. This shows that (2) holds iff
α = log μ.

Let us show more generally that if H ⊂ G is a compact subgroup of G and if both d∗g and d∗h are normalized by (2) one has
∫ (∫ f(h y) d∗h) d_0 y = ∫ f d∗g
where d_0 y is the Haar measure of integral 1 on G/H
∫_{G/H} d_0 y = 1.
The left hand side of (9) defines a Haar measure on G and we just need to show that it satisfies (2).
One has ‖ρ_Λ(· y) − ρ_Λ‖_1 → 0 when Λ→∞, and
∫ ρ_Λ(h y) d∗h → 1 when Λ→∞
uniformly on compact sets of y∈G, thus
∫ (∫ ρ_Λ(h y) d∗h) d_0 y → 1 when Λ→∞.

---

## Appendix III. Distribution trace formulas

In this appendix we recall for the convenience of the reader the coordinate free treatment of distributions of [GS] and give the details of the transversality conditions.

Given a vector space E over R, dim E = n, a density is a map, ρ ∈ |E|,
ρ : ∧^n E → C
ρ(λ v) = |λ| ρ(v) ∀λ∈R, ∀v∈∧^n E.

Given a linear map T: E → F we let |T| : |F| → |E| be the corresponding linear map, it depends contravariantly on T.

Given a manifold M and ρ ∈ C_c^∞(M, |T M|) one has a canonical integral,
∫ ρ ∈ C.

Given a vector bundle L on M one defines the generalized sections on M as the dual space of C_c^∞(M, L^* ⊗ |T M|)
C^{-∞}(M, L) = dual of C_c^∞(M, L^* ⊗ |T M|)
where L^* is the dual bundle. One has a natural inclusion,
C^∞(M, L) ⊂ C^{-∞}(M, L)
given by the pairing
σ ∈ C^∞(M, L), s ∈ C_c^∞(M, L^* ⊗ |T M|) → ∫ ⟨s, σ⟩
where ⟨s, σ⟩ is viewed as a density, ⟨s, σ⟩ ∈ C_c^∞(M, |T M|).

One has a similar notion of generalized section with compact support.

Given a smooth map φ : X → Y, then if φ is proper, it gives a (contravariantly) associated map
φ^* : C_c^∞(Y, L) → C_c^∞(X, φ^*(L)), (φ^*ξ)(x) = ξ(φ(x))
where φ^*(L) is the pull back of the vector bundle L.

Thus, given a linear form on C_c^∞(X, φ^*(L)) one has a (covariantly) associated linear form on C_c^∞(Y, L). In particular with L trivial we see that given a generalized density ρ ∈ C^{-∞}(X, |T|) one has a pushforward
φ_*(ρ) ∈ C^{-∞}(Y, |T|)
with ⟨φ_*(ρ), ξ⟩ = ⟨ρ, φ^*ξ⟩ ∀ξ∈C_c^∞(X).

Next, if φ is a fibration and ρ ∈ C_c^∞(X, |T|) is a density then one can integrate ρ along the fibers, the obtained density on Y, φ_*(ρ) is given as in (7) by
⟨φ_*(ρ), f⟩ = ⟨ρ, φ^*f⟩ ∀f∈C^∞(Y)
but the point is that it is not only a generalized section but a smooth section φ_*(ρ) ∈ C_c^∞(Y, |T|).

It follows that if f ∈ C^{-∞}(Y) is a generalized function, then one obtains a generalized function φ^*(f) on X by,
⟨φ^*(f), ρ⟩ = ⟨f, φ_*(ρ)⟩ ∀ρ∈C_c^∞(X, |T|).

In general, the pullback φ^*(f) continues to make sense provided the following transversality condition holds,
d(φ^*(l)) ≠ 0 ∀ l ∈ WF(f),
where WF(f) is the wave front set of f ([GS]). The next point is the construction of the generalized section of a vector bundle L on a manifold X associated to a submanifold Z ⊂ X and a symbol,
σ ∈ C^∞(Z, L ⊗ |N_Z^*|),
where N_Z is the normal bundle of Z. The construction is the same as that of the current of integration on a cycle. Given ξ ∈ C_c^∞(X, L^* ⊗ |T|), the product σ ξ / Z is a density on Z, since it is a section of |T_Z| = |T_X| ⊗ |N_Z^*|. One can thus integrate it over Z. When Z = X one has N_Z^* = {0} and |N_Z^*| has a canonical section, so that the current associated to σ is just given by (5). When Z = pt is a single point x∈X a generalized section of L given by a dirac distribution at x requires not only a vector ξ_x ∈ L_x but also a dual density, i.e. a volume multivector v ∈ |T_x^*|.

Now let φ : X → Y with Z a submanifold of Y and σ as in (11).

Let us assume that φ is transverse to Z, so that for each x∈X with y=φ(x)∈Z one has
φ_*(T_x) + T_{φ(x)}(Z) = T_y Y.

Let
τ_x = { X ∈ T_x, φ_*(X) ∈ T_y(Z) }.
Then φ_* gives a canonical isomorphism,
φ_* : T_x(X)/τ_x ≃ T_y(Y)/T_y(Z) = N_y(Z).

And φ^{-1}(Z) is a submanifold of X of the same codimension as Z with a natural isomorphism of normal bundles
N_{φ^{-1}(Z)} ≃ φ^* N_Z.

In particular, given a (generalized) δ-section of a bundle L with support Z and symbol σ ∈ C^∞(Z, L ⊗ |N_Z^*|) one has a corresponding symbol on φ^{-1}(Z) given by
φ^*σ(x) = σ(φ(x)) ∈ (φ^*L)_x ⊗ |N_x^*|
using the isomorphism (15) i.e. N_x^* ≃ N_{φ(x)}^*.

Now for any δ-section associated to Z,σ, the wave front set is contained in the conormal bundle of the submanifold Z which shows that if φ is transverse to Z the pull back φ^*δ_{Z,σ} of the distribution on Y associated to Z,σ makes sense, it is equal to δ_{φ^{-1}(Z), φ^*(σ)}.

Let us now formulate the Schwartz kernel theorem. One considers a continuous linear map,
T : C_c^∞(Y) → C^{-∞}(X),
the statement is that one can write it as
(Tξ)(x) = ∫ k(x,y) ξ(y) dy
where k(x,y) dy is a generalized section,
k ∈ C^{-∞}(X×Y, pr_Y^*(|T|)).

Let f : X → Y be a smooth map, and T = f^* the operator
(Tξ)(x) = ξ(f(x)) ∀ξ∈C_c^∞(Y).
Let us show that the corresponding k is the δ-section associated to the submanifold of X×Y given by
Graph(f) = { (x, f(x)) ; x∈X } = Z
and identify its symbol, σ ∈ C^∞(Z, pr_Y^*(|T|) ⊗ |N_Z^*|).

Given ξ∈T_x^*(X), η∈T_y^*(Y) one has (ξ,η)∈N_Z^* iff it is orthogonal to (v, f_* v) for any v∈T_x(X), i.e. ⟨v,ξ⟩ + ⟨f_*v,η⟩ = 0 so that
ξ = − f_*^t η.
Thus one has a canonical isomorphism j : T_y^*(Y) ≃ N_Z^*, η → (−f_*^t η, η). The transposed (j^{-1})^t is given by (j^{-1})^t(Y) = class of (0,Y) in N_Z ∀Y∈T_y(Y). Thus, there is a canonical choice of symbol σ
σ = |j^{-1}| ∈ C^∞(Z, pr_Y^*(|T|) ⊗ |N_Z^*|).
We denote the corresponding δ-distribution by
k(x,y) dy = δ(y−f(x)) dy.
One then checks the formula,
∫ δ(y−f(x)) ξ(y) dy = ξ(f(x)) ∀ξ∈C_c^∞(Y).

Let us now consider a manifold M with a flow F_t
F_t(x) = exp(t v)x, v∈C^∞(M, T_M)
and the corresponding map f
f : M×R → M, f(x,t) = F_t(x).

We apply the above discussion with X = M×R, Y = M. The graph of f is the submanifold Z of X×Y
Z = { (x,t,y) ; y = F_t(x) }.

One lets φ be the diagonal map,
φ(x,t) = (x,t,x), φ : M×R → X×Y
and the first issue is the transversality φ ↑ Z.

We thus need to consider (12) for each (x,t) such that φ(x,t)∈Z, i.e. such that x = F_t(x). One looks at the image by φ_* of the tangent space T_x M × R to M×R at (x,t). One lets ∂_t be the natural vector field on R. The image of (X, λ∂_t) is (X, λ∂_t, X) for X∈T_x M, λ∈R. Dividing the tangent space of M×R×M by the image of φ_* one gets an isomorphism,
(X, λ∂_t, Y) → Y−X
with T_x M. The tangent space to Z is { (X′, μ∂_t, (F_t)_* X′ + μ v_{F_t(x)}) ; X′∈T_x M, μ∈R }. Thus the transversality condition means that every element of T_x M is of the form
(F_t)_* X − X + μ v_x, X∈T_x M, μ∈R.

One has
(F_t)_* μ v_x = μ v_x
so that (F_t)_* defines a quotient map, the Poincaré return map
P : T_x / R v_x → T_x / R v_x = N_x
and the transversality condition (31) means exactly,
1−P is invertible.

Let us make this hypothesis and compute the symbol σ of the distribution,
τ = φ^*( δ(y − F_t(x)) dy ).

First, as above, let W = φ^{-1}(Z) = { (x,t) : F_t(x)=x }. The codimension of φ^{-1}(Z) in M×R is the same as the codimension of Z in M×R×M so it is dim M which shows that φ^{-1}(Z) is 1-dimensional. If (x,t)∈φ^{-1}(Z) then (F_s(x), t)∈φ^{-1}(Z). Thus, if we assume that v does not vanish at x, the map,
(x,t) → t
is locally constant on the connected component of φ^{-1}(Z) containing (x,t).

This allows to identify the transverse space to W = φ^{-1}(Z) as the product,
N_{x,t}^W ≃ N_x × R
where to (X, λ∂_t)∈T_{x,t}(M×R) we associate the pair (X̃, λ) given by the class of X in N_x = T_x / R v_x and λ∈R.

The symbol σ of the distribution (35) is a smooth section of |N^{W^*}| tensored by the pull back φ^*(L) where L = pr_Y^* |T_M|, and one has
φ^*(L) ≃ |p^* T_M|
where p(x,t) = x ∀(x,t)∈M×R.

To compute σ one needs the isomorphism,
N_{(x,t)}^W → T_{φ(x,t)}(M×R×M) / T_{φ(x,t)}(Z) = N^Z.
The map φ_* : N_{x,t}^W → N^Z is given by
φ_*(X, λ∂_t) = (1−(F_t)_*) X − λ v, X∈N_x, λ∈R
and the symbol σ is just
σ = |φ_*^{-1}| ∈ |p^* T_M| ⊗ |N^{W^*}|.
This makes sense since φ_*^{-1} : p^* T_M → N^W.

Let us now consider the second projection,
q(x,t) = t ∈ R
and compute the pushforward q_*(τ) of the distribution τ.

By construction δ(y−F_t(x)) dy is a generalized section of pr_Y^* |T|, so that τ is a generalized section of p^*|T| = φ^* pr_Y^* |T|.

Thus q_*(τ) is a generalized function.

We first look at the contribution of a periodic orbit, the corresponding part of φ^{-1}(Z) is of the form,
φ^{-1}(Z) = V × Γ ⊂ M×R
where Γ is a discrete cocompact subgroup of R, while V⊂M is a one dimensional compact submanifold of M.

To compute q_*(τ), we let h(t)|dt| be a 1-density on R and pull it back by q as the section on M×R of the bundle q^*|T|,
ξ(x,t) = h(t)|dt|.

We now need to compute ∫_{φ^{-1}(Z)} ξ σ. We can look at the contribution of each component: V×{T}, T∈Γ.

One gets
T^# \frac{1}{|1−P_T|} h(T).
Where T^# is the length of the primitive orbit or equivalently the covolume of Γ in R for the Haar measure |dt|. We can thus write the contributions of the periodic orbits as
∑_{γ_p} ∑_{Γ} Covol(Γ) \frac{1}{|1−P_T|} h(T).

Where the test function h vanishes at 0.

The next case to consider is when the vector field v_x has an isolated 0, v_{x_0}=0. In that case, the transversality condition (31) becomes
1−(F_t)_* invertible at x_0.
One has F_t(x_0)=x_0 for all t∈R and now the relevant component of φ^{-1}(Z) is {x_0}×R. The transverse space N^W is identified with T_x and the map φ_* : N^W ≃ N^Z is given by:
φ_* = 1−(F_t)_*
Thus the symbol σ is the scalar function |1−(F_t)_*|^{-1}. The generalized section q_* φ^*(δ(y−F_t(x)) dy) is the function, t → |1−(F_t)_*|^{-1}. We can thus write the contribution of the zeros of the flow as,
∑_{zeros} ∫ \frac{h(t)}{|1−(F_t)_*|} dt
where h is a test function vanishing at 0.

We can thus collect the contributions 47 and 50 as
∑_γ ∫_{I_γ} \frac{h(u)}{|1−(F_u)_*|} d∗u
where h is as above, I_γ is the isotropy group of the periodic orbit γ, the haar measure d∗u on I_γ is normalised so that the covolume of I_γ is equal to one and we still write (F_u)_* for its restriction to the transverse space of γ.

---

以上是附录 I, II, III 的全部内容。