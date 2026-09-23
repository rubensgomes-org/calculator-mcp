# Demo

This file provides commands to be used during the demo of this project 
running in Azure Container App.

## AZ Commands

- Find out if there is an active replica of this container:

```bash
az containerapp replica list \
  --name "ca-mathmcp-dev" \
  --resource-group "rg-rgomesapp-dev" \
  --output table
```

- To see the current image deployed to the container app:

```bash
az containerapp show \
  --name "ca-mathmcp-dev" \
  --resource-group "rg-rgomesapp-dev" \
  --query "properties.template.containers[0].image" \
  --output tsv
  # if it is mcr.microsoft.com/k8se/quickstart:latest, then the calculator-mcp 
  # image has not been deployed yet.
```

- Find the conatiner FQDN:

```bash
az containerapp show \
  --name "ca-mathmcp-dev" \
  --resource-group "rg-rgomesapp-dev" \
  --query "properties.configuration.ingress.fqdn" \
  --output tsv
```

- Connect to the `debug` container:

```bash
az containerapp debug \
  -n "ca-mathmcp-dev" \
  -g "rg-rgomesapp-dev" 
```

- It is better for the demo to keep 1 (one) replica running:

```bash
az containerapp update \
  -n "ca-mathmcp-dev" \
  -g "rg-rgomesapp-dev" \
  --min-replicas 1
```

- Returns the server name and other information:

```bash
# Handshake: returns the server name, version and capabilities
curl -s http://ca-mathmcp-dev/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":3,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"1"}}}' \
  | sed -n 's/^data://p' | jq .
```

- List the MCP tools:

```bash
# List the tools
curl -s http://ca-mathmcp-dev/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  | sed -n 's/^data://p' | jq .
```
