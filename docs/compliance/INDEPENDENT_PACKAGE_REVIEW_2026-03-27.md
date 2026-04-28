> [!WARNING]
> Non-authoritative supporting review. For the current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, `CERTIFICATION_STATUS.md`, and the generated current-state reports.

# Independent package review — 2026-03-27

## Update — target/profile truth reconciliation complete

A later alignment-only update in the same checkpoint series resolved the previously reported retained scope/claim mismatches for `RFC 7516`, `RFC 7592`, and `RFC 9207`. No new certification evidence was collected in that follow-up. The remaining final-certification blockers in this review still apply.

## Executive summary

After extracting and reviewing this checkpoint, the package remains **not certifiably fully featured** and **not certifiably fully RFC/spec compliant**.

The decisive blockers are not primarily missing source files for the retained boundary. The larger problem is that the repository's **certification evidence plane is incomplete**:

- the preserved validated runtime matrix is still empty for the required supported cells;
- the preserved in-scope certification lane inventory is incomplete;
- PostgreSQL migration portability is not preserved as passing;
- Tier 4 independent external peer bundles are still absent and replaced by handoff/checklist placeholders.

This review also identified two truthfulness/alignment issues that were fixed directly in this checkpoint update:

1. `tigrbl_auth/config/settings.py` defaulted `enable_rfc9700` to `False` while `tigrbl_auth/config/deployment.py` defaulted the same capability to `True`. That caused a settings-driven hardening deployment to disagree with the deployment resolver's own default model.
2. `compliance/claims/repository-state.yaml` still said `release_gate_passed_for_final_decision: true` even though the release-gate reports are currently red.

## What is complete now

### Retained target boundary

The retained boundary is broadly built out at the repository evidence tier:

- retained in-scope targets: `48`
- retained RFC targets: `30`
- retained non-RFC targets: `18`
- partial retained targets reported in the current checkpoint: `0`
- Tier 3 ready targets: `48`
- Tier 4 ready targets: `0`

In other words: the repository currently presents a **Tier 3-complete retained target set**, but **not a certifiable final release**.

### RFC targets reported as built out at Tier 3

The current retained RFC target set is:

- RFC 6265
- RFC 6749
- RFC 6750
- RFC 7009
- RFC 7515
- RFC 7516
- RFC 7517
- RFC 7518
- RFC 7519
- RFC 7521
- RFC 7523
- RFC 7591
- RFC 7592
- RFC 7636
- RFC 7662
- RFC 8252
- RFC 8414
- RFC 8615
- RFC 8628
- RFC 8693
- RFC 8705
- RFC 8707
- RFC 9068
- RFC 9101
- RFC 9126
- RFC 9207
- RFC 9396
- RFC 9449
- RFC 9700
- RFC 9728

### Non-RFC / operational / platform targets reported as built out at Tier 3

- ASGI 3 application package
- Runner profile: Uvicorn
- Runner profile: Hypercorn
- Runner profile: Tigrcorn
- CLI operator surface
- Bootstrap and migration lifecycle
- Key lifecycle and JWKS publication
- Import/export portability
- Release bundle and signature verification
- OpenAPI 3.1 / 3.2 compatible public contract
- OpenRPC 1.4.x admin/control-plane contract
- OIDC Core 1.0
- OIDC Discovery 1.0
- OIDC UserInfo
- OIDC Session Management
- OIDC RP-Initiated Logout
- OIDC Front-Channel Logout
- OIDC Back-Channel Logout

### Target features currently passing in the repository evidence model

The current feature-completeness report shows these capabilities as passing:

- initialize repo/project tree
- bootstrap storage
- register/manage clients
- rotate and publish keys / JWKS
- export/import state
- emit OpenAPI/OpenRPC/discovery artifacts
- build, sign, and verify release bundles
- remain Tigrbl-native with no FastAPI/Starlette drift

## Gaps still preventing final certification

### 1. Validated runtime matrix is not preserved as green

The required supported runtime matrix expects `14` validated runtime cells, but the current preserved count is `0`.

Missing required runtime identities include:

- `base@py3.10`
- `base@py3.11`
- `base@py3.12`
- `sqlite-uvicorn@py3.10`
- `sqlite-uvicorn@py3.11`
- `sqlite-uvicorn@py3.12`
- `postgres-hypercorn@py3.10`
- `postgres-hypercorn@py3.11`
- `postgres-hypercorn@py3.12`
- `tigrcorn@py3.11`
- `tigrcorn@py3.12`
- `devtest@py3.10`
- `devtest@py3.11`
- `devtest@py3.12`

This blocks truthful claims that the app factory, serve checks, and HTTP surface probes are preserved as passing across the kept certification matrix.

### 2. In-scope certification lanes are not preserved as green

The current validated execution inventory expects `15` in-scope test lanes. The repository preserves only `5` in-scope passing lane manifests, all on Python 3.11.

The missing in-scope lanes are:

- `core@py3.10`
- `core@py3.12`
- `integration@py3.10`
- `integration@py3.12`
- `conformance@py3.10`
- `conformance@py3.12`
- `security-negative@py3.10`
- `security-negative@py3.12`
- `interop@py3.10`
- `interop@py3.12`

The repository also contains out-of-scope `py3.13` validated manifests, which are useful as supporting evidence but cannot close the supported certification matrix.

