"""Tests for calculator MCP server prompts."""

from fastmcp import Client

from calculator_mcp.server import mcp


async def test_list_prompts():
    async with Client(mcp) as client:
        prompts = await client.list_prompts()
    assert [p.name for p in prompts] == ["solve_word_problem"]
    assert [a.name for a in prompts[0].arguments or []] == ["problem"]


async def test_get_solve_word_problem():
    async with Client(mcp) as client:
        result = await client.get_prompt(
            "solve_word_problem", {"problem": "What is 2 plus 3?"}
        )
    message = result.messages[0]
    assert message.role == "user"
    assert "Problem: What is 2 plus 3?" in message.content.text
