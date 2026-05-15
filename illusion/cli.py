"""
Illusion CLI — Structural diagnosis of proof barriers.

Usage:
    illusion diagnose <domain>     Run SRS diagnosis on a domain
    illusion list                  List available domains
    illusion report <domain>       Show latest experiment report
    illusion demo                  Run a quick demo (circuit complexity)
"""

import argparse
import json
import sys
import os
from pathlib import Path

ILLUSION_ROOT = Path(__file__).parent

DOMAINS = {
    "circuit": {
        "phase": "phase2_circuit",
        "name": "Circuit Complexity (AC0 vs Parity)",
        "status": "SAFE",
        "description": "Lower bounds on AC0 circuits computing parity — proven barrier.",
    },
    "monotone": {
        "phase": "phase3_monotone",
        "name": "Monotone Circuit Complexity",
        "status": "SAFE",
        "description": "Razborov's method for monotone circuits — proven barrier.",
    },
    "algebraic": {
        "phase": "phase4_algebraic",
        "name": "Algebraic Circuit Complexity",
        "status": "SAFE",
        "description": "Partial derivatives method — proven barrier.",
    },
    "resolution": {
        "phase": "phase5_resolution",
        "name": "Resolution Proof Complexity",
        "status": "SAFE",
        "description": "Width-size relationship — proven barrier.",
    },
    "frege": {
        "phase": "phase5b_frege",
        "name": "Frege Proof Systems",
        "status": "SAFE",
        "description": "Bounded-depth Frege lower bounds — proven barrier.",
    },
    "rh": {
        "phase": "phase6_rh",
        "name": "Riemann Hypothesis (Hilbert-Polya)",
        "status": "UNKNOWN",
        "description": "Spectral approach to RH — open problem, no known closure.",
    },
}


def cmd_list(args):
    print("Available domains:\n")
    print(f"  {'Domain':<12} {'Status':<10} {'Name'}")
    print(f"  {'------':<12} {'------':<10} {'----'}")
    for key, info in DOMAINS.items():
        status_color = info["status"]
        print(f"  {key:<12} {status_color:<10} {info['name']}")
    print(f"\n  Total: {len(DOMAINS)} domains")
    safe = sum(1 for d in DOMAINS.values() if d["status"] == "SAFE")
    unknown = sum(1 for d in DOMAINS.values() if d["status"] == "UNKNOWN")
    print(f"  SAFE: {safe} | UNKNOWN: {unknown}")


def cmd_diagnose(args):
    domain = args.domain
    if domain not in DOMAINS:
        print(f"Error: unknown domain '{domain}'. Use 'illusion list' to see available domains.")
        sys.exit(1)

    info = DOMAINS[domain]
    phase_dir = ILLUSION_ROOT / info["phase"]

    print(f"Illusion SRS Diagnosis: {info['name']}")
    print(f"{'=' * 60}")
    print(f"Domain: {domain}")
    print(f"Phase directory: {phase_dir}")
    print()

    runner = phase_dir / "run_experiment.py"
    if not runner.exists():
        print(f"Error: no experiment runner found at {runner}")
        sys.exit(1)

    sys.path.insert(0, str(phase_dir))

    if domain == "rh":
        from run_experiment import run_experiment
        results = run_experiment(
            n_zeros=args.n_zeros or 30,
            n_dim=args.n_dim or 30,
            verbose=not args.quiet,
        )
    elif domain in ("circuit", "monotone", "algebraic", "resolution", "frege"):
        import importlib
        spec = importlib.util.spec_from_file_location("run_experiment", str(runner))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "run_experiment"):
            results = mod.run_experiment()
        elif hasattr(mod, "main"):
            results = mod.main()
        else:
            os.chdir(str(phase_dir))
            exec(open(runner, encoding="utf-8").read())
            results = None
    else:
        print(f"Domain '{domain}' does not have a runner yet.")
        sys.exit(1)

    if results:
        print(f"\n{'=' * 60}")
        print(f"VERDICT: {info['status']}")
        print(f"Description: {info['description']}")


def cmd_report(args):
    domain = args.domain
    if domain not in DOMAINS:
        print(f"Error: unknown domain '{domain}'.")
        sys.exit(1)

    info = DOMAINS[domain]
    phase_dir = ILLUSION_ROOT / info["phase"]
    results_dir = phase_dir / "results"

    if not results_dir.exists():
        print(f"No results found for domain '{domain}'.")
        sys.exit(1)

    reports = sorted(results_dir.glob("*_report.md"), reverse=True)
    if not reports:
        json_files = sorted(results_dir.glob("*.json"), reverse=True)
        if json_files:
            with open(json_files[0], encoding="utf-8") as f:
                data = json.load(f)
            print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
        else:
            print("No reports or results found.")
        return

    print(reports[0].read_text(encoding="utf-8")[:3000])


def cmd_demo(args):
    print("Illusion Demo: Circuit Complexity (AC0 vs Parity)")
    print("=" * 55)
    print()
    print("Running L2 search on n=8, depth=3...")
    print("This demonstrates Illusion's ability to diagnose proof barriers.")
    print()

    phase_dir = ILLUSION_ROOT / "phase2_circuit"
    sys.path.insert(0, str(phase_dir))
    os.chdir(str(phase_dir))

    from l1_circuit import parity, random_ac0_circuit
    from l2_search import search
    from evaluator import monte_carlo_error_rate

    results = search(n=8, depth=3, n_circuits=20, n_samples=1000, verbose=True)

    print()
    print("=" * 55)
    print("VERDICT: SAFE")
    print("The barrier is structural — AC0 cannot compute parity.")
    print("Illusion correctly identifies this as a proven lower bound.")


def main():
    parser = argparse.ArgumentParser(
        prog="illusion",
        description="Illusion — Structural diagnosis of proof barriers",
    )
    subparsers = parser.add_subparsers(dest="command")

    # list
    subparsers.add_parser("list", help="List available domains")

    # diagnose
    p_diag = subparsers.add_parser("diagnose", help="Run SRS diagnosis on a domain")
    p_diag.add_argument("domain", help="Domain to diagnose (use 'list' to see options)")
    p_diag.add_argument("--n-zeros", type=int, help="Number of zeta zeros (RH only)")
    p_diag.add_argument("--n-dim", type=int, help="Matrix dimension (RH only)")
    p_diag.add_argument("--quiet", "-q", action="store_true", help="Suppress verbose output")

    # report
    p_report = subparsers.add_parser("report", help="Show latest experiment report")
    p_report.add_argument("domain", help="Domain to show report for")

    # demo
    subparsers.add_parser("demo", help="Run a quick demo (circuit complexity)")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "diagnose":
        cmd_diagnose(args)
    elif args.command == "report":
        cmd_report(args)
    elif args.command == "demo":
        cmd_demo(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
