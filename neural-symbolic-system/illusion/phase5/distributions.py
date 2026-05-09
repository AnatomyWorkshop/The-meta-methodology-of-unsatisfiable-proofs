import random
from typing import List, Tuple, Set

Clause = frozenset  # frozenset of literals; literal = (var_idx, polarity)
Formula = List[Clause]


def php_formula(n_pigeons: int, n_holes: int) -> Formula:
    """
    Pigeonhole principle PHP(n_pigeons, n_holes).
    Variables: p_{i,j} encoded as i * n_holes + j (0-indexed).
    Returns CNF as list of frozensets of (var, polarity) pairs.
    polarity True = positive literal, False = negative literal.
    """
    clauses = []
    def var(i, j):
        return i * n_holes + j

    # Pigeon clauses: each pigeon must be in at least one hole
    for i in range(n_pigeons):
        clause = frozenset((var(i, j), True) for j in range(n_holes))
        clauses.append(clause)

    # Hole clauses: no two pigeons share a hole
    for j in range(n_holes):
        for i1 in range(n_pigeons):
            for i2 in range(i1 + 1, n_pigeons):
                clause = frozenset([
                    (var(i1, j), False),
                    (var(i2, j), False),
                ])
                clauses.append(clause)

    return clauses


def n_vars(n_pigeons: int, n_holes: int) -> int:
    return n_pigeons * n_holes


def formula_width(formula: Formula) -> int:
    if not formula:
        return 0
    return max(len(c) for c in formula)


def sample_d_plus(n_samples: int, seed: int = None) -> List[Tuple[Formula, int, int]]:
    """
    D+: formulas that can be proved with small width.
    Uses PHP(n, n-1) for n in {3, 4} — small enough for short proofs.
    Returns list of (formula, n_pigeons, n_holes).
    """
    rng = random.Random(seed)
    results = []
    sizes = [(3, 2), (4, 3)]
    for _ in range(n_samples):
        n_p, n_h = rng.choice(sizes)
        results.append((php_formula(n_p, n_h), n_p, n_h))
    return results


def sample_d_minus(n_samples: int, seed: int = None) -> List[Tuple[Formula, int, int]]:
    """
    D-: formulas that require exponential-width proofs.
    Uses PHP(n+1, n) for n in {5, 6} — requires width >= n by Ben-Sasson-Wigderson.
    Returns list of (formula, n_pigeons, n_holes).
    """
    rng = random.Random(seed)
    results = []
    sizes = [(6, 5), (7, 6)]
    for _ in range(n_samples):
        n_p, n_h = rng.choice(sizes)
        results.append((php_formula(n_p, n_h), n_p, n_h))
    return results


if __name__ == "__main__":
    f = php_formula(3, 2)
    print(f"PHP(3,2): {len(f)} clauses, width {formula_width(f)}")
    f2 = php_formula(4, 3)
    print(f"PHP(4,3): {len(f2)} clauses, width {formula_width(f2)}")
    f3 = php_formula(6, 5)
    print(f"PHP(6,5): {len(f3)} clauses, width {formula_width(f3)}")
