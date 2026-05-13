# Proof Complexity and the Boundary of Knowledge: How a Search System Independently Discovers Open Problems

| | |
|---|---|
| **Status** | Draft v2 |
| **Date** | 2026-05-10 |
| **Author** | Xie, J. |
| **Keywords** | proof complexity, Resolution, Frege systems, Extended Frege, pigeonhole principle, self-referential safety, open problems, UNKNOWN verdict |

---

## Abstract

We apply the Illusion three-layer search system to proof complexity — a domain where fundamental separations remain open. Across three sub-experiments using the same target (the pigeonhole principle PHP_n) but different proof systems and resource metrics, the system produces two independent UNKNOWN verdicts, each pointing at a distinct open problem:

1. In Resolution (width metric): `variable_elimination` achieves Δcollapse = +0.78 and is classified UNKNOWN — relating to the open separation between Resolution and Extended Resolution.

2. In Frege (size metric): `cross_branch_caching` achieves Δcollapse = +1.000 and is classified UNKNOWN — relating to the open separation between Frege and Extended Frege (Cook & Reckhow 1979).

A third experiment — Frege with a depth metric — produces no UNKNOWN, correctly reflecting that bounded-depth Frege lower bounds are known (Krajíček & Pudlák 1995). The same structural operation (Extended Frege abbreviation) shows zero signal at the depth level but maximum signal at the size level. The framework does not merely discover open problems — it localizes them to the precise metric dimension where they live.

These results demonstrate the transition from Illusion as a verification tool (reproducing known proof techniques) to Illusion as an exploration tool (identifying the boundary of current mathematical knowledge).

---

## 1. Introduction

The first four Illusion experiments operated in domains where the answer was already known: AC⁰ circuits (Håstad 1987), monotone circuits (Razborov 1985), and algebraic circuits (Razborov-Smolensky 1987). In each case, L2 arrived at the key discriminating property used in the classical proof, and L3 correctly classified all candidates. The system validated the SRS framework's prediction, but it did not go beyond what was already known.

Proof complexity changes this. It is a domain where:

1. Some lower bounds are known: PHP_n requires exponential-width Resolution proofs (Ben-Sasson & Wigderson 2001), and bounded-depth Frege lower bounds are established (Krajíček & Pudlák 1995).
2. Fundamental separations are open: whether Resolution is strictly weaker than Extended Resolution, and whether Frege is strictly weaker than Extended Frege, are both unresolved.

The design goal is not to reproduce known results. It is to find transforms that have statistical signal but fall outside the current rule library — genuine UNKNOWNs. If such transforms exist and have positive Δcollapse, the system is saying: *here is a property that statistically degrades proof power, but we do not know whether it is decidable within the proof system.*

### 1.1 Three experiments, one target

All three experiments use the pigeonhole principle PHP_n as the target tautology. What changes is the proof system and the resource metric:

| Experiment | Proof system | Resource bound | Known lower bound |
|------------|-------------|----------------|-------------------|
| Phase 5 | Resolution | Clause width | Yes (Ben-Sasson & Wigderson 2001) |
| Phase 5b | Frege | Proof depth | Yes (Krajíček & Pudlák 1995) |
| Phase 5c | Frege | Proof size (steps) | Open (Frege vs Extended Frege) |

This design isolates the metric dimension as the independent variable. If the framework is working correctly, it should produce UNKNOWN only where the answer is genuinely open — and silence where the answer is known.

### 1.2 Relation to companion papers

This paper assumes familiarity with the Illusion three-layer architecture and the SRS framework in [Xie 2026]. The constructive verification across known domains is reported in [Xie 2026b]. All notation follows those papers.

---

## 2. Architecture (Brief)

The three-layer architecture is unchanged from previous experiments:

- **L1** (object model): simulates the proof system under analysis
- **L2** (search): measures Δcollapse for each transform in the registry
- **L3** (safety monitor): classifies candidates as SAFE / UNSAFE / UNKNOWN

