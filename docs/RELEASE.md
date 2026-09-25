# Release Process

The release is run from the `release.yml` GitHub Actions workflow. Prior to
running the `release` workflow, several GitHub Actions variables and
secrets must be provisioned in this project's GitHub Actions settings.

**Currently, only Rubens Gomes is authorized to push a release.**

## Prerequisites

- GitHub account
- gh 2.97+

## GitHub Actions Settings

**NOTE:** the environment variables below must be defined in the
user's environment first.

```text
GitHub environment
------------------
  GH_HOST
  GITHUB_USER
  GIT_AUTHOR_EMAIL
  GIT_COMMITTER_EMAIL
  GIT_AUTHOR_NAME

Actions variables to delete and recreate (8):
  AZURE_CLIENT_ID
  AZURE_SUBSCRIPTION_ID
  AZURE_TENANT_ID
  TF_VAR_BACKEND_RESOURCE_GROUP_NAME
  TF_VAR_CONTAINER_NAME
  TF_VAR_LOCATION
  TF_VAR_STORAGE_ACCOUNT_ID
  TF_VAR_TARGET_PORT

Actions secrets to delete and recreate (3):
  PYPI_API_TOKEN
  AZURE_CLIENT_SECRET
  SONAR_TOKEN
```

- Set up the GitHub Action Secrets and Variables

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    ./scripts/initvars.sh -dv
    ```

## Starting a Release

- From the project `GitHub Actions` page run the `release` workflow.

---
Author: [Rubens Gomes](https://rubensgomes.com/)