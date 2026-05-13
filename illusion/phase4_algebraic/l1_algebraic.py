"""
L1: Algebraic circuit simulator over GF(p).

Algebraic circuits use addition (+) and multiplication (*) gates over a
finite field GF(p). They compute multivariate polynomials.

Target functions:
  - Permanent(M): sum over all permutations σ of product M[i][σ(i)]
    Known: requires exponential-size algebraic circuits (Valiant 1979).
  - Determinant(M): sum over all permutations σ of sgn(σ) * product M[i][σ(i)]
    Known: computable by polynomial-size algebraic circuits.

Input encoding: n×n matrix flattened to n² field elements.
"""

import itertools
import random
from enum import Enum
from typing import List, Tuple


# Default prime field
DEFAULT_P = 7


class AlgGateType(Enum):
    ADD = "ADD"
    MUL = "MUL"
    CONST = "CONST"   # constant gate (leaf)
    INPUT = "INPUT"   # input variable (leaf)


class AlgGate:
    __slots__ = ("gate_type", "inputs", "const_val")

    def __init__(self, gate_type: AlgGateType, inputs: List[int], const_val: int = 0):
        self.gate_type = gate_type
        self.inputs = inputs
        self.const_val = const_val

    def evaluate(self, values: List[int], p: int) -> int:
        if self.gate_type == AlgGateType.INPUT:
            return values[self.inputs[0]] % p
        if self.gate_type == AlgGateType.CONST:
            return self.const_val % p
        if self.gate_type == AlgGateType.ADD:
            return sum(values[i] for i in self.inputs) % p
        if self.gate_type == AlgGateType.MUL:
            result = 1
            for i in self.inputs:
                result = (result * values[i]) % p
            return result
        raise ValueError(f"Unknown gate type: {self.gate_type}")


class AlgebraicCircuit:
    """
    An algebraic circuit over GF(p): ADD/MUL gates.
    Computes a polynomial in n² variables (entries of an n×n matrix).
    """

    def __init__(self, n: int, p: int, gates: List[AlgGate]):
        self.n = n           # matrix dimension
        self.p = p           # field characteristic
        self.n_inputs = n * n
        self.gates = gates

    @property
    def size(self) -> int:
        return len(self.gates)

    @property
    def depth(self) -> int:
        # Approximate depth: number of MUL layers
        return sum(1 for g in self.gates if g.gate_type == AlgGateType.MUL)

    def evaluate(self, x: Tuple[int, ...]) -> int:
        """Evaluate circuit on input x (flattened n×n matrix over GF(p))."""
        values = list(x) + [0] * len(self.gates)
        for i, gate in enumerate(self.gates):
            values[self.n_inputs + i] = gate.evaluate(values, self.p)
        return values[-1] if self.gates else 0


# ---------------------------------------------------------------------------
# Target functions
# ---------------------------------------------------------------------------

def permanent(matrix: List[List[int]], p: int) -> int:
    """Compute Permanent(M) mod p."""
    n = len(matrix)
    result = 0
    for perm in itertools.permutations(range(n)):
        term = 1
        for i, j in enumerate(perm):
            term = (term * matrix[i][j]) % p
        result = (result + term) % p
    return result


def determinant(matrix: List[List[int]], p: int) -> int:
    """Compute Determinant(M) mod p using permutation expansion."""
    n = len(matrix)
    result = 0
    for perm in itertools.permutations(range(n)):
        # Compute sign of permutation
        sign = _perm_sign(perm)
        term = sign
        for i, j in enumerate(perm):
            term = (term * matrix[i][j]) % p
        result = (result + term) % p
    return result


def _perm_sign(perm: Tuple[int, ...]) -> int:
    """Return +1 or -1 (as integer) for the sign of a permutation."""
    n = len(perm)
    visited = [False] * n
    sign = 1
    for i in range(n):
        if not visited[i]:
            j = i
            cycle_len = 0
            while not visited[j]:
                visited[j] = True
                j = perm[j]
                cycle_len += 1
            if cycle_len % 2 == 0:
                sign *= -1
    return sign


def matrix_from_flat(x: Tuple[int, ...], n: int) -> List[List[int]]:
    """Reconstruct n×n matrix from flattened input."""
    return [[x[i * n + j] for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------------------
# Random circuit generator
# ---------------------------------------------------------------------------

def permanent_circuit(n: int, p: int) -> AlgebraicCircuit:
    """
    Build an explicit algebraic circuit that computes Permanent(M) mod p.

    For each permutation σ, create a MUL gate computing product M[i][σ(i)].
    Then ADD all permutation products.

    This is the canonical exponential-size circuit for Permanent.
    Size = n! MUL gates + 1 ADD gate.
    """
    n_inputs = n * n
    gates = []

    # One MUL gate per permutation
    perm_gate_indices = []
    for perm in itertools.permutations(range(n)):
        # Inputs: M[0][perm[0]], M[1][perm[1]], ..., M[n-1][perm[n-1]]
        inputs = [i * n + perm[i] for i in range(n)]
        gates.append(AlgGate(AlgGateType.MUL, inputs))
        perm_gate_indices.append(n_inputs + len(gates) - 1)

    # Final ADD gate: sum all permutation products
    gates.append(AlgGate(AlgGateType.ADD, perm_gate_indices))

    return AlgebraicCircuit(n, p, gates)


def partial_permanent_circuit(n: int, p: int, n_perms: int = None) -> AlgebraicCircuit:
    """
    Build a circuit computing a random subset of Permanent terms.
    Approximates Permanent but with fewer gates.

    If n_perms is None, uses n! // 2 permutations (half the terms).
    This circuit is "almost Permanent" — it can distinguish D+ from D-
    but is weaker than the full Permanent circuit.
    """
    import math
    all_perms = list(itertools.permutations(range(n)))
    if n_perms is None:
        n_perms = max(1, len(all_perms) // 2)
    selected = random.sample(all_perms, min(n_perms, len(all_perms)))

    n_inputs = n * n
    gates = []
    perm_gate_indices = []

    for perm in selected:
        inputs = [i * n + perm[i] for i in range(n)]
        gates.append(AlgGate(AlgGateType.MUL, inputs))
        perm_gate_indices.append(n_inputs + len(gates) - 1)

    gates.append(AlgGate(AlgGateType.ADD, perm_gate_indices))
    return AlgebraicCircuit(n, p, gates)


def random_algebraic_circuit(
    n: int,
    p: int,
    depth: int = 3,
    fan_in: int = 2,
) -> AlgebraicCircuit:
    """
    Generate a random algebraic circuit over GF(p) for n×n matrix inputs.
    Alternates ADD/MUL layers. Approximates a random polynomial computation.
    """
    n_inputs = n * n
    gates = []
    prev_layer = list(range(n_inputs))

    for d in range(depth):
        gate_type = AlgGateType.MUL if d % 2 == 0 else AlgGateType.ADD
        layer_size = max(2, n_inputs // (d + 1))
        current_layer = []

        for _ in range(layer_size):
            actual_fan_in = min(fan_in, len(prev_layer))
            inputs = random.sample(prev_layer, actual_fan_in)
            gates.append(AlgGate(gate_type, inputs))
            current_layer.append(n_inputs + len(gates) - 1)

        prev_layer = current_layer

    # Output gate: ADD over last layer
    output_gate = AlgGate(AlgGateType.ADD, prev_layer)
    gates.append(output_gate)

    return AlgebraicCircuit(n, p, gates)