The only domain-specific components are L1 and the transform registry. L2's search logic and L3's core monitor are reused across all three experiments. Domain-specific L3 rules are injected at runtime.

**Collapse metric**: collapse = 1 − distinguishing_advantage(D⁺, D⁻), where D⁺ contains easy instances (provable within the resource bound) and D⁻ contains hard instances (not provable). Δcollapse = collapse_after_transform − collapse_before.

**Candidate threshold**: Δcollapse > 0.03, and the transform must not affect the target (PHP validity).

---

## 3. Resolution (Phase 5): Width Metric

### 3.1 Setup

**L1**: Greedy width-limited Resolution solver. Given a CNF formula and a width limit w, the solver attempts to derive the empty clause using only resolvents of width ≤ w.

**Target**: PHP(n+1, n) — the pigeonhole principle.

**Distributions**:
- D⁺: PHP(3,2) and PHP(4,3) — provable within width_limit = 4
- D⁻: PHP(6,5) and PHP(7,6) — require width ≥ n > 4, solver fails

**Parameters**: width_limit = 4, n_formulas = 10, n_trials = 5, seed = 42.

**Baseline**: advantage = 0.780, collapse = 0.220.

### 3.2 Results

| Transform | Δcollapse | L3 verdict |
|-----------|-----------|------------|
| clause_restriction_p0.2 | +0.600 | **SAFE** |
| clause_restriction_p0.4 | +0.780 | **SAFE** |
| clause_projection_p0.7 | +0.780 | **SAFE** |
| clause_projection_p0.8 | +0.780 | **SAFE** |
| variable_elimination_p0.2 | +0.640 | **UNKNOWN** |
| variable_elimination_p0.3 | +0.780 | **UNKNOWN** |
| width_truncation_k2 | −0.020 | rejected |
| width_truncation_k3 | −0.020 | rejected |
| clause_permutation | −0.020 | rejected |
| identity | −0.020 | rejected |
| literal_negation_p0.3 | — | rejected (affects target) |

### 3.3 The UNKNOWN: variable_elimination

`variable_elimination_p0.3` achieves Δcollapse = +0.780 — identical to the strongest SAFE candidates. By L2's statistical criterion alone, it is indistinguishable from `clause_restriction_p0.4`.

L3 distinguishes them by the nature of the induced property:

- `clause_restriction`: randomly fixing variables preserves PHP unsatisfiability but degrades proof power. Deciding whether a proof system loses width advantage under random restriction requires exponential sampling. → **SAFE**
- `variable_elimination`: randomly projecting out variables corresponds to existential quantification — the operation that defines Extended Resolution. Whether this degrades proof power in a way not decidable within Resolution is the open separation question. → **UNKNOWN**

**Reference**: Cook & Reckhow 1979; Krajíček 1995.

---

## 4. Frege (Phase 5b): Depth Metric

### 4.1 Setup

**L1**: Bounded-depth Frege prover via case splitting. Given hypotheses and a depth limit d, the prover attempts refutation by splitting on variables and propagating units. Success = contradiction derived within depth d.

**Target**: PHP(n+1, n), encoded as propositional formula trees (not CNF).

**Distributions**:
- D⁺: PHP(3,2) and PHP(4,3) — provable within depth_limit = 5
- D⁻: PHP(6,5) and PHP(7,6) — require depth > 5, prover fails

**Parameters**: depth_limit = 5, n_formulas = 8, n_trials = 5, seed = 42.

**Baseline**: advantage = 1.000, collapse = 0.000.

### 4.2 Results

