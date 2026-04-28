> [!WARNING]
> Non-authoritative supporting plan. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, `CERTIFICATION_STATUS.md`, and the generated current-state reports.

# Certifiable delivery plan — 2026-03-27

## Status update

The runtime-foundation checkpoint target/profile truth-normalization action for `RFC 7516`, `RFC 7592`, and `RFC 9207` is now complete in the current checkpoint. No new certification evidence was collected during that alignment-only update. The remaining tracks below are still open.

## Objective

Deliver a package that can truthfully claim all of the following at once:

- certifiably fully featured
- certifiably fully RFC/spec compliant for the retained boundary
- certifiably fully non-RFC spec/standard compliant for the retained non-RFC boundary
- strict independent/public claim readiness

## Ordered execution plan

### runtime-foundation checkpoint — eliminate claim-boundary ambiguity before new evidence is recorded

1. **Completed.** Normalize target/profile scope for the three previously reported discrepancies:
   - RFC 7516
   - RFC 7592
   - RFC 9207
2. Decide one truth for each target:
   - either move the target profile declaration to match the effective runtime surface,
   - or remove the runtime activation from profiles where the target is not claimed.
3. Update all of the following together so there is no split-brain truth:
   - `compliance/targets/rfc-targets.yaml`
   - `tigrbl_auth/config/feature_flags.py`
   - `tigrbl_auth/config/deployment.py`
   - `tigrbl_auth/config/surfaces.py`
   - generated route/contract/target reports in `docs/compliance/`
4. Regenerate:
   - target reality matrix
   - RFC family status report
   - OpenAPI / OpenRPC artifacts
   - claims/effective-target manifests
5. **Completed and now enforced by repository truth.** No new certification evidence is collected until the scope discrepancies report is empty.

### persistence-domain checkpoint — make the clean-room install substrate genuinely reproducible

1. Provision clean-room executors for Python `3.10`, `3.11`, and `3.12`.
2. Ensure every profile in `tox.ini` is installable only from pinned published dependencies and constraints.
3. Execute and preserve install-substrate verification for:
   - `base`
   - `sqlite-uvicorn`
   - `postgres-hypercorn`
   - `tigrcorn`
   - `devtest`
4. Require preserved install manifests for every supported interpreter/profile cell.
5. Reject any matrix run that depends on the current container's ad hoc dependency availability.

### public-route checkpoint — close the runtime matrix with preserved serve-check evidence

1. Run the required runtime cells:
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
2. For each runtime cell, preserve all of the following:
   - install manifest
   - app-factory probe result
   - serve-check result
   - HTTP surface probe result
   - environment identity and runner identity
3. Record every passing run via `scripts/record_validated_run.py runtime-profile`.
4. Fail the track unless `docs/compliance/runtime_profile_report.md` shows:
   - ready profiles > 0 for all kept runners,
   - validated runtime matrix green = true,
   - surface probe passed = true,
   - execution probe complete = true.

### browser-session checkpoint — close the in-scope certification lanes across the supported interpreter matrix

1. Run and preserve these in-scope lanes:
   - core on py310 / py311 / py312
   - integration on py310 / py311 / py312
   - conformance on py310 / py311 / py312
   - security-negative on py310 / py311 / py312
   - interop on py310 / py311 / py312
2. Preserve JSON manifests and pytest reports for each lane.
3. Record them into `dist/validated-runs/` using the supported identities only.
4. Exclude py313 evidence from certification counts, but keep it as supplemental evidence if useful.
5. Fail the track unless `docs/compliance/validated_execution_report.md` shows `in_scope_test_lanes_green: True`.

### operator-service checkpoint — close migration portability for both supported backends

1. Provision PostgreSQL in the clean-room matrix.
2. Execute migration portability runs on both:
   - SQLite
   - PostgreSQL
3. Preserve for each backend:
   - upgrade artifact
   - downgrade artifact
   - reapply artifact
   - exact revision identifiers
