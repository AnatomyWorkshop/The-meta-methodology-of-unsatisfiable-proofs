# Illusion in Proof Complexity: Resolution, PHP, and the First UNKNOWN

| | |
|---|---|
| **Status** | Draft |
| **Date** | 2026-05-09 |
| **Keywords** | proof complexity, Resolution, pigeonhole principle, UNKNOWN verdict, Extended Resolution, self-referential safety |

---

## Abstract

We apply the Illusion three-layer search system to Resolution proof complexity, using the pigeonhole principle PHP_n as the target. This is the first Illusion experiment in a domain where the answer is not fully known: while Ben-Sasson and Wigderson (2001) established that PHP_n requires exponential-width Resolution proofs, the relationship between Resolution and Extended Resolution remains an open problem.

The experiment produces the first UNKNOWN verdict in the Illusion system. `variable_elimination` — randomly projecting out a fraction of proof variables — achieves Δcollapse = +0.64 to +0.78, comparable to the strongest SAFE candidates, but L3 cannot classify it: the property it induces relates to the separation between Resolution and Extended Resolution, which is not resolved in current proof complexity theory.

This result marks the transition from Illusion as a verification tool to Illusion as an exploration tool. In the three previous domains (AC⁰, monotone circuits, algebraic circuits), L3 produced no UNKNOWN verdicts because the rule library was sufficient for known domains. Here, for the first time, the system is pointing at the boundary of current mathematical knowledge.

---

## 1. Introduction

The first three Illusion experiments operated in domains where the answer was already known. In each case, L2 arrived at the key discriminating property used in the classical proof, and L3 correctly classified all candidates as SAFE or UNSAFE. The system validated the SRS framework's prediction, but it did not go beyond what was already known.

Phase 5 changes this. Resolution proof complexity is a domain where:

1. A lower bound is known: PHP_n requires exponential-width Resolution proofs (Ben-Sasson & Wigderson 2001).
2. A separation is open: whether Resolution is strictly weaker than Extended Resolution is not resolved.

The design goal is not to reproduce the Ben-Sasson-Wigderson result. It is to find a transform that has statistical signal but falls outside the current rule library — a genuine UNKNOWN. If such a transform exists and has positive Δcollapse, the system is saying: *here is a property that statistically degrades proof power, but we do not know whether it is decidable within Resolution.*

That is new information.

### 1.1 What changes in Phase 5

In previous phases, UNKNOWN was a failure mode — it meant the rule library was incomplete. In Phase 5, UNKNOWN is the primary success criterion. The L3 rule library is deliberately designed to trigger UNKNOWN on transforms that relate to open problems, rather than defaulting to SAFE or UNSAFE.

### 1.2 Relation to companion papers

This paper assumes familiarity with the Illusion three-layer architecture and the SRS framework in [Xie 2026]. All notation follows those papers.

---

## 2. Experimental Setup

**L1**: Greedy width-limited Resolution solver. Given a CNF formula and a width limit w, the solver attempts to derive the empty clause using only resolvents of width ≤ w. Success = empty clause derived; failure = search exhausted within max_steps.

**Target**: PHP_n — the pigeonhole principle with n+1 pigeons and n holes. Known to require Resolution proofs of width ≥ n (Ben-Sasson & Wigderson 2001).

**Distributions**:
- D⁺: PHP(n+1, n) with n < width_limit (e.g., PHP(3,2) and PHP(4,3)) — the solver finds proofs within the width limit
- D⁻: PHP(n+1, n) with n ≥ width_limit (e.g., PHP(6,5) and PHP(7,6)) — proofs require width ≥ n > width_limit, solver fails

The width_limit = 4 creates a clean separation: D⁺ formulas are provable within the limit, D⁻ formulas are not. The distinguishing advantage measures how reliably the solver can tell them apart.

**Collapse metric**: collapse = 1 − distinguishing_advantage, where distinguishing_advantage = |Pr[L1 succeeds | D⁺] − Pr[L1 succeeds | D⁻]|.

**Baseline**: advantage = 0.78, collapse = 0.22 (width_limit = 4, 10 formulas per distribution, 5 trials each).

**Parameters**: width_limit = 4, n_formulas = 10, n_trials = 5, seed = 42.

---

## 3. Results

### 3.1 Full results table

| Transform | Δcollapse | Target affected | L3 verdict |
|-----------|-----------|----------------|------------|
| clause_restriction_p0.2 | +0.600 | No | **SAFE** |
| clause_restriction_p0.4 | +0.780 | No | **SAFE** |
| clause_projection_p0.7 | +0.780 | No | **SAFE** |
| clause_projection_p0.8 | +0.780 | No | **SAFE** |
| variable_elimination_p0.2 | +0.640 | No | **UNKNOWN** |
| variable_elimination_p0.3 | +0.780 | No | **UNKNOWN** |
| width_truncation_k2 | −0.020 | No | rejected |
| width_truncation_k3 | −0.020 | No | rejected |
| clause_permutation | −0.020 | No | rejected |
| identity | −0.020 | No | rejected |
| literal_negation_p0.3 | — | Yes | rejected |

### 3.2 L3 verdicts for candidates

**SAFE — clause_restriction**: Randomly fixing a fraction of variables preserves the PHP unsatisfiability structure but degrades the proof system's distinguishing power. Deciding whether a proof system loses width advantage under random variable fixing requires exponential sampling over all possible restrictions. This is the Resolution analog of Håstad's random restriction and the core operation of the Ben-Sasson-Wigderson width method.