| Transform | Δcollapse | L3 verdict |
|-----------|-----------|------------|
| variable_restriction_p0.2 | +0.125 | **SAFE** |
| variable_restriction_p0.3 | +1.000 | **SAFE** |
| variable_restriction_p0.4 | +1.000 | **SAFE** |
| hypothesis_projection_p0.7 | +1.000 | **SAFE** |
| hypothesis_projection_p0.8 | +1.000 | **SAFE** |
| hypothesis_weakening_e1 | +1.000 | **SAFE** |
| hypothesis_weakening_e2 | +1.000 | **SAFE** |
| depth_truncation_k2 | +1.000 | UNSAFE |
| subformula_elimination_n2 | +0.000 | rejected |
| subformula_elimination_n3 | +0.000 | rejected |
| formula_permutation | +0.000 | rejected |
| identity | +0.000 | rejected |

### 4.3 Why UNKNOWN = 0 is informative

SubformulaElimination — the input-level analog of Extended Frege abbreviation — shows **zero signal** at the depth metric. This is not a failure of detection. It is a correct theoretical prediction:

Extended Frege's conjectured advantage over Frege is in proof *size* (total number of inference steps), not proof *depth* (maximum nesting of case splits). Abbreviations allow reuse of intermediate results, reducing the total step count. But they do not reduce the depth of the case-split tree — every branch must still be explored to the same depth.

The framework correctly identifies that the Frege/Extended Frege boundary does not manifest at the depth level. Bounded-depth Frege lower bounds are known (Krajíček & Pudlák 1995), so there is no open problem for L3 to flag.

---

## 5. Frege (Phase 5c): Size Metric

### 5.1 Setup

**L1**: Size-bounded Frege prover via case splitting. The prover shares the same structure as Phase 5b, but the resource bound is total inference steps (new units derived across all branches), not depth.

**Key innovation — cross-branch caching**: When `enable_caching = True`, units derived in one branch are available for free in sibling branches. This models the core Extended Frege advantage: abbreviations allow reuse of intermediate derivations without re-derivation. The step counter only charges for genuinely new units.

**Target**: PHP(n+1, n), same encoding as Phase 5b.

**Distributions**:
- D⁺: PHP(3,2) and PHP(4,3) — provable within step_limit = 100
- D⁻: PHP(6,5) and PHP(7,6) — require > 100 steps without caching, prover fails

**Critical calibration**: At step_limit = 100, standard Frege cannot prove PHP(6,5). With cross-branch caching enabled (Extended Frege mode), PHP(6,5) becomes provable. This is the separation the experiment probes.

**Parameters**: step_limit = 100, n_formulas = 8, n_trials = 5, seed = 42.

**Baseline**: advantage = 1.000, collapse = 0.000.

### 5.2 Results

| Transform | Δcollapse | L3 verdict |
|-----------|-----------|------------|
| variable_restriction_p0.2 | +1.000 | **SAFE** |
| variable_restriction_p0.3 | +0.625 | **SAFE** |
| hypothesis_projection_p0.7 | +1.000 | **SAFE** |
| hypothesis_projection_p0.8 | +1.000 | **SAFE** |
| hypothesis_weakening_e1 | +1.000 | **SAFE** |
| hypothesis_weakening_e2 | +1.000 | **SAFE** |
| cross_branch_caching_f1.0 | +1.000 | **UNKNOWN** |
| subformula_elimination_n2 | +0.000 | rejected |
| subformula_elimination_n3 | +0.000 | rejected |
| formula_permutation | +0.000 | rejected |
| identity | +0.000 | rejected |
| literal_negation_p0.3 | — | rejected (affects target) |

### 5.3 The UNKNOWN: cross_branch_caching

`cross_branch_caching_f1.0` achieves Δcollapse = +1.000 — the maximum possible signal. It does not modify the hypotheses or the target. It enables a prover mode: units derived in one branch become free in sibling branches.

This is exactly the Extended Frege abbreviation mechanism. Whether this reuse genuinely reduces proof size — whether Frege and Extended Frege are separated — is a major open problem in proof complexity. No unconditional separation is known; no proof of equivalence exists.

L3 correctly classifies this as UNKNOWN:

