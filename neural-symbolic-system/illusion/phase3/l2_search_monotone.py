"""
L2: Discriminating property search for monotone circuits.

Enumerates transforms, applies each to a batch of monotone circuits,
and measures distinguishing advantage on D+ vs D-.

Key metric: delta_collapse = collapse_after - collapse_before per circuit.
collapse = 1 - distinguishing_advantage(D+, D-).

Success criterion: find a transform T such that
  1. For all monotone circuits C of bounded size: collapse(T(C)) is high
  2. T does not destroy the k-CLIQUE function itself (affects_clique = False)
  3. (L3 check) The property "C satisfies T" is not decidable in monotone P
"""

from typing import List, Dict, Any
import random
from l1_monotone import MonotoneCircuit, random_monotone_circuit
from evaluator_monotone import measure_collapse_monotone
from transforms import MonotoneTransform, MONOTONE_TRANSFORM_REGISTRY


class MonotoneSearchResult:
    def __init__(self, transform: MonotoneTransform,
                 clique_affected: bool,
                 avg_collapse_before: float, avg_collapse_after: float,
                 avg_delta_collapse: float, details: Dict[str, Any]):
        self.transform = transform
        self.clique_affected = clique_affected
        self.avg_collapse_before = avg_collapse_before
        self.avg_collapse_after = avg_collapse_after
        self.avg_delta_collapse = avg_delta_collapse
        self.details = details

    @property
    def is_candidate(self) -> bool:
        return self.avg_delta_collapse > 0.03 and not self.clique_affected

    @property
    def avg_collapse(self) -> float:
        return self.avg_collapse_after

    def __repr__(self):
        status = "CANDIDATE" if self.is_candidate else "rejected"
        return (f"MonotoneSearchResult({self.transform.name}, "
                f"collapse_before={self.avg_collapse_before:.3f}, "
                f"collapse_after={self.avg_collapse_after:.3f}, "
                f"delta={self.avg_delta_collapse:+.3f}, "
                f"clique_affected={self.clique_affected}, "
                f"{status})")


def search(
    n_vertices: int = 6,
    k: int = 3,
    depth: int = 3,
    n_circuits: int = 30,
    n_samples: int = 500,
    transforms: List[MonotoneTransform] = None,
    verbose: bool = True,
) -> List[MonotoneSearchResult]:
    if transforms is None:
        transforms = MONOTONE_TRANSFORM_REGISTRY

    if verbose:
        print(f"L2 Monotone Search: n={n_vertices}, k={k}, depth={depth}, "
              f"{n_circuits} circuits, {len(transforms)} transforms")
        print("=" * 60)

    circuits = [random_monotone_circuit(n_vertices, depth) for _ in range(n_circuits)]

    if verbose:
        print(f"Generated {len(circuits)} monotone circuits (avg size={sum(c.size for c in circuits)/len(circuits):.0f})")
        print("-" * 60)

    results = []

    for transform in transforms:
        if verbose:
            print(f"\nTesting: {transform.name}")

        collapse_befores = []
        collapse_afters = []

        for c in circuits:
            collapse_before = measure_collapse_monotone(c, n_vertices, k, n_samples=n_samples)
            collapse_befores.append(collapse_before)

            transformed_c = transform.apply(c, n_vertices, k)
            collapse_after = measure_collapse_monotone(transformed_c, n_vertices, k, n_samples=n_samples)
            collapse_afters.append(collapse_after)

        avg_before = sum(collapse_befores) / len(collapse_befores)
        avg_after = sum(collapse_afters) / len(collapse_afters)
        deltas = [a - b for a, b in zip(collapse_afters, collapse_befores)]
        avg_delta = sum(deltas) / len(deltas)
        clique_affected = transform.affects_clique(n_vertices, k)

        sr = MonotoneSearchResult(
            transform=transform,
            clique_affected=clique_affected,
            avg_collapse_before=avg_before,
            avg_collapse_after=avg_after,
            avg_delta_collapse=avg_delta,
            details={
                "collapse_befores": collapse_befores,
                "collapse_afters": collapse_afters,
                "delta_collapses": deltas,
            }
        )
        results.append(sr)

        if verbose:
            print(f"  Collapse: before={avg_before:.3f}, after={avg_after:.3f}, delta={avg_delta:+.3f}")
            print(f"  Clique affected: {clique_affected}")
            print(f"  => {sr}")

    results.sort(key=lambda r: (-r.is_candidate, -r.avg_delta_collapse))

    if verbose:
        print("\n" + "=" * 60)
        print("SEARCH SUMMARY")
        candidates = [r for r in results if r.is_candidate]
        print(f"Candidates found: {len(candidates)}/{len(results)}")
        for r in candidates:
            print(f"  * {r}")

    return results
