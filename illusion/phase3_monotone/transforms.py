"""
L2 transformation rule library for monotone circuits.

Each transform operates on monotone circuits and/or evaluation context.
The key insight: in the monotone setting, the discriminating property is
about distribution distinguishing (D+ vs D-), not variance reduction.
"""

import random
from typing import Tuple, List
from l1_monotone import MonotoneCircuit, MonotoneGate, MonotoneGateType, edge_index, n_edge_bits


class MonotoneTransform:
    """Base class for monotone circuit transformations."""
    name: str = "base"

    def apply(self, circuit: MonotoneCircuit, n: int, k: int):
        raise NotImplementedError

    def affects_clique(self, n: int, k: int) -> bool:
        raise NotImplementedError

    def __repr__(self):
        return f"MonotoneTransform({self.name})"


class DistributionSwitch(MonotoneTransform):
    """
    The key transform -- analog of RandomRestriction in Phase 1.

    Does not modify the circuit. Instead, the L2 search evaluates the
    circuit on D+ vs D- distributions and measures distinguishing advantage.
    The "collapse" is the circuit's inability to distinguish the two.

    This is Razborov's approximation method: monotone circuits of bounded
    size cannot distinguish D+ from D- with non-negligible advantage.
    """
    name = "distribution_switch"

    def apply(self, circuit, n, k):
        return circuit

    def affects_clique(self, n, k):
        return False


class EdgeDeletion(MonotoneTransform):
    """
    Randomly delete edges (set inputs to 0).
    Monotone analog of random restriction.

    In a monotone circuit, setting inputs to 0 can only decrease the output.
    Aggressive deletion destroys cliques, so this should be rejected by L2.
    """
    name = "edge_deletion"

    def __init__(self, deletion_prob: float = 0.3):
        self.deletion_prob = deletion_prob
        self.name = f"edge_deletion_p{deletion_prob}"

    def apply(self, circuit, n, k):
        return EdgeDeletedCircuit(circuit, self.deletion_prob)

    def affects_clique(self, n, k):
        return self.deletion_prob > 0.15


class EdgeDeletedCircuit:
    """Wrapper that randomly zeroes out some edge inputs."""

    def __init__(self, original: MonotoneCircuit, deletion_prob: float):
        self.original = original
        self.deletion_prob = deletion_prob
        self.n_inputs = original.n_inputs
        self.depth = original.depth

    @property
    def size(self):
        return self.original.size

    def evaluate(self, x: Tuple[bool, ...]) -> bool:
        modified = tuple(
            False if (v and random.random() < self.deletion_prob) else v
            for v in x
        )
        return self.original.evaluate(modified)


class SubgraphProjection(MonotoneTransform):
    """
    Restrict to an induced subgraph on a random vertex subset.
    Edges between removed vertices are set to 0.
    """
    name = "subgraph_projection"

    def __init__(self, vertex_survival_prob: float = 0.7):
        self.vertex_survival_prob = vertex_survival_prob
        self.name = f"subgraph_projection_p{vertex_survival_prob}"

    def apply(self, circuit, n, k):
        return SubgraphCircuit(circuit, n, self.vertex_survival_prob)

    def affects_clique(self, n, k):
        expected_m = n * self.vertex_survival_prob
        return expected_m < k + 1


class SubgraphCircuit:
    """Wrapper that zeros out edges involving removed vertices."""

    def __init__(self, original: MonotoneCircuit, n_vertices: int, survival_prob: float):
        self.original = original
        self.n_vertices = n_vertices
        self.surviving = {v for v in range(n_vertices) if random.random() < survival_prob}
        self.n_inputs = original.n_inputs
        self.depth = original.depth

    @property
    def size(self):
        return self.original.size

    def evaluate(self, x: Tuple[bool, ...]) -> bool:
        modified = list(x)
        for u in range(self.n_vertices):
            for v in range(u):
                if u not in self.surviving or v not in self.surviving:
                    modified[edge_index(u, v)] = False
        return self.original.evaluate(tuple(modified))


class GateElevation(MonotoneTransform):
    """
    Replace AND gates at the bottom layer with OR gates.
    Still monotone, but changes circuit selectivity.
    Control transform -- expected to affect clique computation.
    """
    name = "gate_elevation"

    def apply(self, circuit, n, k):
        new_gates = []
        for i, gate in enumerate(circuit.gates):
            if i < len(circuit.gates) // 3 and gate.gate_type == MonotoneGateType.AND:
                new_gates.append(MonotoneGate(MonotoneGateType.OR, gate.inputs))
            else:
                new_gates.append(MonotoneGate(gate.gate_type, gate.inputs))
        return MonotoneCircuit(circuit.n_inputs, circuit.depth, new_gates)

    def affects_clique(self, n, k):
        return True


class IdentityTransform(MonotoneTransform):
    """Control: return circuit unchanged."""
    name = "identity"

    def apply(self, circuit, n, k):
        return circuit

    def affects_clique(self, n, k):
        return False


class EdgePermutation(MonotoneTransform):
    """
    Control: permute vertex labels.
    k-CLIQUE is invariant under vertex relabeling.
    """
    name = "edge_permutation"

    def apply(self, circuit, n, k):
        return PermutedCircuit(circuit, n)

    def affects_clique(self, n, k):
        return False


class PermutedCircuit:
    """Wrapper that permutes vertex labels before evaluation."""

    def __init__(self, original: MonotoneCircuit, n_vertices: int):
        self.original = original
        self.n_vertices = n_vertices
        self.perm = list(range(n_vertices))
        random.shuffle(self.perm)
        self.n_inputs = original.n_inputs
        self.depth = original.depth

    @property
    def size(self):
        return self.original.size

    def evaluate(self, x: Tuple[bool, ...]) -> bool:
        m = n_edge_bits(self.n_vertices)
        modified = [False] * m
        for u in range(self.n_vertices):
            for v in range(u):
                old_idx = edge_index(u, v)
                new_u, new_v = self.perm[u], self.perm[v]
                new_idx = edge_index(new_u, new_v)
                if old_idx < len(x):
                    modified[new_idx] = x[old_idx]
        return self.original.evaluate(tuple(modified))


MONOTONE_TRANSFORM_REGISTRY = [
    DistributionSwitch(),
    EdgeDeletion(deletion_prob=0.1),
    EdgeDeletion(deletion_prob=0.3),
    EdgeDeletion(deletion_prob=0.5),
    SubgraphProjection(vertex_survival_prob=0.7),
    SubgraphProjection(vertex_survival_prob=0.5),
    GateElevation(),
    IdentityTransform(),
    EdgePermutation(),
]
