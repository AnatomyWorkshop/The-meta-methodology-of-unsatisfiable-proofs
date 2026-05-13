"""
L1 domain model for Frege proof systems — SIZE metric variant.

Key difference from Phase 5b:
  5b bounds case-split DEPTH (maps to depth-d Frege).
  5c bounds total STEPS (maps to size-s Frege).

Extended Frege's conjectured advantage is in proof SIZE, not depth.
SubformulaElimination (abbreviation) compresses repeated subproofs,
reducing total step count. If it shows signal here, we're probing
the Frege vs Extended Frege separation directly.
"""

import random
from typing import List, Optional, Set, Tuple, Union
from dataclasses import dataclass


# --- Formula tree (same as phase5b) ---

@dataclass(frozen=True)
class Var:
    idx: int
    def __repr__(self):
        return f"x{self.idx}"

@dataclass(frozen=True)
class Not:
    child: "Formula"
    def __repr__(self):
        return f"~{self.child}"

@dataclass(frozen=True)
class And:
    left: "Formula"
    right: "Formula"
    def __repr__(self):
        return f"({self.left} & {self.right})"

@dataclass(frozen=True)
class Or:
    left: "Formula"
    right: "Formula"
    def __repr__(self):
        return f"({self.left} | {self.right})"

@dataclass(frozen=True)
class Implies:
    left: "Formula"
    right: "Formula"
    def __repr__(self):
        return f"({self.left} -> {self.right})"


Formula = Union[Var, Not, And, Or, Implies]
Proof = List[Formula]


def depth(f: Formula) -> int:
    if isinstance(f, Var):
        return 0
    if isinstance(f, Not):
        return 1 + depth(f.child)
    if isinstance(f, (And, Or, Implies)):
        return 1 + max(depth(f.left), depth(f.right))
    raise TypeError(f"Unknown formula type: {type(f)}")


def size(f: Formula) -> int:
    if isinstance(f, Var):
        return 1
    if isinstance(f, Not):
        return 1 + size(f.child)
    if isinstance(f, (And, Or, Implies)):
        return 1 + size(f.left) + size(f.right)
    raise TypeError(f"Unknown formula type: {type(f)}")


def variables(f: Formula) -> Set[int]:
    if isinstance(f, Var):
        return {f.idx}
    if isinstance(f, Not):
        return variables(f.child)
    if isinstance(f, (And, Or, Implies)):
        return variables(f.left) | variables(f.right)
    return set()


def _flatten_or(f: Formula) -> List[Formula]:
    if isinstance(f, Or):
        return _flatten_or(f.left) + _flatten_or(f.right)
    return [f]


# --- Inference rules ---

def disjunctive_syllogism(disj: Formula, negated: Formula) -> Optional[Formula]:
    """From (A | B) and ~A, derive B. Handles nested Or trees."""
    if not isinstance(disj, Or):
        return None
    disjuncts = _flatten_or(disj)
    new_disjuncts = []
    eliminated = False
    for d in disjuncts:
        if not eliminated:
            if isinstance(negated, Not) and negated.child == d:
                eliminated = True
                continue
            if isinstance(d, Not) and d.child == negated:
                eliminated = True
                continue
        new_disjuncts.append(d)
    if not eliminated:
        return None
    if len(new_disjuncts) == 0:
        return None
    if len(new_disjuncts) == 1:
        return new_disjuncts[0]
    result = Or(new_disjuncts[0], new_disjuncts[1])
    for i in range(2, len(new_disjuncts)):
        result = Or(result, new_disjuncts[i])
    return result


# --- Unit propagation ---

def _is_unit(f: Formula) -> bool:
    if isinstance(f, Var):
        return True
    if isinstance(f, Not) and isinstance(f.child, Var):
        return True
    return False


def _negate_unit(f: Formula) -> Formula:
    if isinstance(f, Not):
        return f.child
    return Not(f)


def _unit_propagate(formulas: Set[Formula], units: Set[Formula]) -> Tuple[Set[Formula], Set[Formula], bool, int]:
    """
    Returns (remaining, all_units, contradiction, steps_used).
    Steps = number of NEW UNITS derived (not simplification operations).
    This correctly models Frege proof size: each new derived formula = one proof line.
    Pre-existing hypotheses and lemmas are free to reference.
    """
    all_units = set(units)
    remaining = set(formulas) - all_units
    steps = 0

    changed = True
    while changed:
        changed = False
        new_remaining = set()
        for f in remaining:
            if _is_unit(f):
                if _negate_unit(f) in all_units:
                    return set(), all_units, True, steps + 1
                all_units.add(f)
                steps += 1
                changed = True
                continue

            simplified = f
            for u in list(all_units):
                result = disjunctive_syllogism(simplified, u)
                if result is not None:
                    simplified = result

            if simplified == f:
                new_remaining.add(f)
            elif _is_unit(simplified):
                if _negate_unit(simplified) in all_units:
                    return set(), all_units, True, steps + 1
                all_units.add(simplified)
                steps += 1
                changed = True
            elif isinstance(simplified, Or):
                new_remaining.add(simplified)
                if simplified != f:
                    changed = True
            else:
                new_remaining.add(simplified)

        remaining = new_remaining

    for u in all_units:
        if _negate_unit(u) in all_units:
            return set(), all_units, True, steps

    return remaining, all_units, False, steps


