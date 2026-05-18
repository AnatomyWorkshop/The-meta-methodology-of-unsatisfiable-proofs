"""
Distributions for Phase 9: Hamiltonian vs non-Hamiltonian bounded-treewidth graphs.
"""

import random
from typing import List, Tuple
from l1_graphs import Graph, generate_hamiltonian_bounded_tw, generate_non_hamiltonian_bounded_tw


def sample_d_plus(
    n_graphs: int, n_vertices: int = 12, tw_bound: int = 3, seed: int = 42
) -> List[Tuple[Graph, int, int]]:
    """D+: Hamiltonian graphs with tw <= tw_bound."""
    rng = random.Random(seed)
    graphs = []
    for _ in range(n_graphs):
        g = generate_hamiltonian_bounded_tw(n_vertices, tw_bound, rng)
        if g is not None:
            graphs.append((g, n_vertices, tw_bound))
    return graphs


def sample_d_minus(
    n_graphs: int, n_vertices: int = 12, tw_bound: int = 3, seed: int = 42
) -> List[Tuple[Graph, int, int]]:
    """D-: Non-Hamiltonian graphs with tw <= tw_bound."""
    rng = random.Random(seed)
    graphs = []
    for _ in range(n_graphs):
        g = generate_non_hamiltonian_bounded_tw(n_vertices, tw_bound, rng)
        if g is not None:
            graphs.append((g, n_vertices, tw_bound))
    return graphs
