# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## How this file is used

`.github/workflows/release.yml` extracts the section matching the version
being released and uses it verbatim as the GitHub Release notes. An empty or
missing section fails the run, so the section must exist before the release
is cut.

The order is:

1. Write what changed under `[Unreleased]`, commit, and push to `main`.
2. Run the `release` workflow.

It renames `[Unreleased]` to the version being released, adds a fresh empty
`[Unreleased]` above it, and pushes that change to `main` itself. It rejects
an `[Unreleased]` section that still holds only the empty `### Added` /
`### Changed` / `### Fixed` skeleton, since there is nothing to rename.

## [Unreleased]

### Added

- Colored log level names in console output via `colorlog`; plain when
  stderr is not a terminal or `NO_COLOR` is set.
- `uvicorn` logger in the bundled and sample configs, so server startup and
  error logs use the project's log format.

### Changed

- Log format adds source file and line number; timestamps show time only.
- `mcp.*` and `httpx` loggers default to `INFO`, and `root` to `WARNING`.
- FastMCP and uvicorn logs use the project's log format instead of their
  own console handlers.
- `config.yaml` is parsed once into typed pydantic models by `get_config()`,
  replacing the `get_*()` and `is_oauth()` getters; an invalid
  `server.transport` now fails validation at startup.
- Only the `http` transport is supported; `stdio` was removed from
  `main.py` and the integration client.
- Logging is configured once at startup, by `main()` or the server lifespan,
  instead of on import of `config.py`.

### Fixed

## [0.0.19] - 2026-09-24

### Added

- `config/config_local.yaml` and `config/config_remote.yaml`: sample
  configurations for the local and Horizon-hosted integration tests.

### Changed

- `README.md`: split into Installation, Configuration, Running and Usage
  sections; added clone-based install, run and integration test steps.
- Bundled `config.yaml`: shortened comments and reordered `server` keys.
- `tests/integration/client.py`: removed the initial `ping()` call.

### Fixed

## [0.0.18] - 2026-09-24

### Added

- `.github/dependabot.yml`: daily version updates for Poetry dependencies
  (minor and patch grouped) and GitHub Actions.
- `pip-audit` dev dependency for dependency vulnerability scanning.
- `.github/workflows/aca-create.yml`: passes
  `health_probe_paths: '{"mathmcp":"/health"}'` so ACA probes `/health`
  over HTTP (requires the next `azure-iac` `v0` release).

### Changed

- Bundled `config.yaml`: all loggers, including `root`, default to `DEBUG`;
  client section documents the Horizon-hosted OAuth endpoint.
- `README.md`: removed the inlined `config.yaml` and replaced the curl
  examples with Modern Era `server/discover` and `tools/list` requests.
- `docs/DEMO.md`, `docs/SETUP.md`, `docs/MCP.md`: added demo commands and
  Prefect Horizon deployment details.
- Bumped `uv` dev dependency to `>=0.12.18`.
- Bumped `fastmcp` dependency to `>=4.0.7`.
- `release.yml`: a `verify` job runs the `build-verify` checks and tests;
  the release job starts only after it passes.
- `Dockerfile`: clarified comments on the dependency layer, `ENV`,
  `EXPOSE` and `HEALTHCHECK` (the latter two are ignored by ACA).
- `docs/DOCKER.md`: environment variables table converted to a list;
  `FASTMCP_SHOW_SERVER_BANNER` documented as `true`.
- `README.md`: installation and protocol-era notes reworded.

### Removed

- `FASTMCP_STATELESS_HTTP` from the `Dockerfile`; `server.stateless` in
  `config.yaml` controls stateless mode.
- `docker-compose.yml`: `environment` and `healthcheck` blocks that
  duplicated the image.
- `.mcp.json`, `docs/oauth-troubleshooting.md` and the `pypi-plan-rel`
  Claude Code skill.

### Fixed

- `pip-audit` failure on `diskcache` (PYSEC-2026-2447): the integration
  client stores OAuth tokens in a `FileTreeStore` instead of a `DiskStore`,
  and the `diskcache` and `pathvalidate` test dependencies are removed.

## [0.0.17] - 2026-09-22

### Added

### Changed

- update documentation

### Fixed

## [0.0.16] - 2026-09-22

### Added

### Changed

- `README.md`: restructured the Installation and Legacy Era sections, and
  wrapped long lines to keep Markdown within the 80-character limit.

### Fixed

- `README.md`: fixed typos (`depdencies`, `serever`), a wrong install
  comment, and a broken reference to a nonexistent step 4 in the
  `Mcp-Session-Id` reuse note.

## [0.0.15] - 2026-09-21

### Added

### Changed

- `.github/workflows/build-deploy.yml`, `aca-create.yml` and
  `repo-delete.yml` now derive the registry name from the selected
  environment instead of taking it as a manual input.
- `.github/workflows/aca-create.yml` and `aca-destroy.yml`: removed the
  `app_name` input; the app name is now the constant `mathmcp`.

### Fixed

## [0.0.13] - 2026-09-21

### Added

### Changed

