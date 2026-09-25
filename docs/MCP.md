## MCP Protocol

The MCP (Model Context Protocol) is an open standard for connecting LLM
applications to external context and capabilities. The shape of it:

- Wire format: JSON-RPC 2.0
- Streamable HTTP requests and responses

### MCP Participants

A host (Claude Code, Claude Desktop, an agent app) runs one client per
connected server. The connection is 1:1 and stateful; that is, a session ID
is exchanged between the client and server after initialization.

### MCP Lifecycle

#### Legacy Initial MCP Client < -- > Server Handshake

1. The MCP client POSTs an `initialize` request
2. The MCP server responds with:

   2.1 HTTP Header among other things:
    - content-type: text/event-stream
    - mcp-session-id: <session-id>

   2.2 HTTP body a JSON containing:
    - JSON RPC version
    - MCP protocol version
    - capabilities
    - serverInfo: including server name, version, website URL and description
    - **system** instructions in natural language to be given to the LLM

3. MCP client confirms `mcp-session-id` by POSTing `notifications/initialized`
   message with the `mcp-session-id` value in the HTTP header

After the handshake is completed, the MCP client and MCP server can exchange
messages such as `tools/call`.

### MCP Server Primitives

A server can offer three kinds of primitives:

- Tools — model-controlled functions the LLM decides to invoke (tools/list,
  tools/call).
- Resources — application-controlled data addressed by URI (resources/list,
  resources/read).
- Prompts — user-controlled templates, typically surfaced as slash commands.

### MCP Client Primitives

Sampling (the server asks the client's model to complete something), roots
(filesystem scope), and elicitation (the server asks the user a question).

### MCP Transport

Two standard transports exist:

- `stdio` (server is a subprocess; JSON-RPC over newline-delimited
  stdin/stdout, with stderr free for logs), and
- Streamable HTTP (a single `/mcp` endpoint taking POSTs, optionally
  upgrading to SSE for server→client streaming, with sessions tracked by an
  `Mcp-Session-Id` header). Remote HTTP servers authenticate with OAuth 2.1.

#### Streamable HTTP

The HTTP connections between the MCP client and server are streamable
bidirectional connections. The HTTP content-type used is `text/event-stream`.
That is, the data is sent as UTF-8 encoded text over the TCP socket, and the
server sends events (Server-Sent Events) to the client over the same socket.

##### Text vs Binary Connection

A number like 12345 takes 5 (five) bytes to be encoded in UTF-8 and sent over
a text connection, while in a binary connection, 12345 takes only 2 bytes to
be represented in a binary format.

A foreign character, like "é", takes 2 bytes to be encoded in UTF-8, but if
using ISO-8859-1 it takes 1 byte. So, the number of bytes used on text
streams depends entirely on the encoding standard chosen by the sender and
receiver for text characters.

##### Bidirectional Connections

Although TCP sockets support an Input Stream and an Output Stream, the
connection is only bidirectional if the higher-level protocol is also
bidirectional. Old HTTP/1.1 connections were unidirectional, while HTTP/2 is
bidirectional.

## How This Project Implements the MCP Protocol

It doesn't hand-roll any of the protocol. FastMCP (`fastmcp >=4.0.4`) supplies
the JSON-RPC layer, the initialize handshake, capability advertisement,
session management, and both transports. The project's job is to declare
what it serves.

Each `@mcp.tool`-decorated function is turned into an MCP tool descriptor
automatically:

- The function name becomes the tool name (`add`, `nth_root`,
  `round_number`).
- The type hints (`a: float, b: float, decimals: int = 0`) become the tool's
  JSON Schema `inputSchema`, including which parameters are required —
  that's what lets FastMCP reject bad arguments before your code runs.
- The Google-style docstring becomes the tool description the model reads
  when deciding what to call. This is why `src/calculator_mcp/server.py`
  treats docstrings as a contract rather than internal commentary.
- A raised `ValueError` (divide by zero, sqrt of a negative) is converted
  into a JSON-RPC tool error — `tests/test_server.py` asserts this by
  expecting `ToolError` from `divide(1, 0)`.

#### Protocol-Level Metadata the Server Sets Explicitly

```python
mcp = FastMCP(
    "Calculator MCP Server",
    version=_VERSION,
    instructions="...",
    website_url=_HOMEPAGE,
)
```

`instructions` is part of the initialize response — server-level guidance
the host can put in front of the model, summarizing the tool families so it
doesn't have to infer them tool by tool.

Every tool also carries MCP behavioral annotations:

```python
annotations = {
    "readOnlyHint": True,
    "idempotentHint": True,
    "openWorldHint": False,
}
```

These are hints to the host, not enforcement: nothing is mutated, calling
twice is safe, and the tool touches no external world. Hosts use them to
decide whether a call needs a confirmation prompt — which is why a
calculator can run unattended. `timeout=_TIMEOUT` (10s from config) bounds
each call.

### This Project's Transport Configuration

Only the `http` transport is supported; `main.py` starts it with the
`config.yaml` settings:

```python
server = get_config().server
mcp.run(transport=server.transport, host=server.host, port=server.port)
```

The shipped default is `0.0.0.0:8080` — bound to all interfaces
deliberately so the server is reachable from outside the container.

`/health` is registered via `@mcp.custom_route` — a plain Starlette route on
the same ASGI app, outside the MCP protocol. Container orchestration needs a
probe that doesn't speak JSON-RPC. `tests/test_server.py::test_health_check`
exercises it in-process with `httpx.ASGITransport` over `mcp.http_app()`, no
port required.

### The Client Side

`tests/integration/client.py` is the mirror image — a real MCP client built
from the same config module. It does the full round trip: `client.ping()`,
`client.list_tools()`, then `call_tool` on each discovered tool with sample
arguments. For the deployed instance at
<https://rubens-calculator-mcp.fastmcp.app/mcp> it wraps
`fastmcp.client.auth.OAuth`, persisting tokens in a `FileTreeStore` behind a
`FernetEncryptionWrapper` keyed from `OAUTH_STORAGE_ENCRYPTION_KEY`, with a
fixed callback port so the OAuth redirect URI stays stable across runs.

The unit tests use the same `Client` (`mcp`) API against the in-process
server object, so tests go through genuine MCP tool dispatch rather than
calling the Python functions directly.

### Observability

`config.yaml` pre-wires loggers for the protocol internals —
`mcp.server.lowlevel.server`, `mcp.server.streamable_http`,
`mcp.server.streamable_http_manager`, `mcp.client.streamable_http`, plus
`httpx`/`httpcore` — at INFO (`httpx` at DEBUG) with a comment saying to flip
them to DEBUG to see the raw JSON-RPC messages or HTTP wire traffic. That's
the debugging path when a host and this server disagree.

## Free FastMCP Deployment

- <https://horizon.prefect.io>
