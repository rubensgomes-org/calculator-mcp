# Running the Calculator MCP Server with Docker

This document covers building, running, and deploying the Calculator MCP
Server as a `docker` container.

## Overview

The image runs the FastMCP server over the Streamable HTTP transport.

| Property        | Value                                      |
|-----------------|--------------------------------------------|
| Base image      | `python:3.14-slim-trixie`                  |
| Listen address  | `0.0.0.0:8080` (inside the container)      |
| Published port  | `8080` on the host (maps to `8080`)        |
| MCP endpoint    | `http://<host>:8080/mcp`                   |
| Health endpoint | `http://<host>:8080/health` (returns `OK`) |
| User            | non-root, `uid=1001 gid=1001` (`app`)      |
| Image size      | ~304 MB                                    |
| Logs            | stderr only, visible via `docker logs`     |

## Prerequisites

- Docker Engine 23+ (or Docker Desktop) with the **buildx** and **compose**
  plugins.

## Quick start

### Install `docker` CLI

- OS: `macOS`

    ```bash
    brew install docker
    ```

- Verify the toolchain:

    ```bash
    docker --version
    docker buildx version
    docker compose version
    ```

### Install `Docker Desktop`

- Follow
  [Install Docker Desktop on Mac](https://docs.docker.com/desktop/setup/install/mac-install/)

### Using `docker` commands

- Start the `Docker Desktop` GUI + engine

    ```bash
    # macOS
    open -a Docker
    ```

- Clean up the `docker` system to start fresh

    ```bash
    docker system prune --all
    ```

- Build the docker image

    ```bash
    # Build
    docker build --build-arg VERSION="$(poetry version -s)" \
        -t "calculator-mcp:$(poetry version -s)" -t calculator-mcp:latest .
    ```

- Launch container from built image

    ```bash
    # Run
    docker run -d --name calculator-mcp -p 8080:8080 \
        --restart unless-stopped "calculator-mcp:$(poetry version -s)"

    # Verify - expect OK
    curl http://127.0.0.1:8080/health
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
    docker compose ps
    # Verify - expect OK
    curl http://127.0.0.1:8080/health
    ```

- Display logs

    ```bash
    docker compose logs -f calculator-mcp
    ```

- Stop container

    ```bash
    docker compose down
    ```

## Connecting a client

- Register the containerized server with Claude Code:

    ```bash
    claude mcp add --scope project --transport http \
        calculator-mcp http://127.0.0.1:8080/mcp
    ```

## Multi-architecture builds

```bash
docker buildx build --platform linux/amd64,linux/arm64 \
    --build-arg VERSION="$(poetry version -s)" \
    -t "calculator-mcp:$(poetry version -s)" .
```

Building `linux/amd64` on Apple Silicon runs the builder stage under QEMU
emulation, which is correct but noticeably slower.
