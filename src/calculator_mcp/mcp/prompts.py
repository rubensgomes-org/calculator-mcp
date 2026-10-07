"""Reusable prompt templates exposed as MCP prompts on ``prompts``."""

from fastmcp import FastMCP

prompts = FastMCP("Calculator Prompts")


@prompts.prompt
def solve_word_problem(problem: str) -> str:
    """Solve a word problem step by step using the calculator tools.

    Args:
        problem: The word problem to solve.
    """
    return (
        "Solve the following problem. Use the calculator tools for every "
        f"arithmetic step and show each step.\n\nProblem: {problem}"
    )
