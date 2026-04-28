> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# tigrbl_auth — CLI Flag Examples

## Scope

The current uploaded package does **not** expose a supported live CLI yet. These examples are for the **proposed** `tigrbl-auth` CLI surface defined in the package planning documents.

Command form:

```bash
tigrbl-auth [GLOBAL FLAGS] <COMMAND> [SUBCOMMAND] [FLAGS]
```

---

## Global flags

| Flag | Example |
|---|---|
| `--config`, `-c` | `tigrbl-auth -c configs/dev.toml doctor` |
| `--env-file`, `-e` | `tigrbl-auth -e .env.local doctor` |
| `--profile`, `-p` | `tigrbl-auth -p production doctor` |
| `--workspace-root` | `tigrbl-auth --workspace-root /workspace/swarmauri verify all` |
| `--tenant`, `-t` | `tigrbl-auth -t acme verify targets` |
| `--issuer` | `tigrbl-auth --issuer https://auth.example.com spec build` |
| `--strict` | `tigrbl-auth --strict verify all` |
| `--no-strict` | `tigrbl-auth --no-strict verify all` |
| `--offline` | `tigrbl-auth --offline spec validate --input specs/openapi/public.openapi.yaml` |
| `--format`, `-f` | `tigrbl-auth -f json claims list` |
| `--output`, `-o` | `tigrbl-auth -o reports/claims.json -f json claims list` |
| `--verbose`, `-v` | `tigrbl-auth -v doctor` |
| `--quiet`, `-q` | `tigrbl-auth -q doctor` |
| `--trace` | `tigrbl-auth --trace verify all` |
| `--color` | `tigrbl-auth --color gate status` |
| `--no-color` | `tigrbl-auth --no-color gate status` |
| `--fail-fast` | `tigrbl-auth --fail-fast verify all` |
| `--no-fail-fast` | `tigrbl-auth --no-fail-fast verify all` |
| `--experimental` | `tigrbl-auth --experimental spec build --include-internal` |
| `--version`, `-V` | `tigrbl-auth -V` |
| `--help`, `-h` | `tigrbl-auth -h` |

---

## `serve`

### Full example

```bash
tigrbl-auth serve \
  --host 0.0.0.0 \
  --port 8443 \
  --workers 4 \
  --reload \
  --root-path /auth \
  --mount-prefix / \
  --database-url postgresql+psycopg://auth:auth@localhost:5432/tigrbl_auth \
  --public-base-url https://auth.example.com \
  --issuer https://auth.example.com \
  --enable-rest \
  --enable-rpc \
  --readiness-path /health/ready \
  --liveness-path /health/live \
  --metrics-path /metrics \
  --access-log \
  --proxy-headers \
  --forwarded-allow-ips 10.0.0.0/8,127.0.0.1 \
  --log-level debug \
  --auto-migrate \
  --dev-seed-keys
```

### Per-flag examples

| Flag | Example |
|---|---|
| `--host` | `tigrbl-auth serve --host 0.0.0.0` |
| `--port` | `tigrbl-auth serve --port 8080` |
| `--workers` | `tigrbl-auth serve --workers 4` |
| `--reload` | `tigrbl-auth serve --reload` |
| `--no-reload` | `tigrbl-auth serve --no-reload` |
| `--uds` | `tigrbl-auth serve --uds /tmp/tigrbl-auth.sock` |
| `--root-path` | `tigrbl-auth serve --root-path /auth` |
| `--mount-prefix` | `tigrbl-auth serve --mount-prefix /` |
| `--database-url` | `tigrbl-auth serve --database-url postgresql://user:pass@db/auth` |
| `--public-base-url` | `tigrbl-auth serve --public-base-url https://auth.example.com` |
| `--issuer` | `tigrbl-auth serve --issuer https://auth.example.com` |
| `--enable-rest` | `tigrbl-auth serve --enable-rest` |
| `--disable-rest` | `tigrbl-auth serve --disable-rest` |
| `--enable-rpc` | `tigrbl-auth serve --enable-rpc` |
| `--disable-rpc` | `tigrbl-auth serve --disable-rpc` |
| `--readiness-path` | `tigrbl-auth serve --readiness-path /readyz` |
| `--liveness-path` | `tigrbl-auth serve --liveness-path /livez` |
| `--metrics-path` | `tigrbl-auth serve --metrics-path /metrics` |
| `--access-log` | `tigrbl-auth serve --access-log` |
| `--no-access-log` | `tigrbl-auth serve --no-access-log` |
| `--proxy-headers` | `tigrbl-auth serve --proxy-headers` |
| `--no-proxy-headers` | `tigrbl-auth serve --no-proxy-headers` |
| `--forwarded-allow-ips` | `tigrbl-auth serve --forwarded-allow-ips '127.0.0.1,10.0.0.0/8'` |
| `--log-level` | `tigrbl-auth serve --log-level info` |
| `--auto-migrate` | `tigrbl-auth serve --auto-migrate` |
| `--no-auto-migrate` | `tigrbl-auth serve --no-auto-migrate` |
| `--dev-seed-keys` | `tigrbl-auth serve --dev-seed-keys` |
| `--no-dev-seed-keys` | `tigrbl-auth serve --no-dev-seed-keys` |

