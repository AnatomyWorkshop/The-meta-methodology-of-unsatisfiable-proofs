"""
L3 rule extensions for Resolution proof complexity domain.

Injects Resolution-specific SAFE/UNSAFE/UNKNOWN patterns into the Phase 1 L3 monitor.
Call inject_resolution_rules() before running L3 checks on Resolution candidates.

The core L3 question changes from:
  "Can an AC^0 circuit decide property P?"
to:
  "Can a polynomial-size Resolution proof system decide property P?"

Key distinction for Phase 5:
  SAFE   — deciding P requires exponential sampling (e.g., over all restrictions)
  UNSAFE — deciding P is a local syntactic check (e.g., clause width)
  UNKNOWN — P relates to an open problem in proof complexity (e.g., Extended Resolution)
"""

import sys
import os

_phase5_dir = os.path.abspath(os.path.dirname(__file__))
_phase2_dir = os.path.abspath(os.path.join(_phase5_dir, '..', 'phase2'))
if _phase5_dir not in sys.path:
    sys.path.insert(0, _phase5_dir)
if _phase2_dir not in sys.path:
    sys.path.insert(1, _phase2_dir)

import l3_monitor
from l3_monitor import _UNSAFE_PATTERNS, _SAFE_PATTERNS


RESOLUTION_UNSAFE_PATTERNS = [
    (r"width_truncation_k\d+",
     "width truncation is a local operation on each clause; "
     "checking clause width is O(n) and decidable within the proof system in polynomial time"),

    (r"clause_permutation",
     "clause permutation is a syntactic operation; "
     "proof validity is invariant under clause reordering — decidable in O(1)"),

    (r"\bidentity\b",
     "identity transform makes no change; trivially decidable"),

    (r"literal_negation",
     "literal negation is a local operation on each literal; "
     "decidable by syntactic inspection in O(n)"),

    (r"variable_renaming",
     "variable renaming is an isomorphism; "
     "proof structure is preserved — decidable in O(n)"),
]


RESOLUTION_SAFE_PATTERNS = [
    (r"clause_restriction_p0\.[1-4]",
     "random clause restriction preserves PHP unsatisfiability structure; "
     "deciding whether a proof system loses width advantage under random variable fixing "
     "requires exponential sampling over all possible restrictions — "
     "this is the Resolution analog of Håstad's random restriction",
     "Ben-Sasson & Wigderson 2001, width lower bounds for Resolution"),

    (r"clause_projection_p0\.[6-9]",
     "random clause projection preserves the core PHP axioms with high probability; "
     "deciding whether a proof system loses distinguishing advantage under random clause removal "
     "requires exponential search over all possible projections",
     "Ben-Sasson & Wigderson 2001, width method for Resolution"),
]


# UNKNOWN patterns: relate to open problems in proof complexity.
# These are injected into a separate list that check() consults before returning UNKNOWN.
RESOLUTION_UNKNOWN_PATTERNS = [
    (r"variable_elimination_p0\.[1-4]",
     "variable elimination corresponds to existential quantification over proof variables; "
     "this relates to Extended Resolution — the separation between Resolution and "
     "Extended Resolution is an open problem in proof complexity. "
     "Cannot determine decidability within Resolution from current theory.",
     "Krajíček 1995, Proof Complexity; Cook & Reckhow 1979, Extended Resolution"),
]


_injected = False


def inject_resolution_rules():
    """Inject Resolution-specific rules into the Phase 1 L3 monitor."""
    global _injected
    if _injected:
        return

    for pattern, reason in RESOLUTION_UNSAFE_PATTERNS:
        _UNSAFE_PATTERNS.append((pattern, reason))

    for pattern, reason, ref in RESOLUTION_SAFE_PATTERNS:
        _SAFE_PATTERNS.append((pattern, reason, ref))

    # Inject UNKNOWN patterns: patch the check() function to consult them
    # before falling through to the default UNKNOWN verdict.
    _patch_l3_monitor_for_unknown()

    _injected = True


def _patch_l3_monitor_for_unknown():
    """
    Patch l3_monitor.check() to consult RESOLUTION_UNKNOWN_PATTERNS
    before returning the default UNKNOWN verdict.
    This preserves the existing check() logic and adds domain-specific
    UNKNOWN reasons with references.
    """
    import re
    original_check = l3_monitor.check

    def patched_check(transform_name, description="", verbose=True):
        # Run original check first
        result = original_check(transform_name, description=description, verbose=False)

        # If original returned UNKNOWN, check if we have a specific reason
        if result.verdict == "UNKNOWN":
            text = (transform_name + " " + description).lower()
            for pattern, reason, reference in RESOLUTION_UNKNOWN_PATTERNS:
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
    inject_resolution_rules()
    import l3_monitor as m

    test_cases = [
        "clause_restriction_p0.3",
        "clause_restriction_p0.4",
        "clause_projection_p0.7",
        "width_truncation_k2",
        "width_truncation_k3",
        "clause_permutation",
        "identity",
        "variable_elimination_p0.2",
        "variable_elimination_p0.3",
        "literal_negation_p0.3",
    ]

    print("L3 Resolution rule test:\n")
    for name in test_cases:
        v = m.check(name, verbose=False)
        print(f"  {name}: {v.verdict} ({v.confidence})")
