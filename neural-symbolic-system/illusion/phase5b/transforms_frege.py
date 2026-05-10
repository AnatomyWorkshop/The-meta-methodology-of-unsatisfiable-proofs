"""
Transforms for Frege proof complexity experiments.

Each transform modifies the hypothesis set or proof parameters.
The key UNKNOWN transform is SubformulaElimination — it corresponds to
the Extended Frege operation (introducing abbreviation variables).
The Frege vs Extended Frege separation is a major open problem.
"""

import random
from typing import List

from l1_frege import (
    Formula, Var, Not, And, Or, Implies,
    depth, variables, _flatten_or,
)
from distributions_frege import FregeInstance


class FregeTransform:
    name: str

    def apply(self, hypotheses: List[Formula], target: Formula,
              n_pigeons: int, n_holes: int, rng: random.Random
              ) -> tuple:
        """Returns (new_hypotheses, new_target)."""
        raise NotImplementedError

    def affects_target(self, hypotheses: List[Formula], target: Formula,
                       n_pigeons: int, n_holes: int, rng: random.Random) -> bool:
        raise NotImplementedError


class IdentityTransform(FregeTransform):
    name = "identity"

    def apply(self, hypotheses, target, n_pigeons, n_holes, rng):
        return list(hypotheses), target

    def affects_target(self, hypotheses, target, n_pigeons, n_holes, rng):
        return False


class FormulaPermutation(FregeTransform):
    name = "formula_permutation"

    def apply(self, hypotheses, target, n_pigeons, n_holes, rng):
        result = list(hypotheses)
        rng.shuffle(result)
        return result, target

    def affects_target(self, hypotheses, target, n_pigeons, n_holes, rng):
        return False


class VariableRestriction(FregeTransform):
    """
    Fix p fraction of variables to True/False and simplify hypotheses.
    Frege analog of random restriction — the core operation of depth lower bounds.
    Expected L3 verdict: SAFE.
    """
    def __init__(self, p: float):
        self.p = p
        self.name = f"variable_restriction_p{p}"

    def apply(self, hypotheses, target, n_pigeons, n_holes, rng):
        all_vars = set()
        for h in hypotheses:
            all_vars |= variables(h)
        n_fix = int(len(all_vars) * self.p)
        vars_to_fix = rng.sample(sorted(all_vars), min(n_fix, len(all_vars)))
        assignment = {v: rng.choice([True, False]) for v in vars_to_fix}

        new_hyps = []
        for h in hypotheses:
            simplified = _simplify_under_assignment(h, assignment)
            if simplified is not None:
                new_hyps.append(simplified)

        new_target = _simplify_under_assignment(target, assignment)
        if new_target is None:
            new_target = target

        return new_hyps, new_target

    def affects_target(self, hypotheses, target, n_pigeons, n_holes, rng):
        return self.p > 0.5


class HypothesisProjection(FregeTransform):
    """
    Randomly keep p fraction of hypotheses.
    Analog of clause_projection in Resolution.
    """
    def __init__(self, p: float):
        self.p = p
        self.name = f"hypothesis_projection_p{p}"

    def apply(self, hypotheses, target, n_pigeons, n_holes, rng):
        result = [h for h in hypotheses if rng.random() < self.p]
        return result, target

    def affects_target(self, hypotheses, target, n_pigeons, n_holes, rng):
        return self.p < 0.6


class SubformulaElimination(FregeTransform):
    """
    Replace repeated subformulas with fresh variables (abbreviation).
    This is the Extended Frege operation: introduce new variable z = phi,
    then use z in place of phi throughout.

    The Frege vs Extended Frege separation is OPEN.
    Expected L3 verdict: UNKNOWN.
    """
    def __init__(self, max_abbrevs: int = 3):
        self.max_abbrevs = max_abbrevs
        self.name = f"subformula_elimination_n{max_abbrevs}"

    def apply(self, hypotheses, target, n_pigeons, n_holes, rng):
        # Find subformulas that appear multiple times
        subf_count = {}
        for h in hypotheses:
            for sf in _all_subformulas(h):
                if depth(sf) >= 2:
                    subf_count[sf] = subf_count.get(sf, 0) + 1

        # Pick most frequent subformulas to abbreviate
        candidates = [(sf, c) for sf, c in subf_count.items() if c >= 2]
        candidates.sort(key=lambda x: -x[1])
        candidates = candidates[:self.max_abbrevs]

        if not candidates:
            return list(hypotheses), target

        # Assign fresh variables
        max_var = max(v for h in hypotheses for v in variables(h))
        abbreviations = {}
        new_hyps = list(hypotheses)
        for i, (sf, _) in enumerate(candidates):
            fresh_var = Var(max_var + 1 + i)
            abbreviations[sf] = fresh_var
            # Add definition: fresh_var <-> sf (as two implications)
            new_hyps.append(Implies(fresh_var, sf))
            new_hyps.append(Implies(sf, fresh_var))

        # Replace subformulas in hypotheses
        result_hyps = []
        for h in new_hyps:
            result_hyps.append(_replace_subformulas(h, abbreviations))

        new_target = _replace_subformulas(target, abbreviations)
        return result_hyps, new_target

    def affects_target(self, hypotheses, target, n_pigeons, n_holes, rng):
        return False


