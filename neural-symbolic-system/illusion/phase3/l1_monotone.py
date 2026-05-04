"""
L1: Monotone circuit simulator.

Monotone circuits use AND/OR gates only (no NOT). They can only compute
monotone Boolean functions: if you flip any input from 0 to 1, the output
can only stay the same or flip from 0 to 1.

Target function: k-CLIQUE on n-vertex graphs.
Input encoding: (n choose 2) bits, one per possible edge.
"""

import itertools
import random
from enum import Enum
from typing import List, Tuple


class MonotoneGateType(Enum):
    AND = "AND"
    OR = "OR"


class MonotoneGate:
    __slots__ = ("gate_type", "inputs")

    def __init__(self, gate_type: MonotoneGateType, inputs: List[int]):
        self.gate_type = gate_type
        self.inputs = inputs

    def evaluate(self, values: List[bool]) -> bool:
        if self.gate_type == MonotoneGateType.AND:
            return all(values[i] for i in self.inputs) if self.inputs else True
        else:
            return any(values[i] for i in self.inputs) if self.inputs else False


class MonotoneCircuit:
    """
    A monotone circuit: AND/OR gates only, no NOT.
    Conforms to the duck-typed circuit interface: .n_inputs, .depth, .size, .evaluate(x)
    """

    def __init__(self, n_inputs: int, depth: int, gates: List[MonotoneGate]):
        self.n_inputs = n_inputs
        self.depth = depth
        self.gates = gates

    @property
    def size(self) -> int:
        return len(self.gates)

    def evaluate(self, x: Tuple[bool, ...]) -> bool:
        values = list(x) + [False] * len(self.gates)
        for i, gate in enumerate(self.gates):
            values[self.n_inputs + i] = gate.evaluate(values)
        return values[-1] if self.gates else False


def edge_index(u: int, v: int) -> int:
    a, b = max(u, v), min(u, v)
    return a * (a - 1) // 2 + b


def n_edge_bits(n: int) -> int:
    return n * (n - 1) // 2


def k_clique(x: Tuple[bool, ...], n: int, k: int) -> bool:
    """Check if graph encoded by x contains a k-clique."""
    for subset in itertools.combinations(range(n), k):
        if all(x[edge_index(u, v)] for u, v in itertools.combinations(subset, 2)):
            return True
    return False


def random_monotone_circuit(
    n_vertices: int,
    depth: int,
    fan_in_range: Tuple[int, int] = (2, 6),
) -> MonotoneCircuit:
    """
    Generate a random monotone circuit over (n choose 2) input bits.
    Alternates AND/OR layers. No negation.
    """
    n_inputs = n_edge_bits(n_vertices)
    gates = []
    prev_layer = list(range(n_inputs))

    for d in range(depth):
        gate_type = MonotoneGateType.AND if d % 2 == 0 else MonotoneGateType.OR
        layer_size = max(2, n_inputs // (d + 1))
        current_layer = []

        for _ in range(layer_size):
            fan_in = random.randint(fan_in_range[0], min(fan_in_range[1], len(prev_layer)))
            inputs = random.sample(prev_layer, fan_in)
            gates.append(MonotoneGate(gate_type, inputs))
            current_layer.append(n_inputs + len(gates) - 1)

        prev_layer = current_layer

    output_gate = MonotoneGate(MonotoneGateType.OR, prev_layer)
    gates.append(output_gate)

    return MonotoneCircuit(n_inputs, depth, gates)
