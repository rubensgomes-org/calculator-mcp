# Azure Container App Provision Workflow

This file describes the provision workflow of the Azure Container App used
to deploy and run the Python calculator MCP server.

## ACA Terraform Provisioning

The [azure-iac](https://github.com/rubensgomes-org/azure-iac) is responsible
for provisioning the following resources in order:

1. Resource groups: the container app uses the `rg-rgomesapp-dev` resource
   group
2. Networking: the container app uses the `app` subnet with CIDR
   `10.0.0.0/23`
3. Log Analytics Workspace: the destination for container apps streams logs
4. UAMI (User-Assigned Managed Identity): the container app is assigned this
   UAMI to have RBAC (Role-Based Access Control) over resources like ACR,
   KeyVault, and database.
5. Key Vault: a repository of secrets that the container app may need to use
   in case it needs access to secrets. This step also grants the previously
   created UAMI shared read-only access to the key vault.
6. ACR Registry: location to store the container images used by the
   container app. An AcrPull RBAC is granted to the UAMI created previously to
   allow the container app to pull images from the registry.
7. CAE (Container App Environment): the container app runs inside and is
   managed by the CAE. CAE is responsible for network boundary, logging sink,
   compute allocation model, runtime services. All the container apps in this
   CAE share same network and logging config.
8. ACA: the container app itself is created with a placeholder/bootstrap
   `quickstart` image from MCR (Microsoft Container Registry) until the real
   image is pushed to ACR. An image is required to create a container app.



