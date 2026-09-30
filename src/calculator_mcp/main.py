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

"""CLI entry point for the calculator-mcp server."""

import argparse
import logging
from importlib.metadata import version

from calculator_mcp.config import configure_logging, get_config
from calculator_mcp.server import mcp

logger = logging.getLogger(__name__)

# name available and used to push this package to PyPI
_DISTRIBUTION_NAME = "calculator-mcp-rubens"


def main(argv: list[str] | None = None) -> None:
    """Entry point for the calculator-mcp application."""
    parser = argparse.ArgumentParser(prog="calculator-mcp")
    parser.add_argument(
        "--version",
        action="version",
        version=version(_DISTRIBUTION_NAME),
    )
    parser.parse_args(argv)
    configure_logging()

    server = get_config().server
    try:
        mcp.run(
            transport=server.transport,
            host=server.host,
            port=server.port,
            stateless_http=server.stateless,
            # Keeps uvicorn from replacing the config.yaml logging.
            uvicorn_config={"log_config": None},
        )
    except KeyboardInterrupt:
        logger.info("Received SIGINT, shutting down gracefully")


if __name__ == "__main__":
    main()
