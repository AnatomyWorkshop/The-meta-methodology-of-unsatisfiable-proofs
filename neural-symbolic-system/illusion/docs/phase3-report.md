# Phase 3 Report — Monotone Circuit Extension

**Date**: 2026-05-04
**Status**: Complete

---

## Goal

Validate the Illusion framework's generalization: apply the same three-layer architecture to monotone circuits (AND/OR only, no NOT) with k-CLIQUE as the target function. If L2 discovers a Razborov-adjacent discriminating property using only domain-specific L1 and transforms, the framework's cross-domain capability is confirmed.

## Domain

| | Phase 1 (AC⁰) | Phase 3 (Monotone) |
|---|---|---|
| L1 model | AC⁰ circuits (AND/OR/NOT, constant depth) | Monotone circuits (AND/OR only) |
| Target function | PARITY | k-CLIQUE |
| Known proof technique | Random restriction (Hastad 1986) | Approximation method (Razborov 1985) |
| Collapse metric | 1 - (output variance / 0.25) | 1 - distinguishing_advantage(D⁺, D⁻) |
| Key transform | RandomRestriction | SubgraphProjection |

## Architecture

**Unchanged**: L2 search loop structure, L3 monitor core, Δcollapse threshold (0.03), UNKNOWN learning loop.

**New files** (all in `phase3/`):
- `l1_monotone.py` — MonotoneCircuit simulator, k-CLIQUE target, random generator
- `distributions.py` — D⁺ (planted clique) and D⁻ ((k-1)-partite) samplers
- `evaluator_monotone.py` — distinguishing_advantage(), measure_collapse_monotone()
- `transforms.py` — 9 transforms: DistributionSwitch, EdgeDeletion (3 rates), SubgraphProjection (2 rates), GateElevation, Identity, EdgePermutation
- `l2_search_monotone.py` — Search loop with distribution-based collapse
- `l3_rules_monotone.py` — Monotone-specific SAFE/UNSAFE patterns, injected at runtime
- `run_experiment.py` — Experiment runner with L2 + L3 pipeline

## Experiment Parameters

n=6 vertices (15 edge-inputs), k=3 (triangle), depth=3, 30 circuits, 500 samples, seed=42.

## Results

### L2 Search (9 transforms)

| Transform | Before | After | Δcollapse | Clique Affected | L2 Status |
|---|---|---|---|---|---|
| subgraph_projection_p0.7 | 0.669 | 0.914 | **+0.245** | No | CANDIDATE |
| edge_deletion_p0.1 | 0.674 | 0.755 | **+0.081** | No | CANDIDATE |
| edge_deletion_p0.3 | 0.671 | 0.887 | +0.216 | Yes | rejected |
| edge_deletion_p0.5 | 0.667 | 0.958 | +0.291 | Yes | rejected |
| subgraph_projection_p0.5 | 0.667 | 0.995 | +0.328 | Yes | rejected |
| gate_elevation | 0.661 | 0.792 | +0.131 | Yes | rejected |
| distribution_switch | 0.668 | 0.671 | +0.004 | No | rejected |
| identity | 0.670 | 0.668 | -0.002 | No | rejected |
| edge_permutation | 0.672 | 0.657 | -0.015 | No | rejected |

### L3 Verdicts

| Candidate | L3 Verdict | Confidence | Reason |
|---|---|---|---|
| subgraph_projection_p0.7 | **SAFE** | high | Deciding whether a circuit loses distinguishing advantage under random vertex removal requires exponential sampling |
| edge_deletion_p0.1 | **UNSAFE** | high | Setting inputs to 0 is a monotone operation; decidable by a monotone circuit |

### Final: 1 SAFE candidate out of 9 transforms

**`subgraph_projection_p0.7`** is the Razborov-adjacent finding. It restricts the graph to a random 70% vertex subset, preserving k-clique structure but degrading the circuit's ability to distinguish D⁺ from D⁻.

## Key Findings

1. **Cross-domain validation succeeded**: The same architecture found a structurally correct discriminating property in a completely different proof domain. Phase 1 found random restriction (Hastad); Phase 3 found subgraph projection (Razborov-adjacent). Different proof techniques, same search framework.

2. **L3 false positive caught**: `edge_deletion_p0.1` passed L2 (positive delta, doesn't destroy clique) but was correctly rejected by L3 as UNSAFE. This mirrors Phase 1's `input_permutation` — high collapse, wrong reason.

3. **distribution_switch correctly rejected by L2**: The "pure" distribution switch (evaluate same circuit on D⁺ vs D⁻) produces Δ=+0.004. The real signal comes from transforms that modify the input space, not from changing the evaluation distribution.

4. **Controls work**: identity (Δ=-0.002) and edge_permutation (Δ=-0.015) correctly rejected. k-CLIQUE is permutation-invariant, so vertex relabeling doesn't change collapse — confirmed.

5. **SubgraphProjection threshold matters**: p=0.7 (SAFE, Δ=+0.245) vs p=0.5 (rejected, clique affected). The boundary between "preserves target" and "destroys target" is sharp and correctly detected by `affects_clique()`.

## What This Means for the Framework

Phase 1 proved the architecture works on one domain. Phase 3 proves it generalizes. The core claim is now:

> The same three-layer search architecture, with only L1 and the transform library replaced, can discover domain-appropriate discriminating properties across structurally different proof domains.

This is no longer a single-domain toy. It is a validated cross-domain prototype.

---

## Scaling Check: n=8 (supplementary, 2026-05-04)

Parameters: n=8, k=3, depth=3, 20 circuits, 300 samples, seed=42.

| Transform | Δcollapse (n=6) | Δcollapse (n=8) | Trend |
|---|---|---|---|
| subgraph_projection_p0.7 | +0.245 | **+0.305** | signal strengthens |
| subgraph_projection_p0.5 | rejected (clique) | **+0.347** | now viable at larger n |
| edge_deletion_p0.1 | +0.081 | +0.091 | stable |
| identity | -0.002 | +0.020 | noise floor |
| edge_permutation | -0.015 | +0.003 | noise floor |

Key observation: `subgraph_projection_p0.5` flips from "clique affected" at n=6 to "clique safe" at n=8, because the expected surviving vertex count (4.0) now exceeds k=3. At larger n, more aggressive projections become viable, and the signal strengthens. This is consistent with Razborov's asymptotic argument — the approximation method becomes more powerful as n grows.

(Suggested by Gemini; confirmed experimentally.)

---
