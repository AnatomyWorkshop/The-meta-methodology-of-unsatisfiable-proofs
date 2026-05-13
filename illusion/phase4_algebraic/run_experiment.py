"""
Phase 4d experiment runner: algebraic circuits over GF(p) + Permanent.

Runs L2 search with distribution-based collapse (D+ vs D-), then L3 safety
check with algebraic-specific rules injected.

Usage:
    python run_experiment.py [n] [p] [depth] [n_circuits] [n_samples] [seed]

Examples:
    python run_experiment.py 3 7 3 20 300 42
    python run_experiment.py 4 7 3 20 300 42
"""

import json
import os
import random
import sys
from datetime import datetime

from l1_algebraic import random_algebraic_circuit, permanent, determinant, matrix_from_flat, partial_permanent_circuit
from l2_search_algebraic import search
from evaluator_algebraic import distinguishing_advantage
from l3_rules_algebraic import inject_algebraic_rules

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))
from l3_monitor import batch_check, append_to_log


def run_experiment(
    n: int = 3,
    p: int = 7,
    depth: int = 3,
    n_circuits: int = 20,
    n_samples: int = 300,
    seed: int = None,
):
    if seed is not None:
        random.seed(seed)

    inject_algebraic_rules()

    print("=" * 60)
    print("ILLUSION Phase 4d Experiment - Algebraic Circuits")
    print(f"Date: {datetime.now().isoformat()}")
    print(f"Parameters: n={n}, p={p}, depth={depth}, "
          f"circuits={n_circuits}, samples={n_samples}, seed={seed}")
    print(f"Domain: algebraic circuits over GF({p}), target: {n}x{n} Permanent")
    print("=" * 60)

    # Sanity check: verify Permanent and Determinant on a small example
    _sanity_check(n, p)

    results = search(
        n=n, p=p, depth=depth,
        n_circuits=n_circuits, n_samples=n_samples,
        verbose=True,
    )

    candidates = [r for r in results if r.is_candidate]
    rejected   = [r for r in results if not r.is_candidate]

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
            print(f"  Permanent affected: {c.permanent_affected}")
            print(f"  L3 question: Can a polynomial-size algebraic circuit over GF({p}) decide")
            print(f"    whether a function satisfies the property induced by '{c.transform.name}'?")

    candidate_dicts = [
        {"name": r.transform.name,
         "avg_collapse_before": r.avg_collapse_before,
         "avg_collapse_after":  r.avg_collapse_after,
         "avg_delta_collapse":  r.avg_delta_collapse,
         "permanent_affected":  r.permanent_affected}
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
        reason = "permanent affected" if r.permanent_affected else f"low delta ({r.avg_delta_collapse:+.3f})"
        print(f"  x {r.transform.name}: {reason}")

    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report = {
        "timestamp": timestamp,
        "phase": "4d",
        "domain": "algebraic_circuits",
        "target": f"{n}x{n} Permanent over GF({p})",
        "params": {
            "n": n, "p": p, "depth": depth,
            "n_circuits": n_circuits, "n_samples": n_samples, "seed": seed,
        },
        "candidates": candidate_dicts,
        "rejected": [
            {"name": r.transform.name,
             "avg_collapse_before": r.avg_collapse_before,
             "avg_collapse_after":  r.avg_collapse_after,
             "avg_delta_collapse":  r.avg_delta_collapse,
             "permanent_affected":  r.permanent_affected}
            for r in rejected
        ],
        "l3_verdicts": [
            {"name": v.transform_name, "verdict": v.verdict,
             "reason": v.reason, "confidence": v.confidence}
            for v in verdicts
        ],
    }

    json_path = os.path.join(results_dir, f"experiment_{timestamp}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\nJSON saved to: {json_path}")

    md_path = _write_markdown_report(report, results_dir, timestamp, verdicts)
    print(f"Report saved to: {md_path}")

    print("\n" + "=" * 60)
    print("OBSERVATIONS")
    print("=" * 60)
    print(f"1. L2 explored {len(results)} transforms")
    print(f"2. {len(candidates)} candidates passed to L3")
    print(f"3. {len(rejected)} rejected (permanent affected or low delta)")
    if verdicts:
        safe    = [v for v in verdicts if v.verdict == "SAFE"]
        unsafe  = [v for v in verdicts if v.verdict == "UNSAFE"]
        unknown = [v for v in verdicts if v.verdict == "UNKNOWN"]
        print(f"4. L3: {len(safe)} SAFE, {len(unsafe)} UNSAFE, {len(unknown)} UNKNOWN")
        if safe:
            print(f"5. Safe candidates: {', '.join(v.transform_name for v in safe)}")
            is_razborov = any("restriction" in v.transform_name for v in safe)
            print(f"6. Razborov-Smolensky analog found? {'YES' if is_razborov else 'NO'}")


def _sanity_check(n: int, p: int):
    """Verify Permanent and Determinant on a small identity matrix."""
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    perm_val = permanent(identity, p)
    det_val  = determinant(identity, p)
    print(f"Sanity check: Permanent(I_{n}) mod {p} = {perm_val} (expected 1)")
    print(f"Sanity check: Determinant(I_{n}) mod {p} = {det_val} (expected 1)")
    assert perm_val == 1, f"Permanent sanity check failed: got {perm_val}"
    assert det_val  == 1, f"Determinant sanity check failed: got {det_val}"
    print("Sanity check passed.")
    print("-" * 60)


def _write_markdown_report(report, results_dir, timestamp, verdicts):
    verdict_map = {v.transform_name: v for v in verdicts}
    params     = report["params"]
    candidates = report["candidates"]
    rejected   = report["rejected"]

    lines = [
        f"# Phase 4d Experiment Report - {timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]}",
        "",
        "## Parameters",
        f"Domain: algebraic circuits over GF({params['p']}), target: {report['target']}",
        f"n={params['n']}, p={params['p']}, depth={params['depth']}, "
        f"circuits={params['n_circuits']}, samples={params['n_samples']}, seed={params['seed']}",
        "",
        "## Candidates (sorted by delta-collapse)",
        "",
        "| Rank | Transform | Delta | Before | After | Perm Affected | L3 Verdict |",
        "|------|-----------|-------|--------|-------|---------------|------------|",
    ]

    for i, c in enumerate(candidates, 1):
        name = c["name"]
        v = verdict_map.get(name)
        verdict_str = v.verdict if v else "PENDING"
        lines.append(
            f"| {i} | {name} | {c['avg_delta_collapse']:+.3f} | "
            f"{c['avg_collapse_before']:.3f} | {c['avg_collapse_after']:.3f} | "
            f"{c['permanent_affected']} | **{verdict_str}** |"
        )

    lines += [
        "",
        "## Rejected by L2",
        "",
        "| Transform | Delta | Reason |",
        "|-----------|-------|--------|",
    ]
    for r in rejected:
        reason = "permanent affected" if r["permanent_affected"] else f"low delta ({r['avg_delta_collapse']:+.3f})"
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

    safe_count    = sum(1 for v in verdicts if v.verdict == "SAFE")
    unsafe_count  = sum(1 for v in verdicts if v.verdict == "UNSAFE")
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
        "",
        "## Framework Interpretation",
        "",
        "The algebraic restriction transform (if SAFE) is the algebraic analog of:",
        "- Phase 1: Håstad's random restriction (AC⁰ lower bounds)",
        "- Phase 3: Razborov's approximation method (monotone circuit lower bounds)",
        "- Phase 4d: Razborov-Smolensky method (algebraic circuit lower bounds)",
        "",
        "If `algebraic_restriction` is SAFE and `field_reduction`/`scalar_multiplication` are UNSAFE,",
        "this confirms the SRS framework's prediction: the discriminating property for Permanent",
        "is not decidable within algebraic P/poly — consistent with Valiant's 1979 hardness result.",
    ]

    md_path = os.path.join(results_dir, f"experiment_{timestamp}_report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return md_path


if __name__ == "__main__":
    n          = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    p          = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    depth      = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    n_circuits = int(sys.argv[4]) if len(sys.argv) > 4 else 20
    n_samples  = int(sys.argv[5]) if len(sys.argv) > 5 else 300
    seed       = int(sys.argv[6]) if len(sys.argv) > 6 else None
    run_experiment(n=n, p=p, depth=depth,
                   n_circuits=n_circuits, n_samples=n_samples, seed=seed)
