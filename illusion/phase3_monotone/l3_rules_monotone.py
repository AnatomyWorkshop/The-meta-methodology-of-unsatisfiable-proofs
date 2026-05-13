"""
L3 rule extensions for monotone circuit domain.

Injects monotone-specific SAFE/UNSAFE patterns into the Phase 1 L3 monitor.
Call inject_monotone_rules() before running L3 checks on monotone candidates.

The core L3 question changes from:
  "Can an AC^0 circuit decide property P?"
to:
  "Can a polynomial-size monotone circuit decide property P?"
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))
from l3_monitor import _UNSAFE_PATTERNS, _SAFE_PATTERNS


MONOTONE_UNSAFE_PATTERNS = [
    (r"edge_deletion", "setting inputs to 0 in a monotone circuit is a monotone "
                       "operation; deciding whether a circuit collapses under edge "
                       "deletion is decidable by a monotone circuit of polynomial size"),

    (r"gate_elevation", "replacing AND gates with OR gates is a local structural "
                        "rewrite; decidable by inspecting the circuit description"),

    (r"subgraph.*p0\.[0-4]", "aggressive subgraph projection (survival < 0.5) "
                              "destroys the target function; the induced property "
                              "is trivially decidable"),
]


MONOTONE_SAFE_PATTERNS = [
    (r"distribution_switch", "the property 'circuit cannot distinguish D+ from D-' "
                             "requires evaluating the circuit on exponentially many "
                             "graph samples from both distributions; no polynomial-size "
                             "monotone circuit can decide this",
     "Razborov 1985, Approximation Method"),

    (r"subgraph_projection.*p0\.[5-9]", "moderate subgraph projection preserves the "
                                         "target function but degrades circuit "
                                         "distinguishing power; deciding whether a "
                                         "circuit loses distinguishing advantage under "
                                         "random vertex removal requires exponential "
                                         "sampling",
     "Razborov 1985, monotone circuit lower bounds"),

    (r"edge_deletion_p0\.1", "mild edge deletion (p=0.1) preserves clique structure "
                              "but degrades circuit performance; deciding the degree "
                              "of degradation requires exponential evaluation",
     "analog of Hastad switching lemma for monotone setting"),
]


_injected = False


def inject_monotone_rules():
    """Inject monotone-specific rules into the Phase 1 L3 monitor."""
    global _injected
    if _injected:
        return

    for pattern, reason in MONOTONE_UNSAFE_PATTERNS:
        _UNSAFE_PATTERNS.append((pattern, reason))

    for pattern, reason, ref in MONOTONE_SAFE_PATTERNS:
        _SAFE_PATTERNS.append((pattern, reason, ref))

    _injected = True