---

## `migrate`

### `migrate plan`

```bash
tigrbl-auth migrate plan \
  --database-url postgresql://user:pass@db/auth \
  --from-revision base \
  --to-revision head \
  --tenant acme \
  --sql \
  --tag bootstrap \
  --format json
```

| Flag | Example |
|---|---|
| `--database-url` | `tigrbl-auth migrate plan --database-url postgresql://user:pass@db/auth` |
| `--from-revision` | `tigrbl-auth migrate plan --from-revision base` |
| `--to-revision` | `tigrbl-auth migrate plan --to-revision head` |
| `--tenant` | `tigrbl-auth migrate plan --tenant acme` |
| `--sql` | `tigrbl-auth migrate plan --sql` |
| `--tag` | `tigrbl-auth migrate plan --tag bootstrap` |
| `--format` | `tigrbl-auth migrate plan --format yaml` |

### `migrate upgrade`

```bash
tigrbl-auth migrate upgrade \
  --revision head \
  --database-url postgresql://user:pass@db/auth \
  --tenant acme \
  --sql \
  --tag release-1 \
  --dry-run
```

| Flag | Example |
|---|---|
| `--revision` | `tigrbl-auth migrate upgrade --revision head` |
| `--database-url` | `tigrbl-auth migrate upgrade --database-url postgresql://user:pass@db/auth` |
| `--tenant` | `tigrbl-auth migrate upgrade --tenant acme` |
| `--sql` | `tigrbl-auth migrate upgrade --sql` |
| `--tag` | `tigrbl-auth migrate upgrade --tag release-1` |
| `--dry-run` | `tigrbl-auth migrate upgrade --dry-run` |

### `migrate downgrade`

```bash
tigrbl-auth migrate downgrade \
  --revision 20260319_01 \
  --database-url postgresql://user:pass@db/auth \
  --tenant acme \
  --sql \
  --tag rollback \
  --dry-run
```

| Flag | Example |
|---|---|
| `--revision` | `tigrbl-auth migrate downgrade --revision 20260319_01` |
| `--database-url` | `tigrbl-auth migrate downgrade --database-url postgresql://user:pass@db/auth` |
| `--tenant` | `tigrbl-auth migrate downgrade --tenant acme` |
| `--sql` | `tigrbl-auth migrate downgrade --sql` |
| `--tag` | `tigrbl-auth migrate downgrade --tag rollback` |
| `--dry-run` | `tigrbl-auth migrate downgrade --dry-run` |

### `migrate revision`

```bash
tigrbl-auth migrate revision \
  --message 'add token exchange tables' \
  --autogenerate \
  --head head \
  --splice \
  --branch-label authz \
  --depends-on 20260318_01 \
  --tenant-aware
```

| Flag | Example |
|---|---|
| `--message` | `tigrbl-auth migrate revision --message 'add oidc session table'` |
| `--autogenerate` | `tigrbl-auth migrate revision --message 'auto diff' --autogenerate` |
| `--no-autogenerate` | `tigrbl-auth migrate revision --message 'manual migration' --no-autogenerate` |
| `--head` | `tigrbl-auth migrate revision --message 'patch' --head head` |
| `--splice` | `tigrbl-auth migrate revision --message 'splice patch' --splice` |
| `--branch-label` | `tigrbl-auth migrate revision --message 'branch' --branch-label authz` |
| `--depends-on` | `tigrbl-auth migrate revision --message 'dependent' --depends-on 20260318_01` |
| `--tenant-aware` | `tigrbl-auth migrate revision --message 'tenant aware' --tenant-aware` |
| `--no-tenant-aware` | `tigrbl-auth migrate revision --message 'global' --no-tenant-aware` |

### `migrate current`

```bash
tigrbl-auth migrate current \
  --database-url postgresql://user:pass@db/auth \
  --tenant acme \
  --verbose
```

| Flag | Example |
|---|---|
| `--database-url` | `tigrbl-auth migrate current --database-url postgresql://user:pass@db/auth` |
| `--tenant` | `tigrbl-auth migrate current --tenant acme` |
| `--verbose` | `tigrbl-auth migrate current --verbose` |

### `migrate history`

```bash
tigrbl-auth migrate history \
  --database-url postgresql://user:pass@db/auth \
  --tenant acme \
  --from-revision base \
  --to-revision head \
  --verbose
```

| Flag | Example |
|---|---|
| `--database-url` | `tigrbl-auth migrate history --database-url postgresql://user:pass@db/auth` |
| `--tenant` | `tigrbl-auth migrate history --tenant acme` |
| `--from-revision` | `tigrbl-auth migrate history --from-revision base` |
| `--to-revision` | `tigrbl-auth migrate history --to-revision head` |
| `--verbose` | `tigrbl-auth migrate history --verbose` |

