# A Notation System for Self-Referential Safety: Annotating the Structure of Impossibility Proofs

| | |
|---|---|
| **Status** | Draft |
| **Date** | 2026-05-09 |
| **Keywords** | notation system, self-referential safety, impossibility proofs, SRS index, proof annotation, model subscript |

---

## Abstract

We introduce a notation system for annotating the self-referential safety (SRS) structure of impossibility proofs. Standard mathematical notation does not distinguish between derivations that occur *within* a computational model M and operations that are applied *from outside* M. This distinction is the structural core of the SRS framework [Xie 2026]: a discriminating property P is self-referentially safe if and only if deciding P costs strictly more than M can compute. Without notation that makes this distinction visible, the framework's claims remain semi-formal.

We define a small set of symbols — derivation arrows ($\to_M$, $\nrightarrow_M$, $\Rrightarrow_M$), equivalence relations ($\equiv_M$, $\simeq_M$, $\approx_M$), capability relations ($\sqsubset_M$, $\mathring{\sqsubset}_M$), and the SRS index α = cost(P)/cap(M) — each carrying a model subscript M that anchors it to a specific computational context. We demonstrate the system by annotating four known impossibility results: AC⁰ lower bounds, monotone circuit lower bounds, Gödel's incompleteness theorem, and the 3D Navier-Stokes regularity problem.

This notation system is not an axiomatic system. It does not produce new proofs. It is a structural annotation tool: a way of reading existing proofs that makes their self-referential safety structure explicit and checkable.

---

## 1. Introduction

The SRS framework [Xie 2026] identifies a common structural feature across known impossibility results: every successful proof uses a discriminating property P whose decidability cost exceeds the capacity of the model being analyzed. This is a claim about the *structure* of proofs, not their content.

Standard mathematical notation does not make this structure visible. When a proof writes $f \notin \mathcal{C}$, it does not say whether the witness to this fact is computable within $\mathcal{C}$ or requires resources beyond $\mathcal{C}$. When a proof uses a random restriction, it does not annotate whether the restriction is an operation inside the model or an external tool applied to it. The distinction matters: if the discriminating property is decidable within the model, the proof either fails or reduces to a known barrier.

The notation system introduced here fills this gap. Every symbol carries a model subscript M. Every derivation step is annotated as either M-internal ($\to_M$) or M-external ($\Rrightarrow_M$). Every equivalence relation is classified by whether it is decidable within M. The SRS index α quantifies how far the discriminating property sits outside M's reach.

### 1.1 Design principles

1. **The model subscript is the core.** Every symbol carries subscript M, anchoring it to a specific computational model. Without M, the symbols have no semantics.

2. **Annotation, not replacement.** This system adds a structural layer on top of traditional proofs. It does not replace them. A traditional proof remains a proof; the annotation records its safety structure.

3. **Operational semantics.** Every symbol answers two questions: *under what conditions is it used*, and *who determines those conditions*. The answer to the second question is always L3 (the self-referential safety monitor in the Illusion system).

4. **Minimal vocabulary.** Only symbols with operational semantics are introduced. No symbol is added for elegance alone.

### 1.2 Relation to the Illusion system

The Illusion system implements the SRS framework as a three-layer search architecture. The notation system introduced here is the *metalanguage* of that architecture: it describes what L3 checks, what L2 produces, and what the SAFE/UNSAFE/UNKNOWN verdicts mean in formal terms. Illusion is the running implementation; this notation system is the formal specification of what it computes.

---

## 2. Core Symbols

### 2.1 Derivation arrows

| Symbol | Reading | Semantics | Determined by |
|--------|---------|-----------|---------------|
| $\to_M$ | "derivable within M" | A derivation chain from premise to conclusion, every step within M's capacity | L2 (automated) |
| $\nrightarrow_M$ | "unreachable within M" | No derivation chain exists within M | L3 (safety check) |
| $\Rrightarrow_M$ | "M-external operation" | Uses tools that exceed M's capacity | L3 (source annotation) |

**Usage rules:**

$A \to_M B$: M contains a derivation chain from A to B. Every step is an M-decidable operation.

$A \nrightarrow_M B$: No such chain exists. This is L3's core judgment — if L3 determines that a property P satisfies $P \nrightarrow_M \text{decidable}$, then P is self-referentially safe.

$A \Rrightarrow_M B$: The derivation from A to B uses tools not simulable within M. This is the annotation for the key step in every successful impossibility proof: the discriminating property is applied from outside the model.

### 2.2 Equivalence relations

| Symbol | Reading | Semantics | Safety level |
|--------|---------|-----------|--------------|
| $\equiv_M$ | "structurally equivalent within M" | Two objects are indistinguishable under M's structural measure | SAFE |
| $\simeq_M$ | "extensionally equivalent within M" | Same outputs under M, different structure | Requires L3 check |
| $\approx_M$ | "undecidably equivalent within M" | M cannot determine whether the two are equivalent | Axiomatic only |

