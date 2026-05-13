"""
L3-MCP Integration: Literature search for UNKNOWN verdicts.

When L3 returns UNKNOWN for a candidate transform, this module calls the
MCP server's search_literature tool to retrieve decidability evidence from
the LLM's knowledge base. The results are presented to the human for final
L3 judgment.

Usage:
    from illusion.mcp.l3_integration import search_for_unknown

    verdict = l3_monitor.check("some_new_transform", description="...")
    if verdict.verdict == "UNKNOWN":
        evidence = await search_for_unknown(verdict)
        # Present evidence to human, human makes final call

Or from CLI:
    python -m illusion.mcp.l3_integration <transform_name> <l1_model> [description]
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("ERROR: mcp package not installed. Run: pip install \"mcp[cli]\"", file=sys.stderr)
    sys.exit(1)


SERVER_SCRIPT = str(Path(__file__).parent / "server.py")

L1_MODEL_MAP = {
    "ac0": "AC0 circuits (constant depth, polynomial size, AND/OR/NOT gates)",
    "monotone": "monotone circuits (AND/OR only, polynomial size)",
    "algebraic": "algebraic circuits (addition/multiplication gates over finite fields)",
}


async def search_for_unknown(
    transform_name: str,
    l1_model: str = "ac0",
    description: str = "",
    l3_question: str = "",
) -> dict:
    """
    Call the MCP server's search_literature tool for an UNKNOWN verdict.

    Args:
        transform_name: Name of the transform that got UNKNOWN
        l1_model: Key from L1_MODEL_MAP or a free-form model description
        description: Natural language description of the transform
        l3_question: The specific decidability question (auto-generated if empty)

    Returns:
        dict with keys: status, evidence (or prompt), transform, l1_model, l3_question
    """
    model_desc = L1_MODEL_MAP.get(l1_model.lower(), l1_model)

    if not l3_question:
        l3_question = (
            f"Can a {model_desc} decide whether a function satisfies "
            f"the property induced by {transform_name}?"
        )

    args = {
        "transform_name": transform_name,
        "transform_description": description,
        "l1_model": model_desc,
        "l3_question": l3_question,
    }

    params = StdioServerParameters(command="python", args=[SERVER_SCRIPT])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("search_literature", args)
            content = result.content[0].text
            return json.loads(content)


def format_evidence_for_human(result: dict) -> str:
    """Format MCP search results for human review."""
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"L3 UNKNOWN — Literature Search Results")
    lines.append(f"{'='*60}")
    lines.append(f"Transform: {result.get('transform', '?')}")
    lines.append(f"L1 Model:  {result.get('l1_model', '?')}")
    lines.append(f"Question:  {result.get('l3_question', '?')}")
    lines.append(f"Status:    {result.get('status', '?')}")
    lines.append(f"{'='*60}")

    if result.get("status") == "completed":
        lines.append("")
        lines.append("EVIDENCE (AI-generated, advisory only):")
        lines.append("-" * 40)
        lines.append(result.get("evidence", "(no evidence returned)"))
        lines.append("-" * 40)
        lines.append("")
        lines.append("NOTE: Human makes the final L3 judgment.")
        lines.append("Options: SAFE / UNSAFE / remain UNKNOWN")
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


async def main():
    if len(sys.argv) < 3:
        print("Usage: python l3_integration.py <transform_name> <l1_model> [description]")
        print(f"  l1_model options: {', '.join(L1_MODEL_MAP.keys())} or free-form")
        sys.exit(1)

    transform_name = sys.argv[1]
    l1_model = sys.argv[2]
    description = sys.argv[3] if len(sys.argv) > 3 else ""

    print(f"Searching literature for: {transform_name} in {l1_model}...")
    result = await search_for_unknown(transform_name, l1_model, description)
    print(format_evidence_for_human(result))


if __name__ == "__main__":
    asyncio.run(main())
