"""
L2-MCP Integration: Automatic transform proposal when search space is exhausted.

When L2 has exhausted its registered transforms (or all candidates are classified),
this module calls the MCP server's propose_transforms tool to get AI-suggested
new transforms. The suggestions are presented to the human for review and
optional implementation.

Termination condition (4c design):
  The search loop terminates when EITHER:
  (a) A SAFE candidate is found (success), OR
  (b) The exhaustion criterion is met:
      - All registered transforms are classified (SAFE/UNSAFE/rejected_l2), AND
      - The last N AI-proposal rounds produced no new SAFE candidates, AND
      - The best delta_collapse in the last M rounds has not improved by > threshold

Usage:
    from illusion.mcp.l2_integration import propose_new_transforms, ExhaustionCriterion

    criterion = ExhaustionCriterion(n_dry_rounds=3, m_rounds=5, delta_threshold=0.01)
    if criterion.should_stop(search_history):
        print("Search exhausted — stopping.")
    else:
        suggestions = await propose_new_transforms(domain, target, existing_results)
        # Present to human, human decides which to implement

Or from CLI:
    python -m illusion.mcp.l2_integration <domain> <target_function>
"""

import asyncio
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("ERROR: mcp package not installed. Run: pip install \"mcp[cli]\"", file=sys.stderr)
    sys.exit(1)


SERVER_SCRIPT = str(Path(__file__).parent / "server.py")


# ---------------------------------------------------------------------------
# Termination condition for unbounded AI-assisted search
# ---------------------------------------------------------------------------

@dataclass
class SearchRound:
    """Record of one AI proposal round."""
    round_number: int
    n_proposed: int
    n_safe_found: int
    best_delta: float


@dataclass
class ExhaustionCriterion:
    """
    Stopping criterion for AI-assisted L2 search.

    Terminates when:
      - n_dry_rounds consecutive rounds produced 0 new SAFE candidates, AND
      - best delta_collapse in the last m_rounds rounds improved by < delta_threshold
    """
    n_dry_rounds: int = 3
    m_rounds: int = 5
    delta_threshold: float = 0.01

    def should_stop(self, history: list[SearchRound]) -> tuple[bool, str]:
        """
        Returns (should_stop, reason).
        """
        if len(history) < self.n_dry_rounds:
            return False, "not enough rounds yet"

        # Check: last n_dry_rounds all produced 0 SAFE candidates
        recent = history[-self.n_dry_rounds:]
        if any(r.n_safe_found > 0 for r in recent):
            return False, f"found SAFE candidate in last {self.n_dry_rounds} rounds"

        # Check: delta improvement in last m_rounds
        window = history[-self.m_rounds:]
        if len(window) >= 2:
            delta_improvement = window[-1].best_delta - window[0].best_delta
            if delta_improvement > self.delta_threshold:
                return False, f"delta still improving ({delta_improvement:+.4f} over {len(window)} rounds)"

        return True, (
            f"exhausted: {self.n_dry_rounds} consecutive dry rounds, "
            f"delta improvement < {self.delta_threshold} over last {len(window)} rounds"
        )


# ---------------------------------------------------------------------------
# Transform proposal
# ---------------------------------------------------------------------------

async def propose_new_transforms(
    domain: str,
    target_function: str,
    existing_transforms: list[dict[str, Any]],
    n_suggestions: int = 2,
) -> dict:
    """
    Call the MCP server's propose_transforms tool, then call the LLM directly
    if the server returns prompt_ready (server-side LLM call failed or not configured).

    Args:
        domain: Description of the L1 model
        target_function: The target function (e.g., "PARITY", "k-CLIQUE")
        existing_transforms: List of dicts with keys: name, delta_collapse, l3_verdict,
                             and optionally rejection_reason
        n_suggestions: Number of new transforms to request (1-3)

    Returns:
        dict with keys: status, suggestions (or prompt), domain, target, n_suggestions
    """
    args = {
        "domain": domain,
        "target_function": target_function,
        "existing_transforms": existing_transforms,
        "n_suggestions": n_suggestions,
    }

    params = StdioServerParameters(command="python", args=[SERVER_SCRIPT])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("propose_transforms", args)
            content = result.content[0].text
            data = json.loads(content)

    # If server returned prompt_ready, call LLM directly from client side
    if data.get("status") == "prompt_ready" and data.get("prompt"):
        llm_result = await _call_llm_direct(data["prompt"])
        if llm_result:
            data["status"] = "completed"
            data["suggestions"] = llm_result
            data.pop("error", None)

    return data


