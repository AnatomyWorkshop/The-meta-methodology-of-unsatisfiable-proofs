# Prism CLI v0.1 Specification

> Generated via Meta-Dispatch adversarial synthesis | deepseek-official | 2000tok

# Prism CLI v0.1 Specification

**Prism** applies Universal Conservation of Action (UCA) duality constraints to network eigenvalue structure, producing a *prism‑adjusted* graph whose spectrum satisfies a given duality law while remaining as close as possible to the original.  
The CLI mirrors the simplicity and demo‑friendliness of the Illusion toolchain: a single command can be run in under 5 minutes on a moderate graph (up to ~500 nodes).

---

## 1. CLI Interface

### Command
```
prism [subcommand] [flags]
```

### Subcommands
| Subcommand | Description |
|------------|-------------|
| `optimize` | Run the UCA duality optimizer on a graph and output the adjusted graph + eigenvalues |
| `check`    | Check duality constraint satisfaction of an existing graph (no optimization) |
| `demo`     | Run optimization on a built‑in small graph (e.g. Karate club) and print summary |

### Flags for `optimize` (and `demo` where applicable)
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--input` | path | **required** | Input file containing the graph |
| `--output` | path | `prism_output.json` | Output file for results (JSON) |
| `--format` | string | `auto` | Format of input: `adjacency`, `laplacian`, `edgelist`, `csv`, `npy`, `auto` (detect) |
| `--type` | string | `adjacency` | How to interpret the matrix: `adjacency` or `laplacian` (the other will be derived) |
| `--constraint` | string | `uca_dual` | Which UCA duality constraint to enforce; currently only `uca_dual` is available |
| `--reg` | float | `1e-6` | L2 regularisation strength for the matrix entries (controls deviation from original) |
| `--tol` | float | `1e-6` | Convergence tolerance on duality residuals (RMSE of eigenvalue violations) |
| `--max-iter` | int | `1000` | Maximum number of optimisation iterations |
| `--lr` | float | `0.01` | Learning rate for the gradient‑based solver |
| `--symmetric` | bool | `true` | Enforce symmetry of the output adjacency (if adjacency) |
| `--zero-diag` | bool | `true` | Enforce zero diagonal for adjacency (no self‑loops) |
| `--verbose` | flag | `false` | Print progress at each iteration |
| `--quiet` | flag | `false` | Suppress all output except the result file |

### Example usage
```bash
# Optimise a graph given as edge list, print Eigenvalue comparison
prism optimize --input graph.edgelist --format edgelist --verbose

# Check duality of an existing adjacency matrix in CSV
prism check --input A.csv --format csv

# Quick demo with built‑in Zachary's karate club
prism demo
```

---

## 2. Core Algorithm Steps

The algorithm enforces **UCA duality constraints** on the Laplacian eigenvalues.  
**Constraint definition (uca_dual):**  
For the graph