**SAFE — clause_projection**: Randomly retaining a subset of clauses preserves the core PHP axioms with high probability but removes the redundancy that enables short proofs. Deciding whether a proof system loses distinguishing advantage under random clause removal requires exponential search over all possible projections.

**UNKNOWN — variable_elimination**: Randomly projecting out a fraction of proof variables corresponds to existential quantification — the operation that defines Extended Resolution. The separation between Resolution and Extended Resolution is an open problem in proof complexity. L3 cannot determine whether the property induced by variable elimination is decidable within Resolution.

---

## 4. The UNKNOWN Result

### 4.1 What UNKNOWN means here

`variable_elimination_p0.3` achieves Δcollapse = +0.78 — identical to the strongest SAFE candidates. By L2's statistical criterion alone, it is indistinguishable from `clause_restriction_p0.4` or `clause_projection_p0.7`.

L3 distinguishes them not by signal strength but by the nature of the induced property:

| Transform | Δcollapse | L3 verdict | Why |
|-----------|-----------|------------|-----|
| clause_restriction_p0.4 | +0.780 | SAFE | Deciding collapse under restriction requires exponential sampling |
| clause_projection_p0.8 | +0.780 | SAFE | Deciding collapse under projection requires exponential search |
| variable_elimination_p0.3 | +0.780 | **UNKNOWN** | Decidability within Resolution is an open problem |

The UNKNOWN verdict is not a failure of the rule library. It is a precise statement: the system has found a transform with strong statistical signal whose logical status cannot be determined from current proof complexity theory.

### 4.2 Connection to Extended Resolution

Extended Resolution (Cook & Reckhow 1979) extends Resolution by allowing the introduction of new variables as abbreviations for subformulas. It is known to be at least as powerful as Resolution, and conjectured to be strictly more powerful — but no separation has been proved.

`variable_elimination` is the inverse operation: it removes variables by existential projection. If Extended Resolution is strictly more powerful than Resolution, then variable elimination should degrade proof power in a way that is not decidable within Resolution — which is exactly what the UNKNOWN verdict captures.

The system is not claiming that variable elimination proves the separation. It is saying: *this transform has the statistical signature of a discriminating property, and its logical status is exactly the open question.*

### 4.3 Comparison with previous UNSAFE false positives

In Phase 3 and Phase 4d, L3 identified UNSAFE candidates with strong statistical signal (`edge_deletion_p0.1`, `field_reduction_q2`). Those were local operations — decidable within the model. The UNKNOWN here is structurally different: it is not a local operation, and its decidability is genuinely unknown.

| Domain | False positive | Δ | Why UNSAFE |
|--------|---------------|---|------------|
| Monotone | edge_deletion_p0.1 | +0.081 | Local edge zeroing, poly-time decidable |
| Algebraic | field_reduction_q2 | +0.105 | Local mod-q operation, poly-time decidable |
| **Resolution** | **variable_elimination_p0.3** | **+0.780** | **Not local — relates to open problem** |

The UNKNOWN is not a stronger false positive. It is a different category entirely.

---

## 5. Limitations

**1. Scale.** Experiments use PHP(3,2) through PHP(7,6). The distinguishing advantage at baseline is 0.78, not 1.0, because the greedy solver occasionally fails on D⁺ formulas. Larger experiments would sharpen the signal.

**2. Greedy solver approximation.** The L1 solver is a greedy width-limited Resolution procedure, not a complete solver. It may fail to find proofs that exist within the width limit. This introduces noise into the collapse metric but does not affect the direction of the results.

**3. UNKNOWN is not a proof.** The UNKNOWN verdict on `variable_elimination` does not prove that variable elimination is a valid discriminating property for the Resolution/Extended Resolution separation. It identifies a candidate that warrants further investigation.

**4. Single experiment.** Phase 5 reports one experiment (seed=42). The results should be replicated with different seeds and larger formula sets before drawing strong conclusions.

---

## 6. Conclusion

Phase 5 produces the first UNKNOWN verdict in the Illusion system. `variable_elimination` achieves Δcollapse = +0.64 to +0.78 — strong statistical signal — but L3 cannot classify it because its logical status is an open problem in proof complexity.

This is the transition the system was designed for. In known domains, Illusion verifies that the SRS framework correctly identifies discriminating properties. In unknown domains, it points at the boundary of current knowledge. The UNKNOWN verdict is not a failure — it is the system doing exactly what Phase 5 asked it to do.

The natural next step is to investigate `variable_elimination` more carefully: does it preserve PHP unsatisfiability? Does its signal strengthen with n? Does it correspond to a known open question in a precise formal sense? These are questions for human mathematicians, not for the search system. Illusion has done its part: it found the candidate and flagged the boundary.

---

## References

Xie, J. (2026). *A Unified Theory of Impossibility Proofs: The SRS Program*. ResearchGate preprint, April 2026. DOI: 10.13140/RG.2.2.25731.26406

Ben-Sasson, E., & Wigderson, A. (2001). Short proofs are narrow — resolution made simple. *Journal of the ACM*, 48(2), 149–169.

Cook, S. A., & Reckhow, R. A. (1979). The relative efficiency of propositional proof systems. *Journal of Symbolic Logic*, 44(1), 36–50.

Krajíček, J. (1995). *Bounded Arithmetic, Propositional Logic, and Complexity Theory*. Cambridge University Press.

Håstad, J. (1987). Computational limitations of small-depth circuits. MIT Press.

Razborov, A. A. (1985). Lower bounds on the monotone complexity of some Boolean functions. *Doklady Mathematics*, 31, 354–357.

Smolensky, R. (1987). Algebraic methods in the theory of lower bounds for Boolean circuit complexity. *STOC 1987*, 77–82.
