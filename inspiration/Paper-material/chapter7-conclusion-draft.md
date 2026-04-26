# Chapter 7 Draft: Conclusion

> Status: First draft
> Role: Restate contribution, acknowledge limitations, point to open problems.
> Design principle: Short (2–3 pages). No new arguments. The reader has already seen the evidence.

---

## 7.1 What the Framework Achieves

This paper has proposed a four-component framework — computational model, target function, discriminating property, self-referential safety — for analyzing impossibility proofs. The framework was tested against three case studies spanning circuit complexity and mathematical logic:

- The AC⁰ lower bound (Håstad, 1986), where the discriminating property is collapse under random restriction.
- The monotone circuit lower bound (Razborov, 1985), where the discriminating property is the inability to distinguish true cliques from pseudo-clique structures.
- Gödel's first incompleteness theorem (1931), where the discriminating property is the self-referential Gödel sentence.

In each case, the proof succeeds because the discriminating property is self-referentially safe — not decidable within the model it constrains. The unified analysis (Chapter 6) verified this pattern across all three cases, formalized three known barriers (relativization, natural proofs, algebrization) as instances of self-referential unsafety, and distilled three structural laws governing the provability of lower bounds. The Third Law (Meta-Methodological Constraint) closes the framework self-reflexively: any meta-methodology that diagnoses lower-bound proofs must itself employ a diagnostic criterion not decidable within the proof class it analyzes — including this one. The framework is a conceptual map, not a proof algorithm, and this limitation is principled rather than accidental.

The framework's contribution is not a new theorem but a new lens: a structured language for asking why impossibility proofs work, why they fail to generalize, and what conditions any future breakthrough must satisfy. The framework's implications for P vs. NP are deferred to future work.

---

## 7.2 Limitations

Three limitations should be stated plainly.

**The framework is diagnostic, not generative.** It can re-express known lower bounds and diagnose known failures, but it cannot produce new lower bounds. The three laws describe the structure of successful proofs; they do not prescribe how to construct one.

**The self-referential safety condition is semi-formal.** Definition 2.4 (equivalently, Definition 6.4) is precise enough to verify against concrete cases, but it is not yet a fully axiomatized mathematical object. In particular, the same definition operates differently on extensional objects (circuit families) and intensional objects (formal systems). This tension is addressed in §6.4 but not resolved.

**The case studies are retrospective.** All three impossibility results analyzed in this paper were already known. The framework's predictive power — its ability to identify which proof strategies will fail before they are attempted — is supported by the barrier analysis (§6.5) and the falsifiable predictions (§6.5.2), but has not yet been tested against a genuinely novel proof attempt.

---

## 7.3 Open Problems

The open problems identified in §6.7 fall into three categories:

**Formalization.** Can the self-referential safety condition be given a fully formal, domain-independent definition that subsumes both the circuit-complexity and logic instances? Can the SRS Index (§6.7.3) be made into a rigorous quantitative measure, or does the safety spectrum (§6.7.4) necessarily remain a qualitative hierarchy?

**Scope.** Are there successful lower-bound proofs whose discriminating properties are *not* self-referentially safe? The false-negative audit (§6.5.3) found none among known cases, but the question of necessity remains open (§6.7.5).

**Application.** The logic–computation correspondence table (§6.4.1) contains predicted entries — structural analogs that have been identified in one domain but not yet verified in the other. Each blank or predicted cell is a concrete research question. In particular, the connection between reflection principles in logic and hardness assumptions in complexity theory (§6.4.1, Remark) may point toward a deeper structural bridge between the two fields.

---

## 7.4 Closing

Impossibility proofs are often seen as negative results — statements about what cannot be done. This paper has argued that they have a positive structure: they are certificates, issued by discriminating properties that escape the reach of the models they constrain. The self-referential safety condition is the structural invariant that makes these certificates possible.

The framework does not tell us how to build new proofs. It tells us what shape they must take. In a field where the most important open problems have resisted all known proof techniques, knowing the shape of the answer may be the most useful thing a meta-theory can provide.
