"""Unit tests for calculator_mcp.cli.main."""

import os
import subprocess
import sys
from importlib.metadata import version
from unittest.mock import patch

import pytest

from calculator_mcp import DISTRIBUTION_NAME
from calculator_mcp.cli import main
from tests.test_config import app_config  # pylint: disable=unused-import


def _with_server(app_config, **updates):
    """Return ``app_config`` with ``server`` fields replaced by ``updates``."""
    server = app_config.server.model_copy(update=updates)
    return app_config.model_copy(update={"server": server})


def _run_main(app_config):
    """Run ``main([])`` with ``app_config`` and return the mocked server."""
    with (
        patch("calculator_mcp.cli.configure_logging"),
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
        patch("calculator_mcp.cli.configure_logging") as mock_configure,
        patch("calculator_mcp.app.get_config", return_value=app_config),
        patch("calculator_mcp.app.mcp"),
    ):
        main([])
    mock_configure.assert_called_once_with()


def test_main_keyboard_interrupt(app_config):
    with (
        patch("calculator_mcp.cli.configure_logging"),
        patch("calculator_mcp.app.get_config", return_value=app_config),
        patch("calculator_mcp.app.mcp") as mock_mcp,
    ):
        mock_mcp.run.side_effect = KeyboardInterrupt
        assert main([]) == 130


def test_main_version_prints_and_exits(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0
    assert capsys.readouterr().out.strip() == (
        f"{DISTRIBUTION_NAME} {version(DISTRIBUTION_NAME)}"
    )


def test_main_exits_on_invalid_config(tmp_path):
    missing = tmp_path / "missing.yaml"
    env = {**os.environ, "CALCULATORMCP_CONFIG": str(missing)}
    result = subprocess.run(
        [sys.executable, "-m", "calculator_mcp"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert result.returncode == 1
    assert result.stderr.startswith(
        f"{DISTRIBUTION_NAME}: Invalid config file {missing}"
    )
