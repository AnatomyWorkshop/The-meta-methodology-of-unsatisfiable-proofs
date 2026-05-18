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

## Phase 2: Sparse Network Experiments (2026-05-18)

Following the financial death sentence, we tested Prism on sparse
topological networks where the Fiedler vector should reflect genuine
structure rather than noise.

### 9. Sparse Benchmark v1: Criticality Detection (9 networks)

**Hypothesis:** Per-node defect identifies critical nodes (whose removal
most degrades algebraic connectivity) in sparse networks.

**Networks tested:** Karate Club, Florentine Families, Les Miserables,
Dolphins, Barbell, Grid 6x6, Tree, Watts-Strogatz, Barabasi-Albert.

**Result:** Prism wins 0/9 networks. Betweenness centrality dominates.

| Network | rho(Prism) | rho(Betweenness) | rho(Degree) |
|---------|-----------|-----------------|-------------|
| Karate Club | +0.512 | +0.801 | +0.817 |
| Florentine | +0.311 | +0.855 | +0.726 |
| Les Mis | +0.390 | +0.757 | +0.804 |
| Dolphins | +0.555 | +0.765 | +0.646 |
| Grid 6x6 | +0.251 | +0.368 | +0.182 |
| Tree | -0.029 | +0.786 | +0.817 |
| Watts-Strogatz | +0.374 | +0.715 | +0.226 |
| Barabasi-Albert | +0.557 | +0.852 | +0.808 |

**Verdict:** Per-node defect does NOT identify engineering-critical nodes
better than betweenness centrality. Not a domain problem — a method problem.

---

### 10. Sparse Benchmark v2: What Does Prism Actually Measure?

**Question:** Prism's rho was 0.3-0.55 on most networks — it measures
SOMETHING. What ground truth does it correlate with best?

**Ground truths tested:**
- Delta algebraic connectivity (betweenness wins)
- Fiedler cut proximity (Prism wins 4/5, mean |rho| = 0.534)
- Cross-cut edges (Prism wins 3/5)
- Spectral gap sensitivity (betweenness wins)
- Community boundary (betweenness wins)
- Pairing distance (Prism wins 3/5)

**Finding:** Prism best correlates with FIEDLER CUT PROXIMITY — how
close a node is to the spectral bisection boundary. This is tautological:
Prism is computed from the Fiedler vector, so it naturally correlates
with Fiedler-derived properties.

---

### 11. Sparse Benchmark v3: Boundary Detection

**Hypothesis (reframed):** Prism identifies community boundary nodes
(structural fault lines) rather than critical nodes.

**Result on planted partition models:**
- SBM (4x15): Prism rho = +0.268, Betweenness rho = +0.601
- SBM (3x20): Prism rho = -0.049, Betweenness rho = +0.479

**Verdict:** Even at boundary detection (its supposed niche),
betweenness still outperforms Prism on ground-truth community boundaries.

---

### 12. Global Defect vs Community Separation

**Test:** Sweep inter-community edge probability from 0 to p_in.

**Result:** Global defect is NON-MONOTONIC with community separation:
- p_out=0.02: defect = 0.54 (clear communities)
- p_out=0.05: defect = 0.65 (PEAK — maximum tension)
- p_out=0.30: defect = 0.35 (no communities, random graph)

Defect peaks at intermediate separation — when the network is most
"conflicted" about its partition. It does not simply measure community
clarity (modularity does that monotonically).

---

## Final Assessment

### What Prism's per-node decomposition actually measures:

It measures proximity to the Fiedler spectral bisection. This is:
1. Tautological (derived from the same eigenvector)
2. Inferior to betweenness for criticality detection
3. Inferior to betweenness for boundary detection
4. Not independently useful as a product

### What the global defect measures:

It measures the tension between graph topology (L) and spectral duality
structure (P). It peaks when the network has community structure that
is neither perfectly separated nor fully blurred. This is a genuine
structural property, but:
- In dense networks: redundant with inverse VIX
- In sparse networks: non-monotonic with modularity, unclear product use

### Structural dead end diagnosis:

The Fiedler duality operator P (pair rank k with rank n+1-k) does not
correspond to any known engineering or physical concept of "criticality,"
"load-bearing," or "boundary." It is a mathematical construction that
produces a well-defined metric, but that metric does not map to actionable
real-world properties in any tested domain.

---

## What Survives (Revised)

1. **The mathematical definition.** delta(L,P) is well-defined and
   computable. It is a legitimate structural metric.

2. **The Karate Club result.** 100% community detection accuracy.
   This works because Karate Club's community structure happens to
   align perfectly with the Fiedler bisection.

3. **The 2017 finding.** One compelling historical episode.

4. **The theoretical paper.** Stands as a contribution to spectral
   graph theory. Does not claim practical utility.

5. **The non-monotonic modularity relationship.** Intellectually
   interesting: defect peaks at maximum structural tension. Potentially
   publishable as a theoretical observation.

---

## What Does Not Survive (Revised)

- Any per-node attribution product (sparse OR dense networks)
- Criticality detection (betweenness wins everywhere)
- Boundary detection (betweenness wins on ground truth)
- Infrastructure monitoring (no correspondence to load-bearing)
- Supply chain bottleneck identification
- Any product requiring per-node defect to mean something actionable

---

## Lessons (Updated)

1. Always test against the simplest baseline first. Betweenness
   centrality is the null hypothesis for node importance.

2. A metric derived from eigenvector X will tautologically correlate
   with properties of eigenvector X. This is not a finding.

3. The failure is now confirmed as METHOD-level, not domain-level.
   The Fiedler duality operator does not correspond to engineering
   criticality in ANY tested network topology.

4. The only remaining value is the GLOBAL scalar defect, and only
   in contexts where "structural tension" (non-monotonic with
   modularity) is itself the quantity of interest.

5. SRS diagnosis confirmed: alpha <= 1 across all domains tested.
   The metric is decidable within simpler frameworks (betweenness,
   modularity) that already exist.

---

*Report date: 2026-05-18 (updated with sparse network results)*
*Experiments: 12 conducted across dense and sparse networks*
*Status: Per-node product direction closed. Global defect: theoretical
interest only. No viable product direction identified.*
