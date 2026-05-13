"""
L2 transformation rule library for algebraic circuits over GF(p).

Each transform operates on algebraic circuits and/or evaluation context.
The key insight: in the algebraic setting, the discriminating property is
about polynomial degree and coefficient structure.

Transforms are analogous to Phase 1/3 but adapted for the algebraic domain:
  - AlgebraicRestriction ≈ RandomRestriction (Phase 1) / DistributionSwitch (Phase 3)
  - DegreeTruncation: zero out high-degree monomials
  - MonomialElimination: zero out specific variable interactions
  - FieldReduction: evaluate over a smaller subfield
"""

import random
from typing import Tuple, List
from l1_algebraic import AlgebraicCircuit, AlgGate, AlgGateType


class AlgebraicTransform:
    """Base class for algebraic circuit transformations."""
    name: str = "base"

    def apply(self, circuit: AlgebraicCircuit):
        raise NotImplementedError

    def affects_permanent(self, n: int, p: int) -> bool:
        """True if this transform also degrades the Permanent function itself."""
        raise NotImplementedError

    def __repr__(self):
        return f"AlgebraicTransform({self.name})"


# ---------------------------------------------------------------------------
# Key transform: AlgebraicRestriction
# Analog of RandomRestriction (Phase 1) and DistributionSwitch (Phase 3).
# Sets a random subset of input variables to random constants.
# This is the algebraic analog of Razborov-Smolensky's method.
# ---------------------------------------------------------------------------

class AlgebraicRestriction(AlgebraicTransform):
    """
    Randomly fix a fraction of input variables to constants in GF(p).
    Analog of random restriction in the Boolean setting.

    For Permanent: fixing variables reduces the matrix size but preserves
    the Permanent structure. A circuit that cannot handle restricted inputs
    has lost its ability to compute Permanent.

    This is the algebraic analog of the Razborov-Smolensky method:
    random restrictions reduce algebraic circuits to low-degree polynomials,
    which cannot compute Permanent (high algebraic degree).
    """
    name = "algebraic_restriction"

    def __init__(self, restriction_prob: float = 0.3):
        self.restriction_prob = restriction_prob
        self.name = f"algebraic_restriction_p{restriction_prob}"

    def apply(self, circuit: AlgebraicCircuit):
        return RestrictedAlgebraicCircuit(circuit, self.restriction_prob)

    def affects_permanent(self, n: int, p: int) -> bool:
        # High restriction probability destroys too many variables
        return self.restriction_prob > 0.6


class RestrictedAlgebraicCircuit:
    """Wrapper that randomly fixes some input variables to constants."""

    def __init__(self, original: AlgebraicCircuit, restriction_prob: float):
        self.original = original
        self.restriction_prob = restriction_prob
        self.n = original.n
        self.p = original.p
        self.n_inputs = original.n_inputs
        self.depth = original.depth
        # Fix a random subset of variables
        self._fixed = {
            i: random.randrange(1, original.p)
            for i in range(original.n_inputs)
            if random.random() < restriction_prob
        }

    @property
    def size(self):
        return self.original.size

    def evaluate(self, x: Tuple[int, ...]) -> int:
        modified = list(x)
        for i, val in self._fixed.items():
            if i < len(modified):
                modified[i] = val
        return self.original.evaluate(tuple(modified))


# ---------------------------------------------------------------------------
# DegreeTruncation: zero out high-degree contributions
# Approximates the effect of degree-reduction in algebraic proofs.
# ---------------------------------------------------------------------------

