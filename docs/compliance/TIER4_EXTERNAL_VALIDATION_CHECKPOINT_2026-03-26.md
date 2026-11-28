# Tier 4 external validation Tier 4 External Validation Checkpoint — 2026-03-26

## Truthful status

- certifiably fully featured: `False`
- certifiably fully RFC compliant: `False`
- strict_independent_claims_ready: `False`
- tier4_bundle_promotion_complete: `False`

## What changed in this checkpoint

- added the missing `--require-full-boundary` CLI flag to `scripts/materialize_tier4_peer_evidence.py`
- hardened Tier 4 bundle validation to reject:
  - repository-staged fixture roots
  - self/non-independent evidence sources
  - placeholder manifests
  - missing peer operator identity
  - missing attesting organization/contact/timestamp metadata
  - missing `package_team_member=false`
  - missing `repository_fixture_generated=false`
  - execution-style mismatches
- made Tier 4 reporting truthful for preserved vs. valid vs. invalid external bundles
- updated the Tier 4 handoff package in `dist/tier4-external-handoff/` with stronger manifest templates, validation rules, and checklist requirements
- regenerated repository-staged fixture roots so they are explicitly marked **non-qualifying** and cannot truthfully be used for Tier 4 promotion
- added regression coverage proving that repository-staged fixtures fail closed and that `--require-full-boundary` returns non-zero when the retained boundary is not fully covered by valid external bundles

## Why this checkpoint matters

A critical fail-closed gap existed before this checkpoint: repository-generated fixture bundles could be materialized as if they were qualifying independent external peer evidence. This checkpoint closes that gap.

## What verified here

Targeted regression and evidence-hardening validation passed:

- `tests/interop/test_tier4_fixture_rejection.py`
- `tests/unit/test_tier4_checkpoint.py`
- `tests/interop/test_tier4_external_handoff_templates.py`
- `tests/interop/test_peer_matrix_external_status.py`
- `tests/interop/test_tier4_promotion_fail_closed.py`

Result: `7 passed`

## Current remaining blockers

This checkpoint does **not** complete final certification. The remaining blockers are still:

- supported runtime-matrix evidence is incomplete
- supported certification-lane evidence is incomplete
- PostgreSQL migration portability evidence is still missing
- real independent external peer bundles for all `16` required profiles are still missing
- therefore the retained boundary is still **not** fully Tier 4 promoted

## Current state references

- `CURRENT_STATE.md`
- `CERTIFICATION_STATUS.md`
- `docs/compliance/peer_matrix_report.md`
- `docs/compliance/TIER4_PEER_PROGRAM_STATUS_2026-03-25.md`
- `docs/runbooks/EXTERNAL_INTEROP_AND_TIER4_PROMOTION.md`
