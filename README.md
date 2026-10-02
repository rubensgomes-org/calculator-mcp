# Calculator MCP Server

[![python](https://img.shields.io/badge/python-3.14%2B-0969da?logo=python)](https://www.python.org/downloads/release/python-3147/)
[![poetry](https://img.shields.io/badge/poetry-2.5%2B-0969da?logo=poetry)](https://python-poetry.org/)
[![FastMCP](https://img.shields.io/badge/FastMCP-4-8250df)](https://gofastmcp.com/getting-started/welcome)
[![GitHub](https://img.shields.io/badge/GitHub-Actions-0969da?logo=github+actions)](https://github.com/features/actions)
[![Microsoft](https://img.shields.io/badge/Microsoft-Azure-0969da)](https://azure.microsoft.com/en-us)
[![AI](https://img.shields.io/badge/AI-Assisted-d29922?logo=claude+code)](https://github.com/rubensgomes-org/calculator-mcp/blob/main/AI_DISCLAIMER.md)
[![license](https://img.shields.io/badge/license-MIT-1a7f37)](https://github.com/rubensgomes-org/calculator-mcp/blob/main/LICENSE)

`calculator-mcp` is an MCP (Model Context Protocol) server that exposes 16
arithmetic operations as callable tools for use by LLMs within agentic
applications. It contains no mathematical logic of its own. Instead, each tool
is a thin synchronous wrapper that logs its arguments and delegates execution to
the open-source
[calculator-lib](https://github.com/rubensgomes-org/calculator-lib) package
published on PyPI as
[calculator-lib-rubens](https://pypi.org/project/calculator-lib-rubens/).

---

## Features

16 calculator functions exposed through an MCP server for consumption by AI
agentic programs:

- **Two-operand operations**: `add`, `subtract`, `multiply`, `divide`, `power`,
  `nth_root`, `modulo`, `floor_divide`
- **Single-operand operations**: `sqrt`, `absolute`, `floor`, `ceil`, `log10`,
  `ln`, `exp`
- **Rounding**: `round_number` (with configurable decimal places)

The following are the supported MCP JSON-RPC 2.0 methods:

- **Lifecycle Methods:** `initialize`, `notifications/initialized`
- **Tools Methods:** `tools/list`, `tools/call`
- **Resources Methods:** `resources/list`, `resources/templates/list`,
  `resources/read`
- **Prompts Methods:** `prompts/list`, `prompts/get`

The following MCP protocols are supported, selected by the client per
request:

- **Legacy MCP (Version: 2025-06-18)**: `initialize` handshake and
  `Mcp-Session-Id` session
- **Modern MCP (Version: 2026-07-28)**: no handshake or session

## Unsupported Features

Unsupported JSON-RPC methods:

- **Logging & Progress Utilities** (e.g. `notifications/progress`)
- **Server-to-Client** calls (e.g.
  `sampling/createMessage`, `elicitation/create`, `roots/list`)

## AI Disclaimer

This project includes code and documentation created with the assistance of AI
tools. For details on usage, limits, and review practices, please see the
[AI Disclaimer](https://github.com/rubensgomes-org/calculator-mcp/blob/main/AI_DISCLAIMER.md).

## Prerequisites

- Python 3.14+
- pip

## Installation

1. Install using `pip`

```bash
pip install calculator-mcp-rubens
```

2. Confirm the installed version matches the latest GitHub release at
   [calculator-mcp/releases](https://github.com/rubensgomes-org/calculator-mcp/releases)

```bash
calculator-mcp --version
pip show calculator-mcp-rubens
```

## Uninstall

```bash
pip uninstall calculator-mcp-rubens
pip cache purge
```

## Configuration

- Copy the file
  [config.yaml](https://github.com/rubensgomes-org/calculator-mcp/blob/main/config/config.yaml)
  to `${HOME}/cfg/calculator-mcp/config.yaml`.

```bash
export CALCULATORMCP_CONFIG="${HOME}/cfg/calculator-mcp/config.yaml"
```

## Usage

1. Run

```bash
calculator-mcp
```

2. Health check

```bash
curl -v http://localhost:8080/health
# Expect: OK
```

3. To stop, press `Ctrl+C` in the running terminal

## License

The project is licensed under the
[MIT License](https://github.com/rubensgomes-org/calculator-mcp/blob/main/LICENSE).

## Links

- [GitHub Project](https://github.com/rubensgomes-org/calculator-mcp)
- [Azure CLI Commands](https://github.com/rubensgomes-org/calculator-mcp/blob/main/docs/AZ_CMD.md)
- [Azure Container App Provisioning](https://github.com/rubensgomes-org/calculator-mcp/blob/main/docs/AZURE_ACA.md)
- [Demo](https://github.com/rubensgomes-org/calculator-mcp/blob/main/docs/DEMO.md)
- [Development Setup](https://github.com/rubensgomes-org/calculator-mcp/blob/main/docs/DEVELOPMENT_SETUP.md)
- [Docker](https://github.com/rubensgomes-org/calculator-mcp/blob/main/docs/DOCKER.md)
- [Integration Test](https://github.com/rubensgomes-org/calculator-mcp/blob/main/docs/INTEGRATION_TEST.md)
- [MCP](https://github.com/rubensgomes-org/calculator-mcp/blob/main/docs/MCP.md)
- [Miscellaneous](https://github.com/rubensgomes-org/calculator-mcp/blob/main/docs/MISC.md)
- [OAuth Diagram](https://github.com/rubensgomes-org/calculator-mcp/blob/main/docs/OAUTH_DIAGRAM.md)
- [PyCharm](https://github.com/rubensgomes-org/calculator-mcp/blob/main/docs/PYCHARM.md)
- [Release Process](https://github.com/rubensgomes-org/calculator-mcp/blob/main/docs/RELEASE.md)

---
Author: [Rubens Gomes](https://rubensgomes.com/)
