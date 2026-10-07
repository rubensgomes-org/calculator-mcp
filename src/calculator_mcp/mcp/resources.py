"""Calculator reference data exposed as MCP resources on ``resources``."""

import math

from fastmcp import FastMCP
from mcp.shared.exceptions import MCPError
from mcp.types import INVALID_PARAMS

from calculator_mcp.mcp.tools import tools

_OPERATIONS_URI = "calculator://operations/{name}"

resources = FastMCP("Calculator Resources")


@resources.resource("calculator://constants", mime_type="application/json")
def constants() -> dict[str, float]:
    """Mathematical constants usable as calculator tool inputs."""
    return {"pi": math.pi, "e": math.e, "tau": math.tau}


# An explicit description keeps the docstring's Args/Raises sections out
# of resources/templates/list.
@resources.resource(
    _OPERATIONS_URI,
    mime_type="application/json",
    description="Describe a calculator operation and its input schema.",
)
async def operation(name: str) -> dict[str, object]:
    """Return the named calculator tool's description and input schema.

    Args:
        name: The calculator tool name, e.g. ``nth_root``.

    Raises:
        MCPError: If no calculator tool has that name, with the same
            ``-32602`` "Resource not found" error FastMCP returns for an
            unknown URI.
    """
    tool = await tools.get_tool(name)
    if tool is None:
        uri = _OPERATIONS_URI.format(name=name)
        raise MCPError(
            code=INVALID_PARAMS,
            message=f"Resource not found: {uri!r}",
            data={"uri": uri},
        )
    return {
        "name": tool.name,
        "description": tool.description,
        "inputSchema": tool.parameters,
    }
