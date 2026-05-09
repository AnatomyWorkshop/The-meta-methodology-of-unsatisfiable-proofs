# Illusion: A Constructive Verification of the Self-Referential Safety Framework

| | |
|---|---|
| **Status** | Draft |
| **Date** | 2026-05-09 |
| **Keywords** | circuit complexity, self-referential safety, discriminating properties, lower bounds, AC⁰, monotone circuits, algebraic circuits |

---

## Abstract

We present Illusion, a three-layer search system that operationalizes the self-referential safety (SRS) framework introduced in [Xie 2026]. The framework predicts that every successful circuit lower bound proof must use a discriminating property that is not decidable within the model being analyzed. Illusion tests this prediction constructively: given a computational model L1 and a target function, the system's L2 layer searches for candidate discriminating properties, while the L3 layer checks whether each candidate satisfies the self-referential safety condition.

We validate Illusion across three domains — AC⁰ circuits, monotone circuits, and algebraic circuits over GF(p) — using the same core architecture throughout. In each domain, L2 independently arrives at the key discriminating property used in the corresponding classical lower bound proof: Håstad's random restriction (AC⁰), Razborov's approximation method (monotone circuits), and the Razborov-Smolensky algebraic restriction (algebraic circuits). The L3 layer correctly classifies all candidates, including a false positive (field reduction) that achieves comparable statistical signal to the true discriminating property but is decidable within the model.

These results provide constructive support for the SRS framework's central claim: the self-referential safety condition is not merely a post-hoc description of known proofs, but a structural constraint that, when enforced architecturally, guides search toward the correct proof techniques.

---

## 1. Introduction

The SRS framework [Xie 2026] identifies a common structural feature across known impossibility results in computational complexity: every successful lower bound proof uses a discriminating property P whose decidability cost exceeds the capacity of the model being analyzed. When this condition fails — when P is decidable within the model — the proof either does not work or reduces to a known barrier (relativization, natural proofs, algebrization).

This is a retrospective claim: it describes known proofs. A stronger claim would be predictive: if we design a search system that enforces the self-referential safety condition architecturally, will it find the correct proof techniques without being told what to look for?

Illusion answers this question. It is not a theorem prover. It is a minimal prototype that asks: in a domain where the answer is already known, does enforcing the SRS condition guide the search to the right place?

The answer, across three domains, is yes.

### 1.1 What Illusion is not

Illusion does not prove new theorems. It does not generate proofs. It does not replace human mathematical judgment. Its L3 layer, which checks self-referential safety, relies on human-written rules in known domains and escalates to human review for unknown cases.

What Illusion does is narrow the search space. Given a computational model and a target function, it identifies which classes of transformations produce discriminating properties that are structurally safe — and which produce properties that are statistically effective but logically unsafe. This distinction, as we show in §6, cannot be made by statistical signal alone.

### 1.2 Relation to the companion paper

This paper assumes familiarity with the SRS framework defined in [Xie 2026], specifically:
- Definition 2.1 (self-referential safety)
- The SRS index α = cost(P) / cap(M)
- The three barriers theorem (§6.3 of [Xie 2026])

We do not restate these definitions here. All notation follows [Xie 2026].

---

## 2. System Architecture

Illusion implements a three-layer architecture. The layers are strictly separated: L2 cannot access L1's internal structure directly, and L3 monitors whether L2's candidates have slipped into L1's decidability range.

```
L3  Self-referential safety monitor
 ↕  monitors whether L2 candidates are decidable within L1
L2  Discriminating property search (transform registry + collapse metric)
 ↕  analyzes L1, generates candidate properties P
L1  Object model (the computational model under analysis)
```

### 2.1 L1: Object model

L1 simulates the computational model being analyzed. In Phase 1, L1 is an AC⁰ circuit simulator. In Phase 3, a monotone circuit simulator. In Phase 4d, an algebraic circuit simulator over GF(p). The L1 interface is uniform: given an input, return an output. The internal structure of L1 is not exposed to L2.

### 2.2 L2: Transform search

L2 maintains a registry of transforms — operations that modify a circuit or its input space. For each transform T, L2 measures the **Δcollapse** metric:

```
collapse(C) = 1 - distinguishing_advantage(C, D⁺, D⁻)
Δcollapse(T) = mean over circuits C of [collapse(T(C)) - collapse(C)]
```

where D⁺ and D⁻ are distributions designed so that a circuit computing the target function can distinguish them, while a circuit that cannot compute the target function cannot.

