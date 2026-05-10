"""
L3 rule extensions for Frege proof complexity domain.

Injects Frege-specific SAFE/UNSAFE/UNKNOWN patterns into the Phase 1 L3 monitor.
Call inject_frege_rules() before running L3 checks on Frege candidates.

The core L3 question for Phase 5b:
  "Can a bounded-depth Frege proof system decide property P?"

Key distinction:
  SAFE   — deciding P requires exponential search (e.g., over all restrictions)
  UNSAFE — deciding P is a local syntactic check (e.g., formula depth)
  UNKNOWN — P relates to an open problem (Frege vs Extended Frege separation)
"""

import sys
import os

_phase5b_dir = os.path.abspath(os.path.dirname(__file__))
_phase2_dir = os.path.abspath(os.path.join(_phase5b_dir, '..', 'phase2'))
if _phase5b_dir not in sys.path:
    sys.path.insert(0, _phase5b_dir)
if _phase2_dir not in sys.path:
    sys.path.insert(1, _phase2_dir)

import l3_monitor
from l3_monitor import _UNSAFE_PATTERNS, _SAFE_PATTERNS


FREGE_UNSAFE_PATTERNS = [
    (r"depth_truncation_k\d+",
     "depth truncation is a local operation on each formula; "
     "checking formula depth is O(n) and decidable within the proof system in polynomial time"),

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
     "deciding whether a bounded-depth Frege proof loses its refutation power "
     "under random variable fixing requires exponential search over all possible "
     "restrictions -- this is the Frege analog of depth lower bound techniques",
     "Krajicek 1994, depth-d Frege lower bounds; Pitassi et al. 1993"),

    (r"hypothesis_projection_p0\.[6-9]",
     "random hypothesis projection preserves the core PHP axioms with high probability; "
     "deciding whether a bounded-depth Frege proof loses distinguishing advantage "
     "under random hypothesis removal requires exponential search",
     "Krajicek 1995, Bounded Arithmetic and Proof Complexity"),

    (r"hypothesis_weakening_e[12]",
     "hypothesis weakening adds random disjuncts, making hypotheses logically weaker; "
     "deciding whether weakened hypotheses still admit short bounded-depth proofs "
     "requires searching over all possible proof structures -- not locally decidable",
     "Krajicek 1995, Proof Complexity; weakening preserves soundness"),
]


FREGE_UNKNOWN_PATTERNS = [
    (r"subformula_elimination_n[1-9]",
     "subformula elimination introduces abbreviation variables -- this is exactly "
     "the Extended Frege operation. Whether abbreviations genuinely reduce proof size "
     "(the Frege vs Extended Frege separation) is a major open problem in proof complexity. "
     "Cannot determine decidability within bounded-depth Frege from current theory.",
     "Cook & Reckhow 1979; Krajicek & Pudlak 1989; "
     "the p-simulation of Frege by Extended Frege is open"),
]


_injected = False


def inject_frege_rules():
    """Inject Frege-specific rules into the Phase 1 L3 monitor."""
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
    """
    Patch l3_monitor.check() to consult FREGE_UNKNOWN_PATTERNS
    before returning the default UNKNOWN verdict.
    """
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
        "depth_truncation_k2",
        "depth_truncation_k3",
        "formula_permutation",
        "identity",
        "subformula_elimination_n2",
        "subformula_elimination_n3",
        "hypothesis_weakening_e1",
        "hypothesis_weakening_e2",
        "literal_negation_p0.3",
    ]

    print("L3 Frege rule test:\n")
    for name in test_cases:
        v = m.check(name, verbose=False)
        print(f"  {name}: {v.verdict} ({v.confidence})")
