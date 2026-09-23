# Demo

This file provides commands to be used during the demo of this project
running in Azure Container App.

## AZ Commands

1. Find out if there is an active replica:

```bash
az containerapp replica list \
  --name "ca-mathmcp-lab" \
  --resource-group "rg-rgomesapp-lab" \
  --output table
az containerapp replica list \
  --name "ca-nettools-lab" \
  --resource-group "rg-rgomesapp-lab" \
  --output table
```

2. List revisions:

```bash
az containerapp revision list \
  --name "ca-mathmcp-lab" \
  --resource-group "rg-rgomesapp-lab" \
  --output table
az containerapp revision list \
  --name "ca-nettools-lab" \
  --resource-group "rg-rgomesapp-lab" \
  --output table
```

3. Ensure at least 1 (one) replica running:

```bash
az containerapp update \
  -n "ca-mathmcp-lab" \
  -g "rg-rgomesapp-lab" \
  --min-replicas 1
az containerapp update \
  -n "ca-nettools-lab" \
  -g "rg-rgomesapp-lab" \
  --min-replicas 1
```

4. Show image deployed to the container app:

```bash
az containerapp show \
  --name "ca-mathmcp-lab" \
  --resource-group "rg-rgomesapp-lab" \
  --query "properties.template.containers[0].image" \
  --output tsv
az containerapp show \
  --name "ca-nettools-lab" \
  --resource-group "rg-rgomesapp-lab" \
  --query "properties.template.containers[0].image" \
  --output tsv
  # if it is mcr.microsoft.com/k8se/quickstart:latest, then the calculator-mcp 
  # image has not been deployed yet.
```

5. Show the conatiner FQDN:

```bash
az containerapp show \
  --name "ca-mathmcp-lab" \
  --resource-group "rg-rgomesapp-lab" \
  --query "properties.configuration.ingress.fqdn" \
  --output tsv
az containerapp show \
  --name "ca-nettools-lab" \
  --resource-group "rg-rgomesapp-lab" \
  --query "properties.configuration.ingress.fqdn" \
  --output tsv
```

6. Connect to the `mathmcp debug` container:

```bash
az containerapp debug \
  -n "ca-mathmcp-lab" \
  -g "rg-rgomesapp-lab" 
```

## From the `nettools` container

1. Connect to the `nettools` console:

```bash
az containerapp exec \
  --name "ca-nettools-lab" \
  --resource-group "rg-rgomesapp-lab" \
  --command /bin/bash
```

2. Health check:

```bash
curl -v http://ca-mathmcp-lab/health

telnet ca-mathmcp-lab 80
GET /health HTTP/1.1
Host: ca-mathmcp-lab
```

3. Show the MCP server name and other information:

```bash
# Modern MCP protocol - Stateless
curl -sS "http://ca-mathmcp-lab/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -H "Mcp-Method: server/discover" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "server/discover",
    "params": {
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientInfo": {"name": "curl", "version": "1.0"},
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  }' | jq .

# Modern MCP protocol - Stateless (debug/vrebose/trace)
curl -v --trace-ascii trace.log "http://ca-mathmcp-lab/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -H "Mcp-Method: server/discover" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "server/discover",
    "params": {
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientInfo": {"name": "curl", "version": "1.0"},
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  }'  | jq .

# Old MCP ptotocol - Stateful
curl -s http://ca-mathmcp-lab/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":3,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"1"}}}' \
  | sed -n 's/^data://p' | jq .
```

4. List the MCP tools:

```bash
# Modern MCP protocol
curl -sS http://ca-mathmcp-lab/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Protocol-Version: 2026-07-28" \
  -H "Mcp-Method: tools/list" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientInfo": {"name": "curl", "version": "1.0"},
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  }' | jq .

# Legacy MCP protocol
curl -s http://ca-mathmcp-lab/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  | sed -n 's/^data://p' | jq .
```

## Don't forget to bring replicas down to 0 (zero)

```bash
az containerapp update \
  -n "ca-mathmcp-lab" \
  -g "rg-rgomesapp-lab" \
  --min-replicas 0
az containerapp update \
  -n "ca-nettools-lab" \
  -g "rg-rgomesapp-lab" \
  --min-replicas 0
```
