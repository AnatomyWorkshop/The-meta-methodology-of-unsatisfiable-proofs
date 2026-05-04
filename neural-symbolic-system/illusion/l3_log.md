# L3 Log — Self-Referential Safety Decisions

> This is the living record of L3 judgments in the Illusion system.
> Each entry records: when, what candidate, what the AI diagnosed, what the human decided, and (later) whether the decision held up.
>
> Format: one entry per candidate, per session. Entries are append-only.
> Human overrides are marked explicitly. Stale entries are never deleted — they are annotated.

---

## How to read this log

| Field | Meaning |
|---|---|
| **Verdict** | AI's rule-based judgment: SAFE / UNSAFE / UNKNOWN |
| **Reason** | Why the AI reached that verdict |
| **Reference** | Known theorem or result that grounds the judgment |
| **Human override** | If the human disagreed, what they said and why |
| **Verification** | Later: did the judgment hold up? |

---

## How to add an entry (for AI)

When L2 produces a new candidate, run:

```bash
python phase1/l3_monitor.py <transform_name>
# or for batch:
python phase1/l3_monitor.py --batch phase1/results/<experiment>.json
```

Then paste the output here and add the **Human decision** line.

---

## Phase 1 Entries

## 2026-05-02 | random_restriction_p0.3

- **Verdict**: SAFE (high confidence)
- **Reason**: deciding whether a circuit collapses under random restriction requires computing E[collapse] over exp(n) restrictions; this exceeds AC^0 capability
- **Reference**: Håstad 1986, Switching Lemma
- **Collapse score**: 0.948
- **PARITY affected**: No
- **Human decision**: SAFE — confirmed. The expectation ranges over $\binom{n}{\lfloor pn \rfloor} \cdot 2^{(1-p)n}$ restrictions, a quantity that grows faster than any polynomial. No AC^0 circuit can compute this.
- **Verification**: Matches Håstad's original method. This IS the Switching Lemma property.

---

## 2026-05-02 | random_restriction_p0.5

- **Verdict**: SAFE (high confidence)
- **Reason**: same as p=0.3 — exponential enumeration required
- **Reference**: Håstad 1986, Switching Lemma
- **Collapse score**: 0.905
- **PARITY affected**: No
- **Human decision**: SAFE — confirmed. Same structural argument as p=0.3.
- **Verification**: Consistent with p=0.3 result. Collapse score slightly lower (fewer inputs fixed), as expected.

---

## 2026-05-02 | random_restriction_p0.7

- **Verdict**: SAFE (high confidence)
- **Reason**: same as p=0.3 — exponential enumeration required
- **Reference**: Håstad 1986, Switching Lemma
- **Collapse score**: 0.834
- **PARITY affected**: No
- **Human decision**: SAFE — confirmed.
- **Verification**: Collapse score lower than p=0.3 (more inputs fixed → less randomness → weaker collapse signal), but still above threshold.

---

## 2026-05-02 | input_permutation

- **Verdict**: UNSAFE (high confidence)
- **Reason**: permutation invariance is decidable in polynomial time (check all n! input permutations; for fixed n this is O(1))
- **Reference**: —
- **Collapse score**: 0.835
- **PARITY affected**: No
- **Human decision**: UNSAFE — confirmed. Deciding "is this function symmetric under all input permutations?" can be done by evaluating the function on all n! permutations of any input, which is polynomial time for fixed n. This is a false positive: high collapse score but not self-referentially safe.
- **Verification**: Correct rejection. This is the canonical false positive for Phase 1 — high collapse, wrong reason.

---

## 2026-05-02 | gate_substitution

- **Verdict**: UNSAFE (high confidence)
- **Reason**: gate substitution is a local rewrite; deciding whether a circuit admits a gate substitution is decidable in AC^0
- **Reference**: —
- **Collapse score**: 0.998
- **PARITY affected**: Yes
- **Human decision**: Rejected by L2 (PARITY affected) before reaching L3. L3 verdict recorded for completeness: UNSAFE.
- **Verification**: Correctly rejected at L2 stage. L3 agreement: also unsafe.

---

## 2026-05-02 | depth_reduction

- **Verdict**: UNSAFE (high confidence)
- **Reason**: depth reduction is a structural circuit transformation; deciding whether a circuit has depth ≤ d is decidable in AC^0
- **Reference**: —
- **Collapse score**: 0.784
- **PARITY affected**: Yes
- **Human decision**: Rejected by L2 (PARITY affected) before reaching L3. L3 verdict recorded for completeness: UNSAFE.
- **Verification**: Correctly rejected at L2 stage.

