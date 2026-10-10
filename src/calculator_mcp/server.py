"""FastMCP server exposing calculator operations."""

# ATTENTION: The Horizon Prefect server environment requires this a "server.py"
# where an FastMCP instance is created. DO NOT rename this file!!!


import logging
from importlib.metadata import version

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from calculator_mcp.config import configure_logging, get_config
from calculator_mcp.mcp.prompts import prompts
from calculator_mcp.mcp.resources import resources
from calculator_mcp.mcp.tools import tools

from . import DISTRIBUTION_NAME, HOMEPAGE_URL, INSTRUCTIONS

_VERSION = version(DISTRIBUTION_NAME)

configure_logging()
logger = logging.getLogger(__name__)

# -------------------------------------------------
# Create the FastMCP mcp instance
# -------------------------------------------------
mcp = FastMCP(
    "Calculator MCP Server",
    version=_VERSION,
    instructions=INSTRUCTIONS,
    website_url=HOMEPAGE_URL,
)

# No namespace, so names and URIs are unchanged.
mcp.mount(tools)
mcp.mount(resources)
mcp.mount(prompts)


@mcp.custom_route("/health", methods=["GET"])
async def health_check(
    request: Request,  # pylint: disable=unused-argument
) -> PlainTextResponse:
    """Return a plain-text health check OK response."""
    logger.debug("health_check called: returning text response: OK")
    return PlainTextResponse("OK")


# -------------------------------------------------
# run() - starts MCP server
# -------------------------------------------------
def run() -> None:
    """Run the MCP server over the configured transport."""
    server = get_config().server
    if server.transport == "stdio":
        logger.info("Starting stdio MCP server")
        mcp.run(transport="stdio")
        return
    logger.info("Starting http MCP server")
    mcp.run(
        transport=server.transport,
        host=server.host,
        port=server.port,
        # Keeps uvicorn from replacing the config.yaml logging.
        uvicorn_config={"log_config": None},
    )
