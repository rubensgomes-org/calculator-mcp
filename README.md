[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/rubensgomes-org/calculator-mcp/blob/main/LICENSE)
[![AI Assisted](https://img.shields.io/badge/AI--Assisted-Development-007ACC)](https://github.com/rubensgomes-org/calculator-mcp/blob/main/AI_DISCLAIMER.md)

# Calculator MCP Server

`calculator-mcp` is a Streamable HTTP MCP (Model Context Protocol) server
that exposes 16 arithmetic operations as callable tools for an AI LLM (Large
Language Model) to consume. It contains no math of its own — every tool is a
thin synchronous wrapper that logs its arguments and delegates to an
open-source shared math calculator `calculator-lib-rubens` PyPI library
package.

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

## Prerequisites

- Python 3.14+
- pip 26.2+
- curl 8.7+

## Installation and Usage

### Installation

**IMPORTANT**: release versioning was recently reset to start again at
version 0.0.1. Uninstall any previously installed version first.

- Uninstall any previously installed release:

    ```bash
    pip uninstall calculator-mcp-rubens
    # recommend to purge the cache as well
    pip cache purge
    ```

- To install into the user's home environment run command below

    ```bash
    # install "calculator-mcp" and dependencies into user local pip environment
    # NOTE: use --no-cache-dir to avoid issues with earlier version in cache
    pip --no-cache-dir install -U --user calculator-mcp-rubens --verbose
    ```

- Confirm installed version with most recently released GitHub version at
  [calculator-mcp/releases](https://github.com/rubensgomes-org/calculator-mcp/releases)

    ```bash
    # show the installed version
    pip show calculator-mcp-rubens
    ```

### Usage

#### Configuration

The server ships with a default `config.yaml` bundled inside the package. To
override it, set the `CALCULATOR_MCP_CONFIG` environment variable to the
absolute path of your custom configuration file:

```bash
export CALCULATOR_MCP_CONFIG=/path/to/your/config.yaml
```

When `CALCULATOR_MCP_CONFIG` is not set, the bundled default is used
automatically. For more information about how to set up the `config.yaml`
and further documentation, refer
to [config.yaml](https://github.com/rubensgomes-org/calculator-mcp/blob/main/src/calculator_mcp/config.yaml)

#### Running the MCP Server

- Launch `calculator-mcp` locally:

    ```bash
    calculator-mcp
    ```

- Health check

    ```bash
    curl -v http://localhost:8080/health
    # Expect: OK
    ```

#### Legacy Era (Pre-July 2026)

The Legacy Era MCP server is based on a stateful session state that requires
a connection setup handshake using `initialize` / `initialized` JSON-RPC
messages.

**NOTE** To run the "Legacy Era" protocol change the config.yaml server -- >
stateless to `false`.

**1. Initialize MCP session**

The MCP endpoint requires a session, established via initialize first.
Run these in order:

- Store the JSON below in a local file `/tmp/initialize.json`:

    ```bash
    # remove indentation spaces when copying/pasting this command to the shell
    cat > /tmp/initialize.json <<EOF
    {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "initialize",
      "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {
          "name": "curl-test",
          "version": "1.0"
        }
      }
    }
    EOF
    ```

- Initialize the session and grab the `Mcp-Session-Id` from the response
  headers:

    ```bash
    # Look for the "mcp-session-id: <SID>" header in the output
    curl -i http://localhost:8080/mcp \
      -H "Content-Type: application/json" \
      -H "Accept: application/json, text/event-stream" \
      -d @/tmp/initialize.json
    ```

- Send the required `notifications/initialized` notification (use the SID
  obtained above):

    ```bash
    SID="<paste-mcp-session-id-here>"
    # Expect "202 Accepted" response
    curl -v http://localhost:8080/mcp \
      -H "Content-Type: application/json" \
      -H "Accept: application/json, text/event-stream" \
      -H "Mcp-Session-Id: $SID" \
      -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
    ```

**2. List tools** — `tools/list`

Once you have initialized your MCP session, list all the tools:

```bash
curl -s http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

This returns all 16 tools: add, subtract, multiply, divide, power, nth_root,
modulo, floor_divide, sqrt, absolute, floor, ceil, log10, ln, exp,
round_number.

**3. Call a tool** (e.g. `add`) — `tools/call`

```bash
curl -s http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":
       {"name":"add","arguments":{"a":2,"b":3}}}'
```

**Note**: reuse the same `Mcp-Session-Id` (obtained during initialization)
for every subsequent request — the server ties the session to that ID.

#### Modern Era (2026-07-28 Spec)

The Modern Era MCP server is stateless. Single-shot tools/call, no handshake
needed.

**NOTE** To run the "Modern Era" protocol change the config.yaml server -- >
stateless to `true`.

- Server discovery:

    ```bash
    curl -sS -X POST http://localhost:8080/mcp \
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
      }'
    ```

- List tools:

    ```bash
    curl -sS -X POST http://localhost:8080/mcp \
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
      }'
    ```

## License

The project is licensed under
[MIT License](https://github.com/rubensgomes-org/calculator-mcp/blob/main/LICENSE).

---
Author: [Rubens Gomes](https://rubensgomes.com/)