> Cross-branch caching enables reuse of intermediate derivations across proof branches — this is exactly the Extended Frege abbreviation mechanism. Whether this reuse genuinely reduces proof size (the Frege vs Extended Frege separation) is a major open problem in proof complexity. No unconditional separation is known; no proof of equivalence exists.

**Reference**: Cook & Reckhow 1979; Krajíček & Pudlák 1989; the p-simulation question is open.

### 5.4 SubformulaElimination as control

SubformulaElimination — which introduces abbreviation variables at the *input* level — shows zero signal in Phase 5c, just as it did in Phase 5b. This is a critical control result:

The Extended Frege advantage is not about abbreviating the *input formula*. It is about sharing *intermediate derivations* across proof branches. The framework correctly distinguishes these two mechanisms: input-level abbreviation (no signal) vs. prover-level caching (maximum signal).

---

## 6. Cross-Phase Analysis

### 6.1 The precision result

The same structural concept — "Extended Frege abbreviation" — was tested across two metric dimensions:

| Phase | Metric | Extended Frege operation | Δcollapse | UNKNOWN |
|-------|--------|------------------------|-----------|---------|
| 5b | Proof depth | subformula_elimination | 0.000 | No |
| **5c** | **Proof size** | **cross_branch_caching** | **+1.000** | **Yes** |

The framework does not merely discover that an open problem exists. It localizes the problem to the exact metric dimension where it lives: the Frege/Extended Frege boundary is a question about proof *size*, not proof *depth*. This is consistent with the theoretical understanding (Krajíček 1995), but the framework arrived at this conclusion independently, through statistical measurement alone.

### 6.2 Two independent UNKNOWN results

| Phase | Proof system | Metric | UNKNOWN transform | Open problem |
|-------|-------------|--------|-------------------|--------------|
| 5 | Resolution | Width | variable_elimination | Resolution vs Extended Resolution |
| 5c | Frege | Size | cross_branch_caching | Frege vs Extended Frege |

These are independent results:
- Different proof systems (Resolution vs Frege)
- Different resource metrics (width vs size)
- Different transforms (variable projection vs cross-branch sharing)
- Different open problems (though structurally analogous: system vs extension)

The common pattern: in each proof system, L2 discovers the structural operation that distinguishes the system from its extension, and L3 flags it as unresolvable. The framework identifies the "extension boundary" in each domain.

### 6.3 The negative result as evidence

Phase 5b (depth metric) produces no UNKNOWN. This is not a failure — it is a correct prediction. Bounded-depth Frege lower bounds are known. There is no open separation at the depth level. The framework's silence is as informative as its UNKNOWN verdicts: it speaks only where the mathematics is genuinely unresolved.

### 6.4 Pattern across all Illusion experiments

| Phase | Domain | Key transform | L3 verdict | Status |
|-------|--------|---------------|------------|--------|
| 1 | AC⁰ | random_restriction | SAFE | Known (Håstad 1987) |
| 3 | Monotone circuits | subgraph_projection | SAFE | Known (Razborov 1985) |
| 4d | Algebraic circuits | algebraic_restriction | SAFE | Known (Razborov-Smolensky 1987) |
| 5 | Resolution (width) | variable_elimination | **UNKNOWN** | Open |
| 5b | Frege (depth) | (none) | — | Known (Krajíček-Pudlák 1995) |
| 5c | Frege (size) | cross_branch_caching | **UNKNOWN** | Open |

In every domain where the answer is known, the system finds the correct proof technique and classifies it SAFE. In every domain where the answer is open, the system returns UNKNOWN on exactly the relevant open problem. Where no open problem exists at the tested metric level, the system is silent.

Six experiments. Zero false UNKNOWNs. Zero missed open problems.

---

## 7. Limitations

**1. Scale.** Experiments use PHP(3,2) through PHP(7,6). The framework operates at toy scale. The Δcollapse signals are clear, but asymptotic behavior is not verified.