class DegreeTruncation(AlgebraicTransform):
    """
    Truncate the circuit by zeroing out MUL gates beyond a depth threshold.
    Simulates restricting to low-degree polynomials.

    Permanent has degree n (each term is a product of n variables).
    Truncating to degree < n should destroy Permanent computation.
    This is the algebraic analog of the degree lower bound method.
    """
    name = "degree_truncation"

    def __init__(self, max_mul_depth: int = 1):
        self.max_mul_depth = max_mul_depth
        self.name = f"degree_truncation_d{max_mul_depth}"

    def apply(self, circuit: AlgebraicCircuit):
        return DegreeTruncatedCircuit(circuit, self.max_mul_depth)

    def affects_permanent(self, n: int, p: int) -> bool:
        # Truncating to degree < n always affects Permanent (degree n)
        return self.max_mul_depth < n - 1


class DegreeTruncatedCircuit:
    """Wrapper that zeros out MUL gates beyond a depth threshold."""

    def __init__(self, original: AlgebraicCircuit, max_mul_depth: int):
        self.original = original
        self.max_mul_depth = max_mul_depth
        self.n = original.n
        self.p = original.p
        self.n_inputs = original.n_inputs
        self.depth = original.depth
        # Identify which gate indices are MUL gates beyond threshold
        mul_count = 0
        self._zeroed = set()
        for i, gate in enumerate(original.gates):
            if gate.gate_type == AlgGateType.MUL:
                mul_count += 1
                if mul_count > max_mul_depth:
                    self._zeroed.add(original.n_inputs + i)

    @property
    def size(self):
        return self.original.size

    def evaluate(self, x: Tuple[int, ...]) -> int:
        values = list(x) + [0] * len(self.original.gates)
        for i, gate in enumerate(self.original.gates):
            idx = self.original.n_inputs + i
            if idx in self._zeroed:
                values[idx] = 0
            else:
                values[idx] = gate.evaluate(values, self.original.p)
        return values[-1] if self.original.gates else 0


# ---------------------------------------------------------------------------
# MonomialElimination: zero out specific variable interactions
# Targets cross-row interactions that Permanent requires.
# ---------------------------------------------------------------------------

class MonomialElimination(AlgebraicTransform):
    """
    Zero out inputs corresponding to a random subset of matrix rows.
    Eliminates the row-column interactions that Permanent depends on.

    Permanent requires all n rows to contribute. Eliminating even one row
    makes the circuit unable to compute the full Permanent.
    This is analogous to the "projection" idea in monotone circuit lower bounds.
    """
    name = "monomial_elimination"

    def __init__(self, row_survival_prob: float = 0.7):
        self.row_survival_prob = row_survival_prob
        self.name = f"monomial_elimination_p{row_survival_prob}"

    def apply(self, circuit: AlgebraicCircuit):
        return MonomialEliminatedCircuit(circuit, self.row_survival_prob)

    def affects_permanent(self, n: int, p: int) -> bool:
        expected_rows = n * self.row_survival_prob
        return expected_rows < n - 0.5  # loses at least one row on average


class MonomialEliminatedCircuit:
    """Wrapper that zeros out inputs for non-surviving rows."""

    def __init__(self, original: AlgebraicCircuit, row_survival_prob: float):
        self.original = original
        self.row_survival_prob = row_survival_prob
        self.n = original.n
        self.p = original.p
        self.n_inputs = original.n_inputs
        self.depth = original.depth
        self._surviving_rows = {
            i for i in range(original.n)
            if random.random() < row_survival_prob
        }

    @property
    def size(self):
        return self.original.size

    def evaluate(self, x: Tuple[int, ...]) -> int:
        modified = list(x)
        n = self.n
        for i in range(n):
            if i not in self._surviving_rows:
                for j in range(n):
                    modified[i * n + j] = 0
        return self.original.evaluate(tuple(modified))


# ---------------------------------------------------------------------------
# FieldReduction: evaluate over a smaller subfield
# ---------------------------------------------------------------------------