# --- Size-bounded Frege prover ---

class StepCounter:
    """Mutable counter shared across recursive calls."""
    def __init__(self, limit: int):
        self.limit = limit
        self.used = 0
        self.exhausted = False

    def add(self, n: int):
        self.used += n
        if self.used >= self.limit:
            self.exhausted = True


def greedy_frege_proof(
    target: Formula,
    hypotheses: List[Formula],
    step_limit: int,
    seed: int = None,
    enable_caching: bool = False,
) -> Tuple[bool, int, Proof]:
    """
    Size-bounded Frege refutation via case splitting.

    When enable_caching=False: standard Frege. Each branch derives independently.
    When enable_caching=True: Extended Frege. Units derived in one branch are
    available for free in sibling branches (cross-branch sharing).

    This models the core Extended Frege advantage: abbreviations allow reuse
    of intermediate results without re-derivation.

    Returns (success, steps_used, proof_trace).
    """
    rng = random.Random(seed)
    proof_trace: List[Formula] = list(hypotheses)

    all_vars = set()
    for h in hypotheses:
        all_vars |= variables(h)
    var_list = sorted(all_vars)
    rng.shuffle(var_list)

    counter = StepCounter(step_limit)
    cache: Set[Formula] = set() if enable_caching else None

    success = _refute_with_splitting_sized(
        set(hypotheses), var_list, counter, rng, cache
    )

    if success:
        proof_trace.append(target)

    return success, counter.used, proof_trace


def _refute_with_splitting_sized(
    formulas: Set[Formula],
    split_vars: List[int],
    counter: StepCounter,
    rng: random.Random,
    cache: Optional[Set[Formula]],
) -> bool:
    """
    Try to derive contradiction. Bounded by total steps across all branches.
    If cache is not None (Extended Frege mode), units found in cache are free.
    """
    if counter.exhausted:
        return False

    units = set()
    for f in formulas:
        if _is_unit(f):
            units.add(f)

    # In Extended Frege mode, cached units are free
    if cache is not None:
        units |= cache

    remaining, all_units, contradiction, steps = _unit_propagate(
        formulas - units, units
    )

    # Only count steps for units NOT already in cache
    if cache is not None:
        new_units = all_units - cache
        actual_steps = len(new_units) - len(units - cache)
        counter.add(max(0, actual_steps))
        cache.update(all_units)
    else:
        counter.add(steps)

    if contradiction:
        return True

    if counter.exhausted:
        return False

    # Pick variable to split on
    available_vars = [v for v in split_vars
                      if Var(v) not in all_units and Not(Var(v)) not in all_units]
    if not available_vars:
        return False

    split_var = available_vars[0]
    counter.add(1)

    if counter.exhausted:
        return False

    # Branch 1
    branch1 = remaining | all_units | {Var(split_var)}
    ok1 = _refute_with_splitting_sized(branch1, available_vars[1:], counter, rng, cache)

    if not ok1:
        return False

    # Branch 2
    branch2 = remaining | all_units | {Not(Var(split_var))}
    ok2 = _refute_with_splitting_sized(branch2, available_vars[1:], counter, rng, cache)

    return ok1 and ok2


# --- Collapse metric ---

def distinguishing_advantage(
    formula: Formula,
    hypotheses: List[Formula],
    step_limit: int,
    n_trials: int = 10,
    seed: int = None,
    enable_caching: bool = False,
) -> float:
    successes = 0
    for t in range(n_trials):
        s = seed * 1000 + t if seed is not None else None
        success, _, _ = greedy_frege_proof(
            formula, hypotheses, step_limit, seed=s, enable_caching=enable_caching
        )
        if success:
            successes += 1
    return successes / n_trials


def measure_collapse(
    formula: Formula,
    hypotheses: List[Formula],
    step_limit: int,
    n_trials: int = 10,
    seed: int = None,
    enable_caching: bool = False,
) -> float:
    return 1.0 - distinguishing_advantage(
        formula, hypotheses, step_limit, n_trials, seed, enable_caching
    )


if __name__ == "__main__":
    # Calibrate: find step_limit that separates D+ from D-
    from distributions_frege import php_frege, php_target

    for n_p, n_h in [(3, 2), (4, 3), (5, 4), (6, 5)]:
        hyps = php_frege(n_p, n_h)
        tgt = php_target(n_p, n_h)
        for sl in [20, 50, 100, 200, 500]:
            successes = 0
            for s in range(5):
                ok, steps, _ = greedy_frege_proof(tgt, hyps, step_limit=sl, seed=s)
                if ok:
                    successes += 1
            print(f"PHP({n_p},{n_h}) step_limit={sl:4d}: {successes}/5")
        print()
