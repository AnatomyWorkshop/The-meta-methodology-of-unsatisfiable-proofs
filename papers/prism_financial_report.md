# Prism Financial Application: Experimental Report

## Summary

This report documents a systematic experimental campaign testing Prism's
duality defect (δ = ||[L,P]||_F / ||L||_F) as a financial market tool.
The conclusion is negative: Prism does not produce actionable financial
signals in dense correlation networks. The theoretical contribution
(structural health metric derived from first principles) stands, but the
financial product direction is closed.

---

## Experiments Conducted

### 1. Historical Backtest (2011-2020)

**Method:** Rolling 60-day defect on 30-stock S&P sector basket.

**Finding:** 2017 chronic fragility — 14 months of δ > 0.78 while VIX
remained at 12. Ended in Feb 2018 Volmageddon.

**Assessment:** Real finding. Single compelling historical episode.
Not reproducible as a systematic signal.

---

### 2. Compression Signal Detection

**Hypothesis (from Deepseek3):** Defect drop from high plateau predicts
volatility release.

**Result:** Tested two versions with different parameters. Lift = 0.98x.
0/4 stress events followed by release within the detection window.

**Root cause:** Compression and release are simultaneous (same event
measured differently), not sequential.

**Verdict:** Dead.

---

### 3. Yield Curve Deep Dive (2006-2023)

**Hypothesis:** Low defect on treasury ETFs = extreme consensus = fragile.

**Result:** The opposite-signal finding is confirmed (low δ correlates
with flat/inverted curve, r = 0.28). But:
- No lead time over the 3m-10y spread
- Low defect is CONCURRENT with inversions, not leading them
- Bottom-quintile entries: spread declined in only 42% of cases
- Defect is descriptive ("curve is in consensus mode"), not predictive

**Verdict:** Intellectually interesting, not actionable.

---

### 4. Per-Node Decomposition (30 stocks, 60-day window)

**Hypothesis:** δ_i identifies which stocks drive structural fragility.

**Result:** 65 fault line migrations in 93 months. Top contributor
changes almost every month. HHI = 0.034-0.056 vs uniform 0.033.
No single node dominates.

**Verdict:** Too noisy to be actionable at individual stock level.

---

### 5. Per-Node Decomposition v2 (S&P 100, 120-day window)

**Hypothesis:** Larger universe + longer window produces stable leaders.

**Result:** Top-5 concentration = 2.5% (uniform would be 5.3%).
Quarter-to-quarter overlap of top-5: typically 0-1 out of 5.
The defect is MORE evenly spread than uniform distribution.

**Root cause:** In dense, highly correlated networks, the commutator
[L,P] distributes uniformly across all nodes. No structural reason
for concentration.

**Verdict:** Structural dead end. Not a parameter problem.

---

### 6. Regime Detector (2010-2023)

**Hypothesis:** FRAGILE regime (high δ) predicts worse future outcomes.

**Result:**
- FRAGILE regime: fwd 20d = +0.31%, fwd 60d = +2.20%
- CALM regime: fwd 20d = +1.99%, fwd 60d = +5.42%
- Corr(defect, VIX) = -0.551

**Key quadrant test (Low VIX + High defect):**
- Fwd 60d = +1.69%, MaxDD = -6.16%
- vs Low VIX + Low defect: Fwd 60d = +1.76%, MaxDD = -5.24%
- Difference is marginal. No actionable edge.

**Root cause:** Defect ≈ inverse VIX. The market already prices this.

**Verdict:** Redundant with existing volatility measures.

---

### 7. Power Grid Structural Analysis

**Hypothesis:** In sparse networks, per-node decomposition identifies
load-bearing infrastructure.

**Result:**
- Top-5 concentration IS above uniform (10-53% vs 4-36% uniform)
- BUT removing high-defect nodes does NOT worsen the system more than
  removing random nodes
- IEEE 118-bus: control (removing LOW-defect nodes) showed 4/5 worsens
  vs treatment (high-defect) 3/10 worsens

**Verdict:** Concentration exists in sparse networks, but does not
correspond to "load-bearing" in the engineering sense.

---

### 8. Spectral Pairing Stability