### 3. Migration portability is only preserved for SQLite

The current migration portability report shows:

- SQLite: passing
- PostgreSQL: unavailable / not preserved as passing

That means the package cannot truthfully claim validated upgrade → downgrade → reapply portability across both supported storage backends.

### 4. Tier 4 independent peer validation is still missing

The current retained peer program expects `16` external Tier 4 bundles.

Current preserved counts:

- Tier 4 external bundles: `0`
- valid external bundles: `0`
- missing external bundles: `16`

The handoff tree still contains `45` placeholder artifacts under `dist/tier4-external-handoff/**/required-artifact-placeholders/`.

Representative incomplete placeholder files include:

- `dist/tier4-external-handoff/browser/required-artifact-placeholders/browser-trace.json.placeholder.txt`
- `dist/tier4-external-handoff/gateway/required-artifact-placeholders/http-transcript.yaml.placeholder.txt`
- `dist/tier4-external-handoff/mtls/required-artifact-placeholders/certificate-chain.pem.placeholder.txt`
- `dist/tier4-external-handoff/resource-server/required-artifact-placeholders/result.yaml.placeholder.txt`
- `dist/tier4-external-handoff/runner-uvicorn/required-artifact-placeholders/result.yaml.placeholder.txt`
- `dist/tier4-external-handoff/runner-hypercorn/required-artifact-placeholders/result.yaml.placeholder.txt`
- `dist/tier4-external-handoff/runner-tigrcorn/required-artifact-placeholders/result.yaml.placeholder.txt`

Until those placeholders are replaced with preserved external results, the package cannot make strict independent/public certification claims.

### 5. Release gates are still red

The current release gate reports still fail at least:

- `gate-20-tests`
- `gate-90-release`

That alone prevents a truthful final-release certification statement.

## Scope discrepancies and alignment gaps

The previously reported retained claim-boundary mismatches for `RFC 7516`, `RFC 7592`, and `RFC 9207` are now resolved in the current checkpoint state.

These items were not primarily missing code-paths; they were **claim-boundary mismatches** between profile flags / effective deployment behavior and retained target-profile declarations. The current repository state now aligns those declarations with runtime behavior before any new certification evidence is collected.

Files most directly involved in those discrepancies include:

- `tigrbl_auth/config/feature_flags.py`
- `tigrbl_auth/config/deployment.py`
- `compliance/targets/rfc-targets.yaml`
- `docs/compliance/TARGET_REALITY_MATRIX.md`
- `docs/compliance/rfc_family_status_report.md`

## Files and modules that are incomplete or still blocked

### Evidence / certification artifact files that are incomplete by repository truth

- `dist/validated-runs/*.json` is incomplete relative to the supported certification matrix.
- `dist/tier4-external-handoff/**/required-artifact-placeholders/*` is intentionally incomplete and still waiting for independent external artifacts.
- `docs/compliance/runtime_profile_report.md` shows no preserved ready runtime profiles.
- `docs/compliance/validated_execution_report.md` shows incomplete validated inventory.
- `docs/compliance/migration_portability_report.md` shows PostgreSQL portability as unavailable in the preserved run inventory.
- `docs/compliance/final_release_gate_report.md` shows the final release aggregation as failing.

### Source modules that still prevent a certifiable final claim

These modules are not necessarily missing implementation, but they sit directly on the remaining certification blockers:

- `tigrbl_auth/config/feature_flags.py` — profile/claim alignment decisions
- `tigrbl_auth/config/deployment.py` — effective target activation and route/flag truth
- `tigrbl_auth/config/settings.py` — runtime default truthfulness
- `tigrbl_auth/runtime/*.py` — supported runner claim boundary and serve-check execution model
- `tigrbl_auth/cli/runtime.py` — runtime inventory and readiness reporting
- `tigrbl_auth/cli/reports.py` — state-report aggregation and final certification truth surfaces
- `tigrbl_auth/migrations/**` and `scripts/run_migration_portability.py` — portability validation closure
- `scripts/record_validated_run.py` — preservation of validated matrix evidence
- `scripts/materialize_tier4_peer_evidence.py` — Tier 4 bundle promotion mechanics

## Direct changes applied in this checkpoint update

This review checkpoint applies the following concrete fixes:

1. `tigrbl_auth/config/settings.py`
   - changed `enable_rfc9700` default from environment-false to environment-true by default;
   - this now matches `tigrbl_auth/config/deployment.py` and eliminates a hardening-profile truth mismatch.

2. `compliance/claims/repository-state.yaml`
   - changed `release_gate_passed_for_final_decision` from `true` to `false`;
   - this now matches the red release-gate reports.

3. `tests/unit/test_truthfulness_alignment.py`
   - added regression coverage for the RFC 9700 default-alignment fix;
   - added regression coverage for the release-gate truthfulness fix.

## Bottom line

The package is **substantially built out** and the retained target boundary is **Tier 3 complete**, but it is **not yet certifiably fully featured** and **not yet certifiably fully RFC/spec compliant**.

The remaining work is dominated by:

- preserved clean-room runtime evidence,
- preserved cross-version test-lane evidence,
- PostgreSQL portability evidence,
- Tier 4 external peer evidence,
- runtime-matrix, test-lane, migration-portability, and Tier 4 closeout work after the already-completed profile/claim scope normalization for RFC 7516 / RFC 7592 / RFC 9207.
