"""
Distribution samplers for Phase 5c (size-bounded Frege).

Same PHP encoding as Phase 5b — the formulas don't change,
only the resource metric (step count instead of depth).
"""

from typing import List, Tuple
import random

from l1_frege import (
    Formula, Var, Not, And, Or, Implies,
    Proof, depth, size, _flatten_or, variables,
)


def php_var(i: int, j: int, n_holes: int) -> Var:
    return Var(i * n_holes + j)


def php_pigeon_axiom(i: int, n_holes: int) -> Formula:
    if n_holes == 1:
        return php_var(i, 0, n_holes)
    result = Or(php_var(i, 0, n_holes), php_var(i, 1, n_holes))
    for j in range(2, n_holes):
        result = Or(result, php_var(i, j, n_holes))
    return result


def php_hole_axiom(i1: int, i2: int, j: int, n_holes: int) -> Formula:
    return Or(Not(php_var(i1, j, n_holes)), Not(php_var(i2, j, n_holes)))


def php_frege(n_pigeons: int, n_holes: int) -> List[Formula]:
    hypotheses = []
    for i in range(n_pigeons):
        hypotheses.append(php_pigeon_axiom(i, n_holes))
    for j in range(n_holes):
        for i1 in range(n_pigeons):
            for i2 in range(i1 + 1, n_pigeons):
                hypotheses.append(php_hole_axiom(i1, i2, j, n_holes))
    return hypotheses


def php_target(n_pigeons: int, n_holes: int) -> Formula:
    if n_holes == 1:
        return Not(php_var(0, 0, n_holes))
    result = And(Not(php_var(0, 0, n_holes)), Not(php_var(0, 1, n_holes)))
    for j in range(2, n_holes):
        result = And(result, Not(php_var(0, j, n_holes)))
    return result


def n_vars(n_pigeons: int, n_holes: int) -> int:
    return n_pigeons * n_holes


FregeInstance = Tuple[List[Formula], Formula, int, int]


def sample_d_plus(n_samples: int, seed: int = None) -> List[FregeInstance]:
    """D+: small PHP, provable within modest step budget."""
    rng = random.Random(seed)
    results = []
    sizes = [(3, 2), (4, 3)]
    for _ in range(n_samples):
        n_p, n_h = rng.choice(sizes)
        hyps = php_frege(n_p, n_h)
        tgt = php_target(n_p, n_h)
        results.append((hyps, tgt, n_p, n_h))
    return results


def sample_d_minus(n_samples: int, seed: int = None) -> List[FregeInstance]:
    """D-: larger PHP, requires many more steps."""
    rng = random.Random(seed)
    results = []
    sizes = [(6, 5), (7, 6)]
    for _ in range(n_samples):
        n_p, n_h = rng.choice(sizes)
        hyps = php_frege(n_p, n_h)
        tgt = php_target(n_p, n_h)
        results.append((hyps, tgt, n_p, n_h))
    return results


if __name__ == "__main__":
    for n_p, n_h in [(3, 2), (4, 3), (5, 4), (6, 5), (7, 6)]:
        hyps = php_frege(n_p, n_h)
        print(f"PHP({n_p},{n_h}): {len(hyps)} hypotheses, {n_vars(n_p, n_h)} variables")
