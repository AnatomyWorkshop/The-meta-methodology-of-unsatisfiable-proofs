"""
Transforms for Phase 5c (size-bounded Frege).

The critical new transform is LemmaIntroduction — it pre-derives intermediate
results that would otherwise be re-derived in multiple branches. This is the
proof-level analog of Extended Frege's abbreviation power.

The open question: does pre-computing lemmas genuinely reduce proof SIZE?
This is exactly the Frege vs Extended Frege separation.
"""

import random
from typing import List, Set

from l1_frege import (
    Formula, Var, Not, And, Or, Implies,
    depth, size, variables, _flatten_or,
)
from distributions_frege import FregeInstance


class FregeTransform:
    name: str
    enable_caching: bool = False  # Extended Frege mode

    def apply(self, hypotheses: List[Formula], target: Formula,
              n_pigeons: int, n_holes: int, rng: random.Random) -> tuple:
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
    def __init__(self, p: float):
        self.p = p
        self.name = f"hypothesis_projection_p{p}"

    def apply(self, hypotheses, target, n_pigeons, n_holes, rng):
        return [h for h in hypotheses if rng.random() < self.p], target

    def affects_target(self, hypotheses, target, n_pigeons, n_holes, rng):
        return self.p < 0.6


class LemmaIntroduction(FregeTransform):
    """
    Enable cross-branch caching: units derived in one branch are available
    for free in sibling branches. This is the proof-level Extended Frege
    operation — abbreviations allow reuse of intermediate derivations.

    In standard Frege: each branch re-derives all needed units independently.
    In Extended Frege: derive once, reuse everywhere (via abbreviation z = phi).

    The Frege vs Extended Frege separation asks: does this reuse genuinely
    reduce total proof size? OPEN PROBLEM.

    This transform does NOT modify hypotheses — it enables caching mode
    in the prover, which is the correct model of Extended Frege's power.
    """
    def __init__(self, fraction: float = 1.0):
        self.fraction = fraction
        self.name = f"cross_branch_caching_f{fraction}"
        self.enable_caching = True

    def apply(self, hypotheses, target, n_pigeons, n_holes, rng):
        return list(hypotheses), target

    def affects_target(self, hypotheses, target, n_pigeons, n_holes, rng):
        return False


class SubformulaElimination(FregeTransform):
    """
    Input-level abbreviation (same as Phase 5b).
    Unlikely to help for PHP but included for comparison.
    """
    def __init__(self, max_abbrevs: int = 3):
        self.max_abbrevs = max_abbrevs
        self.name = f"subformula_elimination_n{max_abbrevs}"

    def apply(self, hypotheses, target, n_pigeons, n_holes, rng):
        subf_count = {}
        for h in hypotheses:
            for sf in _all_subformulas(h):
                if depth(sf) >= 2:
                    subf_count[sf] = subf_count.get(sf, 0) + 1

        candidates = [(sf, c) for sf, c in subf_count.items() if c >= 2]
        candidates.sort(key=lambda x: -x[1])
        candidates = candidates[:self.max_abbrevs]

        if not candidates:
            return list(hypotheses), target

        max_var = max(v for h in hypotheses for v in variables(h))
        abbreviations = {}
        new_hyps = list(hypotheses)
        for i, (sf, _) in enumerate(candidates):
            fresh_var = Var(max_var + 1 + i)
            abbreviations[sf] = fresh_var
            new_hyps.append(Implies(fresh_var, sf))
            new_hyps.append(Implies(sf, fresh_var))

        result_hyps = [_replace_subformulas(h, abbreviations) for h in new_hyps]
        new_target = _replace_subformulas(target, abbreviations)
        return result_hyps, new_target

    def affects_target(self, hypotheses, target, n_pigeons, n_holes, rng):
        return False


class HypothesisWeakening(FregeTransform):
    def __init__(self, extra: int = 1):
        self.extra = extra
        self.name = f"hypothesis_weakening_e{extra}"

    def apply(self, hypotheses, target, n_pigeons, n_holes, rng):
        all_vars = sorted(set(v for h in hypotheses for v in variables(h)))
        result = []
        for h in hypotheses:
            if isinstance(h, Or) and rng.random() < 0.5:
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
    def __init__(self, p: float):
        self.p = p
        self.name = f"literal_negation_p{p}"

    def apply(self, hypotheses, target, n_pigeons, n_holes, rng):
        all_vars = sorted(set(v for h in hypotheses for v in variables(h)))
        n_flip = int(len(all_vars) * self.p)
        flip_set = set(rng.sample(all_vars, min(n_flip, len(all_vars))))

        def flip(f):
            if isinstance(f, Var):
                return Not(f) if f.idx in flip_set else f
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

        return [flip(h) for h in hypotheses], flip(target)

    def affects_target(self, hypotheses, target, n_pigeons, n_holes, rng):
        return True


# --- Helpers ---

def _simplify_under_assignment(f: Formula, assignment: dict) -> Formula:
    if isinstance(f, Var):
        if f.idx in assignment:
            return None if assignment[f.idx] else Not(Var(-1))
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
                return None
            if not (isinstance(s, Not) and isinstance(s.child, Var) and s.child.idx == -1):
                remaining.append(s)
        if not remaining:
            return Not(Var(-1))
        if len(remaining) == 1:
            return remaining[0]
        result = Or(remaining[0], remaining[1])
        for i in range(2, len(remaining)):
            result = Or(result, remaining[i])
        return result
    if isinstance(f, And):
        left = _simplify_under_assignment(f.left, assignment)
        right = _simplify_under_assignment(f.right, assignment)
        if isinstance(left, Not) and isinstance(left.child, Var) and left.child.idx == -1:
            return Not(Var(-1))
        if isinstance(right, Not) and isinstance(right.child, Var) and right.child.idx == -1:
            return Not(Var(-1))
        if left is None and right is None:
            return None
        if left is None:
            return right
        if right is None:
            return left
        return And(left, right)
    if isinstance(f, Implies):
        return _simplify_under_assignment(Or(Not(f.left), f.right), assignment)
    return f


def _all_subformulas(f: Formula) -> List[Formula]:
    result = [f]
    if isinstance(f, Var):
        return result
    if isinstance(f, Not):
        return result + _all_subformulas(f.child)
    if isinstance(f, (And, Or, Implies)):
        return result + _all_subformulas(f.left) + _all_subformulas(f.right)
    return result


def _replace_subformulas(f: Formula, replacements: dict) -> Formula:
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
    HypothesisProjection(0.7),
    HypothesisProjection(0.8),
    LemmaIntroduction(1.0),
    SubformulaElimination(2),
    SubformulaElimination(3),
    HypothesisWeakening(1),
    HypothesisWeakening(2),
    LiteralNegation(0.3),
]


if __name__ == "__main__":
    from distributions_frege import php_frege, php_target
    rng = random.Random(42)
    hyps = php_frege(5, 4)
    tgt = php_target(5, 4)
    print(f"Original PHP(5,4): {len(hyps)} hypotheses")
    for t in FREGE_TRANSFORM_REGISTRY:
        new_hyps, new_tgt = t.apply(hyps, tgt, 5, 4, rng)
        affected = t.affects_target(hyps, tgt, 5, 4, rng)
        print(f"  {t.name}: {len(new_hyps)} hyps, affects_target={affected}")
