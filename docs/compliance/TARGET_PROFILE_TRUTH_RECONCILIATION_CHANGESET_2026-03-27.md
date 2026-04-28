# Target/Profile Truth Reconciliation Changeset — 2026-03-27

## Scope of this checkpoint update

This update is limited to **target/profile truth reconciliation** for the three retained RFC targets that previously had profile/scope mismatches:

- `RFC 7516`
- `RFC 7592`
- `RFC 9207`

No new certification evidence was collected in this changeset. The purpose of the update is to normalize the repository's retained truth across manifests, deployment activation, target buckets, surface manifests, generated reports, and checkpoint documentation before any additional certification evidence is gathered.

## Reconciled truth

| Target | Earliest claimable profile | Active profiles | Scope bucket | Public surface |
|---|---|---|---|---|
| RFC 7516 | `baseline` | `baseline`, `production`, `hardening` | `baseline-certifiable-now` | no standalone route; JOSE/JWE helper support and conditional discovery metadata |
| RFC 7592 | `production` | `production`, `hardening` | `production-completion-required` | `/register/{client_id}` |
| RFC 9207 | `production` | `production`, `hardening` | `production-completion-required` | `/authorize`, `/.well-known/openid-configuration` |

## Repository areas updated

- `compliance/targets/rfc-targets.yaml`
- `compliance/targets/target-buckets.yaml`
- `compliance/claims/declared-target-claims.yaml`
- `compliance/targets/public-operator-surface.yaml`
- `compliance/claims/repository-state.yaml`
- `tigrbl_auth/cli/claims.py`
- `tigrbl_auth/cli/feature_surface.py`
- `scripts/generate_certification_scope.py`
- `scripts/generate_release_decision_record.py`
- `scripts/materialize_tier4_peer_evidence.py`
- `tests/unit/test_truthfulness_alignment.py`
- `README.md`
- `docs/reference/PUBLIC_ROUTE_SURFACE.md`
- `docs/compliance/README.md`
- `docs/compliance/STEP12_FINAL_CERTIFICATION_AGGREGATION_CHECKPOINT_2026-03-27.md`
- regenerated current-state and scope reports under `docs/compliance/`

## Validation executed in this checkpoint

- `python scripts/generate_effective_release_manifests.py`
- `python scripts/generate_certification_scope.py`
- `python scripts/generate_state_reports.py`
- `python scripts/generate_rfc_family_status_report.py`
- `python -c "from scripts.materialize_tier4_peer_evidence import update_final_target_decision_matrix; update_final_target_decision_matrix()"`
- `python scripts/generate_release_decision_record.py`
- `python scripts/generate_package_review_gap_analysis.py`
- `pytest -q tests/unit/test_truthfulness_alignment.py`
- strict claims lint
- strict feature-surface/modularity lint

## Result

The retained target/profile mismatch set for `RFC 7516`, `RFC 7592`, and `RFC 9207` is now empty in the authoritative scope and generated current-state reports.

This checkpoint is **still not** a certifiably fully featured package and **still not** a certifiably fully RFC compliant package. The remaining blockers continue to be the preserved supported-matrix runtime inventory, supported test-lane inventory, migration portability preservation, and Tier 4 independent peer evidence.
