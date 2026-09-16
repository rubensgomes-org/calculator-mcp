# Release Process

**Currently, only Rubens Gomes is authorized to push a release**

## Prerequisites

1. Ensure the following packages and tools are installed:

    - coreutils package
    - dnsutils package
    - curl 8.7.1 or later
    - gawk 5.4.1 or later
    - gh version 2.97.0 or later (GitHub CLI tool)
    - git version 2.55.0 or later
    - grep version 3.11, 2.6.0-FreeBSD, or later

## Environment Variables

The release process is done on a UNIX machine using a "Claude Code" custom
skill `.claude/skills/pypi-plan-rel/SKILL.md`. Therefore, it is expected that a
`Claude Code` CLI session is running with access to underlying `bash` shell and
the following environment variables:

- GIT_AUTHOR_NAME
- GIT_AUTHOR_EMAIL
- GIT_COMMITTER_EMAIL
- GITHUB_USER
- GITHUB_TOKEN
- GH_TOKEN (should be same as GITHUB_TOKEN)
- PYPI_API_TOKEN

## Starting a Release

- The release plan is generated/executed within `Claude Code`. You must start
  `Claude Code`, and run skill command `/pypi-plan-rel` from within Claude Code:

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    claude --debug --ide  --verbose
    # Claude Code edit mode command:
    /pypi-plan-rel rubensgomes-org/calculator-mcp
    ```

---
Author: [Rubens Gomes](https://rubensgomes.com/)