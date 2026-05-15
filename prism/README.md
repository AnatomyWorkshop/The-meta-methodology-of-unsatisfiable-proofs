# Prism

**A structural symmetry scanner for complex networks.**

Prism measures how far a network is from perfect duality self-consistency. Input a graph, get a number: 0 means structurally symmetric, larger means asymmetric. The whole computation takes 0.08 seconds.

## What it does

Every network can be tested against a duality constraint: reverse the node ordering and check if the structure is preserved. Prism quantifies this precisely:

```
$ prism demo
  Prism Demo: Zachary's Karate Club (34 nodes, 78 edges)

  PRISM SPECTRAL ANALYSIS
  Network: 34 nodes
  Duality defect (original):    16.733201
  Duality defect (constrained): 0.00e+00
  Spectral RMSE (shift):        0.562236
  Max eigenvalue shift:         1.529174
  Time: 0.08s

  VERDICT: Significant duality gap (RMSE = 0.5622)
```

A 5-node cycle (perfectly symmetric) returns defect = 0. A real social network returns 16.7. The tool discriminates structure from noise in milliseconds.

## Install

```bash
pip install -e .
```

Requires: Python 3.10+, numpy, scipy, networkx (optional, for built-in demo graphs).

## Usage

```bash
# Run demo on built-in Karate Club graph
prism demo

# Analyze your own network
prism analyze graph.edgelist
prism analyze adjacency.npy --format npy
prism analyze matrix.csv --format csv

# Quick duality check (no optimization)
prism check graph.edgelist

# JSON output for downstream processing
prism analyze graph.edgelist --json -o result.json
```

## How it works

1. Compute graph Laplacian: `L = D - A`
2. Define duality operator `P` (index reversal)
3. Decompose into P-eigenbasis (even/odd sectors)
4. Find closest Laplacian `L'` satisfying `[L', P] = 0` via L-BFGS-B optimization in the block-diagonal subspace
5. Report: original vs constrained eigenvalues, duality defect, spectral shift per mode

The constraint `[L, P] = 0` is enforced exactly by construction (block-diagonal parameterization), not as a soft penalty. This is a hard structural test, not a statistical one.

## Output

| Field | Meaning |
|-------|---------|
| Duality defect | Frobenius norm of `[L, P]` — 0 means self-consistent |
| Spectral RMSE | How much eigenvalues shift to satisfy duality |
| Max shift | Largest single eigenvalue displacement |
| Per-eigenvalue table | Which modes violate duality most |

## Applications

- **Network anomaly detection**: duality defect spikes signal attacks, faults, or phase transitions
- **GNN regularization**: use defect as a structural prior during training
- **Adversarial robustness**: perturbations that spike defect indicate fragile predictions
- **Graph quality filtering**: discard structurally inconsistent subgraphs before downstream analysis
- **Generative design**: molecules/materials must satisfy structural constraints — Prism filters invalid candidates

## Theoretical basis

Prism implements the discrete projection of the Universal Closure Axiom (UCA) onto graph structures. The continuous form `D·phi = star·D†·star·phi` reduces to `[L, P] = 0` on finite networks. This is not a statistical test — it is a first-principles structural admissibility condition.

For the full derivation, see [Paper 1: UCA + Classical Physics](../papers/uca/paper1-classical-physics.md).

## Roadmap

- [ ] Directed graph support (asymmetric Laplacian)
- [ ] Weighted edge handling
- [ ] Local defect heatmap (per-node contribution)
- [ ] PyG/DGL integration (PrismRegularizer layer)
- [ ] Benchmark on SNAP datasets (power grid, protein networks)
- [ ] Temporal defect tracking (dynamic networks)

## License

MIT
