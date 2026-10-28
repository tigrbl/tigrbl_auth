> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# tba_auth — CLI Flag Examples

## Scope

The current uploaded package does **not** expose a supported live CLI yet. These examples are for the **proposed** `tba-auth` CLI surface defined in the package planning documents.

Command form:

```bash
tba-auth [GLOBAL FLAGS] <COMMAND> [SUBCOMMAND] [FLAGS]
```

---

## Global flags

| Flag | Example |
|---|---|
| `--config`, `-c` | `tba-auth -c configs/dev.toml doctor` |
| `--env-file`, `-e` | `tba-auth -e .env.local doctor` |
| `--profile`, `-p` | `tba-auth -p production doctor` |
| `--workspace-root` | `tba-auth --workspace-root /workspace/swarmauri verify all` |
| `--tenant`, `-t` | `tba-auth -t acme verify targets` |
| `--issuer` | `tba-auth --issuer https://auth.example.com spec build` |
| `--strict` | `tba-auth --strict verify all` |
| `--no-strict` | `tba-auth --no-strict verify all` |
| `--offline` | `tba-auth --offline spec validate --input specs/openapi/public.openapi.yaml` |
| `--format`, `-f` | `tba-auth -f json claims list` |
| `--output`, `-o` | `tba-auth -o reports/claims.json -f json claims list` |
| `--verbose`, `-v` | `tba-auth -v doctor` |
| `--quiet`, `-q` | `tba-auth -q doctor` |
| `--trace` | `tba-auth --trace verify all` |
| `--color` | `tba-auth --color gate status` |
| `--no-color` | `tba-auth --no-color gate status` |
| `--fail-fast` | `tba-auth --fail-fast verify all` |
| `--no-fail-fast` | `tba-auth --no-fail-fast verify all` |
| `--experimental` | `tba-auth --experimental spec build --include-internal` |
| `--version`, `-V` | `tba-auth -V` |
| `--help`, `-h` | `tba-auth -h` |

---

## `serve`

### Full example

```bash
tba-auth serve \
  --host 0.0.0.0 \
  --port 8443 \
  --workers 4 \
  --reload \
  --root-path /auth \
  --mount-prefix / \
  --database-url postgresql+psycopg://auth:auth@localhost:5432/tba_auth \
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
| `--host` | `tba-auth serve --host 0.0.0.0` |
| `--port` | `tba-auth serve --port 8080` |
| `--workers` | `tba-auth serve --workers 4` |
| `--reload` | `tba-auth serve --reload` |
| `--no-reload` | `tba-auth serve --no-reload` |
| `--uds` | `tba-auth serve --uds /tmp/tba-auth.sock` |
| `--root-path` | `tba-auth serve --root-path /auth` |
| `--mount-prefix` | `tba-auth serve --mount-prefix /` |
| `--database-url` | `tba-auth serve --database-url postgresql://user:pass@db/auth` |
| `--public-base-url` | `tba-auth serve --public-base-url https://auth.example.com` |
| `--issuer` | `tba-auth serve --issuer https://auth.example.com` |
| `--enable-rest` | `tba-auth serve --enable-rest` |
| `--disable-rest` | `tba-auth serve --disable-rest` |
| `--enable-rpc` | `tba-auth serve --enable-rpc` |
| `--disable-rpc` | `tba-auth serve --disable-rpc` |
| `--readiness-path` | `tba-auth serve --readiness-path /readyz` |
| `--liveness-path` | `tba-auth serve --liveness-path /livez` |
| `--metrics-path` | `tba-auth serve --metrics-path /metrics` |
| `--access-log` | `tba-auth serve --access-log` |
| `--no-access-log` | `tba-auth serve --no-access-log` |
| `--proxy-headers` | `tba-auth serve --proxy-headers` |
| `--no-proxy-headers` | `tba-auth serve --no-proxy-headers` |
| `--forwarded-allow-ips` | `tba-auth serve --forwarded-allow-ips '127.0.0.1,10.0.0.0/8'` |
| `--log-level` | `tba-auth serve --log-level info` |
| `--auto-migrate` | `tba-auth serve --auto-migrate` |
| `--no-auto-migrate` | `tba-auth serve --no-auto-migrate` |
| `--dev-seed-keys` | `tba-auth serve --dev-seed-keys` |
| `--no-dev-seed-keys` | `tba-auth serve --no-dev-seed-keys` |

