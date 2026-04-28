# Chapter 3: Case Study I — AC⁰ Circuit Lower Bounds

> Status: First draft (translated from Chinese)
> Framework components: Structured constraints / Search space / Hidden trap / Best approximation

---

## 3.1 Opening Proposition

Håstad's Switching Lemma proof can be read as a paradigm case of an unsatisfiability proof. It constructs no algorithm, finds no counterexample. Instead, it demonstrates that within a restricted computational model, the ability to compute a target function perfectly is permanently foreclosed by a strictly positive error rate lower bound.

This is the first concrete instance of the paper's framework.

---

## 3.2 Background: AC⁰ Circuits and the Parity Function

**Definition (AC⁰ circuits).** AC⁰ is the class of Boolean circuit families of constant depth $d$ with unbounded fan-in AND/OR gates, where the circuit size (number of gates) is polynomial in the input length $n$.

**Target function.** The parity function $\mathrm{PARITY}_n$, defined as the XOR of $n$ input bits: the output is 1 if and only if the number of 1s among the inputs is odd.

**Known result (Håstad, 1986).** No polynomial-size AC⁰ circuit family can compute $\mathrm{PARITY}_n$. More precisely, any AC⁰ circuit of depth $d$ and size $s$ computing $\mathrm{PARITY}_n$ has error rate at least

$$\mathrm{Err} \geq \frac{1}{2} - \frac{1}{2} \cdot \exp\!\left(-\Omega\!\left(\frac{\log s}{d-1}\right)^{1/(d-1)}\right).$$

When $s = \mathrm{poly}(n)$ and $d$ is a fixed constant, the right-hand side approaches $\frac{1}{2}$ — the circuit's performance degrades to random guessing.

---

## 3.3 The Four-Step Framework Applied

### Step 1: Structured Constraint Set $C$

The constraint set consists of three rules:

- **C1 (Depth constraint).** Circuit depth does not exceed a fixed constant $d$.
- **C2 (Gate type constraint).** Only unbounded fan-in AND and OR gates are permitted; NOT gates appear only at the input layer (or equivalently, are absent).
- **C3 (Size constraint).** The number of gates does not exceed $\mathrm{poly}(n)$.

These three constraints together define the AC⁰ constraint, which determines the boundary of the search space.

### Step 2: Search Space $S$

$$S = \{ C = \{C_n\}_{n=1}^\infty \mid C_n \text{ satisfies constraints C1, C2, C3} \}.$$

This is the set of all AC⁰ circuit families. We search within this space for a candidate that computes $\mathrm{PARITY}$ perfectly.

**Objective function.** Define the global error rate of a circuit family $C$ as

$$\mathrm{Err}(C) = \limsup_{n \to \infty} \Pr_{x \in \{0,1\}^n}\!\left[C_n(x) \neq \mathrm{PARITY}_n(x)\right].$$

The optimization problem: minimize $\mathrm{Err}(C)$ over $S$. If the optimum is 0, then $\mathrm{PARITY} \in \mathrm{AC}^0$; if the optimum is strictly positive, unsatisfiability is established.

### Step 3: The Hidden Trap $T$

The trap lies in the conflict between constraint C1 (depth) and the intrinsic complexity of $\mathrm{PARITY}$.

**Intuition.** The parity function is maximally sensitive to every input bit: flipping any single input bit always flips the output. This global sensitivity requires the circuit to "see" the relationship among all inputs simultaneously. A circuit of depth $d$ can only "see" information within $d$ layers from the output gate; under size constraints, it cannot capture the global parity relationship across all inputs.

**Formal trap (the core of the Switching Lemma).** Apply a *random restriction* $\rho$ to an AC⁰ circuit: randomly select a $(1-p)$ fraction of the $n$ input variables and fix them to random values, leaving the remaining $pn$ variables free.