class DepthTruncation(FregeTransform):
    """
    Truncate all formulas to max depth k by replacing deep subformulas
    with fresh variables. This is a LOCAL operation — decidable in O(n).
    Expected L3 verdict: UNSAFE.
    """
    def __init__(self, k: int):
        self.k = k
        self.name = f"depth_truncation_k{k}"

    def apply(self, hypotheses, target, n_pigeons, n_holes, rng):
        max_var = max(v for h in hypotheses for v in variables(h))
        counter = [max_var + 1]

        def truncate(f, current_depth):
            if current_depth >= self.k:
                v = Var(counter[0])
                counter[0] += 1
                return v
            if isinstance(f, Var):
                return f
            if isinstance(f, Not):
                return Not(truncate(f.child, current_depth + 1))
            if isinstance(f, And):
                return And(truncate(f.left, current_depth + 1),
                          truncate(f.right, current_depth + 1))
            if isinstance(f, Or):
                return Or(truncate(f.left, current_depth + 1),
                         truncate(f.right, current_depth + 1))
            if isinstance(f, Implies):
                return Implies(truncate(f.left, current_depth + 1),
                              truncate(f.right, current_depth + 1))
            return f

        new_hyps = [truncate(h, 0) for h in hypotheses]
        new_target = truncate(target, 0)
        return new_hyps, new_target

    def affects_target(self, hypotheses, target, n_pigeons, n_holes, rng):
        return self.k < 2


class HypothesisWeakening(FregeTransform):
    """
    Add random disjuncts to hypotheses (weakening them).
    Weaker hypotheses make proofs harder.
    """
    def __init__(self, extra: int = 1):
        self.extra = extra
        self.name = f"hypothesis_weakening_e{extra}"

    def apply(self, hypotheses, target, n_pigeons, n_holes, rng):
        all_vars = sorted(set(v for h in hypotheses for v in variables(h)))
        result = []
        for h in hypotheses:
            if isinstance(h, Or) and rng.random() < 0.5:
                # Add a random disjunct
                for _ in range(self.extra):
                    v = Var(rng.choice(all_vars))
                    if rng.random() < 0.5:
                        v = Not(v)
                    h = Or(h, v)
            result.append(h)
        return result, target

    def affects_target(self, hypotheses, target, n_pigeons, n_holes, rng):
        return False


class LiteralNegation(FregeTransform):
    """
    Randomly flip polarity of p fraction of variables.
    Breaks PHP structure.
    """
    def __init__(self, p: float):
        self.p = p
        self.name = f"literal_negation_p{p}"

    def apply(self, hypotheses, target, n_pigeons, n_holes, rng):
        all_vars = sorted(set(v for h in hypotheses for v in variables(h)))
        n_flip = int(len(all_vars) * self.p)
        flip_set = set(rng.sample(all_vars, min(n_flip, len(all_vars))))

        def flip(f):
            if isinstance(f, Var):
                if f.idx in flip_set:
                    return Not(f)
                return f
            if isinstance(f, Not):
                if isinstance(f.child, Var) and f.child.idx in flip_set:
                    return f.child
                return Not(flip(f.child))
            if isinstance(f, And):
                return And(flip(f.left), flip(f.right))
            if isinstance(f, Or):
                return Or(flip(f.left), flip(f.right))
            if isinstance(f, Implies):
                return Implies(flip(f.left), flip(f.right))
            return f

        new_hyps = [flip(h) for h in hypotheses]
        new_target = flip(target)
        return new_hyps, new_target

    def affects_target(self, hypotheses, target, n_pigeons, n_holes, rng):
        return True


