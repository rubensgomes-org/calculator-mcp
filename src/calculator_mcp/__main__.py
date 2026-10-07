"""Executes the calculator_mcp package code at startup

``poetry run python -m calculator_mcp````
"""

# pylint: disable=invalid-name

from calculator_mcp.cli import main

raise SystemExit(main())
