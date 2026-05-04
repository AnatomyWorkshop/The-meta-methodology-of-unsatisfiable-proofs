"""
Phase 3 experiment runner: monotone circuits + k-CLIQUE.

Runs L2 search with distribution-based collapse, then L3 safety check
with monotone-specific rules injected.

Usage:
    python run_experiment.py [n_vertices] [k] [depth] [n_circuits] [n_samples] [seed]

Examples:
    python run_experiment.py 6 3 3 30 500 42
"""

import json
import os
import random
import sys
from datetime import datetime

from l1_monotone import random_monotone_circuit, k_clique
from l2_search_monotone import search
from evaluator_monotone import distinguishing_advantage
from l3_rules_monotone import inject_monotone_rules

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))
from l3_monitor import batch_check, append_to_log


def run_experiment(
    n_vertices: int = 6,
    k: int = 3,
    depth: int = 3,
    n_circuits: int = 30,
    n_samples: int = 500,
    seed: int = None,
):
    if seed is not None:
        random.seed(seed)

    inject_monotone_rules()

    print("=" * 60)
    print("ILLUSION Phase 3 Experiment - Monotone Circuits")
    print(f"Date: {datetime.now().isoformat()}")
    print(f"Parameters: n={n_vertices}, k={k}, depth={depth}, "
          f"circuits={n_circuits}, samples={n_samples}, seed={seed}")
    print("=" * 60)

    results = search(
        n_vertices=n_vertices, k=k, depth=depth,
        n_circuits=n_circuits, n_samples=n_samples,
        verbose=True,
    )

    candidates = [r for r in results if r.is_candidate]
    rejected = [r for r in results if not r.is_candidate]

    print("\n" + "=" * 60)
    print("L3 REVIEW QUEUE")
    print("=" * 60)

    if not candidates:
        print("No candidates found.")
    else:
        for i, c in enumerate(candidates):
            print(f"\nCandidate {i+1}: {c.transform.name}")
            print(f"  Collapse: before={c.avg_collapse_before:.3f}, "
                  f"after={c.avg_collapse_after:.3f}, delta={c.avg_delta_collapse:+.3f}")
            print(f"  Clique affected: {c.clique_affected}")
            print(f"  L3 question: Can a polynomial-size monotone circuit decide")
            print(f"    whether a function satisfies the property induced by '{c.transform.name}'?")

    candidate_dicts = [
        {"name": r.transform.name,
         "avg_collapse_before": r.avg_collapse_before,
         "avg_collapse_after": r.avg_collapse_after,
         "avg_delta_collapse": r.avg_delta_collapse,
         "clique_affected": r.clique_affected}
        for r in candidates
    ]

    print("\n" + "=" * 60)
    print("L3 AUTOMATED CHECK")
    print("=" * 60)
    verdicts = batch_check(candidate_dicts, verbose=True)

    print("\n" + "=" * 60)
    print("REJECTED BY L2")
    print("=" * 60)
    for r in rejected:
        reason = "clique affected" if r.clique_affected else f"low delta ({r.avg_delta_collapse:+.3f})"
        print(f"  x {r.transform.name}: {reason}")

    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report = {
        "timestamp": timestamp,
        "phase": 3,
        "domain": "monotone_circuits",
        "target": f"{k}-CLIQUE on {n_vertices} vertices",
        "params": {
            "n_vertices": n_vertices, "k": k, "depth": depth,
            "n_circuits": n_circuits, "n_samples": n_samples, "seed": seed,
        },
        "candidates": candidate_dicts,
        "rejected": [
            {"name": r.transform.name,
             "avg_collapse_before": r.avg_collapse_before,
             "avg_collapse_after": r.avg_collapse_after,
             "avg_delta_collapse": r.avg_delta_collapse,
             "clique_affected": r.clique_affected}
            for r in rejected
        ],
        "l3_verdicts": [
            {"name": v.transform_name, "verdict": v.verdict,
             "reason": v.reason, "confidence": v.confidence}
            for v in verdicts
        ],
    }

    json_path = os.path.join(results_dir, f"experiment_{timestamp}.json")
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nJSON saved to: {json_path}")

    md_path = _write_markdown_report(report, results_dir, timestamp, verdicts)
    print(f"Report saved to: {md_path}")

    print("\n" + "=" * 60)
    print("OBSERVATIONS")
    print("=" * 60)
    print(f"1. L2 explored {len(results)} transforms")
    print(f"2. {len(candidates)} candidates passed to L3")
    print(f"3. {len(rejected)} rejected (clique affected or low delta)")
    if verdicts:
        safe = [v for v in verdicts if v.verdict == "SAFE"]
        unsafe = [v for v in verdicts if v.verdict == "UNSAFE"]
        unknown = [v for v in verdicts if v.verdict == "UNKNOWN"]
        print(f"4. L3: {len(safe)} SAFE, {len(unsafe)} UNSAFE, {len(unknown)} UNKNOWN")
        if safe:
            print(f"5. Safe candidates: {', '.join(v.transform_name for v in safe)}")
            is_razborov = any("distribution" in v.transform_name or "subgraph" in v.transform_name for v in safe)
            print(f"6. Razborov-adjacent method found? {'YES' if is_razborov else 'NO'}")