---

## `spec`

### `spec build`

```bash
tigrbl-auth spec build \
  --target public \
  --kind openapi \
  --format yaml \
  --out-dir specs/ \
  --canonical-server-url https://auth.example.com \
  --include-examples \
  --include-internal \
  --fail-on-warning \
  --stamp-version
```

| Flag | Example |
|---|---|
| `--target` | `tigrbl-auth spec build --target admin` |
| `--kind` | `tigrbl-auth spec build --kind openrpc` |
| `--format` | `tigrbl-auth spec build --format json` |
| `--out-dir` | `tigrbl-auth spec build --out-dir build/specs` |
| `--canonical-server-url` | `tigrbl-auth spec build --canonical-server-url https://auth.example.com` |
| `--include-examples` | `tigrbl-auth spec build --include-examples` |
| `--no-include-examples` | `tigrbl-auth spec build --no-include-examples` |
| `--include-internal` | `tigrbl-auth spec build --include-internal` |
| `--exclude-internal` | `tigrbl-auth spec build --exclude-internal` |
| `--fail-on-warning` | `tigrbl-auth spec build --fail-on-warning` |
| `--no-fail-on-warning` | `tigrbl-auth spec build --no-fail-on-warning` |
| `--stamp-version` | `tigrbl-auth spec build --stamp-version` |
| `--no-stamp-version` | `tigrbl-auth spec build --no-stamp-version` |

### `spec validate`

```bash
tigrbl-auth spec validate \
  --input specs/openapi/public.openapi.yaml \
  --kind openapi \
  --lint-profile release \
  --schema schemas/openapi-3.1.json \
  --fail-on-warning \
  --offline
```

| Flag | Example |
|---|---|
| `--input` | `tigrbl-auth spec validate --input specs/openrpc/admin.openrpc.json` |
| `--kind` | `tigrbl-auth spec validate --input specs/openapi/public.openapi.yaml --kind openapi` |
| `--lint-profile` | `tigrbl-auth spec validate --input specs/openapi/public.openapi.yaml --lint-profile strict` |
| `--schema` | `tigrbl-auth spec validate --input specs/openapi/public.openapi.yaml --schema schemas/openapi-3.1.json` |
| `--fail-on-warning` | `tigrbl-auth spec validate --input specs/openapi/public.openapi.yaml --fail-on-warning` |
| `--no-fail-on-warning` | `tigrbl-auth spec validate --input specs/openapi/public.openapi.yaml --no-fail-on-warning` |
| `--offline` | `tigrbl-auth spec validate --input specs/openapi/public.openapi.yaml --offline` |

### `spec diff`

```bash
tigrbl-auth spec diff \
  --base specs/baseline/public.openapi.yaml \
  --head specs/openapi/public.openapi.yaml \
  --kind openapi \
  --breaking-only \
  --fail-on-breaking \
  --format json
```

| Flag | Example |
|---|---|
| `--base` | `tigrbl-auth spec diff --base specs/old.yaml --head specs/new.yaml` |
| `--head` | `tigrbl-auth spec diff --base specs/old.yaml --head specs/new.yaml` |
| `--kind` | `tigrbl-auth spec diff --base specs/old.json --head specs/new.json --kind openrpc` |
| `--breaking-only` | `tigrbl-auth spec diff --base specs/old.yaml --head specs/new.yaml --breaking-only` |
| `--no-breaking-only` | `tigrbl-auth spec diff --base specs/old.yaml --head specs/new.yaml --no-breaking-only` |
| `--fail-on-breaking` | `tigrbl-auth spec diff --base specs/old.yaml --head specs/new.yaml --fail-on-breaking` |
| `--no-fail-on-breaking` | `tigrbl-auth spec diff --base specs/old.yaml --head specs/new.yaml --no-fail-on-breaking` |
| `--format` | `tigrbl-auth spec diff --base specs/old.yaml --head specs/new.yaml --format table` |

### `spec publish`

```bash
tigrbl-auth spec publish \
  --source specs/ \
  --target all \
  --registry s3://example-spec-registry \
  --version-tag v1.2.3 \
  --sign \
  --attestation compliance/reports/release.attestation.json
```

| Flag | Example |
|---|---|
| `--source` | `tigrbl-auth spec publish --source specs/` |
| `--target` | `tigrbl-auth spec publish --target public --registry s3://specs --version-tag v1.0.0` |
| `--registry` | `tigrbl-auth spec publish --source specs/ --registry s3://specs --version-tag v1.0.0` |
| `--version-tag` | `tigrbl-auth spec publish --source specs/ --registry s3://specs --version-tag v1.0.0` |
| `--sign` | `tigrbl-auth spec publish --source specs/ --registry s3://specs --version-tag v1.0.0 --sign` |
| `--no-sign` | `tigrbl-auth spec publish --source specs/ --registry s3://specs --version-tag v1.0.0 --no-sign` |
| `--attestation` | `tigrbl-auth spec publish --source specs/ --registry s3://specs --version-tag v1.0.0 --attestation compliance/reports/release.attestation.json` |

