# Certifiable completion plan — 2026-03-26

This plan is ordered so every later certification statement is supported by preserved artifacts rather than by code presence alone.

## 1. Recreate the clean-room dependency environments

1. Provision Python 3.10, 3.11, 3.12, 3.13, and 3.14 environments.
2. Install the published dependency stack from `constraints/base.txt` plus the runner/storage extras required by each tox lane.
3. Verify that `tigrbl`, `swarmauri_*`, SQLAlchemy, bcrypt, and runner packages import in each target environment.
4. Fail the lane immediately if the app factory still cannot import `tigrbl`.

## 2. Make the runtime matrix pass with preserved evidence

1. Run the full kept runtime matrix from `tox.ini`:
   - `py310-base`, `py311-base`, `py312-base`
   - `py310-sqlite-uvicorn`, `py311-sqlite-uvicorn`, `py312-sqlite-uvicorn`
   - `py310-postgres-hypercorn`, `py311-postgres-hypercorn`, `py312-postgres-hypercorn`
   - `py311-tigrcorn`, `py312-tigrcorn`
   - `py310-devtest`, `py311-devtest`, `py312-devtest`
2. Preserve app-factory probe, serve-check, and HTTP surface-probe artifacts for every lane.
3. Record the results into the validated execution manifest so `runtime_matrix_green = true` is supported by artifacts, not inference.

## 3. Make the in-scope certification test lanes pass with preserved evidence

1. Execute the in-scope lane set across the supported interpreter matrix:
   - `core`
   - `integration`
   - `conformance`
   - `security-negative`
   - `interop`
2. Preserve machine-readable results for every lane.
3. Update `docs/compliance/validated_execution_report.*` so the lane counts and pass/fail truth are derived from those preserved artifacts.

## 4. Certify migration portability

1. Run upgrade → downgrade → reapply for SQLite.
2. Run upgrade → downgrade → reapply for PostgreSQL.
3. Preserve schema/version/result artifacts for both backends.
4. Do not mark portability complete until both backends are recorded as passing in the validated execution manifest.

## 5. Rebuild Tier 3 evidence from validated runs

1. Regenerate Tier 3 evidence bundles only after runtime matrix, test lanes, and migration portability are green.
2. Make the evidence rebuild consume validated-run manifests rather than local ad hoc state.
3. Re-run release-bundle generation and signature verification after the rebuild.

## 6. Complete Tier 4 independent peer validation

1. Use `dist/tier4-external-handoff/` to collect preserved external bundles for all `16` peer profiles.
2. Require peer identity, version, runtime/container provenance, transcripts, scenario outputs, and reproduction material for every submitted bundle.
3. Normalize and validate the incoming external bundles.
4. Promote Tier 4 targets only when the preserved bundle set is complete and passes validation.

## 7. Re-run all fail-closed gates

1. Re-run state-report generation.
2. Re-run release gates.
3. Re-run final release readiness.
4. Confirm these values are all true before making any final certification claim:
   - `fully_certifiable_now`
   - `fully_rfc_compliant_now`
   - `strict_independent_claims_ready`
   - `runtime_matrix_green`
   - `in_scope_test_lanes_green`
   - `migration_portability_passed`
   - `tier3_evidence_rebuilt_from_validated_runs`
   - `tier4_bundle_promotion_complete`

## 8. Cut the final certified release bundle

1. Rebuild release bundles for baseline, production, hardening, and peer-claim.
2. Re-sign the release bundle set.
3. Re-verify attestation signatures.
4. Freeze authoritative current docs.
5. Only then change top-level claims from candidate/blocked to final/certified.

## Acceptance criteria for a truthful “certifiably fully featured and certifiably fully RFC compliant” claim

- All `48` retained targets remain at least Tier 3.
- The validated runtime matrix is completely green and preserved.
- The validated in-scope test lanes are completely green and preserved.
- Migration portability is green for SQLite and PostgreSQL.
- Tier 3 evidence is rebuilt from validated runs.
- All `16` Tier 4 peer bundles are preserved and valid.
- Final release gates pass without warnings being used as substitutes for evidence.
