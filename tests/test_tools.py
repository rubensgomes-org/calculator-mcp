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

"""Unit tests for the tool functions in calculator_mcp.server."""

import math

import pytest

from calculator_mcp.server import (
    absolute,
    add,
    ceil,
    divide,
    exp,
    floor,
    floor_divide,
    ln,
    log10,
    modulo,
    multiply,
    nth_root,
    power,
    round_number,
    sqrt,
    subtract,
)

# --- Two-operand tools ---


class TestAdd:
    def test_positive_numbers(self):
        assert add(2, 3) == 5.0

    def test_negative_numbers(self):
        assert add(-2, -3) == -5.0

    def test_zero(self):
        assert add(0, 0) == 0.0

    def test_float_precision(self):
        assert add(0.1, 0.2) == pytest.approx(0.3)


class TestSubtract:
    def test_positive_numbers(self):
        assert subtract(10, 4) == 6.0

    def test_negative_result(self):
        assert subtract(3, 7) == -4.0

    def test_zero(self):
        assert subtract(5, 5) == 0.0


class TestMultiply:
    def test_positive_numbers(self):
        assert multiply(3, 7) == 21.0

    def test_by_zero(self):
        assert multiply(5, 0) == 0.0

    def test_negative_numbers(self):
        assert multiply(-3, -4) == 12.0


class TestDivide:
    def test_even_division(self):
        assert divide(10, 2) == 5.0

    def test_fractional_result(self):
        assert divide(7, 2) == 3.5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError):
            divide(1, 0)


class TestPower:
    def test_square(self):
        assert power(2, 3) == 8.0

    def test_zero_exponent(self):
        assert power(5, 0) == 1.0

    def test_negative_exponent(self):
        assert power(2, -1) == 0.5


class TestNthRoot:
    def test_cube_root(self):
        assert nth_root(27, 3) == pytest.approx(3.0)

    def test_square_root(self):
        assert nth_root(16, 2) == pytest.approx(4.0)


class TestModulo:
    def test_positive(self):
        assert modulo(10, 3) == 1.0

    def test_even_division(self):
        assert modulo(9, 3) == 0.0

    def test_by_zero(self):
        with pytest.raises(ValueError):
            modulo(10, 0)


class TestFloorDivide:
    def test_positive(self):
        assert floor_divide(7, 2) == 3.0

    def test_even_division(self):
        assert floor_divide(6, 3) == 2.0

    def test_by_zero(self):
        with pytest.raises(ValueError):
            floor_divide(7, 0)


# --- Single-operand tools ---


class TestSqrt:
    def test_perfect_square(self):
        assert sqrt(16) == 4.0

    def test_zero(self):
        assert sqrt(0) == 0.0

    def test_negative(self):
        with pytest.raises(ValueError):
            sqrt(-1)


class TestAbsolute:
    def test_negative(self):
        assert absolute(-5) == 5.0

    def test_positive(self):
        assert absolute(5) == 5.0

    def test_zero(self):
        assert absolute(0) == 0.0


class TestFloor:
    def test_positive_fraction(self):
        assert floor(3.7) == 3.0

    def test_negative_fraction(self):
        assert floor(-3.2) == -4.0

    def test_integer(self):
        assert floor(5.0) == 5.0


class TestCeil:
    def test_positive_fraction(self):
        assert ceil(3.2) == 4.0

    def test_negative_fraction(self):
        assert ceil(-3.7) == -3.0

    def test_integer(self):
        assert ceil(5.0) == 5.0


class TestLog10:
    def test_hundred(self):
        assert log10(100) == 2.0

    def test_one(self):
        assert log10(1) == 0.0

    def test_non_positive(self):
        with pytest.raises(ValueError):
            log10(0)


class TestLn:
    def test_one(self):
        assert ln(1) == 0.0

    def test_e(self):
        assert ln(math.e) == pytest.approx(1.0)

    def test_non_positive(self):
        with pytest.raises(ValueError):
            ln(0)


class TestExp:
    def test_zero(self):
        assert exp(0) == 1.0

    def test_one(self):
        assert exp(1) == pytest.approx(math.e)


# --- Round tool ---


class TestRoundNumber:
    def test_two_decimals(self):
        assert round_number(3.14159, 2) == 3.14

    def test_zero_decimals(self):
        assert round_number(3.7, 0) == 4.0

    def test_default_decimals(self):
        assert round_number(3.7) == 4.0
