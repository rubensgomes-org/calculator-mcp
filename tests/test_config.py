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

from calculator_mcp.config import config


@pytest.fixture(autouse=True)
def _clear_caches():
    """Isolate each test from the cached config and logging setup."""
    config.get_config.cache_clear()
    config.configure_logging.cache_clear()
    yield
    config.get_config.cache_clear()
    config.configure_logging.cache_clear()


@pytest.fixture()
def app_config() -> config.AppConfig:
    """Return a minimal ``AppConfig`` with test values."""
    return config.AppConfig.model_validate(
        {
            "server": {
                "host": "127.0.0.1",
                "transport": "http",
                "port": 9000,
                "homepage": "https://example.com",
            },
            "logging": {
                "version": 1,
                "disable_existing_loggers": False,
                "root": {"level": "WARNING"},
            },
        }
    )


@pytest.fixture()
def cfg(app_config):
    """Return a config.yaml mapping built from ``app_config``."""
    return app_config.model_dump()


def _write(tmp_path, mapping):
    """Write ``mapping`` as YAML and return the file path."""
    path = tmp_path / "config.yaml"
    path.write_text(yaml.dump(mapping))
    return path


# --- _resolve_config_path ---


def test_resolve_config_path_uses_env_var(tmp_path, monkeypatch):
    custom = tmp_path / "custom.yaml"
    monkeypatch.setenv("CALCULATORMCP_CONFIG", str(custom))
    # pylint: disable=protected-access
    assert config._resolve_config_path() == custom


def test_resolve_config_path_falls_back_to_package(monkeypatch):
    monkeypatch.delenv("CALCULATORMCP_CONFIG", raising=False)
    # pylint: disable=protected-access
    result = config._resolve_config_path()
    assert result.name == "config.yaml"
    assert "calculator_mcp" in str(result)


# --- load_config ---


def test_load_config(tmp_path, cfg, app_config):
    assert config.load_config(_write(tmp_path, cfg)) == app_config


def test_load_config_ignores_removed_stateless(tmp_path, cfg, app_config):
    cfg["server"]["stateless"] = True
    assert config.load_config(_write(tmp_path, cfg)) == app_config


def test_load_config_accepts_stdio_transport(tmp_path, cfg):
    cfg["server"]["transport"] = "stdio"
    loaded = config.load_config(_write(tmp_path, cfg))
    assert loaded.server.transport == "stdio"


def test_load_config_rejects_invalid_transport(tmp_path, cfg):
    cfg["server"]["transport"] = "sse"
    with pytest.raises(config.ConfigError):
        config.load_config(_write(tmp_path, cfg))


def test_load_config_requires_logging(tmp_path, cfg):
    del cfg["logging"]
    with pytest.raises(config.ConfigError):
        config.load_config(_write(tmp_path, cfg))


@pytest.mark.parametrize("port", [0, 65536])
def test_load_config_rejects_out_of_range_port(tmp_path, cfg, port):
    cfg["server"]["port"] = port
    with pytest.raises(config.ConfigError):
        config.load_config(_write(tmp_path, cfg))


def test_load_config_rejects_missing_file(tmp_path):
    missing = tmp_path / "missing.yaml"
    with pytest.raises(config.ConfigError, match="missing.yaml"):
        config.load_config(missing)


def test_load_config_rejects_invalid_yaml(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("server: [")
    with pytest.raises(config.ConfigError, match="config.yaml"):
        config.load_config(path)


def test_config_is_immutable(app_config):
    with pytest.raises(ValidationError):
        app_config.server.port = 1


def test_bundled_config_is_valid(monkeypatch):
    monkeypatch.delenv("CALCULATORMCP_CONFIG", raising=False)
    assert config.get_config().server.transport == "http"


# --- get_config ---


def test_get_config_loads_once(tmp_path, monkeypatch, cfg):
    monkeypatch.setenv("CALCULATORMCP_CONFIG", str(_write(tmp_path, cfg)))
    first = config.get_config()
    cfg["server"]["port"] = 1234
    _write(tmp_path, cfg)
    assert config.get_config() is first
    assert first.server.port == 9000


# --- configure_logging ---


def test_configure_logging_applies_config(tmp_path, monkeypatch, cfg):
    cfg["logging"]["root"]["level"] = "ERROR"
    monkeypatch.setenv("CALCULATORMCP_CONFIG", str(_write(tmp_path, cfg)))
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
