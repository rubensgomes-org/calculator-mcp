"""MCP client that connects to the calculator server."""

import argparse
import asyncio
import logging
import logging.config
import os
from pathlib import Path
from typing import Any

import yaml
from cryptography.fernet import Fernet
from fastmcp import Client
from fastmcp.client.auth import OAuth
from key_value.aio.stores.filetree import (
    FileTreeStore,
    FileTreeV1CollectionSanitizationStrategy,
    FileTreeV1KeySanitizationStrategy,
)
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from mcp.types import TextContent, TextResourceContents
from pydantic import BaseModel

logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent / "config.yaml"


class ClientConfig(BaseModel):
    """The ``client`` section of config.yaml."""

    url: str
    is_oauth: bool = False
    token_dir: str
    callback_port: int


class IntegrationConfig(BaseModel):
    """The full config.yaml; ``logging`` is a ``dictConfig`` mapping."""

    client: ClientConfig
    logging: dict[str, Any]


def load_config(path: Path = CONFIG_PATH) -> IntegrationConfig:
    """Parse and validate the config file at ``path``.

    Raises:
        pydantic.ValidationError: If the file does not match the models.
    """
    with open(path, encoding="utf-8") as f:
        return IntegrationConfig.model_validate(yaml.safe_load(f))


def create_token_store(token_dir: str) -> FileTreeStore:
    """Create a JSON file store for OAuth tokens under token_dir.

    The sanitization strategies keep OAuth keys, which contain URL
    characters, valid as file and directory names.
    """
    directory = Path(token_dir)
    directory.mkdir(parents=True, exist_ok=True)
    return FileTreeStore(
        data_directory=directory,
        key_sanitization_strategy=FileTreeV1KeySanitizationStrategy(directory),
        collection_sanitization_strategy=(
            FileTreeV1CollectionSanitizationStrategy(directory)
        ),
    )


def create_client(config: ClientConfig) -> Client:
    """Create and return an MCP Client based on config.yaml settings.

    Returns:
        A ``fastmcp.Client`` connected over HTTP to ``config.url``.
    """
    url = config.url
    logger.info("Creating HTTP MCP client: %s", url)

    if config.is_oauth:
        logger.info("OAuth enabled, using OAuthClient")
        token_dir = str(Path(config.token_dir).expanduser())
        logger.debug(
            "Creating encrypted file storage for OAuth tokens: %s",
            token_dir,
        )
        encrypted_storage = FernetEncryptionWrapper(
            key_value=create_token_store(token_dir),
            fernet=Fernet(os.environ["OAUTH_STORAGE_ENCRYPTION_KEY"]),
        )
        oauth = OAuth(
            token_storage=encrypted_storage,
            callback_port=config.callback_port,
            additional_client_metadata={
                "token_endpoint_auth_method": "client_secret_post",
            },
        )
        return Client(url, auth=oauth)

    return Client(url)


_SAMPLE_ARGS: dict[str, dict[str, float | int]] = {
    "add": {"a": 2, "b": 3},
    "subtract": {"a": 10, "b": 4},
    "multiply": {"a": 3, "b": 7},
    "divide": {"a": 15, "b": 4},
    "power": {"a": 2, "b": 8},
    "nth_root": {"a": 27, "b": 3},
    "modulo": {"a": 17, "b": 5},
    "floor_divide": {"a": 17, "b": 5},
    "sqrt": {"a": 16},
    "absolute": {"a": -42},
    "floor": {"a": 3.7},
    "ceil": {"a": 3.2},
    "log10": {"a": 1000},
    "ln": {"a": 2.718281828},
    "exp": {"a": 1},
    "round_number": {"a": 3.14159, "decimals": 2},
}


_SAMPLE_OPERATION_URI = "calculator://operations/add"

_SAMPLE_PROMPT_ARGS = {"problem": "A pizza costs 12.50 split 4 ways."}


def _text(content: object) -> str:
    """Return the text of a text content item, else its ``repr``."""
    if isinstance(content, (TextContent, TextResourceContents)):
        return content.text
    return repr(content)


async def exercise_tools(client: Client) -> None:
    """List and call each tool."""
    tools = await client.list_tools()
    print(f"Connected — {len(tools)} tools available:\n")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
        args = _SAMPLE_ARGS.get(tool.name, {})
        result = await client.call_tool(tool.name, args)
        print(f"    call_tool({tool.name}, {args}) => {result}\n")


async def exercise_resources(client: Client) -> None:
    """List and read each resource, then read a sample template URI."""
    resources = await client.list_resources()
    print(f"{len(resources)} resources available:\n")
    for resource in resources:
        contents = await client.read_resource(resource.uri)
        print(f"  - {resource.uri} => {_text(contents[0])}\n")

    templates = await client.list_resource_templates()
    print(f"{len(templates)} resource templates available:\n")
    for template in templates:
        print(f"  - {template.uri_template}")
    contents = await client.read_resource(_SAMPLE_OPERATION_URI)
    print(f"    read_resource({_SAMPLE_OPERATION_URI}) =>")
    print(f"{_text(contents[0])}\n")


async def exercise_prompts(client: Client) -> None:
    """List and get each prompt."""
    prompts = await client.list_prompts()
    print(f"{len(prompts)} prompts available:\n")
    for prompt in prompts:
        result = await client.get_prompt(prompt.name, _SAMPLE_PROMPT_ARGS)
        print(f"  - {prompt.name}: {prompt.description}")
        print(f"    get_prompt({prompt.name}) =>")
        print(f"{_text(result.messages[0].content)}\n")


async def run_client(config: ClientConfig) -> None:
    """Connect to the MCP server and exercise its tools, resources, and
    prompts."""
    client = create_client(config)

    async with client:
        await exercise_tools(client)
        await exercise_resources(client)
        await exercise_prompts(client)


def parse_config_path() -> Path:
    """Return the config file path given on the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "config",
        nargs="?",
        type=Path,
        default=CONFIG_PATH,
        help=f"config file path (default: {CONFIG_PATH.name})",
    )
    return parser.parse_args().config


def main() -> None:
    """Entry point for the MCP client."""
    config_path = parse_config_path()
    config = load_config(config_path)
    logging.config.dictConfig(config.logging)
    logger.debug("Loaded config from %s", config_path)
    asyncio.run(run_client(config.client))


if __name__ == "__main__":
    main()
