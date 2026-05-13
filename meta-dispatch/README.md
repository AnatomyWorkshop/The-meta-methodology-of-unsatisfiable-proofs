# Meta-Dispatch — AI Model Router

> Status: Placeholder. Implementation follows repository reorganization.

## Purpose

Route tasks to the optimal AI model based on task type, cost constraints, and quality requirements.

## Design Principles

1. Default to cheapest model that meets quality threshold
2. Escalate only when quality check fails
3. Track cost per task for budget visibility
4. Support iterative adversarial validation (Claude ↔ Deepseek)

## Planned Components

- `router.py` — Task classification + model selection
- `config.yaml` — Model capabilities, costs, routing rules
- `cost_tracker.py` — Per-call cost logging and monthly reports

## Model Tiers

| Tier | Models | Use Cases |
|------|--------|-----------|
| Cheap | Deepseek-v4-pro, 豆包 | Formatting, translation, data cleaning |
| Mid | GPT-4o, Gemini | Analysis, writing, code generation |
| Expensive | Claude Opus | Architecture, judgment, creative work |

## API Configuration

Reads from `../.env.keys` (gitignored).
