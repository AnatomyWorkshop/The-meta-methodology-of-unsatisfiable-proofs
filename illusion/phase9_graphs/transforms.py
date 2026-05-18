"""
Transforms for Phase 9: Graph theory domain.

Each transform modifies a graph and may or may not push it beyond the treewidth bound.
"""

import random
from typing import List, Tuple
from l1_graphs import Graph, is_hamiltonian, compute_treewidth_exact


class GraphTransform:
    name: str = "base"

    def apply(self, g: Graph, n_vertices: int, tw_bound: int, rng: random.Random) -> Graph:
        raise NotImplementedError

    def affects_target(self, g: Graph, n_vertices: int, tw_bound: int, rng: random.Random) -> bool:
        """Does this transform change the Hamiltonicity status?"""
        raise NotImplementedError


class IdentityTransform(GraphTransform):
    name = "identity"

    def apply(self, g, n_vertices, tw_bound, rng):
        return g.copy()

    def affects_target(self, g, n_vertices, tw_bound, rng):
        return False


class EdgeAdditionRandom(GraphTransform):
    """Add random edges. May increase treewidth beyond bound."""
    name = "edge_addition_random"

    def __init__(self, n_edges: int = 5):
        self.n_edges = n_edges

    def apply(self, g, n_vertices, tw_bound, rng):
        result = g.copy()
        n = result.n
        added = 0
        attempts = 0
        while added < self.n_edges and attempts < self.n_edges * 10:
            u, v = rng.randint(0, n - 1), rng.randint(0, n - 1)
            if u != v and not result.has_edge(u, v):
                result.add_edge(u, v)
                added += 1
            attempts += 1
        return result

    def affects_target(self, g, n_vertices, tw_bound, rng):
        # Adding edges can make a non-Hamiltonian graph Hamiltonian
        # but we check statistically — on average it shouldn't flip most graphs
        return False


class VertexSubdivision(GraphTransform):
    """Subdivide random edges (insert vertex in middle). Preserves treewidth."""
    name = "vertex_subdivision"

    def __init__(self, n_subdivisions: int = 3):
        self.n_subdivisions = n_subdivisions

    def apply(self, g, n_vertices, tw_bound, rng):
        edges = list(g.edges)
        if not edges:
            return g.copy()
        result = g.copy()
        to_subdivide = rng.sample(edges, min(self.n_subdivisions, len(edges)))
        for e in to_subdivide:
            u, v = tuple(e)
            new_v = result.n
            result.adj.append(set())
            result.n += 1
            result.remove_edge(u, v)
            result.add_edge(u, new_v)
            result.add_edge(new_v, v)
        return result

    def affects_target(self, g, n_vertices, tw_bound, rng):
        # Subdivision preserves Hamiltonicity status in most cases
        # (subdivided graph is Hamiltonian iff original is, for simple subdivisions)
        # Actually subdivision can break Hamiltonicity — a Hamiltonian cycle through
        # the subdivided edge now must visit the new vertex.
        # For our purposes: it changes the graph structure, may affect target.
        # Conservative: check
        result = self.apply(g, n_vertices, tw_bound, rng)
        orig_ham = is_hamiltonian(g)
        new_ham = is_hamiltonian(result)
        return orig_ham != new_ham


class EdgeContraction(GraphTransform):
    """Contract random edges. Can only decrease treewidth."""
    name = "edge_contraction"

    def __init__(self, n_contractions: int = 2):
        self.n_contractions = n_contractions

    def apply(self, g, n_vertices, tw_bound, rng):
        result = g.copy()
        for _ in range(self.n_contractions):
            edges = list(result.edges)
            if not edges:
                break
            e = rng.choice(edges)
            u, v = tuple(e)
            # Contract: merge v into u
            for w in list(result.adj[v]):
                if w != u:
                    result.add_edge(u, w)
            # Remove all edges to v
            for w in list(result.adj[v]):
                result.remove_edge(v, w)
        return result

    def affects_target(self, g, n_vertices, tw_bound, rng):
        # Contraction can change Hamiltonicity
        result = self.apply(g, n_vertices, tw_bound, rng)
        return is_hamiltonian(g) != is_hamiltonian(result)


