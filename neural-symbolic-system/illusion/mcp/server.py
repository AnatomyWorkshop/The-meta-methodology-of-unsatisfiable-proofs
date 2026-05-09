"""
Illusion MCP Server — Phase 4b

Two tools:
  propose_transforms   — given domain context + existing results, suggest new transforms
  search_literature    — given a transform + L1 model, retrieve decidability evidence

Transport: stdio (for Claude Code local MCP config)
Requires: pip install "mcp[cli]"

LLM backend (pick one via .env):
  Anthropic / relay:  set ANTHROPIC_API_KEY + optionally ANTHROPIC_BASE_URL
  DeepSeek (OpenAI-compat): set DEEPSEEK_API_KEY + optionally DEEPSEEK_BASE_URL
  Falls back to prompt-only mode if neither key is set.
"""

import json
import os
import sys
from typing import Any

# Auto-load .env from the same directory as this script (optional dependency)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print(
        "ERROR: mcp package not installed.\n"
        "Run: pip install \"mcp[cli]\"\n"
        "Or with proxy: pip install --proxy <proxy_url> \"mcp[cli]\"",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# LLM backend selection
# Priority: ANTHROPIC_API_KEY > DEEPSEEK_API_KEY > prompt-only
# ---------------------------------------------------------------------------

_backend = None   # "anthropic" | "openai" | None
_client = None
_MODEL = os.environ.get("ILLUSION_MODEL", "")

_anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
# Normalize base URL: strip trailing slash and trailing /v1 so we always append /v1/messages once.
_raw_base = os.environ.get("ANTHROPIC_BASE_URL", "").rstrip("/")
if _raw_base.endswith("/v1"):
    _anthropic_base = _raw_base[:-3].rstrip("/")  # strip /v1 suffix
else:
    _anthropic_base = _raw_base

_deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")
_deepseek_base = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

if _anthropic_key:
    # Use httpx directly to avoid Anthropic SDK URL construction issues with relay servers.
    # The SDK appends /v1 in a way that can double-append when the relay already routes /v1.
    try:
        import httpx as _httpx
        _backend = "anthropic"
        if not _MODEL:
            _MODEL = "claude-opus-4-7"
    except ImportError:
        pass

if _backend is None and _deepseek_key:
    try:
        import openai as _openai_sdk
        _client = _openai_sdk.OpenAI(
            api_key=_deepseek_key,
            base_url=_deepseek_base,
        )
        _backend = "openai"
        if not _MODEL:
            _MODEL = "deepseek-chat"
    except ImportError:
        pass

_MAX_TOKENS = int(os.environ.get("ILLUSION_MAX_TOKENS", "2048"))

app = Server("illusion-mcp")


async def _call_llm(system: str, prompt: str) -> str | None:
    """Call the configured LLM backend. Returns response text, error string, or None."""
    if _backend is None:
        return None
    try:
        if _backend == "anthropic":
            import httpx as _httpx
            import asyncio as _asyncio
            base = _anthropic_base if _anthropic_base else "https://api.anthropic.com"
            url = f"{base}/v1/messages"
            headers = {
                "x-api-key": _anthropic_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }
            body = {
                "model": _MODEL,
                "max_tokens": _MAX_TOKENS,
                "system": system,
                "messages": [{"role": "user", "content": prompt}],
            }

            def _sync_call():
                with _httpx.Client(timeout=60) as client:
                    resp = client.post(url, headers=headers, json=body)
                    resp.raise_for_status()
                    data = resp.json()
                    for block in data.get("content", []):
                        if isinstance(block, dict) and block.get("type") == "text":
                            return block["text"]
                    return f"[no text block: {list(data.keys())}]"

            # Run sync httpx in thread to avoid blocking the MCP event loop
            loop = _asyncio.get_event_loop()
            return await loop.run_in_executor(None, _sync_call)

        elif _backend == "openai":
            response = _client.chat.completions.create(
                model=_MODEL,
                max_tokens=_MAX_TOKENS,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"[LLM call failed: {e}]"
    return None


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

PROPOSE_TRANSFORMS_SCHEMA = {
    "type": "object",
    "properties": {
        "domain": {
            "type": "string",
            "description": (
                "Description of the computational model (L1). "
                "E.g. 'AC0 circuits, constant depth, AND/OR/NOT gates' or "
                "'monotone circuits, AND/OR only, k-CLIQUE target'."
            ),
        },
        "target_function": {
            "type": "string",
            "description": "The target function the model is trying to compute. E.g. 'PARITY', 'k-CLIQUE'.",
        },
        "existing_transforms": {
            "type": "array",
            "description": "List of transforms already in the registry with their results.",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "delta_collapse": {"type": "number"},
                    "l3_verdict": {"type": "string", "enum": ["SAFE", "UNSAFE", "UNKNOWN", "rejected_l2"]},
                    "rejection_reason": {"type": "string"},
                },
                "required": ["name", "delta_collapse", "l3_verdict"],
            },
        },
        "n_suggestions": {
            "type": "integer",
            "description": "Number of new transform suggestions to return (1-3).",
            "minimum": 1,
            "maximum": 3,
            "default": 2,
        },
    },
    "required": ["domain", "target_function", "existing_transforms"],
}

