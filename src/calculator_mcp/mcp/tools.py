"""Calculator operations registered as MCP tools on ``tools``.

Every tool raises ValueError if its result is not a finite real number.
"""

import math
from collections.abc import Callable
from functools import partial

from calculator_lib import Calculator
from fastmcp import FastMCP

_calculator = Calculator()

# Strict validation rejects lax coercions such as JSON true into a number.
tools = FastMCP("Calculator Tools", strict_input_validation=True)

# Shared settings for every calculator tool.
_calculator_tool = partial(
    tools.tool,
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)


def _compute(operation: Callable[..., float | complex], *args: float) -> float:
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
    return _compute(_calculator.add, a, b)


@_calculator_tool
def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers.

    Args:
        a: The minuend.
        b: The subtrahend.

    Returns:
        The difference a - b.
    """
    return _compute(_calculator.subtract, a, b)


@_calculator_tool
def multiply(a: float, b: float) -> float:
    """Return the product of two numbers.

    Args:
        a: The first factor.
        b: The second factor.

    Returns:
        The product a * b.
    """
    return _compute(_calculator.multiply, a, b)


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
    return _compute(_calculator.divide, a, b)


@_calculator_tool
def power(a: float, b: float) -> float:
    """Return a raised to the power b.

    Args:
        a: The base.
        b: The exponent.

    Returns:
        The result of a ** b.

    Raises:
        OverflowError: If the result is too large to represent.
        ZeroDivisionError: If a is zero and b is negative.
    """
    return _compute(_calculator.power, a, b)


@_calculator_tool
def nth_root(a: float, b: float) -> float:
    """Return the b-th root of a.

    Args:
        a: The radicand.
        b: The degree of the root.

    Returns:
        The b-th root of a.

    Raises:
        ValueError: If b is zero, or if a is negative and b is even or
            not an integer.
        ZeroDivisionError: If a is zero and b is negative.
    """
    # Stopgap: calculator_lib returns a real result for a negative a and
    # a fractional b, whose true root is complex.
    if a < 0 and not float(b).is_integer():
        raise ValueError("Cannot take a fractional root of a negative number")
    return _compute(_calculator.nth_root, a, b)


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
    return _compute(_calculator.modulo, a, b)


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
    return _compute(_calculator.floor_divide, a, b)


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
    return _compute(_calculator.sqrt, a)


@_calculator_tool
def absolute(a: float) -> float:
    """Return the absolute value.

    Args:
        a: The input value.

    Returns:
        The absolute value of a.
    """
    return _compute(_calculator.absolute, a)


@_calculator_tool
def floor(a: float) -> float:
    """Return the floor of a.

    Args:
        a: The input value.

    Returns:
        The largest integer less than or equal to a.

    Raises:
        ValueError: If a is NaN.
        OverflowError: If a is infinite.
    """
    return _compute(_calculator.floor, a)


@_calculator_tool
def ceil(a: float) -> float:
    """Return the ceiling of a.

    Args:
        a: The input value.

    Returns:
        The smallest integer greater than or equal to a.

    Raises:
        ValueError: If a is NaN.
        OverflowError: If a is infinite.
    """
    return _compute(_calculator.ceil, a)


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
    return _compute(_calculator.log10, a)


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
    return _compute(_calculator.ln, a)


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
    return _compute(_calculator.exp, a)


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
    return _compute(_calculator.round_number, a, decimals)