---

## `migrate`

### `migrate plan`

```bash
tba-auth migrate plan \
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
| `--database-url` | `tba-auth migrate plan --database-url postgresql://user:pass@db/auth` |
| `--from-revision` | `tba-auth migrate plan --from-revision base` |
| `--to-revision` | `tba-auth migrate plan --to-revision head` |
| `--tenant` | `tba-auth migrate plan --tenant acme` |
| `--sql` | `tba-auth migrate plan --sql` |
| `--tag` | `tba-auth migrate plan --tag bootstrap` |
| `--format` | `tba-auth migrate plan --format yaml` |

### `migrate upgrade`

```bash
tba-auth migrate upgrade \
  --revision head \
  --database-url postgresql://user:pass@db/auth \
  --tenant acme \
  --sql \
  --tag release-1 \
  --dry-run
```

| Flag | Example |
|---|---|
| `--revision` | `tba-auth migrate upgrade --revision head` |
| `--database-url` | `tba-auth migrate upgrade --database-url postgresql://user:pass@db/auth` |
| `--tenant` | `tba-auth migrate upgrade --tenant acme` |
| `--sql` | `tba-auth migrate upgrade --sql` |
| `--tag` | `tba-auth migrate upgrade --tag release-1` |
| `--dry-run` | `tba-auth migrate upgrade --dry-run` |

### `migrate downgrade`

```bash
tba-auth migrate downgrade \
  --revision 20260319_01 \
  --database-url postgresql://user:pass@db/auth \
  --tenant acme \
  --sql \
  --tag rollback \
  --dry-run
```

| Flag | Example |
|---|---|
| `--revision` | `tba-auth migrate downgrade --revision 20260319_01` |
| `--database-url` | `tba-auth migrate downgrade --database-url postgresql://user:pass@db/auth` |
| `--tenant` | `tba-auth migrate downgrade --tenant acme` |
| `--sql` | `tba-auth migrate downgrade --sql` |
| `--tag` | `tba-auth migrate downgrade --tag rollback` |
| `--dry-run` | `tba-auth migrate downgrade --dry-run` |

### `migrate revision`

```bash
tba-auth migrate revision \
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
| `--message` | `tba-auth migrate revision --message 'add oidc session table'` |
| `--autogenerate` | `tba-auth migrate revision --message 'auto diff' --autogenerate` |
| `--no-autogenerate` | `tba-auth migrate revision --message 'manual migration' --no-autogenerate` |
| `--head` | `tba-auth migrate revision --message 'patch' --head head` |
| `--splice` | `tba-auth migrate revision --message 'splice patch' --splice` |
| `--branch-label` | `tba-auth migrate revision --message 'branch' --branch-label authz` |
| `--depends-on` | `tba-auth migrate revision --message 'dependent' --depends-on 20260318_01` |
| `--tenant-aware` | `tba-auth migrate revision --message 'tenant aware' --tenant-aware` |
| `--no-tenant-aware` | `tba-auth migrate revision --message 'global' --no-tenant-aware` |

### `migrate current`

```bash
tba-auth migrate current \
  --database-url postgresql://user:pass@db/auth \
  --tenant acme \
  --verbose
```

| Flag | Example |
|---|---|
| `--database-url` | `tba-auth migrate current --database-url postgresql://user:pass@db/auth` |
| `--tenant` | `tba-auth migrate current --tenant acme` |
| `--verbose` | `tba-auth migrate current --verbose` |

### `migrate history`

```bash
tba-auth migrate history \
  --database-url postgresql://user:pass@db/auth \
  --tenant acme \
  --from-revision base \
  --to-revision head \
  --verbose
```

| Flag | Example |
|---|---|
| `--database-url` | `tba-auth migrate history --database-url postgresql://user:pass@db/auth` |
| `--tenant` | `tba-auth migrate history --tenant acme` |
| `--from-revision` | `tba-auth migrate history --from-revision base` |
| `--to-revision` | `tba-auth migrate history --to-revision head` |
| `--verbose` | `tba-auth migrate history --verbose` |

---

## `spec`

### `spec build`

