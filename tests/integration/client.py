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

"""MCP client that connects to the calculator server."""

import asyncio
import logging
import os

from cryptography.fernet import Fernet
from fastmcp import Client
from fastmcp.client.auth import OAuth
from key_value.aio.stores.disk import DiskStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper

from calculator_mcp.config import (
    get_callback_port,
    get_token_dir,
    get_transport,
    get_url,
    is_oauth,
)

logger = logging.getLogger(__name__)


def create_client() -> Client:
    """Create and return an MCP Client based on config.yaml settings.

    Returns:
        A ``fastmcp.Client`` configured for either HTTP or stdio transport,
        depending on the ``client.transport`` value in config.yaml.
    """
    transport = get_transport()

    if transport == "http":
        url = get_url()
        logger.info("Creating HTTP MCP client: %s", url)

        if is_oauth():
            logger.info("OAuth enabled, using OAuthClient")
            token_dir = get_token_dir()
            logger.debug(
                "Creating encrypted disk storage for OAuth tokens: %s",
                token_dir,
            )
            encrypted_storage = FernetEncryptionWrapper(
                key_value=DiskStore(directory=token_dir),
                fernet=Fernet(os.environ["OAUTH_STORAGE_ENCRYPTION_KEY"]),
            )
            oauth = OAuth(
                token_storage=encrypted_storage,
                callback_port=get_callback_port(),
                additional_client_metadata={
                    "token_endpoint_auth_method": "client_secret_post",
                },
            )
            return Client(url, auth=oauth)

        return Client(url)

    logger.info("Creating stdio MCP client")
    return Client("calculator-mcp")


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


async def run_client() -> None:
    """Connect to the MCP server, list and call each tool."""
    client = create_client()

    async with client:
        await client.ping()

        tools = await client.list_tools()
        print(f"Connected — {len(tools)} tools available:\n")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
            args = _SAMPLE_ARGS.get(tool.name, {})
            result = await client.call_tool(tool.name, args)
            print(f"    call_tool({tool.name}, {args}) => {result}\n")


def main() -> None:
    """Entry point for the MCP client."""
    asyncio.run(run_client())


if __name__ == "__main__":
    main()
