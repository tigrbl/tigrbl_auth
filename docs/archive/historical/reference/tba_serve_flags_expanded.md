> [!WARNING]
> Archived historical reference. This document is retained for audit history only and is **not** an authoritative current-state artifact.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` for the current source of truth.

# tba_auth — Expanded `serve` Flags and Color / Output Contract

## Purpose

This document expands the `serve` command into a development-, operations-, and production-ready CLI surface.

It is intentionally **parser-agnostic**:

- this is a **CLI contract**, not a Typer design,
- no flag here depends on Typer semantics,
- the current commented Typer entry-point hint in `pyproject.toml` should be removed once the new CLI contract is adopted.

## Design goals

1. Make local development fast and explicit.
2. Make operations observable and automatable.
3. Make production startup deterministic and safe.
4. Separate human-facing colorized output from machine-facing structured logs.
5. Keep the surface aligned with Tigrbl runtime composition rather than CLI-framework quirks.

---

## Command shape

```bash
tba-auth serve [FLAGS]
```

## Serve execution model

`serve` should support three operating modes:

- **development** — optimized for local iteration, visibility, reload, seeded local keys, and fast failure.
- **operations** — optimized for staging, diagnosis, support, and controlled observability.
- **production** — optimized for deterministic boot, strict validation, structured logs, hardened exposure, and safe shutdown.

Recommended selector:

```bash
tba-auth serve --environment development|operations|production
```

Rules:

- explicit flags override environment defaults,
- `--environment production` must disable unsafe defaults,
- `--reload`, ephemeral keys, and developer seed paths must be rejected in production.

---

## Revised `serve` flags

### 1. Environment and startup mode

| Flag | Type | Default | Mode | Purpose |
|---|---:|---|---|---|
| `--environment` | enum | `development` | all | `development`, `operations`, `production` |
| `--check` | bool | false | all | Validate config, dependencies, migrations, key material, and exit without serving |
| `--print-effective-config` | bool | false | dev/ops | Print resolved runtime config with secret redaction |
| `--print-routes` | bool | false | dev/ops | Print mounted REST/RPC routes and exit or continue |
| `--print-capabilities` | bool | false | ops | Print enabled standards surfaces, profiles, and claims |
| `--startup-timeout` | duration | `60s` | ops/prod | Max startup budget before hard failure |
| `--shutdown-timeout` | duration | `30s` | ops/prod | Max graceful shutdown budget |
| `--graceful-drain-timeout` | duration | `15s` | ops/prod | Drain in-flight requests before exit |
| `--exit-after-startup` | bool | false | ops | Start, validate readiness, then exit 0 |
| `--fail-on-config-warning` | bool | false | ops/prod | Promote config warnings to startup failure |

### 2. Bind, routing, and surface exposure

| Flag | Type | Default | Mode | Purpose |
|---|---:|---|---|---|
| `--host` | string | `127.0.0.1` | all | Bind host |
| `--port` | int | `8000` | all | Bind port |
| `--uds` | path | none | ops/prod | UNIX domain socket |
| `--uds-mode` | octal | none | ops/prod | Socket file mode, e.g. `660` |
| `--root-path` | string | none | all | ASGI root path |
| `--mount-prefix` | string | `/` | all | Tigrbl mount prefix |
| `--public-base-url` | string | config | all | External canonical base URL |
| `--issuer` | string | config | all | Issuer URL override |
| `--enable-rest` / `--disable-rest` | bool | `--enable-rest` | all | Control REST surface |
| `--enable-rpc` / `--disable-rpc` | bool | `--enable-rpc` | all | Control JSON-RPC surface |
| `--enable-openapi` / `--disable-openapi` | bool | `--enable-openapi` | dev/ops | Control OpenAPI surface publication |
| `--enable-openrpc` / `--disable-openrpc` | bool | `--enable-openrpc` | dev/ops | Control OpenRPC surface publication |
| `--enable-diagnostics` / `--disable-diagnostics` | bool | `--disable-diagnostics` in prod | dev/ops/prod | Control diagnostics routes |
| `--docs-path` | string | `/docs` | dev/ops | Docs UI path |
| `--redoc-path` | string | `/redoc` | dev/ops | ReDoc path |
| `--openapi-path` | string | `/openapi.json` | dev/ops | OpenAPI artifact path |
| `--openrpc-path` | string | `/openrpc.json` | dev/ops | OpenRPC artifact path |
| `--rpc-path` | string | `/rpc` | all | JSON-RPC mount path |
| `--rest-prefix` | string | `/` | all | REST surface prefix |

### 3. Development ergonomics

| Flag | Type | Default | Mode | Purpose |
|---|---:|---|---|---|
| `--reload` / `--no-reload` | bool | `--no-reload` | dev | Auto-reload on source change |
| `--reload-dir` | path[] | package root | dev | Extra watch directories |
| `--reload-include` | glob[] | source defaults | dev | Include patterns for reload |
| `--reload-exclude` | glob[] | cache defaults | dev | Exclude patterns for reload |
| `--dev-seed-keys` / `--no-dev-seed-keys` | bool | `--no-dev-seed-keys` | dev | Create local deterministic dev key material |
| `--seed-demo-data` / `--no-seed-demo-data` | bool | `--no-seed-demo-data` | dev | Seed demo tenants, clients, and principals |
| `--allow-http` / `--require-https` | bool | `--allow-http` in dev | dev/prod | Permit insecure local HTTP only in development |
| `--browser-open` / `--no-browser-open` | bool | `--no-browser-open` | dev | Open docs or landing page after startup |
| `--show-banner` / `--no-banner` | bool | `--show-banner` | dev/ops | Show colorized startup summary |
| `--local-trust-proxy` | bool | false | dev | Trust loopback proxy headers for local reverse proxies |
| `--ephemeral-secrets` | bool | false | dev | Generate ephemeral runtime secrets for local throwaway runs |

### 4. Process, workers, and backpressure

| Flag | Type | Default | Mode | Purpose |
|---|---:|---|---|---|
| `--workers` | int | `1` | all | Worker count |
| `--worker-name` | string | auto | ops/prod | Logical worker/process label |
| `--pid-file` | path | none | ops/prod | Write primary process id |
| `--backlog` | int | `2048` | ops/prod | Listen backlog |
| `--limit-concurrency` | int | none | ops/prod | Hard concurrency cap |
| `--max-requests` | int | none | ops/prod | Restart worker after N requests |
| `--max-requests-jitter` | int | `0` | ops/prod | Randomize request cap restarts |
| `--keep-alive-timeout` | duration | `5s` | ops/prod | HTTP keepalive timeout |
| `--request-timeout` | duration | `60s` | ops/prod | End-to-end request budget |
| `--header-timeout` | duration | `10s` | prod | Header read timeout |
| `--body-timeout` | duration | `60s` | prod | Request body read timeout |
| `--response-timeout` | duration | `60s` | prod | Response write timeout |
| `--shutdown-signal` | enum | platform default | ops/prod | Signal used for controlled stop |

### 5. Proxy, network, and ingress integration

| Flag | Type | Default | Mode | Purpose |
|---|---:|---|---|---|
| `--proxy-headers` / `--no-proxy-headers` | bool | `--proxy-headers` | ops/prod | Respect trusted proxy headers |
| `--forwarded-allow-ips` | string | config | ops/prod | Trusted proxy IP/CIDR list |
| `--forwarded-prefix-header` | string | `X-Forwarded-Prefix` | ops/prod | Prefix header override |
| `--forwarded-proto-header` | string | `X-Forwarded-Proto` | ops/prod | Proto header override |
| `--forwarded-host-header` | string | `X-Forwarded-Host` | ops/prod | Host header override |
| `--trusted-host` | string[] | none | prod | Allowed Host header values |
| `--cors-origin` | string[] | none | dev/ops | Allowed CORS origins |
| `--cors-method` | string[] | safe defaults | dev/ops | Allowed CORS methods |
| `--cors-header` | string[] | safe defaults | dev/ops | Allowed CORS headers |
| `--cors-allow-credentials` | bool | false | dev/ops | Allow credentialed browser CORS |
| `--server-header` / `--no-server-header` | bool | `--no-server-header` in prod | dev/prod | Emit or suppress server banner header |

### 6. TLS and transport hardening

| Flag | Type | Default | Mode | Purpose |
|---|---:|---|---|---|
| `--tls-cert-file` | path | none | prod | TLS certificate path |
| `--tls-key-file` | path | none | prod | TLS private key path |
| `--tls-key-password-file` | path | none | prod | Password file for encrypted private key |
| `--tls-ca-file` | path | none | prod | Trusted CA bundle |
| `--tls-client-auth` | enum | `none` | prod | `none`, `optional`, `required` |
| `--tls-min-version` | enum | `1.2` | prod | Min TLS version |
| `--tls-cipher-profile` | enum | `modern` | prod | Cipher suite profile |
| `--hsts` / `--no-hsts` | bool | `--hsts` in prod | prod | Emit HSTS header |
| `--hsts-max-age` | duration | `31536000s` | prod | HSTS max-age |
| `--hsts-include-subdomains` | bool | true | prod | Include subdomains in HSTS |
| `--hsts-preload` | bool | false | prod | Advertise preload intent |

### 7. Database and migration safety

| Flag | Type | Default | Mode | Purpose |
|---|---:|---|---|---|
| `--database-url` | string | config | all | Database DSN override |
| `--db-pool-size` | int | config | ops/prod | Base pool size |
| `--db-max-overflow` | int | config | ops/prod | Overflow connections |
| `--db-pool-timeout` | duration | `30s` | ops/prod | Pool acquisition timeout |
| `--db-pool-recycle` | duration | config | ops/prod | Recycle idle DB connections |
| `--db-connect-timeout` | duration | `10s` | ops/prod | Initial DB connect timeout |
| `--wait-for-db` | bool | true | ops/prod | Retry until DB becomes reachable |
| `--db-max-retries` | int | `30` | ops/prod | Startup DB retry cap |
| `--db-retry-interval` | duration | `2s` | ops/prod | Delay between startup retries |
| `--auto-migrate` / `--no-auto-migrate` | bool | `--no-auto-migrate` | dev/ops | Apply migrations at startup |
| `--require-migrations-at-head` | bool | true in prod | prod | Refuse startup if schema is behind |
| `--migration-lock-timeout` | duration | `60s` | ops/prod | Migration lock wait budget |

### 8. Keys, JWT/JWKS, and crypto readiness

| Flag | Type | Default | Mode | Purpose |
|---|---:|---|---|---|
| `--keyset-dir` | path | config | all | Persistent keyset directory |
| `--active-kid` | string | auto | ops/prod | Force active signing key id |
| `--jwks-cache-ttl` | duration | `300s` | ops/prod | Cache TTL for remote JWKS |
| `--jwks-refresh-interval` | duration | `300s` | ops/prod | Background JWKS refresh interval |
| `--jwks-warmup` | bool | true | ops/prod | Preload JWKS before ready |
| `--require-persistent-keys` | bool | true in prod | prod | Reject startup on ephemeral key mode |
| `--allow-ephemeral-keys` | bool | true in dev | dev | Permit throwaway local key material |
| `--key-rotation-policy` | enum | config | ops/prod | Rotation profile selector |
| `--key-rotation-check` | bool | true | ops/prod | Validate rotation policy at startup |
| `--signing-alg-allowlist` | string[] | config | prod | Allowed JWT signing algorithms |
| `--encryption-alg-allowlist` | string[] | config | prod | Allowed JWE algorithms |
| `--reject-weak-algs` | bool | true | prod | Reject insecure JOSE algorithms |

### 9. Session and cookie behavior

| Flag | Type | Default | Mode | Purpose |
|---|---:|---|---|---|
| `--cookie-domain` | string | config | ops/prod | Session cookie domain |
| `--cookie-path` | string | `/` | all | Session cookie path |
| `--cookie-secure` / `--no-cookie-secure` | bool | `--cookie-secure` in prod | dev/prod | Secure cookie flag |
| `--cookie-http-only` / `--no-cookie-http-only` | bool | `--cookie-http-only` | all | HttpOnly cookie flag |
| `--cookie-samesite` | enum | `lax` | all | `strict`, `lax`, `none` |
| `--session-max-age` | duration | config | ops/prod | Browser/session lifetime |
| `--session-idle-timeout` | duration | config | ops/prod | Idle timeout |
| `--disable-browser-sessions` | bool | false | prod | Disable cookie/browser session mode |
| `--logout-propagation-mode` | enum | config | ops/prod | `local`, `front-channel`, `back-channel`, `hybrid` |

### 10. Health, metrics, tracing, and diagnostics

| Flag | Type | Default | Mode | Purpose |
|---|---:|---|---|---|
| `--readiness-path` | string | `/health/ready` | all | Readiness path |
| `--liveness-path` | string | `/health/live` | all | Liveness path |
| `--startup-path` | string | `/health/startup` | ops/prod | Startup probe path |
| `--metrics-path` | string | `/metrics` | all | Metrics path |
| `--enable-metrics` / `--disable-metrics` | bool | `--enable-metrics` | all | Enable metrics exposition |
| `--enable-tracing` / `--disable-tracing` | bool | `--disable-tracing` | ops/prod | Enable trace emission |
| `--trace-exporter` | enum | `otlp` | ops/prod | Trace exporter type |
| `--trace-endpoint` | string | none | ops/prod | Trace exporter endpoint |
| `--trace-sample-rate` | float | config | ops/prod | Sampling ratio |
| `--request-id-header` | string | `X-Request-ID` | ops/prod | Request correlation header |
| `--correlation-id-header` | string | `X-Correlation-ID` | ops/prod | Cross-service correlation header |
| `--diagnostics-path` | string | `/system` | dev/ops | Diagnostics base path |
| `--status-interval` | duration | none | ops | Periodic service status log interval |

### 11. Logging, color, and operator-facing output

| Flag | Type | Default | Mode | Purpose |
|---|---:|---|---|---|
| `--log-level` | enum | `info` | all | `critical`, `error`, `warning`, `info`, `debug`, `trace` |
| `--access-log` / `--no-access-log` | bool | `--access-log` | all | HTTP access log control |
| `--log-format` | enum | `pretty` in dev, `json` in prod | all | `pretty`, `plain`, `json`, `systemd` |
| `--log-destination` | enum | `stderr` | ops/prod | `stderr`, `stdout`, `file`, `journald` |
| `--log-file` | path | none | ops/prod | File sink when destination is `file` |
| `--log-config` | path | none | ops/prod | External logging config override |
| `--log-request-bodies` | bool | false | dev only | Diagnostic request body logging |
| `--log-response-bodies` | bool | false | dev only | Diagnostic response body logging |
| `--redact-secrets` / `--no-redact-secrets` | bool | `--redact-secrets` | all | Redact secrets in logs and config dumps |
| `--banner-style` | enum | `summary` | dev/ops | `summary`, `compact`, `none` |
| `--color` | enum | `auto` | all | `auto`, `always`, `never` |
| `--color-scope` | enum | `ui` | all | `ui`, `logs`, `all`, `none` |
| `--theme` | enum | `default` | all | `default`, `dark`, `light`, `mono`, `high-contrast` |
| `--glyphs` | enum | `unicode` | all | `unicode`, `ascii`, `none` |
| `--timestamps` / `--no-timestamps` | bool | `--timestamps` | all | Timestamp display in human logs |
| `--show-palette-preview` | bool | false | dev/ops | Preview output theme and exit |

### 12. Production hardening and exposure control

| Flag | Type | Default | Mode | Purpose |
|---|---:|---|---|---|
| `--disable-dev-endpoints` | bool | true in prod | prod | Remove development-only endpoints |
| `--disable-docs-ui` | bool | true in prod | prod | Disable interactive docs UIs |
| `--disable-sample-clients` | bool | true in prod | prod | Disable demo/sample auth clients |
| `--strict-issuer-match` | bool | true | prod | Reject issuer mismatches and ambiguous host config |
| `--strict-forwarded-host` | bool | true | prod | Reject untrusted forwarded host combinations |
| `--strict-cookies` | bool | true | prod | Enforce secure cookie policy |
| `--strict-jwks` | bool | true | prod | Refuse malformed or insecure JWKS state |
| `--strict-startup` | bool | true in prod | prod | Treat readiness preconditions as fatal |
| `--min-password-hash-profile` | enum | config | prod | Required password hashing policy floor |
| `--forbid-localhost-issuer` | bool | true in prod | prod | Reject localhost issuer in production |

---

## Recommended environment defaults

### Development

```text
--environment development
--host 127.0.0.1
--port 8000
--reload
--show-banner
--log-format pretty
--color auto
--theme default
--enable-openapi
--enable-openrpc
--enable-diagnostics
--dev-seed-keys
--allow-http
```

### Operations / staging

```text
--environment operations
--workers 2
--proxy-headers
--enable-metrics
--enable-tracing
--log-format pretty or json
--print-effective-config (optional)
--wait-for-db
--jwks-warmup
--startup-timeout 60s
```

### Production

```text
--environment production
--workers >= 2
--no-reload
--require-https
--proxy-headers
--trusted-host ...
--require-migrations-at-head
--require-persistent-keys
--reject-weak-algs
--strict-startup
--disable-docs-ui
--disable-dev-endpoints
--log-format json
--color never or --color-scope ui
```

---

## Color and output contract

Color should improve operator readability without contaminating machine logs.

### Output classes

| Output class | Default sink | Color default | Intended consumer |
|---|---|---|---|
| startup banner | stderr | on in TTY | human operator |
| serve summary | stderr | on in TTY | human operator |
| pretty logs | stderr | on in TTY | human operator |
| structured logs | stdout/stderr | off | machines / collectors |
| config dumps | stdout | on if TTY and not `json` | human operator |
| health endpoints | HTTP response | none | machines |
| metrics | HTTP response | none | machines |

### Severity palette

| Severity | Suggested style |
|---|---|
| TRACE | dim cyan |
| DEBUG | blue |
| INFO | green |
| WARNING | yellow |
| ERROR | red |
| CRITICAL | bold white on red |

### Service-state palette

| State | Suggested style |
|---|---|
| READY | bold green |
| STARTING | cyan |
| DEGRADED | yellow |
| DRAINING | magenta |
| FAILED | bold red |
| DISABLED | dim |

### Surface palette

| Surface | Suggested style |
|---|---|
| REST | cyan |
| JSON-RPC | magenta |
| OAuth2 | blue |
| OIDC | green |
| JOSE/JWKS | yellow |
| DB | white |
| KEYS | bright yellow |
| GATES / CLAIMS | bright magenta |

### Color behavior rules

1. `--color auto` enables color only when stdout/stderr are terminals.
2. `--color always` forces ANSI color even when piped.
3. `--color never` disables color and glyph styling.
4. `--log-format json` must disable color in emitted log records.
5. `--color-scope ui` colors banners, summaries, and help, but not operational logs.
6. `--color-scope logs` colors pretty logs only.
7. `--color-scope all` colors both UI summaries and pretty logs.
8. `--theme mono` keeps emphasis via bold/dim only.
9. `--glyphs ascii` replaces Unicode checkmarks, arrows, and box-drawing characters.
10. Secret values must never be color-highlighted in a way that prevents redaction.

### Suggested status glyphs

| Meaning | Unicode | ASCII fallback |
|---|---|---|
| success | `✓` | `[OK]` |
| warning | `!` | `[!]` |
| failure | `✗` | `[X]` |
| info | `ℹ` | `[i]` |
| pending | `…` | `[...]` |

---

## Examples

### Development run

```bash
tba-auth serve \
  --environment development \
  --host 127.0.0.1 \
  --port 8000 \
  --reload \
  --dev-seed-keys \
  --seed-demo-data \
  --show-banner \
  --log-format pretty \
  --color always \
  --theme default \
  --glyphs unicode \
  --print-effective-config
