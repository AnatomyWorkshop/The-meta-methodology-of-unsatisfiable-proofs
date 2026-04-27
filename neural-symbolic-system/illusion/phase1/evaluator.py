"""
Error rate evaluator via Monte Carlo sampling.

Given a circuit and a target function, estimates the error rate
(fraction of inputs on which the circuit disagrees with the target).
"""

import random
from typing import Callable, Tuple

from l1_circuit import AC0Circuit, parity


def monte_carlo_error_rate(
    circuit: AC0Circuit,
    target_fn: Callable[[Tuple[bool, ...]], bool],
    n_samples: int = 10000,
) -> float:
    """Estimate error rate of circuit against target function."""
    n = circuit.n_inputs
    errors = 0
    for _ in range(n_samples):
        x = tuple(random.choice([True, False]) for _ in range(n))
        if circuit.evaluate(x) != target_fn(x):
            errors += 1
    return errors / n_samples


def error_rate_with_confidence(
    circuit: AC0Circuit,
    target_fn: Callable[[Tuple[bool, ...]], bool],
    n_samples: int = 10000,
) -> Tuple[float, float]:
    """Return (error_rate, standard_error)."""
    rate = monte_carlo_error_rate(circuit, target_fn, n_samples)
    se = (rate * (1 - rate) / n_samples) ** 0.5
    return rate, se


def batch_error_rates(
    circuits: list,
    target_fn: Callable[[Tuple[bool, ...]], bool],
    n_samples: int = 5000,
) -> list:
    """Evaluate error rates for a batch of circuits."""
    return [monte_carlo_error_rate(c, target_fn, n_samples) for c in circuits]