4. Record the run via `scripts/record_validated_run.py migration-portability`.
5. Fail the track unless `docs/compliance/migration_portability_report.md` shows both backends passing.

### runtime-hardening checkpoint — rebuild Tier 3 from validated evidence only

1. Re-run Tier 3 evidence materialization from the now-complete validated-run inventory.
2. Remove any residual dependency on older, non-validated, or out-of-scope manifests.
3. Rebuild:
   - target evidence mapping
   - certification state report
   - release decision record
   - release gate report
4. Confirm every retained target still has complete Tier 3 evidence after the rebuild.
5. Fail the track unless the Tier 3 rebuild is demonstrably sourced from preserved validated runs only.

### RFC-family runtime checkpoint — execute the Tier 4 peer program for the retained boundary

1. For each retained peer profile in the peer matrix, produce preserved external bundles.
2. Replace every placeholder under:
   - `dist/tier4-external-handoff/**/required-artifact-placeholders/`
   with the actual preserved artifact at the required path.
3. Preserve peer identity, runtime identity, independence assertions, and reproduction instructions.
4. Validate bundle structure and completeness using the Tier 4 tooling.
5. Promote only when every required bundle is both present and valid.
6. Fail the track unless:
   - Tier 4 external bundle count equals required bundle count,
   - missing count is zero,
   - invalid count is zero,
   - strict independent claims ready becomes true.

### capability-wiring checkpoint — final release gate aggregation

1. Re-run release-gate aggregation after Phases 1–7 are green.
2. Ensure these are all true simultaneously:
   - validated inventory complete
   - clean-room install matrix green
   - runtime profiles truly ready
   - in-scope test lanes green
   - migration portability passed
   - Tier 3 evidence rebuilt from validated runs
   - Tier 4 bundle promotion complete
3. Rebuild all current-state documents.
4. Verify README, `CURRENT_STATE.md`, `CERTIFICATION_STATUS.md`, and generated reports all tell the same truth.
5. Only then switch package-level statements from checkpoint/release-candidate wording to final certified-release wording.

## File-by-file worklist

### Claim-boundary normalization

- `compliance/targets/rfc-targets.yaml`
- `tigrbl_auth/config/feature_flags.py`
- `tigrbl_auth/config/deployment.py`
- `tigrbl_auth/config/surfaces.py`
- `docs/compliance/TARGET_REALITY_MATRIX.md`
- `docs/compliance/rfc_family_status_report.md`

### Runtime and validated evidence

- `tox.ini`
- `.github/workflows/ci-install-profiles.yml`
- `.github/workflows/ci-release-gates.yml`
- `scripts/verify_clean_room_install_substrate.py`
- `scripts/clean_room_profile_smoke.py`
- `scripts/record_validated_run.py`
- `docs/compliance/runtime_profile_report.md`
- `docs/compliance/validated_execution_report.md`

### Migration portability

- `scripts/run_migration_portability.py`
- `tigrbl_auth/migrations/**`
- `docs/compliance/migration_portability_report.md`
- `dist/migration-portability/**`

### Tier 4 independent evidence

- `scripts/materialize_tier4_peer_evidence.py`
- `dist/tier4-external-handoff/**`
- `docs/compliance/PEER_MATRIX_REPORT.md`
- `docs/compliance/TIER4_PROMOTION_MATRIX.md`

### Final state and release truth

- `docs/compliance/release_gate_report.md`
- `docs/compliance/final_release_gate_report.md`
- `docs/compliance/certification_state_report.md`
- `docs/compliance/RELEASE_DECISION_RECORD.md`
- `CURRENT_STATE.md`
- `CERTIFICATION_STATUS.md`
- `README.md`

## Exit criteria

The package should not be called certifiably fully featured or certifiably fully RFC compliant until all of the following are true at the same time:

- RFC scope discrepancy list is empty
- runtime matrix green is true
- in-scope test lanes green is true
- SQLite and PostgreSQL portability both pass
- Tier 4 required external bundle count equals valid external bundle count
- strict independent claims ready is true
- release gates passed is true
- all top-level and generated state documents agree