---

## `verify`

### Common verify flags

| Flag | Example |
|---|---|
| `--target` | `tigrbl-auth verify all --target oauth2` |
| `--` | `tigrbl-auth verify all --production-readiness` |
| `--tier` | `tigrbl-auth verify all --tier 3` |
| `--matrix` | `tigrbl-auth verify all --matrix compliance/targets/standards-matrix.yaml` |
| `--evidence-dir` | `tigrbl-auth verify all --evidence-dir compliance/evidence/` |
| `--junit` | `tigrbl-auth verify all --junit reports/verify.xml` |
| `--json-report` | `tigrbl-auth verify all --json-report reports/verify.json` |
| `--max-failures` | `tigrbl-auth verify all --max-failures 10` |
| `--marker` | `tigrbl-auth verify all --marker conformance` |
| `--pytest-args` | `tigrbl-auth verify all --pytest-args '-k oauth and not slow'` |

### `verify targets`

```bash
tigrbl-auth verify targets \
  --target oauth2 \
  --baseline-interoperability \
  --tier 2 \
  --matrix compliance/targets/standards-matrix.yaml \
  --evidence-dir compliance/evidence/ \
  --require-adrs \
  --require-tests \
  --require-evidence \
  --require-specs \
  --fail-unmapped
```

| Flag | Example |
|---|---|
| `--require-adrs` | `tigrbl-auth verify targets --require-adrs` |
| `--no-require-adrs` | `tigrbl-auth verify targets --no-require-adrs` |
| `--require-tests` | `tigrbl-auth verify targets --require-tests` |
| `--no-require-tests` | `tigrbl-auth verify targets --no-require-tests` |
| `--require-evidence` | `tigrbl-auth verify targets --require-evidence` |
| `--no-require-evidence` | `tigrbl-auth verify targets --no-require-evidence` |
| `--require-specs` | `tigrbl-auth verify targets --require-specs` |
| `--no-require-specs` | `tigrbl-auth verify targets --no-require-specs` |
| `--fail-unmapped` | `tigrbl-auth verify targets --fail-unmapped` |
| `--no-fail-unmapped` | `tigrbl-auth verify targets --no-fail-unmapped` |

### `verify contracts`

```bash
tigrbl-auth verify contracts \
  --openapi specs/openapi/ \
  --openrpc specs/openrpc/ \
  --fail-on-breaking \
  --require-generated
```

| Flag | Example |
|---|---|
| `--openapi` | `tigrbl-auth verify contracts --openapi specs/openapi/` |
| `--openrpc` | `tigrbl-auth verify contracts --openrpc specs/openrpc/` |
| `--fail-on-breaking` | `tigrbl-auth verify contracts --fail-on-breaking` |
| `--no-fail-on-breaking` | `tigrbl-auth verify contracts --no-fail-on-breaking` |
| `--require-generated` | `tigrbl-auth verify contracts --require-generated` |
| `--no-require-generated` | `tigrbl-auth verify contracts --no-require-generated` |

### `verify conformance`

```bash
tigrbl-auth verify conformance \
  --suite oauth2 \
  --rfc 6749 \
  --oidc-profile basic \
  --record-evidence \
  --negative-only
```

| Flag | Example |
|---|---|
| `--suite` | `tigrbl-auth verify conformance --suite oidc` |
| `--rfc` | `tigrbl-auth verify conformance --rfc 7636` |
| `--oidc-profile` | `tigrbl-auth verify conformance --oidc-profile basic` |
| `--record-evidence` | `tigrbl-auth verify conformance --record-evidence` |
| `--no-record-evidence` | `tigrbl-auth verify conformance --no-record-evidence` |
| `--negative-only` | `tigrbl-auth verify conformance --negative-only` |
| `--no-negative-only` | `tigrbl-auth verify conformance --no-negative-only` |

### `verify interop`

```bash
tigrbl-auth verify interop \
  --profile resource-server \
  --peer hydra \
  --peer-config peers/hydra.toml \
  --record-wire \
  --publish-report
```

| Flag | Example |
|---|---|
| `--profile` | `tigrbl-auth verify interop --profile spa` |
| `--peer` | `tigrbl-auth verify interop --peer keycloak` |
| `--peer-config` | `tigrbl-auth verify interop --peer-config peers/keycloak.toml` |
| `--record-wire` | `tigrbl-auth verify interop --record-wire` |
| `--no-record-wire` | `tigrbl-auth verify interop --no-record-wire` |
| `--publish-report` | `tigrbl-auth verify interop --publish-report` |
| `--no-publish-report` | `tigrbl-auth verify interop --no-publish-report` |

### `verify security`

```bash
tigrbl-auth verify security \
  --profile hardening \
  --check-dpop \
  --check-mtls \
  --check-par \
  --check-jar \
  --check-rar \
  --check-rotation \
  --check-replay
```

