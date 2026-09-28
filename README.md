# Calculator MCP Server

[![python](https://img.shields.io/badge/python-3.14.7-0969da)](https://www.python.org/downloads/release/python-3147/)
[![License](https://img.shields.io/badge/License-MIT-0969da)](https://github.com/rubensgomes-org/calculator-mcp/blob/main/LICENSE)
[![AI--Assisted](https://img.shields.io/badge/AI--Assisted-Development-8250df)](https://github.com/rubensgomes-org/calculator-mcp/blob/main/AI_DISCLAIMER.md)

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

The following MCP protocols are supported:

- **Legacy MCP (Version: 2025-06-18)** when stateless is true in `config.yaml`
- **Modern MCP (Version: 2026-07-28)** when stateless is false in `config.yaml`

## Non-Supported Features

- **Server-sent events (SSE)** are not supported for the MCP communication.
- **Streaming communication channels**, such as HTTP Streamable, are not
  supported. In other words, the MCP server is expected to generate the
  entire output before sending it.

Non-supported JSON-RPC methods:

- **Resources Methods:** `resources/list`, `resources/read`
- **Prompts Methods:** `prompts/list`, `prompts/get`
- **Logging & Progress Utilities**
- **Server-to-Client** calls are not supported

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
pip show calculator-mcp-rubens
```

## Configuration

The server ships with a
default [config.yaml](https://github.com/rubensgomes-org/calculator-mcp/blob/main/src/calculator_mcp/config.yaml)
bundled inside the PyPI package. To override it, make a copy and paste in 
your "${HOME}" folder, and set the `CALCULATOR_MCP_CONFIG` environment 
variable to the path of your custom configuration file:

```bash
# assuming config.yaml placed in my home folder
export CALCULATOR_MCP_CONFIG="${HOME}/cfg/calculator-mcp/config.yaml"
```

## Usage

1. Ensure `CALCULATOR_MCP_CONFIG` is properly setup, and run:

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

---
Author: [Rubens Gomes](https://rubensgomes.com/)
