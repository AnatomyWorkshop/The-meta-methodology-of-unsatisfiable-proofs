"""
L1: Graph domain model for Illusion Phase 9.

Model M = graphs with bounded treewidth (tw <= k).
Target f = Hamiltonicity.
Decidability boundary: Courcelle's theorem (MSO2 on bounded tw = linear time).
"""

import itertools
import random
from typing import List, Set, Tuple, Optional, FrozenSet


class Graph:
    """Simple undirected graph via adjacency sets."""

    def __init__(self, n_vertices: int, edges: Optional[Set[Tuple[int, int]]] = None):
        self.n = n_vertices
        self.adj: List[Set[int]] = [set() for _ in range(n_vertices)]
        self.edges: Set[FrozenSet[int]] = set()
        if edges:
            for u, v in edges:
                self.add_edge(u, v)

    def add_edge(self, u: int, v: int):
        if u == v or u < 0 or v < 0 or u >= self.n or v >= self.n:
            return
        self.adj[u].add(v)
        self.adj[v].add(u)
        self.edges.add(frozenset((u, v)))

    def remove_edge(self, u: int, v: int):
        self.adj[u].discard(v)
        self.adj[v].discard(u)
        self.edges.discard(frozenset((u, v)))

    def has_edge(self, u: int, v: int) -> bool:
        return frozenset((u, v)) in self.edges

    def degree(self, v: int) -> int:
        return len(self.adj[v])

    def copy(self) -> 'Graph':
        g = Graph(self.n)
        for e in self.edges:
            u, v = tuple(e)
            g.add_edge(u, v)
        return g

    @property
    def num_edges(self) -> int:
        return len(self.edges)


def is_hamiltonian(g: Graph) -> bool:
    """Check Hamiltonicity via backtracking. Exact, exponential worst-case."""
    n = g.n
    if n < 3:
        return False
    if any(g.degree(v) < 2 for v in range(n)):
        return False

    path = [0]
    visited = {0}

    def backtrack() -> bool:
        if len(path) == n:
            return path[0] in g.adj[path[-1]]
        last = path[-1]
        for nxt in sorted(g.adj[last]):
            if nxt not in visited:
                path.append(nxt)
                visited.add(nxt)
                if backtrack():
                    return True
                path.pop()
                visited.remove(nxt)
        return False

    return backtrack()


def compute_treewidth_exact(g: Graph) -> int:
    """
    Upper bound on treewidth via greedy min-degree elimination.
    Fast (O(n^2)) and gives exact results for small/sparse graphs.
    For our purposes (tw <= 3 check), this is sufficient.
    """
    n = g.n
    if n <= 1:
        return 0
    if n == 2:
        return 1 if g.has_edge(0, 1) else 0

    # Greedy min-degree elimination (gives upper bound, often exact for small tw)
    adj = [set(g.adj[v]) for v in range(n)]
    remaining = set(range(n))
    width = 0

    while remaining:
        v = min(remaining, key=lambda x: len(adj[x] & remaining))
        neighbors = adj[v] & remaining
        width = max(width, len(neighbors))
        for u, w in itertools.combinations(neighbors, 2):
            adj[u].add(w)
            adj[w].add(u)
        remaining.remove(v)

    return width


def generate_bounded_tw_graph(n: int, tw_bound: int, rng: random.Random) -> Graph:
    """
    Generate a random graph with treewidth <= tw_bound.
    Strategy: start with a random tree (tw=1), then add edges greedily
    while maintaining tw <= tw_bound.
    """
    g = Graph(n)

    # Build a random spanning tree
    vertices = list(range(n))
    rng.shuffle(vertices)
    for i in range(1, n):
        parent = rng.choice(vertices[:i])
        g.add_edge(vertices[i], parent)

    # Add random edges while tw stays within bound
    all_possible = [(u, v) for u in range(n) for v in range(u + 1, n)
                    if not g.has_edge(u, v)]
    rng.shuffle(all_possible)

    for u, v in all_possible[:n * tw_bound]:
        g.add_edge(u, v)
        if compute_treewidth_exact(g) > tw_bound:
            g.remove_edge(u, v)

    return g


def generate_hamiltonian_bounded_tw(n: int, tw_bound: int, rng: random.Random) -> Optional[Graph]:
    """Generate a Hamiltonian graph with tw <= tw_bound."""
    # Strategy: start with a Hamiltonian cycle, then verify tw
    for _ in range(100):
        g = Graph(n)
        # Create a Hamiltonian cycle
        perm = list(range(n))
        rng.shuffle(perm)
        for i in range(n):
            g.add_edge(perm[i], perm[(i + 1) % n])

        # Add a few random edges (cycles have tw=2, adding edges may increase)
        extra = rng.randint(0, min(n, tw_bound * n // 2))
        for _ in range(extra):
            u, v = rng.randint(0, n - 1), rng.randint(0, n - 1)
            if u != v and not g.has_edge(u, v):
                g.add_edge(u, v)
                if compute_treewidth_exact(g) > tw_bound:
                    g.remove_edge(u, v)

        if is_hamiltonian(g) and compute_treewidth_exact(g) <= tw_bound:
            return g
    return None


def generate_non_hamiltonian_bounded_tw(n: int, tw_bound: int, rng: random.Random) -> Optional[Graph]:
    """Generate a non-Hamiltonian graph with tw <= tw_bound."""
    for _ in range(100):
        # Strategy: tree with some extra edges (trees are never Hamiltonian for n>2)
        g = Graph(n)
        # Random tree
        vertices = list(range(n))
        rng.shuffle(vertices)
        for i in range(1, n):
            parent = rng.choice(vertices[:i])
            g.add_edge(vertices[i], parent)

        # Add a few edges but try to keep non-Hamiltonian
        # (keep a vertex with degree 1 to guarantee non-Hamiltonicity)
        leaves = [v for v in range(n) if g.degree(v) == 1]
        if not leaves:
            continue
        protected_leaf = rng.choice(leaves)

        extra = rng.randint(0, n // 2)
        for _ in range(extra):
            u, v = rng.randint(0, n - 1), rng.randint(0, n - 1)
            if u == protected_leaf or v == protected_leaf:
                continue
            if u != v and not g.has_edge(u, v):
                g.add_edge(u, v)
                if compute_treewidth_exact(g) > tw_bound:
                    g.remove_edge(u, v)

        if not is_hamiltonian(g) and compute_treewidth_exact(g) <= tw_bound:
            return g
    return None
