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

### Changed

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
