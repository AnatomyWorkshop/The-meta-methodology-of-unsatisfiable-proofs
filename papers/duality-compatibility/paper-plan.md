# Paper Plan: Duality Compatibility

> Last updated: 2026-05-18
> Position: Independent of the Illusion/SRS program. Differential geometry / mathematical physics.
> Language: English
> Venue: ResearchGate preprint (short note)
> Former name: Universal Closure Axiom — renamed for accuracy

---

## The Condition

$$[\nabla, \star] = 0$$

Duality compatibility: the covariant derivative commutes with the Hodge star.

---

## Core Theorem (the only rigorous result)

**Theorem**: On a pseudo-Riemannian manifold $(M, g)$ with connection $\nabla$:

$$[\nabla, \star] = 0 \iff \nabla g = 0$$

Duality compatibility is equivalent to metric compatibility. This uniquely selects the Levi-Civita connection (given torsion-free assumption).

---

## What this theorem does NOT do

The following claims appeared in earlier drafts and are **logically flawed** (per multiple independent reviews):

| Claim | Problem | Status |
|-------|---------|--------|
| "Derives quantum mechanics" | Self-adjointness ≠ QM; ★=id limit doesn't exist for forms | **Deleted** |
| "Derives Maxwell/Yang-Mills" | Shows consistency, not derivation; no selection principle | **Deleted** |
| "Uniquely derives Einstein gravity" | Requires additional "pure metric" assumption (Brans-Dicke satisfies ∇g=0 too) | **Weakened to: derives Einstein under pure-metric assumption** |

---

## Revised Paper Structure (short note, ~6 pages)

1. **Setup**: Metric manifold, Hodge star, connection, formal adjoint
2. **Theorem**: [∇,★]=0 ⟺ ∇g=0, with proof
3. **Consequence**: Under pure-metric assumption + Lovelock theorem → Einstein equations in 4D
4. **Discussion**: Structural correspondence (not derivation) with gauge field formalism; analogy with QM self-adjointness

---

## Paper Series Status (revised)

| Paper | Title | Status | Action |
|-------|-------|--------|--------|
| 1 | DC + Classical Physics (`dc-classical-physics.md`) | Published (RG, DOI: 10.13140/RG.2.2.11627.91685) | Needs erratum or replacement |
| 4 | DC + Riemann Hypothesis (`dc-riemann-hypothesis.md`) | Content complete | On hold — circular (per claude2 review) |
| 5 | DC + BSD Conjecture (`dc-bsd-conjecture.md`) | Draft complete | On hold — rank ≥ 2 problem remains open |

Papers 2 and 3 (quantum gravity, predictions) are **cancelled** — they depended on claims now known to be unsupported.

---

## Honest Assessment

The core theorem is real and publishable as a short differential geometry note. Everything else built on top of it (QM, gauge fields, quantum gravity, particle predictions) was overreach. The theorem says: "if you want Hodge duality to commute with parallel transport, you must have metric compatibility." That's clean, non-trivial, and useful. It's not a theory of everything.

The RH and BSD connections (Papers 4, 5) reframe known spectral problems in duality-compatibility language. The reframing is suggestive but does not constitute progress toward proofs. These are on hold until the core note is published and the framing is validated by peer response.
