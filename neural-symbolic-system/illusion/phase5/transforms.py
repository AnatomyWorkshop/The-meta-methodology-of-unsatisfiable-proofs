import random
from typing import List, Optional
from distributions import Clause, Formula


class ResolutionTransform:
    name: str

    def apply(self, formula: Formula, n_pigeons: int, n_holes: int,
              rng: random.Random) -> Formula:
        raise NotImplementedError

    def affects_target(self, formula: Formula, n_pigeons: int,
                       n_holes: int, rng: random.Random) -> bool:
        """
        Returns True if the transform destroys the unsatisfiability structure
        (i.e., the transformed formula might become satisfiable or trivially provable).
        """
        raise NotImplementedError


class IdentityTransform(ResolutionTransform):
    name = "identity"

    def apply(self, formula, n_pigeons, n_holes, rng):
        return list(formula)

    def affects_target(self, formula, n_pigeons, n_holes, rng):
        return False


class ClausePermutation(ResolutionTransform):
    name = "clause_permutation"

    def apply(self, formula, n_pigeons, n_holes, rng):
        result = list(formula)
        rng.shuffle(result)
        return result

    def affects_target(self, formula, n_pigeons, n_holes, rng):
        return False


class ClauseRestriction(ResolutionTransform):
    """
    Randomly fix p fraction of variables to 0 or 1.
    Analog of random_restriction / algebraic_restriction.
    """
    def __init__(self, p: float):
        self.p = p
        self.name = f"clause_restriction_p{p}"

    def apply(self, formula, n_pigeons, n_holes, rng):
        total_vars = n_pigeons * n_holes
        n_fix = int(total_vars * self.p)
        vars_to_fix = rng.sample(range(total_vars), min(n_fix, total_vars))
        assignment = {v: rng.choice([True, False]) for v in vars_to_fix}

        result = []
        for clause in formula:
            new_clause = set()
            satisfied = False
            for (var, pol) in clause:
                if var in assignment:
                    if assignment[var] == pol:
                        satisfied = True
                        break
                    # literal falsified — drop it
                else:
                    new_clause.add((var, pol))
            if not satisfied:
                result.append(frozenset(new_clause))
        return result

    def affects_target(self, formula, n_pigeons, n_holes, rng):
        # Restriction with p > 0.5 may make formula satisfiable
        return self.p > 0.5


class WidthTruncation(ResolutionTransform):
    """
    Remove all clauses with width > k.
    Local operation — UNSAFE (width is checkable in O(n)).
    """
    def __init__(self, k: int):
        self.k = k
        self.name = f"width_truncation_k{k}"

    def apply(self, formula, n_pigeons, n_holes, rng):
        return [c for c in formula if len(c) <= self.k]

    def affects_target(self, formula, n_pigeons, n_holes, rng):
        # Removing wide clauses may make formula satisfiable
        return self.k < n_holes


class ClauseProjection(ResolutionTransform):
    """
    Randomly keep p fraction of clauses.
    Analog of subgraph_projection.
    """
    def __init__(self, p: float):
        self.p = p
        self.name = f"clause_projection_p{p}"

    def apply(self, formula, n_pigeons, n_holes, rng):
        return [c for c in formula if rng.random() < self.p]

    def affects_target(self, formula, n_pigeons, n_holes, rng):
        # Removing too many clauses may make formula satisfiable
        return self.p < 0.6


class VariableElimination(ResolutionTransform):
    """
    Eliminate p fraction of variables by existential quantification
    (replace each eliminated variable with both True and False, take intersection).
    Corresponds to Extended Resolution — decidability within Resolution is open.
    Expected L3 verdict: UNKNOWN.
    """
    def __init__(self, p: float):
        self.p = p
        self.name = f"variable_elimination_p{p}"

    def apply(self, formula, n_pigeons, n_holes, rng):
        total_vars = n_pigeons * n_holes
        n_elim = int(total_vars * self.p)
        vars_to_elim = set(rng.sample(range(total_vars), min(n_elim, total_vars)))

        result = []
        for clause in formula:
            # Project out eliminated variables
            new_clause = frozenset(
                (var, pol) for (var, pol) in clause
                if var not in vars_to_elim
            )
            if new_clause not in result:
                result.append(new_clause)
        return result

    def affects_target(self, formula, n_pigeons, n_holes, rng):
        return self.p > 0.4


class LiteralNegation(ResolutionTransform):
    """
    Randomly flip polarity of p fraction of literals.
    Expected to affect target (breaks PHP structure).
    """
    def __init__(self, p: float):
        self.p = p
        self.name = f"literal_negation_p{p}"

    def apply(self, formula, n_pigeons, n_holes, rng):
        result = []
        for clause in formula:
            new_clause = frozenset(
                (var, not pol) if rng.random() < self.p else (var, pol)
                for (var, pol) in clause
            )
            result.append(new_clause)
        return result

    def affects_target(self, formula, n_pigeons, n_holes, rng):
        return True  # always breaks PHP structure


RESOLUTION_TRANSFORM_REGISTRY = [
    IdentityTransform(),
    ClausePermutation(),
    ClauseRestriction(0.2),
    ClauseRestriction(0.3),
    ClauseRestriction(0.4),
    ClauseProjection(0.7),
    ClauseProjection(0.8),
    WidthTruncation(2),
    WidthTruncation(3),
    VariableElimination(0.2),
    VariableElimination(0.3),
    LiteralNegation(0.3),
]


if __name__ == "__main__":
    from distributions import php_formula
    rng = random.Random(42)
    f = php_formula(4, 3)
    print(f"Original: {len(f)} clauses")
    for t in RESOLUTION_TRANSFORM_REGISTRY:
        transformed = t.apply(f, 4, 3, rng)
        affected = t.affects_target(f, 4, 3, rng)
        print(f"  {t.name}: {len(transformed)} clauses, affects_target={affected}")
