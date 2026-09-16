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
from importlib.metadata import PackageNotFoundError, version

from calculator_lib import Calculator
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from calculator_mcp.config import get_homepage, get_timeout

logger = logging.getLogger(__name__)

_HOMEPAGE = get_homepage()
_TIMEOUT = get_timeout()

# Distribution name on PyPI, which differs from the ``calculator_mcp``
# import package name.
_DISTRIBUTION = "calculator-mcp-rubens"

try:
    _VERSION = version(_DISTRIBUTION)
except PackageNotFoundError:  # pragma: no cover - source checkout only
    logger.warning("Distribution %s not installed", _DISTRIBUTION)
    _VERSION = "0.0.0+unknown"

_calc = Calculator()

mcp = FastMCP(
    "Calculator MCP Server",
    version=_VERSION,
    instructions=(
        "This server provides 16 calculator operations as tools. "
        "Use add, subtract, multiply, divide, power, nth_root, modulo, "
        "and floor_divide for two-operand arithmetic. "
        "Use sqrt, absolute, floor, ceil, log10, ln, and exp for "
        "single-operand operations. "
        "Use round_number to round a value to a given number of decimals. "
        "All inputs are floats; division, modulo, and floor_divide raise "
        "ValueError when the divisor is zero."
    ),
    website_url=_HOMEPAGE,
)
logger.info("Initialized Calculator MCP Server")


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
    logger.info("health_check called")
    logger.debug("returning text response: OK")
    return PlainTextResponse("OK")


# --- Two-operand tools ---


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def add(a: float, b: float) -> float:
    """Return the sum of two numbers.

    Args:
        a: The first addend.
        b: The second addend.

    Returns:
        The sum a + b.
    """
    logger.info("add called with a=%s, b=%s", a, b)
    logger.debug("delegating to library Calculator instance: _calc.add")
    return _calc.add(a, b)


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers.

    Args:
        a: The minuend.
        b: The subtrahend.

    Returns:
        The difference a - b.
    """
    logger.info("subtract called with a=%s, b=%s", a, b)
    logger.debug("delegating to library Calculator instance: _calc.subtract")
    return _calc.subtract(a, b)


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def multiply(a: float, b: float) -> float:
    """Return the product of two numbers.

    Args:
        a: The first factor.
        b: The second factor.

    Returns:
        The product a * b.
    """
    logger.info("multiply called with a=%s, b=%s", a, b)
    logger.debug("delegating to library Calculator instance: _calc.multiply")
    return _calc.multiply(a, b)


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def divide(a: float, b: float) -> float:
    """Return the quotient of two numbers.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The quotient a / b.

    Raises:
        ValueError: If b is zero.
    """
    logger.info("divide called with a=%s, b=%s", a, b)
    logger.debug("delegating to library Calculator instance: _calc.divide")
    return _calc.divide(a, b)


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def power(a: float, b: float) -> float:
    """Return a raised to the power b.

    Args:
        a: The base.
        b: The exponent.

    Returns:
        The result of a ** b.
    """
    logger.info("power called with a=%s, b=%s", a, b)
    logger.debug("delegating to library Calculator instance: _calc.power")
    return _calc.power(a, b)


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def nth_root(a: float, b: float) -> float:
    """Return the b-th root of a.

    Args:
        a: The radicand.
        b: The degree of the root.

    Returns:
        The b-th root of a.

    Raises:
        ValueError: If the input is invalid (e.g. even root of negative).
    """
    logger.info("nth_root called with a=%s, b=%s", a, b)
    logger.debug("delegating to library Calculator instance: _calc.nth_root")
    return _calc.nth_root(a, b)


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def modulo(a: float, b: float) -> float:
    """Return a mod b.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The remainder of a / b.

    Raises:
        ValueError: If b is zero.
    """
    logger.info("modulo called with a=%s, b=%s", a, b)
    logger.debug("delegating to library Calculator instance: _calc.modulo")
    return _calc.modulo(a, b)


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def floor_divide(a: float, b: float) -> float:
    """Return floor division of a by b.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The floor of a / b.

    Raises:
        ValueError: If b is zero.
    """
    logger.info("floor_divide called with a=%s, b=%s", a, b)
    logger.debug("delegating to library Calculator instance: _calc.floor_divide")
    return _calc.floor_divide(a, b)


# --- Single-operand tools ---


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def sqrt(a: float) -> float:
    """Return the square root.

    Args:
        a: The value to take the square root of.

    Returns:
        The square root of a.

    Raises:
        ValueError: If a is negative.
    """
    logger.info("sqrt called with a=%s", a)
    return _calc.sqrt(a)


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def absolute(a: float) -> float:
    """Return the absolute value.

    Args:
        a: The input value.

    Returns:
        The absolute value of a.
    """
    logger.info("absolute called with a=%s", a)
    logger.debug("delegating to library Calculator instance: _calc.absolute")
    return _calc.absolute(a)


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def floor(a: float) -> float:
    """Return the floor of a.

    Args:
        a: The input value.

    Returns:
        The largest integer less than or equal to a.
    """
    logger.info("floor called with a=%s", a)
    logger.debug("delegating to library Calculator instance: _calc.floor")
    return _calc.floor(a)


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def ceil(a: float) -> float:
    """Return the ceiling of a.

    Args:
        a: The input value.

    Returns:
        The smallest integer greater than or equal to a.
    """
    logger.info("ceil called with a=%s", a)
    logger.debug("delegating to library Calculator instance: _calc.float")
    return _calc.ceil(a)


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def log10(a: float) -> float:
    """Return the base-10 logarithm.

    Args:
        a: The input value.

    Returns:
        The base-10 logarithm of a.

    Raises:
        ValueError: If a is not positive.
    """
    logger.info("log10 called with a=%s", a)
    logger.debug("delegating to library Calculator instance: _calc.log10")
    return _calc.log10(a)


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def ln(a: float) -> float:
    """Return the natural logarithm.

    Args:
        a: The input value.

    Returns:
        The natural logarithm of a.

    Raises:
        ValueError: If a is not positive.
    """
    logger.info("ln called with a=%s", a)
    logger.debug("delegating to library Calculator instance: _calc.ln")
    return _calc.ln(a)


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def exp(a: float) -> float:
    """Return e raised to the power a.

    Args:
        a: The exponent.

    Returns:
        The value of e ** a.
    """
    logger.info("exp called with a=%s", a)
    logger.debug("delegating to library Calculator instance: _calc.nth_exp")
    return _calc.exp(a)


# --- Round tool ---


@mcp.tool(
    timeout=_TIMEOUT,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def round_number(a: float, decimals: int = 0) -> float:
    """Return a rounded to the given number of decimal places.

    Args:
        a: The value to round.
        decimals: The number of decimal places. Defaults to 0.

    Returns:
        The rounded value.
    """
    logger.info("round_number called with a=%s, decimals=%s", a, decimals)
    logger.debug("delegating to library Calculator instance: _calc.round_number")
    return _calc.round_number(a, decimals)
