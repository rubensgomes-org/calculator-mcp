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

"""Unit tests for calculator_mcp.main module."""

from unittest.mock import patch

from calculator_mcp.main import main


def test_main_http_transport():
    with (
        patch("calculator_mcp.main.get_transport", return_value="http"),
        patch("calculator_mcp.main.get_host", return_value="127.0.0.1"),
        patch("calculator_mcp.main.get_port", return_value=9000),
        patch("calculator_mcp.main.mcp") as mock_mcp,
    ):
        main()
    mock_mcp.run.assert_called_once_with(
        transport="http", host="127.0.0.1", port=9000
    )


def test_main_stdio_transport():
    with (
        patch("calculator_mcp.main.get_transport", return_value="stdio"),
        patch("calculator_mcp.main.mcp") as mock_mcp,
    ):
        main()
    mock_mcp.run.assert_called_once_with(transport="stdio")


def test_main_keyboard_interrupt():
    with (
        patch("calculator_mcp.main.get_transport", return_value="stdio"),
        patch("calculator_mcp.main.mcp") as mock_mcp,
    ):
        mock_mcp.run.side_effect = KeyboardInterrupt
        main()
