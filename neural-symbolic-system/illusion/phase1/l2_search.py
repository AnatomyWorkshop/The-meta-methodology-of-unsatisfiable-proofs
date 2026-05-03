"""
L2: Discriminating property search engine.

Enumerates transforms from the registry, applies each to a batch of AC0 circuits,
and checks whether the transform causes a persistent error rate lower bound
while leaving PARITY unaffected.

Success criterion: find a transform T such that
  1. For all AC0 circuits C of depth <= d, size <= s: error_rate(T(C), PARITY) >= epsilon
  2. T does not cause PARITY itself to "collapse" (PARITY remains hard after T)
  3. (L3 manual check) The property "C satisfies T" is not decidable within AC0

Key metric: collapse_score = how much the circuit simplifies under T.
A good discriminating property causes circuits to collapse (simplify)
while PARITY does not collapse.
"""

from typing import List, Dict, Any
import random
from l1_circuit import AC0Circuit, parity, random_ac0_circuit
from evaluator import monte_carlo_error_rate
from transforms import Transform, RestrictedCircuit, TRANSFORM_REGISTRY


def measure_collapse(circuit, n_samples: int = 500) -> float:
    """
    Measure how much a circuit has 'collapsed' relative to a fresh random circuit.
    Proxy: variance of output over random inputs. A collapsed (constant-like) circuit
    has low variance. A hard circuit has variance near 0.25 (Bernoulli(0.5)).
    Returns a collapse score in [0, 1]: 1 = fully collapsed, 0 = no collapse.
    """
    n = circuit.n_inputs
    outputs = []
    for _ in range(n_samples):
        x = tuple(random.choice([True, False]) for _ in range(n))
        outputs.append(1 if circuit.evaluate(x) else 0)
    if not outputs:
        return 0.0
    mean = sum(outputs) / len(outputs)
    variance = sum((o - mean) ** 2 for o in outputs) / len(outputs)
    # Max variance for Bernoulli is 0.25; collapse = 1 - normalized variance
    collapse = 1.0 - (variance / 0.25) if variance < 0.25 else 0.0
    return max(0.0, min(1.0, collapse))


class SearchResult:
    def __init__(self, transform: Transform, avg_error: float,
                 baseline_error: float, parity_affected: bool,
                 avg_collapse: float, details: Dict[str, Any]):
        self.transform = transform
        self.avg_error = avg_error
        self.baseline_error = baseline_error
        self.parity_affected = parity_affected
        self.avg_collapse = avg_collapse  # how much circuits collapse under T
        self.details = details

    @property
    def error_lift(self) -> float:
        """How much error increased above baseline."""
        return self.avg_error - self.baseline_error

    @property
    def is_candidate(self) -> bool:
        """
        A valid discriminating property candidate:
        - Circuits collapse significantly under T (collapse_score > 0.15)
        - PARITY is NOT affected (stays hard)
        The error_lift criterion is secondary; collapse is the primary signal.
        """
        return self.avg_collapse > 0.15 and not self.parity_affected

    def __repr__(self):
        status = "CANDIDATE" if self.is_candidate else "rejected"
        return (f"SearchResult({self.transform.name}, "
                f"err={self.avg_error:.3f}, "
                f"collapse={self.avg_collapse:.3f}, "
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

    Returns list of SearchResults, sorted by candidacy then collapse score.
    """
    if transforms is None:
        transforms = TRANSFORM_REGISTRY

    if verbose:
        print(f"L2 Search: n={n}, depth={depth}, {n_circuits} circuits, "
              f"{len(transforms)} transforms")
        print("=" * 60)

    circuits = [random_ac0_circuit(n, depth) for _ in range(n_circuits)]

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
        collapse_scores = []

        for c in circuits:
            try:
                result = transform.apply(c)
                transformed_c = result[0] if isinstance(result, tuple) else result
                err = monte_carlo_error_rate(transformed_c, parity, n_samples)
                errors_after.append(err)
                collapse = measure_collapse(transformed_c, n_samples=200)
                collapse_scores.append(collapse)
            except Exception as e:
                if verbose:
                    print(f"  Error applying transform: {e}")
                errors_after.append(0.5)
                collapse_scores.append(0.0)

        avg_error = sum(errors_after) / len(errors_after) if errors_after else 0.0
        avg_collapse = sum(collapse_scores) / len(collapse_scores) if collapse_scores else 0.0
        parity_affected = transform.affects_parity(n)

        sr = SearchResult(
            transform=transform,
            avg_error=avg_error,
            baseline_error=avg_baseline,
            parity_affected=parity_affected,
            avg_collapse=avg_collapse,
            details={
                "individual_errors": errors_after,
                "collapse_scores": collapse_scores,
                "baseline": avg_baseline,
                "error_lift": avg_error - avg_baseline,
            }
        )
        results.append(sr)

        if verbose:
            print(f"  Avg error: {avg_error:.3f} (lift={avg_error - avg_baseline:+.3f})")
            print(f"  Avg collapse score: {avg_collapse:.3f}")
            print(f"  PARITY affected: {parity_affected}")
            print(f"  => {sr}")

    results.sort(key=lambda r: (-r.is_candidate, -r.avg_collapse))

    if verbose:
        print("\n" + "=" * 60)
        print("SEARCH SUMMARY")
        candidates = [r for r in results if r.is_candidate]
        print(f"Candidates found: {len(candidates)}/{len(results)}")
        for r in candidates:
            print(f"  * {r}")

    return results

