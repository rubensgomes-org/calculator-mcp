---
description: Generate a release plan for the project.
argument-hint: Git repository name (e.g., rubensgomes/calculator-mcp)
---

# Generate Release Plan

1. If no argument is provided, respond with "Error: Git repository name is
   required." and stop.
2. If the argument is provided, check if the $ARGUMENT repository exists.
3. MUST run `scripts/test_github.sh $ARGUMENT`, and ensure it succeeds;
   otherwise, it MUST report error and stop. 
4. MUST update the project documentation files to ensure it is up-to-date with
   the recent code changes 
5. Now, you MUST create a NEW release plan containing following steps:
    - MUST run `poetry run mypy src/` and fix any issues.
    - MUST run `poetry run isort src/ tests/` and fix any issues.
    - MUST run `poetry run black src/ tests/` and fix any issues.
    - MUST run `poetry run pylint src/ tests/` and fix any issues.
    - MUST run `poetry run pytest` and fix any issues.
    - MUST run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` and fix
      any issues.
    - MUST run `docker build --build-arg VERSION="$(poetry version -s)" -t
      "calculator-mcp:$(poetry version -s)" -t calculator-mcp:latest .` and fix
      any issues. The `--build-arg` is required; without it the image's
      `org.opencontainers.image.version` label falls back to `0.0.0-dev`. The
      build fails if `poetry.lock` is stale or if `config.yaml` is missing from
      the wheel.
    - MUST verify the container starts, reports the correct version, and serves
      the health endpoint, and fix any issues:

        ```bash
        VER="$(poetry version -s)"
        docker run -d --name calculator-mcp-rel -p 9000:9000 "calculator-mcp:${VER}"
        sleep 5
        curl -fsS http://127.0.0.1:9000/health   # MUST return OK

        # The image label and the packaged distribution MUST both equal ${VER}.
        test "$(docker inspect "calculator-mcp:${VER}" \
            --format '{{index .Config.Labels "org.opencontainers.image.version"}}')" = "${VER}"
        test "$(docker run --rm "calculator-mcp:${VER}" python -c \
            'from importlib.metadata import version; print(version("calculator-mcp-rubens"))')" = "${VER}"

        docker rm -f calculator-mcp-rel
        ```

    - MUST ensure a `CHANGELOG.md` file exists in the project root folder.
    - MUST update the `CHANGELOG.md` with the current release changes.
    - MUST commit all changes to main, create a new version tag, push, and
      create a GitHub release 
    - MUST run `poetry publish -v` as the VERY LAST step in the release
6. MUST mark off checkboxes as steps in the plan are completed
