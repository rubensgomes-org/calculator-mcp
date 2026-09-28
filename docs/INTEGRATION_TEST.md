## Integration Test Using Git Cloned Project

1. Launch `calculator-mcp` locally from the local Git repo folder

```bash
# On my machine the project is installed here:
pushd ~/github/rubens/dev/python/calculator-mcp/
# ensure we are at the project git local root folder
cd $(git rev-parse --show-toplevel) || exit
# config.yaml placed in my home folder
export CALCULATOR_MCP_CONFIG="${HOME}/cfg/calculator-mcp/config_local.yaml"
poetry run calculator-mcp
```

2. Integration test using local MCP server

```bash
# On my machine the project is installed here:
pushd ~/github/rubens/dev/python/calculator-mcp/
# ensure we are at the project git local root folder
cd $(git rev-parse --show-toplevel) || exit
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
poetry run python tests/integration/client.py \
  tests/integration/config_remote.yaml
```

## Modern MCP (Version: 2026-07-28)

The "Modern Era MCP" server is stateless, which is the default in this
project's configuration file. Each `tools/call` is a single request; no
handshake is needed.

1. Launch `calculator-mcp` locally

```bash
# On my machine the project is installed here:
pushd ~/github/rubens/dev/python/calculator-mcp/
# ensure we are at the project git local root folder
cd $(git rev-parse --show-toplevel) || exit
# config.yaml placed in my home folder
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

## Legacy MCP (Version: 2025-06-18)

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
# config_stateful.yaml placed in my home folder
export CALCULATOR_MCP_CONFIG="${HOME}/cfg/calculator-mcp/config_local_stateful.yaml"
poetry run calculator-mcp
```

### Establish Session

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
