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

"""Unit tests for calculator_mcp.app.main."""

import os
import subprocess
import sys
from importlib.metadata import version
from unittest.mock import patch

import pytest

from calculator_mcp.app import main
from tests.test_config import app_config  # pylint: disable=unused-import


def _with_server(app_config, **updates):
    """Return ``app_config`` with ``server`` fields replaced by ``updates``."""
    server = app_config.server.model_copy(update=updates)
    return app_config.model_copy(update={"server": server})


def _run_main(app_config):
    """Run ``main([])`` with ``app_config`` and return the mocked server."""
    with (
        patch("calculator_mcp.app.configure_logging"),
        patch("calculator_mcp.app.get_config", return_value=app_config),
        patch("calculator_mcp.app.mcp") as mock_mcp,
    ):
        main([])
    return mock_mcp


def test_main_http_transport(app_config):
    mock_mcp = _run_main(app_config)
    mock_mcp.run.assert_called_once_with(
        transport="http",
        host="127.0.0.1",
        port=9000,
        uvicorn_config={"log_config": None},
    )


def test_main_stdio_transport(app_config):
    mock_mcp = _run_main(_with_server(app_config, transport="stdio"))
    mock_mcp.run.assert_called_once_with(transport="stdio")


def test_main_configures_logging(app_config):
    with (
        patch("calculator_mcp.app.configure_logging") as mock_configure,
        patch("calculator_mcp.app.get_config", return_value=app_config),
        patch("calculator_mcp.app.mcp"),
    ):
        main([])
    mock_configure.assert_called_once_with()


def test_main_keyboard_interrupt(app_config):
    with (
        patch("calculator_mcp.app.configure_logging"),
        patch("calculator_mcp.app.get_config", return_value=app_config),
        patch("calculator_mcp.app.mcp") as mock_mcp,
    ):
        mock_mcp.run.side_effect = KeyboardInterrupt
        main([])


def test_main_version_prints_and_exits(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0
    assert capsys.readouterr().out.strip() == version("calculator-mcp-rubens")


def test_main_exits_on_invalid_config(tmp_path):
    missing = tmp_path / "missing.yaml"
    env = {**os.environ, "CALCULATORMCP_CONFIG": str(missing)}
    result = subprocess.run(
        [sys.executable, "-m", "calculator_mcp.app"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert result.returncode == 1
    assert result.stderr.startswith(
        f"calculator-mcp: Invalid config file {missing}"
    )
