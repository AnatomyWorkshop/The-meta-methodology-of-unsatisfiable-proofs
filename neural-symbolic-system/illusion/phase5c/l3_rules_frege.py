"""
L3 rule extensions for Phase 5c: size-bounded Frege.

The critical UNKNOWN pattern: cross_branch_caching — this is the
Extended Frege operation. Whether cross-branch sharing genuinely reduces
proof size is the Frege vs Extended Frege separation (OPEN).
"""

import sys
import os

_phase5c_dir = os.path.abspath(os.path.dirname(__file__))
_phase2_dir = os.path.abspath(os.path.join(_phase5c_dir, '..', 'phase2'))
if _phase5c_dir not in sys.path:
    sys.path.insert(0, _phase5c_dir)
if _phase2_dir not in sys.path:
    sys.path.insert(1, _phase2_dir)

import l3_monitor
from l3_monitor import _UNSAFE_PATTERNS, _SAFE_PATTERNS


FREGE_UNSAFE_PATTERNS = [
    (r"formula_permutation",
     "formula permutation is a syntactic operation; "
     "proof validity is invariant under hypothesis reordering -- decidable in O(1)"),

    (r"\bidentity\b",
     "identity transform makes no change; trivially decidable"),

    (r"literal_negation",
     "literal negation is a local operation on each variable occurrence; "
     "decidable by syntactic inspection in O(n)"),
]


FREGE_SAFE_PATTERNS = [
    (r"variable_restriction_p0\.[1-4]",
     "random variable restriction preserves PHP unsatisfiability structure; "
     "deciding whether a size-bounded Frege proof loses its refutation power "
     "under random variable fixing requires exponential search over all possible "
     "restrictions",
     "Krajicek 1994; Pitassi et al. 1993, Frege lower bound techniques"),

    (r"hypothesis_projection_p0\.[6-9]",
     "random hypothesis projection preserves the core PHP axioms with high probability; "
     "deciding whether a size-bounded Frege proof loses distinguishing advantage "
     "under random hypothesis removal requires exponential search",
     "Krajicek 1995, Bounded Arithmetic and Proof Complexity"),

    (r"hypothesis_weakening_e[12]",
     "hypothesis weakening adds random disjuncts, making hypotheses logically weaker; "
     "deciding whether weakened hypotheses still admit short proofs "
     "requires searching over all possible proof structures",
     "Krajicek 1995, Proof Complexity"),
]


FREGE_UNKNOWN_PATTERNS = [
    (r"cross_branch_caching",
     "cross-branch caching enables reuse of intermediate derivations across "
     "proof branches -- this is exactly the Extended Frege abbreviation mechanism. "
     "Whether this reuse genuinely reduces proof size (the Frege vs Extended Frege "
     "separation) is a major open problem in proof complexity. "
     "No unconditional separation is known; no proof of equivalence exists.",
     "Cook & Reckhow 1979; Krajicek & Pudlak 1989; "
     "Frege vs Extended Frege p-simulation is OPEN"),

    (r"subformula_elimination",
     "subformula elimination introduces abbreviation variables -- "
     "the input-level analog of Extended Frege. Whether abbreviations "
     "genuinely reduce proof size is open.",
     "Cook & Reckhow 1979; the p-simulation question is open"),
]


_injected = False


def inject_frege_rules():
    global _injected
    if _injected:
        return

    for pattern, reason in FREGE_UNSAFE_PATTERNS:
        _UNSAFE_PATTERNS.append((pattern, reason))

    for pattern, reason, ref in FREGE_SAFE_PATTERNS:
        _SAFE_PATTERNS.append((pattern, reason, ref))

    _patch_l3_monitor_for_unknown()
    _injected = True


def _patch_l3_monitor_for_unknown():
    import re
    original_check = l3_monitor.check

    def patched_check(transform_name, description="", verbose=True):
        result = original_check(transform_name, description=description, verbose=False)

        if result.verdict == "UNKNOWN":
            text = (transform_name + " " + description).lower()
            for pattern, reason, reference in FREGE_UNKNOWN_PATTERNS:
                if re.search(pattern, text):
                    from l3_monitor import L3Verdict
                    result = L3Verdict(
                        transform_name=transform_name,
                        verdict="UNKNOWN",
                        reason=reason,
                        reference=reference,
                        confidence="low",
                    )
                    break

        if verbose:
            print(result.l3_question)
        return result

    l3_monitor.check = patched_check


if __name__ == "__main__":
    inject_frege_rules()
    import l3_monitor as m

    test_cases = [
        "variable_restriction_p0.2",
        "variable_restriction_p0.3",
        "hypothesis_projection_p0.7",
        "hypothesis_projection_p0.8",
        "formula_permutation",
        "identity",
        "cross_branch_caching_f1.0",
        "subformula_elimination_n2",
        "hypothesis_weakening_e1",
        "literal_negation_p0.3",
    ]

    print("L3 Frege (size metric) rule test:\n")
    for name in test_cases:
        v = m.check(name, verbose=False)
        print(f"  {name}: {v.verdict} ({v.confidence})")