- `fastmcp` bumped to `>=4.0.5`; `calculator-lib-rubens` upper bound
  narrowed to `<1.0.0`; `py-key-value-aio` bumped to `>=0.4.6` and no
  longer pins the `[disk]` extra; added `cryptography` and `key-value`
  dependencies.

### Fixed

## [0.0.12] - 2026-09-21

### Added

- `docs/AZ_CMD.md`: commands to show the ACA scale setting, shut down all
  replicas, open a debug container shell, and find the HTTP endpoint URL.

### Changed

- `.github/workflows/build-deploy.yml` now calls the
  `acr-build-push-python.yml` reusable workflow instead of
  `acr-build-deploy-python.yml`.
- `README.md`: license/AI-disclaimer badges now link to GitHub instead of
  local files; MCP usage steps note their JSON-RPC method names.
- `.github/workflows/acr-repo-delete.yml` renamed to `repo-delete.yml`.

### Fixed

## [0.0.11] - 2026-09-20

### Added

- `scripts/initvars.sh`: manages the `TF_VAR_TARGET_PORT` repository
  variable.
- `docs/AZ_CMD.md`: commands to delete an ACR image and show the ACA
  ingress target port.

### Changed

- Application now listens on port `8080` instead of `9000`, so its
  bind port matches the Azure Container Apps ingress target port
  (`config.yaml`, `Dockerfile`, `docker-compose.yml`, `README.md`,
  `docs/DOCKER.md`, `docs/SETUP.md`, `docs/MCP.md`, and the
  `pypi-plan-rel` skill).

### Fixed

## [0.0.10] - 2026-09-19

### Added

- `aca-create.yml` and `aca-destroy.yml`: `app_name` input (default
  `mathmcp`), passed to the callee `azure-iac` reusable workflows as `apps`.

### Changed

- `scripts/initvars.sh` no longer manages `TF_VAR_apps`; it deletes the
  variable from the repository instead.
- `scripts/initvars.sh` now creates all Actions variable names upper-cased
  (e.g. `TF_VAR_BACKEND_RESOURCE_GROUP_NAME`), matching how GitHub stores
  them.

### Fixed

## [0.0.9] - 2026-09-19

### Added

- `docs/AZ_CMD.md`: reference of `az acr` CLI commands used in this project.

### Changed

- `aca-create.yml` and `aca-destroy.yml` now call the `azure-iac` reusable
  workflows at `@v0` instead of a pinned patch version.

### Fixed

## [0.0.8] - 2026-09-18

### Added

- `.github/workflows/release.yml` now renames `[Unreleased]` to the release
  version and commits a fresh empty `[Unreleased]` to `main` itself, so
  that step no longer needs to be done manually before running the workflow.
- `.github/workflows/acr-build-deploy.yml`: manually-triggered workflow to
  build the application, publish its container image to an Azure Container
  Registry, and purge orphaned untagged manifests. Requires
  `AZURE_CLIENT_ID`, `AZURE_SUBSCRIPTION_ID`, `AZURE_TENANT_ID` Actions
  variables and an `AZURE_CLIENT_SECRET` Actions secret.

### Fixed

- `Dockerfile` no longer uses BuildKit-only `RUN --mount=type=cache`: `az acr
  build` (ACR Tasks) builds without BuildKit and failed with "the --mount
  option requires BuildKit".

## [0.0.7] - 2026-09-17

### Added

- `.github/workflows/acr-repo-delete.yml`: manually-triggered, destructive
  workflow to delete a repository (all tags and manifests) from an Azure
  Container Registry. Requires `AZURE_CLIENT_ID`, `AZURE_SUBSCRIPTION_ID`,
  `AZURE_TENANT_ID` Actions variables and an `AZURE_CLIENT_SECRET` Actions
  secret.
- `scripts/initvars.sh` and `docs/SETUP.md` now manage the above Azure
  Actions variables/secret.

## [0.0.6] - 2026-09-17

### Added

- sonar-project.properties file
- `.github/workflows/release.yml`: resolves the version, verifies the
  CHANGELOG, builds the package, and publishes it to PyPI and GitHub. Fails
  fast if the resolved tag already exists, instead of failing inside
  `poetry publish`. Bumps `pyproject.toml` to the next patch version and
  pushes it to main after a successful release.

### Fixed

- `docker-compose.yml` healthcheck now also verifies the response body,
  matching the Dockerfile's `HEALTHCHECK`.

## [0.0.5] - 2026-09-17

### Added

- SonarQube static analysis via `pysonar`, run during release when
  `SONAR_TOKEN` is set.

## [0.0.4] - 2026-09-16

### Changed

- README install instructions clarified: recommend `pip cache purge`
  after uninstall, and use `--no-cache-dir -U` on install.

## [0.0.3] - 2026-09-16

### Changed

- Docker container now publishes on host port `9999` instead of `9000`
  (internal container port and `config.yaml` remain `9000`).

## [0.0.2] - 2026-09-16

### Added

- Initial release: MCP server exposing 16 arithmetic tools over Streamable
  HTTP, with optional OAuth-protected transport.
- Docker image with health check endpoint.
