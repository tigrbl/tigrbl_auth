> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# tigrbl_auth — Proposed CLI Flags

## Current package state

From the uploaded package as inspected locally:

- there is **no active CLI implementation** in the current package,
- there is **no live `project.scripts` entry point** in `pyproject.toml`, and
- the only CLI hint is a **commented** script line for a future Typer app.

So, today, the current package effectively exposes **no supported CLI flags**.

This document defines the **authoritative CLI surface that should exist in the new package** based on:

- the revised standards / compliance matrix,
- the required ADR and release-gate model,
- strict Tigrbl framework adherence,
- the need for certifiable RFC/OIDC/OAuth/OpenAPI/OpenRPC evidence.

---

## Root executable

```bash
tigrbl-auth [GLOBAL FLAGS] <COMMAND> [SUBCOMMAND] [FLAGS]
```

## Command groups

- `serve`
- `migrate`
- `spec`
- `verify`
- `gate`
- `evidence`
- `claims`
- `adr`
- `doctor`
- `keys`

---

## Global flags

| Flag | Short | Type | Default | Purpose |
|---|---|---:|---|---|
| `--config` | `-c` | path | none | Load package config file |
| `--env-file` | `-e` | path | none | Load environment overrides |
| `--profile` | `-p` | string | `default` | Named runtime/compliance profile |
| `--workspace-root` |  | path | repo root | Monorepo root override |
| `--tenant` | `-t` | string | none | Tenant context for tenant-scoped operations |
| `--issuer` |  | string | config | Override issuer URL |
| `--strict` / `--no-strict` |  | bool | `--strict` | Fail on warnings or incomplete evidence |
| `--offline` |  | bool | false | Disable network-dependent validations |
| `--format` | `-f` | enum | `table` | Output format: `table`, `json`, `yaml` |
| `--output` | `-o` | path | stdout | Output file path |
| `--verbose` | `-v` | count | 0 | Increase verbosity |
| `--quiet` | `-q` | bool | false | Suppress non-essential output |
| `--trace` |  | bool | false | Emit tracebacks and debugging detail |
| `--color` / `--no-color` |  | bool | `--color` | ANSI color control |
| `--fail-fast` / `--no-fail-fast` |  | bool | `--fail-fast` | Stop on first fatal failure |
| `--experimental` |  | bool | false | Enable experimental command paths |
| `--version` | `-V` | bool | false | Print CLI version |
| `--help` | `-h` | bool | false | Show help |

---

## `serve`

Run the Tigrbl/FastAPI auth service.

```bash
tigrbl-auth serve [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--host` | string | `127.0.0.1` | Bind host |
| `--port` | int | `8000` | Bind port |
| `--workers` | int | `1` | Worker count |
| `--reload` / `--no-reload` | bool | `--no-reload` | Auto-reload for development |
| `--uds` | path | none | UNIX domain socket |
| `--root-path` | string | none | ASGI root path |
| `--mount-prefix` | string | `/` | Mount prefix for Tigrbl surface |
| `--database-url` | string | config | DB override |
| `--public-base-url` | string | config | Public-facing base URL |
| `--issuer` | string | config | Issuer URL override |
| `--enable-rest` / `--disable-rest` | bool | `--enable-rest` | Mount REST routes |
| `--enable-rpc` / `--disable-rpc` | bool | `--enable-rpc` | Mount JSON-RPC routes |
| `--readiness-path` | string | `/health/ready` | Readiness path |
| `--liveness-path` | string | `/health/live` | Liveness path |
| `--metrics-path` | string | `/metrics` | Metrics path |
| `--access-log` / `--no-access-log` | bool | `--access-log` | Uvicorn access log control |
| `--proxy-headers` / `--no-proxy-headers` | bool | `--proxy-headers` | Respect proxy headers |
| `--forwarded-allow-ips` | string | config | Trusted proxy list |
| `--log-level` | enum | `info` | `critical`, `error`, `warning`, `info`, `debug`, `trace` |
| `--auto-migrate` / `--no-auto-migrate` | bool | `--no-auto-migrate` | Apply startup migrations |
| `--dev-seed-keys` / `--no-dev-seed-keys` | bool | `--no-dev-seed-keys` | Seed local dev keys |

---

## `migrate`

Schema migration and migration introspection.

### `migrate plan`

