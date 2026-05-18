"""
L2 Search for Phase 9: Graph theory domain.

Enumerates transforms, measures Δcollapse, filters candidates, passes to L3.
"""

import random
import sys
import os
from dataclasses import dataclass
from typing import List, Optional

_phase9_dir = os.path.abspath(os.path.dirname(__file__))
_phase2_dir = os.path.abspath(os.path.join(_phase9_dir, '..', 'phase2_circuit'))
if _phase9_dir not in sys.path:
    sys.path.insert(0, _phase9_dir)
if _phase2_dir not in sys.path:
    sys.path.insert(1, _phase2_dir)

import l3_monitor
from l3_monitor import L3Verdict
from distributions import sample_d_plus, sample_d_minus
from evaluator_graphs import measure_distinguishing_advantage
from transforms import GRAPH_TRANSFORM_REGISTRY, GraphTransform
from l3_rules_graphs import inject_graph_rules

DELTA_THRESHOLD = 0.03


@dataclass
class GraphSearchResult:
    transform_name: str
    advantage_before: float
    advantage_after: float
    delta_collapse: float
    delta_advantage: float
    target_affected: bool
    is_candidate: bool
    l3_verdict: Optional[str] = None
    l3_reason: Optional[str] = None
    l3_reference: Optional[str] = None
    l3_confidence: Optional[str] = None


def search(
    n_vertices: int = 12,
    tw_bound: int = 3,
    n_graphs: int = 20,
    n_trials: int = 5,
    seed: int = 42,
    verbose: bool = True,
) -> List[GraphSearchResult]:
    inject_graph_rules()

    rng = random.Random(seed)

    if verbose:
        print(f"Phase 9: Graph Theory (Treewidth Boundary)")
        print(f"  Model M: graphs with tw <= {tw_bound}")
        print(f"  Target f: Hamiltonicity")
        print(f"  Parameters: n_vertices={n_vertices}, n_graphs={n_graphs}, "
              f"n_trials={n_trials}, seed={seed}")
        print(f"  Generating distributions...")

    d_plus = sample_d_plus(n_graphs, n_vertices, tw_bound, seed=seed)
    d_minus = sample_d_minus(n_graphs, n_vertices, tw_bound, seed=seed + 1)

    if verbose:
        print(f"  D+ (Hamiltonian, tw<={tw_bound}): {len(d_plus)} graphs")
        print(f"  D- (non-Hamiltonian, tw<={tw_bound}): {len(d_minus)} graphs")

    if not d_plus or not d_minus:
        print("ERROR: Could not generate enough graphs. Try smaller n_vertices or larger tw_bound.")
        return []

    # Baseline advantage
    baseline_adv = measure_distinguishing_advantage(
        d_plus, d_minus, tw_bound, n_trials, seed=seed
    )
    baseline_collapse = 1.0 - baseline_adv

    if verbose:
        print(f"\n  Baseline: advantage={baseline_adv:.3f}, collapse={baseline_collapse:.3f}")
        print(f"\n  Evaluating {len(GRAPH_TRANSFORM_REGISTRY)} transforms...\n")

    results = []
    candidates = []

    for transform in GRAPH_TRANSFORM_REGISTRY:
        # Check affects_target on sample graphs
        n_affected = 0
        n_checked = min(5, len(d_plus))
        for i in range(n_checked):
            g, n_v, tw_b = d_plus[i]
            t_rng = random.Random(seed + hash(transform.name) % 10000)
            if transform.affects_target(g, n_v, tw_b, t_rng):
                n_affected += 1

        affected = n_affected > n_checked // 2

        if affected:
            if verbose:
                print(f"  {transform.name}: rejected (affects target, "
                      f"{n_affected}/{n_checked} graphs)")
            results.append(GraphSearchResult(
                transform_name=transform.name,
                advantage_before=baseline_adv,
                advantage_after=float('nan'),
                delta_collapse=float('nan'),
                delta_advantage=float('nan'),
                target_affected=True,
                is_candidate=False,
            ))
            continue

        # Apply transform to all graphs and measure advantage
        transformed_plus = []
        for g, n_v, tw_b in d_plus:
            t_rng = random.Random(seed + hash(transform.name) % 10000)
            tg = transform.apply(g, n_v, tw_b, t_rng)
            transformed_plus.append((tg, n_v, tw_b))

        transformed_minus = []
        for g, n_v, tw_b in d_minus:
            t_rng = random.Random(seed + hash(transform.name) % 10000 + 1)
            tg = transform.apply(g, n_v, tw_b, t_rng)
            transformed_minus.append((tg, n_v, tw_b))

        adv_after = measure_distinguishing_advantage(
            transformed_plus, transformed_minus, tw_bound, n_trials,
            seed=seed + 1000
        )
        collapse_after = 1.0 - adv_after
        delta_collapse = collapse_after - baseline_collapse
        delta_adv = adv_after - baseline_adv

        is_candidate = delta_collapse > DELTA_THRESHOLD

        if verbose:
            status = "CANDIDATE" if is_candidate else "rejected"
            print(f"  {transform.name}: Δcollapse={delta_collapse:+.3f} "
                  f"(adv {baseline_adv:.3f}→{adv_after:.3f}) [{status}]")

        result = GraphSearchResult(
            transform_name=transform.name,
            advantage_before=baseline_adv,
            advantage_after=adv_after,
            delta_collapse=delta_collapse,
            delta_advantage=delta_adv,
            target_affected=False,
            is_candidate=is_candidate,
        )

        if is_candidate:
            candidates.append(result)
        results.append(result)

    # L3 check on candidates
    if candidates:
        if verbose:
            print(f"\n  L3 safety check on {len(candidates)} candidate(s):\n")
        for result in candidates:
            verdict: L3Verdict = l3_monitor.check(result.transform_name, verbose=False)
            result.l3_verdict = verdict.verdict
            result.l3_reason = verdict.reason
            result.l3_reference = verdict.reference
            result.l3_confidence = verdict.confidence
            if verbose:
                print(f"    {result.transform_name}: [{verdict.verdict}] "
                      f"({verdict.confidence}) — {verdict.reason[:80]}...")

    return results
