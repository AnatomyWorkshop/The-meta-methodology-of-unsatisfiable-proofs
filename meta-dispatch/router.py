"""
Meta-Dispatch Router v0.1

Static routing by task type + layered context injection + @op parsing.
Built on raw HTTP (LiteLLM integration in v0.2).
"""

import json
import urllib.request
import os
import sys
import time
import uuid
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
    "sonnet-4.6": {
        "base_url": ENV.get("RELAY_LANYI_BASE_URL", "https://lanyiapi.com/"),
        "key": ENV.get("RELAY_LANYI_KEY", ""),
        "model": "claude-sonnet-4-6-20250514",
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
# Prompt Variants (A/B testing infrastructure)
# ---------------------------------------------------------------------------

_VARIANTS_FILE = ROOT / "meta-dispatch" / "prompts" / "variants.yaml"


def _load_variants() -> dict:
    """Load prompt variants from YAML (simple parser, no PyYAML dependency)."""
    if not _VARIANTS_FILE.exists():
        return {}
    variants = {}
    current_type = None
    current_variant = None
    for line in _VARIANTS_FILE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0 and stripped.endswith(":"):
            current_type = stripped[:-1]
            variants[current_type] = {}
            current_variant = None
        elif indent == 2 and stripped.endswith(":"):
            current_variant = stripped[:-1]
            variants[current_type][current_variant] = {}
        elif indent == 4 and ":" in stripped and current_type and current_variant:
            k, v = stripped.split(":", 1)
            variants[current_type][current_variant][k.strip()] = v.strip().strip('"')
    return variants


PROMPT_VARIANTS = _load_variants()


def get_variant_suffix(task_type: str, variant: str = "default") -> str:
    """Get the system prompt suffix for a given task_type + variant."""
    type_variants = PROMPT_VARIANTS.get(task_type, {})
    v = type_variants.get(variant, type_variants.get("default", {}))
    return v.get("system_suffix", "")


# ---------------------------------------------------------------------------
# Layered Context Injection
# ---------------------------------------------------------------------------

LEVEL_0 = "Apophenia is a research automation company. Core products: Illusion (structural diagnosis of proof barriers), Meta-Dispatch (AI model router), Growth Agent (accumulating research memory)."

# Level 1 loaded from file if available, otherwise fallback
_LEVEL_1_FILE = ROOT / "meta-dispatch" / "context_level1.md"

def _load_level_1() -> str:
    if _LEVEL_1_FILE.exists():
        return _LEVEL_1_FILE.read_text(encoding="utf-8").strip()
    return """Current state (2026-05):
- 3 UCA papers published (classical physics, Riemann hypothesis, BSD conjecture)
- Illusion validated across 6 mathematical domains (SAFE on solved, UNKNOWN on open)
- Meta-dispatch v0.1 under construction (static routing + context injection + @op parsing)
- Company: Apophenia Pte. Ltd. (Singapore), pre-revenue, AI-native team
- Key insight: duality self-consistency as structural origin of fundamental equations"""

LEVEL_1 = _load_level_1()


def inject_context(task_type: str, task_background: str = "", variant: str = "default") -> str:
    """Build context packet based on task complexity + prompt variant."""
    if task_type in ("format", "code"):
        ctx = LEVEL_0
    elif task_type == "analysis":
        ctx = f"{LEVEL_0}\n\n{LEVEL_1}"
    else:
        ctx = f"{LEVEL_0}\n\n{LEVEL_1}"
        if task_background:
            ctx += f"\n\nTask background: {task_background}"

    suffix = get_variant_suffix(task_type, variant)
    if suffix:
        ctx += f"\n\n{suffix}"
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
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        elapsed = time.time() - start
        body = e.read().decode("utf-8", errors="replace")[:500] if e.fp else ""
        return {
            "content": f"[API ERROR {e.code}] {e.reason}\n{body}",
            "model": model_name,
            "elapsed": elapsed,
            "input_tokens": 0,
            "output_tokens": 0,
            "ops": [],
            "error": True,
        }
    except (urllib.error.URLError, TimeoutError) as e:
        elapsed = time.time() - start
        return {
            "content": f"[NETWORK ERROR] {e}",
            "model": model_name,
            "elapsed": elapsed,
            "input_tokens": 0,
            "output_tokens": 0,
            "ops": [],
            "error": True,
        }

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
    auto_execute: bool = False,
    variant: str = "default",
) -> dict:
    """
    Main dispatch function.

    Args:
        task: The task/question to send to the model
        task_type: One of: judgment, critique, code, format, analysis
        background: Additional context for this specific task
        thread_id: Research thread identifier for cost aggregation
        model_override: Force a specific model (bypass routing table)
        auto_execute: If True, automatically execute any @ops in the response
        variant: Prompt style variant for A/B testing (logged in cost_log)
    """
    model = model_override or ROUTING_TABLE.get(task_type, "deepseek")
    context = inject_context(task_type, background, variant=variant)

    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": task},
    ]

    result = call_model(model, messages)
    result["task_type"] = task_type
    result["thread_id"] = thread_id
    result["variant"] = variant

    _log_cost(result)

    if auto_execute and result["ops"]:
        result["op_results"] = execute_ops(result["ops"])

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
        "variant": result.get("variant", "default"),
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],
        "elapsed": round(result["elapsed"], 2),
    }
    with open(COST_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


# ---------------------------------------------------------------------------
# @op Execution
# ---------------------------------------------------------------------------

def execute_ops(ops: list[dict], context: dict = None) -> list[dict]:
    """
    Execute parsed @op commands. Returns list of execution results.
    Each op is sandboxed: failures don't halt the batch.
    """
    results = []
    for op in ops:
        name = op["op"]
        params = op.get("params", {})
        handler = _OP_HANDLERS.get(name)
        if not handler:
            results.append({"op": name, "status": "error", "msg": f"no handler for @{name}"})
            continue
        try:
            result = handler(params, context or {})
            results.append({"op": name, "status": "ok", **result})
        except Exception as e:
            results.append({"op": name, "status": "error", "msg": str(e)})
    return results


def _op_diagnose(params: dict, ctx: dict) -> dict:
    """Run Illusion SRS diagnosis on a target domain."""
    target = params.get("target", "rh")
    phase_map = {
        "circuit": "phase2_circuit",
        "monotone": "phase3_monotone",
        "algebraic": "phase4_algebraic",
        "resolution": "phase5_resolution",
        "frege": "phase5b_frege",
        "rh": "phase6_rh",
        "adelic": "phase7_adelic",
        "bsd": "phase8_bsd",
    }
    phase_dir = ROOT / "illusion" / phase_map.get(target, f"phase6_rh")
    runner = phase_dir / "run_experiment.py"
    if not runner.exists():
        return {"msg": f"no runner found for target={target}", "path": str(runner)}

    import subprocess
    result = subprocess.run(
        [sys.executable, str(runner)],
        capture_output=True, text=True, timeout=300, cwd=str(phase_dir)
    )
    return {"stdout": result.stdout[-2000:], "returncode": result.returncode}


def _op_archive(params: dict, ctx: dict) -> dict:
    """Move a file to archive/."""
    import shutil
    src = params.get("path", "")
    if not src:
        return {"msg": "no path specified"}
    src_path = ROOT / src
    if not src_path.exists():
        return {"msg": f"file not found: {src}"}
    dest_dir = ROOT / "archive"
    dest_dir.mkdir(exist_ok=True)
    shutil.move(str(src_path), str(dest_dir / src_path.name))
    return {"msg": f"archived {src_path.name}"}


_DISPATCH_DEPTH = 0
_MAX_DISPATCH_DEPTH = 3


def _op_dispatch(params: dict, ctx: dict) -> dict:
    """Route a sub-task to another model (recursive dispatch)."""
    global _DISPATCH_DEPTH
    if _DISPATCH_DEPTH >= _MAX_DISPATCH_DEPTH:
        return {"msg": f"max recursion depth ({_MAX_DISPATCH_DEPTH}) reached", "status": "blocked"}
    task = params.get("task", "")
    task_type = params.get("type", "analysis")
    model = params.get("model")
    if not task:
        return {"msg": "no task specified"}
    _DISPATCH_DEPTH += 1
    try:
        result = dispatch(task, task_type=task_type, model_override=model)
    finally:
        _DISPATCH_DEPTH -= 1
    return {"msg": "sub-dispatch complete", "content_preview": result["content"][:200]}


def _op_validate(params: dict, ctx: dict) -> dict:
    """Validate a claim against known data (stub — returns structure for manual check)."""
    claim = params.get("claim", "")
    return {"msg": "validation requested", "claim": claim, "status": "manual_review"}


def _op_srs_check(params: dict, ctx: dict) -> dict:
    """Check SRS safety classification for a domain."""
    target = params.get("target", "")
    known_safe = {"circuit", "monotone", "algebraic", "resolution", "frege", "frege_scaling"}
    known_unknown = {"rh", "bsd", "adelic"}
    if target in known_safe:
        return {"classification": "SAFE", "target": target}
    elif target in known_unknown:
        return {"classification": "UNKNOWN", "target": target}
    return {"classification": "UNCLASSIFIED", "target": target}


def _op_transform(params: dict, ctx: dict) -> dict:
    """Apply a transform in L2 search (stub — logs intent)."""
    transform = params.get("name", "unknown")
    return {"msg": f"transform '{transform}' noted for L2 search", "status": "logged"}


_OP_HANDLERS = {
    "diagnose": _op_diagnose,
    "archive": _op_archive,
    "dispatch": _op_dispatch,
    "validate": _op_validate,
    "srs_check": _op_srs_check,
    "transform": _op_transform,
}


# ---------------------------------------------------------------------------
# Adversarial iteration
# ---------------------------------------------------------------------------

def adversarial(
    task: str,
    background: str = "",
    rounds: int = 4,
    thread_id: str = "",
    converge_threshold: int = 2,
) -> list[dict]:
    """
    Run adversarial iteration: Claude proposes → Deepseek critiques → repeat.
    Stops early if critic produces no new substantive issues for `converge_threshold`
    consecutive rounds (inspired by CEGAR counterexample elimination).
    Returns list of all responses.
    """
    history = []
    no_new_issues = 0

    proposal = dispatch(
        task=task,
        task_type="judgment",
        background=background,
        thread_id=thread_id,
        model_override="claude",
    )
    history.append({"role": "proposer", **proposal})

    for i in range(rounds):
        critique_prompt = (
            "请严格审查以下方案，找出漏洞、风险和遗漏。"
            "如果你认为方案已经足够完善没有明显问题，请回复'无新问题'。\n\n"
            f"{proposal['content']}"
        )
        critique = dispatch(
            task=critique_prompt,
            task_type="critique",
            background=background,
            thread_id=thread_id,
        )
        history.append({"role": "critic", "round": i + 1, **critique})

        if _is_converged(critique["content"]):
            no_new_issues += 1
            if no_new_issues >= converge_threshold:
                history.append({"role": "system", "content": f"Converged after {i + 1} rounds (no new issues x{converge_threshold})"})
                break
        else:
            no_new_issues = 0

        address_prompt = f"以下是对你方案的批评，请修正：\n\n批评：{critique['content']}\n\n你的原方案：{proposal['content']}"
        proposal = dispatch(
            task=address_prompt,
            task_type="judgment",
            background=background,
            thread_id=thread_id,
            model_override="claude",
        )
        history.append({"role": "proposer", "round": i + 1, **proposal})

    return history


def _is_converged(critique_text: str) -> bool:
    """Heuristic: critic found no new substantive issues."""
    markers = ["无新问题", "没有明显问题", "方案完善", "no new issues", "no major issues"]
    text_lower = critique_text.lower()[:200]
    return any(m in text_lower for m in markers)


# ---------------------------------------------------------------------------
# Dispatch to file (write result directly to lab/ or inbox/)
# ---------------------------------------------------------------------------

def dispatch_to_file(
    task: str,
    filename: str,
    task_type: str = "analysis",
    background: str = "",
    thread_id: str = "",
    output_dir: str = "lab",
) -> Path:
    """Dispatch and write result to a file. Returns the file path."""
    result = dispatch(task, task_type=task_type, background=background, thread_id=thread_id)

    out_dir = ROOT / output_dir
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / filename

    header = f"# {filename.replace('.md', '').replace('-', ' ').title()}\n\n"
    header += f"> Model: {result['model']} | Tokens: {result['input_tokens']}+{result['output_tokens']} | Time: {result['elapsed']:.1f}s\n\n"

    out_path.write_text(header + result["content"], encoding="utf-8")
    return out_path


# ---------------------------------------------------------------------------
# Batch Processing (with safety: dedup, timeout, failure isolation, logging)
# ---------------------------------------------------------------------------

BATCH_LOG = ROOT / "meta-dispatch" / "batch_log.jsonl"


def batch(
    tasks: list[dict] = None,
    inbox_dir: str = "inbox",
    thread_id: str = "",
    timeout_per_task: int = 600,
    skip_on_failure: bool = True,
) -> list[dict]:
    """
    Process a batch of tasks. Sources:
    1. Explicit task list (each dict has 'task', optional 'task_type', 'background', 'filename')
    2. All .md files in inbox_dir (if tasks is None)

    Safety mechanisms (per Doubao review):
    - Unique task ID per execution
    - .done marker for dedup
    - Per-task timeout
    - Failure isolation (skip or halt)
    - Structured logging
    """
    if tasks is None:
        tasks = _load_inbox(inbox_dir)

    results = []
    for task_spec in tasks:
        task_id = uuid.uuid4().hex[:8]
        task_text = task_spec.get("task", "")
        task_type = task_spec.get("task_type", "analysis")
        background = task_spec.get("background", "")
        filename = task_spec.get("filename", f"{task_id}.md")
        source_file = task_spec.get("_source_file")

        if source_file and _is_done(source_file):
            results.append({"task_id": task_id, "status": "skipped", "reason": "already processed"})
            continue

        start = time.time()
        try:
            result = dispatch(
                task=task_text,
                task_type=task_type,
                background=background,
                thread_id=thread_id or task_id,
                auto_execute=True,
            )
            elapsed = time.time() - start

            if elapsed > timeout_per_task:
                entry = {"task_id": task_id, "status": "timeout", "elapsed": elapsed}
            else:
                out_path = _write_batch_result(task_id, filename, result)
                entry = {"task_id": task_id, "status": "ok", "output": str(out_path), "elapsed": round(elapsed, 2)}

            if source_file:
                _mark_done(source_file)

        except Exception as e:
            elapsed = time.time() - start
            entry = {"task_id": task_id, "status": "error", "msg": str(e), "elapsed": round(elapsed, 2)}
            if not skip_on_failure:
                _log_batch(entry)
                results.append(entry)
                break

        _log_batch(entry)
        results.append(entry)

    return results


def _load_inbox(inbox_dir: str) -> list[dict]:
    """Load all .md files from inbox as tasks."""
    inbox = ROOT / inbox_dir
    if not inbox.exists():
        return []
    tasks = []
    for f in sorted(inbox.glob("*.md")):
        if f.name.startswith(".") or _is_done(str(f)):
            continue
        content = f.read_text(encoding="utf-8").strip()
        if not content:
            continue
        tasks.append({
            "task": content,
            "task_type": "analysis",
            "filename": f.stem + "-result.md",
            "_source_file": str(f),
        })
    return tasks


def _is_done(filepath: str) -> bool:
    return Path(filepath + ".done").exists()


def _mark_done(filepath: str):
    Path(filepath + ".done").write_text(time.strftime("%Y-%m-%dT%H:%M:%S"), encoding="utf-8")


def _write_batch_result(task_id: str, filename: str, result: dict) -> Path:
    out_dir = ROOT / "lab" / "batch"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename

    header = f"# {filename.replace('.md', '').replace('-', ' ').title()}\n\n"
    header += f"> Task ID: {task_id} | Model: {result['model']} | Tokens: {result['input_tokens']}+{result['output_tokens']} | Time: {result['elapsed']:.1f}s\n\n"

    out_path.write_text(header + result["content"], encoding="utf-8")
    return out_path


def _log_batch(entry: dict):
    entry["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(BATCH_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python router.py <task> [--type TYPE] [--thread THREAD] [--execute]")
        print("       python router.py --batch [--thread THREAD]")
        print("Types: judgment, critique, code, format, analysis")
        sys.exit(1)

    sys.stdout.reconfigure(encoding="utf-8")

    if sys.argv[1] == "--batch":
        thread_id = ""
        for i, arg in enumerate(sys.argv[2:], 2):
            if arg == "--thread" and i + 1 < len(sys.argv):
                thread_id = sys.argv[i + 1]
        results = batch(thread_id=thread_id)
        for r in results:
            print(f"[{r['status']}] {r['task_id']} — {r.get('output', r.get('msg', r.get('reason', '')))}")
        sys.exit(0)

    task = sys.argv[1]
    task_type = "analysis"
    thread_id = ""
    auto_exec = False

    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--type" and i + 1 < len(sys.argv):
            task_type = sys.argv[i + 1]
        elif arg == "--thread" and i + 1 < len(sys.argv):
            thread_id = sys.argv[i + 1]
        elif arg == "--execute":
            auto_exec = True

    result = dispatch(task, task_type=task_type, thread_id=thread_id, auto_execute=auto_exec)
    print(result["content"])
    if result["ops"]:
        print(f"\n--- @ops detected: {result['ops']}")
    if result.get("op_results"):
        print(f"--- @op results: {result['op_results']}")
