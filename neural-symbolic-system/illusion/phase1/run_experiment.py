"""
Phase 1 main experiment script.

Runs the L2 search engine, collects results, and outputs a report
for L3 (human) review.
"""

import json
import os
import sys
from datetime import datetime

from l1_circuit import parity, random_ac0_circuit
from l2_search import search
from evaluator import monte_carlo_error_rate


def run_experiment(
    n: int = 8,
    depth: int = 3,
    n_circuits: int = 50,
    n_samples: int = 2000,
):
    print("=" * 60)
    print("ILLUSION Phase 1 Experiment")
    print(f"Date: {datetime.now().isoformat()}")
    print(f"Parameters: n={n}, depth={depth}, circuits={n_circuits}, samples={n_samples}")
    print("=" * 60)

    # Run L2 search
    results = search(
        n=n, depth=depth,
        n_circuits=n_circuits,
        n_samples=n_samples,
        verbose=True,
    )

    # Collect candidates for L3 review
    candidates = [r for r in results if r.is_candidate]
    rejected = [r for r in results if not r.is_candidate]

    print("\n" + "=" * 60)
    print("L3 REVIEW QUEUE (manual self-referential safety check)")
    print("=" * 60)

    if not candidates:
        print("No candidates found. L2 search space may need expansion.")
    else:
        for i, c in enumerate(candidates):
            print(f"\nCandidate {i+1}: {c.transform.name}")
            print(f"  Average error rate: {c.avg_error:.3f}")
            print(f"  PARITY affected: {c.parity_affected}")
            print(f"  L3 question: Can an AC^0 circuit decide whether")
            print(f"    a function satisfies the property induced by '{c.transform.name}'?")
            print(f"  If YES => UNSAFE, discard")
            print(f"  If NO  => SAFE, this is a valid discriminating property")

    print("\n" + "=" * 60)
    print("DEAD ENDS (rejected transforms)")
    print("=" * 60)
    for r in rejected:
        reason = "PARITY affected" if r.parity_affected else f"low error ({r.avg_error:.3f})"
        print(f"  x {r.transform.name}: {reason}")

    # Save results
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "timestamp": timestamp,
        "params": {"n": n, "depth": depth, "n_circuits": n_circuits, "n_samples": n_samples},
        "candidates": [
            {"name": r.transform.name, "avg_error": r.avg_error,
             "parity_affected": r.parity_affected}
            for r in candidates
        ],
        "rejected": [
            {"name": r.transform.name, "avg_error": r.avg_error,
             "parity_affected": r.parity_affected}
            for r in rejected
        ],
    }

    report_path = os.path.join(results_dir, f"experiment_{timestamp}.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nResults saved to: {report_path}")

    # Key observations for the research log
    print("\n" + "=" * 60)
    print("OBSERVATIONS (for phase1-results.md)")
    print("=" * 60)
    print(f"1. L2 explored {len(results)} transforms")
    print(f"2. {len(candidates)} candidates passed to L3")
    print(f"3. {len(rejected)} transforms rejected")
    if candidates:
        best = candidates[0]
        print(f"4. Best candidate: {best.transform.name} (error={best.avg_error:.3f})")
        is_hastad = "random_restriction" in best.transform.name
        print(f"5. Is this Hastad's method? {'YES' if is_hastad else 'NO'}")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    depth = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    run_experiment(n=n, depth=depth)
