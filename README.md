# The Meta-Methodology of Unsatisfiable Proofs

A computational framework that structurally diagnoses mathematical proof barriers — identifying which proof paths are valid, which are invalid, and which remain open — across six domains from circuit complexity to the Riemann Hypothesis.

---

## Core Result

One architecture (L1/L2/L3), six domains, consistent structural verdicts:

| Phase | Domain | Target | Verdict | Mathematical Status |
|-------|--------|--------|---------|-------------------|
| 2 | AC0 circuits | PARITY lower bound | SAFE | Solved (Razborov-Smolensky 1987) |
| 3 | Monotone circuits | CLIQUE lower bound | SAFE | Solved (Razborov 1985) |
| 4 | Algebraic circuits | Permanent vs Determinant | SAFE | Solved (partial, Shpilka 2003) |
| 5 | Resolution proofs | Resolution vs Extended Resolution | UNKNOWN | Open (Cook-Reckhow 1979) |
| 5c | Frege proofs (size) | Frege vs Extended Frege | UNKNOWN | Open (Cook-Reckhow 1979) |
| 6 | Riemann Hypothesis | Hilbert-Polya operator | UNKNOWN | Open (millennium problem) |

The system produces SAFE on solved problems and UNKNOWN precisely at the frontier of open problems. It never produces a false SAFE on an open problem.

Full diagnostic: [cross-domain-diagnostic.md](cross-domain-diagnostic.md)

---

## Structure

```
├── cross-domain-diagnostic.md          # The unified diagnostic (start here)
├── neural-symbolic-system/
│   ├── illusion/                        # The computational system
│   │   ├── phase2/                      # AC0 / PARITY
│   │   ├── phase3/                      # Monotone / CLIQUE
│   │   ├── phase4/                      # Algebraic / PERMANENT
│   │   ├── phase5/                      # Resolution proof complexity
│   │   ├── phase5b/                     # Frege depth complexity
│   │   ├── phase5c/                     # Frege size complexity
│   │   ├── phase6_rh/                   # Riemann Hypothesis closure search
│   │   └── papers/                      # Technical papers
│   ├── closure-axiom-derivations/       # Formal derivations
│   └── inspiration/                     # Field notes and working notes
├── inspiration/                         # Thinking process and drafts
└── LICENSE
```

---

## Papers

**Illusion / SRS framework:**
- [Manifesto](neural-symbolic-system/illusion/papers/manifesto.md) — The self-referential safety framework
- [Proof Complexity](neural-symbolic-system/illusion/papers/illusion-proof-complexity.md) — Resolution and Frege systems
- [Symbol System](neural-symbolic-system/illusion/papers/illusion-symbol-system.md) — Formal specification
- [Constructive Verification](neural-symbolic-system/illusion/papers/illusion-constructive-verification.md) — Experimental validation

**Universal Closure Axiom (UCA):**
- [Paper 1: UCA and Classical Physics](neural-symbolic-system/closure-axiom-derivations/papers/paper1-universal-closure-axiom.md) — One axiom derives QM, Yang-Mills, Einstein gravity
- [Paper 4: RH as a UCA Consistency Condition](neural-symbolic-system/closure-axiom-derivations/papers/paper4-uca-riemann-hypothesis.md) — RH ↔ zeta function satisfies UCA; Berry-Keating as classical limit

---

## Key Concepts

**Self-Referential Safety (SRS)**: A model M cannot decide proposition P if the cost of deciding P exceeds M's capacity. The ratio alpha = cost/capacity determines decidability.

**Three-layer architecture**:
- L1: Domain-specific model (neural classifier, proof evaluator, spectral analyzer)
- L2: Search engine (finds transforms/operators that expose structural gaps)
- L3: Classifier (SAFE / UNSAFE / UNKNOWN based on structural analysis)

**Four closure laws** (for millennium problems):
1. Duality — bijection between two mathematical domains
2. Rigidity — no free parameters (self-adjointness, modularity)
3. Explicit symmetry — hidden symmetry made manifest
4. Dimension reduction — infinite complexity compressed to finite invariant

---

## Current State

Phase 6 (Riemann Hypothesis) identifies the PT-symmetric Berry-Keating Hamiltonian as the structurally strongest candidate for the Hilbert-Polya operator. Gap: spectral match (the specific potential function that produces zeta zeros from a PT-symmetric Hamiltonian is unknown). Active work: inverse spectral optimization.

---

## Thinking Process

The `inspiration/` directories contain the full intellectual trajectory — from initial intuitions through failed attempts to current results. They are preserved intentionally as part of the scientific record.
