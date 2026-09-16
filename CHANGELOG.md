# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.3] - 2026-09-16

### Changed

- Docker container now publishes on host port `9999` instead of `9000`
  (internal container port and `config.yaml` remain `9000`).

## [0.0.2] - 2026-09-16

### Added

- Initial release: MCP server exposing 16 arithmetic tools over Streamable
  HTTP, with optional OAuth-protected transport.
- Docker image with health check endpoint.
