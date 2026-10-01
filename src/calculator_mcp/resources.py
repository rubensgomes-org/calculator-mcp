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

"""Calculator reference data exposed as MCP resources on ``resources``."""

import math

from fastmcp import FastMCP
from mcp.shared.exceptions import MCPError
from mcp.types import INVALID_PARAMS

from calculator_mcp.tools import tools

_OPERATIONS_URI = "calculator://operations/{name}"

resources = FastMCP("Calculator Resources")


@resources.resource("calculator://constants", mime_type="application/json")
def constants() -> dict[str, float]:
    """Mathematical constants usable as calculator tool inputs."""
    return {"pi": math.pi, "e": math.e, "tau": math.tau}


# An explicit description keeps the docstring's Args/Raises sections out
# of resources/templates/list.
@resources.resource(
    _OPERATIONS_URI,
    mime_type="application/json",
    description="Describe a calculator operation and its input schema.",
)
async def operation(name: str) -> dict[str, object]:
    """Return the named calculator tool's description and input schema.

    Args:
        name: The calculator tool name, e.g. ``nth_root``.

    Raises:
        MCPError: If no calculator tool has that name, with the same
            ``-32602`` "Resource not found" error FastMCP returns for an
            unknown URI.
    """
    tool = await tools.get_tool(name)
    if tool is None:
        uri = _OPERATIONS_URI.format(name=name)
        raise MCPError(
            code=INVALID_PARAMS,
            message=f"Resource not found: {uri!r}",
            data={"uri": uri},
        )
    return {
        "name": tool.name,
        "description": tool.description,
        "inputSchema": tool.parameters,
    }
