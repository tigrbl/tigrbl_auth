# CLI Surface

> Generated from `tigrbl_auth.cli.metadata`; argparse help, CLI docs, contract artifacts, and conformance snapshots derive from the same metadata source.

## Global flags

- `--config` — Path to the runtime/configuration file.
- `--env-file` — Optional environment file loaded before resolution.
- `--profile` — Effective standards/compliance profile.
- `--tenant` — Tenant identifier for multi-tenant operators.
- `--issuer` — Issuer override for discovery and contract generation.
- `--surface-set` — Installable surface set. May be supplied multiple times.
- `--slice` — Protocol slice. May be supplied multiple times.
- `--extension` — Extension boundary slice. May be supplied multiple times.
- `--plugin-mode` — Plugin composition mode.
- `--runtime-style` — Runtime style for installation or standalone serving.
- `--strict` — Fail closed when governance or certification checks fail.
- `--no-strict` — Downgrade failures to warnings for exploratory use.
- `--format` — Output format.
- `--output` — Optional output file path.
- `--verbose, -v` — Increase operator verbosity; may be repeated.
- `--trace` — Emit trace-oriented operator details.

## Runtime

### `serve`

Resolve deployment, materialize a runner-qualified runtime plan, validate the selected profile, and optionally launch runtime.

- Flags:
  - `--repo-root` — Repository root for governance automation.
  - `--report-dir` — Directory for generated reports.
  - `--environment` — Deployment environment label.
  - `--server` — Runner profile used to qualify and launch runtime.
  - `--host` — Bind host.
  - `--port` — Bind port.
  - `--workers` — Process count for the selected runtime profile.
  - `--uds` — Optional Unix domain socket path.
  - `--log-level` — Operator log level for serve plans.
  - `--access-log` — Enable access logging for the selected runtime profile.
  - `--proxy-headers` — Honor proxy forwarding headers.
  - `--lifespan` — ASGI lifespan policy.
  - `--graceful-timeout` — Graceful shutdown timeout in seconds.
  - `--pid-file` — Optional PID file written for the launched runtime.
  - `--health` — Enable health endpoints in serve plans.
  - `--metrics` — Enable metrics in serve plans.
  - `--public` — Enable the public REST/auth plane.
  - `--admin` — Enable the admin/control plane.
  - `--rpc` — Enable the JSON-RPC control plane.
  - `--diagnostics` — Enable diagnostics surfaces.
  - `--require-tls` — Require TLS on the public plane.
  - `--enable-mtls` — Enable mTLS slice for the serve plan.
  - `--cookies` — Enable cookie/session helpers in serve plans.
  - `--jwks-refresh-seconds` — JWKS refresh cadence in seconds.
  - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
  - `--check` — Validate the selected runner profile and application factory without launching runtime.
  - `--db-safe-start` — Require a safe database start posture.
  - `--uvicorn-loop` — Uvicorn event-loop implementation.
  - `--uvicorn-http` — Uvicorn HTTP protocol implementation.
  - `--uvicorn-ws` — Uvicorn WebSocket implementation.
  - `--hypercorn-worker-class` — Hypercorn worker class.
  - `--hypercorn-http2` — Enable HTTP/2 ALPN for Hypercorn.
  - `--tigrcorn-contract` — Preferred Tigrcorn adapter contract.
  - `--tigrcorn-mode` — Preferred Tigrcorn runtime mode hint.
- Output: `runtime-launch` — Runtime plan, runner diagnostics, and launch/evidence metadata.
- Exit codes:
  - `0` — Operation completed successfully.
  - `1` — Operation failed or verification did not pass.
  - `2` — CLI argument or contract validation failed before execution.
- Examples:
  - `tigrbl-auth serve --server uvicorn --check`
  - `tigrbl-auth serve --server hypercorn --host 0.0.0.0 --port 8443`
  - `tigrbl-auth serve --server tigrcorn --dry-run --format yaml`

## Governance and certification

### `verify`

Execute one or more verification scopes and emit structured results.

- Flags:
  - `--repo-root` — Repository root for governance automation.
  - `--report-dir` — Directory for generated reports.
  - `--scope` — Verification scope.