```bash
tba-auth spec build \
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
| `--target` | `tba-auth spec build --target admin` |
| `--kind` | `tba-auth spec build --kind openrpc` |
| `--format` | `tba-auth spec build --format json` |
| `--out-dir` | `tba-auth spec build --out-dir build/specs` |
| `--canonical-server-url` | `tba-auth spec build --canonical-server-url https://auth.example.com` |
| `--include-examples` | `tba-auth spec build --include-examples` |
| `--no-include-examples` | `tba-auth spec build --no-include-examples` |
| `--include-internal` | `tba-auth spec build --include-internal` |
| `--exclude-internal` | `tba-auth spec build --exclude-internal` |
| `--fail-on-warning` | `tba-auth spec build --fail-on-warning` |
| `--no-fail-on-warning` | `tba-auth spec build --no-fail-on-warning` |
| `--stamp-version` | `tba-auth spec build --stamp-version` |
| `--no-stamp-version` | `tba-auth spec build --no-stamp-version` |

### `spec validate`

```bash
tba-auth spec validate \
  --input specs/openapi/public.openapi.yaml \
  --kind openapi \
  --lint-profile release \
  --schema schemas/openapi-3.1.json \
  --fail-on-warning \
  --offline
```

| Flag | Example |
|---|---|
| `--input` | `tba-auth spec validate --input specs/openrpc/admin.openrpc.json` |
| `--kind` | `tba-auth spec validate --input specs/openapi/public.openapi.yaml --kind openapi` |
| `--lint-profile` | `tba-auth spec validate --input specs/openapi/public.openapi.yaml --lint-profile strict` |
| `--schema` | `tba-auth spec validate --input specs/openapi/public.openapi.yaml --schema schemas/openapi-3.1.json` |
| `--fail-on-warning` | `tba-auth spec validate --input specs/openapi/public.openapi.yaml --fail-on-warning` |
| `--no-fail-on-warning` | `tba-auth spec validate --input specs/openapi/public.openapi.yaml --no-fail-on-warning` |
| `--offline` | `tba-auth spec validate --input specs/openapi/public.openapi.yaml --offline` |

### `spec diff`

```bash
tba-auth spec diff \
  --base specs/baseline/public.openapi.yaml \
  --head specs/openapi/public.openapi.yaml \
  --kind openapi \
  --breaking-only \
  --fail-on-breaking \
  --format json
```

| Flag | Example |
|---|---|
| `--base` | `tba-auth spec diff --base specs/old.yaml --head specs/new.yaml` |
| `--head` | `tba-auth spec diff --base specs/old.yaml --head specs/new.yaml` |
| `--kind` | `tba-auth spec diff --base specs/old.json --head specs/new.json --kind openrpc` |
| `--breaking-only` | `tba-auth spec diff --base specs/old.yaml --head specs/new.yaml --breaking-only` |
| `--no-breaking-only` | `tba-auth spec diff --base specs/old.yaml --head specs/new.yaml --no-breaking-only` |
| `--fail-on-breaking` | `tba-auth spec diff --base specs/old.yaml --head specs/new.yaml --fail-on-breaking` |
| `--no-fail-on-breaking` | `tba-auth spec diff --base specs/old.yaml --head specs/new.yaml --no-fail-on-breaking` |
| `--format` | `tba-auth spec diff --base specs/old.yaml --head specs/new.yaml --format table` |

### `spec publish`

```bash
tba-auth spec publish \
  --source specs/ \
  --target all \
  --registry s3://example-spec-registry \
  --version-tag v1.2.3 \
  --sign \
  --attestation compliance/reports/release.attestation.json
```

| Flag | Example |
|---|---|
| `--source` | `tba-auth spec publish --source specs/` |
| `--target` | `tba-auth spec publish --target public --registry s3://specs --version-tag v1.0.0` |
| `--registry` | `tba-auth spec publish --source specs/ --registry s3://specs --version-tag v1.0.0` |
| `--version-tag` | `tba-auth spec publish --source specs/ --registry s3://specs --version-tag v1.0.0` |
| `--sign` | `tba-auth spec publish --source specs/ --registry s3://specs --version-tag v1.0.0 --sign` |
| `--no-sign` | `tba-auth spec publish --source specs/ --registry s3://specs --version-tag v1.0.0 --no-sign` |
| `--attestation` | `tba-auth spec publish --source specs/ --registry s3://specs --version-tag v1.0.0 --attestation compliance/reports/release.attestation.json` |

