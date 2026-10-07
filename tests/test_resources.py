"""Tests for calculator MCP server resources."""

import json
import math

import pytest
from fastmcp import Client
from mcp.shared.exceptions import MCPError
from mcp.types import INVALID_PARAMS

from calculator_mcp.app import mcp


async def test_list_resources():
    async with Client(mcp) as client:
        resources = await client.list_resources()
    assert [str(r.uri) for r in resources] == ["calculator://constants"]


async def test_list_resource_templates():
    async with Client(mcp) as client:
        templates = await client.list_resource_templates()
    assert [t.uri_template for t in templates] == [
        "calculator://operations/{name}"
    ]
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


async def test_read_operation():
    async with Client(mcp) as client:
        contents = await client.read_resource("calculator://operations/add")
    operation = json.loads(contents[0].text)
    assert operation["name"] == "add"
    assert operation["description"].startswith("Return the sum")
    assert operation["inputSchema"]["required"] == ["a", "b"]


async def test_read_unknown_operation():
    uri = "calculator://operations/unknown"
    async with Client(mcp) as client:
        with pytest.raises(MCPError) as error:
            await client.read_resource(uri)
    assert error.value.code == INVALID_PARAMS
    assert error.value.message == f"Resource not found: {uri!r}"
    assert error.value.data == {"uri": uri}
