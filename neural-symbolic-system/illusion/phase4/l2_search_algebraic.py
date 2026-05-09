"""
L2: Discriminating property search for algebraic circuits over GF(p).

Enumerates transforms, applies each to a batch of algebraic circuits,
and measures distinguishing advantage on D+ (random) vs D- (rank-1).

Key metric: delta_collapse = collapse_after - collapse_before per circuit.
collapse = 1 - distinguishing_advantage(D+, D-).

Success criterion: find a transform T such that
  1. For all algebraic circuits C of bounded size: collapse(T(C)) is high
  2. T does not destroy the Permanent function itself (affects_permanent = False)
  3. (L3 check) The property "C satisfies T" is not decidable in algebraic P/poly
"""

from typing import List, Dict, Any
import random
from l1_algebraic import AlgebraicCircuit, partial_permanent_circuit
from evaluator_algebraic import measure_collapse_algebraic
from transforms import AlgebraicTransform, ALGEBRAIC_TRANSFORM_REGISTRY


class AlgebraicSearchResult:
    def __init__(self, transform: AlgebraicTransform,
                 permanent_affected: bool,
                 avg_collapse_before: float, avg_collapse_after: float,
                 avg_delta_collapse: float, details: Dict[str, Any]):
        self.transform = transform
        self.permanent_affected = permanent_affected
        self.avg_collapse_before = avg_collapse_before
        self.avg_collapse_after = avg_collapse_after
        self.avg_delta_collapse = avg_delta_collapse
        self.details = details

    @property
    def is_candidate(self) -> bool:
        return self.avg_delta_collapse > 0.03 and not self.permanent_affected

    @property
    def avg_collapse(self) -> float:
        return self.avg_collapse_after

    def __repr__(self):
        status = "CANDIDATE" if self.is_candidate else "rejected"
        return (f"AlgebraicSearchResult({self.transform.name}, "
                f"collapse_before={self.avg_collapse_before:.3f}, "
                f"collapse_after={self.avg_collapse_after:.3f}, "
                f"delta={self.avg_delta_collapse:+.3f}, "
                f"perm_affected={self.permanent_affected}, "
                f"{status})")


def search(
    n: int = 3,
    p: int = 7,
    depth: int = 3,
    n_circuits: int = 20,
    n_samples: int = 300,
    transforms: List[AlgebraicTransform] = None,
    verbose: bool = True,
) -> List[AlgebraicSearchResult]:
    if transforms is None:
        transforms = ALGEBRAIC_TRANSFORM_REGISTRY

    if verbose:
        print(f"L2 Algebraic Search: n={n}, p={p}, depth={depth}, "
              f"{n_circuits} circuits, {len(transforms)} transforms")
        print("=" * 60)

    circuits = [partial_permanent_circuit(n, p) for _ in range(n_circuits)]

    if verbose:
        print(f"Generated {len(circuits)} algebraic circuits over GF({p}) "
              f"(avg size={sum(c.size for c in circuits)/len(circuits):.0f})")
        print("-" * 60)

    results = []

    for transform in transforms:
        if verbose:
            print(f"\nTesting: {transform.name}")

        collapse_befores = []
        collapse_afters = []

        for c in circuits:
            collapse_before = measure_collapse_algebraic(c, n, p, n_samples=n_samples)
            collapse_befores.append(collapse_before)

            transformed_c = transform.apply(c)
            collapse_after = measure_collapse_algebraic(transformed_c, n, p, n_samples=n_samples)
            collapse_afters.append(collapse_after)

        avg_before = sum(collapse_befores) / len(collapse_befores)
        avg_after  = sum(collapse_afters)  / len(collapse_afters)
        deltas     = [a - b for a, b in zip(collapse_afters, collapse_befores)]
        avg_delta  = sum(deltas) / len(deltas)
        perm_affected = transform.affects_permanent(n, p)

        sr = AlgebraicSearchResult(
            transform=transform,
            permanent_affected=perm_affected,
            avg_collapse_before=avg_before,
            avg_collapse_after=avg_after,
            avg_delta_collapse=avg_delta,
            details={
                "collapse_befores": collapse_befores,
                "collapse_afters":  collapse_afters,
                "delta_collapses":  deltas,
            }
        )
        results.append(sr)

        if verbose:
            print(f"  Collapse: before={avg_before:.3f}, after={avg_after:.3f}, delta={avg_delta:+.3f}")
            print(f"  Permanent affected: {perm_affected}")
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
