> [!WARNING]
> Archived historical reference. This document is retained for audit history only and is **not** an authoritative current-state artifact.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` for the current source of truth.

# tba_auth — Recommended `serve` Flags

## Scope

This is the **recommended** `serve` surface for the new `tba_auth` package.
It is not a claim that the current package already implements this CLI.

## Command shape

```bash
tba-auth serve <subcommand> [flags]
```

## Recommended subcommands

- `all`
- `public`
- `admin`
- `worker`
- `rpc`
- `rest`

---

## 1) Inherited global flags accepted by `serve`

| Flag | Type | Priority | Meaning |
|---|---|---:|---|
| `-c`, `--config` | path | MUST | Primary config file path |
| `-e`, `--env-file` | path | SHOULD | Optional env-file input |
| `-p`, `--profile` | string | SHOULD | Named configuration profile |
| `--workspace-root` | path | MAY | Resolve package-relative assets from a fixed root |
| `-t`, `--tenant` | string | MUST | Tenant / issuer partition |
| `--issuer` | URL/string | MUST | Canonical issuer identifier |
| `--strict` / `--no-strict` | bool | SHOULD | Enable or disable strict validation |
| `--offline` | bool | MAY | Disable network-dependent checks |
| `-f`, `--format` | string | MAY | Output format selector |
| `-o`, `--output` | path | MAY | Output destination |
| `-v`, `--verbose` | counter | SHOULD | Increase verbosity |
| `-q`, `--quiet` | bool | MAY | Reduce output |
| `--trace` | bool | MAY | Enable trace-level diagnostics |
| `--color` / `--no-color` | bool | MAY | ANSI color control |
| `--fail-fast` / `--no-fail-fast` | bool | MAY | Stop after first fatal startup validation failure |
| `--experimental` | bool | MAY | Enable experimental surface area |
| `-V`, `--version` | bool | SHOULD | Print version |
| `-h`, `--help` | bool | MUST | Print help |

---

## 2) Serve-only runtime / bind flags

| Flag | Type | Applies to | Priority | Meaning |
|---|---|---|---:|---|
| `--host` | host | all | MUST | Bind host |
| `--port` | int | public/admin/rest/rpc/all | MUST | Bind port |
| `--workers` | int | public/admin/rest/rpc/all | SHOULD | Worker count |
| `--reload` | bool | public/admin/rest/rpc/all | SHOULD | Live reload for development |
| `--uds` | path | public/admin/rest/rpc/all | MAY | Unix domain socket path |
| `--root-path` | string | all | SHOULD | ASGI root path |
| `--mount-prefix` | string | all | SHOULD | URL mount prefix |
| `--public-base-url` | URL | all | MUST | External public base URL |
| `--admin-base-url` | URL | all | SHOULD | External admin base URL |
| `--enable-rest` | bool | all | MUST | Enable REST surface |
| `--enable-rpc` | bool | all | SHOULD | Enable JSON-RPC surface |
| `--surface-name` | string | all | MAY | Explicit Tigrbl surface selector |
| `--app-import` | import path | all | MAY | Explicit ASGI app import path override |

---

## 3) Database / storage flags used during serve

| Flag | Type | Priority | Meaning |
|---|---|---:|---|
| `--database-url` | DSN | MUST | Database connection string |
| `--dsn` | DSN | MAY | Alternate DSN spelling |
| `--db-pool-size` | int | SHOULD | Connection pool size |
| `--db-max-overflow` | int | SHOULD | Pool overflow limit |
| `--db-pool-timeout` | seconds | SHOULD | Pool checkout timeout |
| `--db-connect-timeout` | seconds | SHOULD | Initial connect timeout |
| `--db-echo` | bool | MAY | SQL echo for debugging |
| `--db-schema` | string | MAY | Default DB schema |
| `--tenant-aware` | bool | SHOULD | Enable tenant-aware database semantics |
| `--state-dir` | path | MAY | Local runtime state directory |
| `--cache-url` | URL | SHOULD | Cache / coordination backend |
| `--queue-url` | URL | SHOULD | Background queue backend |

---

## 4) TLS / proxy / ingress flags

| Flag | Type | Priority | Meaning |
|---|---|---:|---|
| `--tls-mode` | enum | MUST | TLS mode selector (`off`, `terminate`, `direct`) |
| `--tls-cert-file` | path | MUST when direct TLS | TLS certificate path |
| `--tls-key-file` | path | MUST when direct TLS | TLS private key path |
| `--tls-ca-file` | path | SHOULD | CA certificate path |
| `--tls-min-version` | enum | SHOULD | Minimum TLS version |
| `--tls-cipher-suite` | repeatable string | MAY | Allowed cipher suites |
| `--proxy-headers` | bool | SHOULD | Trust proxy headers |
| `--trusted-proxy` | repeatable CIDR/IP | SHOULD | Trusted proxy list |
| `--forwarded-allow-ips` | repeatable CIDR/IP | SHOULD | Allowed forwarded IP sources |
| `--proxy-mode` | enum | MAY | Explicit proxy behavior (`none`, `edge`, `reencrypt`, `passthrough`) |
| `--hostname-strict` | bool | SHOULD | Enforce hostname / issuer consistency |
| `--insecure-http` | bool | MAY | Allow cleartext HTTP for local development only |
| `--skip-tls-verify` | bool | MAY | Skip outbound TLS verification for upstream checks |

---

## 5) Health / metrics / diagnostics flags

| Flag | Type | Priority | Meaning |
|---|---|---:|---|
| `--health-enabled` | bool | SHOULD | Enable health endpoints |
| `--metrics-enabled` | bool | SHOULD | Enable metrics endpoints |
| `--health-path` | path | SHOULD | Combined health path |
| `--liveness-path` | path | SHOULD | Liveness endpoint path |
| `--readiness-path` | path | SHOULD | Readiness endpoint path |
| `--metrics-path` | path | SHOULD | Metrics endpoint path |
| `--diagnostics-enabled` | bool | MAY | Enable diagnostics surface |
| `--diagnostics-path` | path | MAY | Diagnostics endpoint path |
| `--pprof-enabled` | bool | MAY | Expose profiling endpoints in non-prod only |

---

## 6) Logging / runtime mode flags

| Flag | Type | Priority | Meaning |
|---|---|---:|---|
| `--access-log` | bool | SHOULD | Enable access logs |
| `--log-level` | enum | MUST | Log level selector |
| `--log-format` | enum | SHOULD | Log format (`text`, `json`) |
| `--request-id-header` | string | MAY | Request ID header name |
| `--dev` | bool | SHOULD | Development runtime mode |
| `--optimized` | bool | SHOULD | Production-optimized mode |
| `--graceful-timeout` | seconds | SHOULD | Graceful shutdown timeout |
| `--startup-timeout` | seconds | SHOULD | Startup completion timeout |
| `--shutdown-timeout` | seconds | SHOULD | Shutdown timeout |

---

## 7) Lifecycle / bootstrap-at-start flags

| Flag | Type | Priority | Meaning |
|---|---|---:|---|
| `--auto-migrate` | bool | SHOULD | Run migrations on startup |
| `--require-clean-migrations` | bool | SHOULD | Refuse start on unapplied required migrations |
| `--bootstrap-admin-username` | string | MAY | Initial admin username for controlled bootstrap |
| `--bootstrap-admin-password` | secret | MAY | Initial admin password |
| `--bootstrap-admin-client-id` | string | MAY | Initial admin client ID |
| `--bootstrap-admin-client-secret` | secret | MAY | Initial admin client secret |
| `--masterkey` | secret | SHOULD | Direct masterkey input |
| `--masterkey-from-env` | string/env-name | SHOULD | Read masterkey from env |
| `--masterkey-file` | path | SHOULD | Read masterkey from file |
| `--seed-dev-data` | bool | MAY | Seed development data |
| `--seed-dev-keys` | bool | MAY | Seed development keys |
| `--no-prompt` | bool | SHOULD | Non-interactive execution |
| `--yes` | bool | MAY | Automatic confirmation |

---

## 8) Protocol feature flags recommended on `serve`

| Flag | Type | Priority | Meaning |
|---|---|---:|---|
| `--features` | repeatable string/list | SHOULD | Enable multiple named features |
| `--features-disabled` | repeatable string/list | SHOULD | Disable multiple named features |
| `--feature` | repeatable string | MAY | Single feature toggle |
| `--enable-device-flow` | bool | SHOULD | Enable RFC 8628 device authorization flow |
| `--enable-token-exchange` | bool | SHOULD | Enable RFC 8693 token exchange |
| `--enable-resource-indicators` | bool | SHOULD | Enable RFC 8707 resource indicators |
| `--enable-jwt-at-profile` | bool | SHOULD | Enable RFC 9068 JWT access token profile |
| `--enable-dynamic-client-registration` | bool | SHOULD | Enable RFC 7591 dynamic client registration |
| `--enable-registration-management` | bool | MAY | Enable RFC 7592 registration management |
| `--enable-par` | bool | SHOULD | Enable RFC 9126 pushed authorization requests |
| `--enable-jar` | bool | SHOULD | Enable RFC 9101 JWT-secured authorization requests |
| `--enable-rar` | bool | MAY | Enable RFC 9396 rich authorization requests |
| `--enable-dpop` | bool | SHOULD | Enable RFC 9449 DPoP |
| `--enable-mtls` | bool | SHOULD | Enable RFC 8705 mutual-TLS client auth / sender constraints |
| `--enable-oidc` | bool | MUST | Enable OpenID Connect identity layer |
| `--enable-userinfo` | bool | SHOULD | Enable OIDC UserInfo endpoint |
| `--enable-session-management` | bool | SHOULD | Enable OIDC session management |
| `--enable-rp-initiated-logout` | bool | SHOULD | Enable RP-initiated logout |
| `--enable-frontchannel-logout` | bool | MAY | Enable front-channel logout |
| `--enable-backchannel-logout` | bool | MAY | Enable back-channel logout |
| `--enable-webauthn` | bool | MAY | Enable WebAuthn / passkeys integration |
| `--enable-openapi` | bool | SHOULD | Publish OpenAPI contract endpoints |
| `--enable-openrpc` | bool | SHOULD | Publish OpenRPC / RPC discoverability |

---

## 9) Protocol hardening / compliance flags

| Flag | Type | Priority | Meaning |
|---|---|---:|---|
| `--require-pkce` | bool | MUST | Require PKCE for public clients |
| `--allow-plain-pkce` | bool | MAY | Allow plain PKCE method; default should be false |
| `--require-par` | bool | MAY | Require PAR for selected clients / profiles |
| `--require-jar` | bool | MAY | Require signed request objects |
| `--require-dpop` | bool | MAY | Require DPoP proof for selected clients / token classes |
| `--require-mtls` | bool | MAY | Require mTLS for selected clients / token classes |
| `--strict-issuer` | bool | SHOULD | Enforce exact issuer matching |
| `--strict-redirect-uri` | bool | MUST | Enforce strict redirect URI matching |
| `--strict-discovery` | bool | SHOULD | Enforce metadata/discovery invariants |
| `--strict-jwks` | bool | SHOULD | Enforce JWKS publication and key-use validation |
| `--same-site` | enum | SHOULD | Cookie SameSite policy |
| `--cookie-secure` | bool | SHOULD | Mark cookies Secure |
| `--cookie-http-only` | bool | SHOULD | Mark cookies HttpOnly |
| `--csrf-enabled` | bool | SHOULD | Enable CSRF protections for browser flows |
| `--nonce-required` | bool | SHOULD | Require nonce where applicable |
| `--refresh-token-rotation` | bool | SHOULD | Enable refresh token rotation |
| `--jwks-rotation-enabled` | bool | SHOULD | Enable JWKS rotation policy |
| `--jwks-active-kid` | string | MAY | Force active signing key ID |
| `--alg-allowlist` | repeatable string | SHOULD | Allowed JOSE algorithms |
| `--clock-skew-seconds` | int | SHOULD | Validation clock skew tolerance |

---

## 10) Discovery / contract publication flags

| Flag | Type | Priority | Meaning |
|---|---|---:|---|
| `--openid-configuration-path` | path | SHOULD | Override OIDC discovery path |
| `--oauth-authorization-server-path` | path | SHOULD | Override OAuth metadata path |
| `--jwks-path` | path | SHOULD | Override JWKS endpoint path |
| `--openapi-path` | path | MAY | Override OpenAPI endpoint path |
| `--openrpc-path` | path | MAY | Override OpenRPC endpoint path |
| `--rpc-discover-enabled` | bool | MAY | Enable `rpc.discover` |
| `--docs-enabled` | bool | MAY | Enable interactive API docs |
| `--docs-path` | path | MAY | Override docs path |

---

## 11) Worker-only serve flags

| Flag | Type | Priority | Meaning |
|---|---|---:|---|
| `--concurrency` | int | SHOULD | Worker concurrency |
| `--poll-interval` | seconds | SHOULD | Queue poll interval |
| `--max-jobs` | int | MAY | Maximum jobs per worker |
| `--job-timeout` | seconds | SHOULD | Job timeout |
| `--retry-limit` | int | MAY | Retry limit |

---

## 12) Recommended usage patterns

### Minimal production public surface

```bash
tba-auth serve public \
  --config ./config/prod.yaml \
  --tenant main \
  --issuer https://auth.example.com \
  --host 0.0.0.0 \
  --port 8443 \
  --database-url postgresql+psycopg://... \
  --public-base-url https://auth.example.com \
  --enable-rest \
  --enable-rpc \
  --enable-oidc \
  --enable-userinfo \
  --require-pkce \
  --strict-redirect-uri \
  --refresh-token-rotation \
  --jwks-rotation-enabled \
  --health-enabled \
  --metrics-enabled \
  --log-level info \
  --optimized