- Output: `verification-report` — Verification result payload with summary, failures, and warnings.
- Exit codes:
  - `0` — Operation completed successfully.
  - `1` — Operation failed or verification did not pass.
  - `2` — CLI argument or contract validation failed before execution.

### `gate`

Run one release gate or the full ordered release gate catalog.

- Flags:
  - `--repo-root` — Repository root for governance automation.
  - `--report-dir` — Directory for generated reports.
  - `--name` — Optional named release gate or artifact selector.
- Output: `verification-report` — Verification result payload with summary, failures, and warnings.
- Exit codes:
  - `0` — Operation completed successfully.
  - `1` — Operation failed or verification did not pass.
  - `2` — CLI argument or contract validation failed before execution.

### `claims`

Operate on the claims plane.

- Verbs:
  - `lint` — Run claims lint.
    - `--repo-root` — Repository root for governance automation.
    - `--report-dir` — Directory for generated reports.
    - Output: `verification-report` — Verification result payload with summary, failures, and warnings.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `show` — Write the effective claims manifest.
    - `--repo-root` — Repository root for governance automation.
    - Output: `claims-artifact` — Claims/evidence payload describing effective certification state.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `status` — Summarize the claims plane.
    - `--repo-root` — Repository root for governance automation.
    - `--report-dir` — Directory for generated reports.
    - Output: `claims-artifact` — Claims/evidence payload describing effective certification state.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.

### `doctor`

Aggregate core verification, runtime profile, contracts, evidence, and gate status.

- Flags:
  - `--repo-root` — Repository root for governance automation.
  - `--report-dir` — Directory for generated reports.
- Output: `verification-report` — Verification result payload with summary, failures, and warnings.
- Exit codes:
  - `0` — Operation completed successfully.
  - `1` — Operation failed or verification did not pass.
  - `2` — CLI argument or contract validation failed before execution.

## Contracts and automation

### `spec`

Operate on the OpenAPI and OpenRPC contract surfaces.

- Verbs:
  - `generate` — Generate contract artifacts.
    - `--repo-root` — Repository root for governance automation.
    - `--kind` — Contract artifact kind.
    - `--report-dir` — Directory for generated reports.
    - Output: `contract-artifact` — OpenAPI/OpenRPC contract generation or validation payload.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `validate` — Validate generated contracts.
    - `--repo-root` — Repository root for governance automation.
    - `--kind` — Contract artifact kind.
    - `--report-dir` — Directory for generated reports.
    - Output: `contract-artifact` — OpenAPI/OpenRPC contract generation or validation payload.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `diff` — Diff generated contracts.
    - `--repo-root` — Repository root for governance automation.
    - `--kind` — Contract artifact kind.
    - `--baseline-file` — Optional explicit baseline artifact for diff operations.
    - `--report-dir` — Directory for generated reports.
    - Output: `contract-artifact` — OpenAPI/OpenRPC contract generation or validation payload.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `report` — Write contract summary reports.
    - `--repo-root` — Repository root for governance automation.
    - `--kind` — Contract artifact kind.
    - `--report-dir` — Directory for generated reports.
    - Output: `contract-artifact` — OpenAPI/OpenRPC contract generation or validation payload.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.

## Evidence and peer validation

### `evidence`

Operate on Tier 3/Tier 4 evidence automation.

- Verbs:
  - `bundle` — Build an evidence bundle.
    - `--repo-root` — Repository root for governance automation.
    - `--tier` — Evidence tier selector.
    - `--bundle-dir` — Explicit bundle output directory.
    - Output: `release-artifact` — Release bundle, signing, or recertification payload.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `status` — Summarize evidence readiness.
    - `--repo-root` — Repository root for governance automation.
    - `--tier` — Evidence tier selector.
    - `--report-dir` — Directory for generated reports.
    - Output: `verification-report` — Verification result payload with summary, failures, and warnings.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `verify` — Verify evidence and peer references.
    - `--repo-root` — Repository root for governance automation.
    - `--report-dir` — Directory for generated reports.
    - Output: `verification-report` — Verification result payload with summary, failures, and warnings.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `peer-status` — Summarize peer profile execution readiness.
    - `--repo-root` — Repository root for governance automation.
    - `--report-dir` — Directory for generated reports.
    - Output: `resource-collection` — Collection output for list/status operations.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `peer-execute` — Materialize peer execution manifests.
    - `--repo-root` — Repository root for governance automation.
    - `--peer-profile` — Peer profile selector. May be supplied multiple times.
    - `--execution-mode` — Peer execution mode.
    - `--report-dir` — Directory for generated reports.
    - Output: `resource-collection` — Collection output for list/status operations.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.

