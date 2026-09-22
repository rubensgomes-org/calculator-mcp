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

"""Configuration helpers — loads config.yaml and configures logging."""

import logging
import logging.config
import os
from importlib.resources import files
from pathlib import Path

import yaml


def _resolve_config_path() -> Path:
    """Return the config.yaml path.

    Uses the ``CALCULATOR_MCP_CONFIG`` environment variable when set;
    otherwise falls back to the ``config.yaml`` bundled inside the
    installed package.

    Returns:
        The resolved path to config.yaml.
    """
    env_path = os.environ.get("CALCULATOR_MCP_CONFIG")
    if env_path:
        return Path(env_path)
    return Path(str(files("calculator_mcp").joinpath("config.yaml")))


_CONFIG_PATH = _resolve_config_path()


def _load_config() -> dict:
    """Load and return the full config.yaml as a dict.

    Returns:
        The parsed YAML configuration.
    """
    with open(_CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def configure_logging() -> None:
    """Apply the logging configuration from config.yaml."""
    config = _load_config()
    logging.config.dictConfig(config["logging"])


configure_logging()

logger = logging.getLogger(__name__)


def get_timeout() -> int:
    """Return the HTTP client timeout (seconds) from config.yaml.

    Returns:
        The timeout in seconds.
    """
    config = _load_config()
    timeout: int = config["server"]["timeout"]
    logger.info("HTTP client timeout: %s seconds", timeout)
    return timeout


def get_homepage() -> str:
    """Return the project homepage URL from config.yaml.

    Returns:
        The homepage URL string.
    """
    config = _load_config()
    homepage: str = config["server"]["homepage"]
    logger.info("Project homepage: %s", homepage)
    return homepage


def get_transport() -> str:
    """Return the MCP transport type ('stdio' or 'http') from config.yaml.

    Returns:
        The transport type string.
    """
    config = _load_config()
    transport: str = config["server"]["transport"]
    logger.info("MCP transport: %s", transport)
    return transport


def get_host() -> str:
    """Return the HTTP/MCP server host address from config.yaml.

    Returns:
        The host address string.
    """
    config = _load_config()
    host: str = config["server"]["host"]
    logger.info("MCP host: %s", host)
    return host


def get_port() -> int:
    """Return the HTTP/MCP server port from config.yaml.

    Returns:
        The port number.
    """
    config = _load_config()
    port: int = config["server"]["port"]
    logger.info("MCP port: %s", port)
    return port


def get_stateless() -> bool:
    """Return whether stateless HTTP mode is enabled from config.yaml.

    Returns:
        True if the server stateless setting is true, False otherwise.
    """
    config = _load_config()
    stateless: bool = config["server"].get("stateless", False)
    logger.info("MCP stateless HTTP: %s", stateless)
    return stateless


def is_oauth() -> bool:
    """Return whether OAuth is enabled from config.yaml.

    Returns:
        True if the client is_oauth setting is true, False otherwise.
    """
    config = _load_config()
    oauth: bool = config["client"].get("is_oauth", False)
    logger.info("OAuth enabled: %s", oauth)
    return oauth


def get_url() -> str:
    """Return the client URL for HTTP transport from config.yaml.

    Returns:
        The client URL string.
    """
    config = _load_config()
    url: str = config["client"]["url"]
    logger.info("MCP client URL: %s", url)
    return url


def get_token_dir() -> str:
    """Return the OAuth token directory from config.yaml.

    Returns:
        The token directory path string.
    """
    config = _load_config()
    token_dir: str = str(Path(config["client"]["token_dir"]).expanduser())
    logger.info("OAuth token directory: %s", token_dir)
    return token_dir


def get_callback_port() -> int:
    """Return the OAuth callback server port from config.yaml.

    Returns:
        The callback port number.
    """
    config = _load_config()
    port: int = config["client"]["callback_port"]
    logger.info("OAuth callback port: %s", port)
    return port
