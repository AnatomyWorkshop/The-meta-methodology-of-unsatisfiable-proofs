"""
Meta-Dispatch Router v0.1

Static routing by task type + layered context injection + @op parsing.
Built on raw HTTP (LiteLLM integration in v0.2).
"""

import json
import urllib.request
import os
import time
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROOT = Path(__file__).parent.parent
ENV_FILE = ROOT / ".env.keys"


def load_env():
    """Load API keys from .env.keys file."""
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


ENV = load_env()

# Model configurations
MODELS = {
    "deepseek": {
        "base_url": ENV.get("RELAY_SPACECX_BASE_URL", "https://ai.space.cx/"),
        "key": ENV.get("RELAY_SPACECX_KEY", ""),
        "model": ENV.get("RELAY_SPACECX_MODEL", "deepseek-v4-pro"),
    },
    "claude": {
        "base_url": ENV.get("RELAY_LANYI_BASE_URL", "https://lanyiapi.com/"),
        "key": ENV.get("RELAY_LANYI_KEY", ""),
        "model": "claude-sonnet-4-20250514",
    },
}

# Task type → model routing table
ROUTING_TABLE = {
    "judgment": "claude",       # architecture, strategy, creative decisions
    "critique": "deepseek",     # finding holes, adversarial review
    "code": "deepseek",         # code generation, numerical experiments
    "format": "deepseek",       # formatting, translation, data cleaning
    "analysis": "deepseek",     # literature review, data analysis
}


# ---------------------------------------------------------------------------
# Layered Context Injection
# ---------------------------------------------------------------------------

LEVEL_0 = "Apophenia is a research automation company. Core products: Illusion (structural diagnosis of proof barriers), Meta-Dispatch (AI model router), Growth Agent (accumulating research memory)."

LEVEL_1 = """Current state (2026-05):
- 3 UCA papers published (classical physics, Riemann hypothesis, BSD conjecture)
- Illusion validated across 6 mathematical domains (SAFE on solved, UNKNOWN on open)
- Meta-dispatch v0.1 under construction (static routing + context injection + @op parsing)
- Company: Apophenia Pte. Ltd. (Singapore), pre-revenue, AI-native team
- Key insight: duality self-consistency as structural origin of fundamental equations"""


def inject_context(task_type: str, task_background: str = "") -> str:
    """Build context packet based on task complexity."""
    if task_type in ("format", "code"):
        # Simple tasks: just identity + content
        return LEVEL_0
    elif task_type == "analysis":
        return f"{LEVEL_0}\n\n{LEVEL_1}"
    else:
        # Complex tasks (judgment, critique): full context
        ctx = f"{LEVEL_0}\n\n{LEVEL_1}"
        if task_background:
            ctx += f"\n\nTask background: {task_background}"
        return ctx


# ---------------------------------------------------------------------------
# @op Protocol
# ---------------------------------------------------------------------------

# Whitelist of allowed operations
OP_WHITELIST = {
    "diagnose",    # run Illusion diagnosis on a target
    "transform",   # apply a transform in L2 search
    "srs_check",   # check SRS safety classification
    "validate",    # validate a result against known data
    "archive",     # move a file to archive/
    "dispatch",    # route a sub-task to another model
}


def parse_ops(text: str) -> list[dict]:
    """Extract @op markers from model output."""
    ops = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("@") and " " in line:
            parts = line.split(None, 1)
            op_name = parts[0][1:]  # remove @
            if op_name in OP_WHITELIST:
                # Parse key=value pairs
                params = {}
                if len(parts) > 1:
                    for token in parts[1].split():
                        if "=" in token:
                            k, v = token.split("=", 1)
                            params[k] = v
                ops.append({"op": op_name, "params": params})
    return ops


# ---------------------------------------------------------------------------
# API Call
# ---------------------------------------------------------------------------

def call_model(model_name: str, messages: list[dict], max_tokens: int = 2000) -> dict:
    """Call a model via its configured API."""
    config = MODELS[model_name]
    url = config["base_url"].rstrip("/") + "/v1/chat/completions"

    data = json.dumps({
        "model": config["model"],
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['key']}",
    })

    start = time.time()
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    elapsed = time.time() - start
    content = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})

    return {
        "content": content,
        "model": model_name,
        "elapsed": elapsed,
        "input_tokens": usage.get("prompt_tokens", 0),
        "output_tokens": usage.get("completion_tokens", 0),
        "ops": parse_ops(content),
    }


# ---------------------------------------------------------------------------
# Dispatch (main entry point)
# ---------------------------------------------------------------------------

def dispatch(
    task: str,
    task_type: str = "analysis",
    background: str = "",
    thread_id: str = "",
    model_override: Optional[str] = None,
) -> dict:
    """
    Main dispatch function.

    Args:
        task: The task/question to send to the model
        task_type: One of: judgment, critique, code, format, analysis
        background: Additional context for this specific task
        thread_id: Research thread identifier for cost aggregation
        model_override: Force a specific model (bypass routing table)
    """
    model = model_override or ROUTING_TABLE.get(task_type, "deepseek")
    context = inject_context(task_type, background)

    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": task},
    ]

    result = call_model(model, messages)
    result["task_type"] = task_type
    result["thread_id"] = thread_id

    # Log cost
    _log_cost(result)

    return result


# ---------------------------------------------------------------------------
# Cost Tracking
# ---------------------------------------------------------------------------

COST_LOG = ROOT / "meta-dispatch" / "cost_log.jsonl"


def _log_cost(result: dict):
    """Append cost entry to log file."""
    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "model": result["model"],
        "task_type": result["task_type"],
        "thread_id": result.get("thread_id", ""),
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],
        "elapsed": round(result["elapsed"], 2),
    }
    with open(COST_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


# ---------------------------------------------------------------------------
# Adversarial iteration
# ---------------------------------------------------------------------------

def adversarial(
    task: str,
    background: str = "",
    rounds: int = 2,
    thread_id: str = "",
) -> list[dict]:
    """
    Run adversarial iteration: Claude proposes → Deepseek critiques → repeat.
    Returns list of all responses.
    """
    history = []

    # Round 1: Claude proposes
    proposal = dispatch(
        task=task,
        task_type="judgment",
        background=background,
        thread_id=thread_id,
        model_override="claude",
    )
    history.append({"role": "proposer", **proposal})

    for i in range(rounds):
        # Deepseek critiques
        critique_prompt = f"请严格审查以下方案，找出漏洞、风险和遗漏：\n\n{proposal['content']}"
        critique = dispatch(
            task=critique_prompt,
            task_type="critique",
            background=background,
            thread_id=thread_id,
        )
        history.append({"role": "critic", **critique})

        # Claude addresses
        address_prompt = f"以下是对你方案的批评，请修正：\n\n批评：{critique['content']}\n\n你的原方案：{proposal['content']}"
        proposal = dispatch(
            task=address_prompt,
            task_type="judgment",
            background=background,
            thread_id=thread_id,
            model_override="claude",
        )
        history.append({"role": "proposer", **proposal})

    return history


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python router.py <task> [--type TYPE] [--thread THREAD]")
        print("Types: judgment, critique, code, format, analysis")
        sys.exit(1)

    task = sys.argv[1]
    task_type = "analysis"
    thread_id = ""

    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--type" and i + 1 < len(sys.argv):
            task_type = sys.argv[i + 1]
        elif arg == "--thread" and i + 1 < len(sys.argv):
            thread_id = sys.argv[i + 1]

    result = dispatch(task, task_type=task_type, thread_id=thread_id)
    print(result["content"])
    if result["ops"]:
        print(f"\n--- @ops detected: {result['ops']}")
