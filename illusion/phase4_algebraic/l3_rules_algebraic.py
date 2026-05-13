"""
L3 rule extensions for algebraic circuit domain.

Injects algebraic-specific SAFE/UNSAFE patterns into the Phase 1 L3 monitor.
Call inject_algebraic_rules() before running L3 checks on algebraic candidates.

The core L3 question changes from:
  "Can an AC^0 circuit decide property P?"
to:
  "Can a polynomial-size algebraic circuit over GF(p) decide property P?"

Key principle: a property P is SAFE (self-referentially safe) if deciding
whether a circuit satisfies P requires computing something at least as hard
as Permanent — i.e., the decision problem is #P-hard or harder.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))
from l3_monitor import _UNSAFE_PATTERNS, _SAFE_PATTERNS


ALGEBRAIC_UNSAFE_PATTERNS = [
    (r"field_reduction",
     "reducing inputs modulo q is a local operation on each variable; "
     "deciding whether a circuit's output changes under field reduction "
     "is decidable by an algebraic circuit of polynomial size"),

    (r"scalar_multiplication",
     "multiplying all inputs by a scalar is a linear operation; "
     "the circuit's behavior under scalar multiplication is determined "
     "by its degree, which is computable in polynomial time"),

    (r"input_permutation",
     "permuting matrix rows is a structural rewrite; "
     "Permanent is invariant under row permutation, so this property "
     "is trivially decidable"),

    (r"identity",
     "identity transform induces no change; trivially decidable"),

    (r"degree_truncation_d[0-9]+",
     "degree truncation zeroes out specific gate types by depth; "
     "the truncation criterion (gate depth) is a local structural property "
     "decidable by inspecting the circuit description in polynomial time"),

    (r"monomial_elimination_p0\.[0-4]",
     "aggressive row elimination (survival < 0.5) destroys the Permanent "
     "function itself; the induced property is trivially decidable"),
]


ALGEBRAIC_SAFE_PATTERNS = [
    (r"algebraic_restriction_p0\.[23456]",
     "random algebraic restriction (p ≤ 0.6) preserves the Permanent structure "
     "but degrades circuit distinguishing power; deciding whether a circuit "
     "loses distinguishing advantage under random variable fixing requires "
     "evaluating the circuit on exponentially many restricted inputs — "
     "this is the algebraic analog of the Razborov-Smolensky method",
     "Razborov-Smolensky 1987/1990, algebraic circuit lower bounds"),

    (r"monomial_elimination_p0\.[5-9]",
     "moderate row elimination preserves the Permanent function on average "
     "but degrades circuit performance; deciding whether a circuit loses "
     "distinguishing advantage under random row removal requires exponential "
     "sampling over all possible row subsets — not decidable in algebraic P/poly",
     "Valiant 1979, Permanent requires exponential algebraic circuits"),
]


_injected = False


def inject_algebraic_rules():
    """Inject algebraic-specific rules into the Phase 1 L3 monitor."""
    global _injected
    if _injected:
        return

    for pattern, reason in ALGEBRAIC_UNSAFE_PATTERNS:
        _UNSAFE_PATTERNS.append((pattern, reason))

    for pattern, reason, ref in ALGEBRAIC_SAFE_PATTERNS:
        _SAFE_PATTERNS.append((pattern, reason, ref))

    _injected = True
