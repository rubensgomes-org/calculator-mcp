"""Command-line entry point."""

import argparse
import logging
from importlib.metadata import metadata, version

from calculator_mcp import DISTRIBUTION_NAME
from calculator_mcp.config import ConfigError, configure_logging

# Must match the console script name in pyproject.toml.
PROGRAM_NAME = "calculator-mcp"
_EXIT_CODE_INTERRUPTED = 130


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description=metadata(DISTRIBUTION_NAME)["Summary"],
    )
    parser.add_argument(
        "--version",
        action="version",
        help="show the installed version",
        version=f"%(prog)s {version(DISTRIBUTION_NAME)}",
    )
    # When argv is None, argparse reads sys.argv[1:] itself.
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    _parse_args(argv)
    try:
        configure_logging()
    except ConfigError as error:
        # Logging is not configured, so report on stderr and exit.
        raise SystemExit(f"{PROGRAM_NAME}: {error}") from error
    # Import the app only after parsing so --help and --version stay fast,
    # and after configuring logging so config errors are reported above.
    # pylint: disable-next=import-outside-toplevel
    from calculator_mcp.server import run

    logger = logging.getLogger(__name__)
    logger.info("Starting %s", PROGRAM_NAME)
    try:
        run()
    except KeyboardInterrupt:
        logger.info("%s stopped by user interrupt", PROGRAM_NAME)
        return _EXIT_CODE_INTERRUPTED
    return 0