```bash
tigrbl-auth migrate plan [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--database-url` | string | config | DB override |
| `--from-revision` | string | current | Starting revision |
| `--to-revision` | string | `head` | Target revision |
| `--tenant` | string | none | Tenant scope |
| `--sql` | bool | false | Emit SQL only |
| `--tag` | string | none | Migration tag |
| `--format` | enum | `table` | Output format |

### `migrate upgrade`

```bash
tigrbl-auth migrate upgrade [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--revision` | string | `head` | Target revision |
| `--database-url` | string | config | DB override |
| `--tenant` | string | none | Tenant scope |
| `--sql` | bool | false | Dry-run SQL output |
| `--tag` | string | none | Migration tag |
| `--dry-run` | bool | false | Validate without applying |

### `migrate downgrade`

```bash
tigrbl-auth migrate downgrade [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--revision` | string | required | Target lower revision |
| `--database-url` | string | config | DB override |
| `--tenant` | string | none | Tenant scope |
| `--sql` | bool | false | Dry-run SQL output |
| `--tag` | string | none | Migration tag |
| `--dry-run` | bool | false | Validate without applying |

### `migrate revision`

```bash
tigrbl-auth migrate revision [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--message` | string | required | Migration message |
| `--autogenerate` / `--no-autogenerate` | bool | `--autogenerate` | Generate from model diff |
| `--head` | string | `head` | Parent revision |
| `--splice` | bool | false | Create splice revision |
| `--branch-label` | string | none | Branch label |
| `--depends-on` | string | none | Dependency revision |
| `--tenant-aware` / `--no-tenant-aware` | bool | `--tenant-aware` | Mark tenant-aware migration |

### `migrate current`

```bash
tigrbl-auth migrate current [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--database-url` | string | config | DB override |
| `--tenant` | string | none | Tenant scope |
| `--verbose` | count | 0 | Include detailed state |

### `migrate history`

```bash
tigrbl-auth migrate history [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--database-url` | string | config | DB override |
| `--tenant` | string | none | Tenant scope |
| `--from-revision` | string | base | Start revision |
| `--to-revision` | string | head | End revision |
| `--verbose` | count | 0 | Include migration body |

---

## `spec`

Build, validate, diff, and publish OpenAPI/OpenRPC artifacts.

### `spec build`

```bash
tigrbl-auth spec build [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--target` | enum | `all` | `public`, `admin`, `resource-server`, `internal`, `all` |
| `--kind` | enum | `all` | `openapi`, `openrpc`, `all` |
| `--format` | enum | `yaml` | `yaml`, `json` |
| `--out-dir` | path | `specs/` | Output directory |
| `--canonical-server-url` | string | config | Canonical server URL |
| `--include-examples` / `--no-include-examples` | bool | `--include-examples` | Include examples |
| `--include-internal` / `--exclude-internal` | bool | `--exclude-internal` | Include internal-only surfaces |
| `--fail-on-warning` / `--no-fail-on-warning` | bool | `--fail-on-warning` | Treat warnings as failures |
| `--stamp-version` / `--no-stamp-version` | bool | `--stamp-version` | Stamp package version into spec |

### `spec validate`

```bash
tigrbl-auth spec validate [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--input` | path | required | Spec file or directory |
| `--kind` | enum | infer | `openapi`, `openrpc` |
| `--lint-profile` | enum | `strict` | `relaxed`, `strict`, `release` |
| `--schema` | path | built-in | Override validation schema |
| `--fail-on-warning` / `--no-fail-on-warning` | bool | `--fail-on-warning` | Warning policy |
| `--offline` | bool | false | Disable remote reference resolution |

### `spec diff`

```bash
tigrbl-auth spec diff [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--base` | path | required | Baseline spec |
| `--head` | path | required | Proposed spec |
| `--kind` | enum | infer | `openapi`, `openrpc` |
| `--breaking-only` / `--no-breaking-only` | bool | `--no-breaking-only` | Show only breaking changes |
| `--fail-on-breaking` / `--no-fail-on-breaking` | bool | `--fail-on-breaking` | Release-breaking policy |
| `--format` | enum | `table` | Output format |

### `spec publish`

```bash
tigrbl-auth spec publish [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--source` | path | `specs/` | Spec source directory |
| `--target` | enum | `all` | Publish target surface |
| `--registry` | string | required | Destination registry or bucket |
| `--version-tag` | string | required | Version tag |
| `--sign` / `--no-sign` | bool | `--sign` | Sign published artifacts |
| `--attestation` | path | none | Attach release attestation |

---

## `verify`

Verify standards targets, contracts, conformance, interop, and security.