---

## `verify`

### Common verify flags

| Flag | Example |
|---|---|
| `--target` | `tba-auth verify all --target oauth2` |
| `--` | `tba-auth verify all --production-readiness` |
| `--tier` | `tba-auth verify all --tier 3` |
| `--matrix` | `tba-auth verify all --matrix compliance/targets/standards-matrix.yaml` |
| `--evidence-dir` | `tba-auth verify all --evidence-dir compliance/evidence/` |
| `--junit` | `tba-auth verify all --junit reports/verify.xml` |
| `--json-report` | `tba-auth verify all --json-report reports/verify.json` |
| `--max-failures` | `tba-auth verify all --max-failures 10` |
| `--marker` | `tba-auth verify all --marker conformance` |
| `--pytest-args` | `tba-auth verify all --pytest-args '-k oauth and not slow'` |

### `verify targets`

```bash
tba-auth verify targets \
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
| `--require-adrs` | `tba-auth verify targets --require-adrs` |
| `--no-require-adrs` | `tba-auth verify targets --no-require-adrs` |
| `--require-tests` | `tba-auth verify targets --require-tests` |
| `--no-require-tests` | `tba-auth verify targets --no-require-tests` |
| `--require-evidence` | `tba-auth verify targets --require-evidence` |
| `--no-require-evidence` | `tba-auth verify targets --no-require-evidence` |
| `--require-specs` | `tba-auth verify targets --require-specs` |
| `--no-require-specs` | `tba-auth verify targets --no-require-specs` |
| `--fail-unmapped` | `tba-auth verify targets --fail-unmapped` |
| `--no-fail-unmapped` | `tba-auth verify targets --no-fail-unmapped` |

### `verify contracts`

```bash
tba-auth verify contracts \
  --openapi specs/openapi/ \
  --openrpc specs/openrpc/ \
  --fail-on-breaking \
  --require-generated
```

| Flag | Example |
|---|---|
| `--openapi` | `tba-auth verify contracts --openapi specs/openapi/` |
| `--openrpc` | `tba-auth verify contracts --openrpc specs/openrpc/` |
| `--fail-on-breaking` | `tba-auth verify contracts --fail-on-breaking` |
| `--no-fail-on-breaking` | `tba-auth verify contracts --no-fail-on-breaking` |
| `--require-generated` | `tba-auth verify contracts --require-generated` |
| `--no-require-generated` | `tba-auth verify contracts --no-require-generated` |

### `verify conformance`

```bash
tba-auth verify conformance \
  --suite oauth2 \
  --rfc 6749 \
  --oidc-profile basic \
  --record-evidence \
  --negative-only
```

| Flag | Example |
|---|---|
| `--suite` | `tba-auth verify conformance --suite oidc` |
| `--rfc` | `tba-auth verify conformance --rfc 7636` |
| `--oidc-profile` | `tba-auth verify conformance --oidc-profile basic` |
| `--record-evidence` | `tba-auth verify conformance --record-evidence` |
| `--no-record-evidence` | `tba-auth verify conformance --no-record-evidence` |
| `--negative-only` | `tba-auth verify conformance --negative-only` |
| `--no-negative-only` | `tba-auth verify conformance --no-negative-only` |

### `verify interop`

```bash
tba-auth verify interop \
  --profile resource-server \
  --peer hydra \
  --peer-config peers/hydra.toml \
  --record-wire \
  --publish-report
