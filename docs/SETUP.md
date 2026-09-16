# Setup

This file describes steps to set up your local Python development environment.

## Prerequisites

The following tools and versions are required:

- Ubuntu Linux 26.04+ LTS or macOS 26.6.2+
- gh version 2.100.0+ (GitHub CLI tool)
- git version 2.55.0+
- isort 9.0.1+
- pip 26.2.1+
- pipx 1.17.2+
- poetry 2.4.3+
- pyenv 2.8.5+
- pylint 4.0.8+
- pytest 9.1.1+
- python 3.14.7+
- uv 0.10.7+

Optional Tools:

- Claude Code 2.1.273+ (as AI Assistant during development)
- Docker 23+ with the buildx and compose plugins (for running the server in a
  container)

## Clone Git Repository

**Clone the repository:**

   ```bash
   git clone https://github.com/rubensgomes-org/calculator-mcp
   cd calculator-mcp
   ```

---

## Installing Tools in User's Environment

### `pyenv`

- Install `pyenv` as follows. Refer
  to [Getting Pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#a-getting-pyenv):

    ```bash
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    ```

- Set up PATH environment for `pyenv` bin folder as follows. Refer
  to [Set up shell environment for Pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#b-set-up-your-shell-environment-for-pyenv):

   ```bash
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
   echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
   echo 'eval "$(pyenv init - bash)"' >> ~/.bash_profile
   ```

### `python`

- Get the latest `python` 3.14+ version using `pyenv` as follows:

    ```bash
    pyenv install --list | grep '^[[:space:]]*3.1[4-9]'
    ```

- Install the latest `python` 3.14 using `pyenv` as follows:

    ```bash
    # assuming 3.14.7 is the latest python 3.14 release.
    pyenv install "3.14.7"
    ```

- Configure the global `python` version:

    ```bash
    # assuming 3.14.7 is the latest python 3.14 release.
    pyenv global "3.14.7"
    ```

- Check the installed `python` version:

    ```bash
    python --version
    ```

### `pipx`

- Install `pipx` (macOS), and ensure PATH is properly configured:

    ```bash
    # macOS brew
    brew install pipx
    pipx ensurepath
    ```

- Install `pipx` (Linux Ubuntu using `apt`), and ensure PATH is properly
  configured:

    ```bash
    # Ubuntu Linux apt.
    sudo apt update
    sudo apt install pipx
    pipx ensurepath
    ```

- Check the installed `pipx` version:

    ```bash
    pipx --version
    ```

### `poetry` `pylint` `pytest` ...

- Install several required utilities:

    ```bash
    pipx install isort
    pipx install poethepoet
    pipx install poetry
    pipx install pylint
    pipx install pytest
    pipx install uv
    uv tool install cookiecutter
    ```

- Upgrade the packages installed using `pipx`:

    ```bash
    pipx upgrade isort
    pipx upgrade poethepoet
    pipx upgrade poetry
    pipx upgrade pylint
    pipx upgrade pytest
    pipx upgrade uv
    uv tool upgrade cookiecutter
    ```

- Check the installed versions:

    ```bash
    poetry --version
    pylint --version
    pytest --version
    ```

### `Claude Code`

- Install `Claude Code` as an AI Coding Assistant:

    ```bash
    curl -fsSL https://claude.ai/install.sh | bash
    ```

- Clear the cache of any previous stale `Claude Code` installation:

    ```bash
    hash -d claude   # clears cached location for 'claude' only
    # if it says 'not found', just run:
    hash -r          # clears the whole cache
    ```

- Display the `Claude Code` version and help:

    ```bash
    claude --version
    claude --help
    ```

- Update `Claude Code`:

    ```bash
    claude update
    ```

- Run `Claude Code` using the `opus` LLM:

    ```bash
    # open project from IDE (e.g., PyCharm)
    # switch to the project folder, and type:
    claude --verbose --debug --model "opus" --ide
    ```

---

## Poetry Virtual Environment

### Create Poetry Virtual Environment

- The `poetry install` command below will automatically create a `poetry`
  `venv` (virtual environment) folder and install all the dependencies and
  tools listed in the project `pyproject.toml` file:

    ```bash
    # change to project git local directory for this project
    cd $(git rev-parse --show-toplevel) || exit
    poetry install
    ```

- To show all the packages and dependencies used by the project:

    ```bash
    # change to project git local directory for this project
    cd $(git rev-parse --show-toplevel) || exit
    poetry show
    ```

- To find out the temporary location of `poetry` installs all packages:

    ```bash
    # change to project git local directory for this project
    cd $(git rev-parse --show-toplevel) || exit
    # below is the location of poetry virtual environment installation folder
    poetry env info --path
    ```

- Activate virtual environment:

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    eval $(poetry env activate)
    ```

- De-activate the virtual environment:

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    deactivate
    ```

### Add Dev and Test Dependencies

- Add the following dependencies to the `pyproject.toml` `dev` and `test`
  dependency groups and install them in the Poetry virtual environment:

    ```bash
    poetry add --dev black
    poetry add --dev mypy
    poetry add --dev types-pyyaml
    poetry add --group test coverage
    poetry add --group test pytest-asyncio
    poetry add --group test pytest-cov
    ```

### Update Poetry Virtual Environment

- Update virtual environment:

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    # poetry automatically uses the existing virtual environment to
    # install/update packages
    poetry update
    # display information about virtual environment
    poetry env info
    poetry show
    ```

### Remove Poetry Virtual Environment

- Remove poetry virtual environment:

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    poetry env remove --all
    ```

## Common Commands

**Note**: You must have previously created and configured a clean virtual
environment to successfully run the following commands.

- Format, lint, type check, sort imports:

    ```bash
    # Format code
    poetry run black src/ tests/ --target-version py314

    # Lint
    poetry run pylint src/

    # Type checking
    poetry run mypy src/

    # Sort imports
    poetry run isort src/ tests/
    ```

- Different commands to run tests:

    ```bash
    # Run all tests
    poetry run pytest

    # Run with coverage
    poetry run pytest --cov=src/ --cov-report=term-missing

    # Run specific test module
    poetry run pytest tests/<module-name>
    ```

- Miscellaneous `poetry` commands:

    ```bash
    # Ensure at the top of the project root folder
    cd $(git rev-parse --show-toplevel) || exit
    # to add runtime dependencies to pyproject.toml
    poetry add <dependency>
    # to add development dependencies to pyproject.toml
    poetry add --dev <dependency>
    ```

- Command to upgrade the packages in the `pyproject.toml`:

    ```bash
    cd $(git rev-parse --show-toplevel) || exit
    poetry update -vv
    poetry lock --regenerate -vv
    ```

## Running the Server

There are three ways to start the server:

1. **Console script** (installed by Poetry):

    ```bash
    # requires poetry to be installed
    poetry install # only needed once
    poetry run calculator-mcp
    ```

2. **As a Python module:**

    ```bash
    # requires poetry to be installed
    poetry install # only needed once
    eval $(poetry env activate)
    python -m calculator_mcp
    deactivate
    ```

3. **With a custom configuration:**

    ```bash
    # requires poetry to be installed
    poetry install # only needed once
    export CALCULATOR_MCP_CONFIG=/path/to/your/config.yaml
    poetry run calculator-mcp
    ```

## Running the Server with Docker

The server can also run as a container. See [DOCKER.md](./DOCKER.md) for
the full reference.

- **Build the image:**

    ```bash
    # requires Docker to be installed and running
    docker build --build-arg VERSION="$(poetry version -s)" \
        -t "calculator-mcp:$(poetry version -s)" -t calculator-mcp:latest .
    ```

- **Run the container:**

    ```bash
    docker run -d --name calculator-mcp -p 9000:9000 \
        --restart unless-stopped "calculator-mcp:$(poetry version -s)"
    ```

- **Verify it is up:**

    ```bash
    curl http://127.0.0.1:9000/health     # -> OK
    ```

- To stop the running container:

    ```bash
    docker stop calculator-mcp
    docker rm calculator-mcp
    ```

- **With Docker Compose:**

    ```bash
    docker compose up --build -d
    docker compose logs -f calculator-mcp
    docker compose down
    ```

Notes:

- The container listens on `0.0.0.0:9000`, per the bundled `config.yaml`.
- The MCP endpoint is `http://127.0.0.1:9000/mcp`.
- The server runs as a non-root user (`uid=1001`).
- To use a custom configuration, mount it and set `CALCULATOR_MCP_CONFIG`
  to the mounted path.

## Running the Client

A sample integration test client is provided in `tests/integration/client.py`
to demonstrate the MCP protocol with the server. It lists all available tools
and calls each one with sample arguments.

**Important:** The server must be running before you start the client. See
[Running the Server](#running-the-server) above.

- **Run the client:** to hit this MCP server deployed at
  <https://rubens-calculator-mcp.fastmcp.app/mcp>

    ```bash
    # requires poetry to be installed
    poetry install # only needed once
    eval $(poetry env activate)
    python tests/integration/client.py
    deactivate
    ```

## Add MCP Server to Claude Code

- Add the MCP server to Claude Code using project scope. The file `.mcp.json` is
  added to the project root folder:

    ```bash
    # It is assumed that the MCP server is running on http://127.0.0.1:9000
    cd $(git rev-parse --show-toplevel) || exit
    claude mcp add \
        --scope project \
        --transport http \
        calculator-mcp http://127.0.0.1:9000/mcp
    ```

## MCP Protocol

For further information about `MCP` refer to [MCP Protocol](./MCP.md).

## Address ZScaler Certificates Issues

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

## PyCharm IDE Development Environment

- First, ensure you have completed all the previous setup steps in this
  document.

1. Open the project `<proj-name>` folder using `PyCharm`
2. Follow instructions
   to [Create a Poetry environment](https://www.jetbrains.com/help/pycharm/poetry.html#poetry-env)
    - Click on the Python Interpreter Selector to "Add New Interpreter"
    - Select "Add Local Interpreter..."
    - Select "Poetry Environment"
    - Ensure "Poetry executable" (e.g., ${HOME}/.local/bin/poetry)
    - Ensure "Base interpreter" is `poetry` and the right Python executable.
    - Enter `Python Integrated Tools`
    - Under `Testing` > `Default test runner` select `pytest`
3. Open `PyCharm` > `Terminal` to go to venv prompt
    - Ensure .venv correct settings:

    ```shell
    poetry env info
    ```

### Edit Configurations in PyCharm

1. Menu: Run -> Edit Configurations...
2. Ensure "Run" drop-down menu shows "poetry (<proj-name>) Python 3.14.7
3. Click: "+" -> Python
4. Select: "module" from the script/module drop-down menu
5. Type: "<proj-name>" in the module

### Run `<proj-name>` in DEBUG mode from within PyCharm

Once the above "Edit Configurations in PyCharm" are configure:

1. Menu: Run -> Debug...
2. Select `<proj-name>` and debug

## PyPI Configuration

- Generate PyPI tokens from account and configure below environment variables:

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
    git remote add origin "https://github.com/rubensgomes/${PROJ_NAME}"
    git push -u origin main
    ```

After previous steps go to GitHub remote repo and create a "release" branch.

## Deploy MCP Server

- For more information: <https://docs.prefect.io/v3/get-started>

1. Login to <https://www.prefect.io/horizon> using GitHub credentials.

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
    # The MCP server listens on port 9000
    sudo firewall-cmd --add-port=9000/tcp --permanent
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
    curl http://127.0.0.1:9000/health     # -> OK
    ```

- The server speaks plain HTTP with no authentication. Put a TLS-terminating
  reverse proxy in front of it before exposing it to the internet.