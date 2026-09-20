# AZ_CMD

This file contains handy az-cli commands used in this project.

## Azure CLI Commands

### CAE Commands

- Shows if the below CAE is provisioned:

    ```bash
    az containerapp env show \
      -g "rg-rgomesapp-dev" \
      -n "cae-rgomes-dev" \
      --query properties.provisioningState
    ```

- List CAEs on a given RG:

    ```bash
    az containerapp env list \
      -g "rg-rgomesapp-dev"
    ```

### ACR commands

- List all the repositories in a registry:

    ```bash
    az acr repository list \
      --name crrgomesdev01 \
      --output json
    ```

- Image tag/version:

    ```bash
    az acr repository show-tags \
      --name crrgomesdev01 \
      --repository dev/calculator-mcp \
      --output table
    # 0.0.9
    ```

- Delete a specific image from the repo:

    ```bash
    az acr repository delete \
      --name crrgomesdev01 \
      --image dev/calculator-mcp:0.0.9
    ```

- Image and registry name:

    ```bash
    az acr repository show \
      --name crrgomesdev01 \
      --repository dev/calculator-mcp \
      --output json
    # crrgomesdev01.azurecr.io
    # dev/calculator-mcp
    ```

- Image Reference:

    ```text
    # <registry>/<image-name>:<tag>
    crrgomesdev01.azurecr.io/dev/calculator-mcp:0.0.9
    ```

## ACA Commands

- Display the container app currently configured ingress target port:

    ```bash
    az containerapp ingress show \
      --name "ca-mathmcp-dev" \
      --resource-group "rg-rgomesapp-dev" \
      --query targetPort
    ```

- Cointainer Appp full settings (image, env vars, resources, scale, ingress,
  registries...)

    ```bash
    # ACA name rg-rgomesmathmcp-dev
    az containerapp show \
      -g "rg-rgomesapp-dev"\
      -n "ca-mathmcp-dev" \
      --output json
    ```

- Just the running image + env vars

    ```bash
    az containerapp show \
      -g "rg-rgomesapp-dev" \
      -n "ca-mathmcp-dev" \
      --query "properties.template.containers[].{image:image, env:env}"
    ```

- Ingress config (external/internal, target port, transport)  

    ```bash
    az containerapp ingress show \
      -g "rg-rgomesapp-dev" \
      -n "ca-mathmcp-dev"
    ```
  
- Registries configured for pulling images, and which identity they use

    ```bash
    az containerapp registry list \
      -g "rg-rgomesapp-dev" \
      -n "ca-mathmcp-dev"
    ```
  
- Managed identity assigned to the app (needed for AcrPull)

    ```bash
    az containerapp identity show \
      -g "rg-rgomesapp-dev" \
      -n "ca-mathmcp-dev"
    ``` 

- Secrets defined on the app (names only, values are not returned)

    ```bash
    az containerapp secret list \
      -g "rg-rgomesapp-dev" \
      -n "ca-mathmcp-dev"
    ```

- Revisions (active/inactive, traffic split, image per revision)

    ```bash
    az containerapp revision list \
      -g "rg-rgomesapp-dev" \
      -n "ca-mathmcp-dev"  \
      --output json
    ```

- Provisioning/health state only

    ```bash
    az containerapp show \
      -g "rg-rgomesapp-dev" \
      -n "ca-mathmcp-dev" \
      --query "{state:properties.provisioningState, fqdn:properties.configuration.ingress.fqdn}"
    ```

- Live log stream

    ```bash
    az containerapp logs show \
      -g "rg-rgomesapp-dev" \
      -n "ca-mathmcp-dev" --follow
    ```

- Show the scale setting provisioned:

```bash
az containerapp revision list \
  -n ca-mathmcp-dev \
  -g "rg-rgomesapp-dev" \
  --query "[].{name:name, active:properties.active, replicas:properties.replicas, provisioningState:properties.provisioningState}" \
  -o table
```

- List live container app replicas:

    ```bash
    az containerapp replica list \
      -n ca-mathmcp-dev \
      -g "rg-rgomesapp-dev"
    ```

- Ensure you have one replica up and running:

    ```bash
    az containerapp update \
      -n ca-mathmcp-dev \
      -g "rg-rgomesapp-dev" \
      --min-replicas 1
    ```

### ACA Troublehooting

- Shell into a container app:

    ```bash
    az containerapp exec \
      --name ca-mathmcp-dev \
      --resource-group "rg-rgomesapp-dev" \
      --command /bin/sh
    ```
