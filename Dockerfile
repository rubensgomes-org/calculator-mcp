# syntax=docker/dockerfile:1
#
# =============================================================================
# NOTE: This file was generated with the assistance of an AI tool.
# =============================================================================
#
# Calculator MCP Server — multi-stage container image.
#
#   builder : installs the pinned runtime dependencies from poetry.lock into
#             /opt/venv, builds the project wheel with poetry-core, and
#             installs that wheel into the same virtual environment.
#   runtime : the same base image, running as a non-root user, carrying only
#             /opt/venv from the builder.
#
# Build:  docker build --build-arg VERSION="$(poetry version -s)" \
#             -t "calculator-mcp:$(poetry version -s)" -t calculator-mcp:latest .
# Run:    docker run --rm -p 9999:9000 "calculator-mcp:$(poetry version -s)"
# Verify: curl http://127.0.0.1:9999/health   ->   OK
# =============================================================================

# Both stages MUST use the identical base image. The runtime stage copies the
# virtual environment verbatim, so its pyvenv.cfg and console-script shebangs
# must keep pointing at the same interpreter.
ARG PYTHON_IMAGE=python:3.14-slim-trixie

# -----------------------------------------------------------------------------
# Stage 1 — builder
# -----------------------------------------------------------------------------
FROM ${PYTHON_IMAGE} AS builder

# Matches the Poetry release that generated poetry.lock, so the lock is
# consumed as-is rather than re-resolved.
ARG POETRY_VERSION=2.4.1

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH

WORKDIR /build

# The application virtual environment. Poetry honours VIRTUAL_ENV and installs
# into it. /opt/venv is an absolute path reused verbatim by the runtime stage.
RUN python -m venv /opt/venv

# Poetry is installed into the *system* interpreter, never into /opt/venv, so
# it is not carried into the runtime image.
RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    /usr/local/bin/python -m pip install "poetry==${POETRY_VERSION}"

# --- dependency layer: invalidated only by pyproject.toml / poetry.lock ------
COPY pyproject.toml poetry.lock ./

# pyproject.toml declares readme = "README.md". A placeholder keeps edits to
# the real README from invalidating this expensive layer; the real file is
# copied below, before poetry build reads it for wheel metadata.
RUN touch README.md

# poetry check --lock fails the build when poetry.lock is stale with respect
# to pyproject.toml, so the image can never ship unpinned dependencies.
#
# --only main excludes the dev dependencies even though they are declared in a
# PEP 735 [dependency-groups] table: Poetry 2.4 records groups = ["dev"] for
# those packages in poetry.lock.
#
# poetry export is deliberately not used — that command moved out of Poetry
# into the separate poetry-plugin-export package in Poetry 2.x.
RUN --mount=type=cache,target=/root/.cache/pypoetry,sharing=locked \
    poetry check --lock \
 && poetry install --only main --no-root

# --- project layer: invalidated by source changes ---------------------------
COPY README.md LICENSE ./
COPY src ./src

RUN poetry build --format wheel

# config.yaml is package data loaded at import time via importlib.resources,
# so a packaging regression would only surface when the container starts.
# Fail the build here instead.
RUN python -c "import glob, zipfile; \
w = glob.glob('dist/*.whl')[0]; \
names = zipfile.ZipFile(w).namelist(); \
assert 'calculator_mcp/config.yaml' in names, names; \
print('OK: config.yaml present in', w)"

# Dependencies are already pinned above, so --no-deps --no-index guarantees
# this step resolves nothing over the network.
RUN /opt/venv/bin/pip install --no-cache-dir --no-deps --no-index dist/*.whl

# Smoke-test the built artifact before it reaches the runtime stage.
RUN /opt/venv/bin/python -c \
      "from importlib.metadata import version; print('dist version:', version('calculator-mcp-rubens'))" \
 && /opt/venv/bin/python -c \
      "from calculator_mcp.config import get_host, get_port, get_transport; \
print('bind:', get_transport(), get_host(), get_port())"

# -----------------------------------------------------------------------------
# Stage 2 — runtime
# -----------------------------------------------------------------------------
FROM ${PYTHON_IMAGE} AS runtime

# Deliberately NOT a real version number. This only feeds the OCI label below,
# and a plausible-looking default would silently drift from pyproject.toml on
# every release. Pass --build-arg VERSION="$(poetry version -s)" to set it.
ARG VERSION=0.0.0-dev

LABEL org.opencontainers.image.title="calculator-mcp" \
      org.opencontainers.image.description="MCP server exposing 16 calculator tools over Streamable HTTP" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.source="https://github.com/rubensgomes/calculator-mcp" \
      org.opencontainers.image.url="https://github.com/rubensgomes/calculator-mcp" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.authors="Rubens Gomes <rubens.s.gomes@gmail.com>"

# FASTMCP_SHOW_SERVER_BANNER / FASTMCP_CHECK_FOR_UPDATES suppress the startup
# banner, which otherwise performs a blocking HTTPS request to pypi.org and
# writes a cache file under $HOME on every container start.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    HOME=/home/app \
    FASTMCP_SHOW_SERVER_BANNER=false \
    FASTMCP_CHECK_FOR_UPDATES=off

# Non-root service account with a fixed uid/gid, stable for volume ownership
# and for Kubernetes runAsUser.
RUN groupadd --system --gid 1001 app \
 && useradd --system --uid 1001 --gid 1001 \
            --create-home --home-dir /home/app \
            --shell /usr/sbin/nologin app

# Owned by root and readable by everyone: the application cannot mutate its
# own dependencies.
COPY --from=builder --chown=root:root /opt/venv /opt/venv

USER app
WORKDIR /home/app

EXPOSE 9000

# python:*-slim ships neither curl nor wget, so the probe uses the standard
# library. 127.0.0.1 is reachable because the server binds 0.0.0.0.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import sys, urllib.request; r = urllib.request.urlopen('http://127.0.0.1:9000/health', timeout=4); sys.exit(0 if r.status == 200 and r.read() == b'OK' else 1)"]

# Exec form, so the console script becomes PID 1 and receives SIGTERM
# directly from `docker stop`.
CMD ["calculator-mcp"]
