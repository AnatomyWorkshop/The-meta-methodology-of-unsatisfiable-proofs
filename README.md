# Apophenia

**Separating signal from noise.**

Tools that determine whether a structural pattern is real or an artifact, built on the Universal Closure Axiom (UCA).

---

## Products

### Illusion — Structural diagnosis for open problems

```bash
pip install -e illusion/
illusion demo          # runs in 5 seconds
illusion list          # show 6 validated domains
illusion diagnose rh   # diagnose Riemann Hypothesis
```

Classifies mathematical domains as SAFE (proof path exists) or UNKNOWN (structural gap). Validated across 6 domains — returns SAFE on solved problems, UNKNOWN on open ones.

| Domain | Status | Result |
|--------|--------|--------|
| AC0 Circuit Complexity | SAFE | Rediscovered Hastad's switching lemma |
| Monotone Circuits | SAFE | Rediscovered Razborov's approximation |
| Algebraic Circuits | SAFE | Partial derivatives method confirmed |
| Resolution Proofs | SAFE | Width-size relationship confirmed |
| Frege Systems | SAFE | Bounded-depth lower bounds confirmed |
| Riemann Hypothesis | UNKNOWN | Structural gap in Hilbert-Polya identified |

### Prism — Spectral constraint analysis for networks

```bash
pip install -e prism/
prism demo             # Karate Club graph in 0.08s
prism analyze graph.edgelist
prism check matrix.npy
```

Computes how much a network's eigenvalue structure must shift to satisfy UCA duality self-consistency. Symmetric structures pass (defect = 0); asymmetric networks show measurable duality gaps.

### Meta-Dispatch — AI model orchestration

```bash
cd meta-dispatch
python router.py "your task here" --type judgment
python router.py --batch
```

Routes research tasks to optimal AI models with adversarial iteration, cost tracking, fallback routing, and structured trace logging.

---

## Research

**Universal Closure Axiom:** `D · phi = star · D† · star · phi`

A system's internal evolution must equal its image under duality-conjugated constraint.

- Paper 1: UCA + Classical Physics (DOI: 10.13140/RG.2.2.11627.91685)
- Paper 4: UCA + Riemann Hypothesis
- Paper 5: UCA + BSD Conjecture

All papers on [ResearchGate](https://www.researchgate.net/).

---

## Structure

```
illusion/           Proof barrier diagnosis (CLI + experiments)
prism/              Network spectral constraint analysis (CLI)
meta-dispatch/      AI model router + adversarial iteration
papers/             Published research (UCA series)
```

Each product has its own README:
- [illusion/](illusion/) — install, commands, domain list
- [prism/](prism/) — install, usage, algorithm, applications
- [meta-dispatch/](meta-dispatch/) — routing, @op protocol, adversarial iteration

Note: `docs/`, `archive/`, and experiment results are excluded from ZIP downloads. Clone the repo for full access.

---

## Website

[anatomyworkshop.github.io/apophenia](https://anatomyworkshop.github.io/apophenia/)

## License

MIT
