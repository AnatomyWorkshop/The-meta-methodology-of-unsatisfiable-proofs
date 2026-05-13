"""
L1: AC⁰ circuit simulator.

Generates and evaluates constant-depth, polynomial-size circuits
with AND/OR/NOT gates. Target function: PARITY (known to be outside AC⁰).
"""

import random
from enum import Enum
from typing import List, Tuple, Optional


class GateType(Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    INPUT = "INPUT"


class Gate:
    __slots__ = ("gate_type", "inputs", "negated")

    def __init__(self, gate_type: GateType, inputs: List[int], negated: bool = False):
        self.gate_type = gate_type
        self.inputs = inputs
        self.negated = negated

    def evaluate(self, values: List[bool]) -> bool:
        if self.gate_type == GateType.INPUT:
            val = values[self.inputs[0]]
        elif self.gate_type == GateType.AND:
            val = all(values[i] for i in self.inputs)
        elif self.gate_type == GateType.OR:
            val = any(values[i] for i in self.inputs)
        elif self.gate_type == GateType.NOT:
            val = not values[self.inputs[0]]
        else:
            raise ValueError(f"Unknown gate type: {self.gate_type}")
        return (not val) if self.negated else val


class AC0Circuit:
    """
    A constant-depth circuit with unbounded fan-in AND/OR gates.
    Gates are stored in topological order; the last gate is the output.
    """

    def __init__(self, n_inputs: int, depth: int, gates: List[Gate]):
        self.n_inputs = n_inputs
        self.depth = depth
        self.gates = gates

    def evaluate(self, x: Tuple[bool, ...]) -> bool:
        values = list(x)
        for gate in self.gates:
            values.append(gate.evaluate(values))
        return values[-1]

    @property
    def size(self) -> int:
        return len(self.gates)


def parity(x: Tuple[bool, ...]) -> bool:
    return sum(x) % 2 == 1


def random_ac0_circuit(n: int, depth: int, fan_in_range: Tuple[int, int] = (2, 6)) -> AC0Circuit:
    """
    Generate a random AC⁰ circuit of given depth over n inputs.
    Alternates AND/OR layers. Each gate picks random inputs from the previous layer.
    """
    gates: List[Gate] = []
    prev_layer_indices = list(range(n))  # input indices

    for d in range(depth):
        gate_type = GateType.AND if d % 2 == 0 else GateType.OR
        layer_size = max(2, n // (d + 1))
        layer_indices = []

        for _ in range(layer_size):
            fan_in = random.randint(*fan_in_range)
            fan_in = min(fan_in, len(prev_layer_indices))
            inputs = random.sample(prev_layer_indices, fan_in)
            negated = random.random() < 0.3
            gates.append(Gate(gate_type, inputs, negated))
            layer_indices.append(n + len(gates) - 1)

        prev_layer_indices = layer_indices

    # output gate: OR of last layer
    if len(prev_layer_indices) > 1:
        gates.append(Gate(GateType.OR, prev_layer_indices))
    else:
        gates.append(Gate(GateType.OR, prev_layer_indices))

    return AC0Circuit(n, depth, gates)


def enumerate_small_circuits(n: int, depth: int, max_size: int) -> List[AC0Circuit]:
    """Generate a batch of random AC⁰ circuits for sampling."""
    circuits = []
    for _ in range(max_size):
        circuits.append(random_ac0_circuit(n, depth))
    return circuits
