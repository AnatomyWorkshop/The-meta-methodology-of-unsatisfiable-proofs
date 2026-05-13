# Apophenia — Separating Signal from Noise

A computational framework for structural diagnosis of mathematical proof barriers, spectral constraint solving, and AI-driven research automation.

---

## What This Is

One architecture (L1/L2/L3), six mathematical domains, consistent structural verdicts:

| Phase | Domain | Target | Verdict | Status |
|-------|--------|--------|---------|--------|
| 2 | AC0 circuits | PARITY lower bound | SAFE | Solved (Razborov-Smolensky 1987) |
| 3 | Monotone circuits | CLIQUE lower bound | SAFE | Solved (Razborov 1985) |
| 4 | Algebraic circuits | Permanent vs Determinant | SAFE | Solved (partial) |
| 5 | Resolution proofs | Resolution vs Extended Resolution | UNKNOWN | Open |
| 5c | Frege proofs | Frege vs Extended Frege | UNKNOWN | Open |
| 6 | Riemann Hypothesis | Hilbert-Polya operator | UNKNOWN | Open (millennium) |

The system produces SAFE on solved problems and UNKNOWN precisely at the frontier of open problems.

---

## Structure

```
├── papers/                     # Published research
│   ├── uca/                    # Universal Closure Axiom series
│   │   ├── paper1-classical-physics.md
│   │   ├── paper4-riemann-hypothesis.md
│   │   └── paper5-bsd-conjecture.md
│   ├── illusion/               # Illusion/SRS framework
│   └── cross-domain-diagnostic.md
│
├── illusion/                   # Computational system
│   ├── phase2_circuit/         # AC0 / PARITY
│   ├── phase3_monotone/        # Monotone / CLIQUE
│   ├── phase4_algebraic/       # Algebraic / PERMANENT
│   ├── phase5_resolution/      # Resolution proof complexity
│   ├── phase5b_frege/          # Frege depth
│   ├── phase5c_frege_scaling/  # Frege size
│   ├── phase6_rh/             # Riemann Hypothesis
│   ├── phase7_adelic/         # Adelic trace formula
│   ├── phase8_bsd/            # BSD conjecture
│   └── mcp/                   # MCP server integration
│
├── meta-dispatch/              # AI model router (元调度器)
│
├── archive/                    # Historical record
│   ├── responses/             # AI conversation logs
│   ├── field-notes/           # Research notes
│   ├── drafts/                # Early paper drafts
│   └── references/            # Academic papers
│
└── docs/                       # Project documentation
```

---

## Papers

**Universal Closure Axiom (UCA):**
- [Paper 1: UCA and Classical Physics](papers/uca/paper1-classical-physics.md) — One axiom derives QM, Yang-Mills, Einstein gravity
- [Paper 4: UCA and the Riemann Hypothesis](papers/uca/paper4-riemann-hypothesis.md) — RH as UCA consistency; Hilbert-Polya via adelic Vladimirov operator
- [Paper 5: UCA and the BSD Conjecture](papers/uca/paper5-bsd-conjecture.md) — BSD as UCA on GL(2); duality rigidity implies upper bound

**Illusion / SRS:**
- [Manifesto](papers/illusion/manifesto.md) — Self-referential safety framework
- [Proof Complexity](papers/illusion/proof-complexity.md) — Resolution and Frege systems
- [Cross-Domain Diagnostic](papers/cross-domain-diagnostic.md) — Unified results across six domains

---

## Key Concepts

**Self-Referential Safety (SRS)**: A model M cannot decide proposition P if the cost of deciding P exceeds M's capacity.

**Three-layer architecture**:
- L1: Domain-specific model
- L2: Search engine (finds transforms that expose structural gaps)
- L3: Classifier (SAFE / UNSAFE / UNKNOWN)

**Universal Closure Axiom**: $\mathcal{D}\phi = \star\,\mathcal{D}^\dagger\,\star\,\phi$ — self-adjointness + duality compatibility as the structural origin of fundamental equations.

---

## License

See [LICENSE](LICENSE).