## Bootstrap, migration, and operator lifecycle

### `bootstrap`

Materialize and verify baseline bootstrap manifests for deployment or plugin installation.

- Verbs:
  - `status` — Summarize bootstrap readiness.
    - `--repo-root` — Repository root for governance automation.
    - `--report-dir` — Directory for generated reports.
    - Output: `resource-collection` — Collection output for list/status operations.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `manifest` — Write bootstrap manifests.
    - `--repo-root` — Repository root for governance automation.
    - `--bundle-dir` — Explicit bundle output directory.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `apply` — Apply bootstrap materialization.
    - `--repo-root` — Repository root for governance automation.
    - `--bundle-dir` — Explicit bundle output directory.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - `--wait` — Wait for completion when the operation supports asynchronous execution.
    - `--timeout` — Maximum wait time in seconds for supported long-running operations.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `verify` — Verify bootstrap artifacts.
    - `--repo-root` — Repository root for governance automation.
    - `--report-dir` — Directory for generated reports.
    - Output: `verification-report` — Verification result payload with summary, failures, and warnings.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.

### `migrate`

Migration-chain status, planning, application, and verification operators.

- Verbs:
  - `status` — Show migration status.
    - `--repo-root` — Repository root for governance automation.
    - `--report-dir` — Directory for generated reports.
    - Output: `resource-collection` — Collection output for list/status operations.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `plan` — Emit migration plan details.
    - `--repo-root` — Repository root for governance automation.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `apply` — Apply the migration checkpoint plan.
    - `--repo-root` — Repository root for governance automation.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - `--wait` — Wait for completion when the operation supports asynchronous execution.
    - `--timeout` — Maximum wait time in seconds for supported long-running operations.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `verify` — Verify migration artifacts.
    - `--repo-root` — Repository root for governance automation.
    - `--report-dir` — Directory for generated reports.
    - Output: `verification-report` — Verification result payload with summary, failures, and warnings.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.

## Release certification and recertification

### `release`

Release automation and recertification operators.

- Verbs:
  - `bundle` — Build a release bundle.
    - `--repo-root` — Repository root for governance automation.
    - `--bundle-dir` — Explicit bundle output directory.
    - `--artifact` — Release artifact subset.
    - Output: `release-artifact` — Release bundle, signing, or recertification payload.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `sign` — Sign a release bundle.
    - `--repo-root` — Repository root for governance automation.
    - `--bundle-dir` — Explicit bundle output directory.
    - `--signing-key` — Optional Ed25519 private signing key path or seed.
    - Output: `release-artifact` — Release bundle, signing, or recertification payload.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `verify` — Verify a signed release bundle.
    - `--repo-root` — Repository root for governance automation.
    - `--bundle-dir` — Explicit bundle output directory.
    - Output: `release-artifact` — Release bundle, signing, or recertification payload.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `status` — Summarize release bundle status.
    - `--repo-root` — Repository root for governance automation.
    - `--report-dir` — Directory for generated reports.
    - Output: `release-artifact` — Release bundle, signing, or recertification payload.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `recertify` — Run recertification checks.
    - `--repo-root` — Repository root for governance automation.
    - `--report-dir` — Directory for generated reports.
    - Output: `verification-report` — Verification result payload with summary, failures, and warnings.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.

## Admin/control and resource planes

### `tenant`

Stateful durable operator-plane tenant lifecycle operators.

