# Phase 9 Experiment Report ¡ª 20260518_234425

## Parameters
Domain: Graph theory (treewidth boundary)
Model M: graphs with tw <= 3
Target f: Hamiltonicity
n_vertices=8, tw_bound=3, n_graphs=10, n_trials=5, seed=42

## Candidates (sorted by ¦¤collapse)

| Rank | Transform | ¦¤collapse | Target Affected | L3 Verdict |
|------|-----------|-----------|-----------------|------------|
| 1 | minor_embedding_k5 | +0.860 | False | **UNKNOWN** |
| 2 | treewidth_expansion | +0.860 | False | **SAFE** |
| 3 | edge_addition_random | +0.480 | False | **SAFE** |
| 4 | random_subgraph_p0.2 | +0.400 | False | **UNSAFE** |
| 5 | edge_addition_random | +0.260 | False | **SAFE** |
| 6 | vertex_subdivision | +0.200 | False | **UNSAFE** |

## Rejected by L2

| Transform | ¦¤collapse | Reason |
|-----------|-----------|--------|
| identity | +0.000 | low ¦¤collapse |
| edge_contraction | ¡ª | target affected |
| clique_sum_k+1 | ¡ª | target affected |
| random_subgraph_p0.4 | ¡ª | target affected |
| planar_projection | +0.000 | low ¦¤collapse |

## L3 Verdicts

- **minor_embedding_k5**: UNKNOWN (low) ¡ª No matching rule in L3 knowledge base. Human review required.
- **treewidth_expansion**: SAFE (high) ¡ª Targeted edge addition to increase treewidth. Verifying that treewidth increased beyond k requires solving an NP-hard problem (for general k). The bounded-tw algorithm cannot self-diagnose whether its own capacity has been exceeded.
- **edge_addition_random**: SAFE (high) ¡ª Adding random edges may increase treewidth beyond bound; deciding whether treewidth increased is NP-hard for general graphs (Arnborg et al. 1987). The induced property 'did the graph exceed tw=k?' requires computing treewidth, which is not decidable within the bounded-tw model itself.
- **random_subgraph_p0.2**: UNSAFE (high) ¡ª Subgraph of a tw<=k graph has tw<=k. Edge deletion is a local operation whose effect on any MSO2 property is decidable in linear time on bounded-tw graphs.
- **edge_addition_random**: SAFE (high) ¡ª Adding random edges may increase treewidth beyond bound; deciding whether treewidth increased is NP-hard for general graphs (Arnborg et al. 1987). The induced property 'did the graph exceed tw=k?' requires computing treewidth, which is not decidable within the bounded-tw model itself.
- **vertex_subdivision**: UNSAFE (high) ¡ª Vertex subdivision preserves treewidth (tw(G') <= tw(G) for subdivisions). The operation is local and MSO2-definable. Deciding whether a graph was subdivided is decidable in linear time on bounded-tw graphs by Courcelle's theorem.

## Summary
- Transforms evaluated: 11
- L2 candidates: 6
- L3 SAFE: 3
- L3 UNSAFE: 2
- L3 UNKNOWN: 1
