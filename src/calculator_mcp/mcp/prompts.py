"""Reusable prompt templates exposed as MCP prompts on ``prompts``."""

from fastmcp import FastMCP

prompts = FastMCP("Calculator Prompts")


@prompts.prompt
def solve_word_problem(problem: str) -> str:
    """Solve a word problem step by step using the calculator tools.

    Args:
        problem: The word problem to solve.

    Raises:
        ValueError: If problem is blank.
    """
    if not problem.strip():
        raise ValueError("problem must not be blank")
    return (
        "Solve the following problem. Use the calculator tools for every "
        "arithmetic step and show each step. End with the final answer on "
        f"its own line.\n\nProblem: {problem}"
    )
