"""Run main() parsing any user CLI arguments."""

import argparse
import logging
from importlib.metadata import metadata, version

from calculator_mcp.config import ConfigError, configure_logging
from . import DISTRIBUTION_NAME

_VERSION=version(DISTRIBUTION_NAME)
_EXIT_CODE_INTERRUPTED = 130

def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=DISTRIBUTION_NAME,
        description=f"%(prog)s {metadata(DISTRIBUTION_NAME)["Summary"]}"
    )
    parser.add_argument(
        "--version",
        action="version",
        help="show the installed version",
        version=f"%(prog)s {_VERSION}",
    )
    #  when argparse gets None, it defaults/reads sys.argv[1:] tself
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    _parse_args(argv)
    try:
        configure_logging()
    except ConfigError as error:
        # Logging is not configured, so report on stderr and exit.
        raise SystemExit(f"{DISTRIBUTION_NAME}: {error}") from error
    # Import the app only after parsing so --help and --version stay fast,
    # and after configuring logging so config errors are reported above.
    # pylint: disable-next=import-outside-toplevel
    from calculator_mcp.app import run

    logger = logging.getLogger(__name__)
    logger.info("Starting %s", DISTRIBUTION_NAME)
    # app:run starts uvicorn web server, and returns None
    try:
        run()
    except KeyboardInterrupt:
        logger.info("%s stopped by user interrupt", DISTRIBUTION_NAME)
        return _EXIT_CODE_INTERRUPTED
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