```

| Flag | Example |
|---|---|
| `--profile` | `tba-auth verify interop --profile spa` |
| `--peer` | `tba-auth verify interop --peer keycloak` |
| `--peer-config` | `tba-auth verify interop --peer-config peers/keycloak.toml` |
| `--record-wire` | `tba-auth verify interop --record-wire` |
| `--no-record-wire` | `tba-auth verify interop --no-record-wire` |
| `--publish-report` | `tba-auth verify interop --publish-report` |
| `--no-publish-report` | `tba-auth verify interop --no-publish-report` |

### `verify security`

```bash
tba-auth verify security \
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
| `--profile` | `tba-auth verify security --profile production` |
| `--check-dpop` | `tba-auth verify security --check-dpop` |
| `--no-check-dpop` | `tba-auth verify security --no-check-dpop` |
| `--check-mtls` | `tba-auth verify security --check-mtls` |
| `--no-check-mtls` | `tba-auth verify security --no-check-mtls` |
| `--check-par` | `tba-auth verify security --check-par` |
| `--no-check-par` | `tba-auth verify security --no-check-par` |
| `--check-jar` | `tba-auth verify security --check-jar` |
| `--no-check-jar` | `tba-auth verify security --no-check-jar` |
| `--check-rar` | `tba-auth verify security --check-rar` |
| `--no-check-rar` | `tba-auth verify security --no-check-rar` |
| `--check-rotation` | `tba-auth verify security --check-rotation` |
| `--no-check-rotation` | `tba-auth verify security --no-check-rotation` |
| `--check-replay` | `tba-auth verify security --check-replay` |
| `--no-check-replay` | `tba-auth verify security --no-check-replay` |

### `verify all`

```bash
tba-auth verify all \
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
tba-auth gate run \
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
| `--gate-file` | `tba-auth gate run --gate-file gates/release/baseline-interoperability-interoperable.yaml --baseline-interoperability` |
| `--` | `tba-auth gate run --production-readiness` |
| `--tier` | `tba-auth gate run --production-readiness --tier 3` |
| `--release` | `tba-auth gate run --production-readiness --release 1.2.3` |
| `--blocking` | `tba-auth gate run --production-readiness --blocking` |
| `--advisory` | `tba-auth gate run --production-readiness --advisory` |
| `--waiver-file` | `tba-auth gate run --production-readiness --waiver-file compliance/waivers/release.yaml` |
| `--evidence-dir` | `tba-auth gate run --production-readiness --evidence-dir compliance/evidence/` |
| `--attest-out` | `tba-auth gate run --production-readiness --attest-out reports/release.attestation.json` |
| `--dry-run` | `tba-auth gate run --production-readiness --dry-run` |

### `gate explain`

```bash
tba-auth gate explain --hardening-interop --tier 4 --format yaml
```

| Flag | Example |
|---|---|
| `--` | `tba-auth gate explain --hardening-interop` |
| `--tier` | `tba-auth gate explain --hardening-interop --tier 4` |
| `--format` | `tba-auth gate explain --hardening-interop --format json` |

### `gate status`

```bash
tba-auth gate status --release 1.2.3 --history --format json
```

| Flag | Example |
|---|---|
| `--release` | `tba-auth gate status --release 1.2.3` |
| `--history` | `tba-auth gate status --history` |
| `--no-history` | `tba-auth gate status --no-history` |
| `--format` | `tba-auth gate status --format yaml` |

### `gate attest`

```bash
tba-auth gate attest \
  --release 1.2.3 \
  --bundle dist/evidence-1.2.3.tar.gz \
  --sign \
  --signing-key kms://prod/tba-auth-release \
  --output compliance/reports/release-1.2.3.attestation.json
```

| Flag | Example |
|---|---|
| `--release` | `tba-auth gate attest --release 1.2.3 --bundle dist/evidence.tar.gz --output reports/attestation.json` |
| `--bundle` | `tba-auth gate attest --release 1.2.3 --bundle dist/evidence.tar.gz --output reports/attestation.json` |
| `--sign` | `tba-auth gate attest --release 1.2.3 --bundle dist/evidence.tar.gz --sign --output reports/attestation.json` |
| `--no-sign` | `tba-auth gate attest --release 1.2.3 --bundle dist/evidence.tar.gz --no-sign --output reports/attestation.json` |
| `--signing-key` | `tba-auth gate attest --release 1.2.3 --bundle dist/evidence.tar.gz --signing-key kms://prod/key --output reports/attestation.json` |
| `--output` | `tba-auth gate attest --release 1.2.3 --bundle dist/evidence.tar.gz --output reports/attestation.json` |

---

## `evidence`

### `evidence collect`

```bash
tba-auth evidence collect \
  --source all \
  --run-id gh-123456 \
  --out-dir compliance/evidence/ \
  --compress \
  --redact-secrets \
  --include-large-artifacts
```

