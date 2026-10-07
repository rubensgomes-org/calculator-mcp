"""Integration tests for calculator MCP server tools."""

import httpx2
import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from calculator_mcp.app import mcp

# --- Two-operand tools ---


async def test_add():
    async with Client(mcp) as client:
        result = await client.call_tool("add", {"a": 2, "b": 3})
    assert result.data == 5.0


async def test_subtract():
    async with Client(mcp) as client:
        result = await client.call_tool("subtract", {"a": 10, "b": 4})
    assert result.data == 6.0


async def test_multiply():
    async with Client(mcp) as client:
        result = await client.call_tool("multiply", {"a": 3, "b": 7})
    assert result.data == 21.0


async def test_divide():
    async with Client(mcp) as client:
        result = await client.call_tool("divide", {"a": 10, "b": 2})
    assert result.data == 5.0


async def test_power():
    async with Client(mcp) as client:
        result = await client.call_tool("power", {"a": 2, "b": 3})
    assert result.data == 8.0


async def test_nth_root():
    async with Client(mcp) as client:
        result = await client.call_tool("nth_root", {"a": 27, "b": 3})
    assert result.data == 3.0


async def test_modulo():
    async with Client(mcp) as client:
        result = await client.call_tool("modulo", {"a": 10, "b": 3})
    assert result.data == 1.0


async def test_floor_divide():
    async with Client(mcp) as client:
        result = await client.call_tool("floor_divide", {"a": 7, "b": 2})
    assert result.data == 3.0


# --- Single-operand tools ---


async def test_sqrt():
    async with Client(mcp) as client:
        result = await client.call_tool("sqrt", {"a": 16})
    assert result.data == 4.0


async def test_absolute():
    async with Client(mcp) as client:
        result = await client.call_tool("absolute", {"a": -5})
    assert result.data == 5.0


async def test_floor():
    async with Client(mcp) as client:
        result = await client.call_tool("floor", {"a": 3.7})
    assert result.data == 3.0


async def test_ceil():
    async with Client(mcp) as client:
        result = await client.call_tool("ceil", {"a": 3.2})
    assert result.data == 4.0


async def test_log10():
    async with Client(mcp) as client:
        result = await client.call_tool("log10", {"a": 100})
    assert result.data == 2.0


async def test_ln():
    async with Client(mcp) as client:
        result = await client.call_tool("ln", {"a": 1})
    assert result.data == 0.0


async def test_exp():
    async with Client(mcp) as client:
        result = await client.call_tool("exp", {"a": 0})
    assert result.data == 1.0


# --- Round tool ---


async def test_round_number():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "round_number", {"a": 3.14159, "decimals": 2}
        )
    assert result.data == 3.14


# --- Error handling ---


async def test_divide_by_zero():
    """Test that division by zero raises an error."""
    async with Client(mcp) as client:
        with pytest.raises(ToolError):
            await client.call_tool("divide", {"a": 1, "b": 0})


@pytest.mark.parametrize(
    ("name", "arguments"),
    [
        ("power", {"a": -8, "b": 0.5}),
        ("multiply", {"a": 1e308, "b": 10}),
        ("exp", {"a": 1000}),
    ],
)
async def test_unrepresentable_result(name, arguments):
    """Test that complex or non-finite results return a tool error."""
    async with Client(mcp) as client:
        with pytest.raises(ToolError):
            await client.call_tool(name, arguments)


# --- Health check ---


async def test_health_check():
    """Test that the /health endpoint returns 200 OK.

    ``mcp.http_app()`` builds the Starlette ASGI application that would
    normally be served by uvicorn in production.  ``httpx2.ASGITransport``
    lets ``httpx2.AsyncClient`` call that ASGI app directly in-process,
    bypassing the network entirely.  This exercises the full HTTP stack
    (routing, middleware, request parsing, response serialization) without
    requiring a running server, an open port, or any network I/O.
    """
    transport = httpx2.ASGITransport(app=mcp.http_app())
    async with httpx2.AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.text == "OK"