SEARCH_LITERATURE_SCHEMA = {
    "type": "object",
    "properties": {
        "transform_name": {
            "type": "string",
            "description": "Name of the transform whose decidability is in question.",
        },
        "transform_description": {
            "type": "string",
            "description": "Natural language description of what the transform does.",
        },
        "l1_model": {
            "type": "string",
            "description": "The computational model class (L1). E.g. 'AC0', 'monotone circuits', 'algebraic circuits'.",
        },
        "l3_question": {
            "type": "string",
            "description": (
                "The specific L3 question: 'Can a [model] decide whether a function satisfies "
                "the property induced by this transform?'"
            ),
        },
    },
    "required": ["transform_name", "l1_model", "l3_question"],
}


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="propose_transforms",
            description=(
                "Given a domain description and the results of existing transforms, "
                "propose 1-3 new candidate transforms for L2 to test. "
                "Output is natural language + pseudocode — human review required before implementation."
            ),
            inputSchema=PROPOSE_TRANSFORMS_SCHEMA,
        ),
        Tool(
            name="search_literature",
            description=(
                "Given a transform name and L1 model class, search for known results "
                "about whether the induced property is decidable within the model. "
                "Returns evidence + citations for human L3 review. "
                "Output is advisory — human makes the final L3 judgment."
            ),
            inputSchema=SEARCH_LITERATURE_SCHEMA,
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "propose_transforms":
        return await _propose_transforms(arguments)
    elif name == "search_literature":
        return await _search_literature(arguments)
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def _propose_transforms(args: dict[str, Any]) -> list[TextContent]:
    domain = args["domain"]
    target = args["target_function"]
    existing = args.get("existing_transforms", [])
    n = args.get("n_suggestions", 2)

    safe_candidates = [t for t in existing if t["l3_verdict"] == "SAFE"]
    unsafe_candidates = [t for t in existing if t["l3_verdict"] == "UNSAFE"]
    rejected_l2 = [t for t in existing if t["l3_verdict"] == "rejected_l2"]

    context = _build_transform_context(domain, target, safe_candidates, unsafe_candidates, rejected_l2)

    system = (
        "You are assisting the Illusion framework — a three-layer search system for "
        "discovering discriminating properties in computational complexity lower bounds. "
        "Your role is to propose new candidate transforms for L2 to test. "
        "Output is for human review — do not claim transforms are definitely SAFE."
    )

    prompt = f"""DOMAIN: {domain}
TARGET FUNCTION: {target}

EXISTING SEARCH RESULTS:
{context}

TASK: Propose {n} new transform(s) for L2 to test. Each transform should:
1. Modify the circuit or its input space in a way that might cause high delta-collapse
2. NOT obviously destroy the target function (avoid transforms that trivially break {target})
3. Be inspired by known proof techniques in this domain or adjacent domains

For each proposed transform, provide:
- NAME: a short identifier (snake_case)
- DESCRIPTION: what it does (2-3 sentences)
- PSEUDOCODE: how to implement it as a circuit wrapper
- HYPOTHESIS: why it might produce a self-referentially safe discriminating property
- RISK: what could go wrong (might affect target, might be decidable within L1)

IMPORTANT: These are suggestions for human review. The human will decide whether to implement them. Do not claim they are definitely SAFE — that is L3's job.

Respond in structured format."""

    llm_response = await _call_llm(system, prompt)

    if llm_response and not llm_response.startswith("[LLM call failed"):
        result = {
            "status": "completed",
            "domain": domain,
            "target": target,
            "n_suggestions": n,
            "suggestions": llm_response,
            "note": "These are AI-generated suggestions. Human review required before implementation.",
        }
    else:
        result = {
            "status": "prompt_ready",
            "note": (
                "No API key configured (set ANTHROPIC_API_KEY). "
                "The prompt below is ready to send manually."
            ),
            "prompt": prompt,
            "domain": domain,
            "target": target,
            "n_suggestions": n,
        }
        if llm_response and llm_response.startswith("[LLM call failed"):
            result["error"] = llm_response

    return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]