| Flag | Example |
|---|---|
| `--source` | `tba-auth evidence collect --source wire` |
| `--run-id` | `tba-auth evidence collect --run-id local-dev-001` |
| `--out-dir` | `tba-auth evidence collect --out-dir compliance/evidence/` |
| `--compress` | `tba-auth evidence collect --compress` |
| `--no-compress` | `tba-auth evidence collect --no-compress` |
| `--redact-secrets` | `tba-auth evidence collect --redact-secrets` |
| `--no-redact-secrets` | `tba-auth evidence collect --no-redact-secrets` |
| `--include-large-artifacts` | `tba-auth evidence collect --include-large-artifacts` |
| `--exclude-large-artifacts` | `tba-auth evidence collect --exclude-large-artifacts` |

### `evidence verify`

```bash
tba-auth evidence verify \
  --bundle dist/evidence-1.2.3.tar.gz \
  --checksums dist/evidence-1.2.3.sha256 \
  --manifest dist/evidence-1.2.3.manifest.json \
  --strict
```

| Flag | Example |
|---|---|
| `--bundle` | `tba-auth evidence verify --bundle dist/evidence.tar.gz` |
| `--checksums` | `tba-auth evidence verify --bundle dist/evidence.tar.gz --checksums dist/evidence.sha256` |
| `--manifest` | `tba-auth evidence verify --bundle dist/evidence.tar.gz --manifest dist/evidence.manifest.json` |
| `--strict` | `tba-auth evidence verify --bundle dist/evidence.tar.gz --strict` |
| `--no-strict` | `tba-auth evidence verify --bundle dist/evidence.tar.gz --no-strict` |

### `evidence bundle`

```bash
tba-auth evidence bundle \
  --input-dir compliance/evidence/ \
  --output dist/evidence-1.2.3.tar.gz \
  --format tar.gz \
  --sign \
  --sbom \
  --provenance
```

| Flag | Example |
|---|---|
| `--input-dir` | `tba-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz` |
| `--output` | `tba-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz` |
| `--format` | `tba-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.zip --format zip` |
| `--sign` | `tba-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz --sign` |
| `--no-sign` | `tba-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz --no-sign` |
| `--sbom` | `tba-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz --sbom` |
| `--no-sbom` | `tba-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz --no-sbom` |
| `--provenance` | `tba-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz --provenance` |
| `--no-provenance` | `tba-auth evidence bundle --input-dir compliance/evidence/ --output dist/evidence.tar.gz --no-provenance` |

### `evidence publish`

```bash
tba-auth evidence publish \
  --bundle dist/evidence-1.2.3.tar.gz \
  --dest s3://tba-auth-evidence \
  --index \
  --visibility internal
```

| Flag | Example |
|---|---|
| `--bundle` | `tba-auth evidence publish --bundle dist/evidence.tar.gz --dest s3://evidence` |
| `--dest` | `tba-auth evidence publish --bundle dist/evidence.tar.gz --dest s3://evidence` |
| `--index` | `tba-auth evidence publish --bundle dist/evidence.tar.gz --dest s3://evidence --index` |
| `--no-index` | `tba-auth evidence publish --bundle dist/evidence.tar.gz --dest s3://evidence --no-index` |
| `--visibility` | `tba-auth evidence publish --bundle dist/evidence.tar.gz --dest s3://evidence --visibility public` |

---

## `claims`

### `claims list`

```bash
tba-auth claims list --tier 3 --production-readiness --status certified --target oidc --format json
```

| Flag | Example |
|---|---|
| `--tier` | `tba-auth claims list --tier 4` |
| `--` | `tba-auth claims list --hardening-interop` |
| `--status` | `tba-auth claims list --status peer-reviewed` |
| `--target` | `tba-auth claims list --target oauth2` |
| `--format` | `tba-auth claims list --format yaml` |

### `claims show`

```bash
tba-auth claims show --claim-id oidc.discovery --evidence --tests --adrs
```

| Flag | Example |
|---|---|
| `--claim-id` | `tba-auth claims show --claim-id oauth2.pkce` |
| `--evidence` | `tba-auth claims show --claim-id oauth2.pkce --evidence` |
| `--no-evidence` | `tba-auth claims show --claim-id oauth2.pkce --no-evidence` |
| `--tests` | `tba-auth claims show --claim-id oauth2.pkce --tests` |
| `--no-tests` | `tba-auth claims show --claim-id oauth2.pkce --no-tests` |
| `--adrs` | `tba-auth claims show --claim-id oauth2.pkce --adrs` |
| `--no-adrs` | `tba-auth claims show --claim-id oauth2.pkce --no-adrs` |

