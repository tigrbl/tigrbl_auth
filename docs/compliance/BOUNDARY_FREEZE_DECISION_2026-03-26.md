# Boundary Freeze Decision — 2026-03-26

## Decision

Freeze the retained certification boundary for closeout at the exact target set recorded in `compliance/targets/certification_scope.yaml`. Do not silently widen the meaning of `fully featured`, `fully RFC compliant`, or `fully non-RFC spec/standard compliant` during certification closeout.

## Freeze record

- decision_id: `BND-012`
- source_of_truth: `compliance/targets/certification_scope.yaml`
- effective_date: `2026-03-26`
- retained_target_count: `48`
- retained_rfc_target_count: `30`
- retained_non_rfc_target_count: `18`
- deferred_target_count: `25`
- retained_target_identity_hash: `b5caac77a8e8bc398c8d4679049f525d94ad701cd345eaa51498567972ce9f60`

## Required closeout rules

- no_target_count_drift_during_closeout: `True`
- closeout_scope_expansion_requires_separate_program: `True`
- fully_featured_claim_boundary_fixed: `True`

## Explicitly prohibited silent expansions

- RFC 7800
- RFC 8417
- RFC 8291
- RFC 8812
- RFC 8932
- OAuth 2.1 alignment profile
- SAML IdP/SP
- LDAP/AD federation
- SCIM
- policy-platform/federation breadth outside the declared boundary

## Current truthful status

This freeze improves claim hygiene and certification traceability. It does **not** make the package certifiably fully featured or certifiably fully RFC/spec compliant by itself. Final certification remains blocked by missing validated runtime/test/migration evidence and missing preserved Tier 4 independent peer bundles.

