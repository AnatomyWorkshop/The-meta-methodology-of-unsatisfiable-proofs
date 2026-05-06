"""
Integration test for the Illusion MCP server.

Tests:
  1. Server starts without error
  2. list_tools returns both expected tools with correct schemas
  3. propose_transforms returns a prompt_ready response
  4. search_literature returns a prompt_ready response

Run from the project root:
  python neural-symbolic-system/illusion/mcp/test_server.py

Requires: pip install "mcp[cli]"
"""

import asyncio
import json
import sys
from pathlib import Path

# Allow running from project root or from mcp/ directory
sys.path.insert(0, str(Path(__file__).parent))

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print(
        "ERROR: mcp package not installed.\n"
        "Run: pip install \"mcp[cli]\"",
        file=sys.stderr,
    )
    sys.exit(1)


SERVER_SCRIPT = str(Path(__file__).parent / "server.py")

PROPOSE_ARGS = {
    "domain": "AC0 circuits, constant depth, AND/OR/NOT gates",
    "target_function": "PARITY",
    "existing_transforms": [
        {
            "name": "random_restriction_p0.5",
            "delta_collapse": 0.312,
            "l3_verdict": "SAFE",
        },
        {
            "name": "identity",
            "delta_collapse": -0.002,
            "l3_verdict": "rejected_l2",
            "rejection_reason": "low delta",
        },
    ],
    "n_suggestions": 2,
}

SEARCH_ARGS = {
    "transform_name": "gate_elevation",
    "transform_description": "Replace AND gates with OR gates in a random subset of depth-1 gates.",
    "l1_model": "monotone circuits",
    "l3_question": (
        "Can a monotone circuit decide whether a function satisfies "
        "the property induced by gate_elevation?"
    ),
}


async def run_tests():
    params = StdioServerParameters(command="python", args=[SERVER_SCRIPT])
    passed = 0
    failed = 0

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Test 1: list_tools
            tools_result = await session.list_tools()
            tool_names = {t.name for t in tools_result.tools}
            expected = {"propose_transforms", "search_literature"}
            if expected == tool_names:
                print(f"[PASS] list_tools: {tool_names}")
                passed += 1
            else:
                print(f"[FAIL] list_tools: expected {expected}, got {tool_names}")
                failed += 1

            # Test 2: propose_transforms schema fields
            pt = next((t for t in tools_result.tools if t.name == "propose_transforms"), None)
            required = set(pt.inputSchema.get("required", []))
            if required == {"domain", "target_function", "existing_transforms"}:
                print("[PASS] propose_transforms schema required fields correct")
                passed += 1
            else:
                print(f"[FAIL] propose_transforms required fields: {required}")
                failed += 1

            # Test 3: call propose_transforms
            result = await session.call_tool("propose_transforms", PROPOSE_ARGS)
            content = result.content[0].text
            data = json.loads(content)
            if data.get("status") == "prompt_ready" and "prompt" in data:
                print("[PASS] propose_transforms returns prompt_ready with prompt")
                passed += 1
                # Spot-check prompt contains domain
                if "AC0" in data["prompt"] or "AC⁰" in data["prompt"]:
                    print("[PASS] propose_transforms prompt contains domain context")
                    passed += 1
                else:
                    print("[FAIL] propose_transforms prompt missing domain context")
                    failed += 1
            else:
                print(f"[FAIL] propose_transforms unexpected response: {data}")
                failed += 1

            # Test 4: call search_literature
            result = await session.call_tool("search_literature", SEARCH_ARGS)
            content = result.content[0].text
            data = json.loads(content)
            if data.get("status") == "prompt_ready" and "prompt" in data:
                print("[PASS] search_literature returns prompt_ready with prompt")
                passed += 1
                if "gate_elevation" in data["prompt"]:
                    print("[PASS] search_literature prompt contains transform name")
                    passed += 1
                else:
                    print("[FAIL] search_literature prompt missing transform name")
                    failed += 1
            else:
                print(f"[FAIL] search_literature unexpected response: {data}")
                failed += 1

    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    ok = asyncio.run(run_tests())
    sys.exit(0 if ok else 1)
