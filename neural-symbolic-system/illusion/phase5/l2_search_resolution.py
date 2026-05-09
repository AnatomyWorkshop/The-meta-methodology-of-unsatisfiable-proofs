import random
import sys
import os
from dataclasses import dataclass, field
from typing import List, Optional

# Insert phase5 dir first so local modules take priority over phase1
_phase5_dir = os.path.abspath(os.path.dirname(__file__))
_phase2_dir = os.path.abspath(os.path.join(_phase5_dir, '..', 'phase2'))
if _phase5_dir not in sys.path:
    sys.path.insert(0, _phase5_dir)
if _phase2_dir not in sys.path:
    sys.path.insert(1, _phase2_dir)

import l3_monitor
from l3_monitor import L3Verdict

from distributions import sample_d_plus, sample_d_minus, Formula
from evaluator_resolution import measure_distinguishing_advantage_batch
from transforms import RESOLUTION_TRANSFORM_REGISTRY, ResolutionTransform
from l3_rules_resolution import inject_resolution_rules

DELTA_THRESHOLD = 0.03


@dataclass
class ResolutionSearchResult:
    transform_name: str
    advantage_before: float
    advantage_after: float
    delta_collapse: float          # collapse_after - collapse_before = -(delta_advantage)
    delta_advantage: float         # advantage_after - advantage_before (negative = degraded)
    target_affected: bool
    is_candidate: bool
    l3_verdict: Optional[str] = None
    l3_reason: Optional[str] = None
    l3_reference: Optional[str] = None
    l3_confidence: Optional[str] = None


def search(
    width_limit: int = 4,
    n_formulas: int = 10,
    n_trials: int = 5,
    seed: int = 42,
    verbose: bool = True,
) -> List[ResolutionSearchResult]:
    inject_resolution_rules()

    rng = random.Random(seed)

    d_plus = sample_d_plus(n_formulas, seed=seed)
    d_minus = sample_d_minus(n_formulas, seed=seed + 1)

    # Baseline advantage (no transform)
    baseline_adv = measure_distinguishing_advantage_batch(
        d_plus, d_minus, width_limit, n_trials, seed=seed
    )
    baseline_collapse = 1.0 - baseline_adv

    if verbose:
        print(f"Baseline: advantage={baseline_adv:.3f}, collapse={baseline_collapse:.3f}")
        print(f"Width limit: {width_limit}, formulas: {n_formulas}, trials: {n_trials}\n")

    results = []
    candidates = []

    for transform in RESOLUTION_TRANSFORM_REGISTRY:
        # Check affects_target on a sample formula
        sample_formula, n_p, n_h = d_plus[0]
        affected = transform.affects_target(sample_formula, n_p, n_h, rng)

        if affected:
            if verbose:
                print(f"  {transform.name}: rejected (affects target)")
            results.append(ResolutionSearchResult(
                transform_name=transform.name,
                advantage_before=baseline_adv,
                advantage_after=float('nan'),
                delta_collapse=float('nan'),
                delta_advantage=float('nan'),
                target_affected=True,
                is_candidate=False,
            ))
            continue

        # Apply transform to all formulas and measure advantage
        transformed_plus = []
        for formula, n_p, n_h in d_plus:
            t_rng = random.Random(seed + hash(transform.name) % 10000)
            tf = transform.apply(formula, n_p, n_h, t_rng)
            transformed_plus.append((tf, n_p, n_h))

        transformed_minus = []
        for formula, n_p, n_h in d_minus:
            t_rng = random.Random(seed + hash(transform.name) % 10000 + 1)
            tf = transform.apply(formula, n_p, n_h, t_rng)
            transformed_minus.append((tf, n_p, n_h))

        adv_after = measure_distinguishing_advantage_batch(
            transformed_plus, transformed_minus, width_limit, n_trials,
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

        result = ResolutionSearchResult(
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
            print(f"\nL3 safety check on {len(candidates)} candidate(s):\n")
        for result in candidates:
            verdict: L3Verdict = l3_monitor.check(result.transform_name, verbose=False)
            result.l3_verdict = verdict.verdict
            result.l3_reason = verdict.reason
            result.l3_reference = verdict.reference
            result.l3_confidence = verdict.confidence
            if verbose:
                status_str = f"[{verdict.verdict}]"
                print(f"  {result.transform_name}: {status_str} "
                      f"({verdict.confidence}) — {verdict.reason[:80]}...")

    return results


if __name__ == "__main__":
    results = search(width_limit=4, n_formulas=10, n_trials=5, seed=42, verbose=True)
    print("\n--- Summary ---")
    safe = [r for r in results if r.l3_verdict == "SAFE"]
    unsafe = [r for r in results if r.l3_verdict == "UNSAFE"]
    unknown = [r for r in results if r.l3_verdict == "UNKNOWN"]
    print(f"SAFE: {[r.transform_name for r in safe]}")
    print(f"UNSAFE: {[r.transform_name for r in unsafe]}")
    print(f"UNKNOWN: {[r.transform_name for r in unknown]}")
