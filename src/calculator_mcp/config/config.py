"""Configuration helpers — loads config.yaml and configures logging."""

import functools
import logging
import logging.config
import os
from importlib.resources import files
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

logger = logging.getLogger(__name__)


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


def _resolve_config_path() -> Path:
    """Return the config.yaml path.

    Uses the ``CALCULATORMCP_CONFIG`` environment variable when set;
    otherwise falls back to the ``config.yaml`` bundled inside the
    installed package.

    Returns:
        The resolved path to config.yaml.
    """
    env_path = os.environ.get("CALCULATORMCP_CONFIG")
    if env_path:
        return Path(env_path)
    return Path(str(files("calculator_mcp.config").joinpath("config.yaml")))


def load_config(path: Path) -> AppConfig:
    """Parse and validate the config file at ``path``.

    Raises:
        ConfigError: If the file cannot be read, is not valid YAML, or
            does not match the models.
    """
    try:
        with path.open(encoding="utf-8") as config_file:
            return AppConfig.model_validate(yaml.safe_load(config_file))
    except (OSError, yaml.YAMLError, ValidationError) as error:
        raise ConfigError(f"Invalid config file {path}: {error}") from error


@functools.cache
def get_config() -> AppConfig:
    """Return the application config, loaded once on first call."""
    return load_config(_resolve_config_path())


@functools.cache
def configure_logging() -> None:
    """Apply the logging configuration from config.yaml, once."""
    logging.config.dictConfig(get_config().logging)
    logger.debug("Loaded config from %s", _resolve_config_path())