| Flag | Example |
|---|---|
| `--profile` | `tigrbl-auth verify security --profile production` |
| `--check-dpop` | `tigrbl-auth verify security --check-dpop` |
| `--no-check-dpop` | `tigrbl-auth verify security --no-check-dpop` |
| `--check-mtls` | `tigrbl-auth verify security --check-mtls` |
| `--no-check-mtls` | `tigrbl-auth verify security --no-check-mtls` |
| `--check-par` | `tigrbl-auth verify security --check-par` |
| `--no-check-par` | `tigrbl-auth verify security --no-check-par` |
| `--check-jar` | `tigrbl-auth verify security --check-jar` |
| `--no-check-jar` | `tigrbl-auth verify security --no-check-jar` |
| `--check-rar` | `tigrbl-auth verify security --check-rar` |
| `--no-check-rar` | `tigrbl-auth verify security --no-check-rar` |
| `--check-rotation` | `tigrbl-auth verify security --check-rotation` |
| `--no-check-rotation` | `tigrbl-auth verify security --no-check-rotation` |
| `--check-replay` | `tigrbl-auth verify security --check-replay` |
| `--no-check-replay` | `tigrbl-auth verify security --no-check-replay` |

### `verify all`

```bash
tigrbl-auth verify all \
  --target all \
  --hardening-interop \
  --tier 4 \
  --matrix compliance/targets/standards-matrix.yaml \
  --evidence-dir compliance/evidence/ \
  --junit reports/verify.xml \
  --json-report reports/verify.json \
  --max-failures 5 \
  --marker release \
  --pytest-args '-m release'
```

---

## `gate`

### `gate run`

```bash
tigrbl-auth gate run \
  --gate-file gates/release/production-readiness-production.yaml \
  --production-readiness \
  --tier 3 \
  --release 1.2.3 \
  --blocking \
  --waiver-file compliance/waivers/release-1.2.3.yaml \
  --evidence-dir compliance/evidence/ \
  --attest-out compliance/reports/release-1.2.3.attestation.json \
  --dry-run
```

| Flag | Example |
|---|---|
| `--gate-file` | `tigrbl-auth gate run --gate-file gates/release/baseline-interoperability-interoperable.yaml --baseline-interoperability` |
| `--` | `tigrbl-auth gate run --production-readiness` |
| `--tier` | `tigrbl-auth gate run --production-readiness --tier 3` |
| `--release` | `tigrbl-auth gate run --production-readiness --release 1.2.3` |
| `--blocking` | `tigrbl-auth gate run --production-readiness --blocking` |
| `--advisory` | `tigrbl-auth gate run --production-readiness --advisory` |
| `--waiver-file` | `tigrbl-auth gate run --production-readiness --waiver-file compliance/waivers/release.yaml` |
| `--evidence-dir` | `tigrbl-auth gate run --production-readiness --evidence-dir compliance/evidence/` |
| `--attest-out` | `tigrbl-auth gate run --production-readiness --attest-out reports/release.attestation.json` |
| `--dry-run` | `tigrbl-auth gate run --production-readiness --dry-run` |

### `gate explain`

```bash
tigrbl-auth gate explain --hardening-interop --tier 4 --format yaml
```

| Flag | Example |
|---|---|
| `--` | `tigrbl-auth gate explain --hardening-interop` |
| `--tier` | `tigrbl-auth gate explain --hardening-interop --tier 4` |
| `--format` | `tigrbl-auth gate explain --hardening-interop --format json` |

### `gate status`

```bash
tigrbl-auth gate status --release 1.2.3 --history --format json
```

| Flag | Example |
|---|---|
| `--release` | `tigrbl-auth gate status --release 1.2.3` |
| `--history` | `tigrbl-auth gate status --history` |
| `--no-history` | `tigrbl-auth gate status --no-history` |
| `--format` | `tigrbl-auth gate status --format yaml` |

### `gate attest`

```bash
tigrbl-auth gate attest \
  --release 1.2.3 \
  --bundle dist/evidence-1.2.3.tar.gz \
  --sign \
  --signing-key kms://prod/tigrbl-auth-release \
  --output compliance/reports/release-1.2.3.attestation.json
```

| Flag | Example |
|---|---|
| `--release` | `tigrbl-auth gate attest --release 1.2.3 --bundle dist/evidence.tar.gz --output reports/attestation.json` |
| `--bundle` | `tigrbl-auth gate attest --release 1.2.3 --bundle dist/evidence.tar.gz --output reports/attestation.json` |
| `--sign` | `tigrbl-auth gate attest --release 1.2.3 --bundle dist/evidence.tar.gz --sign --output reports/attestation.json` |
| `--no-sign` | `tigrbl-auth gate attest --release 1.2.3 --bundle dist/evidence.tar.gz --no-sign --output reports/attestation.json` |
| `--signing-key` | `tigrbl-auth gate attest --release 1.2.3 --bundle dist/evidence.tar.gz --signing-key kms://prod/key --output reports/attestation.json` |
| `--output` | `tigrbl-auth gate attest --release 1.2.3 --bundle dist/evidence.tar.gz --output reports/attestation.json` |