### `claims check`

```bash
tba-auth claims check --claim-id oidc.discovery --require-tier 4 --require-peer --format json
```

| Flag | Example |
|---|---|
| `--claim-id` | `tba-auth claims check --claim-id oauth2.pkce` |
| `--require-tier` | `tba-auth claims check --claim-id oauth2.pkce --require-tier 3` |
| `--require-peer` | `tba-auth claims check --claim-id oauth2.pkce --require-peer` |
| `--no-require-peer` | `tba-auth claims check --claim-id oauth2.pkce --no-require-peer` |
| `--format` | `tba-auth claims check --claim-id oauth2.pkce --format yaml` |

### `claims lock`

```bash
tba-auth claims lock --release 1.2.3 --output compliance/claims/locked-1.2.3.yaml --sign
```

| Flag | Example |
|---|---|
| `--release` | `tba-auth claims lock --release 1.2.3 --output compliance/claims/locked-1.2.3.yaml` |
| `--output` | `tba-auth claims lock --release 1.2.3 --output compliance/claims/locked-1.2.3.yaml` |
| `--sign` | `tba-auth claims lock --release 1.2.3 --output compliance/claims/locked-1.2.3.yaml --sign` |
| `--no-sign` | `tba-auth claims lock --release 1.2.3 --output compliance/claims/locked-1.2.3.yaml --no-sign` |

### `claims promote`

```bash
tba-auth claims promote \
  --claim-id oidc.discovery \
  --to-tier 4 \
  --peer-report compliance/reports/peer/oidc.discovery.md \
  --waiver-file compliance/waivers/claims.yaml
```

| Flag | Example |
|---|---|
| `--claim-id` | `tba-auth claims promote --claim-id oauth2.pkce --to-tier 3` |
| `--to-tier` | `tba-auth claims promote --claim-id oauth2.pkce --to-tier 4` |
| `--peer-report` | `tba-auth claims promote --claim-id oauth2.pkce --to-tier 4 --peer-report compliance/reports/peer/oauth2.pkce.md` |
| `--waiver-file` | `tba-auth claims promote --claim-id oauth2.pkce --to-tier 3 --waiver-file compliance/waivers/claims.yaml` |

---

## `adr`

### `adr new`

```bash
tba-auth adr new \
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
| `--id` | `tba-auth adr new --id 0011 --title 'Adopt PAR'` |
| `--title` | `tba-auth adr new --title 'Adopt PAR for production profile'` |
| `--status` | `tba-auth adr new --title 'Adopt PAR' --status accepted` |
| `--supersedes` | `tba-auth adr new --title 'Replace prior key policy' --supersedes 0003` |
| `--owners` | `tba-auth adr new --title 'Adopt PAR' --owners 'security-team,platform-team'` |
| `--template` | `tba-auth adr new --title 'Adopt PAR' --template default` |
| `--target` | `tba-auth adr new --title 'Adopt PAR' --target oauth2.par` |
| `--` | `tba-auth adr new --title 'Adopt PAR' --hardening-interop` |
| `--tier` | `tba-auth adr new --title 'Adopt PAR' --tier 4` |

### `adr list`

```bash
tba-auth adr list --status accepted --target oidc.discovery --format json
```

| Flag | Example |
|---|---|
| `--status` | `tba-auth adr list --status proposed` |
| `--target` | `tba-auth adr list --target oauth2.pkce` |
| `--format` | `tba-auth adr list --format yaml` |

### `adr show`

```bash
tba-auth adr show --id 0006 --render markdown
```

| Flag | Example |
|---|---|
| `--id` | `tba-auth adr show --id 0006` |
| `--render` | `tba-auth adr show --id 0006 --render json` |

### `adr check`

```bash
tba-auth adr check \
  --required \
  --changed-path tba_auth/standards/oauth2/pushed_authorization.py \
  --fail-missing \
  --enforce-target-links
