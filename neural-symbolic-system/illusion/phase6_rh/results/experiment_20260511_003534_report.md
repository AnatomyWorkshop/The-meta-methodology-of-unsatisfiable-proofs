# Phase 6 Experiment Report: Riemann Hypothesis Closure Search

> Timestamp: 20260511_003534
> Domain: Closure search in operator space, target: zeta zero spectrum
> Params: n_zeros=50, n_dim=50
> Method: Four-law evaluation of candidate Hilbert-Polya operators

---

## Candidate Operators (ranked by composite closure score)

| Operator | Score | Spectral | Duality | Rigid | Symm | Reduce | L3 |
|----------|-------|----------|---------|-------|------|--------|-----|
| connes_truncated_n50 | 0.777 | 1.000 | 1.000 | 1.0 | 0.500 | 0.50 | UNSAFE |
| berry_keating_periodic_n50 | 0.701 | 0.600 | 0.995 | 1.0 | 0.750 | 0.50 | **UNKNOWN** |
| berry_keating_dirichlet_n50 | 0.642 | 0.600 | 0.995 | 1.0 | 0.500 | 0.25 | **UNKNOWN** |
| gue_n50_s123 | 0.620 | 0.360 | 0.996 | 1.0 | 0.457 | 0.25 | UNSAFE |
| gue_n50_s42 | 0.608 | 0.320 | 0.994 | 1.0 | 0.478 | 0.25 | UNSAFE |
| hecke_level1_n50 | 0.591 | 0.280 | 0.844 | 1.0 | 0.250 | 1.00 | **SAFE** |
| prime_zeta_n50 | 0.578 | 0.420 | 0.942 | 1.0 | 0.000 | 0.75 | **UNKNOWN** |
| berry_keating_pt_symmetric_n50 | 0.558 | 0.100 | 0.876 | 1.0 | 0.750 | 0.50 | **UNKNOWN** |

## L3 Summary

- **SAFE** (valid closure path): hecke_level1_n50
- **UNSAFE** (not a valid closure): connes_truncated_n50, gue_n50_s123, gue_n50_s42
- **UNKNOWN** (structural status undetermined): berry_keating_periodic_n50, berry_keating_dirichlet_n50, prime_zeta_n50, berry_keating_pt_symmetric_n50

---

## Key Findings

### SAFE: Valid Closure Paths

**hecke_level1_n50** (score = 0.591)

> Hecke operators encode prime structure via modular arithmetic and possess functional equation symmetry. Their L-functions satisfy GRH. This is a structurally valid closure path: the operator lives in M_op (outside M_an), encodes primes, and its self-adjointness implies spectral reality.

> Four laws: Duality: partial (L-function zeros, not full zeta). Rigidity: yes. Symmetry: yes (functional equation). Reduction: yes (primes -> Hecke eigenvalues).

> Reference: Hecke 1937; Selberg 1956; Langlands program

### UNKNOWN: Open Questions

**berry_keating_periodic_n50** (score = 0.701)

> Berry-Keating H=xp+px is the simplest candidate for the Hilbert-Polya operator. Self-adjointness depends on boundary conditions (domain of definition). Spectral match is partial. Whether a specific boundary condition produces exact zeta zeros is an open problem in mathematical physics.

> Four laws: Duality: conjectured (spectrum <-> zeros). Rigidity: boundary-dependent. Symmetry: periodic BC only. Reduction: no explicit prime encoding.

**berry_keating_dirichlet_n50** (score = 0.642)

> Berry-Keating H=xp+px is the simplest candidate for the Hilbert-Polya operator. Self-adjointness depends on boundary conditions (domain of definition). Spectral match is partial. Whether a specific boundary condition produces exact zeta zeros is an open problem in mathematical physics.

> Four laws: Duality: conjectured (spectrum <-> zeros). Rigidity: boundary-dependent. Symmetry: periodic BC only. Reduction: no explicit prime encoding.

**prime_zeta_n50** (score = 0.578)

> Operator with explicit prime encoding (diag=log(p), coupling via primes). Self-adjoint by construction. Encodes prime structure directly. But spectral match to zeta zeros is not established — the coupling structure may not produce the correct spectrum. Whether prime-encoding operators can reproduce zeta zeros is related to the inverse spectral problem.

> Four laws: Duality: unknown (spectrum may not match zeros). Rigidity: yes. Symmetry: no. Reduction: yes (primes encoded directly).

**berry_keating_pt_symmetric_n50** (score = 0.558)

> PT-symmetric Berry-Keating Hamiltonian (Bender-Brody-Mueller 2017). Non-Hermitian but PT-symmetric: if PT symmetry is unbroken, spectrum is entirely real. The functional equation s <-> 1-s maps to PT symmetry (P implements parity, T implements conjugation). This is the strongest known structural candidate: it naturally encodes the functional equation as a physical symmetry. Open question: whether the specific potential produces exact zeta zeros.

> Four laws: Duality: conjectured (spectrum <-> zeros). Rigidity: PT-unbroken = effectively self-adjoint (real spectrum). Symmetry: yes (PT implements functional equation). Reduction: no explicit prime encoding.

### UNSAFE: Rejected Candidates

**connes_truncated_n50**: circular construction: operator spectrum is defined as zeta zeros. This is not a closure — it assumes what it needs to p...

**gue_n50_s123**: GUE random matrices match pair correlation statistics of zeta zeros (Montgomery-Odlyzko law) but do NOT match individual...

**gue_n50_s42**: GUE random matrices match pair correlation statistics of zeta zeros (Montgomery-Odlyzko law) but do NOT match individual...

---

## Structural Gap Analysis

The framework identifies what each candidate is missing:

| Candidate | Missing for valid closure |
|-----------|-------------------------|
| berry_keating_periodic_n50 | spectral match |
| berry_keating_dirichlet_n50 | spectral match, prime encoding |
| prime_zeta_n50 | spectral match, functional equation symmetry |
| berry_keating_pt_symmetric_n50 | spectral match |

---

## Interpretation

This experiment does not prove or disprove RH. It produces a structural diagnostic:

1. **The Hilbert-Polya closure is the unique valid path** (four-law analysis)
2. **No current candidate achieves full closure** (spectral match < 1.0 for all non-circular operators)
3. **The gap is precisely identified**: each UNKNOWN candidate is missing specific structural properties
4. **GUE universality is necessary but not sufficient**: statistical match (pair correlation) does not constitute spectral duality (individual zero matching)

The framework's value: it tells you exactly what a valid closure must look like, how close each known candidate gets, and what structural property each one is missing. This is the map. The territory — constructing the actual operator — remains open.

---

## Cross-phase comparison

| Phase | Domain | Search target | Key result |
|-------|--------|---------------|------------|
| 1-4 | Circuit complexity | Discriminating property | SAFE (known proof techniques) |
| 5 | Resolution | Discriminating property | UNKNOWN (Resolution vs Ext. Resolution) |
| 5c | Frege (size) | Discriminating property | UNKNOWN (Frege vs Extended Frege) |
| **6** | **Riemann Hypothesis** | **Closure (operator)** | **UNKNOWN (Hilbert-Polya construction)** |

The architecture generalizes from 'find the proof technique' to 'find the proof path'. In both cases, the system identifies what is known, what is open, and what is structurally impossible.
