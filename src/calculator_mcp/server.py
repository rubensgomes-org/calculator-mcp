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

"""FastMCP server exposing calculator operations as tools."""

import logging
from collections.abc import AsyncIterator
from importlib.metadata import PackageNotFoundError, version

from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan
from fastmcp.server.middleware.logging import LoggingMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from calculator_mcp.config import configure_logging, get_config
from calculator_mcp.prompts import prompts
from calculator_mcp.resources import resources
from calculator_mcp.tools import tools

# Not __name__: `fastmcp run server.py:mcp` (e.g. Prefect Horizon) loads this
# file as "server_module", which would bypass the calculator_mcp logger config.
logger = logging.getLogger("calculator_mcp.server")

# Distribution name on PyPI, which differs from the ``calculator_mcp``
# import package name.
_DISTRIBUTION = "calculator-mcp-rubens"

# Legacy (session-capable) and modern (sessionless) MCP protocol versions
_MODERN_PROTOCOL = "2026-07-28"
_LEGACY_PROTOCOL = "2025-06-18"

try:
    _VERSION = version(_DISTRIBUTION)
except PackageNotFoundError:  # pragma: no cover - source checkout only
    logger.warning("Distribution %s not installed", _DISTRIBUTION)
    _VERSION = "0.0.0+unknown"


@lifespan
async def _logging_lifespan(
    server: FastMCP,
) -> AsyncIterator[dict[str, object]]:
    """Configure logging on startup, including hosts that skip ``main()``."""
    configure_logging()
    logger.info("Initializing %s %s", server.name, _VERSION)
    logger.info(
        "Serving MCP protocols %s and %s; legacy sessions %s",
        _LEGACY_PROTOCOL,
        _MODERN_PROTOCOL,
        "disabled (stateless)" if get_config().server.stateless else "enabled",
    )
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
    website_url=get_config().server.homepage,
    lifespan=_logging_lifespan,
)

# Logs each inbound MCP message (e.g. initialize, tools/list, tools/call)
# with its JSON-RPC payload and duration, at DEBUG level.
mcp.add_middleware(
    LoggingMiddleware(
        logger=logging.getLogger("calculator_mcp.requests"),
        log_level=logging.DEBUG,
        include_payloads=True,
    )
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
