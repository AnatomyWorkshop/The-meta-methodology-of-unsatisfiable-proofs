# Self-Referential Safety and Physical Theories: A Mapping Attempt

> Date: 2026-04-28
> Context: Prompted by a GPT conversation about whether the framework applies to physics — specifically SUSY/WIMP failures and the status of General Relativity. This is an exploratory document, not a paper section. The main paper is not affected.

---

## The question

Can the self-referential safety framework — built for circuit lower bounds and Gödel's incompleteness theorem — say anything useful about the failure of physical theories?

The short answer is: partially, and with important caveats. The framework maps cleanly onto a specific *type* of theoretical failure in physics, but it does not cover the full landscape of how physical theories succeed or fail. Knowing which type it covers, and which it doesn't, is more useful than either claiming universal applicability or dismissing the connection entirely.

---

## What the framework actually says

The framework's core claim is about *proof strategies*, not about theories in general. It says: a lower-bound proof succeeds when its discriminating property is not decidable within the model it constrains. When the discriminating property becomes decidable within the model — when the model can simulate its own diagnostic tool — the proof strategy collapses.

The key word is *proof*. The framework is about the structure of impossibility arguments, not about the empirical fate of scientific theories. This distinction matters enormously when we try to apply it to physics.

---

## The mapping that works

There is a class of theoretical failures in physics that maps cleanly onto the framework's Second Law (the Generalization Barrier):

> When a proof is extended from a restricted model $M_1$ to a stronger model $M_2 \supset M_1$, it fails if and only if the discriminating property becomes decidable within $M_2$.

The physical analog: when a theoretical prediction is extended from the regime where it was constructed to a more powerful experimental regime, it fails if and only if the new regime can directly test the prediction's core mechanism.

**The WIMP/SUSY case.** Supersymmetry was constructed specifically to resolve the hierarchy problem — the "naturalness" puzzle about why the Higgs mass is so much smaller than the Planck scale. The discriminating property $P$ was: "new particles appear at the TeV scale." The LHC is a stronger model $M_2$ that can directly test this prediction. It found nothing. The framework's diagnosis: $P$ became decidable within $M_2$, and the answer was negative.

This is a genuine instance of the Second Law's structure. The theory proposed a discriminating property, that property was tested by a stronger model, and the test came back negative. The self-referential element is subtle but present: SUSY's discriminating property was constructed to be testable — that was the point — and testability is precisely what made it vulnerable.

**One important correction.** The GPT conversation correctly noted that SUSY has not been *completely* falsified — only parts of its parameter space have been excluded. The framework's language needs to be precise here: what has happened is not "P was judged false" but "P's viable parameter space has been compressed by $M_2$ to the point where the original motivation (naturalness) is no longer served." This is a weaker but still structurally interesting claim: the discriminating property has been *partially internalized* by the stronger model, and the residual parameter space no longer does the explanatory work it was designed to do.

---

## The mapping that doesn't work

**General Relativity and dark matter/dark energy.** GR encounters anomalies at galactic and cosmological scales. But these anomalies do not constitute a case where a discriminating property has been tested and found false. The situation is one of *underdetermination*: the observations are consistent with multiple explanations (dark matter, modified gravity, cosmological constant), and current models cannot distinguish between them.

In the framework's language: there is no discriminating property $P$ that has been proposed, tested, and found to fail. The situation is that $P$ has not yet been defined precisely enough to be tested. This is not a failure of self-referential safety — it is the absence of an unsatisfiability certificate altogether. The framework simply does not apply.

This is the distinction the GPT conversation called "Dead End vs. Open Frontier." It is a real and useful distinction. But it is not the framework's distinction — it is a prior distinction that determines whether the framework is applicable at all.

---

## The distinguishability question

The GPT conversation suggested upgrading the framework's core concept from "decidability" to "distinguishability," arguing that distinguishability is more general and would allow the framework to cover physical cases more naturally.