- **Circuit behavior under random restriction.** Håstad's Switching Lemma shows that under a random restriction $\rho$, a depth-$d$, size-$s$ AC⁰ circuit collapses with high probability ($1 - \exp(-\Omega(n))$) to a circuit of depth at most $d-1$, and ultimately to a shallow decision tree.

- **$\mathrm{PARITY}$ behavior under random restriction.** Under any random restriction, $\mathrm{PARITY}$ remains equal to the parity of the surviving free variables — its complexity does not decrease.

This is the trap: **the circuit collapses under random restriction, but the target function does not.** This asymmetry is the hidden conflict within the constraint set.

### Step 4: Best Approximation $A^*$

By induction on depth $d$ over the random restriction process, one can show:

For any circuit family $C$ satisfying the AC⁰ constraints, there exists an absolute positive constant $\epsilon > 0$ (depending on $d$) such that

$$\mathrm{Err}(C) \geq \epsilon.$$

Specifically, when depth $d$ is fixed and size $s = \mathrm{poly}(n)$, the error rate lower bound approaches $\frac{1}{2}$ — the circuit degrades to random guessing.

**Conclusion.** Under the AC⁰ constraints, the optimization goal of driving $\mathrm{PARITY}$'s error rate to zero is **unsatisfiable**. The best approximation satisfies $A^* \geq \epsilon > 0$, and this bound is tight (there exist circuit families whose error rate approaches $\frac{1}{2}$).

---

## 3.4 Self-Referential Safety Analysis

Why does this proof succeed? The key lies in the choice of discriminating property $P$.

**Discriminating property $P$.** Circuit $C_n$ collapses with high probability to a decision tree of depth less than $d$ under a random restriction $\rho$.

**Self-referential safety.** Deciding property $P$ requires computing the expected collapse behavior of a circuit over exponentially many random restrictions — specifically, estimating the probability that a random $\rho$ reduces the circuit to a decision tree of depth $< d$. This expectation ranges over $\binom{n}{\lfloor pn \rfloor} \cdot 2^{(1-p)n}$ possible restrictions, a quantity that grows faster than any polynomial in $n$. No AC⁰ circuit can perform this computation: the required resources are at least quasi-polynomial, far exceeding the polynomial-size constraint C3. Therefore, **no AC⁰ circuit can decide "whether a given circuit satisfies property $P$."**

Property $P$ is self-referentially safe with respect to the AC⁰ model. The proof tool (random restriction analysis) does not fall within the constrained class (AC⁰), and therefore does not trigger the self-referential trap.

This is precisely the core structure that Chapter 6 will distill: *every successful lower-bound proof uses a discriminating property that is self-referentially safe.*

---

## 3.5 Summary

| Framework component | AC⁰ case |
|---|---|
| Structured constraint set $C$ | Constant depth + unbounded fan-in AND/OR + polynomial size |
| Search space $S$ | All AC⁰ circuit families |
| Hidden trap $T$ | Circuit collapses under random restriction; PARITY does not |
| Best approximation $A^*$ | Error rate $\geq \epsilon > 0$, approaching $1/2$ |
| Discriminating property $P$ | Collapse behavior under random restriction |
| Self-referentially safe? | Yes — deciding $P$ exceeds AC⁰ capability |

This case establishes the first concrete instance of the framework. The next chapter turns to the monotone circuit lower bound, where the hidden trap takes a different form but the logic of self-referential safety is identical — until we attempt to generalize the proof to unrestricted circuits, at which point the self-referential trap detonates.

---

## Notes and References

- Complete proof of Håstad's Switching Lemma: Håstad (1986), doctoral dissertation; or Arora & Barak, *Computational Complexity*, Chapter 14, Theorem 14.20.
- The error rate lower bound formula in §3.2 follows Arora & Barak, Corollary 14.25.
- An earlier version of the random restriction method: Furst, Saxe & Sipser (1984), who first proved $\mathrm{PARITY} \notin \mathrm{AC}^0$, with a weaker bound than Håstad's.
