# Architecture Overview

## System Components

### Illusion (Structural Diagnosis Engine)

Three-layer architecture for classifying mathematical proof barriers:

```
L1 (Model)     → Domain-specific neural/symbolic model
L2 (Search)    → Finds transforms that degrade L1 performance
L3 (Classify)  → SAFE / UNSAFE / UNKNOWN based on structural analysis
```

Each phase implements this architecture for a specific mathematical domain.

### UCA (Universal Closure Axiom)

Theoretical framework: $\mathcal{D}\phi = \star\,\mathcal{D}^\dagger\,\star\,\phi$

Applied to:
- GL(1): Riemann Hypothesis (Paper 4)
- GL(2): BSD Conjecture (Paper 5)
- Classical physics: QM, Yang-Mills, gravity (Paper 1)

### Meta-Dispatch (AI Router)

Routes tasks to optimal AI models based on:
- Task complexity → model selection
- Cost constraints → cheaper models for routine work
- Quality requirements → expensive models for judgment

## Data Flow

```
User intent → Meta-Dispatch → [Model A, Model B, ...] → Results → Quality check → Output
```

## File Conventions

- Papers: `papers/{topic}/paper{N}-{short-name}.md`
- Phases: `illusion/phase{N}_{domain}/`
- Archive: `archive/{type}/{date}-{description}.md`
- Private: `private/` (gitignored)
