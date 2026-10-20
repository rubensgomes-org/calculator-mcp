"""Tests for calculator MCP server prompts."""

import pytest
from fastmcp import Client
from mcp.shared.exceptions import MCPError

from calculator_mcp.server import mcp


async def test_list_prompts():
    async with Client(mcp) as client:
        prompts = await client.list_prompts()
    assert [p.name for p in prompts] == ["solve_word_problem"]
    prompt = prompts[0]
    assert prompt.description == (
        "Solve a word problem step by step using the calculator tools."
    )
    arguments = prompt.arguments or []
    assert [(a.name, a.description, a.required) for a in arguments] == [
        ("problem", "The word problem to solve.", True)
    ]


async def test_get_solve_word_problem():
    async with Client(mcp) as client:
        result = await client.get_prompt(
            "solve_word_problem", {"problem": "What is 2 plus 3?"}
        )
    message = result.messages[0]
    assert message.role == "user"
    text = message.content.text
    assert "Use the calculator tools for every arithmetic step" in text
    assert "final answer on its own line" in text
    assert text.endswith("Problem: What is 2 plus 3?")


@pytest.mark.parametrize(
    "arguments",
    [{}, {"problem": ""}, {"problem": "  "}],
    ids=["missing", "empty", "blank"],
)
async def test_get_solve_word_problem_rejects_invalid_problem(arguments):
    async with Client(mcp) as client:
        with pytest.raises(MCPError):
            await client.get_prompt("solve_word_problem", arguments)
