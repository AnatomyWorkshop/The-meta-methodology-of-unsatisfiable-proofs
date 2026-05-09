import random
from typing import List, Tuple
from distributions import Formula, sample_d_plus, sample_d_minus
from l1_resolution import measure_collapse, distinguishing_advantage


def measure_collapse_batch(
    formulas: List[Tuple[Formula, int, int]],
    width_limit: int,
    n_trials: int = 5,
    seed: int = None,
) -> float:
    """Average collapse over a batch of formulas."""
    if not formulas:
        return 1.0
    collapses = []
    for idx, (formula, n_p, n_h) in enumerate(formulas):
        s = seed * 10000 + idx if seed is not None else None
        c = measure_collapse(formula, n_p, n_h, width_limit, n_trials, s)
        collapses.append(c)
    return sum(collapses) / len(collapses)


def measure_distinguishing_advantage_batch(
    d_plus: List[Tuple[Formula, int, int]],
    d_minus: List[Tuple[Formula, int, int]],
    width_limit: int,
    n_trials: int = 5,
    seed: int = None,
) -> float:
    """
    Distinguishing advantage of the proof system at width_limit:
    |mean_advantage(D+) - mean_advantage(D-)|
    """
    def mean_adv(formulas, offset):
        advs = []
        for idx, (formula, n_p, n_h) in enumerate(formulas):
            s = seed * 10000 + offset + idx if seed is not None else None
            a = distinguishing_advantage(formula, n_p, n_h, width_limit, n_trials, s)
            advs.append(a)
        return sum(advs) / len(advs) if advs else 0.0

    adv_plus = mean_adv(d_plus, 0)
    adv_minus = mean_adv(d_minus, 100000)
    return abs(adv_plus - adv_minus)


def baseline_collapse(
    n_formulas: int = 10,
    width_limit: int = 4,
    n_trials: int = 5,
    seed: int = 42,
) -> float:
    """
    Baseline collapse: average over D+ and D- without any transform.
    collapse = 1 - distinguishing_advantage
    """
    d_plus = sample_d_plus(n_formulas // 2, seed=seed)
    d_minus = sample_d_minus(n_formulas // 2, seed=seed + 1)
    adv = measure_distinguishing_advantage_batch(
        d_plus, d_minus, width_limit, n_trials, seed
    )
    return 1.0 - adv


if __name__ == "__main__":
    print("Baseline calibration...")
    d_plus = sample_d_plus(6, seed=42)
    d_minus = sample_d_minus(6, seed=43)

    for wl in [3, 4, 5]:
        adv = measure_distinguishing_advantage_batch(d_plus, d_minus, wl, n_trials=5, seed=42)
        collapse = 1.0 - adv
        print(f"  width_limit={wl}: advantage={adv:.3f}, collapse={collapse:.3f}")
