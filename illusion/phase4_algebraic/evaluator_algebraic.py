"""
Evaluator for algebraic circuit experiments.

Key metric: distinguishing advantage
  adv(C) = |Pr[C(M) ≠ 0 | M~D+] - Pr[C(M) ≠ 0 | M~D-]|

Collapse = 1 - advantage (matches Phase 1/3 convention: higher = more degraded).

The circuit "accepts" a matrix if its output is nonzero mod p.
D+ matrices (random) should trigger nonzero output more often than D- (rank-1).
A circuit that cannot distinguish them has high collapse.
"""

import random
from typing import Callable, Tuple
from distributions import sample_d_plus, sample_d_minus


def acceptance_rate(circuit, sampler: Callable, n_samples: int = 300) -> float:
    """Pr[C(M) ≠ 0] where M drawn from sampler."""
    accepts = sum(1 for _ in range(n_samples) if circuit.evaluate(sampler()) != 0)
    return accepts / n_samples


def distinguishing_advantage(circuit, n: int, p: int, n_samples: int = 300) -> float:
    """Estimate |Pr[C(M)≠0 | M~D+] - Pr[C(M)≠0 | M~D-]|."""
    rate_plus  = acceptance_rate(circuit, lambda: sample_d_plus(n, p),  n_samples)
    rate_minus = acceptance_rate(circuit, lambda: sample_d_minus(n, p), n_samples)
    return abs(rate_plus - rate_minus)


def measure_collapse_algebraic(circuit, n: int, p: int, n_samples: int = 300) -> float:
    """
    Collapse = 1 - distinguishing_advantage.
    1 = fully collapsed (cannot distinguish D+ from D-).
    0 = no collapse (perfect distinguisher).
    """
    adv = distinguishing_advantage(circuit, n, p, n_samples)
    return max(0.0, min(1.0, 1.0 - adv))
