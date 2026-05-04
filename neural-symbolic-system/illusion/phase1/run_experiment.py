"""
Phase 1 main experiment script.

Runs the L2 search engine, collects results, and outputs a report
for L3 (human) review.

Usage:
    python run_experiment.py [n] [depth] [n_circuits] [n_samples] [seed]

Examples:
    python run_experiment.py 8 3
    python run_experiment.py 12 3 50 2000
    python run_experiment.py 8 3 50 2000 42   # reproducible run
"""

import json
import os
import random
import sys
from datetime import datetime

from l1_circuit import parity, random_ac0_circuit
from l2_search import search
from evaluator import monte_carlo_error_rate
from l3_monitor import batch_check, append_to_log


def _write_markdown_report(report: dict, results_dir: str, timestamp: str, avg_baseline: float) -> str:
    """Generate a unified markdown report combining L2 results and L3 verdicts."""
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from l3_monitor import batch_check

    params = report["params"]
    candidates = report["candidates"]
    rejected = report["rejected"]

    # Run L3 on candidates
    verdicts = batch_check(candidates, verbose=False)
    verdict_map = {v.transform_name: v for v in verdicts}

    lines = [
        f"# Experiment Report — {timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[9:11]}:{timestamp[11:13]}",
        "",
        "## Parameters",
        f"n={params['n']}, depth={params['depth']}, circuits={params['n_circuits']}, "
        f"samples={params['n_samples']}, seed={params.get('seed', 'None')}",
        f"Baseline error on PARITY: {avg_baseline:.3f}",
        "",
        "## Candidates (sorted by collapse score)",
        "",
        "| Rank | Transform | Collapse | Error | L3 Verdict | L3 Reason |",
        "|------|-----------|----------|-------|------------|-----------|",
    ]

    for i, c in enumerate(candidates, 1):
        name = c["name"]
        v = verdict_map.get(name)
        verdict_str = v.verdict if v else "PENDING"
        reason_str = (v.reason[:60] + "...") if v and len(v.reason) > 60 else (v.reason if v else "")
        lines.append(
            f"| {i} | {name} | {c['avg_collapse']:.3f} | {c['avg_error']:.3f} "
            f"| **{verdict_str}** | {reason_str} |"
        )

    lines += [
        "",
        "## Rejected by L2",
        "",
        "| Transform | Reason |",
        "|-----------|--------|",
    ]
    for r in rejected:
        reason = "PARITY affected" if r["parity_affected"] else f"low collapse ({r['avg_collapse']:.3f})"
        lines.append(f"| {r['name']} | {reason} |")

    lines += [
        "",
        "## L3 Review Queue",
        "",
    ]
    for c in candidates:
        name = c["name"]
        v = verdict_map.get(name)
        verdict_str = v.verdict if v else "PENDING"
        marker = "x" if verdict_str == "UNSAFE" else ("o" if verdict_str == "SAFE" else "?")
        lines.append(f"- [{marker}] {name} => {verdict_str}")

    lines += [
        "",
        "## Summary",
        f"- Total transforms evaluated: {len(candidates) + len(rejected)}",
        f"- Candidates passed to L3: {len(candidates)}",
        f"- Rejected by L2: {len(rejected)}",
    ]
    if verdicts:
        safe = sum(1 for v in verdicts if v.verdict == "SAFE")
        unsafe = sum(1 for v in verdicts if v.verdict == "UNSAFE")
        unknown = sum(1 for v in verdicts if v.verdict == "UNKNOWN")
        lines += [
            f"- L3 SAFE: {safe}",
            f"- L3 UNSAFE: {unsafe}",
            f"- L3 UNKNOWN (needs human review): {unknown}",
        ]

    md_path = os.path.join(results_dir, f"experiment_{timestamp}_report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Markdown report saved to: {md_path}")
    return md_path


def run_experiment(
    n: int = 8,
    depth: int = 3,
    n_circuits: int = 50,
    n_samples: int = 2000,
    seed: int = None,
):
    if seed is not None:
        random.seed(seed)

    print("=" * 60)
    print("ILLUSION Phase 1 Experiment")
    print(f"Date: {datetime.now().isoformat()}")
    print(f"Parameters: n={n}, depth={depth}, circuits={n_circuits}, samples={n_samples}, seed={seed}")
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
            print(f"  Collapse score: {c.avg_collapse:.3f} (threshold: 0.15)")
            print(f"  Average error rate: {c.avg_error:.3f} (lift: {c.error_lift:+.3f})")
            print(f"  PARITY affected: {c.parity_affected}")
            print(f"  L3 question: Can an AC^0 circuit decide whether")
            print(f"    a function satisfies the property induced by '{c.transform.name}'?")
            print(f"  If YES => UNSAFE, discard")
            print(f"  If NO  => SAFE, this is a valid discriminating property")

    print("\n" + "=" * 60)
    print("DEAD ENDS (rejected transforms)")
    print("=" * 60)
    for r in rejected:
        reason = "PARITY affected" if r.parity_affected else f"low collapse ({r.avg_collapse:.3f})"
        print(f"  x {r.transform.name}: {reason}")

    # Save results
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "timestamp": timestamp,
        "params": {"n": n, "depth": depth, "n_circuits": n_circuits, "n_samples": n_samples, "seed": seed},
        "candidates": [
            {"name": r.transform.name, "avg_error": r.avg_error,
             "avg_collapse": r.avg_collapse, "error_lift": r.error_lift,
             "parity_affected": r.parity_affected}
            for r in candidates
        ],
        "rejected": [
            {"name": r.transform.name, "avg_error": r.avg_error,
             "avg_collapse": r.avg_collapse,
             "parity_affected": r.parity_affected}
            for r in rejected
        ],
    }

    report_path = os.path.join(results_dir, f"experiment_{timestamp}.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nResults saved to: {report_path}")

    # Generate unified markdown report
    _write_markdown_report(report, results_dir, timestamp, avg_baseline=results[0].baseline_error if results else 0.5)

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
    n          = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    depth      = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    n_circuits = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    n_samples  = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
    seed       = int(sys.argv[5]) if len(sys.argv) > 5 else None
    run_experiment(n=n, depth=depth, n_circuits=n_circuits, n_samples=n_samples, seed=seed)

