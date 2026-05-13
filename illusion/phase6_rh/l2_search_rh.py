"""
L2 search loop for Phase 6: Riemann Hypothesis closure search.

Evaluates all candidate operators, ranks them by closure score,
and passes candidates above threshold to L3 for classification.
"""

from typing import List
from dataclasses import dataclass, field

from l1_rh import zeta_zeros
from operators_rh import build_candidate_registry, OperatorCandidate
from evaluator_rh import evaluate_candidate, ClosureScore
from l3_rules_rh import classify, L3Verdict


CANDIDATE_THRESHOLD = 0.45


@dataclass
class RHSearchResult:
    name: str
    composite_score: float
    spectral_match: float
    duality_score: float
    rigidity_score: float
    symmetry_score: float
    reduction_score: float
    is_candidate: bool
    l3_verdict: str = ""
    l3_reason: str = ""
    l3_reference: str = ""
    l3_confidence: str = ""
    l3_four_law_summary: str = ""
    description: str = ""


def search(n_zeros: int = 50, n_dim: int = 50, verbose: bool = True) -> List[RHSearchResult]:
    """
    Run the closure search over all candidate operator families.
    """
    if verbose:
        print(f"Computing first {n_zeros} zeta zeros...")
    zeros = zeta_zeros(n_zeros)

    if verbose:
        print(f"Building candidate operators (dim={n_dim})...")
    candidates = build_candidate_registry(n_dim, zeros)

    if verbose:
        print(f"Evaluating {len(candidates)} candidates...\n")

    results = []

    for candidate in candidates:
        score = evaluate_candidate(candidate, zeros)

        is_candidate = score.composite_score >= CANDIDATE_THRESHOLD

        result = RHSearchResult(
            name=candidate.name,
            composite_score=score.composite_score,
            spectral_match=score.spectral_match,
            duality_score=score.duality_score,
            rigidity_score=score.rigidity_score,
            symmetry_score=score.symmetry_score,
            reduction_score=score.reduction_score,
            is_candidate=is_candidate,
            description=candidate.description,
        )

        if is_candidate:
            verdict = classify(score)
            result.l3_verdict = verdict.verdict
            result.l3_reason = verdict.reason
            result.l3_reference = verdict.reference
            result.l3_confidence = verdict.confidence
            result.l3_four_law_summary = verdict.four_law_summary

        if verbose:
            status = "CANDIDATE" if is_candidate else "rejected"
            l3_str = f" -> [{result.l3_verdict}]" if is_candidate else ""
            print(f"  {candidate.name}: score={score.composite_score:.3f} [{status}]{l3_str}")

        results.append(result)

    results.sort(key=lambda r: r.composite_score, reverse=True)

    if verbose:
        print(f"\n--- Summary ---")
        cands = [r for r in results if r.is_candidate]
        safe = [r for r in cands if r.l3_verdict == "SAFE"]
        unsafe = [r for r in cands if r.l3_verdict == "UNSAFE"]
        unknown = [r for r in cands if r.l3_verdict == "UNKNOWN"]
        print(f"  Candidates: {len(cands)}")
        print(f"  SAFE: {[r.name for r in safe]}")
        print(f"  UNSAFE: {[r.name for r in unsafe]}")
        print(f"  UNKNOWN: {[r.name for r in unknown]}")

    return results


if __name__ == "__main__":
    search(n_zeros=30, n_dim=30, verbose=True)