A transform T is a **candidate** if:
1. Δcollapse(T) > threshold (default: 0.03), and
2. T does not affect the target function itself (verified by a separate `affects_target` check)

### 2.3 L3: Self-referential safety monitor

L3 checks whether each candidate property P is decidable within L1. It maintains a rule library of known SAFE and UNSAFE patterns, and returns one of three verdicts:

- **SAFE**: P is not decidable within L1 (self-referentially safe, valid candidate)
- **UNSAFE**: P is decidable within L1 (discard)
- **UNKNOWN**: no matching rule; escalate to human review

The L3 rule library is domain-specific and injected at runtime. The core monitor logic is unchanged across all domains.

### 2.4 MCP integration (Phase 4)

When L2's transform registry is exhausted without finding a SAFE candidate, the system calls an external LLM via the Model Context Protocol (MCP) to propose new transforms. The LLM suggestions are presented to the human for review before implementation. The L3 safety check applies to all AI-proposed transforms without exception.

The termination condition (ExhaustionCriterion) fires when: N consecutive AI-proposal rounds produce no new SAFE candidates, and the best Δcollapse in the last M rounds has not improved by more than a threshold.

---

## 3. AC⁰ Experiment (Phase 1)

**L1**: AC⁰ circuit simulator (constant depth, AND/OR/NOT gates, fan-in 2)
**Target function**: PARITY (known to require exponential AC⁰ circuits, Håstad 1987)
**Distributions**: D⁺ = inputs with even parity, D⁻ = inputs with odd parity
**Parameters**: n=8 input bits, depth=3, 30 circuits, 500 samples

### 3.1 Results

| Transform | Δcollapse | Target affected | L3 verdict |
|-----------|-----------|----------------|------------|
| exhaustive_parity_equivalent_check | +0.115 | No | **SAFE** |
| random_restriction_p0.5 | +0.080 | No | **SAFE** |
| random_restriction_p0.3 | +0.058 | No | **SAFE** |
| gate_substitution | +0.113 | Yes | rejected |
| input_negation | +0.008 | No | rejected |
| identity | +0.005 | No | rejected |
| input_permutation | −0.002 | No | rejected |

### 3.2 Interpretation

L2 identified two structurally distinct SAFE candidates. `exhaustive_parity_equivalent_check` — deciding whether a circuit computes PARITY by exhaustive evaluation — achieves the highest signal (Δ=+0.115) and is SAFE: verifying parity equivalence requires exponential time within AC⁰. `random_restriction` (Δ=+0.080 at p=0.5) is the structural analog of Håstad's switching lemma: randomly fixing input variables collapses the circuit's distinguishing power. Both are valid discriminating properties; `random_restriction` is the one that corresponds to the classical proof technique.

The system's only input was: here is an AC⁰ circuit simulator, here is PARITY, find a transform that degrades circuit performance without destroying the target function. It arrived at the same structural technique used in Håstad's proof without being told what to look for.

---

## 4. Monotone Circuit Experiment (Phase 3)

**L1**: Monotone circuit simulator (AND/OR gates only, no NOT)
**Target function**: k-CLIQUE (known to require exponential monotone circuits, Razborov 1985)
**Distributions**: D⁺ = random graph with planted k-clique, D⁻ = random (k-1)-partite graph
**Parameters**: n=6 vertices, k=3, depth=3, 30 circuits, 500 samples

### 4.1 Results

| Transform | Δcollapse | Target affected | L3 verdict |
|-----------|-----------|----------------|------------|
| subgraph_projection_p0.7 | +0.245 | No | **SAFE** |
| edge_deletion_p0.1 | +0.081 | No | **UNSAFE** |
| distribution_switch | +0.004 | No | rejected |
| identity | −0.002 | No | rejected |
| edge_permutation | −0.015 | No | rejected |

Transforms rejected by L2 for affecting clique structure (Δcollapse > threshold but clique_affected = True): `subgraph_projection_p0.5` (+0.328), `edge_deletion_p0.5` (+0.291), `edge_deletion_p0.3` (+0.216), `gate_elevation` (+0.131).

L3 classified `subgraph_projection_p0.7` as SAFE: deciding whether a circuit loses distinguishing advantage under random vertex removal requires exponential sampling over all possible vertex subsets. `edge_deletion_p0.1` was classified UNSAFE: setting edge inputs to 0 in a monotone circuit is a monotone operation decidable by a polynomial-size monotone circuit.

### 4.2 Interpretation

