"""
Evaluator for Frege proof complexity experiments.

Measures distinguishing advantage and collapse over batches of D+/D- instances.
Parallel to phase5/evaluator_resolution.py but uses depth-bounded Frege prover.
"""

from typing import List
from distributions_frege import FregeInstance
from l1_frege import measure_collapse, distinguishing_advantage


def measure_collapse_batch(
    instances: List[FregeInstance],
    depth_limit: int,
    n_trials: int = 5,
    seed: int = None,
) -> float:
    """Average collapse over a batch of Frege instances."""
    if not instances:
        return 1.0
    collapses = []
    for idx, (hyps, tgt, n_p, n_h) in enumerate(instances):
        s = seed * 10000 + idx if seed is not None else None
        c = measure_collapse(hyps=hyps, formula=tgt, depth_limit=depth_limit,
                             n_trials=n_trials, seed=s)
        collapses.append(c)
    return sum(collapses) / len(collapses)


def measure_distinguishing_advantage_batch(
    d_plus: List[FregeInstance],
    d_minus: List[FregeInstance],
    depth_limit: int,
    n_trials: int = 5,
    seed: int = None,
) -> float:
    """
    Distinguishing advantage of bounded-depth Frege at depth_limit:
    |mean_advantage(D+) - mean_advantage(D-)|
    """
    def mean_adv(instances, offset):
        advs = []
        for idx, (hyps, tgt, n_p, n_h) in enumerate(instances):
            s = seed * 10000 + offset + idx if seed is not None else None
            a = distinguishing_advantage(
                formula=tgt, hypotheses=hyps,
                depth_limit=depth_limit, n_trials=n_trials, seed=s
            )
            advs.append(a)
        return sum(advs) / len(advs) if advs else 0.0

    adv_plus = mean_adv(d_plus, 0)
    adv_minus = mean_adv(d_minus, 100000)
    return abs(adv_plus - adv_minus)


def baseline_collapse(
    n_formulas: int = 10,
    depth_limit: int = 5,
    n_trials: int = 5,
    seed: int = 42,
) -> float:
    """
    Baseline collapse: average over D+ and D- without any transform.
    collapse = 1 - distinguishing_advantage
    """
    from distributions_frege import sample_d_plus, sample_d_minus
    d_plus = sample_d_plus(n_formulas // 2, seed=seed)
    d_minus = sample_d_minus(n_formulas // 2, seed=seed + 1)
    adv = measure_distinguishing_advantage_batch(
        d_plus, d_minus, depth_limit, n_trials, seed
    )
    return 1.0 - adv


if __name__ == "__main__":
    from distributions_frege import sample_d_plus, sample_d_minus

    print("Baseline calibration...")
    d_plus = sample_d_plus(6, seed=42)
    d_minus = sample_d_minus(6, seed=43)

    for dl in [3, 4, 5, 6]:
        adv = measure_distinguishing_advantage_batch(
            d_plus, d_minus, dl, n_trials=5, seed=42
        )
        collapse = 1.0 - adv
        print(f"  depth_limit={dl}: advantage={adv:.3f}, collapse={collapse:.3f}")
