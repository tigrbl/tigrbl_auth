# Docker Local Runtime

This runbook starts a `tigrbl_auth` example runtime on `Tigrcorn` using `uv`
inside Docker and exposes it on `http://127.0.0.1:8001`.

## Build and Run

```powershell
docker build -f docker/Dockerfile.dev-tigrbl -t tigrbl-auth-local:latest .
docker run -d --name tigrbl-auth-local -p 8001:8000 `
  -e AUTHN_ISSUER=http://localhost:8001 `
  -e TIGRBL_AUTH_PROTECTED_RESOURCE_IDENTIFIER=http://localhost:8001/resource `
  -e TIGRBL_AUTH_REQUIRE_TLS=false `
  -e TIGRBL_AUTH_SESSION_COOKIE_FORCE_SECURE=false `
  -e TIGRBL_AUTH_BOOTSTRAP_ADMIN_USERNAME=admin `
  -e TIGRBL_AUTH_BOOTSTRAP_ADMIN_EMAIL=admin@example.test `
  -e TIGRBL_AUTH_BOOTSTRAP_ADMIN_PASSWORD=AdminPass123! `
  -e TIGRBL_AUTH_BOOTSTRAP_ADMIN_FORCE_PASSWORD_CHANGE=true `
  tigrbl-auth-local:latest
```

Equivalent compose workflow:

```powershell
docker compose -f docker/docker-compose.yml up -d --build
```

The local compose runtime now bootstraps a default super-admin identity for the
admin UIX:

- username: `admin`
- email: `admin@example.test`
- password: `AdminPass123!`

The first login is expected to force a password rotation.

Useful container checks:

```powershell
docker ps --filter name=tigrbl-auth-local
docker logs --tail 80 tigrbl-auth-local
```

## CLI

Run the packaged operator CLI inside the container:

```powershell
docker exec tigrbl-auth-local /app/.venv/bin/tigrbl-auth --help
docker exec tigrbl-auth-local /app/.venv/bin/tigrbl-auth serve --server tigrcorn --check --profile production --format json
docker exec tigrbl-auth-local /app/.venv/bin/tigrbl-auth discovery show --repo-root /app --profile production --format json
docker exec tigrbl-auth-local /app/.venv/bin/tigrbl-auth spec validate --kind openrpc --repo-root /app --profile production --format json
```

## REST

Fetch published contracts and discovery metadata:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/openapi.json
Invoke-RestMethod http://127.0.0.1:8001/.well-known/openid-configuration
Invoke-RestMethod http://127.0.0.1:8001/.well-known/jwks.json
Invoke-RestMethod http://127.0.0.1:8001/system/healthz
```

The local Docker runtime sets `AUTHN_ISSUER=http://localhost:8001`, so
`/.well-known/openid-configuration` advertises localhost URLs instead of the
package fallback `https://authn.example.com`.

The image installs the published `tigrcorn` runner profile with `uv sync` and
launches the prebuilt virtual environment directly so runtime startup does not
re-resolve optional extras:

```powershell
/app/.venv/bin/tigrbl-auth serve --server tigrcorn --profile production --host 0.0.0.0 --port 8000 --proxy-headers --no-require-tls
```

List the bootstrapped tenants over REST:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/tenant
```

Admin UIX authentication for the local stack is browser-session based. The local
compose runtime disables the `Secure` cookie bit so the admin session can be
tested over `http://127.0.0.1` without weakening the production default.

## JSON-RPC

Discover the runtime-mounted model RPC methods:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/system/methodz
```

Call the JSON-RPC endpoint:

```powershell
$body = @{
  jsonrpc = "2.0"
  id = 1
  method = "Tenant.list"
  params = @{}
} | ConvertTo-Json -Depth 6

Invoke-RestMethod -Uri http://127.0.0.1:8001/rpc -Method Post -ContentType "application/json" -Body $body
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

$user = Invoke-RestMethod -Uri http://127.0.0.1:8001/rpc -Method Post -ContentType "application/json" -Body $userBody

$keyBody = @{
  jsonrpc = "2.0"
  id = 3
  method = "ApiKey.create"
  params = @{
    label = "rpc-demo-key"
    user_id = $user.result.id
  }
} | ConvertTo-Json -Depth 6

Invoke-RestMethod -Uri http://127.0.0.1:8001/rpc -Method Post -ContentType "application/json" -Body $keyBody
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
