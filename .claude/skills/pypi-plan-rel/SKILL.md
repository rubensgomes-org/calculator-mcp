---
name: pypi-plan-rel
description: >-
    Generate a release plan to build, package, and distribute this
    project to PyPI - The Python Package Index. Also, publish a release
    to the project's GitHub repository.
argument-hint: "[owner/repo] (e.g., rubensgomes-org/calculator-mcp)"
disable-model-invocation: true
---

# Generate Release Plan

1. If no argument is provided, respond with "Error: Git repository name is
   required." and stop.
2. Determine the absolute path of the directory containing this `SKILL.md`.
3. Execute the bundled script `scripts/gh-test.sh $ARGUMENTS` using its
   absolute path, and ensure it succeeds; otherwise, it MUST report error
   and stop.
4. Ensure the shell environment has the `PYPI_API_TOKEN` variable set. If
   not, stop and report error.
5. Ensure a `CHANGELOG.md` file exists in the project root folder.
6. Create a release plan containing following steps:
    - run `poetry run isort src/ tests/` and fix any issues.
    - run `poetry run black src/ tests/` and fix any issues.
    - run `poetry run pylint src/ tests/` and fix any issues.
    - run `poetry run mypy src/` and fix any issues.
    - run `poetry run pytest --cov=src` and fix any issues.
7. If the `SONAR_TOKEN` environment variable is set, then run:
    - run `poetry run pysonar` and stop if it fails.
8. Continue with remaing steps:
    - run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` and fix any
      issues.
    - run `docker build --build-arg VERSION="$(poetry version -s)" -t
      "calculator-mcp:$(poetry version -s)" -t calculator-mcp:latest .` and fix
      any issues. The `--build-arg` is required; without it the image's
      `org.opencontainers.image.version` label falls back to `0.0.0-dev`. The
      build fails if `poetry.lock` is stale or if `config.yaml` is missing from
      the wheel.
    - verify the container starts, reports the correct version, and serves the
      health endpoint, and fix any issues:

        ```bash
        VER="$(poetry version -s)"
        docker run -d --name calculator-mcp-rel -p 9999:8080 \
            "calculator-mcp:${VER}"
        sleep 5
        curl -fsS http://127.0.0.1:9999/health   # MUST return OK

        # The image label and the packaged distribution MUST both equal
        # ${VER}.
        LABEL_FMT='{{index .Config.Labels "org.opencontainers.image.version"}}'
        IMAGE_LABEL="$(docker inspect "calculator-mcp:${VER}" \
            --format "${LABEL_FMT}")"
        test "${IMAGE_LABEL}" = "${VER}"

        VERSION_CODE='from importlib.metadata import version; \
            print(version("calculator-mcp-rubens"))'
        PKG_VERSION="$(docker run --rm "calculator-mcp:${VER}" \
            python -c "${VERSION_CODE}")"
        test "${PKG_VERSION}" = "${VER}"

        docker rm -f calculator-mcp-rel
        ```

    - update the project documentation files to ensure they are
      up-to-date with the recent code changes.
    - update the `CHANGELOG.md` with the current release changes.
    - commit all changes to main, create a new version tag, push, and
      create a GitHub release.
    - run `poetry config pypi-token.pypi "$PYPI_API_TOKEN"` to store the
      PyPI credential.
    - run `poetry publish -v` as the VERY LAST step in the release.
9. MUST mark off checkboxes as steps in the plan are completed.
