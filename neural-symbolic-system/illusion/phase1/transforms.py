"""
L2 transformation rule library.

Each transform takes an AC⁰ circuit and returns a modified circuit.
These are the "candidate discriminating properties" that L2 searches over:
a transform T is useful if applying T causes AC⁰ circuits to degrade
(error rate locked above ε) while PARITY remains unaffected.
"""

import random
from typing import Tuple, Optional
from l1_circuit import AC0Circuit, Gate, GateType


class Transform:
    """Base class for circuit transformations."""

    name: str = "base"

    def apply(self, circuit: AC0Circuit) -> AC0Circuit:
        raise NotImplementedError

    def affects_parity(self, n: int) -> bool:
        """
        Does this transform cause PARITY to 'collapse'?
        Returns True if PARITY becomes trivial after transform.
        For a useful discriminating property, this should return False.
        """
        raise NotImplementedError

    def __repr__(self):
        return f"Transform({self.name})"


class RandomRestriction(Transform):
    """
    Fix a random subset of inputs to random values.
    This is the key transform from Håstad's proof:
    - AC⁰ circuits collapse to shallow decision trees
    - PARITY on remaining variables stays hard

    Instead of rebuilding the circuit, we evaluate the original circuit
    with fixed inputs substituted, measuring error on the restricted function.
    """

    name = "random_restriction"

    def __init__(self, survival_prob: float = 0.5):
        self.survival_prob = survival_prob

    def apply(self, circuit: AC0Circuit) -> "RestrictedCircuit":
        n = circuit.n_inputs
        surviving = []
        fixed = {}

        for i in range(n):
            if random.random() < self.survival_prob:
                surviving.append(i)
            else:
                fixed[i] = random.choice([True, False])

        if not surviving:
            surviving = [0]
            if 0 in fixed:
                del fixed[0]

        return RestrictedCircuit(circuit, fixed, surviving)

    def affects_parity(self, n: int) -> bool:
        return False


class RestrictedCircuit:
    """A circuit with some inputs fixed. Behaves like an AC0Circuit for evaluation."""

    def __init__(self, original: AC0Circuit, fixed: dict, surviving: list):
        self.original = original
        self.fixed = fixed
        self.surviving = surviving
        self.n_inputs = len(surviving)
        self.depth = original.depth

    def evaluate(self, x: Tuple[bool, ...]) -> bool:
        full_input = []
        free_idx = 0
        for i in range(self.original.n_inputs):
            if i in self.fixed:
                full_input.append(self.fixed[i])
            else:
                full_input.append(x[free_idx])
                free_idx += 1
        return self.original.evaluate(tuple(full_input))

    @property
    def size(self) -> int:
        return self.original.size


class GateSubstitution(Transform):
    """
    Replace AND gates with OR gates (or vice versa) at a random layer.
    A 'null' transform — unlikely to be a useful discriminating property.
    """

    name = "gate_substitution"

    def __init__(self, target_type: GateType = GateType.AND, replacement: GateType = GateType.OR):
        self.target_type = target_type
        self.replacement = replacement

    def apply(self, circuit: AC0Circuit) -> AC0Circuit:
        new_gates = []
        for gate in circuit.gates:
            if gate.gate_type == self.target_type:
                new_gates.append(Gate(self.replacement, gate.inputs, gate.negated))
            else:
                new_gates.append(Gate(gate.gate_type, gate.inputs, gate.negated))
        return AC0Circuit(circuit.n_inputs, circuit.depth, new_gates)

    def affects_parity(self, n: int) -> bool:
        return True  # destroys structure, PARITY also affected


class InputPermutation(Transform):
    """
    Permute input variables. Should not change error rate
    (PARITY is symmetric, and random circuits are statistically symmetric).
    A 'control' transform.
    """

    name = "input_permutation"

    def apply(self, circuit: AC0Circuit) -> AC0Circuit:
        n = circuit.n_inputs
        perm = list(range(n))
        random.shuffle(perm)
        inv_perm = [0] * n
        for i, p in enumerate(perm):
            inv_perm[p] = i

        new_gates = []
        for gate in circuit.gates:
            new_inputs = []
            for inp in gate.inputs:
                if inp < n:
                    new_inputs.append(inv_perm[inp])
                else:
                    new_inputs.append(inp)
            new_gates.append(Gate(gate.gate_type, new_inputs, gate.negated))
        return AC0Circuit(n, circuit.depth, new_gates)

    def affects_parity(self, n: int) -> bool:
        return False  # PARITY is symmetric


