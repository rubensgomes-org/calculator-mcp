# Running the Calculator MCP Server with Docker

This document covers building, running, and deploying the Calculator MCP
Server as a container. For general project usage see [README.md](../README.md),
and for workstation setup see [SETUP.md](./SETUP.md).

## Overview

The image runs the FastMCP server over the Streamable HTTP transport.

| Property        | Value                                      |
|-----------------|--------------------------------------------|
| Base image      | `python:3.14-slim-trixie`                  |
| Listen address  | `0.0.0.0:8080` (inside the container)      |
| Published port  | `9999` on the host (maps to `8080`)        |
| MCP endpoint    | `http://<host>:9999/mcp`                   |
| Health endpoint | `http://<host>:9999/health` (returns `OK`) |
| User            | non-root, `uid=1001 gid=1001` (`app`)      |
| Image size      | ~304 MB                                    |
| Logs            | stderr only, visible via `docker logs`     |

## Prerequisites

- Docker Engine 23+ (or Docker Desktop) with the **buildx** and **compose**
  plugins.

Verify the toolchain:

```bash
docker --version
docker buildx version
docker compose version
docker info --format '{{.ServerVersion}}'   # fails if the daemon is not running
```

## Quick start

### Using `docker` commands

- Build the image

    ```bash
    # Build
    docker build --build-arg VERSION="$(poetry version -s)" \
        -t "calculator-mcp:$(poetry version -s)" -t calculator-mcp:latest .
    ```

If a build fails with `docker-credential-desktop: executable file not found`,
Docker Desktop's helper binaries are not on your `PATH`:

```bash
export PATH="$HOME/.docker/bin:$PATH"
```

- Launch container from built image

    ```bash
    # Run
    docker run -d --name calculator-mcp -p 9999:8080 \
        --restart unless-stopped "calculator-mcp:$(poetry version -s)"
    
    # Verify
    curl http://127.0.0.1:9999/health     # -> OK
    ```

- To stop the running container:

    ```bash
    docker stop calculator-mcp
    docker rm calculator-mcp
    ```

### Using `docker compose` commands

- Build and launch container

    ```bash
    docker compose up --build -d
    docker compose ps                     # STATUS should reach "healthy"
    docker compose logs -f calculator-mcp
    ```

- Display logs

    ```bash
    docker compose logs -f calculator-mcp
    ```

- Stop container

    ```bash
    docker compose down
    ```

## Image architecture

The [Dockerfile](../Dockerfile) is a two-stage build.

| Stage     | Contents                                                                                                                                                                                                 |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `builder` | Poetry 2.4.1 in the system interpreter; installs the pinned runtime dependencies from `poetry.lock` into `/opt/venv`; builds the project wheel with `poetry-core`; installs that wheel into `/opt/venv`. |
| `runtime` | Same base image; a non-root `app` user; only `/opt/venv` copied from the builder. Poetry, the build toolchain and the source tree are all left behind.                                                   |

Design notes:

- **Both stages pin the same `python:3.14-slim-trixie` image.** The runtime
  stage copies the virtual environment verbatim, so `pyvenv.cfg` and the
  console-script shebang must keep pointing at the same interpreter. Pinning
  the Debian codename also prevents a silent base-OS swap when the floating
  `3.14-slim` tag moves.
- **`poetry install --only main --no-root`, not `poetry export`.** The `export`
  command moved out of Poetry into the separate `poetry-plugin-export` package
  in Poetry 2.x and is not available. Installing from the lock also uses the
  per-file hashes directly, which is stronger than a generated
  `requirements.txt`.
- **PEP 735 dependency groups work as expected.** The dev dependencies live in
  a `[dependency-groups]` table, and Poetry 2.4 records `groups = ["dev"]` for
  them in `poetry.lock`, so `--only main` correctly excludes black, mypy and
  pytest.
- **`poetry check --lock` gates the build**, turning a stale lock file into a
  build failure rather than a silently different dependency set.