def _write_markdown_report(report, results_dir, timestamp, verdicts):
    verdict_map = {v.transform_name: v for v in verdicts}
    params = report["params"]
    candidates = report["candidates"]
    rejected = report["rejected"]

    lines = [
        f"# Phase 3 Experiment Report - {timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]}",
        "",
        "## Parameters",
        f"Domain: monotone circuits, target: {report['target']}",
        f"n={params['n_vertices']}, k={params['k']}, depth={params['depth']}, "
        f"circuits={params['n_circuits']}, samples={params['n_samples']}, seed={params['seed']}",
        "",
        "## Candidates (sorted by delta-collapse)",
        "",
        "| Rank | Transform | Delta | Before | After | Clique Affected | L3 Verdict |",
        "|------|-----------|-------|--------|-------|-----------------|------------|",
    ]

    for i, c in enumerate(candidates, 1):
        name = c["name"]
        v = verdict_map.get(name)
        verdict_str = v.verdict if v else "PENDING"
        lines.append(
            f"| {i} | {name} | {c['avg_delta_collapse']:+.3f} | "
            f"{c['avg_collapse_before']:.3f} | {c['avg_collapse_after']:.3f} | "
            f"{c['clique_affected']} | **{verdict_str}** |"
        )

    lines += [
        "",
        "## Rejected by L2",
        "",
        "| Transform | Delta | Reason |",
        "|-----------|-------|--------|",
    ]
    for r in rejected:
        reason = "clique affected" if r["clique_affected"] else f"low delta ({r['avg_delta_collapse']:+.3f})"
        lines.append(f"| {r['name']} | {r['avg_delta_collapse']:+.3f} | {reason} |")

    lines += [
        "",
        "## L3 Verdicts",
        "",
    ]
    for c in candidates:
        v = verdict_map.get(c["name"])
        if v:
            lines.append(f"- **{v.transform_name}**: {v.verdict} ({v.confidence}) - {v.reason}")

    safe_count = sum(1 for v in verdicts if v.verdict == "SAFE")
    unsafe_count = sum(1 for v in verdicts if v.verdict == "UNSAFE")
    unknown_count = sum(1 for v in verdicts if v.verdict == "UNKNOWN")
    lines += [
        "",
        "## Summary",
        f"- Transforms evaluated: {len(candidates) + len(rejected)}",
        f"- L2 candidates: {len(candidates)}",
        f"- L2 rejected: {len(rejected)}",
        f"- L3 SAFE: {safe_count}",
        f"- L3 UNSAFE: {unsafe_count}",
        f"- L3 UNKNOWN: {unknown_count}",
    ]

    md_path = os.path.join(results_dir, f"experiment_{timestamp}_report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return md_path


if __name__ == "__main__":
    n_vertices = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    k          = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    depth      = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    n_circuits = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    n_samples  = int(sys.argv[5]) if len(sys.argv) > 5 else 500
    seed       = int(sys.argv[6]) if len(sys.argv) > 6 else None
    run_experiment(n_vertices=n_vertices, k=k, depth=depth,
                   n_circuits=n_circuits, n_samples=n_samples, seed=seed)
