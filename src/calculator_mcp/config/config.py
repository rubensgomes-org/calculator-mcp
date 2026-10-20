"""Configuration helpers — loads config.yaml and configures logging."""

import functools
import logging
import logging.config
import os
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

logger = logging.getLogger(__name__)

_CONFIG_ENV_VAR = "CALCULATORMCP_CONFIG"
_CONFIG_FILE_NAME = "config.yaml"
_MAX_PORT = 65535


class ConfigError(Exception):
    """Raised when config.yaml cannot be read or is invalid."""


class ServerConfig(BaseModel):
    """The ``server`` section of config.yaml."""

    model_config = ConfigDict(frozen=True)

    host: str
    transport: Literal["http", "stdio"]
    port: int = Field(ge=1, le=_MAX_PORT)


class AppConfig(BaseModel):
    """The full config.yaml; ``logging`` is a ``dictConfig`` mapping."""

    model_config = ConfigDict(frozen=True)

    server: ServerConfig
    logging: dict[str, Any]


@functools.cache
def _resolve_config_path() -> Traversable:
    """Return ``$CALCULATORMCP_CONFIG`` if set, else the bundled config.yaml."""
    env_path = os.environ.get(_CONFIG_ENV_VAR)
    if env_path:
        return Path(env_path)
    return files("calculator_mcp.config").joinpath(_CONFIG_FILE_NAME)


def load_config(path: Traversable) -> AppConfig:
    """Parse and validate the config file at ``path``.

    Raises:
        ConfigError: If the file cannot be read, is not valid YAML, or
            does not match the models.
    """
    try:
        with path.open(encoding="utf-8") as config_file:
            return AppConfig.model_validate(yaml.safe_load(config_file))
    except (
        OSError,
        UnicodeDecodeError,
        yaml.YAMLError,
        ValidationError,
    ) as error:
        raise ConfigError(f"Invalid config file {path}: {error}") from error


@functools.cache
def get_config() -> AppConfig:
    """Return the application config, loaded once on first call."""
    return load_config(_resolve_config_path())


@functools.cache
def configure_logging() -> None:
    """Apply the logging configuration from config.yaml, once.

    Raises:
        ConfigError: If the config is invalid or ``dictConfig`` rejects it.
    """
    logging_config = get_config().logging
    path = _resolve_config_path()
    try:
        logging.config.dictConfig(logging_config)
    except (ValueError, TypeError, AttributeError, ImportError) as error:
        raise ConfigError(
            f"Invalid logging config in {path}: {error}"
        ) from error
    logger.debug("Loaded config from %s", path)
