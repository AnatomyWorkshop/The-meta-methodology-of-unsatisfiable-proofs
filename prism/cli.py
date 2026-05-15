"""
Prism CLI — UCA-constrained spectral analysis for complex networks.

Usage:
    prism analyze <input>    Run UCA spectral constraint analysis on a network
    prism check <input>      Check duality defect without optimization
    prism demo               Run demo on Zachary's Karate Club graph
"""

import argparse
import json
import sys
import time
import numpy as np
from pathlib import Path

from prism.core import analyze_network, parity_operator, PrismResult


def load_network(path: str, fmt: str = "auto") -> np.ndarray:
    """Load a network from file. Returns adjacency matrix."""
    p = Path(path)
    if not p.exists():
        print(f"Error: file not found: {path}")
        sys.exit(1)

    if fmt == "auto":
        suffix = p.suffix.lower()
        if suffix == ".npy":
            fmt = "npy"
        elif suffix in (".csv", ".tsv"):
            fmt = "csv"
        else:
            fmt = "edgelist"

    if fmt == "npy":
        return np.load(path)
    elif fmt == "csv":
        return np.loadtxt(path, delimiter=",")
    elif fmt == "edgelist":
        edges = []
        max_node = 0
        for line in p.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("%"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                u, v = int(parts[0]), int(parts[1])
                weight = float(parts[2]) if len(parts) > 2 else 1.0
                edges.append((u, v, weight))
                max_node = max(max_node, u, v)
        n = max_node + 1
        A = np.zeros((n, n))
        for u, v, w in edges:
            A[u, v] = w
            A[v, u] = w
        return A
    else:
        print(f"Error: unknown format '{fmt}'")
        sys.exit(1)


def karate_club_adjacency() -> np.ndarray:
    """Zachary's Karate Club graph (34 nodes). Built-in demo network."""
    try:
        import networkx as nx
        G = nx.karate_club_graph()
        return nx.to_numpy_array(G)
    except ImportError:
        pass

    edges = [
        (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,10),(0,11),
        (0,12),(0,13),(0,17),(0,19),(0,21),(0,31),(1,2),(1,3),(1,7),(1,13),
        (1,17),(1,19),(1,21),(1,30),(2,3),(2,7),(2,8),(2,9),(2,13),(2,27),
        (2,28),(2,32),(3,7),(3,12),(3,13),(4,6),(4,10),(5,6),(5,10),(5,16),
        (6,16),(8,30),(8,32),(8,33),(9,33),(13,33),(14,32),(14,33),(15,32),
        (15,33),(18,32),(18,33),(19,33),(20,32),(20,33),(22,32),(22,33),
        (23,25),(23,27),(23,29),(23,32),(23,33),(24,25),(24,27),(24,31),
        (25,31),(26,29),(26,33),(27,33),(28,31),(28,33),(29,32),(29,33),
        (30,32),(30,33),(31,32),(31,33),(32,33),
    ]
    n = 34
    A = np.zeros((n, n))
    for u, v in edges:
        A[u, v] = 1.0
        A[v, u] = 1.0
    return A


def print_result(result: PrismResult, verbose: bool = False):
    """Pretty-print analysis results."""
    n = result.metadata["n"]
    print(f"\n{'=' * 60}")
    print(f"  PRISM SPECTRAL ANALYSIS")
    print(f"{'=' * 60}")
    print(f"  Network: {n} nodes")
    print(f"  Duality defect (original):    {result.duality_defect_original:.6f}")
    print(f"  Duality defect (constrained): {result.duality_defect_constrained:.2e}")
    print(f"  Spectral RMSE (shift):        {result.rmse:.6f}")
    print(f"  Max eigenvalue shift:         {result.max_shift:.6f}")
    print(f"  Optimizer iterations:         {result.n_iterations}")
    print(f"  Converged:                    {result.converged}")
    print()

    n_show = min(10, n)
    print(f"  Eigenvalue comparison (first {n_show}):")
    print(f"  {'#':>3}  {'Original':>10}  {'Constrained':>12}  {'Shift':>10}")
    print(f"  {'---':>3}  {'--------':>10}  {'-----------':>12}  {'-----':>10}")
    for i in range(n_show):
        o = result.original_eigenvalues[i]
        c = result.constrained_eigenvalues[i]
        s = result.spectral_shift[i]
        print(f"  {i+1:>3}  {o:>10.4f}  {c:>12.4f}  {s:>+10.6f}")

    if n > n_show:
        print(f"  ... ({n - n_show} more eigenvalues)")

    print()
    if result.duality_defect_original < 1e-6:
        print("  VERDICT: Network already satisfies UCA duality (defect ≈ 0)")
        print("  The spectrum is self-consistent under index-reversal symmetry.")
    elif result.rmse < 0.01:
        print("  VERDICT: Near-duality. Small spectral adjustment needed.")
        print("  The network is close to UCA-compatible.")
    else:
        print(f"  VERDICT: Significant duality gap (RMSE = {result.rmse:.4f})")
        print("  The constrained spectrum differs meaningfully from the original.")
        print("  Eigenvalues with large shifts indicate structural asymmetry.")
    print()


def cmd_analyze(args):
    A = load_network(args.input, fmt=args.format)
    n = A.shape[0]
    print(f"Prism: analyzing network ({n} nodes)...")

    start = time.time()
    result = analyze_network(
        A,
        reg=args.reg,
        max_iter=args.max_iter,
        verbose=args.verbose,
    )
    elapsed = time.time() - start

    print_result(result, verbose=args.verbose)
    print(f"  Time: {elapsed:.2f}s")

    if args.json:
        out = {
            "n": n,
            "original_eigenvalues": result.original_eigenvalues.tolist(),
            "constrained_eigenvalues": result.constrained_eigenvalues.tolist(),
            "spectral_shift": result.spectral_shift.tolist(),
            "duality_defect_original": result.duality_defect_original,
            "duality_defect_constrained": result.duality_defect_constrained,
            "rmse": result.rmse,
            "max_shift": result.max_shift,
            "converged": result.converged,
            "metadata": result.metadata,
        }
        if args.output:
            Path(args.output).write_text(json.dumps(out, indent=2))
            print(f"  Results written to: {args.output}")
        else:
            print(json.dumps(out, indent=2))


def cmd_check(args):
    A = load_network(args.input, fmt=args.format)
    n = A.shape[0]
    D = np.diag(A.sum(axis=1))
    L = D - A
    L_sym = (L + L.T) / 2
    P = parity_operator(n)

    defect = np.linalg.norm(L_sym @ P - P @ L_sym, 'fro')
    eigs = np.sort(np.linalg.eigvalsh(L_sym))

    print(f"\n  Prism Check: {n} nodes")
    print(f"  Duality defect ||[L, P]||_F: {defect:.6f}")
    if defect < 1e-6:
        print("  Status: UCA-COMPATIBLE (duality satisfied)")
    else:
        print(f"  Status: DUALITY GAP (run 'prism analyze' for constrained spectrum)")
    print(f"\n  Spectrum (first 5): {eigs[:5]}")
    print(f"  Spectrum (last 5):  {eigs[-5:]}")


def cmd_demo(args):
    print("Prism Demo: Zachary's Karate Club (34 nodes, 78 edges)")
    print("=" * 58)
    print()
    print("This network represents friendships between members of a")
    print("university karate club. It famously splits into two factions.")
    print()
    print("Prism asks: does this network's spectral structure satisfy")
    print("UCA duality self-consistency? If not, how much does the")
    print("spectrum need to shift to become duality-compatible?")
    print()

    A = karate_club_adjacency()
    start = time.time()
    result = analyze_network(A, reg=1e-6, max_iter=2000, verbose=args.verbose)
    elapsed = time.time() - start

    print_result(result)
    print(f"  Time: {elapsed:.2f}s")
    print()
    print("Interpretation: eigenvalues with large shifts correspond to")
    print("modes that violate duality -- these are the structurally")
    print("asymmetric features of the network.")


def main():
    parser = argparse.ArgumentParser(
        prog="prism",
        description="Prism — UCA-constrained spectral analysis for complex networks",
    )
    subparsers = parser.add_subparsers(dest="command")

    # analyze
    p_analyze = subparsers.add_parser("analyze", help="Run UCA spectral constraint analysis")
    p_analyze.add_argument("input", help="Input file (edgelist, .npy, or .csv)")
    p_analyze.add_argument("--format", default="auto", choices=["auto", "edgelist", "npy", "csv"])
    p_analyze.add_argument("--reg", type=float, default=1e-6, help="Regularization strength")
    p_analyze.add_argument("--max-iter", type=int, default=2000, help="Max optimizer iterations")
    p_analyze.add_argument("--json", action="store_true", help="Output JSON")
    p_analyze.add_argument("--output", "-o", help="Write JSON results to file")
    p_analyze.add_argument("--verbose", "-v", action="store_true")

    # check
    p_check = subparsers.add_parser("check", help="Check duality defect (no optimization)")
    p_check.add_argument("input", help="Input file")
    p_check.add_argument("--format", default="auto", choices=["auto", "edgelist", "npy", "csv"])

    # demo
    p_demo = subparsers.add_parser("demo", help="Run demo on Karate Club graph")
    p_demo.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    if args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "check":
        cmd_check(args)
    elif args.command == "demo":
        cmd_demo(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