```

### Hardened advanced profile

```bash
tba-auth serve all \
  --config ./config/hardened.yaml \
  --tenant main \
  --issuer https://auth.example.com \
  --database-url postgresql+psycopg://... \
  --cache-url redis://... \
  --queue-url redis://... \
  --public-base-url https://auth.example.com \
  --admin-base-url https://auth-admin.example.com \
  --enable-rest \
  --enable-rpc \
  --enable-oidc \
  --enable-par \
  --enable-jar \
  --enable-dpop \
  --enable-mtls \
  --enable-token-exchange \
  --enable-device-flow \
  --enable-dynamic-client-registration \
  --require-pkce \
  --strict-issuer \
  --strict-redirect-uri \
  --strict-discovery \
  --csrf-enabled \
  --refresh-token-rotation \
  --jwks-rotation-enabled \
  --alg-allowlist ES256 --alg-allowlist RS256 \
  --metrics-enabled \
  --health-enabled \
  --log-format json \
  --optimized
```

---

## Bottom line

For `serve`, the recommended surface is:

- **global config and tenancy flags**,
- **bind/runtime flags**,
- **database and queue flags**,
- **TLS/proxy flags**,
- **observability and logging flags**,
- **feature toggles for OAuth2/OIDC/JWKS/OpenAPI/OpenRPC**, and
- **hardening flags for PKCE, issuer, redirects, cookies, CSRF, DPoP, mTLS, PAR, JAR, and key rotation**.

That is the right shape for a certifiable `tba_auth` runtime command.
