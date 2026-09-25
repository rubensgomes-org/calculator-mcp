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

import functools
import logging
import logging.config
import os
from importlib.resources import files
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ServerConfig(BaseModel):
    """The ``server`` section of config.yaml."""

    host: str
    transport: Literal["http"]
    port: int
    timeout: int
    stateless: bool = False
    homepage: str


class ClientConfig(BaseModel):
    """The ``client`` section of config.yaml."""

    url: str
    is_oauth: bool = False
    token_dir: str
    callback_port: int


class AppConfig(BaseModel):
    """The full config.yaml; ``logging`` is a ``dictConfig`` mapping."""

    server: ServerConfig
    client: ClientConfig
    logging: dict[str, Any]


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


def load_config(path: Path) -> AppConfig:
    """Parse and validate the config file at ``path``.

    Raises:
        pydantic.ValidationError: If the file does not match the models.
    """
    with open(path, encoding="utf-8") as f:
        return AppConfig.model_validate(yaml.safe_load(f))


@functools.cache
def get_config() -> AppConfig:
    """Return the application config, loaded once on first call."""
    return load_config(_resolve_config_path())


@functools.cache
def configure_logging() -> None:
    """Apply the logging configuration from config.yaml, once."""
    logging.config.dictConfig(get_config().logging)
    logger.debug("Loaded config from %s", _resolve_config_path())
