"""
L3 classification rules for Phase 6: Riemann Hypothesis closure search.

Classifies candidate operators as:
  SAFE: valid closure path (satisfies structural requirements)
  UNSAFE: not a valid closure (circular, statistical-only, or internal to M_an)
  UNKNOWN: partial match, structural status undetermined
"""

import re
from dataclasses import dataclass
from typing import Optional

from evaluator_rh import ClosureScore


@dataclass
class L3Verdict:
    name: str
    verdict: str  # SAFE, UNSAFE, UNKNOWN
    reason: str
    reference: str
    confidence: str
    four_law_summary: str


# Thresholds
COMPOSITE_CANDIDATE_THRESHOLD = 0.45
SPECTRAL_MATCH_HIGH = 0.6
DUALITY_HIGH = 0.95


def classify(score: ClosureScore) -> L3Verdict:
    """
    Classify a candidate operator based on its closure score.
    """
    name = score.name

    # --- UNSAFE patterns ---

    # Circular construction (uses zeros as input)
    if re.search(r"connes_truncated", name):
        return L3Verdict(
            name=name,
            verdict="UNSAFE",
            reason="circular construction: operator spectrum is defined as zeta zeros. "
                   "This is not a closure — it assumes what it needs to prove. "
                   "Serves only as upper-bound reference.",
            reference="Connes 1999; circularity noted in Sarnak 2005",
            confidence="high",
            four_law_summary="Duality: trivial (by construction). "
                            "Rigidity: yes. Symmetry: inherited. Reduction: no (no prime encoding).",
        )

    # GUE random matrix — statistical match only
    if re.search(r"gue_n\d+", name):
        return L3Verdict(
            name=name,
            verdict="UNSAFE",
            reason="GUE random matrices match pair correlation statistics of zeta zeros "
                   "(Montgomery-Odlyzko law) but do NOT match individual zeros. "
                   "No prime encoding, no functional equation structure. "
                   "Statistical universality, not spectral duality.",
            reference="Montgomery 1973; Odlyzko 1987; Katz & Sarnak 1999",
            confidence="high",
            four_law_summary="Duality: statistical only (not bijective). "
                            "Rigidity: yes (self-adjoint). Symmetry: no. Reduction: no.",
        )

    # --- SAFE patterns ---

    # Hecke operators with prime encoding + symmetry
    if re.search(r"hecke", name):
        if score.reduction_score >= 0.75 and score.rigidity_score >= 1.0:
            return L3Verdict(
                name=name,
                verdict="SAFE",
                reason="Hecke operators encode prime structure via modular arithmetic "
                       "and possess functional equation symmetry. Their L-functions "
                       "satisfy GRH. This is a structurally valid closure path: "
                       "the operator lives in M_op (outside M_an), encodes primes, "
                       "and its self-adjointness implies spectral reality.",
                reference="Hecke 1937; Selberg 1956; Langlands program",
                confidence="medium",
                four_law_summary="Duality: partial (L-function zeros, not full zeta). "
                                "Rigidity: yes. Symmetry: yes (functional equation). "
                                "Reduction: yes (primes -> Hecke eigenvalues).",
            )

    # --- UNKNOWN patterns ---

    # Berry-Keating PT-symmetric (Bender-Brody-Mueller type)
    if re.search(r"berry_keating_pt_symmetric", name):
        return L3Verdict(
            name=name,
            verdict="UNKNOWN",
            reason="PT-symmetric Berry-Keating Hamiltonian (Bender-Brody-Mueller 2017). "
                   "Non-Hermitian but PT-symmetric: if PT symmetry is unbroken, "
                   "spectrum is entirely real. The functional equation s <-> 1-s "
                   "maps to PT symmetry (P implements parity, T implements conjugation). "
                   "This is the strongest known structural candidate: it naturally "
                   "encodes the functional equation as a physical symmetry. "
                   "Open question: whether the specific potential produces exact zeta zeros.",
            reference="Bender, Brody & Mueller 2017; Berry & Keating 1999; "
                      "Sierra 2019; Bender 2007 (PT-symmetric quantum mechanics)",
            confidence="medium",
            four_law_summary="Duality: conjectured (spectrum <-> zeros). "
                            "Rigidity: PT-unbroken = effectively self-adjoint (real spectrum). "
                            "Symmetry: yes (PT implements functional equation). "
                            "Reduction: no explicit prime encoding.",
        )

    # Berry-Keating family (standard boundary conditions)
    if re.search(r"berry_keating", name):
        return L3Verdict(
            name=name,
            verdict="UNKNOWN",
            reason="Berry-Keating H=xp+px is the simplest candidate for the "
                   "Hilbert-Polya operator. Self-adjointness depends on boundary "
                   "conditions (domain of definition). Spectral match is partial. "
                   "Whether a specific boundary condition produces exact zeta zeros "
                   "is an open problem in mathematical physics.",
            reference="Berry & Keating 1999; Sierra & Townsend 2008; "
                      "Bender, Brody & Mueller 2017",
            confidence="low",
            four_law_summary="Duality: conjectured (spectrum <-> zeros). "
                            "Rigidity: boundary-dependent. Symmetry: periodic BC only. "
                            "Reduction: no explicit prime encoding.",
        )

    # Prime-encoding operator
    if re.search(r"prime_zeta", name):
        return L3Verdict(
            name=name,
            verdict="UNKNOWN",
            reason="Operator with explicit prime encoding (diag=log(p), coupling via primes). "
                   "Self-adjoint by construction. Encodes prime structure directly. "
                   "But spectral match to zeta zeros is not established — "
                   "the coupling structure may not produce the correct spectrum. "
                   "Whether prime-encoding operators can reproduce zeta zeros "
                   "is related to the inverse spectral problem.",
            reference="Hilbert-Polya conjecture; inverse spectral theory; "
                      "Lapidus & van Frankenhuijsen 2006",
            confidence="low",
            four_law_summary="Duality: unknown (spectrum may not match zeros). "
                            "Rigidity: yes. Symmetry: no. "
                            "Reduction: yes (primes encoded directly).",
        )

    # Default: UNKNOWN
    return L3Verdict(
        name=name,
        verdict="UNKNOWN",
        reason="Candidate does not match any known classification pattern. "
               "Structural status undetermined.",
        reference="",
        confidence="low",
        four_law_summary="Undetermined.",
    )


if __name__ == "__main__":
    from l1_rh import zeta_zeros
    from operators_rh import build_candidate_registry
    from evaluator_rh import evaluate_candidate

    zeros = zeta_zeros(30)
    candidates = build_candidate_registry(30, zeros)

    print("L3 Classification of RH closure candidates:\n")
    for c in candidates:
        score = evaluate_candidate(c, zeros)
        verdict = classify(score)
        print(f"  {verdict.name}: [{verdict.verdict}] ({verdict.confidence})")
        print(f"    {verdict.reason[:100]}...")
        print()