async def _search_literature(args: dict[str, Any]) -> list[TextContent]:
    transform_name = args["transform_name"]
    description = args.get("transform_description", "")
    l1_model = args["l1_model"]
    l3_question = args["l3_question"]

    system = (
        "You are assisting the Illusion framework's L3 safety monitor. "
        "Your role is to search your knowledge for known decidability results "
        "that bear on whether a given property is decidable within a computational model. "
        "Be precise with citations. If uncertain, say so. "
        "Output is advisory — a human makes the final L3 judgment."
    )

    prompt = f"""A candidate discriminating property has been flagged as UNKNOWN — the automated rule library has no matching rule.

TRANSFORM: {transform_name}
DESCRIPTION: {description}
L1 MODEL: {l1_model}
L3 QUESTION: {l3_question}

TASK: Search your knowledge for relevant results that bear on this question. Specifically:

1. Is there a known theorem or result that directly answers whether this property is decidable within {l1_model}?
2. Are there analogous properties in related models where decidability is known?
3. What is the computational complexity of deciding this property?
4. Are there known barriers (e.g., Natural Proofs, relativization) that apply?

For each piece of evidence, provide:
- CLAIM: the specific result
- SOURCE: paper title, authors, year (be precise — do not hallucinate citations)
- RELEVANCE: how it bears on the L3 question
- CONFIDENCE: high / medium / low (low if you are uncertain about the citation)

IMPORTANT: If you are uncertain about a citation, say so explicitly — a wrong citation is worse than no citation.

Respond in structured format."""

    llm_response = await _call_llm(system, prompt)

    if llm_response and not llm_response.startswith("[LLM call failed"):
        result = {
            "status": "completed",
            "transform": transform_name,
            "l1_model": l1_model,
            "l3_question": l3_question,
            "evidence": llm_response,
            "note": "This is AI-generated advisory output. Human makes the final L3 judgment.",
        }
    else:
        result = {
            "status": "prompt_ready",
            "note": (
                "No API key configured (set ANTHROPIC_API_KEY). "
                "The prompt below is ready to send manually."
            ),
            "prompt": prompt,
            "transform": transform_name,
            "l1_model": l1_model,
            "l3_question": l3_question,
        }
        if llm_response and llm_response.startswith("[LLM call failed"):
            result["error"] = llm_response

    return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]


def _build_transform_context(domain, target, safe, unsafe, rejected) -> str:
    lines = []
    if safe:
        lines.append("SAFE (self-referentially safe, valid discriminating properties):")
        for t in safe:
            lines.append(f"  - {t['name']} (delta={t['delta_collapse']:+.3f})")
    if unsafe:
        lines.append("UNSAFE (decidable within L1, rejected by L3):")
        for t in unsafe:
            lines.append(f"  - {t['name']} (delta={t['delta_collapse']:+.3f})")
    if rejected:
        lines.append("Rejected by L2 (low delta or target affected):")
        for t in rejected:
            reason = t.get("rejection_reason", "low delta or target affected")
            lines.append(f"  - {t['name']} (delta={t['delta_collapse']:+.3f}, reason: {reason})")
    return "\n".join(lines) if lines else "No existing transforms."


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