`subgraph_projection` is the structural analog of Razborov's approximation method: restricting to a random induced subgraph degrades the circuit's ability to detect cliques, in the same way that Razborov's method shows that monotone circuits cannot approximate the clique function. L2 arrived at this technique without being told about Razborov's proof.

`edge_deletion_p0.1` is a secondary case analogous to `field_reduction` in the algebraic domain: it produces measurable signal (Δ=+0.081) but is UNSAFE because the operation is local and decidable within the model. Statistical signal alone would not have distinguished it from `subgraph_projection`.

---

## 5. Algebraic Circuit Experiment (Phase 4d/4e)

**L1**: Algebraic circuit simulator over GF(7) (addition and multiplication gates)
**Target function**: n×n Permanent (known to require exponential algebraic circuits, Valiant 1979)
**Distributions**: D⁺ = random matrices over GF(7), D⁻ = rank-1 matrices (outer products)
**Parameters**: n=3 and n=4, depth=3, 20 circuits, 300 samples

The circuits used are `partial_permanent_circuit` instances — circuits that compute a random subset of Permanent terms. Random algebraic circuits have collapse ≈ 0.97 at baseline (already unable to distinguish D⁺ from D⁻), so they cannot serve as meaningful test subjects. Circuits that actually compute Permanent terms have collapse ≈ 0.86, providing measurable signal.

### 5.1 Results (n=3)

| Transform | Δcollapse | Permanent affected | L3 verdict |
|-----------|-----------|-------------------|------------|
| algebraic_restriction_p0.5 | +0.115 | No | **SAFE** |
| algebraic_restriction_p0.3 | +0.104 | No | **SAFE** |
| field_reduction_q2 | +0.105 | No | **UNSAFE** |
| algebraic_restriction_p0.7 | +0.132 | Yes | rejected |
| degree_truncation_d1 | +0.141 | Yes | rejected |
| identity | -0.008 | No | rejected |
| input_permutation | -0.008 | No | rejected |
| scalar_multiplication | +0.004 | No | rejected |

### 5.2 Results (n=4, Phase 4e)

| Transform | Δcollapse (n=3) | Δcollapse (n=4) | Trend |
|-----------|----------------|----------------|-------|
| algebraic_restriction_p0.3 | +0.104 | +0.124 | ↑ stronger |
| algebraic_restriction_p0.5 | +0.115 | +0.119 | ↑ stronger |
| field_reduction_q2 | +0.105 | +0.082 | ↓ weaker |

Signal for `algebraic_restriction` strengthens with n; signal for `field_reduction` weakens. This is the expected pattern: a true discriminating property becomes more powerful at larger scales, while a local operation's relative effect is diluted.

### 5.3 Interpretation

`algebraic_restriction` is the algebraic analog of the Razborov-Smolensky method: randomly fixing input variables reduces the circuit to a low-degree polynomial, which cannot compute Permanent (degree n). L2 found this without being told about Razborov-Smolensky.

---

## 6. Cross-Domain Analysis

### 6.1 Architecture invariance

The same L2 search engine and L3 monitor were used across all three domains. Only L1 and the transform registry were replaced.

| Phase | Domain | Target | Key transform | L3 | Classical method |
|-------|--------|--------|---------------|----|-----------------|
| 1 | AC⁰ | PARITY | random_restriction | SAFE | Håstad switching lemma |
| 3 | Monotone | k-CLIQUE | subgraph_projection | SAFE | Razborov approximation |
| 4d | Algebraic | Permanent | algebraic_restriction | SAFE | Razborov-Smolensky |

This is not a coincidence of design. The transforms were not pre-selected to match the classical proofs. The registry contained control transforms (identity, permutation, scalar multiplication) and domain-specific transforms at various parameter settings. L2 found the correct one in each case by measuring Δcollapse; L3 confirmed it by checking self-referential safety.

### 6.2 UNSAFE candidates: why L3 is necessary

The same pattern appears in two domains independently.

In the algebraic circuit experiment, `field_reduction_q2` achieved Δcollapse = +0.105 — nearly identical to `algebraic_restriction_p0.3` at +0.104. In the monotone circuit experiment, `edge_deletion_p0.1` achieved Δcollapse = +0.081, comparable to weaker parameter settings of `subgraph_projection`. By L2's statistical criterion alone, these would be valid candidates.

L3 distinguishes them in both cases:

| Domain | SAFE candidate | Δ | UNSAFE candidate | Δ | Why UNSAFE |
|--------|---------------|---|-----------------|---|------------|
| Algebraic | algebraic_restriction_p0.3 | +0.104 | field_reduction_q2 | +0.105 | local mod-q operation, poly-time decidable |
| Monotone | subgraph_projection_p0.7 | +0.245 | edge_deletion_p0.1 | +0.081 | monotone edge zeroing, decidable by monotone circuit |

The recurrence of this pattern across unrelated domains is not coincidental. Local operations — those that act independently on each input variable or gate — systematically produce statistical signal while remaining decidable within the model. They are the structural false positives of the Δcollapse metric. L3's self-referential safety check is the mechanism that removes them.

### 6.3 SRS index interpretation

Using the notation of [Xie 2026]:

For `algebraic_restriction`: the property P = "circuit loses distinguishing advantage under random variable fixing" has cost(P) = exponential (requires evaluating the circuit on exponentially many restricted inputs). For algebraic P/poly, cap(M) = polynomial. Therefore α = cost(P)/cap(M) ≫ 1 → **SAFE**.

For `field_reduction`: P = "circuit output changes under mod-q reduction" has cost(P) = O(n²) (local check). Therefore α ≤ 1 → **UNSAFE**.

---

## 7. Limitations

**1. Handwritten search space.** L2's transform registry is designed by humans. The system arrives at transforms that were placed in the search space. It does not invent genuinely new transforms. The MCP integration (§2.4) addresses this partially: when the registry is exhausted, an LLM proposes new transforms for human review. But the human remains the bottleneck for transform design.

**2. Collapse metric baseline bias.** The raw collapse score has a baseline of ~0.89 for identity transforms (circuits that are already unable to distinguish D⁺ from D⁻). The Δcollapse metric corrects for this, but the correction depends on the baseline being stable across circuit families. In the algebraic domain, random circuits have collapse ≈ 0.97, which is why `partial_permanent_circuit` was necessary.

**3. Scale.** Experiments use n=3–8. The Δcollapse signal strengthens with n (confirmed for Phase 3 and Phase 4e), but asymptotic behavior is not verified. The experiments are proofs of concept, not complexity-theoretic results.

**4. Signal strength dependency.** The framework requires the target circuit to have meaningful distinguishing ability at baseline. If the circuit family cannot distinguish D⁺ from D⁻ at all (collapse ≈ 1), no transform can produce measurable Δcollapse. This is a boundary condition on the framework's applicability, not a flaw — it reflects the fact that the framework is designed to analyze circuits that are trying to compute the target function.

**5. L3 rule coverage.** In all three experiments, L3 produced no UNKNOWN verdicts. This means the rule library was sufficient for the known domains tested. In unknown domains (Phase 5 target: proof complexity), UNKNOWN verdicts are expected and desired — they indicate candidate properties that may be genuinely new.

---

## 8. Conclusion

Illusion provides constructive support for the SRS framework's central prediction: enforcing the self-referential safety condition architecturally guides search toward the correct proof techniques. Across three domains with completely different proof structures, the same architecture independently arrived at the key discriminating property in each case.

The next step is Phase 5: applying the same architecture to proof complexity (Resolution/Frege), where the answer is not fully known. Phase 5 results are reported separately: applying the same architecture to Resolution proof complexity, the system produces the first UNKNOWN verdict on `variable_elimination`, pointing at the open separation between Resolution and Extended Resolution.

The Illusion codebase is available at: https://github.com/AnatomyWorkshop/The-meta-methodology-of-unsatisfiable-proofs

---

## References

Xie, J. (2026). *A Unified Theory of Impossibility Proofs: The SRS Program*. ResearchGate preprint, April 2026. DOI: 10.13140/RG.2.2.25731.26406

Håstad, J. (1987). Computational limitations of small-depth circuits. MIT Press.

Razborov, A. A. (1985). Lower bounds on the monotone complexity of some Boolean functions. *Doklady Mathematics*, 31, 354–357.

Razborov, A. A. (1987). Lower bounds on the size of bounded depth circuits over a complete basis with logical addition. *Mathematical Notes*, 41(4), 333–338.

Smolensky, R. (1987). Algebraic methods in the theory of lower bounds for Boolean circuit complexity. *STOC 1987*, 77–82.

Valiant, L. G. (1979). The complexity of computing the permanent. *Theoretical Computer Science*, 8(2), 189–201.

Ben-Sasson, E., & Wigderson, A. (2001). Short proofs are narrow — resolution made simple. *Journal of the ACM*, 48(2), 149–169.