**Operational semantics:**

$X \equiv_M Y$: M contains a decidable procedure verifying that X and Y are structurally identical. Example: two AC⁰ circuits with isomorphic gate structure (verifiable in poly(n) time).

$X \simeq_M Y$: X and Y agree on some extensional measure, but M cannot verify structural identity. Example: two transforms that produce the same Δcollapse on a test set but operate differently (random restriction vs. exhaustive parity check).

$X \approx_M Y$: M cannot determine whether X and Y are equivalent — the verification requires resources beyond M. Example: deciding whether a restricted circuit equals a known constant function requires enumerating 2ⁿ inputs.

**Who classifies?** L3. When L2 generates a candidate equivalence, L3 checks: is the verification process completable within M? If yes, label $\equiv_M$; if only extensionally verifiable, label $\simeq_M$; if not verifiable at all, label $\approx_M$.

**Decision rule for $\simeq_M$.** A pair (X, Y) is classified as $\simeq_M$ if L3 can verify that X and Y agree on M-observable measures but cannot verify structural identity within M's capacity. The boundary between $\equiv_M$ and $\simeq_M$ is M-dependent and determined by L3.

### 2.3 Capability relations

| Symbol | Reading | Semantics |
|--------|---------|-----------|
| $\sqsubset_M$ | "strictly weaker within M" | A's capacity is a proper subset of B's under M's measure |
| $\mathring{\sqsubset}_M$ | "axiom-level separation within M" | The separation between A and B is undecidable within M but consistent as an external assumption |

**Precise definition of $\mathring{\sqsubset}_M$:**

$$A \mathring{\sqsubset}_M B \;\iff\; (A \nrightarrow_M B) \;\land\; (B \nrightarrow_M A) \;\land\; \text{Con}(M + A \sqsubset B)$$

Read: within M, the separation of A and B is neither provable nor refutable, but assuming A is strictly weaker than B does not break M's consistency.

**Canonical instances:**
- $P \mathring{\sqsubset}_{P/\text{poly}} NP$: within the polynomial circuit model, the P vs. NP separation is undecidable, but assuming P ≠ NP is consistent.
- $\text{Con}(F) \mathring{\sqsubset}_F \text{True}$: within formal system F, F's consistency is unprovable, but assuming F is consistent does not break F.

### 2.4 Quantifiers

| Symbol | Reading | Semantics |
|--------|---------|-----------|
| $\forall_M$ | "for all within M" | Over all M-enumerable objects |
| $\exists_M$ | "constructible within M" | There exists an M-constructible object |

When M's object space is not enumerable (e.g., real numbers), $\forall_M$ reduces to the standard universal quantifier. The subscript M then marks only that the quantification occurs in M's context.

### 2.5 Model extension

When an external tool $T^*$ is added to M:

$$M^* = M \cup \{T^*\}$$

The SRS index of a property P may decrease under extension:

$$\alpha_{M^*}(P) \leq \alpha_M(P)$$

If $T^*$ reduces α from $\gg 1$ to $\approx 1$, then P becomes decidable within $M^*$. This is the precise meaning of "reducing" a discriminating property — and the mechanism behind the three known barriers (relativization, natural proofs, algebrization).

---

## 3. The SRS Index

### 3.1 Definition

$$\alpha = \text{SRS}(M, P) = \frac{\text{minimum computational resources required to decide } P}{\text{maximum computational resources available within } M}$$

| α value | Meaning | Safety verdict |
|---------|---------|----------------|
| α ≤ 1 | P is decidable within M | UNSAFE |
| α > 1 | P is not decidable within M | SAFE |
| α = ∞ | P is structurally unreachable within M | SAFE (Gödel-level) |

### 3.2 Verified numerical values

| Case | n | α | Scaling |
|------|---|---|---------|
| AC⁰ vs. PARITY | 8 | ≈ 10² | 3ⁿ / poly(n) |
| Monotone circuits vs. k-CLIQUE | 6 | ≈ 9.1×10² | 2^{n(n-1)/2} / poly(n) |
| Gödel's incompleteness | — | ∞ | — |
| 2D Navier-Stokes (control) | — | ≈ 1 | poly(Re) / poly(Re) |
| 3D Navier-Stokes (estimate) | Re=10⁴ | ≳ 10¹⁰ | Re³ / O(1) → ∞ |

The α values for AC⁰ and monotone circuits are experimentally verified via the Illusion system. The Gödel case is exact by definition. The NS estimate is structural rather than empirical and awaits numerical validation.

### 3.3 Compact inline notation

When annotating a proof step inline:

$$P \nrightarrow_M \text{decidable} \quad (\alpha \approx 10^2)$$

