> [!WARNING] Non-authoritative active checkpoint note. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and the generated compliance reports.

# Step 10 Tier 3 Evidence Rebuild Checkpoint — 2026-03-26

## Honest status

This checkpoint is **not certifiably fully featured** and **not certifiably fully RFC compliant**.

The Step 10 work completed the **Tier 3 rebuild-from-validated-runs requirement**, but it did **not** close the remaining certification blockers.

## What changed

- Reworked validated-artifact download collection so downloaded GitHub Actions artifacts are normalized into preserved local destinations for:
  - `dist/validated-runs/`
  - `dist/runtime-smoke/collected/`
  - `dist/runtime-profiles/collected/`
  - `dist/install-substrate/collected/`
  - `dist/test-reports/collected/`
  - `dist/migration-portability/collected/`
  - `docs/compliance/collected/`
- Hardened artifact collection so empty artifact directories fail the collection step instead of silently passing.
- Added validated-runs reporting mode for runtime-profile aggregation so `docs/compliance/runtime_profile_report.*` can now be rebuilt from preserved manifests rather than ad hoc local probing.
- Expanded validated-run manifests to be more self-describing, including report references and SHA-256 bindings.
- Added a generated Tier 3 evidence rebuild report:
  - `docs/compliance/tier3_evidence_rebuild_report.md`
  - `docs/compliance/tier3_evidence_rebuild_report.json`
- Hardened final aggregation so release readiness now fails explicitly when validated inventory is below the required threshold of:
  - `14` runtime cells
  - `15` supported certification lanes
  - `1` migration portability manifest
- Updated CI so missing expected upload payloads fail fast instead of warning-only.

## What verified in this checkpoint

- `tier3_evidence_rebuilt_from_validated_runs = True`
- `runtime_profile_report` now rebuilds in `validated-runs` mode
- targeted regression coverage passed for the Step 10 hardening paths
- release/state reports were regenerated after the Tier 3 rebuild

## Current preserved evidence posture

From the regenerated reports:

- required validated inventory: `30`
- validated inventory present: `6`
- runtime matrix present: `0 / 14`
- supported certification lanes present: `5 / 15`
- migration portability preserved for both SQLite and PostgreSQL: `False`
- Tier 3 rebuild from validated runs only: `True`
- Tier 4 external bundle promotion complete: `False`

## Why this is not a final certified release

The repository still lacks enough preserved supported-matrix evidence to support a truthful final certification claim. The remaining blockers are:

- full supported runtime-matrix evidence is still absent
- supported certification-lane evidence is still incomplete
- PostgreSQL migration portability evidence is still absent
- validated inventory is still below the required threshold
- Tier 4 external peer bundles are still missing for the retained boundary

## Files most relevant to Step 10

- `scripts/collect_validated_artifact_downloads.py`
- `scripts/record_validated_run.py`
- `tigrbl_auth/cli/runtime.py`
- `tigrbl_auth/cli/reports.py`
- `.github/workflows/ci-release-gates.yml`
- `tox.ini`
- `tests/unit/test_tier3_validated_rebuild.py`

## Current release-gate posture after Step 10

The regenerated release-gate state still has two failing gates:

- `gate-20-tests`
- `gate-90-release`

That outcome is consistent with the preserved evidence counts and is the truthful current state for this checkpoint.
