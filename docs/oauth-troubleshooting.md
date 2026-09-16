# OAuth Troubleshooting Guide

This document captures issues encountered when connecting a custom Python MCP
client to a hosted FastMCP server using OAuth, and their solutions.

## Environment

- **Client**: Python 3.14+ running in WSL2 Ubuntu on Windows 11
- **Server**: Hosted FastMCP at `https://rubens-calculator-mcp.fastmcp.app`
- **Auth Provider**: WorkOS via Prefect Horizon (`auth.horizon.prefect.io`)
- **Libraries**: `fastmcp>=3.1.0`, `mcp>=1.26.0`

---

## Issue 1: "The redirect URI provided for the application was invalid"

### Symptom

After authenticating in the browser, the authorization server displayed:

> Authorization Error — The redirect URI provided for the application was
> invalid.

### Root Cause

Stale OAuth client registration data was cached in `~/.fastmcp`.
The cached `client_id` was registered with a different `redirect_uri` than
the one the client was now sending (`http://localhost:10000/callback`).

### Solution

Clear the cached OAuth data and re-run the client:

```bash
rm -rf ~/.fastmcp/*
```

The client performs dynamic client registration (RFC 7591) on each fresh
start, which registers the correct `redirect_uri` with the authorization
server.

---

## Issue 2: Token exchange fails with 401 `{"error":"unauthorized"}`

### Symptom

After successful browser authentication and OAuth callback, the token
exchange (`POST /oauth2/token`) returned:

```
HTTP/1.1 401 Error
{"error":"unauthorized"}
```

### Analysis

Debug logging revealed the following:

1. **Dynamic client registration** succeeded (201 Created) and the server
   returned `token_endpoint_auth_method: "client_secret_basic"`.

2. With `client_secret_basic`, the MCP library sends client credentials via
   an `Authorization: Basic <base64(client_id:client_secret)>` header.

3. The token endpoint (`/oauth2/token`) is proxied through a **CloudFront
   Lambda** function. The 401 response came from this Lambda (evidenced by
   `X-Cache: LambdaGeneratedResponse from cloudfront`), NOT from the
   underlying WorkOS auth server.

4. The CloudFront Lambda proxy intercepts and rejects the `Authorization:
   Basic` header before forwarding the request to WorkOS.

### Solution

Force `client_secret_post` as the token endpoint auth method by passing
`additional_client_metadata` to the `OAuth` constructor:

```python
oauth = OAuth(
    token_storage=encrypted_storage,
    callback_port=get_callback_port(),
    additional_client_metadata={
        "token_endpoint_auth_method": "client_secret_post",
    },
)
```

With `client_secret_post`, the `client_id` and `client_secret` are sent in
the POST body instead of the `Authorization` header. The CloudFront proxy
does not intercept POST body parameters, so the request reaches WorkOS
successfully.

**Before (failing)**:
- Auth method: `client_secret_basic`
- Headers: `Authorization: Basic <base64>`
- Result: 401 from CloudFront Lambda

**After (working)**:
- Auth method: `client_secret_post`
- Body: `...&client_secret=<secret>`
- Result: 200 OK with access token

---

## Issue 3: Health check returns 401 on hosted FastMCP

### Symptom

After successful OAuth connection, the `/health` endpoint returned:

```
HTTP/1.1 401 Unauthorized
{"error":"invalid_request","error_description":"Bearer token required"}
```

### Root Cause

The `_check_health()` function uses a plain `httpx.AsyncClient()` without
OAuth credentials. On the hosted FastMCP platform, the `/health` endpoint
sits behind the same CloudFront proxy that requires a bearer token.

### Solution

Skip the health check for OAuth connections since `client.ping()` already
verifies server connectivity through the authenticated MCP session:

```python
if transport == "http" and not is_oauth():
    base_url = url.rsplit("/mcp", 1)[0]
    await _check_health(base_url)
```

---

## Debugging Tips

### Enable debug logging

Set these levels in `config.yaml` to trace the full OAuth flow:

```yaml
logging:
  loggers:
    calculator_mcp:
      level: DEBUG          # client application logs
    mcp.client.streamable_http:
      level: DEBUG          # JSON-RPC messages
    httpx:
      level: DEBUG          # HTTP request/response summaries
    httpcore:
      level: DEBUG          # wire-level tracing (headers, TCP)
  root:
    level: DEBUG            # catch all library logs (fastmcp.client.auth, etc.)
```

### Inspect OAuth server metadata

```bash
# Authorization server metadata (endpoints, supported methods)
curl -s https://rubens-calculator-mcp.fastmcp.app/.well-known/oauth-authorization-server | python3 -m json.tool

# Protected resource metadata (resource URI, auth servers)
curl -s https://rubens-calculator-mcp.fastmcp.app/.well-known/oauth-protected-resource/mcp | python3 -m json.tool
```

### Identify where a 401 originates

Compare response headers to determine if the rejection comes from the
CloudFront Lambda proxy or the upstream WorkOS auth server:

| Source | Key headers |
|--------|-------------|
| CloudFront Lambda | `X-Cache: LambdaGeneratedResponse from cloudfront`, minimal headers |
| WorkOS (via Cloudflare) | `Set-Cookie: ...domain=.workos.com`, `x-workos-backend-routing`, `x-vercel-id` |

### Clear cached OAuth data

```bash
rm -rf ~/.fastmcp/*
```

This forces fresh dynamic client registration on the next run.
