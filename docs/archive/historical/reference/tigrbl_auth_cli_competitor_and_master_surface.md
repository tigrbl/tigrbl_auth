> [!WARNING]
> Archived historical reference. This document is retained for audit history only and is **not** an authoritative current-state artifact.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` for the current source of truth.

# tigrbl_auth — Competitive Landscape, Master Command Groups, and Unified Flag Surface

## Scope

This document normalizes a proposed CLI and operational surface for `tigrbl_auth` using three inputs:

1. the current `tigrbl_auth` package state,
2. the standards/compliance matrices already defined for the package, and
3. comparable or adjacent identity/authn/authz platforms that operate within the same protocol boundary.

The goal is not to copy any one product. The goal is to produce a **certifiable, Tigrbl-native command surface** that is broad enough for OAuth 2.0 / OIDC / JOSE / operational lifecycle work, while also supporting ADRs, release gates, evidence collection, and independent peer-claim workflows.

---

## 1. Competitive / adjacent software within our boundary

## 1.1 Summary comparison matrix

| Product | Boundary overlap with `tigrbl_auth` | Notable supported features | How configuration / flags are expressed | What to borrow | What not to copy blindly |
|---|---|---|---|---|---|
| **Keycloak** | Full OAuth2/OIDC AS and IdP, admin/runtime ops | Device Flow, DPoP, PAR, token exchange, passkeys/WebAuthn, CIBA, admin bootstrap, realm import/export, OpenAPI endpoint toggles, health/metrics/proxy/TLS controls | Rich runtime flags and feature toggles | Feature toggles, start vs start-dev, bootstrap-admin, import/export, operational flags | Realm-centric semantics and Java/Quarkus-specific runtime model |
| **ORY Hydra** | Strong OAuth2/OIDC AS boundary | Client CRUD, JWK/JWKS CRUD, introspection, revocation, device code, token exchange, migration commands, separate public/admin/all serving | Deep resource-oriented CLI with per-command flags | Resource-centric commands (`client`, `jwk`, `serve`, `migrate`, `perform`) and precise protocol flags | Hydra does not cover the full self-service identity surface alone |
| **ORY Kratos** | Identity lifecycle adjacent to AS boundary | Registration, login, recovery, verification, MFA, WebAuthn/passkeys, identity schema, self-service flows | Serve/config/migrate plus identity-oriented APIs | Identity and session/credential command shape | Kratos is not a replacement for the AS boundary by itself |
| **ZITADEL** | Full CIAM / workforce / machine auth platform | Bootstrap lifecycle, multi-tenancy, OIDC/OAuth2/SAML, machine users, config layering, masterkey controls, TLS mode, init/setup/start sequencing | Lifecycle-oriented server command model + strong config/env options | `init/setup/start` thinking, masterkey/config/steps flags, operational modeling | Product-specific deployment sequencing and internal service topology |
| **Dex** | Federated OIDC provider / broker | Upstream OIDC/SAML/LDAP/OAuth2 connectors, scopes/claims modeling, local password DB option | Mostly config-driven, very small CLI | Connector-oriented configuration and issuer/discovery fidelity | Too little CLI surface for a certifiable auth platform |
| **authentik** | Broad identity and federation platform | OIDC/SAML logout, health/ready endpoints, admin recovery commands, provider/session behavior, extensibility/outposts | Mixture of config, UI, and small admin CLI | Health/doctor commands, recovery/admin actions, session/logout emphasis | Heavier UI-first posture than we want for certification workflows |

---

## 1.2 Product notes and borrowed feature classes

### Keycloak — strongest feature-flag inspiration

Borrow these patterns:
- **runtime feature toggles** for protocol capabilities,
- **bootstrap-admin** command family,
- explicit **start** vs **start-dev** modes,
- realm-like import/export idea translated into **tenant/client/identity** import/export,
- operational flags for **health**, **metrics**, **proxy**, **TLS**, **logging**, and **OpenAPI**.

Suggested borrowed feature flags:
- `--features`, `--features-disabled`
- `--enable-device-flow`
- `--enable-dpop`
- `--enable-par`
- `--enable-token-exchange`
- `--enable-passkeys`
- `--enable-webauthn`
- `--metrics-enabled`
- `--health-enabled`
- `--proxy-headers`
- `--trusted-proxy`
- `--openapi-enabled`
- `--openapi-ui-enabled`

### ORY Hydra — strongest protocol CLI inspiration

Borrow these patterns:
- protocol resource command groups:
  - `client`
  - `key` / `jwks`
  - `token`
  - `perform`
  - `serve`
  - `migrate`
- precise per-client flags for grant types, logout callbacks, request objects, request URIs, token endpoint auth methods, redirect URIs, scopes, audience.

Suggested borrowed feature flags:
- `--grant-type`
- `--response-type`
- `--scope`
- `--audience`
- `--redirect-uri`
- `--post-logout-callback`
- `--frontchannel-logout-callback`
- `--backchannel-logout-callback`
- `--request-object-signing-alg`
- `--request-uri`
- `--token-endpoint-auth-method`
- `--jwks-uri`
- `--sector-identifier-uri`
- `--subject-type`
- `--skip-consent`
- `--endpoint`
- `--http-header`
- `--skip-tls-verify`

### ORY Kratos — strongest identity-flow inspiration

Borrow these patterns:
- self-service flow language for:
  - `login`
  - `register`
  - `verify`
  - `recover`
  - `settings`
  - `session`
- identity schema and trait handling,
- credential-type selection,
- WebAuthn / MFA / recovery control flags.

Suggested borrowed feature flags:
- `--schema`
- `--schema-id`
- `--traits-file`
- `--credential-type`
- `--password`
- `--passkey`
- `--totp`
- `--recovery-code`
- `--verification-channel`
- `--recovery-channel`
- `--session-id`
- `--identity-id`

### ZITADEL — strongest lifecycle/bootstrap inspiration

Borrow these patterns:
- explicit lifecycle commands:
  - `init`
  - `setup`
  - `start`
- config layering and secret material handling,
- masterkey-driven bootstrap,
- `--steps`-style controlled initialization.

Suggested borrowed feature flags:
- `--config`
- `--steps`
- `--masterkey`
- `--masterkey-from-env`
- `--masterkey-file`
- `--tls-mode`
- `--public-base-url`
- `--admin-base-url`

### Dex — strongest connector/discovery inspiration

Borrow these patterns:
- connector/issuer-centric federation configuration,
- claims/scope visibility,
- upstream discovery and issuer validation,
- mostly declarative rather than imperative connector settings.

Suggested borrowed feature flags:
- `--issuer`
- `--upstream-issuer`
- `--connector`
- `--connector-config`
- `--enable-password-db`
- `--hosted-domain`
- `--groups-claim`
- `--prompt-type`

### authentik — strongest health/recovery/logout inspiration

Borrow these patterns:
- health/ready/live checks,
- recovery/admin emergency commands,
- logout/session operational checks,
- provider logout behavior awareness.

Suggested borrowed feature flags:
- `--liveness-path`
- `--readiness-path`
- `--health-path`
- `--metrics-path`
- `--force-logout`
- `--revoke-sessions`
- `--create-recovery-admin`
- `--reset-admin-password`

---

## 2. Master command group list

The normalized top-level command surface for `tigrbl_auth` should be:

```text
tigrbl-auth
├── serve
├── bootstrap
├── migrate
├── tenant
├── client
├── identity
├── flow
├── session
├── token
├── key
├── discovery
├── perform
├── import
├── export
├── spec
├── verify
├── gate
├── evidence
├── claims
├── adr
└── doctor
```

### Why this grouping works

- **serve / bootstrap / migrate / doctor** cover lifecycle and operations.
- **tenant / client / identity / session / token / key** cover stateful auth resources.
- **flow / perform / discovery** cover protocol interactions.
- **spec / verify / gate / evidence / claims / adr** cover certification and governance.
- **import / export** make reproducibility and migration first-class.

---

## 3. Master command groups, subcommands, and flags

## 3.1 `serve`

### Purpose
Run one or more runtime surfaces of `tigrbl_auth`.

### Subcommands
- `all`
- `public`
- `admin`
- `worker`
- `rpc`
- `rest`

### Flags
- `--host`
- `--port`
- `--workers`
- `--reload`
- `--uds`
- `--root-path`
- `--mount-prefix`
- `--public-base-url`
- `--admin-base-url`
- `--enable-rest`
- `--enable-rpc`
- `--health-enabled`
- `--metrics-enabled`
- `--health-path`
- `--liveness-path`
- `--readiness-path`
- `--metrics-path`
- `--proxy-headers`
- `--trusted-proxy`
- `--forwarded-allow-ips`
- `--tls-mode`
- `--tls-cert-file`
- `--tls-key-file`
- `--tls-ca-file`
- `--access-log`
- `--log-level`
- `--dev`
- `--optimized`
- `--auto-migrate`

---

## 3.2 `bootstrap`

### Purpose
Initialize admin, tenant, secrets, and controlled startup prerequisites.

### Subcommands
- `admin`
- `tenant`
- `dev`
- `keys`

### Flags
- `--bootstrap-admin-username`
- `--bootstrap-admin-password`
- `--bootstrap-admin-client-id`
- `--bootstrap-admin-client-secret`
- `--masterkey`
- `--masterkey-from-env`
- `--masterkey-file`
- `--steps`
- `--no-prompt`
- `--yes`
- `--seed-dev-data`
- `--seed-dev-keys`
- `--tenant`
- `--issuer`

---

## 3.3 `migrate`

### Purpose
Manage schema and data migrations.

### Subcommands
- `plan`
- `status`
- `up`
- `down`
- `current`
- `history`
- `revision`

### Flags
- `--database-url`
- `--revision`
- `--from-revision`
- `--to-revision`
- `--sql`
- `--dry-run`
- `--yes`
- `--tag`
- `--message`
- `--autogenerate`
- `--branch-label`
- `--depends-on`
- `--tenant-aware`

---

## 3.4 `tenant`

### Purpose
Manage Tigrbl auth tenancy / issuer partitions.

### Subcommands
- `create`
- `list`
- `get`
- `update`
- `delete`
- `import`
- `export`

### Flags
- `--tenant`
- `--issuer`
- `--name`
- `--display-name`
- `--domain`
- `--metadata`
- `--enabled`
- `--disabled`
- `--json`
- `--yaml`

---

## 3.5 `client`

### Purpose
Manage OAuth2 / OIDC clients.

### Subcommands
- `create`
- `list`
- `get`
- `update`
- `delete`
- `rotate-secret`
- `import`
- `export`

### Flags
- `--client-id`
- `--client-secret`
- `--name`
- `--owner`
- `--grant-type`
- `--response-type`
- `--scope`
- `--audience`
- `--redirect-uri`
- `--post-logout-callback`
- `--frontchannel-logout-callback`
- `--backchannel-logout-callback`
- `--frontchannel-logout-session-required`
- `--backchannel-logout-session-required`
- `--request-object-signing-alg`
- `--request-uri`
- `--token-endpoint-auth-method`
- `--jwks-uri`
- `--jwk`
- `--sector-identifier-uri`
- `--subject-type`
- `--allowed-cors-origin`
- `--contact`
- `--client-uri`
- `--policy-uri`
- `--tos-uri`
- `--skip-consent`
- `--metadata`

---

## 3.6 `identity`

### Purpose
Manage local identities and credentials inside the auth package boundary.

### Subcommands
- `create`
- `list`
- `get`
- `update`
- `delete`
- `activate`
- `deactivate`
- `credential`

### Flags
- `--identity-id`
- `--user-id`
- `--schema`
- `--schema-id`
- `--traits-file`
- `--credential-type`
- `--password`
- `--passkey`
- `--totp`
- `--recovery-code`
- `--verification-channel`
- `--recovery-channel`
- `--enabled`
- `--disabled`

---

## 3.7 `flow`

### Purpose
Trigger or inspect user-facing authn flows.

### Subcommands
- `login`
- `register`
- `verify`
- `recover`
- `logout`
- `status`
- `settings`

### Flags
- `--identity-id`
- `--session-id`
- `--flow-id`
- `--credential-type`
- `--password`
- `--passkey`
- `--totp`
- `--recovery-code`
- `--verification-channel`
- `--recovery-channel`
- `--redirect-uri`
- `--return-to`
- `--prompt`
- `--max-age`
- `--ui-locale`

---

## 3.8 `session`

### Purpose
Inspect and revoke browser and API sessions.

### Subcommands
- `list`
- `get`
- `revoke`
- `revoke-all`
- `delete`

### Flags
- `--session-id`
- `--identity-id`
- `--client-id`
- `--sid`
- `--issuer`
- `--tenant`
- `--force`
- `--reason`
- `--logout-uri`

---

## 3.9 `token`

### Purpose
Operate on tokens and token-adjacent protocol objects.

### Subcommands
- `mint`
- `introspect`
- `revoke`
- `exchange`
- `userinfo`

### Flags
- `--token`
- `--token-type`
- `--subject-token`
- `--actor-token`
- `--requested-token-type`
- `--scope`
- `--audience`
- `--resource`
- `--client-id`
- `--client-secret`
- `--dpop-proof`
- `--mtls-cert-file`
- `--mtls-key-file`

---

## 3.10 `key`

### Purpose
Manage signing and encryption keys and JWKS publication.

### Subcommands
- `create`
- `list`
- `get`
- `rotate`
- `publish-jwks`
- `import`
- `export`
- `delete`

### Flags
- `--key-set`
- `--kid`
- `--alg`
- `--kty`
- `--use`
- `--curve`
- `--size`
- `--jwk`
- `--jwks-uri`
- `--keystore`
- `--kms-uri`
- `--rotate-after`
- `--signing`
- `--encryption`
- `--publish-jwks`

---

## 3.11 `discovery`

### Purpose
Render or validate metadata and well-known surfaces.

### Subcommands
- `show`
- `jwks`
- `validate`
- `publish`

### Flags
- `--issuer`
- `--canonical-server-url`
- `--out-dir`
- `--format`
- `--strict`
- `--public-base-url`
- `--admin-base-url`

---

## 3.12 `perform`

### Purpose
Run protocol flows from the CLI for smoke, interop, and evidence collection.

### Subcommands
- `authorization-code`
- `client-credentials`
- `device-code`
- `refresh-token`

### Flags
- `--endpoint`
- `--client-id`
- `--client-secret`
- `--redirect-uri`
- `--scope`
- `--audience`
- `--resource`
- `--device-code`
- `--code-verifier`
- `--code-challenge`
- `--state`
- `--nonce`
- `--http-header`
- `--skip-tls-verify`

---

## 3.13 `import`

### Purpose
Import package state and fixtures.

### Subcommands
- `tenant`
- `client`
- `identity`
- `keys`
- `sessions`

### Flags
- `--file`
- `--dir`
- `--format`
- `--merge`
- `--replace`
- `--dry-run`
- `--tenant`

---

## 3.14 `export`

### Purpose
Export package state and fixtures.

### Subcommands
- `tenant`
- `client`
- `identity`
- `keys`
- `sessions`

### Flags
- `--file`
- `--dir`
- `--format`
- `--pretty`
- `--tenant`
- `--issuer`

---

## 3.15 `spec`

### Purpose
Build and validate API contracts.

### Subcommands
- `build`
- `validate`
- `diff`
- `publish`

### Flags
- `--kind`
- `--input`
- `--out-dir`
- `--base`
- `--head`
- `--breaking-only`
- `--fail-on-breaking`
- `--stamp-version`
- `--openapi`
- `--openrpc`

---

## 3.16 `verify`

### Purpose
Run standards, conformance, contract, and interoperability checks.

### Subcommands
- `rfc`
- `oauth2`
- `oidc`
- `openapi`
- `openrpc`
- `interop`
- `all`

### Flags
- `--target`
- `--`
- `--tier`
- `--matrix`
- `--evidence-dir`
- `--rfc`
- `--record-evidence`
- `--strict`
- `--fail-fast`
- `--junit-xml`
- `--json`

---

## 3.17 `gate`

### Purpose
Evaluate release and certification gates.

### Subcommands
- `list`
- `check`
- `explain`
- `attest`

### Flags
- `--`
- `--tier`
- `--gate-file`
- `--waiver-file`
- `--attest-out`
- `--require-peer`
- `--fail-fast`

---

## 3.18 `evidence`

### Purpose
Collect, bundle, verify, and publish certifiable evidence.

### Subcommands
- `collect`
- `bundle`
- `verify`
- `publish`
- `ls`

### Flags
- `--source`
- `--bundle`
- `--manifest`
- `--provenance`
- `--out-dir`
- `--include-logs`
- `--include-wire-captures`
- `--include-fixtures`
- `--sign`

---

## 3.19 `claims`

### Purpose
Manage standards and certification claims.

### Subcommands
- `list`
- `show`
- `promote`
- `demote`
- `waive`
- `attest`

### Flags
- `--claim-id`
- `--require-tier`
- `--require-peer`
- `--to-tier`
- `--reason`
- `--evidence-dir`
- `--waiver-file`

---

## 3.20 `adr`

### Purpose
Create and validate Architecture Decision Records.

### Subcommands
- `new`
- `list`
- `show`
- `status`
- `link`
- `check`

### Flags
- `--id`
- `--title`
- `--status`
- `--target`
- `--`
- `--tier`
- `--link-target`
- `--enforce-target-links`

---

## 3.21 `doctor`

### Purpose
Run operational diagnostics.

### Subcommands
- `env`
- `db`
- `keys`
- `tls`
- `proxy`
- `health`

### Flags
- `--database-url`
- `--issuer`
- `--tenant`
- `--tls-cert-file`
- `--tls-key-file`
- `--tls-ca-file`
- `--proxy-headers`
- `--trusted-proxy`
- `--json`
- `--verbose`

---

## 4. Master unified flag feature list

This section deduplicates all flags into one normalized feature catalog.

## 4.1 Global / UX flags

| Flag | Feature family | Meaning |
|---|---|---|
| `-c`, `--config` | config | Primary config file path |
| `-e`, `--env-file` | config | Optional env-file input |
| `-p`, `--profile` | config | Named configuration profile |
| `--workspace-root` | config | Resolve package-relative assets from a fixed root |
| `-t`, `--tenant` | tenancy | Tenant / issuer partition |
| `--issuer` | tenancy | Canonical issuer identifier |
| `--strict` / `--no-strict` | validation | Enable or disable strict validation |
| `--offline` | runtime | Disable network-dependent checks |
| `-f`, `--format` | output | Output format selector |
| `-o`, `--output` | output | Output destination |
| `-v`, `--verbose` | logging | Increase verbosity |
| `-q`, `--quiet` | logging | Reduce output |
| `--trace` | logging | Enable trace-level diagnostics |
| `--color` / `--no-color` | output | ANSI color control |
| `--fail-fast` / `--no-fail-fast` | execution | Stop after the first failure |
| `--experimental` | feature gating | Enable experimental surface area |
| `-V`, `--version` | ux | Print version |
| `-h`, `--help` | ux | Print help |

## 4.2 Runtime / server flags

| Flag | Feature family | Meaning |
|---|---|---|
| `--host` | serving | Bind host |
| `--port` | serving | Bind port |
| `--workers` | serving | Worker count |
| `--reload` | serving | Live reload for development |
| `--uds` | serving | Unix domain socket path |
| `--root-path` | serving | ASGI root path |
| `--mount-prefix` | serving | URL mount prefix |
| `--public-base-url` | serving | Public endpoint base URL |
| `--admin-base-url` | serving | Admin endpoint base URL |
| `--enable-rest` | transport | Enable REST surface |
| `--enable-rpc` | transport | Enable JSON-RPC surface |
| `--health-enabled` | observability | Enable health endpoints |
| `--metrics-enabled` | observability | Enable metrics endpoints |
| `--health-path` | observability | Combined health path |
| `--liveness-path` | observability | Liveness endpoint path |
| `--readiness-path` | observability | Readiness endpoint path |
| `--metrics-path` | observability | Metrics endpoint path |
| `--proxy-headers` | proxy | Trust proxy headers |
| `--trusted-proxy` | proxy | Trusted proxy list |
| `--forwarded-allow-ips` | proxy | Allowed forwarded IP sources |
| `--tls-mode` | tls | TLS mode selector |
| `--tls-cert-file` | tls | TLS certificate path |
| `--tls-key-file` | tls | TLS key path |
| `--tls-ca-file` | tls | CA certificate path |
| `--access-log` | logging | Enable access logs |
| `--log-level` | logging | Log level selector |
| `--dev` | runtime | Development runtime mode |
| `--optimized` | runtime | Production-optimized mode |
| `--auto-migrate` | lifecycle | Run migrations on startup |

## 4.3 Bootstrap / secret / lifecycle flags

| Flag | Feature family | Meaning |
|---|---|---|
| `--bootstrap-admin-username` | bootstrap | Initial admin username |
| `--bootstrap-admin-password` | bootstrap | Initial admin password |
| `--bootstrap-admin-client-id` | bootstrap | Initial admin client ID |
| `--bootstrap-admin-client-secret` | bootstrap | Initial admin client secret |
| `--masterkey` | secrets | Direct masterkey input |
| `--masterkey-from-env` | secrets | Read masterkey from env |
| `--masterkey-file` | secrets | Read masterkey from file |
| `--steps` | lifecycle | Controlled bootstrap/setup steps |
| `--no-prompt` | ux | Non-interactive execution |
| `--yes` | ux | Automatic confirmation |
| `--seed-dev-data` | lifecycle | Seed development data |
| `--seed-dev-keys` | lifecycle | Seed development keys |

## 4.4 Migration / database flags

| Flag | Feature family | Meaning |
|---|---|---|
| `--database-url` | database | Database DSN |
| `--dsn` | database | Alternate DSN spelling |
| `--revision` | migration | Specific revision target |
| `--from-revision` | migration | Starting revision |
| `--to-revision` | migration | Ending revision |
| `--sql` | migration | Emit SQL instead of applying |
| `--dry-run` | migration | Preview execution |
| `--tag` | migration | Tag migration context |
| `--message` | migration | Revision message |
| `--autogenerate` | migration | Generate migration from diff |
| `--branch-label` | migration | Branch label for migration |
| `--depends-on` | migration | Explicit migration dependency |
| `--tenant-aware` | migration | Apply migration with tenant semantics |

## 4.5 Client / protocol registration flags

| Flag | Feature family | Meaning |
|---|---|---|
| `--endpoint` | protocol | Remote endpoint base URL |
| `--skip-tls-verify` | tls | Disable TLS verification |
| `-H`, `--http-header` | protocol | Custom HTTP header |
| `--client-id` | client | OAuth client identifier |
| `--client-secret` | client | OAuth client secret |
| `--name` | client | Display name |
| `--owner` | client | Owning principal |
| `-g`, `--grant-type` | oauth2 | Allowed grant type |
| `-r`, `--response-type` | oauth2 | Allowed response type |
| `-a`, `--scope` | oauth2 | Scope value |
| `--audience` | oauth2 | Token audience |
| `-c`, `--redirect-uri` | oauth2 | Redirect URI |
| `--post-logout-callback` | oidc logout | Post-logout redirect URI |
| `--frontchannel-logout-callback` | oidc logout | Front-channel logout URI |
| `--backchannel-logout-callback` | oidc logout | Back-channel logout URI |
| `--frontchannel-logout-session-required` | oidc logout | Require session on front-channel logout |
| `--backchannel-logout-session-required` | oidc logout | Require session on back-channel logout |
| `--request-object-signing-alg` | oauth2 jar | Request object signing alg |
| `--request-uri` | oauth2 jar | Request URI value |
| `--token-endpoint-auth-method` | oauth2 client auth | Token endpoint client auth method |
| `--jwks-uri` | jose | JWKS URI |
| `--jwk` | jose | Inline JWK |
| `--sector-identifier-uri` | oidc pairwise | Sector identifier URI |
| `--subject-type` | oidc pairwise | Subject type |
| `--allowed-cors-origin` | browser | Allowed CORS origin |
| `--contact` | metadata | Client contacts |
| `--client-uri` | metadata | Client home URI |
| `--policy-uri` | metadata | Policy URI |
| `--tos-uri` | metadata | Terms of service URI |
| `--skip-consent` | oauth2 ux | Skip consent prompt |
| `--metadata` | metadata | Arbitrary JSON metadata |

## 4.6 Identity / authn flow flags

| Flag | Feature family | Meaning |
|---|---|---|
| `--identity-id` | identity | Identity identifier |
| `--user-id` | identity | User identifier |
| `--schema` | identity | Identity schema reference |
| `--schema-id` | identity | Identity schema identifier |
| `--traits-file` | identity | Identity traits payload |
| `--credential-type` | authn | Credential type selector |
| `--password` | authn | Password input |
| `--passkey` | authn | Passkey / WebAuthn selector |
| `--totp` | authn | TOTP code |
| `--recovery-code` | authn | Recovery code |
| `--verification-channel` | authn | Verification delivery channel |
| `--recovery-channel` | authn | Recovery delivery channel |
| `--session-id` | session | Session identifier |
| `--sid` | session | OIDC session identifier |
| `--logout-uri` | logout | Logout redirect or target URI |
| `--flow-id` | flow | Auth flow identifier |
| `--return-to` | flow | Post-flow return target |
| `--prompt` | oidc | Prompt value |
| `--max-age` | oidc | Max session age |
| `--ui-locale` | ux | UI locale hint |

## 4.7 Key / JOSE / JWKS flags

| Flag | Feature family | Meaning |
|---|---|---|
| `--key-set` | jose | Logical key set name |
| `--kid` | jose | Key ID |
| `--alg` | jose | JOSE algorithm |
| `--kty` | jose | JWK key type |
| `--use` | jose | JWK use |
| `--curve` | jose | Elliptic curve |
| `--size` | jose | Key size |
| `--keystore` | keystore | Local keystore selector |
| `--kms-uri` | keystore | Remote KMS URI |
| `--rotate-after` | key lifecycle | Rotation window |
| `--publish-jwks` | discovery | Publish JWKS after update |
| `--signing` | key lifecycle | Mark signing key |
| `--encryption` | key lifecycle | Mark encryption key |

## 4.8 Advanced protocol / hardening flags

| Flag | Feature family | Meaning |
|---|---|---|
| `--resource` | oauth2 | Resource indicator |
| `--subject-token` | token exchange | Subject token |
| `--actor-token` | token exchange | Actor token |
| `--requested-token-type` | token exchange | Requested output token type |
| `--dpop-proof` | dpop | DPoP proof value |
| `--mtls-cert-file` | mtls | mTLS certificate |
| `--mtls-key-file` | mtls | mTLS key |
| `--device-code` | device flow | Device code |
| `--code-verifier` | pkce | PKCE code verifier |
| `--code-challenge` | pkce | PKCE code challenge |
| `--state` | oauth2 | CSRF state |
| `--nonce` | oidc | Replay-protection nonce |

## 4.9 Discovery / spec / contract flags

| Flag | Feature family | Meaning |
|---|---|---|
| `--target` | compliance | Standards target identifier |
| `--kind` | spec | Spec kind selector |
| `--canonical-server-url` | discovery | Canonical published server URL |
| `--input` | spec | Input spec file |
| `--out-dir` | spec | Output directory |
| `--base` | spec diff | Base revision / file |
| `--head` | spec diff | Head revision / file |
| `--breaking-only` | spec diff | Filter to breaking changes |
| `--fail-on-breaking` | spec diff | Exit non-zero on breaking changes |
| `--stamp-version` | spec | Stamp version metadata |
| `--openapi` | spec | OpenAPI artifact selector |
| `--openrpc` | spec | OpenRPC artifact selector |

## 4.10 Verification / gate / evidence / claim flags

| Flag | Feature family | Meaning |
|---|---|---|
| `--` | certification | Implementation |
| `--tier` | certification | Certification tier |
| `--matrix` | compliance | Target matrix file |
| `--evidence-dir` | evidence | Evidence directory |
| `--rfc` | conformance | RFC selector |
| `--record-evidence` | evidence | Persist evidence during verify |
| `--junit-xml` | reporting | Emit JUnit XML |
| `--json` | reporting | Emit JSON |
| `--gate-file` | gates | Gate manifest |
| `--waiver-file` | gates | Waiver manifest |
| `--attest-out` | attestation | Attestation output path |
| `--require-peer` | certification | Require peer-reviewed evidence |
| `--source` | evidence | Evidence source |
| `--bundle` | evidence | Bundle path |
| `--manifest` | evidence | Manifest path |
| `--provenance` | evidence | Provenance metadata |
| `--include-logs` | evidence | Include logs |
| `--include-wire-captures` | evidence | Include wire captures |
| `--include-fixtures` | evidence | Include fixtures |
| `--sign` | attestation | Sign evidence or attestation |
| `--claim-id` | claims | Claim identifier |
| `--require-tier` | claims | Minimum required tier |
| `--to-tier` | claims | Claim promotion target tier |
| `--reason` | claims | Human reason |

## 4.11 ADR / governance flags

| Flag | Feature family | Meaning |
|---|---|---|
| `--id` | adr | ADR identifier |
| `--title` | adr | ADR title |
| `--status` | adr | ADR status |
| `--link-target` | adr | Target / artifact link |
| `--enforce-target-links` | adr | Require traceability links |

---

## 5. Recommended implementation priorities

## runtime-foundation checkpoint — minimum viable CLI
Implement first:
- `serve`
- `bootstrap`
- `migrate`
- `client`
- `token`
- `key`
- `discovery`
- `spec`
- `verify`
- `gate`

## persistence-domain checkpoint — production CLI
Add:
- `tenant`
- `identity`
- `flow`
- `session`
- `import`
- `export`
- `doctor`

## public-route checkpoint — certification / governance completion
Add:
- `evidence`
- `claims`
- `adr`
- `perform`

---

## 6. Bottom line

The best command surface for `tigrbl_auth` is not a clone of Keycloak, Hydra, Kratos, ZITADEL, Dex, or authentik.

It should be:
- **Keycloak-like** in feature toggles and runtime controls,
- **Hydra-like** in protocol resource management,
- **Kratos-like** in identity-flow operations,
- **ZITADEL-like** in lifecycle/bootstrap discipline,
- **Dex-like** in connector/discovery clarity,
- **authentik-like** in health/recovery/logout diagnostics,
- and uniquely **Tigrbl-native** in ADR, release-gate, evidence, and peer-claim workflows.
