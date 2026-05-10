"""
Distribution samplers for Frege proof complexity experiments.

Encodes PHP (pigeonhole principle) as propositional formulas in tree form,
not as CNF clauses. This is the key structural difference from Phase 5:
Frege operates on arbitrary formulas, not just disjunctions of literals.

D+ = small PHP instances (provable with bounded-depth Frege in short proofs)
D- = larger PHP instances (require deeper formulas or longer proofs at fixed depth)

The depth-complexity tradeoff for PHP in bounded-depth Frege:
  Krajíček (1994): depth-d Frege proofs of PHP(n) require size n^{Ω(1/d)}
  So at fixed depth, larger n → exponentially harder.
"""

from typing import List, Tuple
import random

from l1_frege import (
    Formula, Var, Not, And, Or, Implies,
    Proof, depth, size,
)


def php_var(i: int, j: int, n_holes: int) -> Var:
    """Variable p_{i,j}: pigeon i is in hole j."""
    return Var(i * n_holes + j)


def php_pigeon_axiom(i: int, n_holes: int) -> Formula:
    """Pigeon i must be in at least one hole: p_{i,0} ∨ p_{i,1} ∨ ... ∨ p_{i,h-1}"""
    if n_holes == 1:
        return php_var(i, 0, n_holes)
    result = Or(php_var(i, 0, n_holes), php_var(i, 1, n_holes))
    for j in range(2, n_holes):
        result = Or(result, php_var(i, j, n_holes))
    return result


def php_hole_axiom(i1: int, i2: int, j: int, n_holes: int) -> Formula:
    """Two pigeons cannot share hole j: ¬p_{i1,j} ∨ ¬p_{i2,j}"""
    return Or(Not(php_var(i1, j, n_holes)), Not(php_var(i2, j, n_holes)))


def php_frege(n_pigeons: int, n_holes: int) -> List[Formula]:
    """
    PHP(n_pigeons, n_holes) encoded as Frege hypotheses.
    Returns list of formulas (pigeon axioms + hole axioms).
    """
    hypotheses = []

    for i in range(n_pigeons):
        hypotheses.append(php_pigeon_axiom(i, n_holes))

    for j in range(n_holes):
        for i1 in range(n_pigeons):
            for i2 in range(i1 + 1, n_pigeons):
                hypotheses.append(php_hole_axiom(i1, i2, j, n_holes))

    return hypotheses


def php_target(n_pigeons: int, n_holes: int) -> Formula:
    """
    The contradiction target for PHP: derive False.
    Encoded as: conjunction of all axioms implies a contradiction.
    We use ¬(conjunction of pigeon axioms) as target — i.e., prove that
    the axiom set is unsatisfiable by deriving any pigeon axiom's negation
    from the hole constraints.

    Simpler target: derive (¬p_{0,0} ∧ ¬p_{0,1} ∧ ... ∧ ¬p_{0,h-1})
    from hole axioms — i.e., pigeon 0 has nowhere to go.
    This is a valid sub-goal in PHP refutation.
    """
    if n_holes == 1:
        return Not(php_var(0, 0, n_holes))
    result = And(Not(php_var(0, 0, n_holes)), Not(php_var(0, 1, n_holes)))
    for j in range(2, n_holes):
        result = And(result, Not(php_var(0, j, n_holes)))
    return result


def n_vars(n_pigeons: int, n_holes: int) -> int:
    return n_pigeons * n_holes


def formula_depth(hypotheses: List[Formula]) -> int:
    if not hypotheses:
        return 0
    return max(depth(f) for f in hypotheses)


# --- Distribution samplers ---

FregeInstance = Tuple[List[Formula], Formula, int, int]
# (hypotheses, target, n_pigeons, n_holes)


def sample_d_plus(n_samples: int, seed: int = None) -> List[FregeInstance]:
    """
    D+: PHP instances provable with small depth.
    Uses PHP(n, n-1) for n in {3, 4} — small enough for bounded-depth proofs.
    """
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
    """
    D-: PHP instances requiring deeper proofs at fixed depth bound.
    Uses PHP(n, n-1) for n in {6, 7} — at bounded depth, proofs are exponentially longer.
    """
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
    hyps = php_frege(3, 2)
    tgt = php_target(3, 2)
    print(f"PHP(3,2): {len(hyps)} hypotheses, max depth={formula_depth(hyps)}")
    print(f"  Target: {tgt} (depth={depth(tgt)})")
    print(f"  Pigeon axioms: {hyps[:3]}")
    print(f"  Hole axioms: {hyps[3:6]}")

    hyps2 = php_frege(5, 4)
    tgt2 = php_target(5, 4)
    print(f"\nPHP(5,4): {len(hyps2)} hypotheses, max depth={formula_depth(hyps2)}")
    print(f"  Target depth={depth(tgt2)}, size={size(tgt2)}")

    hyps3 = php_frege(7, 6)
    tgt3 = php_target(7, 6)
    print(f"\nPHP(7,6): {len(hyps3)} hypotheses, max depth={formula_depth(hyps3)}")
    print(f"  Target depth={depth(tgt3)}, size={size(tgt3)}")
    print(f"  Variables: {n_vars(7, 6)}")
