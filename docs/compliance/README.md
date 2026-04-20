# Compliance Reports

This directory contains generated current-state and release-decision artifacts.

## Current authoritative docs

Use `.ssot/specs/SPEC-1052-ssot-document-authority.yaml` as the authoritative active document for current document authority.

Use `docs/compliance/truth_chain.json` as the canonical generated checkpoint projection derived from that SSOT policy.

Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` only as a human-readable compatibility projection of the current doc set projected from SSOT. It is not authoritative.

The repository-root `CURRENT_STATE.md` and `CERTIFICATION_STATUS.md`, plus the generated report set listed in the compatibility projection manifest, are derived artifacts and must agree with `truth_chain.json` and the SSOT authority spec.

## Historical / non-authoritative docs

Historical and superseded planning/checkpoint material is retained under `docs/archive/`.

Files listed under `explicitly_deauthorized_current_adjacent_docs` in `compliance/targets/document-authority.yaml` are retained for history only and must not be used for current release claims.

## Certification bundle policy

Only the generated truth-chain and current-state artifacts listed under `current_release_bundle_docs` in `compliance/targets/document-authority.yaml` are copied into certification release bundles.
