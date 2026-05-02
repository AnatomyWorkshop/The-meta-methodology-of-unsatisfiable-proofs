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

---

*Entries below this line are from Phase 2 and later.*

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

