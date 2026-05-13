"""
Distribution samplers for monotone circuit lower bounds.

D+: random graph with a planted k-clique
D-: random (k-1)-partite graph (no k-clique by pigeonhole)

Both return Tuple[bool, ...] in edge encoding: bit i corresponds to
edge (u,v) where i = u*(u-1)//2 + v for u > v.
"""

import random
import itertools
from typing import Tuple, List


def n_edges(n: int) -> int:
    return n * (n - 1) // 2


def edge_index(u: int, v: int) -> int:
    """Map edge (u,v) to bit position. Requires u != v."""
    a, b = max(u, v), min(u, v)
    return a * (a - 1) // 2 + b


def sample_d_plus(n: int, k: int) -> Tuple[bool, ...]:
    """
    D+ (positive distribution):
    1. Choose a random k-subset S of [n]
    2. All edges within S are present
    3. Remaining edges present independently with prob 1/2
    """
    m = n_edges(n)
    edges = [False] * m

    clique_vertices = random.sample(range(n), k)
    clique_set = set()
    for u, v in itertools.combinations(clique_vertices, 2):
        clique_set.add(edge_index(u, v))

    for i in range(m):
        if i in clique_set:
            edges[i] = True
        else:
            edges[i] = random.random() < 0.5

    return tuple(edges)


def sample_d_minus(n: int, k: int) -> Tuple[bool, ...]:
    """
    D- (negative distribution):
    1. Partition [n] into (k-1) parts uniformly at random
    2. Edges between different parts present with prob 1/2
    3. No edges within the same part

    A (k-1)-partite graph has no k-clique (pigeonhole).
    """
    m = n_edges(n)
    edges = [False] * m

    parts = [random.randint(0, k - 2) for _ in range(n)]

    for u in range(n):
        for v in range(u):
            if parts[u] != parts[v]:
                edges[edge_index(u, v)] = random.random() < 0.5

    return tuple(edges)