class DepthReduction(Transform):
    """
    Collapse the bottom two layers into one by removing the first layer of gates
    and connecting the second layer directly to inputs.
    Reduces depth but may lose precision.
    """

    name = "depth_reduction"

    def apply(self, circuit: AC0Circuit) -> AC0Circuit:
        if circuit.depth <= 1 or len(circuit.gates) <= 1:
            return circuit
        # Keep only the top half of gates, remap inputs to raw input indices
        n = circuit.n_inputs
        mid = len(circuit.gates) // 2
        new_gates = []
        for gate in circuit.gates[mid:]:
            new_inputs = [inp if inp < n else max(0, inp - mid) for inp in gate.inputs]
            new_inputs = [min(i, n + len(new_gates) - 1) if i >= n else i for i in new_inputs]
            if not new_inputs:
                new_inputs = [0]
            new_gates.append(Gate(gate.gate_type, new_inputs, gate.negated))
        return AC0Circuit(n, max(1, circuit.depth - 1), new_gates)

    def affects_parity(self, n: int) -> bool:
        return True


class ExhaustiveParityEquivalentCheck(Transform):
    """
    Pressure-test transform designed to reach L3 (not be filtered by L2).

    Behavior:
    - If circuit is equivalent to PARITY: return circuit unchanged (collapse low)
    - If circuit is NOT equivalent to PARITY: replace with constant 0 (collapse high)

    This satisfies L2's filter:
    - affects_parity = False: PARITY itself passes the equivalence test, stays unchanged
    - avg_collapse will be high: almost all random AC^0 circuits are not PARITY-equivalent

    The L3 question this forces: is "deciding whether a circuit is PARITY-equivalent"
    self-referentially safe?

    The answer is subtle:
    - Deciding equivalence requires enumerating all 2^n inputs: O(2^n) work
    - For fixed n this is O(1), so technically in AC^0 (finite lookup)
    - But asymptotically, this is exponential — it does NOT fit in AC^0

    However: this transform does NOT reveal structural weakness in AC^0.
    It brute-forces equivalence rather than exploiting architectural fragility.
    A correct L3 should mark this UNKNOWN, then human review should mark UNSAFE:
    "exponential enumeration alone is not sufficient for self-referential safety —
    the property must reveal why AC^0 circuits fail, not just detect that they do."

    If L3 incorrectly marks this SAFE (because "exponential enumeration → safe"),
    it has the blind spot: exponential cost ≠ self-referential safety.
    """

    name = "exhaustive_parity_equivalent_check"

    def apply(self, circuit: AC0Circuit) -> AC0Circuit:
        import itertools
        n = circuit.n_inputs
        for bits in itertools.product([False, True], repeat=n):
            parity_val = sum(bits) % 2 == 1
            if circuit.evaluate(bits) != parity_val:
                # Not PARITY-equivalent: collapse to constant 0
                const_gate = Gate(GateType.AND, list(range(n)), negated=True)
                return AC0Circuit(n, 1, [const_gate])
        # PARITY-equivalent: return unchanged
        return circuit

    def affects_parity(self, n: int) -> bool:
        # PARITY itself is PARITY-equivalent, so it passes unchanged
        return False


# Registry of all transforms for L2 to search over
TRANSFORM_REGISTRY = [
    RandomRestriction(survival_prob=0.5),
    RandomRestriction(survival_prob=0.3),
    RandomRestriction(survival_prob=0.7),
    GateSubstitution(GateType.AND, GateType.OR),
    GateSubstitution(GateType.OR, GateType.AND),
    InputPermutation(),
    DepthReduction(),
    ExhaustiveParityEquivalentCheck(),  # adversarial pressure-test: reaches L3, tests "exponential ≠ safe" blind spot
]