The parenthetical α value is supporting information, not part of the core symbol. The core judgment is $\nrightarrow_M$ (qualitative); α provides quantitative support.

---

## 4. Annotation Examples

### 4.1 AC⁰ lower bounds for PARITY

$$M = AC^0 \text{ (depth } d\text{, size poly}(n)\text{, AND/OR/NOT)}$$
$$f = \text{PARITY}$$
$$P = \text{"circuit collapses to a constant under random restriction"}$$

$$P \nrightarrow_{AC^0} \text{decidable} \quad (\alpha \approx 10^2)$$
$$\text{random\_restriction} \Rrightarrow_{AC^0} \text{collapse}$$
$$\therefore P \text{ is a self-referentially safe discriminating property}$$

The random restriction is applied from outside AC⁰ (it requires computing an expectation over exponentially many restrictions). The induced property — that the circuit collapses — is not decidable within AC⁰. This is the structural content of Håstad's switching lemma.

### 4.2 Monotone circuit lower bounds for k-CLIQUE

$$M = \text{Monotone circuits (AND/OR only, poly}(n)\text{)}$$
$$f = k\text{-CLIQUE}$$
$$P = \text{"circuit loses distinguishing advantage under random subgraph projection"}$$

$$P \nrightarrow_{\text{Monotone}} \text{decidable} \quad (\alpha \approx 9.1 \times 10^2)$$
$$\text{subgraph\_projection} \Rrightarrow_{\text{Monotone}} \text{advantage loss}$$
$$\therefore P \text{ is a self-referentially safe discriminating property}$$

### 4.3 Gödel's incompleteness theorem

$$M = F \text{ (consistent, sufficiently expressive formal system)}$$
$$G_F \equiv_M \neg\text{Prov}_M(G_F) \quad \text{(diagonal lemma, constructed within } M\text{)}$$
$$G_F \nrightarrow_M \text{provable} \quad (\alpha = \infty)$$
$$\mathbb{N} \models G_F \quad (\Rrightarrow_{\mathbb{N}} \text{true in the standard model, external semantic step})$$

The Gödel sentence is constructed within M (the diagonal lemma is an M-internal operation), but its truth is established from outside M (the standard model is an external semantic resource). The separation is $\alpha = \infty$: no finite extension of M can decide $G_F$ without changing the system.

### 4.4 3D Navier-Stokes regularity (exploratory)

$$M_{\text{NS}} = \text{3D incompressible NS + current best analytic tools}$$
$$P_{\text{smooth}} = \forall \boldsymbol{u}_0 \in C^\infty: \text{global smooth solution exists}$$

$$P_{\text{smooth}} \nrightarrow_{M_{\text{NS}}} \text{provable} \quad (\alpha \gtrsim 10^{10},\ \text{Re}=10^4,\ \text{conjectured})$$
$$\neg P_{\text{smooth}} \nrightarrow_{M_{\text{NS}}} \text{provable} \quad \text{(conjectured)}$$
$$\therefore P_{\text{smooth}} \mathring{\sqsubset}_{M_{\text{NS}}} \text{True?} \quad \text{(candidate axiom-level separation)}$$

This is a structural conjecture, not a proof. The annotation records the hypothesis that the NS regularity question may be an axiom-level separation within current analytic tools — analogous to P vs. NP within polynomial circuits.

---

## 5. Known Misuse Patterns

Three misuse patterns were identified during the development of this notation system:

**1. Treating definitions as axioms.** The commutativity of real addition is not an axiom — it is a definitional property of the real field. AC⁰ ⊊ NC¹ is not an axiom — it is a proved theorem. Monotone circuits excluding NOT gates is not an axiom — it is the model's definition. Only statements that can be assumed or not assumed without breaking consistency qualify for $\mathring{\sqsubset}_M$.

**2. Confusing external reasoning with choice.** $\Rrightarrow_M$ marks an external *inference step*, not a human *choice of assumption*. "P ≠ NP is the optimal axiom" cannot be written as $\Rrightarrow_M$ — that is a meta-level judgment, not a derivation. The correct notation is $\mathring{\sqsubset}_M$.

**3. Using the same $\Rrightarrow_M$ for structurally different external operations.** The halting problem's "external" is pure logical diagonalization; Gödel's "external" is the standard model's semantic interpretation; the CLIQUE lower bound's "external" is a combinatorial construction. These are different kinds of M-external operations. The current system does not distinguish them — this is a deliberate simplification. If finer annotation is needed, superscripts ($\Rrightarrow_M^{\text{diag}}$, $\Rrightarrow_M^{\text{sem}}$, $\Rrightarrow_M^{\text{comb}}$) can be introduced.

---

## 6. Relation to the Illusion System

The Illusion system implements the SRS framework as a three-layer architecture. The notation system introduced here is the formal language of that architecture:

| Illusion component | Notation counterpart |
|-------------------|---------------------|
| L1 (object model) | M (the subscripted model) |
| L2 (transform search) | Generates candidate $\Rrightarrow_M$ operations |
| L3 SAFE verdict | $P \nrightarrow_M \text{decidable}$, α > 1 |
| L3 UNSAFE verdict | $P \to_M \text{decidable}$, α ≤ 1 |
| L3 UNKNOWN verdict | $P \mathring{\sqsubset}_M \text{decidable}$? — open question |
| Δcollapse metric | Empirical estimate of α > 1 |

Two UNKNOWN verdicts have been produced, each corresponding to a distinct $\mathring{\sqsubset}_M$ instance:

**Resolution (width metric):** The system found `variable_elimination` (Δcollapse = +0.78) whose induced property cannot be classified as decidable or undecidable within Resolution, because the relevant separation (Resolution vs. Extended Resolution) is an open problem:

$$P_{\text{var\_elim}} \mathring{\sqsubset}_{\text{Resolution}} \text{decidable?} \quad \text{(Cook \& Reckhow 1979, open)}$$

**Frege (size metric):** The system found `cross_branch_caching` (Δcollapse = +1.000) whose induced property — whether cross-branch sharing of intermediate derivations genuinely reduces proof size — is the Frege vs Extended Frege separation:

$$P_{\text{caching}} \mathring{\sqsubset}_{\text{Frege}} \text{decidable?} \quad \text{(Cook \& Reckhow 1979; Krajíček \& Pudlák 1989, open)}$$

The same operation tested at the depth metric produces zero signal and no UNKNOWN — correctly reflecting that bounded-depth Frege lower bounds are known (Krajíček & Pudlák 1995). In the notation of this paper: $P_{\text{caching}} \to_{\text{depth-Frege}} \text{irrelevant}$ (the property does not induce collapse at the depth level, so the decidability question does not arise).

---

## 7. What This System Does Not Do

- **It does not produce new proofs.** It annotates existing ones.
- **It does not replace traditional mathematics.** Traditional proofs remain proofs; the annotation adds a structural layer.
- **It does not automate L3.** The annotation records L3's judgment; it does not replace it.
- **It does not annotate its own safety.** L3's annotations are for L2's candidates, not for L3 itself. This is a design constraint, not a flaw.

---

## 8. Open Problems

1. **Granularity of $\to_M$.** The current system does not distinguish single-step from multi-step derivations. If Lean/Coq integration requires annotating individual proof tree steps, $\to_M^{(1)}$ (single step) and $\to_M^{(*)}$ (transitive closure) may be needed.

2. **PDE evolution.** In the NS case, "solution evolves over time" is not a derivation — it is a dynamical process. Candidate symbol: $\leadsto_M$ (M-internal evolution, endpoint unknown). Not introduced here.

3. **Algebraic analog of α.** The companion paper [Xie 2026] proposes $\text{SRS}_\otimes(M,P) = \text{rank}(X_P) / \max_{A \in M} \text{rank}(X_A)$ for algebraic circuit domains. This definition becomes operationally necessary in Phase 4d of the Illusion system. Formal development is deferred.

4. **Operational semantics of $\simeq_M$.** Under what conditions is an equivalence classified as $\simeq_M$ rather than $\equiv_M$? The boundary depends on M's structure and is determined by L3. Precise rules will be defined when the first concrete case arises in the Illusion system.

5. **Granularity of $\Rrightarrow_M$.** The current system does not distinguish between structurally different kinds of external operations: logical diagonalization (halting problem), semantic interpretation (Gödel), and combinatorial construction (CLIQUE lower bound) all receive the same annotation. This is a deliberate simplification. For integration with formal proof assistants (Lean, Coq), superscript annotations ($\Rrightarrow_M^{\text{diag}}$, $\Rrightarrow_M^{\text{sem}}$, $\Rrightarrow_M^{\text{comb}}$) would be needed. This is an implementation-level extension, not a defect in the current design.

---

## References

Xie, J. (2026). *A Unified Theory of Impossibility Proofs: The SRS Program*. ResearchGate preprint, April 2026. DOI: 10.13140/RG.2.2.25731.26406

Gödel, K. (1931). Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I. *Monatshefte für Mathematik und Physik*, 38, 173–198.

Håstad, J. (1987). Computational limitations of small-depth circuits. MIT Press.

Razborov, A. A. (1985). Lower bounds on the monotone complexity of some Boolean functions. *Doklady Mathematics*, 31, 354–357.

Ben-Sasson, E., & Wigderson, A. (2001). Short proofs are narrow — resolution made simple. *Journal of the ACM*, 48(2), 149–169.

Cook, S. A., & Reckhow, R. A. (1979). The relative efficiency of propositional proof systems. *Journal of Symbolic Logic*, 44(1), 36–50.
