"""
Evaluator for monotone circuit experiments.

Key metric: distinguishing advantage
  adv(C) = |Pr[C(G)=1 | G~D+] - Pr[C(G)=1 | G~D-]|

Collapse = 1 - advantage (matches Phase 1 convention: higher = more degraded).
"""

import random
from typing import Callable, Tuple
from distributions import sample_d_plus, sample_d_minus


def acceptance_rate(circuit, sampler: Callable, n_samples: int = 500) -> float:
    """Pr[C(G)=1] where G drawn from sampler."""
    accepts = sum(1 for _ in range(n_samples) if circuit.evaluate(sampler()))
    return accepts / n_samples


def distinguishing_advantage(circuit, n: int, k: int, n_samples: int = 500) -> float:
    """Estimate |Pr[C(G)=1 | G~D+] - Pr[C(G)=1 | G~D-]|."""
    rate_plus = acceptance_rate(circuit, lambda: sample_d_plus(n, k), n_samples)
    rate_minus = acceptance_rate(circuit, lambda: sample_d_minus(n, k), n_samples)
    return abs(rate_plus - rate_minus)


def measure_collapse_monotone(circuit, n: int, k: int, n_samples: int = 300) -> float:
    """
    Collapse = 1 - distinguishing_advantage.
    1 = fully collapsed (cannot distinguish D+ from D-).
    0 = no collapse (perfect distinguisher).
    """
    adv = distinguishing_advantage(circuit, n, k, n_samples)
    return max(0.0, min(1.0, 1.0 - adv))
