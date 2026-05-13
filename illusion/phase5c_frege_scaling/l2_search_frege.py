"""
L2 search loop for Phase 5c (size-bounded Frege).

Key difference from Phase 5b: transforms can enable cross-branch caching
(Extended Frege mode). The search loop passes this flag to the evaluator.
"""

import random
import sys
import os
from dataclasses import dataclass
from typing import List, Optional

_phase5c_dir = os.path.abspath(os.path.dirname(__file__))
_phase2_dir = os.path.abspath(os.path.join(_phase5c_dir, '..', 'phase2'))
if _phase5c_dir not in sys.path:
    sys.path.insert(0, _phase5c_dir)
if _phase2_dir not in sys.path:
    sys.path.insert(1, _phase2_dir)

import l3_monitor
from l3_monitor import L3Verdict

from distributions_frege import sample_d_plus, sample_d_minus, FregeInstance
from evaluator_frege import measure_distinguishing_advantage_batch
from transforms_frege import FREGE_TRANSFORM_REGISTRY, FregeTransform
from l3_rules_frege import inject_frege_rules

DELTA_THRESHOLD = 0.03


@dataclass
class FregeSearchResult:
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
    step_limit: int = 100,
    n_formulas: int = 8,
    n_trials: int = 5,
    seed: int = 42,
    verbose: bool = True,
) -> List[FregeSearchResult]:
    inject_frege_rules()

    rng = random.Random(seed)

    d_plus = sample_d_plus(n_formulas, seed=seed)
    d_minus = sample_d_minus(n_formulas, seed=seed + 1)

    baseline_adv = measure_distinguishing_advantage_batch(
        d_plus, d_minus, step_limit, n_trials, seed=seed
    )
    baseline_collapse = 1.0 - baseline_adv

    if verbose:
        print(f"Baseline: advantage={baseline_adv:.3f}, collapse={baseline_collapse:.3f}")
        print(f"Step limit: {step_limit}, formulas: {n_formulas}, trials: {n_trials}\n")

    results = []
    candidates = []

    for transform in FREGE_TRANSFORM_REGISTRY:
        sample_hyps, sample_tgt, n_p, n_h = d_plus[0]
        affected = transform.affects_target(sample_hyps, sample_tgt, n_p, n_h, rng)

        if affected:
            if verbose:
                print(f"  {transform.name}: rejected (affects target)")
            results.append(FregeSearchResult(
                transform_name=transform.name,
                advantage_before=baseline_adv,
                advantage_after=float('nan'),
                delta_collapse=float('nan'),
                delta_advantage=float('nan'),
                target_affected=True,
                is_candidate=False,
            ))
            continue

        # Apply transform to all instances
        transformed_plus = []
        for hyps, tgt, n_p, n_h in d_plus:
            t_rng = random.Random(seed + hash(transform.name) % 10000)
            new_hyps, new_tgt = transform.apply(hyps, tgt, n_p, n_h, t_rng)
            transformed_plus.append((new_hyps, new_tgt, n_p, n_h))

        transformed_minus = []
        for hyps, tgt, n_p, n_h in d_minus:
            t_rng = random.Random(seed + hash(transform.name) % 10000 + 1)
            new_hyps, new_tgt = transform.apply(hyps, tgt, n_p, n_h, t_rng)
            transformed_minus.append((new_hyps, new_tgt, n_p, n_h))

        # Pass enable_caching if the transform requests it
        caching = getattr(transform, 'enable_caching', False)

        adv_after = measure_distinguishing_advantage_batch(
            transformed_plus, transformed_minus, step_limit, n_trials,
            seed=seed + 1000, enable_caching=caching,
        )
        collapse_after = 1.0 - adv_after
        delta_collapse = collapse_after - baseline_collapse
        delta_adv = adv_after - baseline_adv

        is_candidate = delta_collapse > DELTA_THRESHOLD

        if verbose:
            status = "CANDIDATE" if is_candidate else "rejected"
            extra = " [CACHING]" if caching else ""
            print(f"  {transform.name}: delta_collapse={delta_collapse:+.3f} "
                  f"(adv {baseline_adv:.3f}->{adv_after:.3f}) [{status}]{extra}")

        result = FregeSearchResult(
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
                      f"({verdict.confidence}) -- {verdict.reason[:80]}...")

    return results


if __name__ == "__main__":
    results = search(step_limit=100, n_formulas=8, n_trials=5, seed=42, verbose=True)
    print("\n--- Summary ---")
    safe = [r for r in results if r.l3_verdict == "SAFE"]
    unsafe = [r for r in results if r.l3_verdict == "UNSAFE"]
    unknown = [r for r in results if r.l3_verdict == "UNKNOWN"]
    print(f"SAFE: {[r.transform_name for r in safe]}")
    print(f"UNSAFE: {[r.transform_name for r in unsafe]}")
    print(f"UNKNOWN: {[r.transform_name for r in unknown]}")
