# Meta-Dispatch — Research Accelerator

> Status: Design phase. Iterative adversarial refinement in progress.

## Purpose

Route research tasks to optimal AI models. Not a cost-saving tool — a research acceleration tool.

## Design Principles (v0.2, post-Deepseek critique)

1. **Static routing by task type**, not dynamic upgrade by quality
2. **Adversarial iteration pre-configured** as Claude ↔ Deepseek pairs
3. **Cost aggregated by research thread**, not by single call
4. **Built on LiteLLM**, not from scratch

## Task Type → Model Routing

| Task Type | Model | Reason |
|-----------|-------|--------|
| Mathematical architecture / judgment | Claude Opus | Irreplaceable for structural reasoning |
| Code generation / numerical experiments | Deepseek-Coder / Deepseek-v4-pro | Fast, cheap, good at code |
| Adversarial critique / hole-finding | Deepseek-v4-pro | Good at finding flaws |
| Literature summary / formatting | Deepseek-v4-pro (via ai.space.cx) | Free, quality sufficient |
| Chinese content / domestic market | 智谱清言 / 豆包 | Native Chinese optimization |
| Multimodal (images, design) | Gemini / GPT-4o | Vision capability |

## Adversarial Iteration Protocol

```
Claude designs v0.N → Deepseek critiques → Claude addresses → Deepseek re-critiques → converge
```

Pre-configured as a single command: `dispatch --adversarial "design the X"`

## Implementation

**Bottom layer**: LiteLLM (handles multi-provider API, failover, rate limits)
**Middle layer**: Task classifier (regex + keyword → task type → model)
**Top layer**: Thread manager (groups calls by research thread, aggregates cost)

### Planned files

- `router.py` — Task classification + LiteLLM dispatch
- `config.yaml` — Model routing table (the table above, as config)
- `cost_tracker.py` — Per-thread cost aggregation
- `adversarial.py` — Two-model iteration loop

## API Configuration

Reads from `../.env.keys` (gitignored).

## Dependencies

- `litellm` — Multi-provider LLM gateway
- `pyyaml` — Config parsing
- `rich` — Terminal output formatting
