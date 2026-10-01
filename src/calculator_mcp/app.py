# General Disclaimer
#
# **AI Generated Content**
#
# This project's source code and documentation were generated predominantly
# by an Artificial Intelligence Large Language Model (AI LLM). The project
# lead, [Rubens Gomes](https://rubensgomes.com), provided initial prompts,
# reviewed, and made refinements to the generated output. While human review and
# refinement have occurred, users should be aware that the output may contain
# inaccuracies, errors, or security vulnerabilities
#
# **Third-Party Content Notice**
#
# This software may include components or snippets derived from third-party
# sources. The software's users and distributors are responsible for ensuring
# compliance with any underlying licenses applicable to such components.
#
# **Copyright Status Statement**
#
# Copyright protection, if any, is limited to the original
# human contributions and modifications made to this project.
# The AI-generated portions of the code and
# documentation are not subject to copyright and are considered to be in the
# public domain.
#
# **Limitation of liability**
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR
# OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
#
# **No-Warranty Disclaimer**
#
# THIS SOFTWARE IS PROVIDED 'AS IS,' WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT.

"""FastMCP server exposing calculator operations, and its CLI entry point."""

import argparse
import logging
from collections.abc import AsyncIterator
from importlib.metadata import PackageNotFoundError, metadata

from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from calculator_mcp.config import ConfigError, configure_logging, get_config
from calculator_mcp.config.config import ServerConfig
from calculator_mcp.mcp.prompts import prompts
from calculator_mcp.mcp.resources import resources
from calculator_mcp.mcp.tools import tools

# Not __name__: `fastmcp run app.py:mcp` (e.g. Prefect Horizon) loads this
# file as "server_module", which would bypass the calculator_mcp logger config.
logger = logging.getLogger("calculator_mcp.app")

# Distribution name on PyPI, which differs from the ``calculator_mcp``
# import package name.
_DISTRIBUTION = "calculator-mcp-rubens"
_UNKNOWN_VERSION = "0.0.0+unknown"


def _package_info() -> tuple[str, str | None]:
    """Return the installed version and ``[project.urls]`` homepage."""
    try:
        package_metadata = metadata(_DISTRIBUTION)
    except PackageNotFoundError:  # pragma: no cover - source checkout only
        logger.warning("Distribution %s not installed", _DISTRIBUTION)
        return _UNKNOWN_VERSION, None
    for entry in package_metadata.get_all("Project-URL") or []:
        label, _, url = entry.partition(", ")
        if label == "Homepage":
            return package_metadata["Version"], url
    return package_metadata["Version"], None


_VERSION, _HOMEPAGE = _package_info()


# The following code supports `fastmcp run app.py:mcp` and Prefect Horizon.
# Those hosts load app.py and start `mcp` themselves, so they never call
# main(). This lifespan is the only place logging gets configured for them,
# and without it they would run with FastMCP's default logging.
@lifespan
async def _logging_lifespan(
    server: FastMCP,
) -> AsyncIterator[dict[str, object]]:
    """Configure logging on startup, including hosts that skip ``main()``."""
    configure_logging()
    logger.info("Initializing %s %s", server.name, _VERSION)
    yield {}


mcp = FastMCP(
    "Calculator MCP Server",
    version=_VERSION,
    instructions=(
        "This server provides calculator operations as tools, covering "
        "arithmetic, powers and roots, logarithms, and rounding. "
        "All inputs are floats. Invalid inputs, or results that are not "
        "finite real numbers, raise ValueError. Results too large to "
        "represent raise OverflowError, and zero raised to a negative "
        "power raises ZeroDivisionError."
    ),
    website_url=_HOMEPAGE,
    lifespan=_logging_lifespan,
)

# No namespace, so names and URIs are unchanged.
mcp.mount(tools)
mcp.mount(resources)
mcp.mount(prompts)


@mcp.custom_route("/health", methods=["GET"])
async def health_check(
    request: Request,  # pylint: disable=unused-argument
) -> PlainTextResponse:
    """Return a plain-text health-check response.

    Args:
        request: The incoming HTTP request.

    Returns:
        A ``PlainTextResponse`` with body ``"OK"``.
    """
    logger.debug("health_check called: returning text response: OK")
    return PlainTextResponse("OK")


# -------------------------------------------------
# main() and related functions
# -------------------------------------------------
def _run_server(server: ServerConfig) -> None:
    """Run the MCP server over the configured transport."""
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


def main(argv: list[str] | None = None) -> None:
    """Entry point for the calculator-mcp application."""
    parser = argparse.ArgumentParser(prog="calculator-mcp")
    parser.add_argument("--version", action="version", version=_VERSION)
    parser.parse_args(argv)
    try:
        configure_logging()
    except ConfigError as error:
        # Logging is not configured, so report on stderr and exit.
        raise SystemExit(f"calculator-mcp: {error}") from error

    try:
        _run_server(get_config().server)
    except KeyboardInterrupt:
        logger.info("Received SIGINT, shutting down gracefully")


if __name__ == "__main__":
    main()
