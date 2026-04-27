"""
L2: Discriminating property search engine.

Enumerates transforms from the registry, applies each to a batch of AC⁰ circuits,
and checks whether the transform causes a persistent error rate lower bound
while leaving PARITY unaffected.

Success criterion: find a transform T such that
  1. For all AC⁰ circuits C of depth ≤ d, size ≤ s: error_rate(T(C), PARITY) ≥ ε
  2. T does not cause PARITY itself to "collapse" (PARITY remains hard after T)
  3. (L3 manual check) The property "C satisfies T" is not decidable within AC⁰
"""

from typing import List, Dict, Any
from l1_circuit import AC0Circuit, parity, random_ac0_circuit
from evaluator import monte_carlo_error_rate
from transforms import Transform, TRANSFORM_REGISTRY


class SearchResult:
    def __init__(self, transform: Transform, avg_error: float,
                 parity_affected: bool, details: Dict[str, Any]):
        self.transform = transform
        self.avg_error = avg_error
        self.parity_affected = parity_affected
        self.details = details

    @property
    def is_candidate(self) -> bool:
        """A candidate discriminating property: high error + PARITY unaffected."""
        return self.avg_error > 0.1 and not self.parity_affected

    def __repr__(self):
        status = "CANDIDATE" if self.is_candidate else "rejected"
        return (f"SearchResult({self.transform.name}, "
                f"err={self.avg_error:.3f}, "
                f"parity_affected={self.parity_affected}, "
                f"{status})")


def search(
    n: int = 8,
    depth: int = 3,
    n_circuits: int = 50,
    n_samples: int = 2000,
    transforms: List[Transform] = None,
    verbose: bool = True,
) -> List[SearchResult]:
    """
    L2 search: enumerate transforms, evaluate each against a batch of circuits.

    Returns list of SearchResults, sorted by candidacy then error rate.
    """
    if transforms is None:
        transforms = TRANSFORM_REGISTRY

    if verbose:
        print(f"L2 Search: n={n}, depth={depth}, {n_circuits} circuits, "
              f"{len(transforms)} transforms")
        print("=" * 60)

    # Generate circuit batch
    circuits = [random_ac0_circuit(n, depth) for _ in range(n_circuits)]

    # Baseline: error rate of raw circuits on PARITY
    baseline_errors = []
    for c in circuits:
        err = monte_carlo_error_rate(c, parity, n_samples)
        baseline_errors.append(err)
    avg_baseline = sum(baseline_errors) / len(baseline_errors)

    if verbose:
        print(f"Baseline avg error on PARITY: {avg_baseline:.3f}")
        print("-" * 60)

    results = []

    for transform in transforms:
        if verbose:
            print(f"\nTesting transform: {transform.name}")

        errors_after = []
        for c in circuits:
            try:
                result = transform.apply(c)
                # Some transforms return (circuit, metadata)
                if isinstance(result, tuple):
                    transformed_c = result[0]
                else:
                    transformed_c = result
                err = monte_carlo_error_rate(transformed_c, parity, n_samples)
                errors_after.append(err)
            except Exception as e:
                if verbose:
                    print(f"  Error applying transform: {e}")
                errors_after.append(0.5)  # degenerate

        avg_error = sum(errors_after) / len(errors_after) if errors_after else 0.0
        parity_affected = transform.affects_parity(n)

        sr = SearchResult(
            transform=transform,
            avg_error=avg_error,
            parity_affected=parity_affected,
            details={
                "individual_errors": errors_after,
                "baseline": avg_baseline,
                "error_increase": avg_error - avg_baseline,
            }
        )
        results.append(sr)

        if verbose:
            print(f"  Avg error after transform: {avg_error:.3f} "
                  f"(Δ={avg_error - avg_baseline:+.3f})")
            print(f"  PARITY affected: {parity_affected}")
            print(f"  => {sr}")

    # Sort: candidates first, then by error rate descending
    results.sort(key=lambda r: (-r.is_candidate, -r.avg_error))

    if verbose:
        print("\n" + "=" * 60)
        print("SEARCH SUMMARY")
        candidates = [r for r in results if r.is_candidate]
        print(f"Candidates found: {len(candidates)}/{len(results)}")
        for r in candidates:
            print(f"  * {r}")

    return results
