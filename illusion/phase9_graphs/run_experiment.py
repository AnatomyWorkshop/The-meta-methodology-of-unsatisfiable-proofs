"""
Phase 9 Experiment: Graph Theory (Treewidth Boundary)

Model M: graphs with bounded treewidth (tw <= k)
Target f: Hamiltonicity
Decidability boundary: Courcelle's theorem
"""

import sys
import os
import json
from datetime import datetime

_phase9_dir = os.path.abspath(os.path.dirname(__file__))
if _phase9_dir not in sys.path:
    sys.path.insert(0, _phase9_dir)

from l2_search_graphs import search, GraphSearchResult


def run_experiment(
    n_vertices: int = 8,
    tw_bound: int = 3,
    n_graphs: int = 10,
    n_trials: int = 5,
    seed: int = 42,
):
    print("=" * 70)
    print("ILLUSION Phase 9: Graph Theory (Treewidth Boundary)")
    print("=" * 70)
    print()

    results = search(
        n_vertices=n_vertices,
        tw_bound=tw_bound,
        n_graphs=n_graphs,
        n_trials=n_trials,
        seed=seed,
        verbose=True,
    )

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    safe = [r for r in results if r.l3_verdict == "SAFE"]
    unsafe = [r for r in results if r.l3_verdict == "UNSAFE"]
    unknown = [r for r in results if r.l3_verdict == "UNKNOWN"]
    rejected_target = [r for r in results if r.target_affected]
    rejected_low = [r for r in results if not r.target_affected and not r.is_candidate]

    print(f"\nTransforms evaluated: {len(results)}")
    print(f"  Rejected (affects target): {len(rejected_target)}")
    print(f"  Rejected (low Δcollapse): {len(rejected_low)}")
    print(f"  Candidates passed to L3: {len(safe) + len(unsafe) + len(unknown)}")
    print(f"\nL3 Verdicts:")
    print(f"  SAFE:    {len(safe)} — {[r.transform_name for r in safe]}")
    print(f"  UNSAFE:  {len(unsafe)} — {[r.transform_name for r in unsafe]}")
    print(f"  UNKNOWN: {len(unknown)} — {[r.transform_name for r in unknown]}")

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = os.path.join(_phase9_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    report_path = os.path.join(results_dir, f"experiment_{timestamp}_report.md")
    json_path = os.path.join(results_dir, f"experiment_{timestamp}.json")

    # JSON output
    json_data = {
        "phase": "9_graphs",
        "timestamp": timestamp,
        "parameters": {
            "n_vertices": n_vertices,
            "tw_bound": tw_bound,
            "n_graphs": n_graphs,
            "n_trials": n_trials,
            "seed": seed,
        },
        "results": [
            {
                "transform": r.transform_name,
                "advantage_before": r.advantage_before,
                "advantage_after": r.advantage_after if r.advantage_after == r.advantage_after else None,
                "delta_collapse": r.delta_collapse if r.delta_collapse == r.delta_collapse else None,
                "target_affected": r.target_affected,
                "is_candidate": r.is_candidate,
                "l3_verdict": r.l3_verdict,
                "l3_reason": r.l3_reason,
            }
            for r in results
        ],
        "summary": {
            "total": len(results),
            "safe": len(safe),
            "unsafe": len(unsafe),
            "unknown": len(unknown),
            "rejected_target": len(rejected_target),
            "rejected_low": len(rejected_low),
        },
    }

    with open(json_path, "w") as f:
        json.dump(json_data, f, indent=2)

    # Markdown report
    with open(report_path, "w") as f:
        f.write(f"# Phase 9 Experiment Report — {timestamp}\n\n")
        f.write(f"## Parameters\n")
        f.write(f"Domain: Graph theory (treewidth boundary)\n")
        f.write(f"Model M: graphs with tw <= {tw_bound}\n")
        f.write(f"Target f: Hamiltonicity\n")
        f.write(f"n_vertices={n_vertices}, tw_bound={tw_bound}, "
                f"n_graphs={n_graphs}, n_trials={n_trials}, seed={seed}\n\n")

        f.write(f"## Candidates (sorted by Δcollapse)\n\n")
        f.write(f"| Rank | Transform | Δcollapse | Target Affected | L3 Verdict |\n")
        f.write(f"|------|-----------|-----------|-----------------|------------|\n")
        candidates_sorted = sorted(
            [r for r in results if r.is_candidate],
            key=lambda r: -r.delta_collapse
        )
        for i, r in enumerate(candidates_sorted, 1):
            f.write(f"| {i} | {r.transform_name} | {r.delta_collapse:+.3f} | "
                    f"{r.target_affected} | **{r.l3_verdict}** |\n")

        f.write(f"\n## Rejected by L2\n\n")
        f.write(f"| Transform | Δcollapse | Reason |\n")
        f.write(f"|-----------|-----------|--------|\n")
        for r in results:
            if r.target_affected:
                f.write(f"| {r.transform_name} | — | target affected |\n")
            elif not r.is_candidate and not r.target_affected:
                dc = f"{r.delta_collapse:+.3f}" if r.delta_collapse == r.delta_collapse else "—"
                f.write(f"| {r.transform_name} | {dc} | low Δcollapse |\n")

        f.write(f"\n## L3 Verdicts\n\n")
        for r in candidates_sorted:
            f.write(f"- **{r.transform_name}**: {r.l3_verdict} ({r.l3_confidence}) — "
                    f"{r.l3_reason}\n")

        f.write(f"\n## Summary\n")
        f.write(f"- Transforms evaluated: {len(results)}\n")
        f.write(f"- L2 candidates: {len(candidates_sorted)}\n")
        f.write(f"- L3 SAFE: {len(safe)}\n")
        f.write(f"- L3 UNSAFE: {len(unsafe)}\n")
        f.write(f"- L3 UNKNOWN: {len(unknown)}\n")

    print(f"\nResults saved to:")
    print(f"  {json_path}")
    print(f"  {report_path}")

    return results


if __name__ == "__main__":
    run_experiment()
