以下是论文第III节至第VIII节的完整内容。

---

## III Spectral interpretation of critical zeros

There is a third approach to the problem of the zeros of the Riemann zeta function, due to G. Pólya [P] and M. Kac [K] and pursued further in [J] [BC]. It is based on statistical mechanics and the construction of a quantum statistical system whose partition function is the Riemann zeta function. Such a system was naturally constructed in [BC] and it does indicate using the first line of the dictionary of Noncommutative Geometry (namely the correspondence between quotient spaces and noncommutative algebras) what the space \(X\) should be in general:

\[X = A / k^{*} \quad (1)\]

namely the quotient of the space \(A\) of adeles, \(A = k_A\) by the action of the multiplicative group \(k^*\) ,

\[a\in A,q\in k^{*}\to aq\in A. \quad (2)\]

This space \(X\) already appears in a very implicit manner in the work of Tate and Iwasawa on the functional equation. It is a noncommutative space in that, even at the level of measure theory, it is a tricky quotient space. For instance at the measure theory level, the corresponding von Neumann algebra,

\[R_{01} = L^{\infty}(A)\searrow k^{*} \quad (3)\]

where \(A\) is endowed with its Haar measure as an additive group, is the hyperfinite factor of type \(\Pi_{\infty}\) .

The idele class group \(C_k\) acts on \(X\) by

\[(j,a)\to ja\qquad \forall j\in C_k,a\in X \quad (4)\]

and it was exactly necessary to divide \(A\) by \(k^{*}\) so that (4) makes good sense. We shall come back later to the analogy between the action of \(C_{k}\) on \(R_{01}\) and the action of the Galois group of the maximal abelian extension of \(k\) .

What we shall do now is to construct the Hilbert space \(L_{\delta}^{2}\) of functions on \(X\) with growth indexed by \(\delta >1\) . Since \(X\) is a quotient space we shall first learn in the usual manifold case how to obtain the Hilbert space \(L^{2}(M)\) of square integrable functions on a manifold \(M\) by working only on the universal cover \(\widetilde{M}\) with the action of \(\Gamma = \pi_{1}(M)\) . Every function \(f\in C_{c}^{\infty}(\widetilde{M})\) gives rise to a function \(\widetilde{f}\) on \(M\) by

\[\widetilde{f} (x) = \sum_{\pi (\widetilde{x}) = x}f(\widetilde{x}) \quad (5)\]

and all \(g\in C^{\infty}(M)\) appear in this way. Moreover, one can write the Hilbert space inner product \(\begin{array}{r}{\int_{M}\widetilde{f}_{1}(x)\widetilde{f}_{2}(x)d x} \end{array}\) , in terms of \(f_{1}\) and \(f_{2}\) alone. Thus \(\begin{array}{r}{\| \widetilde{f}\| ^2 = \int \left|\sum_{\gamma \in \Gamma}f(\gamma x)\right|^2 d x} \end{array}\) where the integral is performed on a fundamental domain for \(\Gamma\) acting on \(\widetilde{M}\) . This formula defines a prehilbert space norm on \(C_{c}^{\infty}(\widetilde{M})\) and \(L^{2}(M)\) is just the completion of \(C_{c}^{\infty}(\widetilde{M})\) for that norm. Note that any function of the form \(f - f_{\gamma}\) has vanishing norm and hence disappears in the process of completion. In our case of \(X = A / k^{*}\) we thus need to define the analogous norm on the Bruhat- Schwartz space \(S(A)\) of functions on \(A\) (cf Appendix I for the general definition of the Bruhat- Schwartz space). Since 0 is fixed by the action of \(k^{*}\) the expression \(\sum_{\gamma \in k^{*}}f(\gamma x)\) does not make sense for \(x = 0\) unless we require that \(f(0) = 0\) . Moreover, when \(|x|\rightarrow 0\) , the above sums approximate, as Riemann sums, the product of \(|x|^{- 1}\) by \(\int f dx\) for the additive Haar measure, thus we also require \(\int f dx = 0\) . We can now define the Hilbert space \(L_{\delta}^{2}(X)_{0}\) as the completion of the codimension 2 subspace

\[\mathcal{S}(A)_0 = \{f\in \mathcal{S}(A);f(0) = 0,\int f dx = 0\} \quad (6)\]

for the norm \(\| \|_{\delta}\) given by

\[\| f\|_{\delta}^{2} = \int \left|\sum_{q\in k^{*}}f(qx)\right|^{2}(1 + \log^{2}|x|)^{\delta /2}|x|d^{*}x \quad (7)\]

where the integral is performed on \(A^{*} / k^{*}\) and \(d^{*}x\) is the multiplicative Haar measure on \(A^{*} / k^{*}\) . The ugly term \((1 + \log^{2}|x|)^{\delta /2}\) is there to control the growth of the functions on the non compact quotient. We shall see how to remove it later in section VII. Note that \(|qx| = |x|\) for any \(q\in k^{*}\) .

The key point is that we use the measure \(|x| d^{*}x\) instead of the additive Haar measure \(dx\) . Of course for a local field \(K\) one has \(dx = |x| d^{*}x\) but this fails in the above global situation. Instead one has,

\[dx = \lim_{\epsilon \to 0}\epsilon |x|^{1 + \epsilon}d^{*}x. \quad (8)\]

One has a natural representation of \(C_k\) on \(L_{\delta}^{2}(X)_{0}\) given by

\[(U(j)f)(x) = f(j^{-1}x)\qquad \forall x\in A,j\in C_k \quad (9)\]

and the result is independent of the choice of a lift of \(j\) in \(J_{k} = \mathrm{GL}_{1}(A)\) because the functions \(f - f_{q}\) are in the kernel of the norm. The conditions (6) which define \(\mathcal{S}(A)_0\) are invariant under the action of \(C_k\) and give the following action of \(C_k\) on the 2- dimensional supplement of \(\mathcal{S}(A)_0\subset \mathcal{S}(A)\) this supplement is \(\mathbb{C}\oplus \mathbb{C}(1)\) where \(\mathbb{C}\) is the trivial \(C_k\) module (corresponding to \(f(0)\) ) while the Tate twist \(\mathbb{C}(1)\) is the module

\[(j,\lambda)\to |j|\lambda \quad (10)\]

coming from the equality

\[\int f(j^{-1}x)d x = |j|\int f(x)d x. \quad (11)\]

In order to analyse the representation (9) of \(C_k\) on \(L_{\delta}^{2}(X)_{0}\) we shall relate it to the left regular representation of the group \(C_k\) on the Hilbert space \(L_{\delta}^{2}(C_k)\) obtained from the following Hilbert space square norm on functions,

\[\| \xi \|_{\delta}^{2} = \int_{C_k}|\xi (g)|^{2}(1 + \log^{2}|g|)^{\delta /2}d^{*}g \quad (12)\]

where we have normalized the Haar measure of the multiplicative group \(C_k\) with module,

\[|\mid :C_k\to \mathbb{R}_+^* \quad (13)\]

in such a way that (cf. [W3])

\[\int_{|g|\in [1,\Lambda]}d^{*}g\sim \log \Lambda \quad \mathrm{when}\quad \Lambda \to +\infty . \quad (14)\]

The left regular representation \(V\) of \(C_k\) on \(L_{\delta}^{2}(C_k)\) is

\[(V(a)\xi)(g) = \xi (a^{-1}g)\qquad \forall g,a\in C_k. \quad (15)\]

Note that because of the weight \((1 + \log^{2}|x|)^{\delta /2}\) , this representation is not unitary but it satisfies the growth estimate

\[\| V(g)\| = 0(\log |g|)^{\delta /2}\quad \mathrm{when}\quad |g|\to \infty\]