class FieldReduction(AlgebraicTransform):
    """
    Reduce inputs modulo a smaller prime q < p.
    Simulates working in a subfield.

    Control transform: field reduction is a local operation (apply mod q to each input),
    so it should be decidable in algebraic P/poly — expected UNSAFE.
    """
    name = "field_reduction"

    def __init__(self, q: int = 2):
        self.q = q
        self.name = f"field_reduction_q{q}"

    def apply(self, circuit: AlgebraicCircuit):
        return FieldReducedCircuit(circuit, self.q)

    def affects_permanent(self, n: int, p: int) -> bool:
        return False  # Permanent mod q is still Permanent; structure preserved


class FieldReducedCircuit:
    """Wrapper that reduces inputs modulo q before evaluation."""

    def __init__(self, original: AlgebraicCircuit, q: int):
        self.original = original
        self.q = q
        self.n = original.n
        self.p = original.p
        self.n_inputs = original.n_inputs
        self.depth = original.depth

    @property
    def size(self):
        return self.original.size

    def evaluate(self, x: Tuple[int, ...]) -> int:
        modified = tuple(v % self.q for v in x)
        return self.original.evaluate(modified)


# ---------------------------------------------------------------------------
# Control transforms
# ---------------------------------------------------------------------------

class IdentityTransform(AlgebraicTransform):
    """Control: return circuit unchanged."""
    name = "identity"

    def apply(self, circuit):
        return circuit

    def affects_permanent(self, n, p):
        return False


class InputPermutation(AlgebraicTransform):
    """
    Control: permute the row indices of the input matrix.
    Permanent is invariant under row permutation (up to sign for Determinant).
    """
    name = "input_permutation"

    def apply(self, circuit: AlgebraicCircuit):
        return PermutedInputCircuit(circuit)

    def affects_permanent(self, n, p):
        return False


class PermutedInputCircuit:
    """Wrapper that permutes matrix rows before evaluation."""

    def __init__(self, original: AlgebraicCircuit):
        self.original = original
        self.n = original.n
        self.p = original.p
        self.n_inputs = original.n_inputs
        self.depth = original.depth
        self._perm = list(range(original.n))
        random.shuffle(self._perm)

    @property
    def size(self):
        return self.original.size

    def evaluate(self, x: Tuple[int, ...]) -> int:
        n = self.n
        modified = [0] * (n * n)
        for i in range(n):
            for j in range(n):
                modified[self._perm[i] * n + j] = x[i * n + j]
        return self.original.evaluate(tuple(modified))


class ScalarMultiplication(AlgebraicTransform):
    """
    Control: multiply all inputs by a random nonzero scalar.
    Permanent scales by scalar^n; circuit output scales accordingly.
    Expected: low delta (circuit behavior preserved up to scaling).
    """
    name = "scalar_multiplication"

    def apply(self, circuit: AlgebraicCircuit):
        return ScaledCircuit(circuit)

    def affects_permanent(self, n, p):
        return False


class ScaledCircuit:
    """Wrapper that scales all inputs by a random nonzero scalar."""

    def __init__(self, original: AlgebraicCircuit):
        self.original = original
        self.n = original.n
        self.p = original.p
        self.n_inputs = original.n_inputs
        self.depth = original.depth
        self._scalar = random.randrange(1, original.p)

    @property
    def size(self):
        return self.original.size

    def evaluate(self, x: Tuple[int, ...]) -> int:
        modified = tuple((v * self._scalar) % self.p for v in x)
        return self.original.evaluate(modified)


# ---------------------------------------------------------------------------
# Transform registry
# ---------------------------------------------------------------------------

ALGEBRAIC_TRANSFORM_REGISTRY = [
    AlgebraicRestriction(restriction_prob=0.3),
    AlgebraicRestriction(restriction_prob=0.5),
    AlgebraicRestriction(restriction_prob=0.7),
    DegreeTruncation(max_mul_depth=1),
    DegreeTruncation(max_mul_depth=2),
    MonomialElimination(row_survival_prob=0.7),
    MonomialElimination(row_survival_prob=0.5),
    FieldReduction(q=2),
    IdentityTransform(),
    InputPermutation(),
    ScalarMultiplication(),
]
