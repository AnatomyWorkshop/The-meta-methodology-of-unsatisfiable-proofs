import random
from typing import List, Optional, Set, Tuple
from distributions import Clause, Formula


def resolve(c1: Clause, c2: Clause) -> Optional[Clause]:
    """
    Try to resolve c1 and c2 on exactly one variable.
    Returns the resolvent if exactly one complementary literal pair exists,
    None otherwise (tautology or no resolution possible).
    """
    pivot_vars = []
    for (var, pol) in c1:
        if (var, not pol) in c2:
            pivot_vars.append(var)
    if len(pivot_vars) != 1:
        return None
    pivot = pivot_vars[0]
    resolvent = frozenset(
        lit for lit in (c1 | c2)
        if lit[0] != pivot
    )
    # tautology check
    for (var, pol) in resolvent:
        if (var, not pol) in resolvent:
            return None
    return resolvent


def clause_width(clause: Clause) -> int:
    return len(clause)


def proof_width(proof: List[Clause]) -> int:
    if not proof:
        return 0
    return max(clause_width(c) for c in proof)


def greedy_resolution(
    formula: Formula,
    width_limit: int,
    max_steps: int = 5000,
    seed: int = None,
) -> Tuple[bool, int, List[Clause]]:
    """
    Greedy width-limited Resolution solver.
    Tries to derive the empty clause within width_limit.

    Returns (success, min_width_used, proof_clauses).
    - success: True if empty clause derived
    - min_width_used: minimum width of any derived clause (proxy for proof quality)
    - proof_clauses: all clauses generated (including input)
    """
    rng = random.Random(seed)
    clauses: Set[Clause] = set(formula)
    proof: List[Clause] = list(formula)
    empty = frozenset()

    if empty in clauses:
        return True, 0, proof

    for _ in range(max_steps):
        clause_list = list(clauses)
        rng.shuffle(clause_list)
        found_new = False
        for i in range(min(len(clause_list), 50)):
            for j in range(i + 1, min(len(clause_list), 50)):
                resolvent = resolve(clause_list[i], clause_list[j])
                if resolvent is None:
                    continue
                if resolvent in clauses:
                    continue
                if clause_width(resolvent) > width_limit:
                    continue
                clauses.add(resolvent)
                proof.append(resolvent)
                found_new = True
                if resolvent == empty:
                    return True, 0, proof
        if not found_new:
            break

    min_w = min(clause_width(c) for c in proof) if proof else width_limit
    return False, min_w, proof


def distinguishing_advantage(
    formula: Formula,
    n_pigeons: int,
    n_holes: int,
    width_limit: int,
    n_trials: int = 10,
    seed: int = None,
) -> float:
    """
    Run greedy_resolution n_trials times with different seeds.
    Returns fraction of trials that succeed (derive empty clause).
    """
    successes = 0
    for t in range(n_trials):
        s = seed * 1000 + t if seed is not None else None
        success, _, _ = greedy_resolution(formula, width_limit, seed=s)
        if success:
            successes += 1
    return successes / n_trials


def measure_collapse(
    formula: Formula,
    n_pigeons: int,
    n_holes: int,
    width_limit: int,
    n_trials: int = 10,
    seed: int = None,
) -> float:
    """collapse = 1 - distinguishing_advantage"""
    return 1.0 - distinguishing_advantage(
        formula, n_pigeons, n_holes, width_limit, n_trials, seed
    )


if __name__ == "__main__":
    from distributions import php_formula

    # D+ formula: PHP(3,2) — should be provable with small width
    f_easy = php_formula(3, 2)
    success, min_w, proof = greedy_resolution(f_easy, width_limit=3, seed=42)
    print(f"PHP(3,2) width_limit=3: success={success}, proof_len={len(proof)}")

    # D- formula: PHP(6,5) — should NOT be provable with width_limit=4
    f_hard = php_formula(6, 5)
    success2, min_w2, proof2 = greedy_resolution(f_hard, width_limit=4, max_steps=2000, seed=42)
    print(f"PHP(6,5) width_limit=4: success={success2}, proof_len={len(proof2)}")

    # Advantage
    adv_easy = distinguishing_advantage(f_easy, 3, 2, width_limit=3, n_trials=5, seed=42)
    adv_hard = distinguishing_advantage(f_hard, 6, 5, width_limit=4, n_trials=5, seed=42)
    print(f"D+ advantage={adv_easy:.3f}, D- advantage={adv_hard:.3f}")
    print(f"Distinguishing gap = {adv_easy - adv_hard:.3f}")
