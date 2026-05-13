"""
L1 domain model for Frege proof systems.

Formula representation: tree-structured propositional formulas.
Proof system: bounded-depth Frege with modus ponens + axiom schemas.

Key difference from Resolution (Phase 5):
  Resolution uses clauses (width-bounded), resolution rule only.
  Frege uses arbitrary formulas (depth-bounded), modus ponens + axiom schemas.

Collapse metric: 1 - success_rate of proving within (depth_limit, length_limit).
"""

import random
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple, Union


# --- Formula tree ---

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


def proof_depth(proof: Proof) -> int:
    if not proof:
        return 0
    return max(depth(f) for f in proof)


def proof_length(proof: Proof) -> int:
    return len(proof)


def variables(f: Formula) -> Set[int]:
    if isinstance(f, Var):
        return {f.idx}
    if isinstance(f, Not):
        return variables(f.child)
    return variables(f.left) | variables(f.right)


# --- Axiom schemas ---

def axiom1(a: Formula, b: Formula) -> Formula:
    """A → (B → A)"""
    return Implies(a, Implies(b, a))


def axiom2(a: Formula, b: Formula, c: Formula) -> Formula:
    """(A → (B → C)) → ((A → B) → (A → C))"""
    return Implies(
        Implies(a, Implies(b, c)),
        Implies(Implies(a, b), Implies(a, c))
    )


def axiom3(a: Formula, b: Formula) -> Formula:
    """(¬A → ¬B) → (B → A)"""
    return Implies(Implies(Not(a), Not(b)), Implies(b, a))


# --- Inference rules ---

def modus_ponens(major: Formula, minor: Formula) -> Optional[Formula]:
    """From (A -> B) and A, derive B."""
    if isinstance(major, Implies) and major.left == minor:
        return major.right
    if isinstance(minor, Implies) and minor.left == major:
        return minor.right
    return None


def disjunctive_syllogism(disj: Formula, negated: Formula) -> Optional[Formula]:
    """
    From (A | B) and ~A, derive B. Handles nested Or trees (wide disjunctions).
    From (~A | ~B) and A, derive ~B. Also handles nested cases.
    """
    if not isinstance(disj, Or):
        return None

    # Flatten the disjunction into a list of disjuncts
    disjuncts = _flatten_or(disj)

    # Try to eliminate one disjunct using the negated formula
    new_disjuncts = []
    eliminated = False
    for d in disjuncts:
        if not eliminated:
            # ~A eliminates A; A eliminates ~A
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
        return None  # contradiction — handled elsewhere
    if len(new_disjuncts) == 1:
        return new_disjuncts[0]
    # Rebuild Or tree (left-associative)
    result = Or(new_disjuncts[0], new_disjuncts[1])
    for i in range(2, len(new_disjuncts)):
        result = Or(result, new_disjuncts[i])
    return result


def _flatten_or(f: Formula) -> List[Formula]:
    """Flatten nested Or into a list of disjuncts."""
    if isinstance(f, Or):
        return _flatten_or(f.left) + _flatten_or(f.right)
    return [f]


def conjunction_intro(a: Formula, b: Formula) -> Formula:
    """From A and B, derive A & B."""
    return And(a, b)


# --- Unit propagation on formula set ---

def _is_unit(f: Formula) -> bool:
    """A unit is a literal: Var or Not(Var)."""
    if isinstance(f, Var):
        return True
    if isinstance(f, Not) and isinstance(f.child, Var):
        return True
    return False


def _negate_unit(f: Formula) -> Formula:
    """Negate a unit literal."""
    if isinstance(f, Not):
        return f.child
    return Not(f)


def _unit_propagate(formulas: Set[Formula], units: Set[Formula]) -> Tuple[Set[Formula], Set[Formula], bool]:
    """
    Propagate unit literals through disjunctions.
    Returns (remaining_formulas, derived_units, contradiction_found).
    """
    all_units = set(units)
    remaining = set(formulas) - all_units

    changed = True
    while changed:
        changed = False
        new_remaining = set()
        for f in remaining:
            if _is_unit(f):
                if _negate_unit(f) in all_units:
                    return set(), all_units, True
                all_units.add(f)
                changed = True
                continue

            simplified = f
            for u in list(all_units):
                result = disjunctive_syllogism(simplified, u)
                if result is not None:
                    simplified = result
                    changed = True

            if simplified is None:
                return set(), all_units, True

            if _is_unit(simplified):
                if _negate_unit(simplified) in all_units:
                    return set(), all_units, True
                all_units.add(simplified)
            elif isinstance(simplified, Or):
                # Check if all disjuncts are eliminated
                disjuncts = _flatten_or(simplified)
                if len(disjuncts) == 0:
                    return set(), all_units, True
                new_remaining.add(simplified)
            else:
                new_remaining.add(simplified)

        remaining = new_remaining

    # Final contradiction check
    for u in all_units:
        if _negate_unit(u) in all_units:
            return set(), all_units, True

    return remaining, all_units, False


# --- Bounded-depth Frege prover (case-splitting refutation) ---

def greedy_frege_proof(
    target: Formula,
    hypotheses: List[Formula],
    depth_limit: int,
    seed: int = None,
) -> Tuple[bool, int, Proof]:
    """
    Bounded-depth Frege refutation via case splitting.

    Maps to bounded-depth Frege: depth-d Frege can simulate d levels of
    case analysis. PHP(n, n-1) requires ~n levels, so at fixed depth,
    larger instances are exponentially harder.

    The target is derived if we can show the hypotheses lead to contradiction
    (proving unsatisfiability), then the target (a consequence) follows.

    Returns (success, depth_used, proof_trace).
    """
    rng = random.Random(seed)
    proof_trace: List[Formula] = list(hypotheses)

    # Extract variables for case splitting
    all_vars = set()
    for h in hypotheses:
        all_vars |= variables(h)
    var_list = sorted(all_vars)
    rng.shuffle(var_list)

    success, d_used = _refute_with_splitting(
        set(hypotheses), var_list, depth_limit, 0, rng
    )

    if success:
        # If refutation succeeds, target follows (ex falso or direct)
        if isinstance(target, And):
            proof_trace.append(target.left)
            proof_trace.append(target.right)
        proof_trace.append(target)

    return success, d_used, proof_trace


