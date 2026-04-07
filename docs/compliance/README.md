# Compliance Reports

This directory contains generated current-state and release-decision artifacts.

## Current authoritative docs

Use `docs/compliance/truth_chain.json` as the canonical generated checkpoint truth.

Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` to identify the current authoritative document set.

The repository-root `CURRENT_STATE.md` and `CERTIFICATION_STATUS.md`, plus the generated report set listed in the authority manifest, are derived artifacts and must agree with `truth_chain.json`.

## Historical / non-authoritative docs

Historical and superseded planning/checkpoint material is retained under `docs/archive/`.

Files listed under `explicitly_deauthorized_current_adjacent_docs` in `compliance/targets/document-authority.yaml` are retained for history only and must not be used for current release claims.

## Certification bundle policy

Only the generated truth-chain and current-state artifacts listed under `current_release_bundle_docs` in `compliance/targets/document-authority.yaml` are copied into certification release bundles.
