"""
Scaling experiment: how does the Frege/Extended Frege gap grow with PHP size?

For PHP(n, n-1) with increasing n, measure:
  - Minimum steps for standard Frege to prove
  - Minimum steps for Extended Frege (with caching) to prove
  - The ratio (scaling law)

If the ratio grows with n, that's empirical evidence that the separation is genuine.
"""

import sys
import os

_phase5c_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, _phase5c_dir)

from l1_frege import greedy_frege_proof
from distributions_frege import php_frege, php_target


def find_min_steps(n_pigeons, n_holes, enable_caching=False, max_limit=2000, n_seeds=3):
    """Binary search for minimum step_limit that allows proof."""
    lo, hi = 1, max_limit

    while lo < hi:
        mid = (lo + hi) // 2
        successes = 0
        for s in range(n_seeds):
            hyps = php_frege(n_pigeons, n_holes)
            tgt = php_target(n_pigeons, n_holes)
            ok, _, _ = greedy_frege_proof(tgt, hyps, step_limit=mid, seed=s,
                                          enable_caching=enable_caching)
            if ok:
                successes += 1
        if successes >= (n_seeds + 1) // 2:
            hi = mid
        else:
            lo = mid + 1

    return lo


def run_scaling():
    print("PHP(n+1, n) Scaling: Standard Frege vs Extended Frege (caching)")
    print("=" * 70)
    print(f"{'PHP':>10} | {'Std Frege':>12} | {'Ext Frege':>12} | {'Ratio':>8} | {'Gap':>8}")
    print("-" * 70)

    results = []

    for n_holes in range(2, 8):
        n_pigeons = n_holes + 1

        steps_std = find_min_steps(n_pigeons, n_holes, enable_caching=False,
                                   max_limit=3000, n_seeds=3)
        steps_ext = find_min_steps(n_pigeons, n_holes, enable_caching=True,
                                   max_limit=3000, n_seeds=3)

        if steps_std >= 3000:
            ratio_str = ">inf"
            gap = ">2970"
        else:
            ratio = steps_std / max(steps_ext, 1)
            ratio_str = f"{ratio:.1f}x"
            gap = str(steps_std - steps_ext)

        print(f"PHP({n_pigeons},{n_holes:>2}) | {steps_std:>12} | {steps_ext:>12} | {ratio_str:>8} | {gap:>8}")

        results.append({
            "n_pigeons": n_pigeons,
            "n_holes": n_holes,
            "steps_std": steps_std,
            "steps_ext": steps_ext,
        })

    print("\n" + "=" * 70)
    print("\nInterpretation:")
    print("  If ratio grows with n → genuine separation (Extended Frege is")
    print("  superpolynomially more efficient than standard Frege on PHP).")
    print("  If ratio is constant → no separation at this scale.")

    return results


if __name__ == "__main__":
    run_scaling()
