<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# browser-session checkpoint — Canonical CLI Verb and Flag Contract

## Result

This checkpoint completes the **browser-session checkpoint CLI contract refactor** against the provided public-route checkpoint runtime-launcher checkpoint.

The CLI surface is now generated from a stronger metadata contract that includes:

- `CommandSpec`
- `VerbSpec`
- `FlagSpec`
- `OutputSpec`
- `ExitCodeSpec`

Derived artifacts now generated from the same metadata source:

- `docs/reference/CLI_SURFACE.md`
- `specs/cli/cli_contract.json`
- `specs/cli/cli_contract.yaml`
- `docs/compliance/cli_conformance_snapshot.json`
- `docs/compliance/cli_conformance_snapshot.md`

## Current measured state

- CLI command count: `21`
- CLI verb count: `86`
- CLI contract artifact present: `True`
- CLI conformance snapshot present: `True`
- CLI help snapshot present: `True`
- Catalog-only resource command count: `0`
- Missing required verb families: `False`
- Release gates passing: `20/20`

## What changed

- refactored `tigrbl_auth/cli/metadata.py` into a canonical command/verb/flag/output/exit-code contract model
- regenerated argparse parser, markdown CLI docs, help snapshots, and machine-readable CLI contract artifacts from that metadata
- expanded operator/admin families from list/show-only to explicit lifecycle verb families
- added repository-backed checkpoint handlers for operator/admin resources so the certified CLI boundary is no longer catalog-only
- added `bootstrap apply/verify` and `migrate apply`
- added key lifecycle verbs and JWKS publication handlers
- added import/export portability verbs and repository-backed status tracking
- updated compliance target/mapping manifests and test classification for the browser-session checkpoint checkpoint
- updated state reports and release bundles to include CLI contract artifacts

## Truthful status

This checkpoint is **not** yet certifiably fully featured and **not** yet certifiably fully RFC/spec compliant across the full declared boundary.

Reasons still open include:

- many retained production and hardening RFC/OIDC targets remain below full Tier 3 closure
- Tier 4 independent peer validation is still absent across the full retained boundary
- the CLI operator plane is now explicit and stateful, but several verbs are still **repository-backed checkpoint implementations**, not full production admin/RPC parity
- clean-checkout runtime validation in this environment is still blocked by missing published runtime dependencies such as `tigrbl`
- Tigrcorn remains unavailable in this checkpoint environment

## Validation performed in this environment

- parser generation from metadata succeeded
- CLI contract artifact generation succeeded
- CLI conformance snapshot generation succeeded
- boundary enforcement passed
- release gates passed: `20/20`
- release bundle build/sign/verify and recertification completed

## Validation limits

Full `pytest` collection still cannot be completed in this container because the published runtime dependency set is not installed here, and repository `tests/conftest.py` imports `tigrbl` during collection.
