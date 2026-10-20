"""Tests for calculator MCP server resources."""

import json
import math

import pytest
from fastmcp import Client
from mcp.shared.exceptions import MCPError
from mcp.types import INVALID_PARAMS

from calculator_mcp.mcp.tools import tools
from calculator_mcp.server import mcp

_JSON = "application/json"


async def test_list_resources():
    async with Client(mcp) as client:
        resources = await client.list_resources()
    assert {str(r.uri): r.mime_type for r in resources} == {
        "calculator://constants": _JSON,
        "calculator://operations": _JSON,
    }


async def test_list_resource_templates():
    async with Client(mcp) as client:
        templates = await client.list_resource_templates()
    assert [t.uri_template for t in templates] == [
        "calculator://operations/{name}"
    ]
    assert templates[0].mime_type == _JSON
    assert templates[0].description == (
        "Describe a calculator operation and its input schema."
    )


async def test_read_constants():
    async with Client(mcp) as client:
        contents = await client.read_resource("calculator://constants")
    assert json.loads(contents[0].text) == {
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
    }


async def test_read_operations():
    async with Client(mcp) as client:
        contents = await client.read_resource("calculator://operations")
    names = json.loads(contents[0].text)
    assert names == sorted(tool.name for tool in await tools.list_tools())
    assert "add" in names


async def test_read_operation():
    async with Client(mcp) as client:
        contents = await client.read_resource("calculator://operations/add")
    operation = json.loads(contents[0].text)
    assert operation["name"] == "add"
    assert operation["description"].startswith("Return the sum")
    assert operation["inputSchema"]["required"] == ["a", "b"]


async def test_every_tool_is_readable_as_operation():
    async with Client(mcp) as client:
        for tool in await client.list_tools():
            uri = f"calculator://operations/{tool.name}"
            contents = await client.read_resource(uri)
            assert json.loads(contents[0].text)["name"] == tool.name


async def test_read_unknown_operation():
    uri = "calculator://operations/unknown"
    async with Client(mcp) as client:
        with pytest.raises(MCPError) as error:
            await client.read_resource(uri)
    assert error.value.code == INVALID_PARAMS
    assert error.value.message == f"Resource not found: {uri!r}"
    assert error.value.data == {"uri": uri}