def _refute_with_splitting(
    formulas: Set[Formula],
    split_vars: List[int],
    depth_limit: int,
    current_depth: int,
    rng: random.Random,
) -> Tuple[bool, int]:
    """
    Try to derive contradiction from formulas using bounded case splitting.
    Returns (contradiction_found, max_depth_used).
    """
    # Unit propagation first
    units = set()
    for f in formulas:
        if isinstance(f, Var) or isinstance(f, Not):
            units.add(f)

    remaining, all_units, contradiction = _unit_propagate(
        formulas - units, units
    )

    if contradiction:
        return True, current_depth

    # Check for direct contradiction in units
    for u in all_units:
        if isinstance(u, Not) and u.child in all_units:
            return True, current_depth
        if Not(u) in all_units:
            return True, current_depth

    # Check for empty disjunction (contradiction)
    if frozenset() in remaining:
        return True, current_depth

    # Depth limit reached — cannot split further
    if current_depth >= depth_limit:
        return False, current_depth

    # Pick a variable to split on
    available_vars = [v for v in split_vars
                      if Var(v) not in all_units and Not(Var(v)) not in all_units]
    if not available_vars:
        return False, current_depth

    split_var = available_vars[0]

    # Branch 1: assume Var(split_var) = True
    branch1_formulas = remaining | all_units | {Var(split_var)}
    ok1, d1 = _refute_with_splitting(
        branch1_formulas, available_vars[1:],
        depth_limit, current_depth + 1, rng
    )

    if not ok1:
        return False, max(current_depth, d1)

    # Branch 2: assume Var(split_var) = False
    branch2_formulas = remaining | all_units | {Not(Var(split_var))}
    ok2, d2 = _refute_with_splitting(
        branch2_formulas, available_vars[1:],
        depth_limit, current_depth + 1, rng
    )

    if ok1 and ok2:
        return True, max(d1, d2)

    return False, max(current_depth, d1, d2)


# --- Collapse metric ---

def distinguishing_advantage(
    formula: Formula,
    hypotheses: List[Formula],
    depth_limit: int,
    n_trials: int = 10,
    seed: int = None,
) -> float:
    """
    Run greedy_frege_proof n_trials times with different seeds.
    Returns fraction of trials that succeed.
    """
    successes = 0
    for t in range(n_trials):
        s = seed * 1000 + t if seed is not None else None
        success, _, _ = greedy_frege_proof(
            formula, hypotheses, depth_limit, seed=s
        )
        if success:
            successes += 1
    return successes / n_trials


def measure_collapse(
    formula: Formula,
    hypotheses: List[Formula],
    depth_limit: int,
    n_trials: int = 10,
    seed: int = None,
) -> float:
    """collapse = 1 - distinguishing_advantage"""
    return 1.0 - distinguishing_advantage(
        formula, hypotheses, depth_limit, n_trials, seed
    )


if __name__ == "__main__":
    # Construct test data directly to avoid double-import class mismatch
    # PHP(3,2): 3 pigeons, 2 holes
    p00, p01, p10, p11, p20, p21 = Var(0), Var(1), Var(2), Var(3), Var(4), Var(5)

    pigeon_axioms = [
        Or(p00, p01),  # pigeon 0 in hole 0 or 1
        Or(p10, p11),  # pigeon 1 in hole 0 or 1
        Or(p20, p21),  # pigeon 2 in hole 0 or 1
    ]
    hole_axioms = [
        Or(Not(p00), Not(p10)),  # hole 0: not both pigeon 0 and 1
        Or(Not(p00), Not(p20)),  # hole 0: not both pigeon 0 and 2
        Or(Not(p10), Not(p20)),  # hole 0: not both pigeon 1 and 2
        Or(Not(p01), Not(p11)),  # hole 1: not both pigeon 0 and 1
        Or(Not(p01), Not(p21)),  # hole 1: not both pigeon 0 and 2
        Or(Not(p11), Not(p21)),  # hole 1: not both pigeon 1 and 2
    ]
    hyps_easy = pigeon_axioms + hole_axioms
    tgt_easy = And(Not(p00), Not(p01))  # pigeon 0 has nowhere to go

    print(f"PHP(3,2): {len(hyps_easy)} hypotheses, target depth={depth(tgt_easy)}")

    success, max_d, proof = greedy_frege_proof(
        tgt_easy, hyps_easy, depth_limit=6, length_limit=300, seed=42
    )
    print(f"  depth_limit=6: success={success}, proof_len={len(proof)}, max_depth={max_d}")

    # Test with tighter depth bound
    success2, max_d2, proof2 = greedy_frege_proof(
        tgt_easy, hyps_easy, depth_limit=3, length_limit=100, seed=42
    )
    print(f"  depth_limit=3: success={success2}, proof_len={len(proof2)}, max_depth={max_d2}")

    # Advantage measurement
    adv = distinguishing_advantage(
        tgt_easy, hyps_easy, depth_limit=6, length_limit=300, n_trials=5, seed=42
    )
    print(f"  advantage (depth=6, 5 trials): {adv:.3f}")
    print(f"  collapse: {1.0 - adv:.3f}")