---

## `evidence`

### `evidence collect`

```bash
tigrbl-auth evidence collect \
  --source all \
  --run-id gh-123456 \
  --out-dir compliance/evidence/ \
  --compress \
  --redact-secrets \
  --include-large-artifacts
```

| Flag | Example |
|---|---|
| `--source` | `tigrbl-auth evidence collect --source wire` |
| `--run-id` | `tigrbl-auth evidence collect --run-id local-dev-001` |
| `--out-dir` | `tigrbl-auth evidence collect --out-dir compliance/evidence/` |
| `--compress` | `tigrbl-auth evidence collect --compress` |
| `--no-compress` | `tigrbl-auth evidence collect --no-compress` |
| `--redact-secrets` | `tigrbl-auth evidence collect --redact-secrets` |
| `--no-redact-secrets` | `tigrbl-auth evidence collect --no-redact-secrets` |
| `--include-large-artifacts` | `tigrbl-auth evidence collect --include-large-artifacts` |
| `--exclude-large-artifacts` | `tigrbl-auth evidence collect --exclude-large-artifacts` |

### `evidence verify`

```bash
tigrbl-auth evidence verify \
  --bundle dist/evidence-1.2.3.tar.gz \
  --checksums dist/evidence-1.2.3.sha256 \
  --manifest dist/evidence-1.2.3.manifest.json \
  --strict
```

| Flag | Example |
|---|---|
| `--bundle` | `tigrbl-auth evidence verify --bundle dist/evidence.tar.gz` |
| `--checksums` | `tigrbl-auth evidence verify --bundle dist/evidence.tar.gz --checksums dist/evidence.sha256` |
| `--manifest` | `tigrbl-auth evidence verify --bundle dist/evidence.tar.gz --manifest dist/evidence.manifest.json` |
| `--strict` | `tigrbl-auth evidence verify --bundle dist/evidence.tar.gz --strict` |
| `--no-strict` | `tigrbl-auth evidence verify --bundle dist/evidence.tar.gz --no-strict` |

### `evidence bundle`

```bash
tigrbl-auth evidence bundle \
  --input-dir compliance/evidence/ \
  --output dist/evidence-1.2.3.tar.gz \
  --format tar.gz \
  --sign \
  --sbom \
  --provenance
```

| Flag | Example |
|---|---|
| `--input-dir` | `tigrbl-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz` |
| `--output` | `tigrbl-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz` |
| `--format` | `tigrbl-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.zip --format zip` |
| `--sign` | `tigrbl-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz --sign` |
| `--no-sign` | `tigrbl-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz --no-sign` |
| `--sbom` | `tigrbl-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz --sbom` |
| `--no-sbom` | `tigrbl-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz --no-sbom` |
| `--provenance` | `tigrbl-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz --provenance` |
| `--no-provenance` | `tigrbl-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz --no-provenance` |

### `evidence publish`

```bash
tigrbl-auth evidence publish \
  --bundle dist/evidence-1.2.3.tar.gz \
  --dest s3://tigrbl-auth-evidence \
  --index \
  --visibility internal
```

| Flag | Example |
|---|---|
| `--bundle` | `tigrbl-auth evidence publish --bundle dist/evidence.tar.gz --dest s3://evidence` |
| `--dest` | `tigrbl-auth evidence publish --bundle dist/evidence.tar.gz --dest s3://evidence` |
| `--index` | `tigrbl-auth evidence publish --bundle dist/evidence.tar.gz --dest s3://evidence --index` |
| `--no-index` | `tigrbl-auth evidence publish --bundle dist/evidence.tar.gz --dest s3://evidence --no-index` |
| `--visibility` | `tigrbl-auth evidence publish --bundle dist/evidence.tar.gz --dest s3://evidence --visibility public` |

---

## `claims`

### `claims list`

```bash
tigrbl-auth claims list --tier 3 --production-readiness --status certified --target oidc --format json
```

| Flag | Example |
|---|---|
| `--tier` | `tigrbl-auth claims list --tier 4` |
| `--` | `tigrbl-auth claims list --hardening-interop` |
| `--status` | `tigrbl-auth claims list --status peer-reviewed` |
| `--target` | `tigrbl-auth claims list --target oauth2` |
| `--format` | `tigrbl-auth claims list --format yaml` |

### `claims show`

```bash
tigrbl-auth claims show --claim-id oidc.discovery --evidence --tests --adrs
```

