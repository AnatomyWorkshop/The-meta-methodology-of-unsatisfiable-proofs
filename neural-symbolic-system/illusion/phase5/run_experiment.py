import json
import os
import sys
import random
from datetime import datetime

_phase5_dir = os.path.abspath(os.path.dirname(__file__))
_phase2_dir = os.path.abspath(os.path.join(_phase5_dir, '..', 'phase2'))
if _phase5_dir not in sys.path:
    sys.path.insert(0, _phase5_dir)
if _phase2_dir not in sys.path:
    sys.path.insert(1, _phase2_dir)

from l2_search_resolution import search
from distributions import php_formula
from l1_resolution import greedy_resolution


def run_experiment(
    width_limit: int = 4,
    n_formulas: int = 10,
    n_trials: int = 5,
    seed: int = 42,
    verbose: bool = True,
) -> dict:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Sanity check
    f = php_formula(3, 2)
    ok, _, _ = greedy_resolution(f, width_limit=3, seed=seed)
    assert ok, "Sanity check failed: PHP(3,2) should be provable with width 3"
    f2 = php_formula(6, 5)
    ok2, _, _ = greedy_resolution(f2, width_limit=4, seed=seed)
    assert not ok2, "Sanity check failed: PHP(6,5) should NOT be provable with width 4"
    if verbose:
        print("Sanity checks passed.\n")

    results = search(
        width_limit=width_limit,
        n_formulas=n_formulas,
        n_trials=n_trials,
        seed=seed,
        verbose=verbose,
    )

    candidates = [r for r in results if r.is_candidate]
    rejected = [r for r in results if not r.is_candidate]

    safe = [r for r in candidates if r.l3_verdict == "SAFE"]
    unsafe = [r for r in candidates if r.l3_verdict == "UNSAFE"]
    unknown = [r for r in candidates if r.l3_verdict == "UNKNOWN"]

    def result_to_dict(r):
        d = {
            "name": r.transform_name,
            "advantage_before": round(r.advantage_before, 4),
            "advantage_after": round(r.advantage_after, 4) if r.advantage_after == r.advantage_after else None,
            "delta_collapse": round(r.delta_collapse, 4) if r.delta_collapse == r.delta_collapse else None,
            "target_affected": r.target_affected,
        }
        if r.l3_verdict:
            d["l3_verdict"] = r.l3_verdict
            d["l3_reason"] = r.l3_reason
            d["l3_reference"] = r.l3_reference
            d["l3_confidence"] = r.l3_confidence
        return d

    output = {
        "timestamp": timestamp,
        "phase": "5",
        "domain": "resolution_proof_complexity",
        "target": f"PHP_n (pigeonhole principle), width_limit={width_limit}",
        "params": {
            "width_limit": width_limit,
            "n_formulas": n_formulas,
            "n_trials": n_trials,
            "seed": seed,
        },
        "candidates": [result_to_dict(r) for r in candidates],
        "rejected": [result_to_dict(r) for r in rejected],
        "l3_summary": {
            "safe": [r.transform_name for r in safe],
            "unsafe": [r.transform_name for r in unsafe],
            "unknown": [r.transform_name for r in unknown],
        },
    }

    os.makedirs(os.path.join(_phase5_dir, "results"), exist_ok=True)
    json_path = os.path.join(_phase5_dir, "results", f"experiment_{timestamp}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    _write_report(output, timestamp)

    if verbose:
        print(f"\nResults saved: {json_path}")

    return output


def _write_report(data: dict, timestamp: str) -> None:
    lines = [
        "# Phase 5 Experiment Report: Resolution Proof Complexity",
        "",
        f"> Timestamp: {timestamp}",
        f"> Domain: Resolution proof system, target: PHP_n (pigeonhole principle)",
        f"> Params: width_limit={data['params']['width_limit']}, "
        f"n_formulas={data['params']['n_formulas']}, "
        f"n_trials={data['params']['n_trials']}, "
        f"seed={data['params']['seed']}",
        "",
        "---",
        "",
        "## Candidates (passed L2 threshold)",
        "",
        "| Transform | delta_collapse | Target affected | L3 verdict |",
        "|-----------|---------------|----------------|------------|",
    ]

    for r in data["candidates"]:
        delta = f"{r['delta_collapse']:+.3f}" if r["delta_collapse"] is not None else "N/A"
        verdict = r.get("l3_verdict", "-")
        verdict_str = f"**{verdict}**" if verdict in ("SAFE", "UNKNOWN") else verdict
        lines.append(
            f"| {r['name']} | {delta} | {'Yes' if r['target_affected'] else 'No'} | {verdict_str} |"
        )

    unknown_list = data['l3_summary']['unknown']
    safe_list = data['l3_summary']['safe']

    lines += [
        "",
        "## L3 Summary",
        "",
        f"- **SAFE**: {', '.join(safe_list) or '(none)'}",
        f"- **UNSAFE**: {', '.join(data['l3_summary']['unsafe']) or '(none)'}",
        f"- **UNKNOWN**: {', '.join(unknown_list) or '(none)'}",
        "",
        "---",
        "",
        "## Key Findings",
        "",
    ]

    if unknown_list:
        lines += [
            "### UNKNOWN verdicts (Phase 5 primary target)",
            "",
            "The following transforms have positive delta_collapse but L3 cannot determine "
            "decidability within Resolution:",
            "",
        ]
        for r in data["candidates"]:
            if r.get("l3_verdict") == "UNKNOWN":
                lines += [
                    f"**{r['name']}** (delta_collapse={r['delta_collapse']:+.3f})",
                    "",
                    f"> {r.get('l3_reason', '')}",
                    "",
                    f"> Reference: {r.get('l3_reference', '')}",
                    "",
                ]
        lines += [
            "UNKNOWN is not a failure. It is the system pointing at the boundary of "
            "current proof complexity theory.",
            "",
        ]

    if safe_list:
        lines += [
            "### SAFE candidates",
            "",
            "`clause_restriction` is the core operation of the Ben-Sasson-Wigderson width method: "
            "randomly fixing variables preserves the PHP width lower bound. "
            "L2 arrived at this without being told about Ben-Sasson-Wigderson.",
            "",
            "`clause_projection` is the Resolution analog of subgraph projection: "
            "randomly retaining a subset of clauses degrades the proof system's distinguishing power.",
            "",
        ]

    lines += [
        "---",
        "",
        "## Comparison with previous phases",
        "",
        "| Phase | Domain | UNKNOWN count | Significance |",
        "|-------|--------|--------------|--------------|",
        "| 1 | AC0 | 0 | Known domain, rule library sufficient |",
        "| 3 | Monotone circuits | 0 | Known domain, rule library sufficient |",
        "| 4d | Algebraic circuits | 0 | Known domain, rule library sufficient |",
        f"| **5** | **Resolution** | **{len(unknown_list)}** | **Knowledge boundary reached** |",
        "",
    ]

    report_path = os.path.join(_phase5_dir, "results", f"experiment_{timestamp}_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("width_limit", type=int, nargs="?", default=4)
    parser.add_argument("n_formulas", type=int, nargs="?", default=10)
    parser.add_argument("n_trials", type=int, nargs="?", default=5)
    parser.add_argument("seed", type=int, nargs="?", default=42)
    args = parser.parse_args()

    run_experiment(
        width_limit=args.width_limit,
        n_formulas=args.n_formulas,
        n_trials=args.n_trials,
        seed=args.seed,
        verbose=True,
    )