- **No compiler is installed.** Every runtime dependency, including
  `cryptography` and `pydantic-core`, ships `abi3`/`cp314` manylinux wheels for
  both `x86_64` and `aarch64`.
- **The build asserts that `config.yaml` is inside the wheel.** That file is
  package data loaded at import time through `importlib.resources`, so a
  packaging regression would otherwise only surface when the container starts.

## Configuration

The bundled `src/calculator_mcp/config.yaml` is baked into the wheel with
`transport: http`, `host: 0.0.0.0`, `port: 8080` and `stateless: true`, so the
image needs no configuration to run.

To override it, mount a replacement file and point `CALCULATOR_MCP_CONFIG`
at it:

```bash
docker run -d --name calculator-mcp -p 9999:8080 \
    -v "$(pwd)/my-config.yaml:/app/config.yaml:ro" \
    -e CALCULATOR_MCP_CONFIG=/app/config.yaml \
    "calculator-mcp:$(poetry version -s)"
```

Caveats:

- `config.yaml` is read and validated **once**, on first use, so
  `CALCULATOR_MCP_CONFIG` must be set before the process starts.
- A replacement file must contain every setting, including the full
  `logging:` block; otherwise startup fails with a pydantic `ValidationError`.
- Keep `host: "0.0.0.0"`. Binding `127.0.0.1` inside a container makes the
  server unreachable from the host.

### Environment variables

- `CALCULATOR_MCP_CONFIG`: absolute path to a replacement `config.yaml`.
- `FASTMCP_SHOW_SERVER_BANNER`: set to `true` in the image.
- `FASTMCP_CHECK_FOR_UPDATES`: set to `off` in the image to skip a blocking
  pypi.org request on start.
- `FASTMCP_LOG_LEVEL`: overrides the FastMCP log level.

Stateless HTTP mode is controlled by `server.stateless` in `config.yaml`, not
an environment variable — the app always passes that value to FastMCP
explicitly, so `FASTMCP_STATELESS_HTTP` has no effect.

## Health checks

`python:*-slim` ships neither `curl` nor `wget`, so the container health probe
uses the Python standard library:

```bash
docker inspect --format '{{.State.Health.Status}}' calculator-mcp
```

The probe allows a 10s start period and then polls every 30s. For Kubernetes,
point a `readinessProbe` and `livenessProbe` at `GET /health` on port 8080.

## Security posture

- Runs as non-root `uid=1001`, with `/opt/venv` owned by root, so the
  application cannot modify its own dependencies.
- The Compose file sets `no-new-privileges:true` and `cap_drop: ALL`.
- The server speaks **plain HTTP with no authentication**. Anything
  internet-facing belongs behind a TLS-terminating reverse proxy
  (nginx, Caddy, Traefik) with authentication in front of it.

## Lifecycle and signals

`CMD` uses the exec form, so the console script is PID 1 and receives SIGTERM
directly from `docker stop`. Uvicorn installs its own SIGTERM handler and
FastMCP configures a 2-second graceful shutdown, so the container stops in well
under a second in practice:

```bash
time docker stop calculator-mcp    # ~0.4s, exit code 0
```

The exit code is `0` when the server is PID 1. With `init: true` (as in
`docker-compose.yml`) tini is PID 1 instead and the conventional `143` is
reported. Both are correct.

## Connecting a client

Register the containerized server with Claude Code:

```bash
claude mcp add --scope project --transport http \
    calculator-mcp http://127.0.0.1:9999/mcp
```

Exercise it directly with the FastMCP client:

```bash
poetry run python -c "
import asyncio
from fastmcp import Client
async def main():
    async with Client('http://127.0.0.1:9999/mcp') as c:
        await c.ping()
        print(len(await c.list_tools()), 'tools')
        print('add(2,3) ->', (await c.call_tool('add', {'a': 2, 'b': 3})).data)
asyncio.run(main())
"
```