which follows from the inequality (valid for \(u,v\in \mathbb{R}\)

\[\rho (u + v)\leq 2^{\delta /2}\rho (u)\rho (v),\rho (u) = (1 + u^{2})^{\delta /2}.\]

We let \(E\) be the linear isometry from \(L_{\delta}^{2}(X)_{0}\) into \(L_{\delta}^{2}(C_{k})\) given by the equality,

\[E(f)(g) = |g|^{1 / 2}\sum_{q\in k^{*}}f(qg)\qquad \forall g\in C_{k}. \quad (18)\]

By comparing (7) with (12) we see that \(E\) is an isometry and the factor \(|g|^{1 / 2}\) is dictated by comparing the measures \(|g|d^{*}g\) of (7) with \(d^{*}g\) of (12).

One has \(E(U(a)f)(g) = |g|^{1 / 2}\sum_{k^{*}}(U(a)f)(qg) = |g|^{1 / 2}\sum_{k^{*}}f(a^{- 1}q g) =\) \(|a|^{1 / 2}|a^{- 1}g|^{1 / 2}\sum_{k^{*}}f(qa^{- 1}g) = |a|^{1 / 2}(V(a)E(f))(g).\)

Thus,

\[E U(a) = |a|^{1 / 2}V(a)E. \quad (19)\]

This equivariance shows that the range of \(E\) in \(L_{\delta}^{2}(C_{k})\) is a closed invariant subspace for the representation \(V\) .

The following theorem and its corollary show that the cokernel \(\mathcal{H} = L_{\delta}^{2}(C_{k}) / \mathrm{Im}(E)\) of the isometry \(E\) plays the role of the Polya- Hilbert space. Since \(\mathrm{Im}E\) is invariant under the representation \(V\) we let \(W\) be the corresponding representation of \(C_{k}\) on \(\mathcal{H}\) .

The abelian locally compact group \(C_{k}\) is (non canonically) isomorphic to \(K\times N\) where

\[K = \{g\in C_k;|g| = 1\} ,N = \mathrm{range}| |\subset \mathbb{R}_+^*.\]

For number fields one has \(N = \mathbb{R}_{+}^{*}\) while for fields of non zero characteristic \(N\simeq \mathbb{Z}\) is the subgroup \(q^{\mathbb{Z}}\subset \mathbb{R}_{+}^{*}\) . (Where \(q = p^{\ell}\) is the cardinality of the field of constants).

We choose (non canonically) an isomorphism

\[C_{k}\simeq K\times N. \quad (21)\]

\[\| W(g)\| = 0(\log |g|)^{\delta /2}\]

and its restriction to \(K\) is unitary. Thus \(\mathcal{H}\) splits as a canonical direct sum of pairwise orthogonal subspaces,

\[\mathcal{H} = \underset {\chi \in \widehat{K}}{\oplus}\mathcal{H}_{\chi},\mathcal{H}_{\chi} = \{\xi ;W(g)\xi = \chi (g)\xi ,\forall g\in K\}\]

where \(\chi\) runs through the Pontrjagin dual group of \(K\) , which is the discrete abelian group \(\widehat{K}\) of characters of \(K\) . Using the non canonical isomorphism (21), i.e. the corresponding inclusion \(N \subset C_k\) one can now restrict the representation \(W\) to any of the sectors \(\mathcal{H}_{\chi}\) . When \(\mathrm{char}(k) > 0\) , then \(N \simeq \mathbb{Z}\) and the condition (22) shows that the action of \(N\) on \(\mathcal{H}_{\chi}\) is given by a single operator with unitary spectrum. (One uses the spectral radius formula \(|\mathrm{Spec} w| = \overline{\mathrm{Lim}} \| w^n \|^{1 / n}\) .) When \(\mathrm{Char}(k) = 0\) , we are dealing with an action of \(\mathbb{R}_+^* \simeq \mathbb{R}\) on \(\mathcal{H}_{\chi}\) and the condition (22) shows that this representation is generated by a closed unbounded operator \(D_{\chi}\) with purely imaginary spectrum. The resolvent \(R_{\lambda} = (D_{\chi} - \lambda)^{- 1}\) is given, for \(\mathrm{Re} \lambda > 0\) , by the equality

\[R_{\lambda} = \int_{0}^{\infty}W_{\chi}(e^{s})e^{-\lambda s}ds \quad (24)\]

and for \(\mathrm{Re} \lambda < 0\) by,

\[R_{\lambda} = \int_{0}^{\infty}W_{\chi}(e^{-s})e^{\lambda s}ds \quad (25)\]

while the operator \(D_{\chi}\) is defined by

\[D_{\chi}\xi = \lim_{\epsilon \to 0}\frac{1}{\epsilon} (W_{\chi}(e^{\epsilon}) - 1)\xi . \quad (26)\]

Theorem 1. Let \(\chi \in \widehat{K}\) , \(\delta > 1\) , \(\mathcal{H}_{\chi}\) and \(D_{\chi}\) be as above. Then \(D_{\chi}\) has discrete spectrum, \(\mathrm{Sp} D_{\chi} \subset i \mathbb{R}\) is the set of imaginary parts of zeros of the \(L\) function with Grössencharakter \(\widetilde{\chi}\) which have real part equal to \(\frac{1}{2}\) ; \(\rho \in \mathrm{Sp} D \Leftrightarrow L(\widetilde{\chi}, \frac{1}{2} + \rho) = 0\) and \(\rho \in i \mathbb{R}\) , where \(\widetilde{\chi}\) is the unique extension of \(\chi\) to \(C_k\) which is equal to 1 on \(N\) . Moreover the multiplicity of \(\rho\) in \(\mathrm{Sp} D\) is equal to the largest integer \(n < \frac{1 + \delta}{2}\) , \(n \leq\) multiplicity of \(\frac{1}{2} + \rho\) as a zero of \(L\) .

Theorem 1 has a similar formulation when the characteristic of \(k\) is non zero. The following corollary is valid for global fields \(k\) of arbitrary characteristic.

Corollary 2. For any Schwartz function \(h \in \mathcal{S}(C_k)\) the operator \(W(h) = \int W(g) h(g) d^* g\) in \(\mathcal{H}\) is of trace class, and its trace is given by

\[Trace W(h) = \sum_{\substack{L\left(\widetilde{\chi},\frac{1}{2} + \rho\right) = 0 \\ \rho \in \mathbb{R} / N^{\perp}}} \widehat{h} (\widetilde{\chi}, \rho)\]

where the multiplicity is counted as in Theorem 1 and where the Fourier transform \(\widehat{h}\) of \(h\) is defined by,

\[\widehat{h} (\widetilde{\chi}, \rho) = \int_{C_k} h(u) \widetilde{\chi} (u) |u|^{\rho} d^* u.\]

Note that we did not have to define the \(L\) functions, let alone their analytic continuation, before stating the theorem, which shows that the pair

\[(\mathcal{H}_\chi , D_\chi) \quad (27)\]

certainly qualifies as a Polya- Hilbert space.

The case of the Riemann zeta function corresponds to the trivial character \(\chi = 1\) for the global field \(k = \mathbb{Q}\) of rational numbers.

In general the zeros of the \(L\) functions can have multiplicity but one expects that for a fixed Grossencharakter \(\chi\) this multiplicity is bounded, so that for a large enough value of \(\delta\) the spectral multiplicity of \(D\) will be the right one. When the characteristic of \(k\) is \(>0\) this is certainly true.

If we modify the choice of non canonical isomorphism (21) this modifies the operator \(D\) by

\[D^{\prime} = D - i s \quad (28)\]

where \(s \in \mathbb{R}\) is determined by the equality

\[\widetilde{\chi} '(g) = \widetilde{\chi} (g) |g|^{\mathrm{is}} \quad \forall g \in C_k. \quad (29)\]

The coherence of the statement of the theorem is insured by the equality

\[L(\widetilde{\chi}', z) = L(\widetilde{\chi}, z + i s) \quad \forall z \in \mathbb{C}. \quad (30)\]

When the zeros of \(L\) have multiplicity and \(\delta\) is large enough the operator \(D\) is not semisimple and has a non trivial Jordan form (cf. Appendix I). This is compatible with the almost unitary condition (22) but not with skew symmetry for \(D\) .

The proof of theorem 1, explained in Appendix I, is based on the distribution theoretic interpretation by A. Weil [W2] of the idea of Tate and Iwasawa on the functional equation. Our construction should be compared with [Bg] and [Z].

As we expected from (C), the Polya- Hilbert space \(\mathcal{H}\) appears as a cokernel. Since we obtain the Hilbert space \(L_{\delta}^{2}(X)_{0}\) by imposing two linear conditions on \(\mathcal{S}(A)\) ,

\[0\rightarrow \mathcal{S}(A)_0\rightarrow \mathcal{S}(A)\stackrel {L}{\rightarrow}\mathbb{C}\oplus \mathbb{C}(1)\rightarrow 0\]

we shall define \(L_{\delta}^{2}(X)\) so that it fits in an exact sequence of \(C_{k}\) - modules

\[0\rightarrow L_{\delta}^{2}(X)_{0}\rightarrow L_{\delta}^{2}(X)\rightarrow \mathbb{C}\oplus \mathbb{C}(1)\rightarrow 0.\]

We can then use the exact sequence of \(C_{k}\) - modules

\[0\rightarrow L_{\delta}^{2}(X)_{0}\rightarrow L_{\delta}^{2}(C_{k})\rightarrow \mathcal{H}\rightarrow 0\]

together with Corollary 2 to compute in a formal manner what the character of the module \(L_{\delta}^{2}(X)\) should be. Using (32) and (33) we obtain,

\[\mathrm{``Trace"}(U(h)) = \widehat{h} (0) + \widehat{h} (1) - \sum_{\stackrel{L(\chi,\rho) = 0}{\mathrm{Re}\rho = \frac{1}{2}}}\widehat{h} (\chi ,\rho) + \infty h(1)\]

where \(\widehat{h} (\chi ,\rho)\) is defined by Corollary 2 and

\[U(h) = \int_{C_k}U(g)h(g)d^*g \quad (35)\]

while the test function \(h\) is in a suitable function space. Note that the trace on the left hand side of (34) only makes sense after a suitable regularisation since the left regular representation of \(C_{k}\) is not tracable. This situation is similar to the one encountered by Atiyah and Bott ([AB]) in their proof of the Lefchetz formula. We shall first learn how to compute in a formal manner

the above trace from the fixed points of the action of \(C_k\) on \(X\) . In section VII, we shall show how to regularize the trace and completely eliminate the parameter \(\delta\) .

---

## IV The distribution trace formula for flows on manifolds

In order to understand how the left hand side of III(34) should be computed we shall first give an account of the proof of the usual Lefchetz formula by Atiyah- Bott ([AB]) and describe the computation of the distribution theoretic trace for flows on manifolds, which is a variation on the theme of [AB] and is due to Guillemin- Sternberg [GS]. We refer to Appendix III for a more detailed coordinate independent treatment following [GS].

Let us start with a diffeomorphism \(\phi\) of a smooth compact manifold \(M\) and assume that the graph of \(\phi\) is transverse to the diagonal in \(M\times M\) One can then easily define and compute the distribution theoretic trace of the operator \(U:C^{\infty}(M)\to C^{\infty}(M)\)

\[(U\xi)(x) = \xi (\phi (x)). \quad (1)\]

Indeed let \(k(x,y)\) be the Schwartz distribution on \(M\times M\) such that

\[(U\xi)(x) = \int k(x,y)\xi (y)dy, \quad (2)\]

The distributional trace of \(U\) is simply

\["Trace"(U) = \int k(x,x)dx, \quad (3)\]

Near the diagonal and in local coordinates one gets,

\[k(x,y) = \delta (y - \phi (x)) \quad (4)\]

where \(\delta\) is the Dirac distribution.

Since, by hypothesis, the fixed points of \(\phi\) are isolated, one can compute the trace (3) as a finite sum \(\sum_{x,\phi (x) = x}\) and get the contribution of each fixed point \(x\in M\) \(\phi (x) = x\) ,as

\[\frac{1}{|1 - \phi^{\prime}(x)|} \quad (5)\]

\[\int \delta (y - \phi (y))dy.\]

One thus gets (cf. [AB]),

\[\mathrm{``Trace"}(U) = \sum_{x,\phi (x) = x}\frac{1}{|1 - \phi^{\prime}(x)|}. \quad (7)\]

This computation immediately extends to the action of \(\phi\) on sections of an equivariant vector bundle \(E\) such as the bundle \(\Lambda^k T^*\) whose sections, \(C^\infty (M, E)\) are the smooth forms of degree \(k\) . The alternate sum of the corresponding distribution theoretic traces is the ordinary trace of the action of \(\phi\) on the de Rham cohomology, thus yielding the usual Lefchetz formula,

\[\sum (-1)^j\mathrm{Trace}\phi^* /H^j = \sum_{\phi (x) = x}\mathrm{sign}\mathrm{det}(1 - \phi '(x)). \quad (8)\]

Let us refer to the appendix for more pedantic notations which show that the distribution theoretic trace is coordinate independent.

We shall now write down the analogue of formula (7) in the case of a flow \(F_{t} = \exp (t v)\) of diffeomorphisms of \(M\) , where \(v \in C^\infty (M, T)\) is a vector field on \(M\) . We get a one parameter group of operators acting on \(C^\infty (M)\) ,

\[(U_{t}\xi)(x) = \xi (F_{t}(x))\qquad \forall \xi \in C^{\infty}(M),x\in M,t\in \mathbb{R}, \quad (9)\]

and we need the formula for,

\[\rho (h) = \mathrm{``Trace"}\left(\int h(t)U_{t}dt\right),h\in C_{c}^{\infty}(\mathbb{R}),h(0) = 0. \quad (10)\]

The condition \(h(0) = 0\) is required because we cannot expect that the identity map \(F_{0}\) is transverse to the diagonal. In order to define \(\rho\) as a distribution evaluated on the test function \(h\) , we let \(f\) be the following map,

\[f:X = M\times \mathbb{R}\rightarrow Y = M,f(x,t) = F_{t}(x). \quad (11)\]

The graph of \(f\) is the submanifold \(Z\) of \(X \times Y\) ,

\[Z = \{(x,t,y):y = F_{t}(x)\} . \quad (12)\]

\[\phi (x,t) = (x,t,x),\phi :M\times \mathbb{R}\to X\times Y\]

and one assumes the transversality \(\phi \vdash \mathcal{Z}\) outside \(M\times (0)\) let \(\tau\) be the distribution,

\[\tau = \phi^{*}(\delta (y - F_{t}(x))dy),\]

and \(q\) be the second projection,

\[q(x,t) = t\in \mathbb{R},\]

then by definition \(\rho\) is the pushforward \(q_{*}(\tau)\) of the distribution \(\tau\)

One checks (cf. Appendix III) that \(q_{*}(\tau)\) is a generalized function.

Exactly as in the case of a single transformation, the contributions to (10) will come from the fixed points of \(F_{t}\) . The latter will come either from a zero of the vector field \(v\) , (i.e. \(x\in M\) such that \(v_{x} = 0\) ) or from a periodic orbit \(\gamma\) of the flow and we call \(T_{\gamma}^{\#}\) the length of such a periodic orbit. Under the above transversality hypothesis the formula for (10) is (cf. [GS], [G] and the Appendix III),

\[\begin{array}{r l} & {\mathrm{~``Trace"~}\left(\int h(t)U_{t}d t\right) =}\\ & {\sum_{x,v_{x} = 0}\int \frac{h(t)}{|1 - (F_{t})_{*}|} d t + \sum_{\gamma}\sum_{T}T_{\gamma}^{\#}\frac{1}{|1 - (F_{T / })_{*}|} h(T)} \end{array} \quad (16)\]

where in the second sum \(\gamma\) is a periodic orbit with length \(T_{\gamma}^{\#}\) , and \(T\) varies in \(\mathcal{Z}T_{\gamma}^{\#}\) while \((F_{T / })_{*}\) is the Poincare return map, i.e. the restriction of the tangent map to the transversal of the orbit.

One can rewrite (16) in a better way as,

\[\mathrm{~``Trace"~}\left(\int h(t)U_{t}d t\right) = \sum_{\gamma}\int_{I_{\gamma}}\frac{h(u)}{|1 - (F_{u})_{*}|} d^{*}u, \quad (17)\]

where the zeros \(x\in M\) \(v_{x} = 0\) , are considered also as periodic orbits \(\gamma\) , while \(I_{\gamma}\subset \mathbb{R}\) is the isotopy subgroup of any \(x\in \gamma\) , and \(d^{*}u\) is the unique Haar measure in \(I_{\gamma}\) such that the covolume of \(I_{\gamma}\) is equal to 1, i.e. such that for the unique Haar measure \(d\mu\) of total mass 1 on \(\mathbb{R} / I\) and any \(f\in C_{c}^{\infty}(\mathbb{R})\)

\[\int_{\mathbb{R}}f(t)d t = \int_{\mathbb{R} / I}\left(\int_{I}f(u + s)d^{*}u\right)d\mu (s),\]

Also we still write \((F_{u})_{*}\) for the restriction of the tangent map to \(F_{u}\) to the transverse space of the orbits.

To understand what \((F_{t})_{*}\) looks like at a zero of \(v\) we can replace \(v(x)\) for \(x\) near \(x_{0}\) by its tangent map. For simplicity we take the one dimensional case, with \(v(x) = x \frac{\partial}{\partial x}\) , acting on \(\mathbb{R} = M\) .

One has \(F_{t}(x) = e^{t} x\) . Since \(F_{t}\) is linear the tangent map \((F_{t})_{*}\) is

\[(F_{t})_{*} = e^{t}\]

and (12) becomes

\[(\mathrm{Trace})^{\prime}\left(\int h(t)U_{t}dt\right) = \int \frac{h(t)}{|1 - e^{t}|} dt,\]

Thus for this flow the distribution trace formula is

\[(\mathrm{Trace})^{\prime}(U(h)) = \int \frac{h(u)}{|1 - u|} d^{*}u\]

where we used the multiplicative notation so that \(\mathbb{R}_{+}^{*}\) acts on \(\mathbb{R}\) by multiplication, while \(U(h) = \int U(v)h(v) d^{*}v\) and \(d^{*}v\) is the haar measure of the group \(\mathbb{R}_{+}^{*}\) .

One can treat in a similar way the action, by multiplication, of the group of non zero complex numbers on the manifold \(\mathbb{C}\) .

We shall now investigate the more general case of an arbitrary local field.

---

## V The action \((\lambda ,x)\to \lambda x\) of \(K^{*}\) on a local field \(K\) .

We let \(K\) be a local field and consider the map,

\[f:K\times K^{*}\to K,f(x,\lambda) = \lambda x\]

together with the diagonal map,

\[\phi :K\times K^{*}\to K\times K^{*}\times K,\phi (x,\lambda) = (x,\lambda ,x)\]

as in IV (11) and (12) above.

When \(K\) is Archimedian we are in the framework of manifolds and we can associate to \(f\) a \(\delta\) - section with support \(Z = \mathrm{Graph}(f)\) ,

\[\delta_{Z} = \delta (y - \lambda x)dy. \quad (3)\]

Using the projection \(q(x, \lambda) = \lambda\) from \(K \times K^{*}\) to \(K^{*}\) we then consider as above the generalized function on \(K^{*}\) given by,

\[q_{*}(\phi^{*}\delta_{Z}). \quad (4)\]

The formal computation of this generalized function of \(\lambda\) is

\[\int \delta (x - \lambda x)d x = \int \delta ((1 - \lambda)x)d x = \int \delta (y)d((1 - \lambda)^{-1}y)\] \[= |1 - \lambda |^{-1}\int \delta (y)d y = |1 - \lambda |^{-1}.\]

We want to justify it by computing the convolution of the Fourier transforms of \(\delta (x - y)\) and \(\delta (y - \lambda x)\) since this is the correct way of defining the product of two distributions in this local context. Let us first compute the Fourier transform of \(\delta (ax + by)\) where \((a, b) \in K^{2}(\neq 0)\) . The pairing between \(K^{2}\) and its dual \(K^{2}\) is given by

\[\langle (x,y),(\xi ,\eta)\rangle = \alpha (x\xi +y\eta)\in U(1). \quad (5)\]

where \(\alpha\) is a fixed nontrivial character of the additive group \(K\) .

Let \((c,d) \in K^{2}\) be such that \(ad - bc = 1\) and consider the linear invertible transformation of \(K^{2}\) ,

\[L\left[ \begin{array}{c}x\\ y \end{array} \right] = \left[ \begin{array}{cc}a & b\\ c & d \end{array} \right]\left[ \begin{array}{c}x\\ y \end{array} \right]. \quad (6)\]

The Fourier transform of \(\phi \circ L\) is given by

\[(\phi \circ L)^{\wedge} = |\operatorname *{det}L|^{-1}\widehat{\phi}\circ (L^{-1})^{t}. \quad (7)\]

Here one has \(\operatorname *{det}L = 1\) and \((L^{- 1})^{t}\) is

\[(L^{-1})^{t} = \left[ \begin{array}{cc}d & -c\\ -b & a \end{array} \right]. \quad (8)\]

One first computes the Fourier transform of \(\delta (x)\) , the additive Haar measure \(dx\) is normalized so as to be selfdual, and in one variable \(\delta (x)\) and 1 are Fourier transforms of each other, thus

\[(\delta \otimes 1)^{\wedge} = 1\otimes \delta . \quad (9)\]

Using (7) one gets that the Fourier transform of \(\delta (a x + b y)\) is \(\delta (- b \xi + a \eta)\) . Thus we have to compute the convolution of the two generalized functions, \(\delta (\xi + \eta)\) and \(\delta (\xi + \lambda \eta)\) . Now

\[\int f(\xi ,\eta)\delta (\xi +\eta)d\xi d\eta = \int f(\xi , - \xi)d\xi\]

and

\[\int f(\xi ,\eta)\delta (\xi +\lambda \eta)d\xi d\eta = \int f(-\lambda \eta ,\eta)d\eta\]

thus we are dealing with two measures carried respectively by two distinct lines. Their convolution evaluated on \(f\in C_{c}^{\infty}(K^{2})\) is \(\begin{array}{r}{\int f(\alpha +\beta)d\mu (\alpha)d\nu (\beta) =} \end{array}\) \(\begin{array}{r}{\int \int f((\xi , - \xi) + (-\lambda \eta ,\eta))d\xi d\eta = \int \int f(\xi -\lambda \eta , - \xi +\eta)d\xi d\eta = \left(\int \int f(\xi^{\prime},\eta^{\prime})\right)} \end{array}\) \(d\xi^{\prime}d\eta^{\prime})\times |J|^{- 1}\) where \(J\) is the determinant of the matrix \(\left[ \begin{array}{cc}1 & -\lambda \\ -1 & 1 \end{array} \right] = L\) so that \(\left[ \begin{array}{c}\xi^{\prime}\\ \eta^{\prime} \end{array} \right] = J\left[ \begin{array}{c}\xi\\ \eta \end{array} \right]\) . One has \(J = 1 - \lambda\) and thus the convolution of the generalized functions \(\delta (\xi +\eta)\) and \(\delta (\xi +\lambda \eta)\) gives as expected the constant function

\[|1 - \lambda |^{-1}1. \quad (10)\]

Correspondingly, the product of the distribution \(\delta (x - y)\) and \(\delta (y - \lambda x)\) gives \(|1 - \lambda |^{- 1}\delta_{0}\) so that,

\[\int \delta (x - y)\delta (y - \lambda x)dxdy = |1 - \lambda |^{-1}. \quad (11)\]

In this local case the Fourier transform alone was sufficient to make sense of the relevant product of distributions. In fact this would continue to make sense if we replace \(\delta (y - \lambda x)\) by \(\int h(\lambda^{- 1})\delta (y - \lambda x)d^{*}\lambda\) where \(h(1) = 0\) .

We shall now treat in detail the more delicate general case where \(h(1)\) is arbitrary.

We shall prove a precise general result (theorem 3) which handles the lack of transversality when \(h(1)\neq 0\) . We deal directly with the following operator in \(L^{2}(K)\)

\[U(h) = \int h(\lambda)U(\lambda)d^{*}\lambda , \quad (12)\]

where the scaling operator \(U(\lambda)\) is defined by

\[(U(\lambda)\xi)(x) = \xi (\lambda^{-1}x)\qquad \forall x\in K \quad (13)\]

and where the multiplicative Haar measure \(d^{*}\lambda\) is normalized by,

\[\int_{|\lambda |\in [1,\Lambda ]}d^{*}\lambda \sim \log \Lambda \qquad \mathrm{when~}\Lambda \to \infty . \quad (14)\]

To understand the "trace" of \(U(h)\) we shall proceed as in the Selberg trace formula ([Se]) and use a cutoff. For this we use the orthogonal projection \(P_{\Lambda}\) onto the subspace,

\[P_{\Lambda} = \{\xi \in L^{2}(K); \xi (x) = 0 \qquad \forall x, |x| > \Lambda \} . \quad (15)\]

Thus, \(P_{\Lambda}\) is the multiplication operator by the function \(\rho_{\Lambda}\) , where \(\rho_{\Lambda}(x) = 1\) if \(|x| \leq \Lambda\) , and \(\rho (x) = 0\) for \(|x| > \Lambda\) . This gives an infrared cutoff and to get an ultraviolet cutoff we use \(\widehat{P}_{\Lambda} = FP_{\Lambda}F^{- 1}\) where \(F\) is the Fourier transform (which depends upon the basic character \(\alpha\) ). We let

\[R_{\Lambda} = \widehat{P}_{\Lambda}P_{\Lambda}. \quad (16)\]

The main result of this section is then,

Theorem 3. Let \(K\) be a local field with basic character \(\alpha\) . Let \(h \in \mathcal{S}(K^{*})\) have compact support. Then \(R_{\Lambda}U(h)\) is a trace class operator and when \(\Lambda \to \infty\) , one has

\[\mathrm{Trace}(R_{\Lambda}U(h)) = 2h(1)\log^{\prime}\Lambda +\int^{\prime}\frac{h(u^{-1})}{|1 - u|} d^{*}u + o(1)\]

where \(2\log^{\prime}\Lambda = \int_{\lambda \in K^{*}, |\lambda |\in [\Lambda^{- 1},\Lambda ]}d^{*}\lambda\) , and the principal value \(\int^{\prime}\) is uniquely determined by the pairing with the unique distribution on \(K\) which agrees with \(\frac{du}{|1 - u|}\) for \(u \neq 1\) and whose Fourier transform vanishes at 1.

Proof. We normalize as above the additive Haar measure to be the selfdual one on \(K\) . Let the constant \(\rho > 0\) be determined by the equality,

\[\int_{1\leq |\lambda |\leq \Lambda}\frac{d\lambda}{|\lambda |}\sim \rho \log \Lambda \qquad \mathrm{when~}\Lambda \to \infty . \quad (17)\]

so that \(d^{*}\lambda = \rho^{- 1}\frac{d\lambda}{|\lambda |}\) . Let \(L\) be the unique distribution, extension of \(\rho^{- 1}\frac{du}{|1 - u|}\) whose Fourier transform vanishes at 1, \(\tilde{L} (1) = 0\) . One then has by definition,

\[\int^{\prime}\frac{h(u^{-1})}{|1 - u|} d^{*}u = \left\langle L,\frac{h(u^{-1})}{|u|}\right\rangle , \quad (18)\]

where \(\frac{h(u^{- 1})}{|u|} = 0\) for \(u^{- 1}\) outside the support of \(h\) .

Let \(T = U(h)\) . We can write the Schwartz kernel of \(T\) as,

\[k(x,y) = \int h(\lambda^{-1})\delta (y - \lambda x)d^{*}\lambda .\]

Given any such kernel \(k\) we introduce its symbol,

\[\sigma (x,\xi) = \int k(x,x + u)\alpha (u\xi)du\]

as its partial Fourier transform. The Schwartz kernel \(r_{\Lambda}^{t}(x,y)\) of the transpose \(R_{\Lambda}^{t}\) is given by,

\[r_{\Lambda}^{t}(x,y) = \rho_{\Lambda}(x)(\widehat{\rho_{\Lambda}})(x - y).\]

Thus, the symbol \(\sigma_{\Lambda}\) of \(R_{\Lambda}^{t}\) is simply,

\[\sigma_{\Lambda}(x,\xi) = \rho_{\Lambda}(x)\rho_{\Lambda}(\xi).\]

The operator \(R_{\Lambda}\) is of trace class and one has,

\[\mathrm{Trace}(R_{\Lambda}T) = \int k(x,y)r_{\Lambda}^{t}(x,y)dxdy.\]

Using the Parseval formula we thus get,

\[\mathrm{Trace}(R_{\Lambda}T) = \int_{|x|\leq \Lambda ,|\xi |\leq \Lambda}\sigma (x,\xi)dxd\xi .\]

Now the symbol \(\sigma\) of \(T\) is given by,

\[\sigma (x,\xi) = \int h(\lambda^{-1})\left(\int \delta (x + u - \lambda x)\alpha (u\xi)du\right)d^{*}\lambda .\]

One has,

\[\int \delta (x + u - \lambda x)\alpha (u\xi)du = \alpha (({\lambda} - 1)x\xi),\]

thus (25) gives,

\[\sigma (x,\xi) = \rho^{-1}\int_{K}g(\lambda)\alpha (\lambda x\xi)d\lambda\]

\[g(\lambda) = h((\lambda +1)^{-1})|\lambda +1|^{-1}.\]

Since \(h\) is smooth with compact support on \(K^{*}\) the function \(g\) belongs to \(C_{c}^{\infty}(K)\) .Thus \(\sigma (x,\xi) = \rho^{- 1}\widehat{g} (x\xi)\) and,

\[\mathrm{Trace}(R_{\Lambda}T) = \rho^{-1}\int_{|x|\leq \Lambda ,|\xi |\leq \Lambda}\widehat{g} (x\xi)dxd\xi .\]

With \(u = x\xi\) one has \(dx d\xi = du\frac{dx}{|x|}\) and, for \(|u|\leq \Lambda^{2}\)

\[\rho^{-1}\int_{\frac{|u|}{\Lambda}\leq |x|\leq \Lambda}\frac{dx}{|x|} = 2\log^{\prime}\Lambda -\log |u|\]

(using the precise definition of \(\log^{\prime}\Lambda\) to handle the boundary terms). Thus we can rewrite (29) as,

\[\mathrm{Trace}(R_{\Lambda}T) = \int_{|u|\leq \Lambda^{2}}\widehat{g} (u)(2\log^{\prime}\Lambda -\log |u|)du \quad (31)\]

Since \(g\in C_{c}^{\infty}(K)\) one has,

\[\int_{|u|\geq \Lambda^{2}}|\widehat{g} (u)|du = O(\Lambda^{-N})\qquad \forall N\]

and similarly for \(|\widehat{g} (u)\log |u||\) .Thus

\[\mathrm{Trace}(R_{\Lambda}T) = 2g(0)\log^{\prime}\Lambda -\int \widehat{g} (u)\log |u|du + o(1). \quad (33)\]

Now for any local field \(K\) and basic character \(\alpha\) , if we take for the Haar measure \(da\) the selfdual one, the Fourier transform of the distribution \(\phi (u) = - \log |u|\) is given outside 0 by

\[\widehat{\phi} (a) = \rho^{-1}\frac{1}{|a|}, \quad (34)\]

with \(\rho\) determined by (17). To see this one lets \(P\) be the distribution on \(K\) given by,

\[P(f) = \lim_{\epsilon \to 0\atop \epsilon \in \mathrm{Mod}(K)}\left(\int_{|x|\geq \epsilon}f(x)d^{*}x + f(0)\log \epsilon\right). \quad (35)\]

One has \(P(f_{a}) = P(f) - \log |a|f(0)\) which is enough to show that the function \(\widehat{P} (x)\) is equal to \(- \log |x| + \mathrm{cst}\) , and \(\widehat{\phi}\) differs from \(P\) by a multiple of \(\delta_{0}\) .Thus the Parseval formula gives, with the convention of theorem 3,

Thus the Parseval formula gives, with the convention of theorem 3,

\[-\int \widehat{g} (u)\log |u|du = \frac{1}{\rho}\int^{\prime}g(a)\frac{da}{|a|}.\]

Replacing \(a\) by \(\lambda - 1\) and applying (28) gives the desired result.

We shall show in appendix II that the privileged principal value, which depends upon the basic character \(\alpha\) , is the same as in Weil's explicit formulas.

---

## VI The global case, and the formal trace computation.

We shall now consider the action of \(C_{k}\) on \(X\) and write down the analogue of IV (17) for the distribution trace formula.

Both \(X\) and \(C_{k}\) are defined as quotients and we let

\[\pi :A\to X,c:\mathrm{GL}_1(A)\to C_k \quad (1)\]

be the corresponding quotient maps.

As above we consider the graph \(Z\) of the action

\[f:X\times C_k\to X,f(x,\lambda) = \lambda x \quad (2)\]

and the diagonal map

\[\phi :X\times C_k\to X\times C_k\times X\qquad \phi (x,\lambda) = (x,\lambda ,x). \quad (3)\]

We first investigate the fixed points, \(\phi^{- 1}(Z)\) , i.e. the pairs \((x,\lambda)\in X\times C_{k}\) such that \(\lambda x = x\) . Let \(x = \pi (\tilde{x})\) and \(\lambda = c(j)\) . Then the equality \(\lambda x = x\) means that \(\pi (j\tilde{x}) = \pi (\tilde{x})\) thus there exists \(q\in k^{*}\) such that with \(\tilde{j} = qj\) , one has

\[\tilde{j}\tilde{x} = \tilde{x}. \quad (4)\]

Recall now that \(A\) is the restricted direct product \(A = \Pi_{k_{v}}\) of the local fields \(k_{v}\) obtained by completion of \(k\) with respect to the place \(v\) . The equality (4) means that \(\tilde{j}_{v}\tilde{x}_{v} = \tilde{x}_{v}\) , thus, if \(\tilde{x}_{v}\neq 0\) for all \(v\) it follows that \(\tilde{j}_{v} = 1\forall v\) and

3 = 1. This shows that the projection of p- 1(Z) n Ck\{1} on X is the union of the hyperplanes

\[\cup H_{v};H_{v} = \pi (\tilde{H}_{v}),\tilde{H}_{v} = \{x;x_{v} = 0\} .\]

Each \(\tilde{H}_{v}\) is closed in \(A\) and is invariant under multiplication by elements of \(k^{*}\) . Thus each \(H_{v}\) is a closed subset of \(X\) and one checks that it is the closure of the orbit under \(C_{k}\) of any of its generic points

\[x,x_{u} = 0\quad \iff \quad u = v. \quad (6)\]

For any such point \(x\) , the isotropy group \(I_{x}\) is the image in \(C_{k}\) of the multiplicative group \(k_{v}^{*}\) ,

\[I_{x} = k_{v}^{*} \quad (7)\]

by the map \(\lambda \in k_{v}^{*}\to (1,\ldots ,1,\lambda ,1,\ldots)\) . This map already occurs in class field theory (cf [W1]) to relate the local Galois theory to the global one.

Both groups \(k_{v}^{*}\) and \(C_{k}\) are commensurable to \(\mathbb{R}_{+}^{*}\) by the module homomorphism, which is proper with cocompact range,

\[G\xrightarrow{||}|_{\mathbb{R}_{+}^{*}}. \quad (8)\]

Since the restriction to \(k_{v}^{*}\) of the module of \(C_{k}\) is the module of \(k_{v}^{*}\) , it follows that

\[I_{x}\mathrm{~is~a~cocompact~subgroup~of~}C_{k}. \quad (9)\]

This allows to normalize the respective Haar measures in such a way that the covolume of \(I_{x}\) is 1. This is in fact insured by the canonical normalisation of the Haar measures of modulated groups ([W3 ]),

\[\int_{|g|\in [1,\Lambda ]}d^{*}g\sim \log \Lambda \mathrm{when}\Lambda \to +\infty . \quad (10)\]

It is important to note that though \(I_{x}\) is cocompact in \(C_{k}\) , the orbit of \(x\) is not closed and one needs to close it, the result being \(H_{v}\) . We shall learn how to justify this point later in section VII, in the similar situation of the action of \(C_{S}\) on \(X_{S}\) . We can now in view of the results of the two preceding sections, write down the contribution of each \(H_{v}\) to the distributional trace;

Since \(\tilde{H}_{v}\) is a hyperplane, we can identify the transverse space \(N_{x}\) to \(H_{v}\) at \(x\) with the quotient

\[N_{x} = A / \tilde{H}_{v} = k_{v}\]

namely the additive group of the local field \(k_{v}\) . Given \(j\in I_{x}\) one has \(j_{u} =\) \(1\forall u\neq v\) , and \(j_{v} = \lambda \in k_{v}^{*}\) . The action of \(j\) on \(A\) is linear and fixes \(x\) , thus the action on the transverse space \(N_{x}\) is given by

\[(\lambda ,a)\to \lambda a\quad \forall a\in k_{v}. \quad (12)\]

We can thus proceed with some faith and write down the contribution of \(H_{v}\) to the distributional trace in the form,

\[\int_{k_{v}^{*}}\frac{h(\lambda)}{|1 - \lambda|} d^{*}\lambda \quad (13)\]

where \(h\) is a test function on \(C_{k}\) which vanishes at 1. We now have to take care of a discrepancy in notation with the third section (formula 9), where we used the symbol \(U(j)\) for the operation

\[(U(j)f)(x) = f(j^{-1}x) \quad (14)\]

whereas we use \(j\) in the above discussion. This amounts to replace the test function \(h(u)\) by \(h(u^{- 1})\) and we thus obtain as a formal analogue of III(17) the following expression for the distributional trace

\["Trace"(U(h)) = \sum_{v}\int_{k_{v}^{*}}\frac{h(u^{-1})}{|1 - u|} d^{*}u. \quad (15)\]

Now the right- hand side of (15) is, when restricted to the hyperplane \(h(1) = 0\) , the distribution obtained by André Weil [W3] as the synthesis of the explicit formulas of number theory for all \(L\) - functions with Grossencharakter. In particular we can rewrite it as

\[\hat{h} (0) + \hat{h} (1) - \sum_{L(\chi ,\rho) = 0}\hat{h} (\chi ,\rho) + \infty h(1) \quad (16)\]

where this time the restriction \(\operatorname {Re}(\rho) = \frac{1}{2}\) has been eliminated.

Thus, equating (34) of section III and (16) for \(h(1) = 0\) would yield the desired information on the zeros. Of course, this does require first eliminating

the role of \(\delta\) , and (as in [AB]) to prove that the distributional trace coincides with the ordinary operator theoretic trace on the cokernel of \(E\) . This is achieved for the usual set- up of the Lefchetz fixed point theorem by the use of families.

A very important property of the right hand side of (15) (and of IV (17) in general) is that if the test function \(h,h(1) = 0\) is positive,

\[h(u)\geq 0\quad \forall u\in C_k \quad (17)\]

then the right- hand side is positive. This indicated from the very start that in order to obtain the Polya- Hilbert space from the Riemann flow, it is not quantization that should be involved but simply the passage to the \(L^2\) space, \(X \to L^2 (X)\) . Indeed the positivity of IV (17) is typical of permutation matrices rather than of quantization. This distinction plays a crucial role in the above discussion of the trace formula, in particular the expected trace formula is not a semi- classical formula but a Lefchetz formula in the spirit of [AB].

The above discussion is not a rigorous justification of this formula. The first obvious obstacle is that the distributional trace is only formal and to give it a rigorous meaning tied up to Hilbert space operators, one needs as in section V, to perform a cutoff. The second difficulty comes from the presence of the parameter \(\delta\) as a label for the Hilbert space, while \(\delta\) does not appear in the trace formula. As we shall see in the next two sections the cutoff will completely eliminate the role of \(\delta\) , and we shall nevertheless show (by proving positivity of the Weil distribution) that the validity of the \((\delta\) independent) trace formula is equivalent to the Riemann Hypothesis for all Grossencharakters of \(k\) .

---

## VII Proof of the trace formula in the \(S\) -local case.

In the formal trace computation of section VI, we skiped over the difficulties inherent to the tricky structure of the space \(X\) . In order to understand how to handle trace formulas on such spaces we shall consider the slightly simpler situation which arises when one only considers a finite set \(S\) of places of \(k\) . As soon as the cardinality of \(S\) is larger than 3, the corresponding space \(X_S\) does share most of the tricky features of the space \(X\) . In particular it is no longer of type I in the sense of Noncommutative Geometry.

We shall nevertheless prove a precise general result (theorem 4) which shows that the above handling of periodic orbits and of their contribution to

the trace is the correct one. It will in particular show why the orbit of the fixed point 0, or of elements \(x \in A\) , such that \(x_{v}\) vanishes for at least two places do not contribute to the trace formula.

At the same time, we shall handle as in section V, the lack of transversality when \(h(1) \neq 0\) .

Let us first describe the reduced framework for the trace formula. We let \(k\) be a global field and \(S\) a finite set of places of \(k\) containing all infinite places. The group \(O_{S}^{*}\) of \(S\) - units is defined as the subgroup of \(k^{*}\) ,

\[O_{S}^{*} = \{q \in k^{*}, |q_{v}| = 1, v \notin S\} \quad (1)\]

It is cocompact in \(J_{S}^{1}\) where,

\[J_{S} = \prod_{v \in S} k_{v}^{*} \quad (2)\]

and,

\[J_{S}^{1} = \{j \in J_{S}, |j| = 1\} . \quad (3)\]

Thus the quotient group \(C_{S} = J_{S} / O_{S}^{*}\) plays the same role as \(C_{k}\) , and acts on the quotient \(X_{S}\) of \(A_{S} = \prod_{v \in S} k_{v}\) by \(O_{S}^{*}\) .

To keep in mind a simple example, one can take \(k = \mathbb{Q}\) , while \(S\) consists of the three places 2, 3, and \(\infty\) . One checks in this example that the topology of \(X_{S}\) is not of type I since for instance the group \(O_{S}^{*} = \{\pm 2^{n}3^{m}; n, m \in \mathbb{Z}\}\) acts ergodically on \(\{0\} \times \mathbb{R} \subset A_{S}\) .

We normalize the multiplicative Haar measure \(d^{*} \lambda\) of \(C_{S}\) by,

\[\int_{|\lambda | \in [1, \Lambda ]} d^{*} \lambda \sim \log \Lambda \qquad \text{when} \Lambda \to \infty , \quad (4)\]

and normalize the multiplicative Haar measure \(d^{*} \lambda\) of \(J_{S}\) so that it agrees with the above on a fundamental domain \(D\) for the action of \(O_{S}^{*}\) on \(J_{S}\) .

There is no difficulty in defining the Hilbert space \(L^{2}(X_{S})\) of square integrable functions on \(X_{S}\) . We proceed as in section III (without the \(\delta\) ), and complete (and separate) the Schwartz space \(\mathcal{S}(A_{S})\) for the pre- Hilbert structure given by,

\[\| f\|^{2} = \int \left|\sum_{q \in O_{S}^{*}} f(qx)\right|^{2} |x| d^{*}x \quad (5)\]

where the integral is performed on \(C_{S}\) or equivalently on a fundamental domain \(D\) for the action of \(O_{S}^{*}\) on \(J_{S}\) . To show that (5) makes sense, one proves that for \(f\in \mathcal{S}(A_{S})\) , the function \(E_{0}(f)(x) = \sum_{q\in O_{S}^{*}}f(qx)\) is bounded above by a power of \(L o g|x|\) when \(|x|\) tends to zero. To see this when \(f\) is the characteristic function of \(\{x\in A_{S},|x_{v}|\leq 1,\forall v\in S\}\) , one uses the cocompactness of \(O_{S}^{*}\) in \(J_{S}^{1}\) , to replace the sum by an integral. The latter is then comparable to,

\[\int_{u_{i}\geq 0,\sum u_{i} = -L o g|x|}\prod d u_{i}, \quad (6)\]

where the index \(i\) varies in \(S\) . The general case follows.

The scaling operator \(U(\lambda)\) is defined by,

\[(U(\lambda)\xi)(x) = \xi (\lambda^{-1}x)\qquad \forall x\in A_{S} \quad (7)\]

and the same formula, with \(x\in X_{S}\) defines its action on \(L^{2}(X_{S})\) . Given a smooth compactly supported function \(h\) on \(C_{S}\) , \(U(h) = \int h(g)U(g)dg\) makes sense as an operator acting on \(L^{2}(X_{S})\) .

We shall now show that the Fourier transform \(F\) on \(\mathcal{S}(A_{S})\) does extend to a unitary operator on the Hilbert space \(L^{2}(X_{S})\) .

Lemma 1. a) For any \(f_{i}\in \mathcal{S}(A_{S})\) the series \(\begin{array}{r}{\sum_{O_{S}^{*}}\langle f_{1},U(q)f_{2}\rangle_{A}} \end{array}\) of inner products in \(L^{2}(A_{S})\) converges geometrically on the abelian finitely generated group \(O_{S}^{*}\) . Moreover its sum is equal to the inner product of \(f_{1}\) and \(f_{2}\) in the Hilbert space \(L^{2}(X_{S})\) .

b) Let \(\alpha = \prod \alpha_{v}\) be a basic character of the additive group \(A_{S}\) and \(F\) the corresponding Fourier transformation. The map \(f\to F(f)\) \(f\in \mathcal{S}(A_{S})\) extends uniquely to a unitary operator in the Hilbert space \(L^{2}(X_{S})\)

Proof. The map \(L:O_{S}^{*}\to \mathbb{R}^{S}\) , given by \(L(u)_{v} = \log |u_{v}|\) has a finite kernel and its range is a lattice in the hyperplane \(H = \{(y_{v}),\sum_{S}y_{v} = 0\}\) . On \(H\) one has \(S u p_{S}y_{v}\geq 1 / 2n\sum |y_{v}|\) , where \(n = c a r d(S)\) . Thus one has the inequality,

\[S u p_{S}|q_{v}|\geq e x p(d(q,1)\qquad \forall q\in O_{S}^{*} \quad (8)\]

for a suitable word metric \(d\) on \(O_{S}^{*}\) .

Let \(K_{n} = \{x\in A_{S};|x_{v}|\leq n,\forall v\in S\}\) and \(k_{n}\) be the characteristic function of \(K_{n}\) . Let \((\lambda_{n})\) be a sequence of rapid decay such that,

\[|f_{i}(x)|\leq \sum \lambda_{n}k_{n}(x)\qquad \forall x\in A_{S}. \quad (9)\]

One has for a suitable constant \(c\)

\[|\langle k_n,U(q^{-1})k_n\rangle |\leq cn^m (Sup_S|q_v|)^{-1}\]

where \(m = Card(S)\)

Using (9) we thus see that \(\langle f_1,U(q)f_2\rangle_A\) decays exponentially on \(O_S^*\) Applying Fubini's theorem yields the equality,

\[\int \Big|\sum_{q\in O_S^*}f(qx)\Big|^2 |x|d^* x = \sum_{O_S^*} \langle f,U(q)f\rangle_A.\]

This proves a). To prove b), one just uses (11) and the equalities \(\langle Ff,Ff\rangle_A =\) \(\langle f,f\rangle_{A}\) and \(F(U(q)f) = U(q^{- 1})F(f)\) .

Now exactly as above for the case of local fields (theorem V.3), we need to use a cutoff. For this we use the orthogonal projection \(P_{\Lambda}\) onto the subspace,

\[P_{\Lambda} = \{\xi \in L^{2}(X_{S});\xi (x) = 0\qquad \forall x,\mid x\mid >\Lambda \} .\]

Thus, \(P_{\Lambda}\) is the multiplication operator by the function \(\rho_{\Lambda}\) , where \(\rho_{\Lambda}(x) = 1\) if \(|x|\leq \Lambda\) , and \(\rho (x) = 0\) for \(|x| > \Lambda\) . This gives an infrared cutoff and to get an ultraviolet cutoff we use \(\widehat{P}_{\Lambda} = FP_{\Lambda}F^{- 1}\) where \(F\) is the Fourier transform (lemma 1) which depends upon the choice of the basic character \(\alpha = \prod \alpha_{v}\) . We let

\[R_{\Lambda} = \widehat{P}_{\Lambda}P_{\Lambda}. \quad (13)\]

The main result of this section is then,

Theorem 4. Let \(A_{S}\) be as above, with basic character \(\alpha = \prod \alpha_{v}\) . Let \(h\in S(C_{S})\) have compact support. Then when \(\Lambda \to \infty\) , one has

\[\mathrm{Trace}(R_{\Lambda}U(h)) = 2h(1)\log^{\prime}\Lambda +\sum_{v\in S}\int_{k_{v}^{*}}^{t}\frac{h(u^{-1})}{|1 - u|} d^{*}u + o(1)\]

where \(2\log^{\prime}\Lambda = \int_{\lambda \in C_{S},|\lambda |\in [\Lambda^{- 1},\Lambda ]}d^{*}\lambda\) , each \(k_{v}^{*}\) is embedded in \(C_{S}\) by the map \(u\to (1,1,\ldots ,u,\ldots ,1)\) and the principal value \(\int^{\prime}\) is uniquely determined by the pairing with the unique distribution on \(k_{v}\) which agrees with \(\frac{du}{|1 - u|}\) for \(u\neq 1\) and whose Fourier transform relative to \(\alpha_{v}\) vanishes at 1.

Proof. We normalize as above the additive Haar measure \(dx\) to be the selfdual one on the abelian group \(A_{S}\) . Let the constant \(\rho >0\) be determined by the equality, (where the fundamental domain \(D\) is as above),

\[\int_{\lambda \in D,1\leq |\lambda |\leq \Lambda}\frac{d\lambda}{|\lambda |}\sim \rho \log \Lambda \qquad \mathrm{when~}\Lambda \to \infty .\]

so that \(d^{*}\lambda = \rho^{- 1}\frac{d\lambda}{|\lambda |}\) .

We let \(f\) be a smooth compactly supported function on \(J_{S}\) such that

\[\sum_{q\in O_{S}^{*}}f(qg) = h(g)\qquad \forall g\in C_{S}. \quad (14)\]

The existence of such an \(f\) follows from the discreteness of \(O_{S}^{*}\) in \(J_{S}\) . We then have the equality \(U(f) = U(h)\) , where

\[U(f) = \int f(\lambda)U(\lambda)d^{*}\lambda , \quad (15)\]

To compute the trace of \(U(h)\) acting on functions on the quotient space \(X_{S}\) , we shall proceed as in the Selberg trace formula ([Se]). Thus for an operator \(T\) , acting on functions on \(A_{S}\) , which commutes with the action of \(O_{S}^{*}\) and is represented by an integral kernel,

\[T(\xi) = \int k(x,y)\xi (y)dy, \quad (16)\]

the trace of its action on \(L^{2}(X_{S})\) is given by,

\[Tr(T) = \sum_{q\in O_{S}^{*}}\int_{D}k(x,qx)dx. \quad (17)\]

where \(D\) is as above a fundamental domain for the action of \(O_{S}^{*}\) on the subset \(J_{S}\) of \(A_{S}\) , whose complement is negligible. Let \(T = U(f)\) . We can write the Schwartz kernel of \(T\) as,

\[k(x,y) = \int f(\lambda^{-1})\delta (y - \lambda x)d^{*}\lambda . \quad (18)\]

by construction one has,

\[k(qx,qy) = k(x,y)\qquad q\in O_{S}^{*}. \quad (19)\]

\[I_{q} = \int_{x\in D}k(qx,y)r_{\Lambda}^{t}(x,y)d y d x\]

where the Schwartz kernel \(r_{\Lambda}^{t}(x,y)\) for the transpose \(R_{\Lambda}^{t}\) is given by,

\[r_{\Lambda}^{t}(x,y) = \rho_{\Lambda}(x)(\widehat{\rho_{\Lambda}})(x - y).\]

To evaluate the above integral, we let \(y = x + a\) and perform a Fourier transform in \(a\) . For the Fourier transform in \(a\) of \(r_{\Lambda}^{t}(x,x + a)\) , one gets,

\[\sigma_{\Lambda}(x,\xi) = \rho_{\Lambda}(x)\rho_{\Lambda}(\xi). \quad (22)\]

For the Fourier transform in \(a\) of \(k(qx,x + a)\) , one gets,

\[\sigma (x,\xi) = \int f(\lambda^{-1})\left(\int \delta (x + a - \lambda q x)\alpha (a\xi)d a\right)d^{*}\lambda .\]

One has,

\[\int \delta (x + a - \lambda q x)\alpha (a\xi)d a = \alpha ((\lambda q - 1)x\xi),\]

thus (23) gives,

\[\sigma (x,\xi) = \rho^{-1}\int_{A_{S}}g_{q}(u)\alpha (ux\xi)d u\]

where,

\[g_{q}(u) = f(q(u + 1)^{-1})|u + 1|^{-1}.\]

Since \(f\) is smooth with compact support on \(A_{S}^{*}\) the function \(g_{q}\) belongs to \(C_{c}^{\infty}(A_{S})\) .

Thus \(\sigma (x,\xi) = \rho^{- 1}\widehat{g}_{q}(x\xi)\) and, using the Parseval formula we get,

\[I_{q} = \int_{x\in D,|x|\leq \Lambda ,|\xi |\leq \Lambda}\sigma (x,\xi)d x d\xi .\]

This gives,

\[I_{q} = \rho^{-1}\int_{x\in D,|x|\leq \Lambda ,|\xi |\leq \Lambda}\widehat{g}_{q}(x\xi)d x d\xi .\]

\[\rho^{-1}\int_{x\in D,\frac{|u|}{\Lambda}\leq |x|\leq \Lambda}\frac{dx}{|x|} = 2\log^{\prime}\Lambda -\log |u|\]

(using the precise definition of \(\log^{\prime}\Lambda\) to handle the boundary terms). Thus we can rewrite (28) as,

\[\mathrm{Trace}(R_{\Lambda}T) = \sum_{q\in O_{S}^{*}}\int_{|u|\leq \Lambda^{2}}\widehat{g}_{q}(u)(2\log^{\prime}\Lambda -\log |u|)du \quad (30)\]

Now \(\log |u| = \sum_{v\in S}\log |u_{v}|\) , and we shall first prove that,

\[\sum_{q\in O_{S}^{*}}\int \widehat{g}_{q}(u)du = h(1), \quad (31)\]

while for any \(v\in S\)

\[\sum_{q\in O_{S}^{*}}\int \widehat{g}_{q}(u)\left(-\log |u_{v}|\right)du = \int_{k_{v}^{*}}^{t}\frac{h(u^{-1})}{|1 - u|} d^{*}u.\]

In fact all the sums in \(q\) will have only finitely many non zero terms. It will then remain to control the error term, namely to show that,

\[\sum_{q\in O_{S}^{*}}\int \widehat{g}_{q}(u)\left(\log |u| - 2\log^{\prime}\Lambda\right)^{+}du = 0(\Lambda^{-N})\]

for any \(N\) , where we used the notation \(x^{+} = 0\) if \(x\leq 0\) and \(x^{+} = x\) if \(x > 0\) . Now recall that,

\[g_{q}(u) = f(q(u + 1)^{-1})|u + 1|^{-1},\]

so that \(\int \widehat{g}_{q}(u)du = g_{q}(0) = f(q)\) . Since \(f\) has compact support in \(A_{S}^{*}\) , the intersection of \(O_{S}^{*}\) with the support of \(f\) is finite and by (14) we get the equality (31).

To prove (32), we consider the natural projection \(p r_{v}\) from \(\prod_{l\in S}k_{l}^{*}\) to \(\prod_{l\neq v}k_{l}^{*}\) . The image \(p r_{v}(O_{S}^{*})\) is still a discrete subgroup of \(\prod_{l\neq v}k_{l}^{*}\) , (since \(k_{v}^{*}\) is cocompact in \(C_{S}\) ), thus there are only finitely many \(q\in O_{S}^{*}\) such that \(k_{v}^{*}\) meets the support of \(f_{q}\) , where \(f_{q}(a) = f(qa)\) for all \(a\) .

For each \(q\in O_{S}^{*}\) one has, as in section V,

\[\int \widehat{g}_{q}(u)\left(-\log |u_{v}|\right)du = \int_{k_{v}^{*}}^{t}\frac{f_{q}(u^{-1})}{|1 - u|} d^{*}u,\]

and from what we have just seen, this vanishes except for finitely many \(q^{\prime}s\) , so that by (14) we get the equality (32). Let us prove (33). Let \(\epsilon_{\Lambda}(u) = (\log |u| - 2\log^{\prime}\Lambda)^{+}\) , and,

\[\delta_{q}(\Lambda) = \int \widehat{g}_{q}(u)\epsilon_{\Lambda}(u)du\]

be the error term. We shall prove,

Lemma 2. For any \(\Lambda\) the series \(\sum_{O_{S}^{*}}|\delta_{q}(\Lambda)|\) converges geometrically on the abelian finitely generated group \(O_{S}^{*}\) . Moreover its sum \(\sigma (\Lambda)\) is \(O(\Lambda^{- N})\) for any \(N\) .

Proof. Let (cf. (8)), \(d\) be a suitable word metric on \(O_{S}^{*}\) such that,

\[S u p_{S}|q_{v}|\geq e x p(d(q,1))\qquad \forall q\in O_{S}^{*} \quad (36)\]

Let \(\xi \in S(A_{S})\) be defined by \(\xi (x) = f(x^{- 1})|x^{- 1}|\) for all \(x\in A_{S}^{*}\) and extended by 0 elsewhere. One has \(g_{q}(x) = \xi (q^{- 1}(1 + x))\) for all \(x\in A_{S}\) , so that \(\widehat{g}_{q}(u) = \int g_{q}(x)\alpha (u x)d x = \alpha (- u)\widehat{\xi} (q u)\) . Now, \(\delta_{q}(\Lambda) = \int \widehat{g}_{q}(u)\epsilon_{\Lambda}(u)d u =\) \(\int \widehat{\xi} (q u)\alpha (- u)\epsilon_{\Lambda}(u)d u = \int \widehat{\xi} (y)\alpha (- q^{- 1}y)\epsilon_{\Lambda}(y)d y\) , since \(\epsilon_{\Lambda}(q u) = \epsilon_{\Lambda}(u)\) for all \(u\) .

Thus we get, using the symbol \(\overline{F}\eta\) for the inverse Fourier transform of \(\eta\) , the equality,

\[\delta_{q}(\Lambda) = \overline{F} (\epsilon_{\Lambda}\widehat{\xi})(q^{-1}). \quad (37)\]

Let \(\alpha \in ]0,1 / 2[\) and consider the norm,

\[\| \eta \| = S u p_{x\in A_{S}}|F(\eta)(x)S u p_{S}|x_{v}|^{\alpha}|. \quad (38)\]

In order to estimate (38), we fix a smooth function \(\psi\) on \(\mathbb{R}\) , equal to 1 in a neighborhood of 0 and with support in \([- 1,1]\) , and introduce the convolution operators,

\[(C_{\alpha ,v}*\eta)(x) = \int_{k_{v}}\psi (|\epsilon |)(\eta (x + \epsilon) - \eta (x))\frac{d\epsilon}{|\epsilon |^{1 + \alpha}}, \quad (39)\]

and the norms,

\[\| \eta \|_{(1,\alpha ,v)} = \| C_{\alpha ,v}*\eta \|_{1}, \quad (40)\]

is the \(L^{1}\) norm.

The Fourier transform on \(k_{v}\) of the distribution \(C_{\alpha ,v}\) behaves like \(|x_{v}|^{\alpha}\) for \(|x_{v}| \to \infty\) . Thus, using the equality \(F(C_{\alpha ,v} * \eta) = F(C_{\alpha ,v}) F(\eta)\) , and the control of the sup norm of \(F(g)\) by the \(L^{1}\) norm of \(g\) , we get an inequality of the form,

\[S u p_{x\in A_{S}}|F(\eta)(x)S u p_{S}|x_{v}|^{\alpha}|\leq c_{\alpha}\sum_{S}\| \eta \|_{(1,\alpha ,v)}.\]

Let us now show that for any \(\eta \in \mathcal{S}(A_{S})\) , and \(\alpha < 1 / 2\) , one has,

\[\| \epsilon_{\Lambda}\eta \|_{(1,\alpha ,v)} = O(\Lambda^{-N}), \quad (42)\]

for any \(N\) .

\[\mathrm{One~has~}|(\epsilon_{\Lambda}(x + \epsilon)\eta (x + \epsilon) - \epsilon_{\Lambda}(x)\eta (x)) - \epsilon_{\Lambda}(x)(\eta (x + \epsilon) - \eta (x))|\leq\] \[|(\epsilon_{\Lambda}(x + \epsilon) - \epsilon_{\Lambda}(x))||\eta (x + \epsilon)|.\]

Moreover using the inequality,

\[|a^{+} - b^{+}|\leq |a - b|, \quad (43)\]

we see that \(|(\epsilon_{\Lambda}(x + \epsilon) - \epsilon_{\Lambda}(x))|\leq |\log |x_{v} + \epsilon | - \log |x_{v}||\) , for \(\epsilon \in k_{v}\) . Let then,

\[c_{\alpha}^{\prime} = \int_{k_{v}}\log |1 + y|\frac{d y}{|y|^{1 + \alpha}}. \quad (44)\]

It is finite for all places \(v \in S\) provided \(\alpha < 1 / 2\) , and one has,

\[\int_{k_{v}}\psi (|\epsilon |)(|\log |x + \epsilon | - \log |x||)\frac{d\epsilon}{|\epsilon|^{1 + \alpha}}\leq c_{\alpha}^{\prime}|x|^{-\alpha}. \quad (45)\]

Thus one obtains the inequality,

\[|C_{\alpha ,v}*\epsilon_{\Lambda}\eta -\epsilon_{\Lambda}(C_{\alpha ,v}*\eta)|(x)\leq c_{\alpha}^{\prime}|x_{v}|^{-\alpha}Sup_{\epsilon \in k_{v},|\epsilon |\leq 1}|\eta (x + \epsilon)|. \quad (46)\]

Since the function \(|x_{v}|^{-\alpha}\) is locally integrable, for \(\alpha < 1\) , one has for \(\eta \in \mathcal{S}(A_{S})\) , and any \(N\) ,

\[\int_{X_{\Lambda}}|x_{v}|^{-\alpha}Sup_{\epsilon \in k_{v},|\epsilon |\leq 1}|\eta (x + \epsilon)|dx = O(\Lambda^{-N}), \quad (47)\]

where \(X_{\Lambda} = \{y + \epsilon ; |y| \geq \Lambda , \epsilon \in k_{v}, |\epsilon | \leq 1\}\) .

Moreover one has for any \(N\) ,

\[\| \epsilon_{\Lambda}(C_{\alpha ,v}*\eta)\|_{1} = O(\Lambda^{-N}).\]

Thus, using (46), we obtain the inequality (42).

Taking \(\eta = \widehat{\xi}\) and using (41), we thus get numbers \(\delta_{\Lambda}\) , such that \(\delta_{\Lambda} = O(\Lambda^{- N})\) for all \(N\) and that,

\[|\overline{F} (\epsilon_{\Lambda}\widehat{\xi})S u p_{S}|x_{v}|^{\alpha}||\leq \delta_{\Lambda}\qquad \forall x\in A_{S}\forall \Lambda .\]

Taking \(x = q\in O_{S}^{*}\) , and using (36) and (37), we thus get,

\[|\delta_{q}(\Lambda)|\leq \delta_{\Lambda}exp(-d(q,1))\qquad \forall q\in O_{S}^{*},\]

which is the desired inequality.

■

---

## VIII The trace formula in the global case, and elimination of \(\delta\) .

The main difficulty created by the parameter \(\delta\) in Theorem 1 is that the formal trace computation of section VI is independent of \(\delta\) , and thus cannot give in general the expected value of the trace of theorem 1, since in the latter each critical zero \(\rho\) is counted with a multiplicity equal to the largest integer \(n< \frac{1 + \delta}{2}\) , \(n\leq\) multiplicity of \(\rho\) as a zero of \(L\) . In particular for \(L\) functions with multiple zeros, the \(\delta\) - dependence of the spectral side is nontrivial. It is also clear that the function space \(L_{\delta}^{2}(X)\) artificially eliminates the non- critical zeros by the introduction of the \(\delta\) .

As we shall see, all these problems are eliminated by the cutoff. The latter will be performed directly on the Hilbert space \(L^{2}(X)\) so that the only value of \(\delta\) that we shall use is \(\delta = 0\) . All zeros will play a role in the spectral side of the trace formula, but while the critical zeros will appear per- se, the non critical ones will appear as resonances and enter in the trace formula through their harmonic potential with respect to the critical line. Thus the spectral side is entirely canonical and independent of \(\delta\) , and by proving positivity of the Weil distribution, we shall show that its equality with the geometric side, i.e. the global analogue of Theorem 4, is equivalent to the Riemann Hypothesis for all \(L\) - functions with Grossencharakter.

The Abelian group \(A\) of Adeles of \(k\) is its own Pontrjagin dual by means of the pairing

\[\langle a,b\rangle = \alpha (ab) \quad (1)\]

where \(\alpha :A\to U(1)\) is a nontrivial character which vanishes on \(k\subset A\) .Note that such a character is not canonical, but that any two such characters \(\alpha\) and \(\alpha^{\prime}\) are related by \(k^{*}\)

\[\alpha^{\prime}(a) = \alpha (qa)\quad \forall a\in A. \quad (2)\]

It follows that the corresponding Fourier transformations on \(A\) are related by

\[\hat{f}^{\prime} = \hat{f}_{q}. \quad (3)\]

This is yet another reason why it is natural to mod out by functions of the form \(f - f_{q}\) , i.e. to consider the quotient space \(X\) .

We fix the additive character \(\alpha\) as above, \(\alpha = \prod \alpha_{v}\) and let \(d\) be a differential idele,

\[\alpha (x) = \alpha_{0}(d x)\quad \forall x\in A, \quad (4)\]

where \(\alpha_{0} = \prod \alpha_{0,v}\) is the product of the local normalized additive characters (cf [W1]). We let \(S_{0}\) be the finite set of places where \(\alpha_{v}\) is ramified.

We shall first concentrate on the case of positive characteristic, i.e. of function fields, both because it is technically simpler and also because it allows to keep track of the geometric significance of the construction (cf. section II).

In order to understand how to perform in the global case, the cutoff \(R_{\Lambda} = \widehat{P}_{\Lambda}P_{\Lambda}\) of section VII, we shall first analyze the relative position of the pair of projections \(\widehat{P}_{\Lambda}\) , \(P_{\Lambda}\) when \(\Lambda \to \infty\) . Thus, we let \(S\supset S_{0}\) be a finite set of places of \(k\) , large enough so that \(mod(C_{S}) = mod(C_{k}) = q^{Z}\) and that for any fundamental domain \(D\) for the action of \(O_{S}^{*}\) on \(J_{S}\) , the product \(D\times \prod R_{v}^{*}\) is a fundamental domain for the action of \(k^{*}\) on \(J_{k}\) .

Both \(\widehat{P}_{\Lambda}\) and \(P_{\Lambda}\) commute with the decomposition of \(L^{2}(X_{S})\) as the direct sum of the subspaces, indexed by characters \(\chi_{0}\) of \(C_{S,1}\) ,

\[L_{\chi_{0}}^{2} = \{\xi \in L^{2}(X_{S});\xi (a^{-1}x) = \chi_{0}(a)\xi (x),\forall x\in X_{S},a\in C_{S,1}\} \quad (5)\]

which corresponds to the projections \(P_{\chi_{0}} = \int \overline{\chi_{0}} (a)U(a)d_{1}a\) , where \(d_{1}a\) is the Haar measure of total mass 1 on \(C_{S,1}\) .

Lemma 1. Let \(\chi_{0}\) be a character of \(C_{S,1}\) , then for \(\Lambda\) large enough \(\widehat{P}_{\Lambda}\) and \(P_{\Lambda}\) commute on the Hilbert space \(L_{\chi_{0}}^{2}\) .

Proof. Let \(\mathcal{U}_{S}\) be the image in \(C_{S}\) of the open subgroup \(\prod R_{v}^{*}\) . It is a subgroup of finite index \(l\) in \(C_{S,1}\) . Let us fix a character \(\chi\) of \(\mathcal{U}_{S}\) and consider the finite direct sum of the Hilbert spaces \(L_{\chi_{0}}^{2}\) where \(\chi_{0}\) varies among the characters of \(C_{S,1}\) whose restriction to \(\mathcal{U}_{S}\) is equal to \(\chi\) ,

\[L^{2}(X_{S})_{\chi} = \{\xi \in L^{2}(X_{S});\xi (a^{-1}x) = \chi (a)\xi (x),\forall x\in X_{S},a\in \mathcal{U}_{S}\} \quad (6)\]

The corresponding orthogonal projection is \(U(h_{\chi})\) , where \(h_{\chi}\in \mathcal{S}(C_{S})\) is such that,

\[S u p p(h_{\chi}) = \mathcal{U}_{S}\qquad h_{\chi}(x) = \lambda \overline{{\chi}} (x)\qquad \forall x\in \mathcal{U}_{S} \quad (7)\]

and the constant \(\lambda = l / \log (q)\) corresponds to our standard normalization of the Haar measure on \(C_{S}\) . Let as in section VII, \(f\in \mathcal{S}(J_{S})\) with support \(\prod R_{v}^{*}\) be such that \(U(f) = U(h)\) and let \(\xi \in \mathcal{S}(A_{S})\) be defined by \(\xi (x) =\) \(f(x^{- 1})|x^{- 1}|\) for all \(x\in A_{S}^{*}\) and extended by 0 elsewhere.

Since \(\xi\) is locally constant, its Fourier transform has compact support and the equality (37) of section VII shows that for \(\Lambda\) large enough one has the equality,

\[\mathrm{Trace}(\widehat{P}_{\Lambda}P_{\Lambda}U(h_{\chi})) = 2h_{\chi}(1)\log^{\prime}\Lambda +\sum_{v\in S}\int_{k_{v}^{*}}^{l}\frac{h_{\chi}(u^{-1})}{|1 - u|} d^{*}u \quad (8)\]

With \(\Lambda = q^{N}\) , one has \(2\log^{\prime}\Lambda = (2N + 1)\log (q)\) so that,

\[2h_{\chi}(1)\log^{\prime}\Lambda = (2N + 1)l \quad (9)\]

The character \(\chi\) of \(\prod R_{v}^{*}\) is a product, \(\chi = \prod \chi_{v}\) and if one uses the standard additive character \(\alpha_{0}\) to take the principal value one has, (cf. [W1] Appendix IV),

\[\int_{R_{*_{v}}}^{l}\frac{\chi_{v}(u)}{|1 - u|} d^{*}u = -f_{v}\log (q_{v}) \quad (10)\]

where \(f_{v}\) is the order of ramification of \(\chi_{v}\) . We thus get,

\[\int_{k_{v}^{*}}^{l}\frac{h_{\chi}(u^{-1})}{|1 - u|} d^{*}u = -f_{v}deg(v)l + l\frac{\log(|d_{v}|)}{\log(q)} \quad (11)\]

where \(q_{v} = q^{deg(v)}\) , and since we use the additive character \(\alpha_{v}\) , we had to take into account the shift \(\log (|d_{v}|)h_{\chi}(1)\) in the principal value.

Now one has \(|d| = \prod |d_{v}| = q^{2 - 2g}\) , where \(g\) is the genus of the curve. Thus we get,

\[\mathrm{Trace}(\widehat{P}_{\Lambda}P_{\Lambda}U(h_{\chi})) = (2N + 1)l - f l + (2 - 2g)l \quad (12)\]

where \(f = \sum_{S}f_{v}deg(v)\) is the order of ramification of \(\chi\) , i.e. the degree of its conductor.

Let \(B_{\Lambda} = Im(P_{\Lambda})\cap Im(\widehat{P}_{\Lambda})\) be the intersection of the ranges of the projections \(P_{\Lambda}\) and \(\widehat{P}_{\Lambda}\) , and \(B_{\Lambda}^{\chi}\) be its intersection with \(L^{2}(X_{S})_{\chi}\) . We shall exhibit for each character \(\chi\) of \(\mathcal{U}_{S}\) a vector \(\eta_{\chi}\in L^{2}(X_{S})_{\chi}\) such that,

\[U(g)(\eta_{\chi})\in B_{\Lambda}\qquad \forall g\in C_{S},|g|\leq \Lambda ,|g^{-1}|\leq q^{2 - 2g - f}\Lambda , \quad (13)\]

while the vectors \(U(g)(\eta_{\chi})\) are linearly independent for \(g\in D_{S}\) , where \(D_{S}\) is the quotient of \(C_{S}\) by the open subgroup \(\mathcal{U}_{S}\) .

With \(\Lambda = q^{N}\) as above, the number of elements \(g\) of \(D_{S}\) such that \(|g|\leq \Lambda ,|g^{- 1}|\leq q^{2 - 2g - f}\Lambda\) is precisely equal to \((2N + 1)l - f l + (2 - 2g)l\) , which allows to conclude that the projections \(\widehat{P}_{\Lambda}\) and \(P_{\Lambda}\) commute in \(L^{2}(X_{S})_{\chi}\) and that the subspace \(B_{\Lambda}^{\chi}\) is the linear span of the \(U(g)(\eta_{\chi})\) .

Let us now construct the vectors \(\eta_{\chi}\in L^{2}(X_{S})_{\chi}\) . With the notations of [W1] Proposition VII.13, we let,

\[\eta_{\chi} = \prod_{S}\phi_{v} \quad (14)\]

be the standard function associated to \(\chi = \prod \chi_{v}\) so that for unramified \(v\) , \(\phi_{v}\) is the characteristic function of \(R_{v}\) , while for ramified \(v\) it vanishes outside \(R_{v}^{*}\) and agrees with \(\overline{\chi}_{v}\) on \(R_{v}^{*}\) . By construction the support of \(\eta_{\chi}\) is contained in \(R = \prod R_{v}\) , thus one has \(U(g)(\eta_{\chi})\in Im(P_{\Lambda})\) if \(|g|\leq \Lambda\) . Similarly by [W1] Proposition VII.13, we get that \(U(g)(\eta_{\chi})\in Im(\widehat{P}_{\Lambda})\) as soon as \(|g^{- 1}|\leq q^{2 - 2g - f}\Lambda\) . This shows that \(\eta_{\chi}\) satisfies (13) and it remains to show that the vectors \(U(g)(\eta_{\chi})\) are linearly independent for \(g\in D_{S}\) .

Let us start with a non trivial relation of the form,

\[\| \sum \lambda_{g}U(g)(\eta_{\chi})\| = 0 \quad (15)\]

where the norm is taken in \(L^{2}(X_{S})\) , (cf. VII. 5). Let then \(\xi_{\chi} = \prod_{S}\phi_{v}\otimes 1_{R}\) where \(R = \prod_{v\notin S}R_{v}\) . Let us assume first that \(\chi \neq 1\) , then \(\xi_{\chi}\) gives an element

\(\begin{array}{r}{L_{\delta}^{2}(X)_{0}} \end{array}\) which is cyclic for the representation \(U\) of \(C_{k}\) in the direct sum of the subspaces \(L_{\delta ,\chi_{0}}^{2}(X)_{0}\) where \(\chi_{0}\) varies among the characters of \(C_{k,1}\) whose restriction to \(\mathcal{U}\) is equal to \(\chi\) .

Now (15) implies that in \(L_{\delta}^{2}(X)_{0}\) one has \(\begin{array}{r}{\sum \lambda_{g}U(g)(\xi_{\chi}) = 0} \end{array}\) . By the cyclicity of \(\xi_{\chi}\) one then gets \(\begin{array}{r}{\sum \lambda_{g}U(g) = 0} \end{array}\) on any \(L_{\delta ,\chi_{0}}^{2}(X)_{0}\) which gives a contradiction (cf. Appendix 1, Lemma 3).

The proof for \(\chi = 1\) is similar but requires more care since \(1_{R}\notin S_{0}(A)\) .

We can thus rewrite Theorem 4 in the case of positive characteristic as,

Corollary 2. Let \(Q_{\Lambda}\) be the orthogonal projection on the subspace of \(L^{2}(X_{S})\) spanned by the \(f\in S(A_{S})\) which vanish as well as their Fourier transform for \(|x| > \Lambda\) . Let \(h\in S(C_{S})\) have compact support. Then when \(\Lambda \to \infty\) , one has

\[\mathrm{Trace}\left(Q_{\Lambda}U(h)\right) = 2h(1)\log^{\prime}\Lambda +\sum_{v\in S}\int_{k_{v}^{*}}^{t}\frac{h(u^{-1})}{|1 - u|} d^{*}u + o(1)\]

where \(2\log^{\prime}\Lambda = \int_{\lambda \in C_{S},|\lambda |\in [\Lambda^{- 1},\Lambda ]}d^{*}\lambda\) , and the other notations are as in Theorem VII.4.

In fact the proof of lemma 1 shows that the subspaces \(B_{\Lambda}\) stabilize very quickly, so that the natural map \(\xi \to \xi \otimes 1_{R}\) from \(L^{2}(X_{S})\) to \(L^{2}(X_{S}^{\prime})\) for \(S\subset S^{\prime}\) maps \(B_{\Lambda}^{S}\) onto \(B_{\Lambda}^{S^{\prime}}\) .

We thus get from corollary 2 an \(S\) - independent global formulation of the cutoff and of the trace formula. We let \(L^{2}(X)\) be the Hilbert space \(L_{\delta}^{2}(X)\) of section III for the trivial value \(\delta = 0\) which of course eliminates the unpleasant term from the inner product, and we let \(Q_{\Lambda}\) be the orthogonal projection on the subspace \(B_{\Lambda}\) of \(L^{2}(X)\) spanned by the \(f\in S(A)\) which vanish as well as their Fourier transform for \(|x| > \Lambda\) . As we mentionned earlier, the proof of lemma 1 shows that for \(S\) and \(\Lambda\) large enough (and fixed character \(\chi\) ), the natural map \(\xi \to \xi \otimes 1_{R}\) from \(L^{2}(X_{S})_{\chi}\) to \(L^{2}(X)_{\chi}\) maps \(B_{\Lambda}^{S}\) onto \(B_{\Lambda}\) .

It is thus natural to expect that the following global analogue of the trace formula of corollary 2 actually holds, i.e. that when \(\Lambda \to \infty\) , one has,

\[\mathrm{Trace}\left(Q_{\Lambda}U(h)\right) = 2h(1)\log^{\prime}\Lambda +\sum_{v}\int_{k_{v}^{*}}^{t}\frac{h(u^{-1})}{|1 - u|} d^{*}u + o(1) \quad (16)\]

where \(2\log^{\prime}\Lambda = \int_{\lambda \in C_{k},|\lambda |\in [\Lambda^{- 1},\Lambda ]}d^{*}\lambda\) , and the other notations are as in Theorem VII.4.

We can prove directly that (16) holds when \(h\) is supported by \(C_{k,1}\) but are not able to prove (16) directly for arbitrary \(h\) (even though the right hand side of the formula only contains finitely many nonzero terms since \(h \in \mathcal{S}(C_k)\) has compact support). What we shall show however is that the trace formula (16) implies the positivity of the Weil distribution, and hence the validity of RH for \(k\) . Remember that we are still in positive characteristic where RH is actually a theorem of A.Weil. It will thus be important to check the actual equivalence between the validity of RH and the formula (16). This is achieved by,

Theorem 5. Let \(k\) be a global field of positive characteristic and \(Q_{\Lambda}\) be the orthogonal projection on the subspace of \(L^{2}(X)\) spanned by the \(f \in \mathcal{S}(A)\) such that \(f(x)\) and \(\hat{f} (x)\) vanish for \(|x| > \Lambda\) . Let \(h \in \mathcal{S}(C_k)\) have compact support. Then the following conditions are equivalent,

a) When \(\Lambda \to \infty\) , one has

\[\mathrm{Trace}\left(Q_{\Lambda}U(h)\right) = 2h(1)\log^{\prime}\Lambda +\sum_{v}\int_{k_{v}^{v}}^{h}\frac{h(u^{-1})}{|1 - u|} d^{v}u + o(1)\]

b) All \(L\) functions with Grössencharakter on \(k\) satisfy the Riemann Hypothesis.

Proof. To prove that a) implies b), we shall prove (assuming a)) the positivity of the Weil distribution (cf. Appendix 2),

\[\Delta = \log |d^{-1}|\delta_{1} + D - \sum_{v}D_{v}. \quad (17)\]

First, by theorem III.1 applied for \(\delta = 0\) , the map \(E\) ,

\[E(f)\left(g\right) = |g|^{1 / 2}\sum_{q\in k^{*}}f(qg)\qquad \forall g\in C_{k}, \quad (18)\]

defines a surjective isometry from \(L^{2}(X)_{0}\) to \(L^{2}(C_{k})\) such that,

\[E U(a) = |a|^{1 / 2}V(a)E, \quad (19)\]

where the left regular representation \(V\) of \(C_k\) on \(L^2 (C_k)\) is given by,

\[(V(a)\xi)(g) = \xi (a^{-1}g)\qquad \forall g,a\in C_k. \quad (20)\]

\[S_{\Lambda} = \{\xi \in L^{2}(C_{k}); \xi (g) = 0, \forall g, |g| \notin [\Lambda^{-1}, \Lambda ]\} .\]

We shall denote by the same letter the corresponding orthogonal projection.

Let \(B_{\Lambda ,0}\) be the subspace of \(L^{2}(X)_{0}\) spanned by the \(f\in S(A)_{0}\) such that \(f(x)\) and \(\widehat{f} (x)\) vanish for \(|x| > \Lambda\) and \(Q_{\Lambda ,0}\) be the corresponding orthogonal projection. Let \(f\in S(A)_{0}\) be such that \(f(x)\) and \(\widehat{f} (x)\) vanish for \(|x| > \Lambda\) then \(E(f)\) (g) vanishes for \(|g| > \Lambda\) , and the equality (Appendix 1),

\[E(f)(g) = E(\widehat{f})\left(\frac{1}{g}\right)\qquad f\in \mathcal{S}(A)_{0},\]

shows that \(E(f)(g)\) vanishes for \(|g|< \Lambda^{- 1}\) .

This shows that \(E(B_{\Lambda ,0})\subset S_{\Lambda}\) , so that if we let \(Q_{\Lambda ,0}^{\prime} = E Q_{\Lambda ,0}E^{- 1}\) , we get the inequality,

\[Q_{\Lambda ,0}^{\prime}\leq S_{\Lambda}\]

and for any \(\Lambda\) the following distribution on \(C_{k}\) is of positive type,

\[\Delta_{\Lambda}(f) = \mathrm{Trace}\left((S_{\Lambda} - Q_{\Lambda ,0}^{\prime})V(f)\right),\]

i.e. one has,

\[\Delta_{\Lambda}(f*f^{*})\geq 0,\]

where \(f^{*}(g) = \overline{f} (g^{- 1})\) for all \(g\in C_{k}\) .

Let then \(f(g) = |g|^{- 1 / 2}h(g^{- 1})\) , so that by (19) one has \(E U(h) = V(\tilde{f})E\) where \(\tilde{f} (g) = f(g^{- 1})\) for all \(g\in C_{k}\) . By lemma 3 of Appendix 2 one has,

\[\sum_{v}D_{v}(f) - \log |d^{-1}| = \sum_{v}\int_{k_{v}^{*}}^{t}\frac{h(u^{-1})}{|1 - u|} d^{*}u.\]

One has Trace \((S_{\Lambda}V(f)) = 2f(1)\log^{\prime}\Lambda\) , thus using a) we see that the limit of \(\Delta_{\Lambda}\) when \(\Lambda \rightarrow \infty\) is the Weil distribution \(\Delta\) (cf.(17)). The term \(D\) in the latter comes from the nuance between the subspaces \(B_{\Lambda}\) and \(B_{\Lambda ,0}\) . This shows using (24), that the distribution \(\Delta\) is of positive type so that b) holds (cf. [W3]).

Let us now show that b) implies a). We shall compute from the zeros of \(L\) - functions and independently of any hypothesis the limit of the distributions \(\Delta_{\Lambda}\) when \(\Lambda \to \infty\) .

We choose (non canonically) an isomorphism

\[C_{k}\simeq C_{k,1}\times N.\]

where \(N = \mathrm{range} | | \subset \mathbb{R}_{+}^{*}\) , \(N \simeq \mathbb{Z}\) is the subgroup \(q^{\mathbb{Z}} \subset \mathbb{R}_{+}^{*}\) .

For \(\rho \in \mathbb{C}\) we let \(d\mu_{\rho}(z)\) be the harmonic measure of \(\rho\) with respect to the line \(i \mathbb{R} \subset \mathbb{C}\) . It is a probability measure on the line \(i \mathbb{R}\) and coincides with the Dirac mass at \(\rho\) when \(\rho\) is on the line.

The implication b) \(\Rightarrow\) a) follows immediately from the explicit formulas (Appendix 2) and the following lemma,

Lemma 3. The limit of the distributions \(\Delta_{\Lambda}\) when \(\Lambda \to \infty\) is given by,

\[\Delta_{\infty}(f) = \sum_{\substack{L\left(\widetilde{\chi},\frac{1}{2} +\rho\right) = 0\\ \rho \in B / N^{\perp}}}N(\widetilde{\chi},\frac{1}{2} +\rho)\int_{z\in i\mathbb{R}}\widehat{f} (\widetilde{\chi},z)d\mu_{\rho}(z)\]

where \(B\) is the open strip \(B = \{\rho \in \mathbb{C};R e(\rho)\in \frac{- 1}{2},\frac{1}{2} [\},N(\widetilde{\chi},\frac{1}{2} +\rho)\) is the multiplicity of the zero, \(d\mu_{\rho}(z)\) is the harmonic measure of \(\rho\) with respect to the line \(i\mathbb{R}\subset \mathbb{C}\) , and the Fourier transform \(\widehat{f}\) of \(f\) is defined by,

\[\widehat{f} (\widetilde{\chi},\rho) = \int_{C_k}f(u)\widetilde{\chi} (u)|u|^{\rho}d^* u.\]

Proof. Let \(\Lambda = q^{N}\) . The proof of Lemma 1 gives the lower bound \((2N + 1) - f + (2 - 2g)\) for the dimension of \(B_{\Lambda ,\chi}\) in terms of the order of ramification \(f\) of the character \(\chi\) of \(C_{k,1}\) , where we assume first that \(\chi \neq 1\) . We have seen moreover that \(E(B_{\Lambda ,\chi}) \subset S_{\Lambda ,\chi}\) while the dimension of \(S_{\Lambda ,\chi}\) is \(2N + 1\) .

Now by Lemma 3 of Appendix 1, every element \(\xi \in E(B_{\Lambda ,\chi})\) satisfies the conditions,

\[\int \xi (x)\chi (x)|x|^{\rho}d^{*}x = 0\qquad \forall \rho \in B / N^{\perp},L\left(\chi ,\frac{1}{2} +\rho\right) = 0. \quad (28)\]

This gives \(2g - 2 + f\) linearly independent conditions (for \(N\) large enough), using [W1] Theorem VII.6, and shows that they actually characterize the subspace \(E(B_{\Lambda ,\chi})\) of \(S_{\Lambda ,\chi}\) .

This reduces the proof of the lemma to the following simple computation: One lets \(F\) be a finite subset (possibly with multiplicity) of \(\mathbb{C}^{*}\) and \(E_{N}\) the subspace of \(S_{N} = \{\xi \in l^{2}(\mathbb{Z}); \xi (n) = 0 \forall n > N\}\) defined by the conditions \(\sum \xi (n)z^{n} = 0 \forall z \in F\) . One then has to compute the limit when \(N \to \infty\) of Trace \(((S_{N} - E_{N})V(f))\) where \(V\) is the regular representation of \(\mathbb{Z}\) (so that \(V(f) = \sum f_{k}V^{k}\) where \(V\) is the shift, \(V(\xi)_{n} = \xi_{n - 1}\) ). One then checks that the unit vectors \(\eta_{z} \in S_{N}\) , \(z \in F\) , \(\eta_{z}(n) = \overline{z}^{n}(|z^{2N + 1}| - |z^{- (2N + 1)}|)^{-\frac{1}{2}}(|z| - |z^{- 1}|)^{\frac{1}{2}} \forall n \in [- N, N]\) , are asymptotically orthogonal and span \((S_{N} - E_{N})\) (when \(F\) has multiplicity one has to be more careful). The conclusion then follows from,

\[\mathrm{Lim}_{N\to \infty}\langle V(f)\eta_z,\eta_z\rangle = \int_{|u| = 1}P_z(u)\widehat{f} (u)du, \quad (29)\]

where \(P_{z}(u)\) is the Poisson kernel, and \(\hat{f}\) the Fourier transform of \(f\) .

One should compare this lemma with Corollary 2 of Theorem III.1. In the latter only the critical zeros were coming into play and with a multiplicity controlled by \(\delta\) . In the above lemma, all zeros do appear and with their full multiplicity, but while the critical zeros appear per- se, the non- critical ones play the role of resonances as in the Fermi theory.

Let us now explain how the above results extend to number fields \(k\) . We first need to analyze, as above, the relative position of the projections \(P_{\Lambda}\) and \(\hat{P}_{\Lambda}\) . Let us first remind the reader of the well known geometry of pairs of projectors. Recall that a pair of orthogonal projections \(P_{i}\) in Hilbert space is the same thing as a unitary representation of the dihedral group \(\Gamma = \mathbb{Z} / 2 * \mathbb{Z} / 2\) . To the generators \(U_{i}\) of \(\Gamma\) correspond the operators \(2P_{i} - 1\) . The group \(\Gamma\) is the semidirect product of the subgroup generated by \(U = U_{1}U_{2}\) by the group \(\mathbb{Z} / 2\) , acting by \(U \mapsto U^{- 1}\) . Its irreducible unitary representations are parametrized by an angle \(\theta \in [0, \frac{\pi}{2} ]\) , the corresponding orthogonal projections \(P_{i}\) being associated to the one dimensional subspaces \(y = 0\) and \(y = x tg(\theta)\) in the Euclidean \(x, y\) plane. In particular these representations are at most two dimensional. A general unitary representation is characterized by the operator \(\Theta\) whose value is the above angle \(\theta\) in the irreducible case. It is uniquely defined by the equality,

\[\mathrm{Sim}(\Theta) = |P_1 - P_2|, \quad (30)\]

and commutes with \(P_{i}\) .

The first obvious difficulty is that when \(v\) is an Archimedian place there exists no non- zero function on \(k_{v}\) which vanishes as well as its Fourier transform for \(|x| > \Lambda\) . This would be a difficult obstacle were it not for the work of Landau, Pollak and Slepian ([LPS]) in the early sixties, motivated by problems of electrical engineering, which allows to overcome it by showing that though the projections \(P_{\Lambda}\) and \(\hat{P}_{\Lambda}\) do not commute exactly even for large \(\Lambda\) , their angle is sufficiently well behaved so that the subspace \(B_{\Lambda}\) makes good sense.

For simplicity we shall take \(k = \mathbb{Q}\) , so that the only infinite place is real. Let \(P_{\Lambda}\) be the orthogonal projection onto the subspace,

\[P_{\Lambda} = \{\xi \in L^{2}(\mathbb{R});\xi (x) = 0,\forall x,|x| > \Lambda \} .\]

and \(\hat{P}_{\Lambda} = FP_{\Lambda}F^{- 1}\) where \(F\) is the Fourier transform associated to the basic character \(\alpha (x) = e^{- 2\pi ix}\) . What the above authors have done is to analyze the relative position of the projections \(P_{\Lambda}\) , \(\hat{P}_{\Lambda}\) for \(\Lambda \to \infty\) in order to account for the obvious existence of signals (a recorded music piece for instance) which for all practical purposes have finite support both in the time variable and the dual frequency variable.

The key observation of ([LPS]) is that the following second order differential operator on \(\mathbb{R}\) actually commutes with the projections \(P_{\Lambda}\) , \(\hat{P}_{\Lambda}\) ,

\[H_{\Lambda}\psi (x) = -\partial ((\Lambda^{2} - x^{2})\partial)\psi (x) + (2\pi \Lambda x)^{2}\psi (x),\]

where \(\partial\) is ordinary differentiation in one variable. Exactly as the generator \(x\partial\) of scaling commutes with the orthogonal projection on the space of functions with positive support, the operator \(\partial ((\Lambda^{2} - x^{2})\partial)\) commutes with \(P_{\Lambda}\) . Moreover \(H_{\Lambda}\) commutes with Fourier transform \(F\) , and the commutativity of \(H_{\Lambda}\) with \(\hat{P}_{\Lambda}\) thus follows.

If one sticks to functions with support in \([- \Lambda , \Lambda ]\) , the operator \(H_{\Lambda}\) has discrete simple spectrum, and was studied long before the work of [LPS]. It appears from the factorization of the Helmholtz equation \(\Delta \psi + k^{2}\psi = 0\) in one of the few separable coordinate systems in Euclidean 3- space, called the prolate spheroidal coordinates. Its eigenvalues \(\chi_{n}(\Lambda), n \geq 0\) are simple, positive and of the order of \(n^{2}\) for \(n \to \infty\) . The corresponding eigenfunctions \(\psi_{n}\) are called the prolate spheroidal wave functions and since \(P_{\Lambda} \hat{P}_{\Lambda} P_{\Lambda}\) commutes with \(H_{\Lambda}\) , they are the eigenfunctions of \(P_{\Lambda} \hat{P}_{\Lambda} P_{\Lambda}\) . A lot is known about them, in particular one can take them to be real valued, and they are even for \(n\) even

and odd for \(n\) odd. The key result of [LPS] is that the corresponding eigenvalues \(\lambda_{n}\) of the operator \(P_{\Lambda}\widehat{P}_{\Lambda}P_{\Lambda}\) are decreasing very slowly from \(\lambda_{0}\simeq 1\) until the value \(n\simeq 4\Lambda^{2}\) of the index \(n\) , they then decrease from \(\simeq 1\) to \(\simeq 0\) in an interval of length \(\simeq \log (\Lambda)\) and then stay close to 0. Of course this gives the eigenvalues of \(\Theta\) , it dictates the analogue of the subspace \(B_{\Lambda}\) of lemma 1, as the linear span of the \(\psi_{n}\) , \(n\leq 4\Lambda^{2}\) , and it gives the justification of the semi- classical counting of the number of quantum mechanical states which are localized in the interval \([- \Lambda ,\Lambda ]\) as well as their Fourier transform as the area of the corresponding square in phase space.

We now know what is the subspace \(B_{\Lambda}\) for the single place \(\infty\) , and to obtain it for an arbitrary set of places (containing the infinite one), we just use the same rule as in the case of function fields, i.e. we consider the map,

\[\psi \mapsto \psi \otimes 1_{R}, \quad (33)\]

which suffices when we deal with the Riemann zeta function. Note also that in that case we restrict ourselves to even functions on \(\mathbb{R}\) . This gives the analogue of Lemma 1, Theorem 5, and Lemma 3.

To end this section we shall come back to our original motivation of section I and show how the formula for the number of zeros

\[N(E)\sim (E / 2\pi)(\log (E / 2\pi) - 1) + 7 / 8 + o(1) + N_{osc}(E)\]

appears from our spectral interpretation.

Let us first do a semiclassical computation for the number of quantum mechanical states in one degree of freedom which fulfill the following conditions,

\[|q|\leq \Lambda ,|p|\leq \Lambda ,|H|\leq E, \quad (35)\]

where \(H = qp\) is the Hamiltonian which generates the group of scaling transformations,

\[(U(\lambda)\xi)(x) = \xi (\lambda^{-1}x)\qquad \lambda \in \mathbb{R}_{+}^{*},x\in \mathbb{R},\xi \in L^{2}(\mathbb{R}), \quad (36)\]

as in our general framework.

To comply with our analysis of section III, we have to restrict ourselves to even functions so that we exclude the region \(pq\leq 0\) of the semiclassical \((p,q)\) plane.

\[D_{+} = \{(p,q)\in \mathbb{R}_{+}\times \mathbb{R}_{+},p\leq \Lambda ,q\leq \Lambda ,pq\leq E\} ,\]

Let us compute the area of \(D_{+}\) for the canonical symplectic form,

\[\omega = \frac{1}{2\pi} dp\wedge dq.\]

By construction \(D_{+}\) is the union of a rectangle with sides \(E / \Lambda\) , \(\Lambda\) with the subgraph, from \(q = E / \Lambda\) to \(q = \Lambda\) , of the hyperbola \(pq = E\) . Thus,

\[\int_{D_{+}}\omega = \frac{1}{2\pi} E / \Lambda \times \Lambda +\frac{1}{2\pi}\int_{E / \Lambda}^{\Lambda}\frac{E dq}{q} = \frac{E}{2\pi} +\frac{2E}{2\pi}\log \Lambda -\frac{E}{2\pi}\log E.\]

Now the above computation corresponds to the standard normalization of the Fourier transform with basic character of \(\mathbb{R}\) given by

\[\alpha (x) = \exp (ix).\]

But we need to comply with the natural normalization at the infinite place,

\[\alpha_0(x) = \exp (-2\pi ix).\]

We thus need to perform the transformation,

\[P = p / 2\pi ,Q = q.\]

The symplectic form is now \(dP\wedge dQ\) and the domain,

\[D^{\prime} = \{(P,Q);|Q|\leq \Lambda ,|P|\leq \Lambda ,|PQ|\leq E / 2\pi \} .\]

The computation is similar and yields the following result,

\[\int_{D_{+}^{\prime}}\omega = \frac{2E}{2\pi}\log \Lambda -\frac{E}{2\pi}\left(\log \frac{E}{2\pi} -1\right).\]

In this formula we thus see the overall term \(\langle N(E)\rangle\) which appears with a minus sign which shows that the number of quantum mechanical states corresponding to \(D^{\prime}\) is less than \(\frac{4E}{2\pi}\log \Lambda\) by the first approximation to the number of zeros of zeta whose imaginary part is less than \(E\) in absolute value (one just multiplies by 2 the equality (43) since \(D^{\prime} = D_{+}^{\prime}\cup (- D_{+}^{\prime})\) .

\(\frac{1}{2\pi}(2E)(2\log \Lambda)\) is the number of quantum states in the Hilbert space \(L^{2}(\mathbb{R}_{+}^{*},d^{*}x)\) which are localized in \(\mathbb{R}_{+}^{*}\) between \(\Lambda^{- 1}\) and \(\Lambda\) and are localized in the dual group \(\mathbb{R}\) (for the pairing \(\langle \lambda ,t\rangle = \lambda^{it}\) ) between \(- E\) and \(E\) . Thus we see clearly that the first approximation to \(N(E)\) appears as the lack of surjectivity of the map which associates to quantum states \(\xi\) belonging to \(D^{\prime}\) the function on \(\mathbb{R}_{+}^{*}\)

\[E(\xi)(x) = |x|^{1 / 2}\sum_{n\in \mathbb{Z}}\xi (nx)\]

where we assume the additional conditions \(\xi (0) = \int \xi (x)dx = 0\) .

A finer analysis, which is just what the trace formula is doing, would yield the additional terms \(7 / 8 + o(1) + N_{osc}(E)\) . The above discussion yields an explicit construction of a large matrix whose spectrum approaches the zeros of zeta as \(\Lambda \rightarrow \infty\) .

It is quite remarkable that the eigenvalues of the angle operator \(\Theta\) which we discussed above, also play a key role in the theory of random unitary matrices. To be more specific, let \(E(n,s)\) be the large \(N\) limit of the probability that there are exactly \(n\) eigenvalues of a random Hermitian \(N\times N\) matrix in the interval \([- \frac{\pi}{\sqrt{2N}} t,\frac{\pi}{\sqrt{2N}} t]\) \(t = s / 2\) . Clearly \(\sum_{n}E(n,s) = 1\) . Let \(P_{t}\) be as above the operator of multiplication by \(1_{[- t,t]}\) - characteristic function of the interval \([- t,t]\) in the Hilbert space \(L^{2}(\mathbb{R})\) . In general (cf [Me]), \(E(n,s)\) is \((- 1)^{n}\) times the \(n\) - th coefficient of the Taylor expansion at \(z = 1\) of \(\zeta_{s}(z) = \prod_{1}^{\infty}(1 - z\lambda_{j}(s))\) , where \(\lambda_{j}(s)\) are the eigenvalues of the operator \(\widehat{P_{n}} P_{t}\) . (Here we denote by \(\widehat{P_{\lambda}} = \mathcal{F}P_{\lambda}\mathcal{F}^{- 1}\) , and \(\mathcal{F}\) denotes the Fourier transform, \(\mathcal{F}\xi (u) = \int e^{i x u}\xi (x)d x\) . Note also that the eigenvalues of \(\widehat{P_{a}} P_{b}\) only depend upon the product \(a b\) so that the relation with the eigenvalues of \(\Theta\) should be clear.)

---

以上是论文第III节至第VIII节的完整内容。