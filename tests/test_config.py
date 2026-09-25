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

"""Unit tests for calculator_mcp.config module."""

import logging
from unittest.mock import patch

import pytest
import yaml
from pydantic import ValidationError

from calculator_mcp import config


@pytest.fixture(autouse=True)
def _clear_caches():
    """Isolate each test from the cached config and logging setup."""
    config.get_config.cache_clear()
    config.configure_logging.cache_clear()
    yield
    config.get_config.cache_clear()
    config.configure_logging.cache_clear()


@pytest.fixture()
def cfg(app_config):
    """Return a config.yaml mapping built from the shared fixture."""
    return app_config.model_dump()


def _write(tmp_path, mapping):
    """Write ``mapping`` as YAML and return the file path."""
    path = tmp_path / "config.yaml"
    path.write_text(yaml.dump(mapping))
    return path


# --- _resolve_config_path ---


def test_resolve_config_path_uses_env_var(tmp_path, monkeypatch):
    custom = tmp_path / "custom.yaml"
    monkeypatch.setenv("CALCULATOR_MCP_CONFIG", str(custom))
    # pylint: disable=protected-access
    assert config._resolve_config_path() == custom


def test_resolve_config_path_falls_back_to_package(monkeypatch):
    monkeypatch.delenv("CALCULATOR_MCP_CONFIG", raising=False)
    # pylint: disable=protected-access
    result = config._resolve_config_path()
    assert result.name == "config.yaml"
    assert "calculator_mcp" in str(result)


# --- load_config ---


def test_load_config(tmp_path, cfg, app_config):
    assert config.load_config(_write(tmp_path, cfg)) == app_config


def test_load_config_defaults(tmp_path, cfg):
    del cfg["server"]["stateless"]
    del cfg["client"]["is_oauth"]
    loaded = config.load_config(_write(tmp_path, cfg))
    assert loaded.server.stateless is False
    assert loaded.client.is_oauth is False


def test_load_config_rejects_invalid_transport(tmp_path, cfg):
    cfg["server"]["transport"] = "stdio"
    with pytest.raises(ValidationError):
        config.load_config(_write(tmp_path, cfg))


def test_load_config_requires_logging(tmp_path, cfg):
    del cfg["logging"]
    with pytest.raises(ValidationError):
        config.load_config(_write(tmp_path, cfg))


def test_bundled_config_is_valid(monkeypatch):
    monkeypatch.delenv("CALCULATOR_MCP_CONFIG", raising=False)
    assert config.get_config().server.transport == "http"


# --- get_config ---


def test_get_config_loads_once(tmp_path, monkeypatch, cfg):
    monkeypatch.setenv("CALCULATOR_MCP_CONFIG", str(_write(tmp_path, cfg)))
    first = config.get_config()
    cfg["server"]["port"] = 1234
    _write(tmp_path, cfg)
    assert config.get_config() is first
    assert first.server.port == 9000


# --- configure_logging ---


def test_configure_logging_applies_config(tmp_path, monkeypatch, cfg):
    cfg["logging"]["root"]["level"] = "ERROR"
    monkeypatch.setenv("CALCULATOR_MCP_CONFIG", str(_write(tmp_path, cfg)))
    root = logging.getLogger()
    original_level = root.level
    try:
        config.configure_logging()
        assert root.level == logging.ERROR
    finally:
        root.setLevel(original_level)


def test_configure_logging_runs_once(app_config):
    with (
        patch.object(config, "get_config", return_value=app_config),
        patch("logging.config.dictConfig") as mock_dict_config,
    ):
        config.configure_logging()
        config.configure_logging()
    mock_dict_config.assert_called_once_with(app_config.logging)
