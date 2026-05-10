"""
Evaluator for Phase 5c (size-bounded Frege).

Measures distinguishing advantage and collapse over batches of D+/D- instances.
Supports enable_caching flag for Extended Frege mode.
"""

from typing import List
from distributions_frege import FregeInstance
from l1_frege import measure_collapse, distinguishing_advantage


def measure_collapse_batch(
    instances: List[FregeInstance],
    step_limit: int,
    n_trials: int = 5,
    seed: int = None,
    enable_caching: bool = False,
) -> float:
    if not instances:
        return 1.0
    collapses = []
    for idx, (hyps, tgt, n_p, n_h) in enumerate(instances):
        s = seed * 10000 + idx if seed is not None else None
        c = measure_collapse(formula=tgt, hypotheses=hyps,
                             step_limit=step_limit, n_trials=n_trials, seed=s,
                             enable_caching=enable_caching)
        collapses.append(c)
    return sum(collapses) / len(collapses)


def measure_distinguishing_advantage_batch(
    d_plus: List[FregeInstance],
    d_minus: List[FregeInstance],
    step_limit: int,
    n_trials: int = 5,
    seed: int = None,
    enable_caching: bool = False,
) -> float:
    def mean_adv(instances, offset):
        advs = []
        for idx, (hyps, tgt, n_p, n_h) in enumerate(instances):
            s = seed * 10000 + offset + idx if seed is not None else None
            a = distinguishing_advantage(
                formula=tgt, hypotheses=hyps,
                step_limit=step_limit, n_trials=n_trials, seed=s,
                enable_caching=enable_caching,
            )
            advs.append(a)
        return sum(advs) / len(advs) if advs else 0.0

    adv_plus = mean_adv(d_plus, 0)
    adv_minus = mean_adv(d_minus, 100000)
    return abs(adv_plus - adv_minus)


if __name__ == "__main__":
    from distributions_frege import sample_d_plus, sample_d_minus

    print("Baseline calibration (size metric)...")
    d_plus = sample_d_plus(6, seed=42)
    d_minus = sample_d_minus(6, seed=43)

    for sl in [50, 80, 100, 150]:
        adv = measure_distinguishing_advantage_batch(
            d_plus, d_minus, sl, n_trials=5, seed=42
        )
        adv_ext = measure_distinguishing_advantage_batch(
            d_plus, d_minus, sl, n_trials=5, seed=42, enable_caching=True
        )
        print(f"  step_limit={sl:3d}: std_adv={adv:.3f}, ext_adv={adv_ext:.3f}")