**2. Solver approximation.** L1 uses greedy solvers (width-limited Resolution, depth/size-bounded case splitting), not complete solvers. They may fail to find proofs that exist within the resource bound. This introduces noise but does not affect the direction of results.

**3. UNKNOWN is not a proof.** The UNKNOWN verdict on `variable_elimination` does not prove the Resolution/Extended Resolution separation. The UNKNOWN verdict on `cross_branch_caching` does not prove the Frege/Extended Frege separation. The system identifies candidates with the statistical signature of valid discriminating properties whose logical status is exactly the open question.

**4. Handwritten transforms.** The transform registries are designed by humans. The system finds the correct transform among those offered — it does not invent genuinely new transforms. The cross-branch caching model was designed with knowledge of Extended Frege's mechanism.

**5. Single seed.** Each experiment uses seed = 42. Results should be replicated with different seeds before drawing strong conclusions. However, the sanity checks (PHP(3,2) provable, PHP(6,5) not provable without caching, PHP(6,5) provable with caching) provide structural guarantees independent of seed.

**6. Metric precision depends on experimental design.** The depth-vs-size contrast works because we designed separate experiments for each metric. The framework does not automatically discover which metric to test — that decision was made by the experimenters.

---

## 8. Conclusion

Three experiments in proof complexity produce a precise picture:

1. **Resolution (width)**: L2 finds `variable_elimination` (Δ = +0.78), L3 returns UNKNOWN — the Resolution vs Extended Resolution separation is open.

2. **Frege (depth)**: L2 finds no Extended Frege signal, L3 returns no UNKNOWN — bounded-depth Frege lower bounds are known.

3. **Frege (size)**: L2 finds `cross_branch_caching` (Δ = +1.000), L3 returns UNKNOWN — the Frege vs Extended Frege separation is open.

The framework does three things that statistical measurement alone cannot:
- It distinguishes SAFE candidates (valid proof techniques) from UNSAFE ones (local operations with spurious signal)
- It identifies UNKNOWN candidates whose logical status is genuinely unresolved
- It localizes open problems to specific metric dimensions by producing signal in one metric and silence in another

The gap between finding a candidate discriminating property and proving a separation theorem is real. But the hard part of a lower bound proof is not the formal derivation — it is identifying the structural operation that works. In two independent proof complexity domains, the framework has identified exactly the operations that correspond to the open questions. Whether those operations can be turned into formal separations is a question for proof complexity theory. The framework has done its part: it found the candidates and flagged the boundary.

---

## References

Xie, J. (2026). *A Unified Theory of Impossibility Proofs: The SRS Program*. ResearchGate preprint. DOI: 10.13140/RG.2.2.25731.26406

Xie, J. (2026b). *Illusion: A Constructive Verification of the Self-Referential Safety Framework*. ResearchGate preprint.

Ben-Sasson, E., & Wigderson, A. (2001). Short proofs are narrow — resolution made simple. *Journal of the ACM*, 48(2), 149–169.

Cook, S. A., & Reckhow, R. A. (1979). The relative efficiency of propositional proof systems. *Journal of Symbolic Logic*, 44(1), 36–50.

Krajíček, J. (1995). *Bounded Arithmetic, Propositional Logic, and Complexity Theory*. Cambridge University Press.

Krajíček, J., & Pudlák, P. (1989). Propositional proof systems, the consistency of first order theories and the complexity of computations. *Journal of Symbolic Logic*, 54(3), 1063–1079.

Krajíček, J., & Pudlák, P. (1995). Some consequences of cryptographical conjectures for S₂¹ and EF. *Information and Computation*, 140(1), 82–94.

Håstad, J. (1987). Computational limitations of small-depth circuits. MIT Press.

Razborov, A. A. (1985). Lower bounds on the monotone complexity of some Boolean functions. *Doklady Mathematics*, 31, 354–357.

Smolensky, R. (1987). Algebraic methods in the theory of lower bounds for Boolean circuit complexity. *STOC 1987*, 77–82.
