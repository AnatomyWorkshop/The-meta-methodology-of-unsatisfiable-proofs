# Phase 3 Experiment Report - 2026-05-04

## Parameters
Domain: monotone circuits, target: 3-CLIQUE on 6 vertices
n=6, k=3, depth=3, circuits=30, samples=500, seed=42

## Candidates (sorted by delta-collapse)

| Rank | Transform | Delta | Before | After | Clique Affected | L3 Verdict |
|------|-----------|-------|--------|-------|-----------------|------------|
| 1 | subgraph_projection_p0.7 | +0.245 | 0.669 | 0.914 | False | **SAFE** |
| 2 | edge_deletion_p0.1 | +0.081 | 0.674 | 0.755 | False | **UNSAFE** |

## Rejected by L2

| Transform | Delta | Reason |
|-----------|-------|--------|
| subgraph_projection_p0.5 | +0.328 | clique affected |
| edge_deletion_p0.5 | +0.291 | clique affected |
| edge_deletion_p0.3 | +0.216 | clique affected |
| gate_elevation | +0.131 | clique affected |
| distribution_switch | +0.004 | low delta (+0.004) |
| identity | -0.002 | low delta (-0.002) |
| edge_permutation | -0.015 | low delta (-0.015) |

## L3 Verdicts

- **subgraph_projection_p0.7**: SAFE (high) - moderate subgraph projection preserves the target function but degrades circuit distinguishing power; deciding whether a circuit loses distinguishing advantage under random vertex removal requires exponential sampling
- **edge_deletion_p0.1**: UNSAFE (high) - setting inputs to 0 in a monotone circuit is a monotone operation; deciding whether a circuit collapses under edge deletion is decidable by a monotone circuit of polynomial size

## Summary
- Transforms evaluated: 9
- L2 candidates: 2
- L2 rejected: 7
- L3 SAFE: 1
- L3 UNSAFE: 1
- L3 UNKNOWN: 0