---

## Phase 1 Summary

| Candidate | L3 Verdict | Human Decision | Match? |
|---|---|---|---|
| random_restriction (p=0.3) | SAFE | SAFE | ✓ |
| random_restriction (p=0.5) | SAFE | SAFE | ✓ |
| random_restriction (p=0.7) | SAFE | SAFE | ✓ |
| input_permutation | UNSAFE | UNSAFE | ✓ |
| gate_substitution | UNSAFE | UNSAFE (also L2-rejected) | ✓ |
| depth_reduction | UNSAFE | UNSAFE (also L2-rejected) | ✓ |

**AI accuracy on Phase 1**: 6/6 correct. All verdicts matched human judgment.

**What this means**: The rule-based L3 correctly distinguishes Håstad's method (exponential enumeration, SAFE) from structural/symmetry properties (polynomial-time decidable, UNSAFE). Phase 1 L3 automation is validated on the known cases.

## 2026-05-04 | identity (baseline calibration)

- **Verdict**: UNSAFE (high confidence, after rule update)
- **Reason**: the identity transform induces no property at all; collapse score reflects measurement baseline (~0.889), not structural collapse; trivially decidable in AC^0
- **Collapse score**: 0.889
- **PARITY affected**: No
- **Design intent**: Control transform to calibrate the collapse score zero-point
- **Key finding**: identity collapse = 0.889, nearly identical to input_permutation (0.892) and input_negation (0.888). This confirms that the collapse score has a high baseline (~0.89) due to the output distribution of random AC^0 circuits. "What does nothing" scores almost as high as "what permutes inputs."
- **Human decision**: UNSAFE — confirmed. The collapse is entirely a measurement artifact. This invalidates the interpretation of input_permutation's 0.892 as "somewhat high" — it is exactly at baseline.
- **Implication for threshold**: The 0.15 threshold filters only near-zero collapse. The meaningful signal is collapse *above* the ~0.89 baseline. random_restriction (0.879–0.969) is at or above baseline; its signal comes from the structural collapse mechanism, not from the baseline itself.

---

## 2026-05-04 | input_negation (baseline calibration)

- **Verdict**: UNSAFE (high confidence)
- **Reason**: negating inputs is a complexity-preserving relabeling; collapse reflects baseline artifact, not structural weakness; decidable in polynomial time
- **Collapse score**: 0.888
- **PARITY affected**: No
- **Design intent**: Verify that complexity-preserving relabeling produces collapse near identity baseline
- **Key finding**: input_negation collapse = 0.888 ≈ identity (0.889). Confirmed: relabeling inputs does not change computational complexity, and collapse score correctly reflects this by staying at baseline.
- **Human decision**: UNSAFE — confirmed. Same reasoning as identity.

---

## Phase 2 Baseline Summary (2026-05-04)

| Transform | Collapse | Interpretation |
|---|---|---|
| identity | 0.889 | **Baseline** — measurement artifact |
| input_negation | 0.888 | At baseline — complexity-preserving |
| input_permutation | 0.892 | At baseline — complexity-preserving (false positive confirmed) |
| random_restriction (p=0.7) | 0.879 | Near baseline — weakest structural signal |
| random_restriction (p=0.3) | 0.940–0.969 | Above baseline — genuine structural collapse |
| exhaustive_parity_equivalent | 1.000 | Far above baseline — but brute-force, not structural |

**Conclusion**: The collapse score baseline is ~0.889, not 0. The threshold 0.15 is not calibrated to this baseline. Phase 2 next step: implement Δcollapse = collapse_after - collapse_before to measure structural change relative to each circuit's own baseline.

---


---

## Phase 2 Pressure Tests

## 2026-05-02 | exhaustive_parity_equivalent_check

- **Verdict**: UNSAFE (high confidence)
- **Reason**: deciding PARITY-equivalence requires enumerating all 2^n inputs, but this is brute-force detection, not structural insight; exponential enumeration alone is not sufficient for self-referential safety
- **Reference**: —
- **Design intent**: This transform was designed to reach L3 (unlike the earlier ExhaustiveConstantCheck which was filtered by L2). It tests whether L3 conflates "requires exponential resources" with "self-referentially safe".
- **Expected behavior**: L2 passes it (affects_parity=False, high collapse). L3 should mark UNSAFE.
- **Human decision**: UNSAFE — confirmed. The key distinction: a self-referentially safe property must reveal WHY AC^0 circuits fail structurally, not merely detect that they fail. Exhaustive PARITY-equivalence checking is brute-force detection. It has no structural content.
- **What this test proves**: The rule "exponential enumeration → SAFE" is wrong. L3's rule library correctly encodes the stronger condition: the property must be structurally revealing, not just computationally expensive to decide.