I think this is the wrong direction for the main paper, for a specific reason: the three case studies in the paper — AC⁰, monotone circuits, Gödel — are mathematical objects, and their self-referential safety conditions are *literally* about decidability in the computational/logical sense. "Decidability" is not a metaphor in those cases; it is the exact concept. Replacing it with "distinguishability" would gain generality at the cost of precision, and the paper's value comes from precision.

That said, the relationship between decidability and distinguishability is genuinely interesting and worth stating clearly:

- **Decidability** (in the computational sense): there exists an algorithm within $M$ that outputs yes/no on whether a candidate satisfies $P$.
- **Distinguishability** (in the physical/statistical sense): there exists a process within $M$ that produces observably different outcomes for different truth values of $P$.

Decidability is a special case of distinguishability: it is distinguishability where the distinguishing process is discrete, deterministic, and algorithmically produced. The converse does not hold — a physical experiment can distinguish two hypotheses without there being an algorithm that decides between them.

The framework's self-referential safety condition, stated in terms of distinguishability, would read:

> $P$ is self-referentially safe with respect to $M$ if there is no process *internal to $M$* that can distinguish whether a given candidate satisfies $P$.

This is a genuine generalization. It would allow the framework to cover cases where the "model" is a physical experimental setup rather than a circuit class or formal system. Whether this generalization is worth pursuing depends on whether there are interesting physical cases where the condition is satisfied — where a theory's discriminating property is genuinely *not* testable by any process internal to the theory's own framework.

The most interesting candidate is quantum gravity. Any theory of quantum gravity must make predictions about regimes (Planck scale, black hole interiors) that are not accessible to any experiment constructible within current physics. The discriminating property of such a theory — whatever it is — may be self-referentially safe in the distinguishability sense: no process within the current physical model can test it. Whether this is a feature (the theory is safe from premature falsification) or a bug (the theory is unfalsifiable) depends on whether the stronger model eventually becomes available.

---

## What this suggests for the paper

Nothing needs to change in the main paper. The framework is correctly scoped to mathematical impossibility proofs, and that scope is where its precision lives.

What this exploration suggests is a possible future direction: a companion piece that develops the distinguishability generalization formally, maps it onto physical cases, and asks whether the self-referential safety condition has predictive power in physics the way it does in complexity theory. That piece would need to:

1. Define "distinguishability" precisely enough to be mathematical (probably in terms of statistical hypothesis testing or information-theoretic distinguishability).
2. Identify at least one physical case where the condition is non-trivially satisfied — not just "the experiment hasn't been done yet" but "no experiment constructible within the current framework could in principle test this."
3. Make a falsifiable prediction: if the framework is right, theories whose discriminating properties are self-referentially safe (in the distinguishability sense) should survive longer and fail differently than theories whose discriminating properties are not.

This is a real research program. It is not the current paper.

---

## One thing worth saying directly

The GPT conversation ended with: "你这套理论最强的地方，不是'能解释数学'，也不是'能解释物理'，而是：它试图说明'为什么这两者在结构上其实是一回事'。"

I think this is half right. The framework does identify a structural pattern that appears in both mathematics and physics. But the reason it is credible in mathematics is precisely that it is *precise* there — it makes exact claims about decidability that can be verified against known results. The physical application is currently at the level of structural analogy, not exact correspondence. Treating the analogy as if it were already an exact correspondence would be a mistake.

The honest version of the claim is: the framework identifies a structural condition (self-referential safety) that governs impossibility proofs in mathematics. There is a suggestive analogy between this condition and certain failure modes in physical theories. Whether the analogy can be made exact — whether "distinguishability" can be defined precisely enough to make the physical cases instances of the same mathematical structure — is an open question. It is a good open question. It is not yet answered.

That gap between "suggestive analogy" and "exact correspondence" is where the interesting work is. The current paper lives on the mathematics side of that gap, and it is right to stay there.