async def _call_llm_direct(prompt: str) -> str | None:
    """Call LLM directly from the client side (avoids MCP subprocess network issues)."""
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).parent / ".env")

        anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
        raw_base = os.environ.get("ANTHROPIC_BASE_URL", "").rstrip("/")
        if raw_base.endswith("/v1"):
            base = raw_base[:-3].rstrip("/")
        else:
            base = raw_base
        model = os.environ.get("ILLUSION_MODEL", "claude-opus-4-7")
        max_tokens = int(os.environ.get("ILLUSION_MAX_TOKENS", "2048"))

        if anthropic_key:
            import httpx
            url = f"{base}/v1/messages" if base else "https://api.anthropic.com/v1/messages"
            system = (
                "You are an expert in computational complexity theory and circuit lower bounds. "
                "Propose new transform ideas for the Illusion L2 search system. "
                "Be precise, concise, and grounded in known proof techniques."
            )
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.post(
                    url,
                    headers={
                        "x-api-key": anthropic_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": model,
                        "max_tokens": max_tokens,
                        "system": system,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                for block in data.get("content", []):
                    if isinstance(block, dict) and block.get("type") == "text":
                        return block["text"]

        deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")
        deepseek_base = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        if deepseek_key:
            import openai
            client = openai.AsyncOpenAI(api_key=deepseek_key, base_url=deepseek_base)
            ds_model = os.environ.get("ILLUSION_MODEL", "deepseek-chat")
            response = await client.chat.completions.create(
                model=ds_model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": "You are an expert in computational complexity theory."},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content

    except Exception as e:
        print(f"[_call_llm_direct failed: {e}]", file=sys.stderr)
    return None


def format_suggestions_for_human(result: dict) -> str:
    """Format AI transform suggestions for human review."""
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"L2 EXHAUSTED — AI Transform Suggestions")
    lines.append(f"{'='*60}")
    lines.append(f"Domain:  {result.get('domain', '?')}")
    lines.append(f"Target:  {result.get('target', '?')}")
    lines.append(f"Requested: {result.get('n_suggestions', '?')} suggestions")
    lines.append(f"Status:  {result.get('status', '?')}")
    lines.append(f"{'='*60}")

    if result.get("status") == "completed":
        lines.append("")
        lines.append("SUGGESTIONS (AI-generated, human review required):")
        lines.append("-" * 40)
        lines.append(result.get("suggestions", "(no suggestions returned)"))
        lines.append("-" * 40)
        lines.append("")
        lines.append("NEXT STEPS:")
        lines.append("  1. Review each suggestion for plausibility")
        lines.append("  2. Implement chosen transforms as Python classes")
        lines.append("  3. Add to transform registry")
        lines.append("  4. Run L2 search again")
        lines.append("  5. All new candidates must pass L3 safety check")
    elif result.get("status") == "prompt_ready":
        lines.append("")
        lines.append("No API key configured. Send this prompt manually:")
        lines.append("-" * 40)
        lines.append(result.get("prompt", ""))
        lines.append("-" * 40)
    else:
        lines.append(f"Unexpected status. Raw result: {json.dumps(result, indent=2)}")

    if result.get("error"):
        lines.append(f"\nError: {result['error']}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

_DEMO_EXISTING = [
    {
        "name": "random_restriction_p0.5",
        "delta_collapse": 0.312,
        "l3_verdict": "SAFE",
    },
    {
        "name": "input_permutation",
        "delta_collapse": 0.003,
        "l3_verdict": "rejected_l2",
        "rejection_reason": "low delta",
    },
    {
        "name": "gate_negation",
        "delta_collapse": 0.089,
        "l3_verdict": "UNSAFE",
    },
]


async def main():
    if len(sys.argv) >= 3:
        domain = sys.argv[1]
        target = sys.argv[2]
        existing = json.loads(sys.argv[3]) if len(sys.argv) > 3 else _DEMO_EXISTING
    else:
        # Demo mode
        domain = "AC0 circuits, constant depth, AND/OR/NOT gates"
        target = "PARITY"
        existing = _DEMO_EXISTING
        print("(Demo mode — using AC0/PARITY with sample existing transforms)")

    print(f"Requesting transform suggestions for: {target} in {domain}...")
    result = await propose_new_transforms(domain, target, existing, n_suggestions=2)
    print(format_suggestions_for_human(result))


if __name__ == "__main__":
    asyncio.run(main())