Expected output: `16 tools` and `add(2,3) -> 5.0`.

### Raw JSON-RPC

The image ships `stateless: true`, so a single-shot `tools/call` needs no
`initialize` handshake or session ID — each request carries its own protocol
version and capabilities in `params._meta`:

```bash
curl -i -sS -X POST http://127.0.0.1:9999/mcp \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"add","arguments":{"a":2,"b":3},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'
```

To exercise the Legacy Era (pre-2026-07-28) `initialize` handshake instead,
mount a replacement `config.yaml` with `stateless: false` (see
[Configuration](#configuration) above and the main
[README](../README.md#legacy-era-pre-july-2026)).

### Using `tests/integration/client.py`

That sample client reads the **client** section of the same `config.yaml`,
which currently points at the hosted FastMCP Cloud deployment with
`is_oauth: true`. To aim it at the container, copy the config and set:

```yaml
client:
    is_oauth: false
    url: "http://127.0.0.1:9999/mcp"
```

then run it with `CALCULATOR_MCP_CONFIG` pointing at that copy.

## Linux VPS deployment

1. Install Docker Engine and the Compose plugin.
2. Copy the repository (or just `Dockerfile` and `docker-compose.yml`) to the
   host and build, or push the image to a registry and pull it.
3. Open the port in the firewall:

    ```bash
    sudo firewall-cmd --add-port=9999/tcp --permanent
    sudo firewall-cmd --reload
    ```

4. Start it with `docker compose up -d`. The `restart: unless-stopped` policy
   brings the container back after a reboot.
5. Put a TLS-terminating reverse proxy in front of it before exposing the
   server to the internet.

## Multi-architecture builds

All runtime dependencies ship `abi3`/`cp314` manylinux wheels for both
architectures, so cross-building works:

```bash
docker buildx build --platform linux/amd64,linux/arm64 \
    --build-arg VERSION="$(poetry version -s)" \
    -t "calculator-mcp:$(poetry version -s)" .
```

Building `linux/amd64` on Apple Silicon runs the builder stage under QEMU
emulation, which is correct but noticeably slower.

## Troubleshooting

| Symptom                                                | Cause and fix                                                                                                                                          |
|--------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `PackageNotFoundError: calculator-mcp`                 | An image built before the distribution-name fix in `src/calculator_mcp/server.py`. Rebuild.                                                            |
| `docker-credential-desktop: executable file not found` | Docker Desktop helpers are not on `PATH`. Run `export PATH="$HOME/.docker/bin:$PATH"`.                                                                 |
| Connection refused from the host                       | The active config binds `127.0.0.1` instead of `0.0.0.0`, or `-p 9999:8080` was omitted.                                                               |
| `poetry check --lock` fails during build               | `poetry.lock` is stale. Run `poetry lock` and rebuild.                                                                                                 |
| Port 9999 already in use                               | Publish a different host port, for example `-p 9100:8080`. The container port stays 8080.                                                              |
| Container reports `unhealthy`                          | Inspect `docker logs calculator-mcp`; the probe needs `/health` to answer `OK` within 4 seconds.                                                       |
| HTTP 421 or 403 on `/mcp` after a FastMCP upgrade      | A future FastMCP release may enable DNS-rebinding protection by default. Set `FASTMCP_HTTP_HOST_ORIGIN_PROTECTION=false` or configure `allowed_hosts`. |

## Image maintenance

```bash
# Rebuild after changing dependencies
poetry lock && docker build --build-arg VERSION="$(poetry version -s)" \
    -t "calculator-mcp:$(poetry version -s)" .

# Inspect size and layers
docker images calculator-mcp
docker history "calculator-mcp:$(poetry version -s)"

# Reclaim space
docker system prune
```

Tag images as `calculator-mcp:<pyproject version>` alongside `:latest`, and
keep the `VERSION` build argument in `docker-compose.yml` in step with the
`version` field in `pyproject.toml`.
