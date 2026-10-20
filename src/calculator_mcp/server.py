"""FastMCP server exposing calculator operations."""

# Horizon requires a server.py module that creates the FastMCP instance.
# Do not rename this file.

import logging
from importlib.metadata import version

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from calculator_mcp import (
    DISTRIBUTION_NAME,
    HOMEPAGE_URL,
    INSTRUCTIONS,
    SERVER_NAME,
)
from calculator_mcp.config import configure_logging, get_config
from calculator_mcp.mcp.prompts import prompts
from calculator_mcp.mcp.resources import resources
from calculator_mcp.mcp.tools import tools

_VERSION = version(DISTRIBUTION_NAME)

# Horizon imports this module directly, bypassing cli.main.
configure_logging()
logger = logging.getLogger(__name__)

mcp = FastMCP(
    SERVER_NAME,
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
    return PlainTextResponse("OK")


def run() -> None:
    """Run the MCP server over the configured transport."""
    server = get_config().server
    if server.transport == "stdio":
        logger.info("Starting stdio MCP server")
        mcp.run(transport="stdio")
        return
    logger.info("Starting http MCP server on %s:%d", server.host, server.port)
    mcp.run(
        transport=server.transport,
        host=server.host,
        port=server.port,
        # Keeps uvicorn from replacing the config.yaml logging.
        uvicorn_config={"log_config": None},
    )