- Verbs:
  - `create` — Create a tenant record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--from-file` — Load mutation input from a JSON or YAML file.
    - `--set` — Inline mutation field assignment in key=value form. May be supplied multiple times.
    - `--if-exists` — Behavior when the target already exists.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - `--wait` — Wait for completion when the operation supports asynchronous execution.
    - `--timeout` — Maximum wait time in seconds for supported long-running operations.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `update` — Update a tenant record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--from-file` — Load mutation input from a JSON or YAML file.
    - `--set` — Inline mutation field assignment in key=value form. May be supplied multiple times.
    - `--if-missing` — Behavior when the target does not already exist.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - `--wait` — Wait for completion when the operation supports asynchronous execution.
    - `--timeout` — Maximum wait time in seconds for supported long-running operations.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `delete` — Delete a tenant record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `get` — Get a tenant record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `list` — List tenant records.
    - `--repo-root` — Repository root for governance automation.
    - `--filter` — Simple substring filter applied to identifiers or names.
    - `--limit` — Maximum number of results to return.
    - `--offset` — Result offset for list operations.
    - `--sort` — Sort key for list operations.
    - `--status` — Status filter for list operations.
    - Output: `resource-collection` — Collection output for list/status operations.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `enable` — Enable a tenant.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `disable` — Disable a tenant.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.

### `client`

Stateful durable operator-plane client lifecycle operators.

- Verbs:
  - `create` — Create a client record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--from-file` — Load mutation input from a JSON or YAML file.
    - `--set` — Inline mutation field assignment in key=value form. May be supplied multiple times.
    - `--if-exists` — Behavior when the target already exists.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - `--wait` — Wait for completion when the operation supports asynchronous execution.
    - `--timeout` — Maximum wait time in seconds for supported long-running operations.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `update` — Update a client record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--from-file` — Load mutation input from a JSON or YAML file.
    - `--set` — Inline mutation field assignment in key=value form. May be supplied multiple times.
    - `--if-missing` — Behavior when the target does not already exist.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - `--wait` — Wait for completion when the operation supports asynchronous execution.
    - `--timeout` — Maximum wait time in seconds for supported long-running operations.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `delete` — Delete a client record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `get` — Get a client record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `list` — List client records.
    - `--repo-root` — Repository root for governance automation.
    - `--filter` — Simple substring filter applied to identifiers or names.
    - `--limit` — Maximum number of results to return.
    - `--offset` — Result offset for list operations.
    - `--sort` — Sort key for list operations.
    - `--status` — Status filter for list operations.
    - Output: `resource-collection` — Collection output for list/status operations.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `rotate-secret` — Rotate a client secret.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `enable` — Enable a client.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `disable` — Disable a client.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.

### `identity`

Stateful durable operator-plane identity lifecycle operators.

