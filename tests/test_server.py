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
# Copyright protection, if any, is limited to the original human contributions
# and modifications made to this project. The AI-generated portions of the code
# and
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

"""Integration tests for calculator MCP server tools."""

import httpx2
import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from calculator_mcp.server import mcp

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
