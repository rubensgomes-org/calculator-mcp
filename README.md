[![python](https://img.shields.io/badge/python-3.14.7-0969da)](https://www.python.org/downloads/release/python-3147/)
[![License](https://img.shields.io/badge/License-MIT-0969da)](https://github.com/rubensgomes-org/calculator-mcp/blob/main/LICENSE)
[![AI--Assisted](https://img.shields.io/badge/AI--Assisted-Development-8250df)](https://github.com/rubensgomes-org/calculator-mcp/blob/main/AI_DISCLAIMER.md)

# Calculator MCP Server

`calculator-mcp` is a Streamable HTTP MCP (Model Context Protocol) server
that exposes 16 arithmetic operations as callable tools for an AI LLM (Large
Language Model) to consume. It contains no math of its own — every tool is a
thin synchronous wrapper that logs its arguments and delegates to the
open-source `calculator-lib-rubens` PyPI package.

## Features

16 calculator tools available via MCP based on JSON-RPC 2.0 messages:

**Two-operand operations**: `add`, `subtract`, `multiply`, `divide`, `power`,
`nth_root`, `modulo`, `floor_divide`

**Single-operand operations**: `sqrt`, `absolute`, `floor`, `ceil`, `log10`,
`ln`, `exp`

**Rounding**: `round_number` (with configurable decimal places)

## AI Disclaimer

This project includes code and documentation created with the assistance of AI
tools. For details on usage, limits, and review practices, please see the
[AI Disclaimer](https://github.com/rubensgomes-org/calculator-mcp/blob/main/AI_DISCLAIMER.md).

## Installation

### Prerequisites

- UNIX OS (e.g., macOS, Linux)
- curl 8.7+
- pip 26.2+
- poetry 2.4+
- python 3.14+

### PyPI Package Installation

**IMPORTANT**: release versioning was recently reset to start again at
version 0.0.1. Uninstall any previously installed version first.

1. Uninstall any previously installed release

```bash
pip uninstall calculator-mcp-rubens
# purging the cache is recommended as well
pip cache purge
```

2. Install into the user's home environment

```bash
# install "calculator-mcp" and dependencies into user local pip environment
# NOTE: use --no-cache-dir to avoid issues with an earlier cached version
pip --no-cache-dir install -U --user calculator-mcp-rubens --verbose
```

3. Confirm the installed version matches the latest GitHub release at
   [calculator-mcp/releases](https://github.com/rubensgomes-org/calculator-mcp/releases)

```bash
# show the installed version
pip show calculator-mcp-rubens
```

### Git Clone Installation

1. `git` clone and install local project package using `poetry`

```bash
# use local `dev` folder to install the project
mkdir -p ~/dev || exit; cd ~/dev
git clone https://github.com/rubensgomes-org/calculator-mcp.git
# change to project git local directory
cd calculator-mcp
# ensure we are at the project git local root folder
cd $(git rev-parse --show-toplevel) || exit
poetry install
```

## Usage

### Configuration

The server ships with a
default [config.yaml](https://github.com/rubensgomes-org/calculator-mcp/blob/main/src/calculator_mcp/config.yaml)
bundled inside the PyPI package. To override it, set the `CALCULATOR_MCP_CONFIG`
environment variable to the absolute path of your custom configuration file:

```bash
# assuming config_local.yaml placed in my home folder
export CALCULATOR_MCP_CONFIG="${HOME}/cfg/calculator-mcp/config_local.yaml"
```

### Running Using PyPI Package

**NOTE:** requires prior installation using
`pip install -U --user calculator-mcp-rubens`.

1. Make a copy of
   [config_local.yaml](https://github.com/rubensgomes-org/calculator-mcp/blob/main/config/config_local.yaml)
   to a local home directory (e.g.,
   `${HOME}/cfg/calculator-mcp/config_local.yaml`).

2. Launch the PyPI-installed `calculator-mcp` package:

```bash
# config_local.yaml placed in my home folder
export CALCULATOR_MCP_CONFIG="${HOME}/cfg/calculator-mcp/config_local.yaml"
# using installed package from PyPI:
calculator-mcp
```

3. Health check

```bash
# ensure config_local.yaml port is 8080
curl -v http://localhost:8080/health
# Expect: OK
```

4. To stop, go to the running terminal and press `Ctrl+C`

### Running Using Git Cloned Project

**NOTE:** requires prior cloning of the project using `git`.

1. Make a copy of
   [config_local.yaml](https://github.com/rubensgomes-org/calculator-mcp/blob/main/config/config_local.yaml)
   to a local home directory (e.g.,
   `${HOME}/cfg/calculator-mcp/config_local.yaml`).

2. Launch `calculator-mcp` from the local Git repo folder

```bash
# On my machine the project is installed here:
pushd ~/github/rubens/dev/python/calculator-mcp/
# ensure we are at the project git local root folder
cd $(git rev-parse --show-toplevel) || exit
# config_local.yaml placed in my home folder
export CALCULATOR_MCP_CONFIG="${HOME}/cfg/calculator-mcp/config_local.yaml"
poetry run calculator-mcp
```

3. Health check

```bash
# ensure config_local.yaml port is 8080
curl -v http://localhost:8080/health
# Expect: OK
```

4. To stop, go to the running terminal and press `Ctrl+C`

### Integration Test Using Git Cloned Project

**NOTE:** requires prior cloning of the project using `git`.

1. Launch `calculator-mcp` locally from the local Git repo folder

```bash
# On my machine the project is installed here:
pushd ~/github/rubens/dev/python/calculator-mcp/
# ensure we are at the project git local root folder
cd $(git rev-parse --show-toplevel) || exit
# config_local.yaml placed in my home folder
export CALCULATOR_MCP_CONFIG="${HOME}/cfg/calculator-mcp/config_local.yaml"
poetry run calculator-mcp
```

2. Integration test using local MCP server

```bash
# On my machine the project is installed here:
pushd ~/github/rubens/dev/python/calculator-mcp/
# ensure we are at the project git local root folder
cd $(git rev-parse --show-toplevel) || exit
# config_local.yaml placed in my home folder
export CALCULATOR_MCP_CONFIG="${HOME}/cfg/calculator-mcp/config_local.yaml"
poetry run python tests/integration/client.py
```

3. Integration test using remote MCP server

**NOTE:** Requires OAuth authentication which currently only Rubens is able to
authorize using his personal GitHub account.

```bash
# On my machine the project is installed here:
pushd ~/github/rubens/dev/python/calculator-mcp/
# ensure we are at the project git local root folder
cd $(git rev-parse --show-toplevel) || exit
# config_remote.yaml placed in my home folder
export CALCULATOR_MCP_CONFIG="${HOME}/cfg/calculator-mcp/config_remote.yaml"
poetry run python tests/integration/client.py
```

### Modern MCP (Version: 2026-07-28)

The "Modern Era MCP" server is stateless, which is the default in this
project's configuration file. Each `tools/call` is a single request; no
handshake is needed.

1. Launch `calculator-mcp` locally

```bash
# On my machine the project is installed here:
pushd ~/github/rubens/dev/python/calculator-mcp/
# ensure we are at the project git local root folder
cd $(git rev-parse --show-toplevel) || exit
# config_local.yaml placed in my home folder
export CALCULATOR_MCP_CONFIG="${HOME}/cfg/calculator-mcp/config_local.yaml"
poetry run calculator-mcp
```

2. Retrieve the MCP server identity `server/discover`

```bash
curl -sS http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -H "Mcp-Method: server/discover" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "server/discover",
    "params": {
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientInfo": {"name": "curl", "version": "1.0"},
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  }' | jq .
```

3. List tools `tools/list`

```bash
curl -sS http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -H "Mcp-Method: tools/list" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientInfo": {"name": "curl", "version": "1.0"},
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  }' | jq .
```

4. Add two numbers `tools/call`

```bash
curl -sS http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -H "Mcp-Method: tools/call" \
  -H "Mcp-Name: add" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "add",
      "arguments": {"a": 2, "b": 2},
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientInfo": {"name": "curl", "version": "1.0"},
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  }' | jq .
```

### Legacy MCP (Version: 2025-06-18)

The Legacy Era MCP server is based on a stateful session that requires
a connection setup handshake using `initialize` / `initialized` JSON-RPC
messages.

**NOTE:** To run the "Legacy MCP" protocol, set `server.stateless` to
`false` in `config.yaml`.

1. Launch `calculator-mcp` locally in "stateful" mode

```bash
# On my machine the project is installed here:
pushd ~/github/rubens/dev/python/calculator-mcp/
# ensure we are at the project git local root folder
cd $(git rev-parse --show-toplevel) || exit
# config_local_stateful.yaml placed in my home folder
export CALCULATOR_MCP_CONFIG="${HOME}/cfg/calculator-mcp/config_local_stateful.yaml"
poetry run calculator-mcp
```

#### Establish Session

**NOTE**: a session must be established for the MCP server to respond to tool
calls.

1. Initialize session `initialize`

```bash
# Grab the value of `mcp-session-id` from the response headers.
curl -sS -i http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": "rgomes-0",
    "method": "initialize",
    "params": {
      "protocolVersion": "2025-06-18",
      "capabilities": {},
      "clientInfo": {"name": "curl", "version": "1.0"}
    }
  }'
```

2. Invalid session `notifications/initialized` (404 session not found)

```bash
SID='1234567890'
curl -v http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: ${SID}" \
  -d '{
    "jsonrpc":"2.0",
    "id": "rgomes-1",
    "method":"notifications/initialized"
  }'
```

3. `initialize` and `notifications/initialized`

```bash
export SID="$(
  curl -sS -i http://localhost:8080/mcp \
      -H "Content-Type: application/json" \
      -H "Accept: application/json, text/event-stream" \
      -d '{
        "jsonrpc": "2.0",
        "id": "rgomes-2",
        "method": "initialize",
        "params": {
          "protocolVersion": "2025-06-18",
          "capabilities": {},
          "clientInfo": {"name": "curl", "version": "1.0"}
        }
      }' | awk -F': ' 'tolower($1)=="mcp-session-id" {print $2}' | tr -d '\r'
  )"
curl -v http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: ${SID}" \
  -d '{
    "jsonrpc":"2.0",
    "id": "rgomes-3",
    "method":"notifications/initialized"
  }'
```

4. Tools Call `tools/call` (initially requires 3 calls)

```bash
export SID="$(
  curl -sS -i http://localhost:8080/mcp \
      -H "Content-Type: application/json" \
      -H "Accept: application/json, text/event-stream" \
      -d '{
        "jsonrpc": "2.0",
        "id": "rgomes-1",
        "method": "initialize",
        "params": {
          "protocolVersion": "2025-06-18",
          "capabilities": {},
          "clientInfo": {"name": "curl", "version": "1.0"}
        }
      }' | awk -F': ' 'tolower($1)=="mcp-session-id" {print $2}' | tr -d '\r'
  )"
curl -q -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: ${SID}" \
  -d '{
    "jsonrpc":"2.0",
    "id": "rgomes-2",
    "method":"notifications/initialized"
  }'
curl -v http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: ${SID}" \
  -d '{
    "jsonrpc":"2.0",
    "id": "rgomes-3",
    "method":"tools/call",
    "params":{
      "name":"add",
      "arguments":{"a":2,"b":3}
    }
  }'
```

5. Tools List `tools/list` (initially requires 3 calls)

```bash
export SID="$(
  curl -sS -i http://localhost:8080/mcp \
      -H "Content-Type: application/json" \
      -H "Accept: application/json, text/event-stream" \
      -d '{
        "jsonrpc": "2.0",
        "id": "rgomes-1",
        "method": "initialize",
        "params": {
          "protocolVersion": "2025-06-18",
          "capabilities": {},
          "clientInfo": {"name": "curl", "version": "1.0"}
        }
      }' | awk -F': ' 'tolower($1)=="mcp-session-id" {print $2}' | tr -d '\r'
  )"
curl -q -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: ${SID}" \
  -d '{
    "jsonrpc":"2.0",
    "id": "rgomes-2",
    "method":"notifications/initialized"
  }'
curl -v http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SID" \
  -d '{
    "jsonrpc":"2.0",
    "id": "rgomes-3",
    "method":"tools/list"
  }'
# parse output to extract tools data
#curl -s http://localhost:8080/mcp \
#  -H "Content-Type: application/json" \
#  -H "Accept: application/json, text/event-stream" \
#  -H "Mcp-Session-Id: $SID" \
#  -d '{
#    "jsonrpc":"2.0",
#    "id": "rgomes-4",
#    "method":"tools/list"
#  }' | sed -n 's/^data://p' | jq .
```

## License

The project is licensed under
[MIT License](https://github.com/rubensgomes-org/calculator-mcp/blob/main/LICENSE).

---
Author: [Rubens Gomes](https://rubensgomes.com/)