- Verbs:
  - `create` — Create an identity record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--from-file` — Load mutation input from a JSON or YAML file.
    - `--set` — Inline mutation field assignment in key=value form. May be supplied multiple times.
    - `--if-exists` — Behavior when the target already exists.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - `--wait` — Wait for completion when the operation supports asynchronous execution.
    - `--timeout` — Maximum wait time in seconds for supported long-running operations.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `update` — Update an identity record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--from-file` — Load mutation input from a JSON or YAML file.
    - `--set` — Inline mutation field assignment in key=value form. May be supplied multiple times.
    - `--if-missing` — Behavior when the target does not already exist.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - `--wait` — Wait for completion when the operation supports asynchronous execution.
    - `--timeout` — Maximum wait time in seconds for supported long-running operations.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `delete` — Delete an identity record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `get` — Get an identity record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `list` — List identity records.
    - `--repo-root` — Repository root for governance automation.
    - `--filter` — Simple substring filter applied to identifiers or names.
    - `--limit` — Maximum number of results to return.
    - `--offset` — Result offset for list operations.
    - `--sort` — Sort key for list operations.
    - `--status` — Status filter for list operations.
    - Output: `resource-collection` — Collection output for list/status operations.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `set-password` — Set an identity password.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--from-file` — Load mutation input from a JSON or YAML file.
    - `--set` — Inline mutation field assignment in key=value form. May be supplied multiple times.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `lock` — Lock an identity.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `unlock` — Unlock an identity.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.

### `flow`

Stateful durable operator-plane flow lifecycle operators.

- Verbs:
  - `create` — Create a flow record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--from-file` — Load mutation input from a JSON or YAML file.
    - `--set` — Inline mutation field assignment in key=value form. May be supplied multiple times.
    - `--if-exists` — Behavior when the target already exists.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - `--wait` — Wait for completion when the operation supports asynchronous execution.
    - `--timeout` — Maximum wait time in seconds for supported long-running operations.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `update` — Update a flow record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--from-file` — Load mutation input from a JSON or YAML file.
    - `--set` — Inline mutation field assignment in key=value form. May be supplied multiple times.
    - `--if-missing` — Behavior when the target does not already exist.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - `--wait` — Wait for completion when the operation supports asynchronous execution.
    - `--timeout` — Maximum wait time in seconds for supported long-running operations.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `delete` — Delete a flow record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `get` — Get a flow record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `list` — List flow records.
    - `--repo-root` — Repository root for governance automation.
    - `--filter` — Simple substring filter applied to identifiers or names.
    - `--limit` — Maximum number of results to return.
    - `--offset` — Result offset for list operations.
    - `--sort` — Sort key for list operations.
    - `--status` — Status filter for list operations.
    - Output: `resource-collection` — Collection output for list/status operations.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `enable` — Enable a flow.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `disable` — Disable a flow.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.

### `session`

Stateful durable operator-plane session control operators.

- Verbs:
  - `get` — Get a session record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `list` — List session records.
    - `--repo-root` — Repository root for governance automation.
    - `--filter` — Simple substring filter applied to identifiers or names.
    - `--limit` — Maximum number of results to return.
    - `--offset` — Result offset for list operations.
    - `--sort` — Sort key for list operations.
    - `--status` — Status filter for list operations.
    - Output: `resource-collection` — Collection output for list/status operations.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `revoke` — Revoke a session.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `revoke-all` — Revoke all sessions.
    - `--repo-root` — Repository root for governance automation.
    - `--filter` — Simple substring filter applied to identifiers or names.
    - `--status` — Status filter for list operations.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.

### `token`

Stateful durable operator-plane token control operators.

- Verbs:
  - `get` — Get a token record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `list` — List token records.
    - `--repo-root` — Repository root for governance automation.
    - `--filter` — Simple substring filter applied to identifiers or names.
    - `--limit` — Maximum number of results to return.
    - `--offset` — Result offset for list operations.
    - `--sort` — Sort key for list operations.
    - `--status` — Status filter for list operations.
    - Output: `resource-collection` — Collection output for list/status operations.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `introspect` — Introspect a token.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `revoke` — Revoke a token.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `exchange` — Exchange a token.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--from-file` — Load mutation input from a JSON or YAML file.
    - `--set` — Inline mutation field assignment in key=value form. May be supplied multiple times.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.

### `keys`

Stateful durable operator-plane key lifecycle and JWKS publication operators.

- Verbs:
  - `generate` — Generate a key record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--kid` — Explicit key identifier.
    - `--alg` — JWA/JOSE algorithm identifier.
    - `--use` — JWK use classification.
    - `--kty` — JWK key type.
    - `--curve` — Curve for EC/OKP keys.
    - `--activate` — Mark a generated or imported key active immediately.
    - `--retire-after` — Retire-after hint or timestamp recorded with the key.
    - `--publish` — Publish JWKS after a successful key mutation.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `import` — Import key material.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--from-file` — Load mutation input from a JSON or YAML file.
    - `--input` — Input path for import, validation, or diff operations.
    - `--activate` — Mark a generated or imported key active immediately.
    - `--publish` — Publish JWKS after a successful key mutation.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `export` — Export key material.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--output` — Optional output file path.
    - `--format` — Output format.
    - `--include-secrets` — Include secret material where the selected surface permits it.
    - `--redact` — Redact secret material from exported output.
    - `--checksum` — Expected checksum or checksum algorithm for import/export validation.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `rotate` — Rotate active key material.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--kid` — Explicit key identifier.
    - `--alg` — JWA/JOSE algorithm identifier.
    - `--use` — JWK use classification.
    - `--kty` — JWK key type.
    - `--curve` — Curve for EC/OKP keys.
    - `--activate` — Mark a generated or imported key active immediately.
    - `--retire-after` — Retire-after hint or timestamp recorded with the key.
    - `--publish` — Publish JWKS after a successful key mutation.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `retire` — Retire a key.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - `--publish` — Publish JWKS after a successful key mutation.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `publish-jwks` — Publish JWKS.
    - `--repo-root` — Repository root for governance automation.
    - `--output` — Optional output file path.
    - `--format` — Output format.
    - `--include-secrets` — Include secret material where the selected surface permits it.
    - `--redact` — Redact secret material from exported output.
    - `--checksum` — Expected checksum or checksum algorithm for import/export validation.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `get` — Get a key record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `list` — List key records.
    - `--repo-root` — Repository root for governance automation.
    - `--filter` — Simple substring filter applied to identifiers or names.
    - `--limit` — Maximum number of results to return.
    - `--offset` — Result offset for list operations.
    - `--sort` — Sort key for list operations.
    - `--status` — Status filter for list operations.
    - Output: `resource-collection` — Collection output for list/status operations.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `delete` — Delete a key record.
    - `--repo-root` — Repository root for governance automation.
    - `--id` — Primary identifier for a single record.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.