```

### Operations / staging run

```bash
tba-auth serve \
  --environment operations \
  --host 0.0.0.0 \
  --port 8080 \
  --workers 2 \
  --proxy-headers \
  --forwarded-allow-ips '10.0.0.0/8,127.0.0.1' \
  --wait-for-db \
  --enable-metrics \
  --enable-tracing \
  --trace-endpoint http://otel-collector:4318 \
  --log-format pretty \
  --color auto \
  --status-interval 30s
```

### Production run

```bash
tba-auth serve \
  --environment production \
  --host 0.0.0.0 \
  --port 8443 \
  --workers 4 \
  --proxy-headers \
  --trusted-host auth.example.com \
  --public-base-url https://auth.example.com \
  --issuer https://auth.example.com \
  --tls-cert-file /run/tls/tls.crt \
  --tls-key-file /run/tls/tls.key \
  --database-url postgresql+psycopg://auth:***@db/tba_auth \
  --require-migrations-at-head \
  --require-persistent-keys \
  --reject-weak-algs \
  --strict-startup \
  --disable-docs-ui \
  --disable-dev-endpoints \
  --log-format json \
  --color never
```

---

## Flags that should be rejected together

| Invalid combination | Reason |
|---|---|
| `--environment production` + `--reload` | unsafe development behavior |
| `--environment production` + `--dev-seed-keys` | non-production key material path |
| `--environment production` + `--allow-http` | insecure transport |
| `--log-format json` + `--color-scope logs` | colorized machine logs are invalid |
| `--disable-rest` + `--disable-rpc` | no service surface remains |
| `--allow-ephemeral-keys` + `--require-persistent-keys` | contradictory key policy |
| `--tls-client-auth required` without CA material | incomplete mTLS config |
| `--disable-openapi` with docs paths still enabled | inconsistent docs contract |

---

## Minimal mandatory additions relative to the current draft

At a minimum, the existing `serve` draft should gain these flags:

- `--environment`
- `--check`
- `--print-effective-config`
- `--startup-timeout`
- `--shutdown-timeout`
- `--trusted-host`
- `--tls-cert-file`
- `--tls-key-file`
- `--db-pool-size`
- `--db-connect-timeout`
- `--wait-for-db`
- `--require-migrations-at-head`
- `--keyset-dir`
- `--require-persistent-keys`
- `--reject-weak-algs`
- `--enable-openapi` / `--disable-openapi`
- `--enable-openrpc` / `--disable-openrpc`
- `--enable-diagnostics` / `--disable-diagnostics`
- `--log-format`
- `--log-destination`
- `--redact-secrets`
- `--color auto|always|never`
- `--color-scope`
- `--theme`
- `--glyphs`
- `--disable-docs-ui`
- `--strict-startup`

These additions turn `serve` from a basic dev launcher into an operable and production-credible service command.
