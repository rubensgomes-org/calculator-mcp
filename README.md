[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/rubensgomes-org/calculator-mcp/blob/main/LICENSE)
[![AI Assisted](https://img.shields.io/badge/AI--Assisted-Development-007ACC)](https://github.com/rubensgomes-org/calculator-mcp/blob/main/AI_DISCLAIMER.md)

# Calculator MCP Server

`calculator-mcp` is a small Streamable HTTP MCP (Model Context Protocol) server
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

**IMPORTANT**: It is recommended that you run `pip uninstall` to remove any
previously installed versions of this software from your local machine. The
application's release versioning was recently reset and to re-start again at
version 0.0.1.

- Uninstall earlier possible installed release:

    ```bash
    pip uninstall calculator-mcp-rubens
    # recommend to purge the cache as well
    pip cache purge
    ```

### Installation

The `calculator-mcp` can be installed by running
`pip install calculator-mcp-rubens`. It requires `python` 3.14+ and `pip` to
run.

- To install locally into the user's home environment run command below

    ```bash
    # install "calculator-mcp" and depdencies into user local pip environment
    # NOTE: use --no-cache-dir to avoid issues with earlier version in cache
    pip --no-cache-dir install -U --user calculator-mcp-rubens --verbose
    ```

- Confirm installed version with most recently released GitHub version at
  [calculator-mcp/releases](https://github.com/rubensgomes-org/calculator-mcp/releases)

    ```bash
    # install "calculator-mcp" and depdencies into user local pip environment
    pip show calculator-mcp-rubens
    ```

### Usage

#### Running the MCP Server

- Launch `calculator-mcp` locally with sensible defaults:

    ```bash
    # Launches the Streamable HTTP MCP server locally at:
    # http://0.0.0.0:8080/mcp
    # The "0.0.0.0" is used because this application is meant to run from
    # within a Docker container, which requires the wildcard address, or
    # INADDR_ANY, to accept HTTP connections from outside the container.
    calculator-mcp
    ```

#### Exercise the MCP Server Endpoints

1. Health check

    ```bash
    curl -v http://localhost:8080/health
    # Expect: OK
    ```

2. Initialize MCP session

The MCP endpoint requires a session, established via initialize first.
Run these in order:

- a) Store JSON below in a local file `/tmp/initialize.json`:

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

- b) MCP client initializes session — grab the `Mcp-Session-Id` from the
  response headers

  ```bash
  # Look for the "mcp-session-id: <SID>" header in the output
  curl -i http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d @/tmp/initialize.json
  ```

- c) `notifications/initialized` MCP client sends the required "initialized"
  notification (use the SID from step b)

  ```bash
  SID="<paste-mcp-session-id-here>"
  # Expect "202 Accepted" response
  curl -v http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
  ```

3. List tools - `tools/list`

- `tools/list` once you have initialized your MCP session, list all the tools:

  ```bash
  curl -s http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
  ```

This returns all 16 tools: add, subtract, multiply, divide, power, nth_root,
modulo, floor_divide, sqrt, absolute, floor, ceil, log10, ln, exp, round_number.

4. Call a tool (e.g. `add`) - `tools/call`

- `tools/call` To call one of the tools (e.g., `add`)

    ```bash
    curl -s http://localhost:8080/mcp \
      -H "Content-Type: application/json" \
      -H "Accept: application/json, text/event-stream" \
      -H "Mcp-Session-Id: $SID" \
      -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"add","arguments":{"a":2,"b":3}}}'
    ```

Returns `{"result": 5.0}` in `structuredContent`. Swap `name` and `arguments`
to call any other tool, e.g.
`{"name": "divide", "arguments": {"a": 15, "b": 4}}`
or `{"name": "sqrt", "arguments": {"a": 16}}`.

**Note**: the same `Mcp-Session-Id` must be reused across steps b, c, 3, and 4
— the server ties the session to that ID.

## Configuration

The server ships with a default `config.yaml` bundled inside the package. To
override it, set the `CALCULATOR_MCP_CONFIG` environment variable to the
absolute path of your custom configuration file:

```bash
export CALCULATOR_MCP_CONFIG=/path/to/your/config.yaml
```

When `CALCULATOR_MCP_CONFIG` is not set, the bundled default is used
automatically.

The configuration file has three sections. The `logging` section controls Python
logging via `dictConfig`. The default configuration logs `calculator_mcp`
messages at `DEBUG` level to stderr.

```yaml
# =============================================================================
# Server Configuration
# =============================================================================
server:
    # the home page of this project
    homepage: "https://github.com/rubensgomes-org/calculator-mcp"
    # MCP transport: "stdio" or "http"
    # http: for web services using the Streamable HTTP protocol
    transport: "http"
    # Host IP address for the HTTP/MCP server.
    # The "0.0.0.0" is used because this application is meant to run from
    # within a Docker container, which requires the wildcard address or
    # NADDR_ANY to accept HTTP connections
    # from outside the Docker container.
    # Use 127.0.0.1 to restrict the server to localhost only.
    host: "0.0.0.0"
    #host: "127.0.0.1"
    # Port for the HTTP/MCP server, defaults to:
    port: 8080
    #port: 9090
    # timeout in seconds
    timeout: 10

# =============================================================================
# Client Configuration
# =============================================================================
client:
    # the URL the client should use when the server transport is "http"
    #    is_oauth: false
    #    url: "http://127.0.0.1:8080/mcp"
    is_oauth: true
    url: "https://rubens-calculator-mcp.fastmcp.app/mcp"
    # location to store OAuth token
    token_dir: "~/.fastmcp"
    # fixed port for the OAuth callback server
    callback_port: 10000

# =============================================================================
# Logging Configuration
# =============================================================================
logging:
    version: 1
    disable_existing_loggers: false
    formatters:
        standard:
            format: "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    handlers:
        console:
            class: logging.StreamHandler
            formatter: standard
            stream: ext://sys.stderr
    loggers:
        calculator_mcp:
            level: DEBUG
            handlers:
                - console
            propagate: false
        # MCP protocol tracing — set to DEBUG to see full JSON-RPC messages
        mcp.client.streamable_http:
            level: INFO
            handlers:
                - console
            propagate: false
        # HTTP request/response summaries — set to DEBUG for detail
        httpx:
            level: DEBUG
            handlers:
                - console
            propagate: false
        # HTTP wire-level tracing (headers, TCP) — set to DEBUG for detail
        httpcore:
            level: INFO
            handlers:
                - console
            propagate: false
        # Server: inbound JSON-RPC messages — set to DEBUG to see parsed requests
        mcp.server.lowlevel.server:
            level: INFO
            handlers:
                - console
            propagate: false
        # Server: StreamableHTTP transport — set to DEBUG for method-level tracing
        mcp.server.streamable_http:
            level: INFO
            handlers:
                - console
            propagate: false
        # Server: session/transport lifecycle — set to DEBUG for session details
        mcp.server.streamable_http_manager:
            level: INFO
            handlers:
                - console
            propagate: false
        # Server: HTTP request lines (method, path, status)
        uvicorn.access:
            level: INFO
            handlers:
                - console
            propagate: false
    root:
        level: WARNING
        handlers:
            - console
```

## License

The project is licensed under
[MIT License](https://github.com/rubensgomes-org/calculator-mcp/blob/main/LICENSE).

---
Author: [Rubens Gomes](https://rubensgomes.com/)