### `discovery`

Discovery and metadata operators bound to repository snapshots.

- Verbs:
  - `show` — Show discovery metadata.
    - `--repo-root` — Repository root for governance automation.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `validate` — Validate discovery metadata.
    - `--repo-root` — Repository root for governance automation.
    - `--report-dir` — Directory for generated reports.
    - Output: `verification-report` — Verification result payload with summary, failures, and warnings.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `publish` — Publish discovery metadata.
    - `--repo-root` — Repository root for governance automation.
    - `--output` — Optional output file path.
    - `--format` — Output format.
    - `--checksum` — Expected checksum or checksum algorithm for import/export validation.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `diff` — Diff discovery metadata.
    - `--repo-root` — Repository root for governance automation.
    - `--input` — Input path for import, validation, or diff operations.
    - `--report-dir` — Directory for generated reports.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.

### `import`

Import durable operator-plane state from portable artifacts.

- Verbs:
  - `validate` — Validate import input.
    - `--repo-root` — Repository root for governance automation.
    - `--input` — Input path for import, validation, or diff operations.
    - `--format` — Output format.
    - `--checksum` — Expected checksum or checksum algorithm for import/export validation.
    - `--report-dir` — Directory for generated reports.
    - Output: `verification-report` — Verification result payload with summary, failures, and warnings.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `run` — Run an import.
    - `--repo-root` — Repository root for governance automation.
    - `--input` — Input path for import, validation, or diff operations.
    - `--format` — Output format.
    - `--checksum` — Expected checksum or checksum algorithm for import/export validation.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - `--wait` — Wait for completion when the operation supports asynchronous execution.
    - `--timeout` — Maximum wait time in seconds for supported long-running operations.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `status` — Show import status.
    - `--repo-root` — Repository root for governance automation.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.

### `export`

Export durable operator-plane state into portable artifacts.

- Verbs:
  - `validate` — Validate export configuration.
    - `--repo-root` — Repository root for governance automation.
    - `--output` — Optional output file path.
    - `--format` — Output format.
    - `--include-secrets` — Include secret material where the selected surface permits it.
    - `--redact` — Redact secret material from exported output.
    - `--checksum` — Expected checksum or checksum algorithm for import/export validation.
    - `--report-dir` — Directory for generated reports.
    - Output: `verification-report` — Verification result payload with summary, failures, and warnings.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
  - `run` — Run an export.
    - `--repo-root` — Repository root for governance automation.
    - `--output` — Optional output file path.
    - `--format` — Output format.
    - `--include-secrets` — Include secret material where the selected surface permits it.
    - `--redact` — Redact secret material from exported output.
    - `--checksum` — Expected checksum or checksum algorithm for import/export validation.
    - `--yes` — Assume yes for state-changing confirmations.
    - `--dry-run` — Resolve and emit the runtime plan without applying or launching state changes.
    - `--wait` — Wait for completion when the operation supports asynchronous execution.
    - `--timeout` — Maximum wait time in seconds for supported long-running operations.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
      - `3` — Requested record or dependent resource was not found.
  - `status` — Show export status.
    - `--repo-root` — Repository root for governance automation.
    - Output: `resource-record` — Single operator resource record with state and metadata.
    - Exit codes:
      - `0` — Operation completed successfully.
      - `1` — Operation failed or verification did not pass.
      - `2` — CLI argument or contract validation failed before execution.