---


## Phase 2 UNKNOWN Learning Loop Validation (2026-05-04)

## 2026-05-04 | fourier_concentration (learning loop test)

- **Verdict**: UNKNOWN → learned SAFE (medium confidence)
- **Reason**: deciding whether Fourier mass concentrates on low-degree coefficients requires computing exponentially many Fourier coefficients; exceeds AC^0
- **Reference**: Linial-Mansour-Nisan 1993
- **Design intent**: Test the UNKNOWN learning loop. This transform name is not in the builtin rule library.
- **Process**: L3 returned UNKNOWN → human provided SAFE + reason → system extracted keywords [fourier, concentration, ...] → generated pattern → persisted to learned_rules.json → re-check returned SAFE (medium confidence)
- **Generalization test**: `fourier_weight_analysis` (different name, same domain) → SAFE via learned "fourier" keyword
- **Human decision**: SAFE — confirmed. Fourier concentration is a structural property that requires exponential computation to decide.

---

## 2026-05-04 | threshold_check (learning loop test)

- **Verdict**: UNKNOWN → learned UNSAFE (medium confidence)
- **Reason**: threshold functions are decidable in AC^0 by evaluating the weighted sum of inputs against a constant
- **Reference**: —
- **Design intent**: Test UNSAFE learning path.
- **Process**: L3 returned UNKNOWN → human provided UNSAFE + reason → system learned → re-check returned UNSAFE (medium confidence)
- **Human decision**: UNSAFE — confirmed.

---

## UNKNOWN Learning Loop Summary (2026-05-04)

| Test | Initial | After learning | Generalization |
|---|---|---|---|
| fourier_concentration | UNKNOWN | SAFE (medium) | fourier_weight_analysis → SAFE |
| threshold_check | UNKNOWN | UNSAFE (medium) | — |

**Conclusion**: The learning loop works. It can learn both SAFE and UNSAFE rules from human feedback, persist them, and generalize to similar transform names via keyword matching. Learned rules fire at medium confidence (vs high for builtins), making provenance visible.

**Note**: Test learned rules were cleaned up after validation. The learned_rules.json file starts empty for real experiments.

---

## Phase 2 Δcollapse Implementation (2026-05-04)

### Metric upgrade: absolute collapse → Δcollapse

**Problem**: Absolute collapse score has a ~0.889 baseline due to random AC⁰ circuit output distribution (OR output gate biases toward True). This made `input_permutation` (0.892) look like a candidate when it was at baseline.

**Solution**: Δcollapse = collapse_after - collapse_before, measured per circuit. Threshold: 0.03 (calibrated against identity Δ ≈ 0.005).

### Verification results (n=8, depth=3, seed=42)

| Transform | Before | After | Δ | Status |
|---|---|---|---|---|
| random_restriction (p=0.3) | 0.889 | 0.969 | **+0.080** | CANDIDATE → L3 SAFE |
| random_restriction (p=0.5) | 0.887 | 0.945 | **+0.058** | CANDIDATE → L3 SAFE |
| random_restriction (p=0.7) | 0.894 | 0.901 | +0.007 | rejected (new finding) |
| exhaustive_parity_equivalent | 0.885 | 1.000 | **+0.115** | CANDIDATE → L3 UNSAFE |
| input_permutation | 0.885 | 0.883 | -0.002 | rejected |
| identity | 0.886 | 0.891 | +0.005 | rejected |
| input_negation | 0.880 | 0.889 | +0.008 | rejected |
| gate_substitution (AND→OR) | 0.880 | 0.993 | +0.113 | rejected (PARITY) |
| gate_substitution (OR→AND) | 0.892 | 0.991 | +0.100 | rejected (PARITY) |
| depth_reduction | 0.888 | 0.755 | -0.133 | rejected (PARITY) |

### Key findings

1. **All known false positives corrected**: input_permutation (Δ=-0.002), identity (Δ=+0.005), input_negation (Δ=+0.008) all below 0.03 threshold
2. **New finding**: random_restriction p=0.7 (Δ=+0.007) is now correctly rejected — the restriction is too weak to produce meaningful structural collapse. Under the old metric (absolute collapse 0.901 > 0.15) it was incorrectly accepted.
3. **Pressure test still passes**: exhaustive_parity_equivalent (Δ=+0.115) reaches L3, correctly marked UNSAFE
4. **Human decision**: Δcollapse is the correct primary metric. Absolute collapse is retained as backward-compatible alias but no longer used for candidacy.