# --- Helper functions ---

def _simplify_under_assignment(f: Formula, assignment: dict) -> Formula:
    """Simplify formula under partial variable assignment. Returns None if formula is True."""
    if isinstance(f, Var):
        if f.idx in assignment:
            return None if assignment[f.idx] else Not(Var(-1))  # sentinel for False
        return f
    if isinstance(f, Not):
        if isinstance(f.child, Var) and f.child.idx in assignment:
            return None if not assignment[f.child.idx] else Not(Var(-1))
        inner = _simplify_under_assignment(f.child, assignment)
        if inner is None:
            return Not(Var(-1))
        return Not(inner)
    if isinstance(f, Or):
        disjuncts = _flatten_or(f)
        remaining = []
        for d in disjuncts:
            s = _simplify_under_assignment(d, assignment)
            if s is None:
                return None  # disjunction is True
            if not (isinstance(s, Not) and isinstance(s.child, Var) and s.child.idx == -1):
                remaining.append(s)
        if not remaining:
            return Not(Var(-1))  # all False
        if len(remaining) == 1:
            return remaining[0]
        result = Or(remaining[0], remaining[1])
        for i in range(2, len(remaining)):
            result = Or(result, remaining[i])
        return result
    if isinstance(f, And):
        left = _simplify_under_assignment(f.left, assignment)
        right = _simplify_under_assignment(f.right, assignment)
        if left is None and right is None:
            return None
        if isinstance(left, Not) and isinstance(left.child, Var) and left.child.idx == -1:
            return Not(Var(-1))
        if isinstance(right, Not) and isinstance(right.child, Var) and right.child.idx == -1:
            return Not(Var(-1))
        if left is None:
            return right
        if right is None:
            return left
        return And(left, right)
    if isinstance(f, Implies):
        return _simplify_under_assignment(Or(Not(f.left), f.right), assignment)
    return f


def _all_subformulas(f: Formula) -> List[Formula]:
    """Collect all subformulas of f."""
    result = [f]
    if isinstance(f, Var):
        return result
    if isinstance(f, Not):
        return result + _all_subformulas(f.child)
    if isinstance(f, (And, Or, Implies)):
        return result + _all_subformulas(f.left) + _all_subformulas(f.right)
    return result


def _replace_subformulas(f: Formula, replacements: dict) -> Formula:
    """Replace subformulas according to replacement dict."""
    if f in replacements:
        return replacements[f]
    if isinstance(f, Var):
        return f
    if isinstance(f, Not):
        return Not(_replace_subformulas(f.child, replacements))
    if isinstance(f, And):
        return And(_replace_subformulas(f.left, replacements),
                  _replace_subformulas(f.right, replacements))
    if isinstance(f, Or):
        return Or(_replace_subformulas(f.left, replacements),
                 _replace_subformulas(f.right, replacements))
    if isinstance(f, Implies):
        return Implies(_replace_subformulas(f.left, replacements),
                      _replace_subformulas(f.right, replacements))
    return f


# --- Registry ---

FREGE_TRANSFORM_REGISTRY = [
    IdentityTransform(),
    FormulaPermutation(),
    VariableRestriction(0.2),
    VariableRestriction(0.3),
    VariableRestriction(0.4),
    HypothesisProjection(0.7),
    HypothesisProjection(0.8),
    DepthTruncation(2),
    DepthTruncation(3),
    SubformulaElimination(2),
    SubformulaElimination(3),
    HypothesisWeakening(1),
    HypothesisWeakening(2),
    LiteralNegation(0.3),
]


if __name__ == "__main__":
    from distributions_frege import php_frege, php_target
    rng = random.Random(42)
    hyps = php_frege(4, 3)
    tgt = php_target(4, 3)
    print(f"Original: {len(hyps)} hypotheses")
    for t in FREGE_TRANSFORM_REGISTRY:
        new_hyps, new_tgt = t.apply(hyps, tgt, 4, 3, rng)
        affected = t.affects_target(hyps, tgt, 4, 3, rng)
        print(f"  {t.name}: {len(new_hyps)} hyps, affects_target={affected}")
