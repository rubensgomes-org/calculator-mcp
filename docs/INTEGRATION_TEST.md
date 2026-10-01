## Integration Test Using Git Cloned Project

1. Launch `calculator-mcp` from local Git repo

```bash
# On my machine the project is installed here:
pushd ~/github/rubens/dev/python/calculator-mcp/
cd $(git rev-parse --show-toplevel) || exit
export CALCULATORMCP_CONFIG="${HOME}/cfg/calculator-mcp/config.yaml"
poetry run calculator-mcp
```

2. Integration test using local MCP server

```bash
# On my machine the project is installed here:
pushd ~/github/rubens/dev/python/calculator-mcp/
cd $(git rev-parse --show-toplevel) || exit
poetry run python tests/integration/client.py
```

3. Integration test using remote MCP server

**NOTE:** Requires OAuth authentication which currently only Rubens is able to
authorize using his personal GitHub account.

```bash
# On my machine the project is installed here:
pushd ~/github/rubens/dev/python/calculator-mcp/
cd $(git rev-parse --show-toplevel) || exit
poetry run python tests/integration/client.py \
  tests/integration/config_remote.yaml
```

## Stateless - Modern Era MCP (Mcp-Protocol-Version: 2026-07-28)

### Server Identity `server/discover`

```bash
curl -v http://localhost:8080/mcp \
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

### Prompts List `prompts/list`

```bash
curl -v http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -H "Mcp-Method: prompts/list" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "prompts/list",
    "params": {
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientInfo": {"name": "curl", "version": "1.0"},
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  }'
```

### Prompts Get `prompts/get"`

```bash
curl -v http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -H "Mcp-Method: prompts/get" \
  -H "Mcp-Name: solve_word_problem" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "prompts/get",
    "params": {
      "name": "solve_word_problem",
      "arguments": {
        "problem": "A pizza costs $12.50 and is split 4 ways. How much does each person pay?"
      },
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientInfo": {"name": "curl", "version": "1.0"},
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  }'
```

### Resources List `resources/list` (Stateless - Modern Era MCP)

```bash
curl -v http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -H "Mcp-Method: resources/list" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "resources/list",
    "params": {
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientInfo": {"name": "curl", "version": "1.0"},
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  }'
```

### Resources Templates List
`resources/templates/list` (Stateless - Modern Era MCP)

```bash
curl -v http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -H "Mcp-Method: resources/templates/list" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "resources/templates/list",
    "params": {
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientInfo": {"name": "curl", "version": "1.0"},
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  }'
```

### Resources Read `resources/read` (Stateless - Modern Era MCP)

```bash
curl -v http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -H "Mcp-Method: resources/read" \
  -H "Mcp-Name: calculator://constants" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "resources/read",
    "params": {
      "uri": "calculator://constants",
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientInfo": {"name": "curl", "version": "1.0"},
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  }'
```

### Resources Read from template `resources/read` (Stateless - Modern Era MCP)

```bash
curl -v http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -H "Mcp-Method: resources/read" \
  -H "Mcp-Name: calculator://operations/nth_root" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "resources/read",
    "params": {
      "uri": "calculator://operations/nth_root",
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientInfo": {"name": "curl", "version": "1.0"},
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  }'
```

### Tools List `tools/list` (Stateless - Modern Era MCP)

```bash
curl -v http://localhost:8080/mcp \
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

### Tools Call `tools/call` (Stateless - Modern Era MCP)

```bash
curl -v http://localhost:8080/mcp \
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
  }'
```

## Legacy MCP (Version: 2025-06-18)

The Legacy Era MCP server is based on a stateful session that requires
a connection setup handshake using `initialize` / `initialized` JSON-RPC
messages.

### Initialize Session `initialize`

```bash
curl -v http://localhost:8080/mcp \
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

### Notifications Initialized `notifications/initialized`


```bash
SID='<enter-sid>'
curl -v http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: ${SID}" \
  -d '{
    "jsonrpc":"2.0",
    "method":"notifications/initialized"
  }'
```

- `initialize` and `notifications/initialized`

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
        "method":"notifications/initialized"
      }'
    ```

### Resources List `resources/list`

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
    "method":"notifications/initialized"
  }'
curl -v http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Protocol-Version: 2025-06-18" \
  -H "Mcp-Session-Id: ${SID}" \
  -d '{"jsonrpc": "2.0", "id": 2, "method": "resources/list"}'
```

### Tools Call `tools/call`

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

### Tools List `tools/list`

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
```