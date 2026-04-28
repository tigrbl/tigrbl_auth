<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# release signing checkpoint — Release Signing and Attestation Completion

## Objective

Replace checkpoint-grade SHA-256/HMAC bundle integrity with a real asymmetric signing and verification workflow.

## What changed

- release bundles are now signed with `Ed25519`
- claims, evidence, and contract artifacts inside the release bundle are individually attested
- a top-level release attestation now binds the signed artifact set together
- public verification key material is written into each signed release bundle
- a verification script now fails closed when a signed artifact, digest, or attestation is missing or invalid
- a new release gate, `gate-60-release-signing`, is installed and enforced
- the release-bundle GitHub workflow now signs and verifies artifacts before upload

## Signed artifact coverage

For each signed bundle profile, the bundle contains attestations for:

- release bundle manifest
- effective claim manifest
- effective evidence manifest
- contract set manifest
- aggregate release attestation

## Verification outputs

release signing checkpoint adds:

- `scripts/verify_release_signing.py`
- `docs/compliance/release_signing_report.md`
- `docs/compliance/release_signing_report.json`
- `docs/runbooks/RELEASE_SIGNING_AND_VERIFICATION.md`

## Honest status

This work closes the repository's earlier release-signing gap materially.

It does **not** by itself make the package certifiably fully featured or certifiably fully RFC/spec compliant across the full declared certification boundary.

The remaining blockers are now concentrated in:

- missing independent Tier 4 external peer evidence
- incomplete full-boundary Tier 3 promotion
- still-bounded RFC targets such as RFC 7516, RFC 7521, and RFC 7523
- broader certification-grade runtime and interop breadth for some advanced production and hardening targets