| Flag | Example |
|---|---|
| `--claim-id` | `tigrbl-auth claims show --claim-id oauth2.pkce` |
| `--evidence` | `tigrbl-auth claims show --claim-id oauth2.pkce --evidence` |
| `--no-evidence` | `tigrbl-auth claims show --claim-id oauth2.pkce --no-evidence` |
| `--tests` | `tigrbl-auth claims show --claim-id oauth2.pkce --tests` |
| `--no-tests` | `tigrbl-auth claims show --claim-id oauth2.pkce --no-tests` |
| `--adrs` | `tigrbl-auth claims show --claim-id oauth2.pkce --adrs` |
| `--no-adrs` | `tigrbl-auth claims show --claim-id oauth2.pkce --no-adrs` |

### `claims check`

```bash
tigrbl-auth claims check --claim-id oidc.discovery --require-tier 4 --require-peer --format json
```

| Flag | Example |
|---|---|
| `--claim-id` | `tigrbl-auth claims check --claim-id oauth2.pkce` |
| `--require-tier` | `tigrbl-auth claims check --claim-id oauth2.pkce --require-tier 3` |
| `--require-peer` | `tigrbl-auth claims check --claim-id oauth2.pkce --require-peer` |
| `--no-require-peer` | `tigrbl-auth claims check --claim-id oauth2.pkce --no-require-peer` |
| `--format` | `tigrbl-auth claims check --claim-id oauth2.pkce --format yaml` |

### `claims lock`

```bash
tigrbl-auth claims lock --release 1.2.3 --output compliance/claims/locked-1.2.3.yaml --sign
```

| Flag | Example |
|---|---|
| `--release` | `tigrbl-auth claims lock --release 1.2.3 --output compliance/claims/locked-1.2.3.yaml` |
| `--output` | `tigrbl-auth claims lock --release 1.2.3 --output compliance/claims/locked-1.2.3.yaml` |
| `--sign` | `tigrbl-auth claims lock --release 1.2.3 --output compliance/claims/locked-1.2.3.yaml --sign` |
| `--no-sign` | `tigrbl-auth claims lock --release 1.2.3 --output compliance/claims/locked-1.2.3.yaml --no-sign` |

### `claims promote`

```bash
tigrbl-auth claims promote \
  --claim-id oidc.discovery \
  --to-tier 4 \
  --peer-report compliance/reports/peer/oidc.discovery.md \
  --waiver-file compliance/waivers/claims.yaml
```

| Flag | Example |
|---|---|
| `--claim-id` | `tigrbl-auth claims promote --claim-id oauth2.pkce --to-tier 3` |
| `--to-tier` | `tigrbl-auth claims promote --claim-id oauth2.pkce --to-tier 4` |
| `--peer-report` | `tigrbl-auth claims promote --claim-id oauth2.pkce --to-tier 4 --peer-report compliance/reports/peer/oauth2.pkce.md` |
| `--waiver-file` | `tigrbl-auth claims promote --claim-id oauth2.pkce --to-tier 3 --waiver-file compliance/waivers/claims.yaml` |

---

## `adr`

### `adr new`

```bash
tigrbl-auth adr new \
  --id 0011 \
  --title 'Adopt PAR for production profile' \
  --status proposed \
  --supersedes 0009 \
  --owners 'security-team,platform-team' \
  --template default \
  --target oauth2.par \
  --hardening-interop \
  --tier 4
```

| Flag | Example |
|---|---|
| `--id` | `tigrbl-auth adr new --id 0011 --title 'Adopt PAR'` |
| `--title` | `tigrbl-auth adr new --title 'Adopt PAR for production profile'` |
| `--status` | `tigrbl-auth adr new --title 'Adopt PAR' --status accepted` |
| `--supersedes` | `tigrbl-auth adr new --title 'Replace prior key policy' --supersedes 0003` |
| `--owners` | `tigrbl-auth adr new --title 'Adopt PAR' --owners 'security-team,platform-team'` |
| `--template` | `tigrbl-auth adr new --title 'Adopt PAR' --template default` |
| `--target` | `tigrbl-auth adr new --title 'Adopt PAR' --target oauth2.par` |
| `--` | `tigrbl-auth adr new --title 'Adopt PAR' --hardening-interop` |
| `--tier` | `tigrbl-auth adr new --title 'Adopt PAR' --tier 4` |

### `adr list`

```bash
tigrbl-auth adr list --status accepted --target oidc.discovery --format json
```

| Flag | Example |
|---|---|
| `--status` | `tigrbl-auth adr list --status proposed` |
| `--target` | `tigrbl-auth adr list --target oauth2.pkce` |
| `--format` | `tigrbl-auth adr list --format yaml` |

### `adr show`

```bash
tigrbl-auth adr show --id 0006 --render markdown
```

| Flag | Example |
|---|---|
| `--id` | `tigrbl-auth adr show --id 0006` |
| `--render` | `tigrbl-auth adr show --id 0006 --render json` |

### `adr check`

```bash
tigrbl-auth adr check \
  --required \
  --changed-path tigrbl_auth/standards/oauth2/pushed_authorization.py \
  --fail-missing \
  --enforce-target-links
```

