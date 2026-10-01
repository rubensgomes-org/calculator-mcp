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

"""Tests for calculator MCP server resources."""

import json
import math

import pytest
from fastmcp import Client
from mcp.shared.exceptions import MCPError
from mcp.types import INVALID_PARAMS

from calculator_mcp.server import mcp


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
