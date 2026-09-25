# Miscellaneous

This file contains miscellaneous information found during development.

## Address Zscaler Certificate Issues

If the HTTPS traffic (https://rubens-calculator-mcp.fastmcp.app) is going
through Zscaler (a corporate proxy/security appliance), which intercepts SSL
connections and re-signs certificates with its own CA, then Python's
certificate bundle won't trust the Zscaler Root CA.

1. Add the Zscaler root CA to your environment

    ```bash
    # Export the Zscaler root CA
    openssl s_client -connect rubens-calculator-mcp.fastmcp.app:443 \
        -showcerts </dev/null 2>/dev/null \
        | awk '/Zscaler Root CA/,/END CERTIFICATE/' > /tmp/zscaler-root.pem

    # Point Python/httpx to a combined CA bundle
    export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")
    cat /tmp/zscaler-root.pem >> "$SSL_CERT_FILE"
    ```

2. Or set SSL_CERT_FILE to your system's CA bundle if it already includes
   Zscaler:

    ```bash
    export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
    ```

3. Configure the OAuth token storage encryption key:

    ```bash
    export OAUTH_STORAGE_ENCRYPTION_KEY=$(
        poetry run python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    )
    ```

4. Enable Ubuntu WSL to open browser during OAuth flow:

    ```bash
    sudo sh -c 'echo 1 > /proc/sys/fs/binfmt_misc/WSLInterop'
    ```

## PyPI Configuration

- Generate PyPI tokens from account and configure the environment variables
  below:

    ```bash
    ######################################################################
    ## PyPI PERSONAL API TOKEN
    export PYPI_API_TOKEN="<SECRET>"
    export TESTPYPI_API_TOKEN="<SECRET>"
    ```

- Store `pypi` credentials

    ```bash
    poetry config -v pypi-token.pypi "${PYPI_API_TOKEN}"
    poetry config -v pypi-token.testpypi "${TESTPYPI_API_TOKEN}"
    ```

- Publish `wheel` package to `PyPI` repository:

    ```bash
    # publish to TestPyPI
    poetry publish -vvv -r testpypi --build --dry-run
    # publish to PyPI
    poetry publish -vvv --build --dry-run
    ```

## Create Remote GitHub Public Git Repository

- This is how Rubens initialized this project:

    ```bash
    PROJ_NAME=<proj-name>
    git init -b main
    git add .
    git commit -m "initial commit" -a
    gh repo create --homepage "https://github.com/rubensgomes" \
        --public "${PROJ_NAME}"
    git remote add origin "https://github.com/rubensgomes-org/${PROJ_NAME}"
    git push -u origin main
    ```

After the previous steps, go to the GitHub remote repo and create a "release"
branch.

## GitHub Actions Secret

### PYPI_API_TOKEN

The `release` workflow reads an Action secret named `PYPI_API_TOKEN` to
publish the package to PyPI.

- Create an Action repository secret in this repository and name it
  PYPI_API_TOKEN storing the PyPI API token:

    ```text
    Repo's Settings -- Secrets and variables -- Actions -- New repository secret
    ```

### AZURE_CLIENT_SECRET

The `repo-delete` workflow reads an Action secret named
`AZURE_CLIENT_SECRET`, used to sign in to Azure Cloud.

- Create an Action repository secret in this repository and name it
  AZURE_CLIENT_SECRET storing the Azure Service Principal password:

    ```text
    Repo's Settings -- Secrets and variables -- Actions -- New repository secret
    ```

### SONAR_TOKEN

The `build-verify` workflow reads an Action secret named `SONAR_TOKEN`, used
during the SonarCloud analysis.

- Create an Action repository secret in this repository and name it
  SONAR_TOKEN storing the SonarCloud authentication token:

    ```text
    Repo's Settings -- Secrets and variables -- Actions -- New repository secret
    ```

## GitHub Actions Variables

### AZURE_CLIENT_ID

The `repo-delete` workflow reads an Action variable named
`AZURE_CLIENT_ID`, used to sign in to Azure Cloud.

- Create an Action repository variable in this repository and name it
  AZURE_CLIENT_ID storing the Azure Service Principal username:

    ```text
    Repo's Settings -- Secrets and variables -- Actions -- New variable
    ```

### AZURE_SUBSCRIPTION_ID

The `repo-delete` workflow reads an Action variable named
`AZURE_SUBSCRIPTION_ID`, used to sign in to Azure Cloud.

- Create an Action repository variable in this repository and name it
  AZURE_SUBSCRIPTION_ID storing the Azure Subscription ID:

    ```text
    Repo's Settings -- Secrets and variables -- Actions -- New variable
    ```

### AZURE_TENANT_ID

The `repo-delete` workflow reads an Action variable named
`AZURE_TENANT_ID`, used to sign in to Azure Cloud.

- Create an Action repository variable in this repository and name it
  AZURE_TENANT_ID storing the Azure Tenant ID:

    ```text
    Repo's Settings -- Secrets and variables -- Actions -- New variable
    ```

## Deploy MCP Server - FREE

- For more information: <https://docs.prefect.io/v3/get-started>

1. Log in to <https://www.prefect.io/horizon> using GitHub credentials.
2. Deployment: `rubens-calculator-mcp`
3. Endpoint URL: `https://rubens-calculator-mcp.fastmcp.app/mcp`

## Deploy MCP Server with Docker

The container build, configuration, security posture and troubleshooting steps
are documented in [DOCKER.md](./DOCKER.md). This section covers only the host
preparation.

### Linux VPS Configuration

- Install Docker Engine and the Compose plugin, then enable the service:

    ```bash
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io \
        docker-compose-plugin
    sudo systemctl enable --now docker
    sudo usermod -aG docker "$USER"   # log out and back in to take effect
    ```

- Configure firewall

    ```bash
    # The container publishes port 8080 on the host
    sudo firewall-cmd --add-port=8080/tcp --permanent
    sudo firewall-cmd --reload
    ```

- Build and start the server:

    ```bash
    cd "${PROJ_NAME}"
    docker compose up --build -d
    docker compose ps          # STATUS should reach "healthy"
    ```

- Verify:

    ```bash
    curl http://127.0.0.1:8080/health     # -> OK
    ```

- The server speaks plain HTTP with no authentication. Put a TLS-terminating
  reverse proxy in front of it before exposing it to the internet.