**Hypothesis:** The temporal derivative of the Fiedler ordering (how
much the spectral pairing reshuffles) is a genuinely non-local signal.

**Result:**
- Mean turnover: 94.5% of pairs change every week
- Rank correlation between consecutive Fiedler orderings: -0.012
- Correlation with future outcomes: ≈ 0 across all metrics

**Root cause:** In dense correlation networks, the Fiedler vector is
dominated by the market factor. Small perturbations in the correlation
matrix completely reshuffle the spectral ordering. The pairing is not
a persistent structural feature — it's noise in the second eigenvector.

**Verdict:** The Fiedler duality operator is structurally unstable in
dense networks. This is the deepest failure.

---

## SRS Diagnosis

Applying our own framework to Prism's financial application:

**Model M:** Dense equity correlation network (88-94 stocks, all
pairwise correlated at r > 0.3).

**Discriminating property P:** Duality defect δ = ||[L,P]||_F / ||L||_F.

**Is P decidable within M?** Yes. The defect correlates -0.55 with VIX,
which is directly observable and already priced by the market. The
spectral pairing reshuffles completely every week (turnover 94.5%),
meaning P is measuring noise in the second eigenvector, not persistent
structure. Any market participant with access to a correlation matrix
can compute δ — it does not escape the model's descriptive capacity.

**SRS index:** α = cost(P) / cap(M) ≤ 1.

**Conclusion:** Prism's financial application fails the self-referential
safety condition. The metric is decidable within the model it claims to
diagnose. It does not measure something that correlation/volatility
structurally cannot.

---

## What Survives

1. **The mathematical definition.** δ(L,P) is a well-defined structural
   metric grounded in UCA's duality compatibility condition.

2. **The Karate Club result.** 100% accuracy on a genuinely structured,
   sparse network with clear community structure.

3. **The 2017 finding.** One compelling historical episode where δ
   detected chronic fragility invisible to VIX. Publishable as a case
   study, not as a systematic signal.

4. **The theoretical paper.** The arXiv submission stands as a
   contribution to structural network analysis. It does not claim
   financial predictive power.

5. **The cross-domain principle.** Same formula, no training data,
   millisecond computation. The formula is correct; the application
   domain (dense correlation networks) was wrong.

---

## What Does Not Survive

- Any financial SaaS product based on rolling defect
- Per-node attribution in dense networks (equity, bond)
- Predictive power for drawdowns, volatility, or regime changes
- The "structural pressure heatmap" product concept
- Power grid load-bearing node identification

---

## Next Direction

The failure is domain-specific, not method-specific. Prism fails on
dense correlation networks because:
1. The Fiedler vector is unstable (dominated by market factor)
2. The commutator distributes uniformly (no concentration)
3. The defect is redundant with inverse VIX (α ≤ 1)

These problems do NOT apply to sparse topological networks where:
- Adjacency is binary (connected or not), not continuous correlation
- Topology is fixed (roads, pipes, wires), not rolling-window estimated
- The Fiedler vector reflects genuine graph structure, not noisy PCA
- Local metrics (degree, betweenness) provably miss spectral properties

**Candidate domains for next phase:**
- Transportation networks (road/rail topology, fixed structure)
- Energy distribution (pipeline networks, grid topology)
- Industrial supply chains (sparse, directed, with bottlenecks)
- Biological metabolism (enzyme networks, pathway structure)

The key requirement: the network must have FIXED TOPOLOGY with genuine
sparsity, not a correlation matrix estimated from time series.

---

## Lessons

1. Always test the null hypothesis first. "Does this add information
   beyond the simplest existing metric?" should be experiment #1.

2. Dense correlation networks are hostile to spectral methods. The
   second eigenvector is noise when all pairwise correlations are high.

3. The SRS framework correctly diagnosed the failure: α ≤ 1 means the
   metric is decidable within the model. We should have applied this
   test before running 8 experiments.

4. A theoretically grounded metric can still fail empirically if the
   domain violates the method's structural assumptions.

---

*Report date: 2026-05-18*
*Experiments: 8 conducted, 0 produced actionable financial signals*
*Status: Financial product direction closed. Sparse network direction open.*
