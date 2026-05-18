"""
Evaluator for Phase 9: measures distinguishing advantage using a treewidth-bounded solver.

The solver attempts to decide Hamiltonicity using a greedy/DP approach that works
well on bounded-treewidth graphs but degrades on high-treewidth graphs.
"""

import random
from typing import List, Tuple
from l1_graphs import Graph, is_hamiltonian, compute_treewidth_exact


def tw_bounded_hamiltonicity_solver(g: Graph, tw_bound: int) -> bool:
    """
    Simulates a tw-bounded solver for Hamiltonicity.

    If tw(g) <= tw_bound: uses exact algorithm (simulating Courcelle's theorem).
    If tw(g) > tw_bound: the solver "fails" — returns a random guess.

    This models the key property: bounded-tw algorithms lose their power
    when the graph exceeds the treewidth bound.
    """
    tw = compute_treewidth_exact(g)
    if tw <= tw_bound:
        return is_hamiltonian(g)
    else:
        # Solver cannot handle this — returns random (50% accuracy)
        return random.random() < 0.5


def measure_distinguishing_advantage(
    d_plus: List[Tuple[Graph, int, int]],
    d_minus: List[Tuple[Graph, int, int]],
    tw_bound: int,
    n_trials: int = 5,
    seed: int = 42,
) -> float:
    """
    Measure the solver's ability to distinguish D+ (Hamiltonian) from D- (non-Hamiltonian).

    Advantage = |Pr[solver says YES | D+] - Pr[solver says YES | D-]|

    For bounded-tw graphs: advantage should be high (solver works correctly).
    After a transform that increases tw: advantage drops (solver guesses randomly).
    """
    rng = random.Random(seed)

    total_correct_plus = 0
    total_correct_minus = 0
    total_plus = 0
    total_minus = 0

    for trial in range(n_trials):
        trial_seed = seed + trial * 1000
        random.seed(trial_seed)

        for g, n_v, tw_b in d_plus:
            result = tw_bounded_hamiltonicity_solver(g, tw_bound)
            if result:  # solver says "yes, Hamiltonian"
                total_correct_plus += 1
            total_plus += 1

        for g, n_v, tw_b in d_minus:
            result = tw_bounded_hamiltonicity_solver(g, tw_bound)
            if not result:  # solver says "no, not Hamiltonian"
                total_correct_minus += 1
            total_minus += 1

    pr_yes_given_plus = total_correct_plus / max(total_plus, 1)
    pr_yes_given_minus = 1.0 - (total_correct_minus / max(total_minus, 1))

    advantage = abs(pr_yes_given_plus - pr_yes_given_minus)
    return advantage
