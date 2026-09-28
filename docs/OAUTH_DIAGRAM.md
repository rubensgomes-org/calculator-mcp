## OAuth Authentication Flow

This project's source code and documentation were generated with the
assistance of Artificial Intelligence (AI). For more information, please
refer to the `AI_DISCLAIMER.md` document located in the project's root
directory.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Agent as math-ai-agent<br/>(FastMCP Client)
    participant Callback as Callback Server<br/>(localhost:10101)
    participant Store as Token Store<br/>(token_dir)
    participant MCP as Calculator MCP Server<br/>(fastmcp.app)
    participant Horizon as Prefect Horizon<br/>(auth.horizon.prefect.io)
    participant GitHub

    Agent->>MCP: POST /mcp (no token)
    MCP-->>Agent: 401 Unauthorized
    Agent->>Callback: Start callback server
    Agent->>MCP: GET /oauth2/authorize (via browser)
    MCP-->>Horizon: Redirect to /signed-in/application-authorization
    Horizon->>User: Request access approval
    User->>Horizon: Allow access
    Horizon->>GitHub: Delegate user authentication
    User->>GitHub: Sign in
    GitHub-->>Horizon: User authenticated
    Horizon-->>Callback: Redirect to /callback with authorization code
    Callback-->>Agent: Authorization code
    Agent->>MCP: Exchange code for tokens
    MCP-->>Agent: Access and refresh tokens
    Agent->>Store: Store encrypted tokens
    Agent->>MCP: POST /mcp (Bearer access token)
    MCP-->>Agent: 200 OK
```