| Flag | Example |
|---|---|
| `--required` | `tigrbl-auth adr check --required` |
| `--no-required` | `tigrbl-auth adr check --no-required` |
| `--changed-path` | `tigrbl-auth adr check --changed-path tigrbl_auth/standards/oauth2/token.py` |
| `--fail-missing` | `tigrbl-auth adr check --fail-missing` |
| `--no-fail-missing` | `tigrbl-auth adr check --no-fail-missing` |
| `--enforce-target-links` | `tigrbl-auth adr check --enforce-target-links` |
| `--no-enforce-target-links` | `tigrbl-auth adr check --no-enforce-target-links` |

### `adr index`

```bash
tigrbl-auth adr index --output docs/adr/index.md --format markdown
```

| Flag | Example |
|---|---|
| `--output` | `tigrbl-auth adr index --output docs/adr/index.md` |
| `--format` | `tigrbl-auth adr index --format json` |

---

## `doctor`

```bash
tigrbl-auth doctor --check all --fix --database-url postgresql://user:pass@db/auth --issuer https://auth.example.com --format json
```

| Flag | Example |
|---|---|
| `--check` | `tigrbl-auth doctor --check keys` |
| `--fix` | `tigrbl-auth doctor --check routes --fix` |
| `--no-fix` | `tigrbl-auth doctor --check routes --no-fix` |
| `--database-url` | `tigrbl-auth doctor --database-url postgresql://user:pass@db/auth` |
| `--issuer` | `tigrbl-auth doctor --issuer https://auth.example.com` |
| `--format` | `tigrbl-auth doctor --format yaml` |

---

## `keys`

### `keys rotate`

```bash
tigrbl-auth keys rotate \
  --provider kms \
  --kid 2026-03-prod-01 \
  --alg ES256 \
  --use sig \
  --activation-time 2026-03-19T12:00:00Z \
  --retire-after 90d \
  --publish-jwks \
  --dry-run
```

| Flag | Example |
|---|---|
| `--provider` | `tigrbl-auth keys rotate --provider kms` |
| `--kid` | `tigrbl-auth keys rotate --kid 2026-03-prod-01` |
| `--alg` | `tigrbl-auth keys rotate --alg ES256` |
| `--use` | `tigrbl-auth keys rotate --use sig` |
| `--activation-time` | `tigrbl-auth keys rotate --activation-time 2026-03-19T12:00:00Z` |
| `--retire-after` | `tigrbl-auth keys rotate --retire-after 90d` |
| `--publish-jwks` | `tigrbl-auth keys rotate --publish-jwks` |
| `--no-publish-jwks` | `tigrbl-auth keys rotate --no-publish-jwks` |
| `--dry-run` | `tigrbl-auth keys rotate --dry-run` |

### `keys jwks`

```bash
tigrbl-auth keys jwks --public-only --issuer https://auth.example.com --output build/jwks.json --format json
```

| Flag | Example |
|---|---|
| `--public-only` | `tigrbl-auth keys jwks --public-only` |
| `--no-public-only` | `tigrbl-auth keys jwks --no-public-only` |
| `--issuer` | `tigrbl-auth keys jwks --issuer https://auth.example.com` |
| `--output` | `tigrbl-auth keys jwks --output build/jwks.json` |
| `--format` | `tigrbl-auth keys jwks --format yaml` |

### `keys verify`

```bash
tigrbl-auth keys verify \
  --token eyJ... \
  --jwks-uri https://auth.example.com/.well-known/jwks.json \
  --alg-allow ES256,RS256 \
  --aud api://resource-server \
  --iss https://auth.example.com \
  --now 2026-03-19T12:00:00Z
```

| Flag | Example |
|---|---|
| `--token` | `tigrbl-auth keys verify --token eyJ...` |
| `--jwks-uri` | `tigrbl-auth keys verify --token eyJ... --jwks-uri https://auth.example.com/.well-known/jwks.json` |
| `--alg-allow` | `tigrbl-auth keys verify --token eyJ... --alg-allow ES256,RS256` |
| `--aud` | `tigrbl-auth keys verify --token eyJ... --aud api://resource-server` |
| `--iss` | `tigrbl-auth keys verify --token eyJ... --iss https://auth.example.com` |
| `--now` | `tigrbl-auth keys verify --token eyJ... --now 2026-03-19T12:00:00Z` |

---

## Suggested aliases for daily use

```bash
# local service
tigrbl-auth -c configs/dev.toml serve --reload --dev-seed-keys

# build and validate contracts
tigrbl-auth spec build --target all --kind all && \
tigrbl-auth spec validate --input specs/

# run production gate
tigrbl-auth verify all --production-readiness --tier 3 && \
tigrbl-auth gate run --production-readiness --tier 3 --release 1.2.3

# build peer-claim bundle
tigrbl-auth verify interop --profile all --record-wire --publish-report && \
tigrbl-auth evidence collect --source all && \
tigrbl-auth evidence bundle --output dist/evidence.tar.gz --sign
```
