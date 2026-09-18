# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