```

| Flag | Example |
|---|---|
| `--required` | `tba-auth adr check --required` |
| `--no-required` | `tba-auth adr check --no-required` |
| `--changed-path` | `tba-auth adr check --changed-path tba_auth/standards/oauth2/token.py` |
| `--fail-missing` | `tba-auth adr check --fail-missing` |
| `--no-fail-missing` | `tba-auth adr check --no-fail-missing` |
| `--enforce-target-links` | `tba-auth adr check --enforce-target-links` |
| `--no-enforce-target-links` | `tba-auth adr check --no-enforce-target-links` |

### `adr index`

```bash
tba-auth adr index --output docs/adr/index.md --format markdown
```

| Flag | Example |
|---|---|
| `--output` | `tba-auth adr index --output docs/adr/index.md` |
| `--format` | `tba-auth adr index --format json` |

---

## `doctor`

```bash
tba-auth doctor --check all --fix --database-url postgresql://user:pass@db/auth --issuer https://auth.example.com --format json
```

| Flag | Example |
|---|---|
| `--check` | `tba-auth doctor --check keys` |
| `--fix` | `tba-auth doctor --check routes --fix` |
| `--no-fix` | `tba-auth doctor --check routes --no-fix` |
| `--database-url` | `tba-auth doctor --database-url postgresql://user:pass@db/auth` |
| `--issuer` | `tba-auth doctor --issuer https://auth.example.com` |
| `--format` | `tba-auth doctor --format yaml` |

---

## `keys`

### `keys rotate`

```bash
tba-auth keys rotate \
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
| `--provider` | `tba-auth keys rotate --provider kms` |
| `--kid` | `tba-auth keys rotate --kid 2026-03-prod-01` |
| `--alg` | `tba-auth keys rotate --alg ES256` |
| `--use` | `tba-auth keys rotate --use sig` |
| `--activation-time` | `tba-auth keys rotate --activation-time 2026-03-19T12:00:00Z` |
| `--retire-after` | `tba-auth keys rotate --retire-after 90d` |
| `--publish-jwks` | `tba-auth keys rotate --publish-jwks` |
| `--no-publish-jwks` | `tba-auth keys rotate --no-publish-jwks` |
| `--dry-run` | `tba-auth keys rotate --dry-run` |

### `keys jwks`

```bash
tba-auth keys jwks --public-only --issuer https://auth.example.com --output build/jwks.json --format json
```

| Flag | Example |
|---|---|
| `--public-only` | `tba-auth keys jwks --public-only` |
| `--no-public-only` | `tba-auth keys jwks --no-public-only` |
| `--issuer` | `tba-auth keys jwks --issuer https://auth.example.com` |
| `--output` | `tba-auth keys jwks --output build/jwks.json` |
| `--format` | `tba-auth keys jwks --format yaml` |

### `keys verify`

```bash
tba-auth keys verify \
  --token eyJ... \
  --jwks-uri https://auth.example.com/.well-known/jwks.json \
  --alg-allow ES256,RS256 \
  --aud api://resource-server \
  --iss https://auth.example.com \
  --now 2026-03-19T12:00:00Z
```

| Flag | Example |
|---|---|
| `--token` | `tba-auth keys verify --token eyJ...` |
| `--jwks-uri` | `tba-auth keys verify --token eyJ... --jwks-uri https://auth.example.com/.well-known/jwks.json` |
| `--alg-allow` | `tba-auth keys verify --token eyJ... --alg-allow ES256,RS256` |
| `--aud` | `tba-auth keys verify --token eyJ... --aud api://resource-server` |
| `--iss` | `tba-auth keys verify --token eyJ... --iss https://auth.example.com` |
| `--now` | `tba-auth keys verify --token eyJ... --now 2026-03-19T12:00:00Z` |

---

## Suggested aliases for daily use

```bash
# local service
tba-auth -c configs/dev.toml serve --reload --dev-seed-keys

# build and validate contracts
tba-auth spec build --target all --kind all && \
tba-auth spec validate --input specs/

# run production gate
tba-auth verify all --production-readiness --tier 3 && \
tba-auth gate run --production-readiness --tier 3 --release 1.2.3

# build peer-claim bundle
tba-auth verify interop --profile all --record-wire --publish-report && \
tba-auth evidence collect --source all && \
tba-auth evidence bundle --output dist/evidence.tar.gz --sign
```
