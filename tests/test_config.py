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

import os
from pathlib import Path
from unittest.mock import patch

from calculator_mcp import config

_SAMPLE_CONFIG = {
    "server": {
        "transport": "http",
        "host": "127.0.0.1",
        "port": 9000,
        "timeout": 10,
    },
    "client": {
        "is_oauth": True,
        "url": "http://localhost:9000/mcp",
        "token_dir": "/tmp/tokens",
        "callback_port": 10000,
    },
    "logging": {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {},
        "root": {"level": "WARNING"},
    },
}


def _patch_load(cfg=None):
    """Return a patch for ``config._load_config``."""
    return patch.object(
        config, "_load_config", return_value=cfg or _SAMPLE_CONFIG
    )


# --- _resolve_config_path ---


def test_resolve_config_path_uses_env_var():
    with patch.dict(
        "os.environ", {"CALCULATOR_MCP_CONFIG": "/custom/path.yaml"}
    ):
        # pylint: disable=protected-access
        result = config._resolve_config_path()
    assert result == Path("/custom/path.yaml")


def test_resolve_config_path_falls_back_to_package():
    env = os.environ.copy()
    env.pop("CALCULATOR_MCP_CONFIG", None)
    with patch.dict("os.environ", env, clear=True):
        # pylint: disable=protected-access
        result = config._resolve_config_path()
    assert result.name == "config.yaml"


# --- get_timeout ---


def test_get_timeout():
    with _patch_load():
        assert config.get_timeout() == 10


# --- get_transport ---


def test_get_transport():
    with _patch_load():
        assert config.get_transport() == "http"


def test_get_transport_stdio():
    cfg = {
        **_SAMPLE_CONFIG,
        "server": {**_SAMPLE_CONFIG["server"], "transport": "stdio"},
    }
    with _patch_load(cfg):
        assert config.get_transport() == "stdio"


# --- get_host ---


def test_get_host():
    with _patch_load():
        assert config.get_host() == "127.0.0.1"


# --- get_port ---


def test_get_port():
    with _patch_load():
        assert config.get_port() == 9000


# --- is_oauth ---


def test_is_oauth_true():
    with _patch_load():
        assert config.is_oauth() is True


def test_is_oauth_false():
    cfg = {
        **_SAMPLE_CONFIG,
        "client": {**_SAMPLE_CONFIG["client"], "is_oauth": False},
    }
    with _patch_load(cfg):
        assert config.is_oauth() is False


def test_is_oauth_missing_defaults_false():
    client_no_oauth = {
        k: v for k, v in _SAMPLE_CONFIG["client"].items() if k != "is_oauth"
    }
    cfg = {**_SAMPLE_CONFIG, "client": client_no_oauth}
    with _patch_load(cfg):
        assert config.is_oauth() is False


# --- get_url ---


def test_get_url():
    with _patch_load():
        assert config.get_url() == "http://localhost:9000/mcp"


# --- get_token_dir ---


def test_get_token_dir():
    with _patch_load():
        assert config.get_token_dir() == "/tmp/tokens"


# --- get_callback_port ---


def test_get_callback_port():
    with _patch_load():
        assert config.get_callback_port() == 10000


# --- configure_logging ---


def test_configure_logging():
    with _patch_load(), patch("logging.config.dictConfig") as mock_dict:
        config.configure_logging()
    mock_dict.assert_called_once_with(_SAMPLE_CONFIG["logging"])
