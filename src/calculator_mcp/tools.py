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

"""Calculator operations registered as MCP tools on ``tools``."""

import math
from collections.abc import Callable
from functools import partial

from calculator_lib import Calculator
from fastmcp import FastMCP

_calc = Calculator()

tools = FastMCP("Calculator Tools")

# Shared settings for every calculator tool.
_calculator_tool = partial(
    tools.tool,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)


def _compute(operation: Callable[..., float], *args: float) -> float:
    """Run ``operation`` and return its result as a finite float.

    Raises:
        ValueError: If the result is complex, infinite, or NaN, none of
            which JSON can represent as a number.
    """
    result = operation(*args)
    if isinstance(result, complex):
        raise ValueError(f"Result is not a real number: {result}")
    real_result = float(result)
    if not math.isfinite(real_result):
        raise ValueError(f"Result is not finite: {real_result}")
    return real_result


# --- Two-operand tools ---


@_calculator_tool
def add(a: float, b: float) -> float:
    """Return the sum of two numbers.

    Args:
        a: The first addend.
        b: The second addend.

    Returns:
        The sum a + b.
    """
    return _compute(_calc.add, a, b)


@_calculator_tool
def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers.

    Args:
        a: The minuend.
        b: The subtrahend.

    Returns:
        The difference a - b.
    """
    return _compute(_calc.subtract, a, b)


@_calculator_tool
def multiply(a: float, b: float) -> float:
    """Return the product of two numbers.

    Args:
        a: The first factor.
        b: The second factor.

    Returns:
        The product a * b.
    """
    return _compute(_calc.multiply, a, b)


@_calculator_tool
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
    return _compute(_calc.divide, a, b)


@_calculator_tool
def power(a: float, b: float) -> float:
    """Return a raised to the power b.

    Args:
        a: The base.
        b: The exponent.

    Returns:
        The result of a ** b.

    Raises:
        ValueError: If the result is not a finite real number.
        OverflowError: If the result is too large to represent.
        ZeroDivisionError: If a is zero and b is negative.
    """
    return _compute(_calc.power, a, b)


@_calculator_tool
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
    return _compute(_calc.nth_root, a, b)


@_calculator_tool
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
    return _compute(_calc.modulo, a, b)


@_calculator_tool
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
    return _compute(_calc.floor_divide, a, b)


# --- Single-operand tools ---


@_calculator_tool
def sqrt(a: float) -> float:
    """Return the square root.

    Args:
        a: The value to take the square root of.

    Returns:
        The square root of a.

    Raises:
        ValueError: If a is negative.
    """
    return _compute(_calc.sqrt, a)


@_calculator_tool
def absolute(a: float) -> float:
    """Return the absolute value.

    Args:
        a: The input value.

    Returns:
        The absolute value of a.
    """
    return _compute(_calc.absolute, a)


@_calculator_tool
def floor(a: float) -> float:
    """Return the floor of a.

    Args:
        a: The input value.

    Returns:
        The largest integer less than or equal to a.
    """
    return _compute(_calc.floor, a)


@_calculator_tool
def ceil(a: float) -> float:
    """Return the ceiling of a.

    Args:
        a: The input value.

    Returns:
        The smallest integer greater than or equal to a.
    """
    return _compute(_calc.ceil, a)


@_calculator_tool
def log10(a: float) -> float:
    """Return the base-10 logarithm.

    Args:
        a: The input value.

    Returns:
        The base-10 logarithm of a.

    Raises:
        ValueError: If a is not positive.
    """
    return _compute(_calc.log10, a)


@_calculator_tool
def ln(a: float) -> float:
    """Return the natural logarithm.

    Args:
        a: The input value.

    Returns:
        The natural logarithm of a.

    Raises:
        ValueError: If a is not positive.
    """
    return _compute(_calc.ln, a)


@_calculator_tool
def exp(a: float) -> float:
    """Return e raised to the power a.

    Args:
        a: The exponent.

    Returns:
        The value of e ** a.

    Raises:
        OverflowError: If the result is too large to represent.
    """
    return _compute(_calc.exp, a)


# --- Round tool ---


@_calculator_tool
def round_number(a: float, decimals: int = 0) -> float:
    """Return a rounded to the given number of decimal places.

    Args:
        a: The value to round.
        decimals: The number of decimal places. Defaults to 0.

    Returns:
        The rounded value.
    """
    return _compute(_calc.round_number, a, decimals)
