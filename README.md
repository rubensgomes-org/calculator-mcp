# Calculator MCP Server

[![Python](https://img.shields.io/badge/Python-3.14%2B-0969da?logo=python)](https://www.python.org/downloads/release/python-3147/)
[![FastMCP](https://img.shields.io/badge/FastMCP-4-8250df)](https://gofastmcp.com/getting-started/welcome)
[![Poetry](https://img.shields.io/badge/Poetry-2.5%2B-0969da?logo=poetry)](https://python-poetry.org/)
[![GitHub](https://img.shields.io/badge/GitHub-Actions-0969da?logo=github+actions)](https://github.com/features/actions)
[![Microsoft](https://img.shields.io/badge/Microsoft-Azure-0969da)](https://azure.microsoft.com/en-us)
[![AI Assisted](https://img.shields.io/badge/AI%20Assisted-Development-d29922)](https://github.com/rubensgomes-org/calculator-mcp/blob/main/AI_DISCLAIMER.md)
[![License](https://img.shields.io/badge/License-MIT-0969da)](https://github.com/rubensgomes-org/calculator-mcp/blob/main/LICENSE)

`calculator-mcp` is an MCP (Model Context Protocol) server that exposes 16
arithmetic operations as callable tools for use by LLMs within agentic
applications. It contains no mathematical logic of its own. Instead, each tool
is a thin synchronous wrapper that logs its arguments and delegates execution to
the open-source `calculator-lib-rubens` package published on PyPI.

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

- **Legacy MCP (Version: 2025-06-18)**: `initialize` handshake; a
  `Mcp-Session-Id` is issued only when `stateless` is false in
  `config.yaml`
- **Modern MCP (Version: 2026-07-28)**: no handshake or session

## Non-Supported Features

Non-supported JSON-RPC methods:

- **Logging & Progress Utilities** (e.g. `notifications/progress`)
- **Server-to-Client** calls are not supported (e.g. 
`sampling/createMessage`, `elicitation/create`, `roots/list`)

## AI Disclaimer

This project includes code and documentation created with the assistance of AI
tools. For details on usage, limits, and review practices, please see the
[AI Disclaimer](https://github.com/rubensgomes-org/calculator-mcp/blob/main/AI_DISCLAIMER.md).

## Prerequisites

- python 3.14+
- pip

## Installation

1. Install in `pip` default installation folder

```bash
pip install calculator-mcp-rubens
```

2. Install in the Python user install directory

```bash
pip --no-cache-dir install -U --user calculator-mcp-rubens
```

3. Confirm the installed version matches the latest GitHub release at
   [calculator-mcp/releases](https://github.com/rubensgomes-org/calculator-mcp/releases)

```bash
calculator-mcp --version
pip show calculator-mcp-rubens
```

## Uninstall

- Uninstall as follows

```bash
pip uninstall calculator-mcp-rubens
pip cache purge
```

## Configuration

- Copy the file
  [config.yaml](https://github.com/rubensgomes-org/calculator-mcp/blob/main/config/config.yaml)
  to `${HOME}/cfg/calculator-mcp/config.yaml`.

```bash
export CALCULATOR_MCP_CONFIG="${HOME}/cfg/calculator-mcp/config.yaml"
```

## Usage

1. Simply run

```bash
calculator-mcp
```

2. Health check

```bash
curl -v http://localhost:8080/health
# Expect: OK
```

3. To stop, go to the running terminal and press `Ctrl+C`

## License

The project is licensed under
[MIT License](https://github.com/rubensgomes-org/calculator-mcp/blob/main/LICENSE).

## Links

- [GitHub Project](https://github.com/rubensgomes-org/calculator-mcp)
- [Azure CLI Commands](https://github.com/rubensgomes-org/calculator-mcp/blob/main/docs/AZ_CMD.md)
- [Azure Container App Provisioning](https://github.com/rubensgomes-org/calculator-mcp/blob/main/docs/AZURE_ACA.md)
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
