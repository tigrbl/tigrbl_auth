# Docker Local Runtime

This runbook starts the SQLite + Uvicorn `tigrbl_auth` runtime from the
repository Dockerfile and exposes it on `http://127.0.0.1:8000`.

## Build and Run

```powershell
docker build -t tigrbl-auth-local:latest .
docker run -d --name tigrbl-auth-local -p 8000:8000 `
  -e AUTHN_ISSUER=http://localhost:8000 `
  -e TIGRBL_AUTH_PROTECTED_RESOURCE_IDENTIFIER=http://localhost:8000/resource `
  -e TIGRBL_AUTH_REQUIRE_TLS=false `
  tigrbl-auth-local:latest
```

Equivalent compose workflow:

```powershell
docker compose up -d --build
```

Useful container checks:

```powershell
docker ps --filter name=tigrbl-auth-local
docker logs --tail 80 tigrbl-auth-local
```

## CLI

Run the packaged operator CLI inside the container:

```powershell
docker exec tigrbl-auth-local tigrbl-auth --help
docker exec tigrbl-auth-local tigrbl-auth serve --server uvicorn --check --profile production --format json
docker exec tigrbl-auth-local tigrbl-auth discovery show --repo-root /app --profile production --format json
docker exec tigrbl-auth-local tigrbl-auth spec validate --kind openrpc --repo-root /app --profile production --format json
```

## REST

Fetch published contracts and discovery metadata:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/openapi.json
Invoke-RestMethod http://127.0.0.1:8000/.well-known/openid-configuration
Invoke-RestMethod http://127.0.0.1:8000/.well-known/jwks.json
Invoke-RestMethod http://127.0.0.1:8000/system/healthz
```

The local Docker runtime sets `AUTHN_ISSUER=http://localhost:8000`, so
`/.well-known/openid-configuration` advertises localhost URLs instead of the
package fallback `https://authn.example.com`.

List the bootstrapped tenants over REST:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/tenant
```

## JSON-RPC

Discover the runtime-mounted model RPC methods:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/system/methodz
```

Call the JSON-RPC endpoint:

```powershell
$body = @{
  jsonrpc = "2.0"
  id = 1
  method = "Tenant.list"
  params = @{}
} | ConvertTo-Json -Depth 6

Invoke-RestMethod -Uri http://127.0.0.1:8000/rpc -Method Post -ContentType "application/json" -Body $body
```

Create a user, then create an API key for that user:

```powershell
$userBody = @{
  jsonrpc = "2.0"
  id = 2
  method = "User.create"
  params = @{
    username = "rpc-user"
    email = "rpc-user@example.com"
    tenant_id = "ffffffff-0000-0000-0000-000000000000"
  }
} | ConvertTo-Json -Depth 6

$user = Invoke-RestMethod -Uri http://127.0.0.1:8000/rpc -Method Post -ContentType "application/json" -Body $userBody

$keyBody = @{
  jsonrpc = "2.0"
  id = 3
  method = "ApiKey.create"
  params = @{
    label = "rpc-demo-key"
    user_id = $user.result.id
  }
} | ConvertTo-Json -Depth 6

Invoke-RestMethod -Uri http://127.0.0.1:8000/rpc -Method Post -ContentType "application/json" -Body $keyBody
```

The mounted `/rpc` endpoint dispatches Tigrbl model methods such as
`Tenant.list`, `Client.list`, and `TokenRecord.list`. The implementation-backed
admin OpenRPC method catalog is generated and validated through the CLI and
committed OpenRPC specs.

`ApiKey.create` requires `label` and `user_id`; an empty `params` object reaches
the database with a null `label` and fails the `api_keys.label` constraint.

## Stop or Remove

Leave the container running during local verification. To stop it later:

```powershell
docker stop tigrbl-auth-local
docker rm tigrbl-auth-local
```