### Common verify flags

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--target` | string | `all` | Standards target selector |
| `--` | enum | all | `foundation-boundary`, `baseline-interoperability`, `production-readiness`, `hardening-interop` |
| `--tier` | enum | all | `0`, `1`, `2`, `3`, `4` |
| `--matrix` | path | `compliance/targets/standards-matrix.yaml` | Standards matrix |
| `--evidence-dir` | path | `compliance/evidence/` | Evidence root |
| `--junit` | path | none | JUnit XML output |
| `--json-report` | path | none | JSON report output |
| `--max-failures` | int | unlimited | Stop after N failures |
| `--marker` | string | none | Test marker selector |
| `--pytest-args` | string | none | Pass-through pytest args |

### `verify targets`

```bash
tigrbl-auth verify targets [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--require-adrs` / `--no-require-adrs` | bool | `--require-adrs` | Target must link ADRs |
| `--require-tests` / `--no-require-tests` | bool | `--require-tests` | Target must link tests |
| `--require-evidence` / `--no-require-evidence` | bool | `--require-evidence` | Target must link evidence |
| `--require-specs` / `--no-require-specs` | bool | `--require-specs` | Target must link contract artifacts |
| `--fail-unmapped` / `--no-fail-unmapped` | bool | `--fail-unmapped` | Reject unmapped targets |

### `verify contracts`

```bash
tigrbl-auth verify contracts [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--openapi` | path | `specs/openapi/` | OpenAPI path |
| `--openrpc` | path | `specs/openrpc/` | OpenRPC path |
| `--fail-on-breaking` / `--no-fail-on-breaking` | bool | `--fail-on-breaking` | Breaking-change policy |
| `--require-generated` / `--no-require-generated` | bool | `--require-generated` | Ensure generated artifacts exist |

### `verify conformance`

```bash
tigrbl-auth verify conformance [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--suite` | string | `all` | Conformance suite selector |
| `--rfc` | string | none | RFC-specific selector |
| `--oidc-profile` | string | none | OIDC profile selector |
| `--record-evidence` / `--no-record-evidence` | bool | `--record-evidence` | Save evidence artifacts |
| `--negative-only` / `--no-negative-only` | bool | `--no-negative-only` | Run only negative tests |

### `verify interop`

```bash
tigrbl-auth verify interop [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--profile` | enum | `all` | `spa`, `confidential`, `native`, `device`, `resource-server`, `gateway`, `all` |
| `--peer` | string | none | Named peer implementation |
| `--peer-config` | path | none | Peer config file |
| `--record-wire` / `--no-record-wire` | bool | `--record-wire` | Save wire captures |
| `--publish-report` / `--no-publish-report` | bool | `--no-publish-report` | Publish interop report |

### `verify security`

```bash
tigrbl-auth verify security [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--profile` | enum | `baseline` | `baseline`, `production`, `hardening` |
| `--check-dpop` / `--no-check-dpop` | bool | `--check-dpop` | Verify DPoP profile |
| `--check-mtls` / `--no-check-mtls` | bool | `--check-mtls` | Verify mTLS profile |
| `--check-par` / `--no-check-par` | bool | `--check-par` | Verify PAR |
| `--check-jar` / `--no-check-jar` | bool | `--check-jar` | Verify JAR |
| `--check-rar` / `--no-check-rar` | bool | `--check-rar` | Verify RAR |
| `--check-rotation` / `--no-check-rotation` | bool | `--check-rotation` | Verify key rotation |
| `--check-replay` / `--no-check-replay` | bool | `--check-replay` | Verify replay defenses |

### `verify all`

```bash
tigrbl-auth verify all [FLAGS]
```

Uses the common verify flags and runs targets, contracts, conformance, interop, and security in the required order.

---

## `gate`

Release-gate evaluation and attestation.

### `gate run`

```bash
tigrbl-auth gate run [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--gate-file` | path | auto | Specific gate manifest |
| `--` | enum | required | `foundation-boundary`, `baseline-interoperability`, `production-readiness`, `hardening-interop` |
| `--tier` | enum | all applicable | `1`, `2`, `3`, `4` |
| `--release` | string | current | Release identifier |
| `--blocking` / `--advisory` | bool | `--blocking` | Gate severity |
| `--waiver-file` | path | none | Approved waiver manifest |
| `--evidence-dir` | path | `compliance/evidence/` | Evidence root |
| `--attest-out` | path | none | Write attestation file |
| `--dry-run` | bool | false | Evaluate without status change |

### `gate explain`

```bash
tigrbl-auth gate explain [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--` | enum | required | `foundation-boundary`, `baseline-interoperability`, `production-readiness`, `hardening-interop` |
| `--tier` | enum | none | Restrict to tier |
| `--format` | enum | `table` | Output format |

### `gate status`

```bash
tigrbl-auth gate status [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--release` | string | current | Release identifier |
| `--history` / `--no-history` | bool | `--no-history` | Include prior evaluations |
| `--format` | enum | `table` | Output format |

### `gate attest`

```bash
tigrbl-auth gate attest [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--release` | string | required | Release identifier |
| `--bundle` | path | required | Evidence bundle |
| `--sign` / `--no-sign` | bool | `--sign` | Sign attestation |
| `--signing-key` | string | config | Signing key reference |
| `--output` | path | required | Attestation output path |

---

## `evidence`

Evidence collection, packaging, verification, and publication.

### `evidence collect`

```bash
tigrbl-auth evidence collect [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--source` | enum | `all` | `tests`, `interop`, `wire`, `logs`, `jwks`, `contracts`, `all` |
| `--run-id` | string | current run | CI or local run identifier |
| `--out-dir` | path | `compliance/evidence/` | Output directory |
| `--compress` / `--no-compress` | bool | `--compress` | Compress evidence |
| `--redact-secrets` / `--no-redact-secrets` | bool | `--redact-secrets` | Secret redaction |
| `--include-large-artifacts` / `--exclude-large-artifacts` | bool | `--exclude-large-artifacts` | Large-artifact policy |

### `evidence verify`

```bash
tigrbl-auth evidence verify [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--bundle` | path | required | Evidence bundle or directory |
| `--checksums` | path | auto | Checksum file |
| `--manifest` | path | auto | Evidence manifest |
| `--strict` / `--no-strict` | bool | `--strict` | Fail on missing or mismatched artifacts |

### `evidence bundle`

```bash
tigrbl-auth evidence bundle [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--input-dir` | path | `compliance/evidence/` | Evidence root |
| `--output` | path | required | Bundle path |
| `--format` | enum | `tar.gz` | `tar.gz`, `zip`, `dir` |
| `--sign` / `--no-sign` | bool | `--sign` | Sign bundle |
| `--sbom` / `--no-sbom` | bool | `--sbom` | Attach SBOM |
| `--provenance` / `--no-provenance` | bool | `--provenance` | Attach provenance |

### `evidence publish`

```bash
tigrbl-auth evidence publish [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--bundle` | path | required | Bundle to publish |
| `--dest` | string | required | Destination registry/bucket |
| `--index` / `--no-index` | bool | `--index` | Update evidence index |
| `--visibility` | enum | `internal` | `private`, `internal`, `public` |

---

## `claims`

Standards-claim inspection and promotion control.

### `claims list`

```bash
tigrbl-auth claims list [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--tier` | enum | all | Filter by tier |
| `--` | enum | all | Filter by |
| `--status` | enum | all | `planned`, `implemented`, `asserted`, `certified`, `peer-reviewed` |
| `--target` | string | all | Standards target selector |
| `--format` | enum | `table` | Output format |

### `claims show`

```bash
tigrbl-auth claims show [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--claim-id` | string | required | Claim identifier |
| `--evidence` / `--no-evidence` | bool | `--evidence` | Show evidence links |
| `--tests` / `--no-tests` | bool | `--tests` | Show linked tests |
| `--adrs` / `--no-adrs` | bool | `--adrs` | Show linked ADRs |

### `claims check`

```bash
tigrbl-auth claims check [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--claim-id` | string | required | Claim identifier |
| `--require-tier` | enum | none | Minimum tier required |
| `--require-peer` / `--no-require-peer` | bool | `--no-require-peer` | Require tier-4 evidence |
| `--format` | enum | `table` | Output format |

### `claims lock`

```bash
tigrbl-auth claims lock [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--release` | string | required | Release identifier |
| `--output` | path | required | Locked claims manifest |
| `--sign` / `--no-sign` | bool | `--sign` | Sign locked claim manifest |

### `claims promote`

```bash
tigrbl-auth claims promote [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--claim-id` | string | required | Claim identifier |
| `--to-tier` | enum | required | Target tier |
| `--peer-report` | path | none | Required for tier-4 promotion |
| `--waiver-file` | path | none | Waiver or exception manifest |

---

## `adr`

Architecture Decision Record management.

### `adr new`

```bash
tigrbl-auth adr new [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--id` | string | auto | ADR number |
| `--title` | string | required | ADR title |
| `--status` | enum | `proposed` | `proposed`, `accepted`, `superseded`, `deprecated` |
| `--supersedes` | string | none | Prior ADR |
| `--owners` | string | none | Comma-separated owners |
| `--template` | string | `default` | ADR template |
| `--target` | string | none | Linked standards target |
| `--` | enum | none | Linked |
| `--tier` | enum | none | Linked tier |

### `adr list`

```bash
tigrbl-auth adr list [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--status` | enum | all | Status filter |
| `--target` | string | none | Linked target filter |
| `--format` | enum | `table` | Output format |

### `adr show`

```bash
tigrbl-auth adr show [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--id` | string | required | ADR number |
| `--render` | enum | `markdown` | `markdown`, `json` |

### `adr check`

```bash
tigrbl-auth adr check [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--required` / `--no-required` | bool | `--required` | Treat missing ADRs as failure |
| `--changed-path` | path | none | Check ADR requirements for changed paths |
| `--fail-missing` / `--no-fail-missing` | bool | `--fail-missing` | Failure policy |
| `--enforce-target-links` / `--no-enforce-target-links` | bool | `--enforce-target-links` | Require standards links |

### `adr index`

```bash
tigrbl-auth adr index [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--output` | path | `docs/adr/index.md` | Generated index path |
| `--format` | enum | `markdown` | `markdown`, `json` |

---

## `doctor`

Runtime and repository health inspection.

```bash
tigrbl-auth doctor [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--check` | enum | `all` | `config`, `db`, `keys`, `routes`, `specs`, `gates`, `all` |
| `--fix` / `--no-fix` | bool | `--no-fix` | Apply safe local fixes |
| `--database-url` | string | config | DB override |
| `--issuer` | string | config | Issuer override |
| `--format` | enum | `table` | Output format |

---

## `keys`

Signing and JWKS operational controls.

### `keys rotate`

```bash
tigrbl-auth keys rotate [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--provider` | string | config | Key provider name |
| `--kid` | string | auto | Key identifier |
| `--alg` | string | config | Signing/encryption algorithm |
| `--use` | enum | `sig` | `sig`, `enc` |
| `--activation-time` | datetime | now | Activation time |
| `--retire-after` | duration | policy | Retirement interval |
| `--publish-jwks` / `--no-publish-jwks` | bool | `--publish-jwks` | Publish new JWKS |
| `--dry-run` | bool | false | Preview rotation only |

### `keys jwks`

```bash
tigrbl-auth keys jwks [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--public-only` / `--no-public-only` | bool | `--public-only` | Emit public JWKS only |
| `--issuer` | string | config | Issuer for metadata links |
| `--output` | path | stdout | JWKS output path |
| `--format` | enum | `json` | `json`, `yaml` |

### `keys verify`

```bash
tigrbl-auth keys verify [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--token` | string | required | JWT or detached proof |
| `--jwks-uri` | string | config | JWKS endpoint or file |
| `--alg-allow` | string | policy | Allowed algorithms |
| `--aud` | string | none | Audience override |
| `--iss` | string | none | Issuer override |
| `--now` | datetime | system time | Validation time override |

---

## Entry-point recommendation

The current package should promote this CLI via a real script entry in `pyproject.toml`:

```toml
[project.scripts]
tigrbl-auth = "tigrbl_auth.cli:app"
```

The implementation should use a single command app with subcommand modules:

- `tigrbl_auth/cli/__init__.py`
- `tigrbl_auth/cli/serve.py`
- `tigrbl_auth/cli/migrate.py`
- `tigrbl_auth/cli/spec.py`
- `tigrbl_auth/cli/verify.py`
- `tigrbl_auth/cli/gate.py`
- `tigrbl_auth/cli/evidence.py`
- `tigrbl_auth/cli/claims.py`
- `tigrbl_auth/cli/adr.py`
- `tigrbl_auth/cli/doctor.py`
- `tigrbl_auth/cli/keys.py`

---

## Bottom line

- **Current package**: no supported CLI flags yet.
- **Required new package CLI**: one root `tigrbl-auth` command with governance, conformance, evidence, ADR, spec, migration, and runtime command groups.
- **Most important commands for certification**: `verify`, `gate`, `evidence`, `claims`, and `adr`.