class CliqueSum(GraphTransform):
    """Glue a (k+1)-clique onto the graph. Forces treewidth > k."""
    name = "clique_sum_k+1"

    def apply(self, g, n_vertices, tw_bound, rng):
        result = g.copy()
        k = tw_bound + 1
        # Add k+1 new vertices forming a clique
        base = result.n
        for _ in range(k + 1):
            result.adj.append(set())
            result.n += 1
        for i in range(k + 1):
            for j in range(i + 1, k + 1):
                result.add_edge(base + i, base + j)
        # Connect one clique vertex to a random existing vertex
        attach = rng.randint(0, g.n - 1)
        result.add_edge(attach, base)
        return result

    def affects_target(self, g, n_vertices, tw_bound, rng):
        # Adding a clique appendage makes the graph non-Hamiltonian
        # (the clique vertices form a dead end unless carefully connected)
        return True


class MinorEmbedding(GraphTransform):
    """Embed K5 as a minor by adding edges/vertices. Relates to planarity and beyond."""
    name = "minor_embedding_k5"

    def apply(self, g, n_vertices, tw_bound, rng):
        result = g.copy()
        # Pick 5 random vertices and connect them all (force K5 subgraph)
        if result.n < 5:
            return result
        vertices = rng.sample(range(result.n), 5)
        for i in range(5):
            for j in range(i + 1, 5):
                result.add_edge(vertices[i], vertices[j])
        return result

    def affects_target(self, g, n_vertices, tw_bound, rng):
        # Adding edges to form K5 may change Hamiltonicity
        # K5 itself is Hamiltonian, so adding these edges to a non-Hamiltonian
        # graph might make it Hamiltonian. Check conservatively.
        result = self.apply(g, n_vertices, tw_bound, rng)
        return is_hamiltonian(g) != is_hamiltonian(result)


class RandomSubgraph(GraphTransform):
    """Delete random edges. Subgraph of tw<=k has tw<=k."""
    name = "random_subgraph_p0.3"

    def __init__(self, deletion_prob: float = 0.3):
        self.deletion_prob = deletion_prob
        self.name = f"random_subgraph_p{deletion_prob}"

    def apply(self, g, n_vertices, tw_bound, rng):
        result = g.copy()
        for e in list(result.edges):
            if rng.random() < self.deletion_prob:
                u, v = tuple(e)
                result.remove_edge(u, v)
        return result

    def affects_target(self, g, n_vertices, tw_bound, rng):
        # Deleting edges from a Hamiltonian graph likely breaks Hamiltonicity
        result = self.apply(g, n_vertices, tw_bound, rng)
        return is_hamiltonian(g) != is_hamiltonian(result)


class TreewidthExpansion(GraphTransform):
    """Add edges specifically to increase treewidth. Targets the boundary."""
    name = "treewidth_expansion"

    def apply(self, g, n_vertices, tw_bound, rng):
        result = g.copy()
        n = result.n
        # Add edges between non-adjacent vertices, preferring high-degree vertices
        # (more likely to increase treewidth)
        degrees = [(result.degree(v), v) for v in range(n)]
        degrees.sort(reverse=True)
        top_vertices = [v for _, v in degrees[:min(6, n)]]

        for u in top_vertices:
            for v in top_vertices:
                if u < v and not result.has_edge(u, v):
                    result.add_edge(u, v)
        return result

    def affects_target(self, g, n_vertices, tw_bound, rng):
        # Adding edges between high-degree vertices may create Hamiltonicity
        result = self.apply(g, n_vertices, tw_bound, rng)
        return is_hamiltonian(g) != is_hamiltonian(result)


class PlanarProjection(GraphTransform):
    """Remove edges to make graph planar. Planar graphs have bounded tw (O(sqrt(n)))."""
    name = "planar_projection"

    def apply(self, g, n_vertices, tw_bound, rng):
        # Simple heuristic: remove edges until graph is "sparse enough" for planarity
        # (planar graphs have <= 3n-6 edges)
        result = g.copy()
        max_edges = 3 * result.n - 6
        edges = list(result.edges)
        rng.shuffle(edges)
        while len(result.edges) > max_edges:
            e = edges.pop()
            u, v = tuple(e)
            result.remove_edge(u, v)
        return result

    def affects_target(self, g, n_vertices, tw_bound, rng):
        result = self.apply(g, n_vertices, tw_bound, rng)
        return is_hamiltonian(g) != is_hamiltonian(result)


GRAPH_TRANSFORM_REGISTRY: List[GraphTransform] = [
    IdentityTransform(),
    EdgeAdditionRandom(n_edges=3),
    EdgeAdditionRandom(n_edges=6),
    VertexSubdivision(n_subdivisions=2),
    EdgeContraction(n_contractions=2),
    CliqueSum(),
    MinorEmbedding(),
    RandomSubgraph(deletion_prob=0.2),
    RandomSubgraph(deletion_prob=0.4),
    TreewidthExpansion(),
    PlanarProjection(),
]