---

## Phase 3 Entries — Monotone Circuits (2026-05-04)

### Domain change

Phase 3 switches from AC⁰ to monotone circuits. The L3 question changes from "Can an AC⁰ circuit decide property P?" to "Can a polynomial-size monotone circuit decide property P?" Collapse metric reinterpreted as 1 - distinguishing_advantage(D⁺, D⁻).

## 2026-05-04 | subgraph_projection_p0.7

- **Verdict**: SAFE (high confidence)
- **Reason**: moderate subgraph projection preserves the target function but degrades circuit distinguishing power; deciding whether a circuit loses distinguishing advantage under random vertex removal requires exponential sampling
- **Reference**: Razborov 1985, monotone circuit lower bounds
- **Δcollapse**: +0.245 (before=0.669, after=0.914)
- **Clique affected**: No
- **Human decision**: SAFE — confirmed. 随机子图投影的结构性坍缩无法被多项式规模单调电路判定：评估区分优势需要对指数数量的随机子图采样，单调电路无概率采样的计算能力。Δcollapse 反映真实结构信号，无假阳性风险。（判定来源：人类 + Deepseek/Doubao 交叉验证）
- **Verification**: 匹配 Razborov 1985 单调电路下界的延伸逻辑。Phase 1 找到 Hastad 的随机限制，Phase 3 找到 Razborov 的子图投影——两个不同证明技术，同一框架发现。
- **Interpretation**: This is the Razborov-adjacent finding. Restricting to a random vertex subset (70% survival) preserves the k-clique structure but degrades the circuit's ability to distinguish D⁺ from D⁻. The induced property — "circuit loses distinguishing power under random subgraph projection" — requires evaluating the circuit on exponentially many random subgraphs, which no polynomial-size monotone circuit can do.

---

## 2026-05-04 | edge_deletion_p0.1

- **Verdict**: UNSAFE (high confidence)
- **Reason**: setting inputs to 0 in a monotone circuit is a monotone operation; deciding whether a circuit collapses under edge deletion is decidable by a monotone circuit of polynomial size
- **Δcollapse**: +0.081 (before=0.674, after=0.755)
- **Clique affected**: No
- **Human decision**: UNSAFE — confirmed. 边删除是单调操作，多项式规模单调电路可通过硬连线置 0 对应输入直接模拟，进而判定"电路是否在边删除下坍缩"。Δcollapse 为正仅反映局部效应，非自指安全的结构信号。与 Phase 1 的 input_permutation 逻辑一致：高坍缩分数但 UNSAFE。（判定来源：人类 + Deepseek/Doubao 交叉验证）
- **Verification**: 正确判定。边删除始终是单调操作，无论删除率高低，可判定性不变。
- **Interpretation**: Edge deletion at low rates (p=0.1) passes L2 (doesn't destroy clique, has positive delta) but is correctly caught by L3. Setting inputs to 0 is itself a monotone operation — a monotone circuit can simulate "evaluate C with some inputs zeroed" by hardwiring those inputs. The induced property is decidable within the model class.

---

## 2026-05-04 | distribution_switch

- **Verdict**: N/A (rejected by L2)
- **Δcollapse**: +0.004
- **Clique affected**: No
- **Interpretation**: The "pure" distribution switch — evaluating the same circuit on D⁺ vs D⁻ without modifying it — produces near-zero delta. This is correct: the before and after measurements use the same circuit, so the delta reflects only sampling noise. The real Razborov insight is captured by transforms that modify the input space (subgraph_projection), not by changing the evaluation distribution alone.

---

## Phase 3 Summary

| Candidate | Δcollapse | L3 Verdict | Interpretation |
|---|---|---|---|
| subgraph_projection_p0.7 | +0.245 | SAFE | Razborov-adjacent: random vertex restriction |
| edge_deletion_p0.1 | +0.081 | UNSAFE | Monotone operation, decidable |

**Rejected by L2** (7 transforms):
- edge_deletion_p0.3/0.5, subgraph_projection_p0.5: clique affected
- gate_elevation: clique affected
- distribution_switch: low delta (+0.004)
- identity: low delta (-0.002)
- edge_permutation: low delta (-0.015)

**Architecture validation**: The same three-layer architecture, with only L1 and the transform library replaced, correctly identifies a Razborov-adjacent method in the monotone circuit domain. This is the first cross-domain validation of the Illusion framework.

---