> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Release Signing and Verification

## Purpose

runtime-foundation checkpoint2 replaces digest-only and HMAC checkpoint signing with asymmetric, externally verifiable release attestations.

## What is signed

For each retained deployment profile release bundle under `dist/release-bundles/<version>/<profile>/`, the repository now signs:

- `release-bundle.json`
- the copied effective claim manifest
- the copied effective evidence manifest
- `attestations/contract-set.manifest.json`
- a top-level `attestations/release-attestation.json` binding the signed artifact set together

## Signature model

- algorithm: `Ed25519`
- attestation format: signed JSON statements with canonicalized payloads
- signature binding includes:
  - signer identity
  - signer key identifier
  - issuance timestamp
  - artifact path
  - artifact digest
  - package/version/profile context

## Verification material

Each signed bundle contains:

- `signature.json` — signing summary and per-artifact attestation references
- `attestations/release-attestation.json` — top-level bundle attestation
- `attestations/*.attestation.json` — per-artifact attestations
- `attestations/keys/*.pub.pem` — public verification key
- `attestations/signer-identity.json` — signer identity manifest

## Signing inputs

Preferred CI inputs:

- `TIGRBL_AUTH_RELEASE_SIGNING_KEY_FILE` — path to an Ed25519 private-key PEM
- `TIGRBL_AUTH_RELEASE_SIGNING_KEY_PEM` — inline Ed25519 private-key PEM
- `TIGRBL_AUTH_RELEASE_SIGNING_KEY` — file path, PEM, or inline secret used to derive a deterministic Ed25519 key
- `TIGRBL_AUTH_RELEASE_SIGNER_ID` — signer identity label included in the attestation payload

If no key material is supplied, the tooling generates an ephemeral checkpoint signing key and writes only the public verification material into the release bundle.

## Standard flow

1. `python scripts/build_release_bundle.py`
2. `python scripts/sign_release_bundle.py`
3. `python scripts/verify_release_signing.py`
4. `python scripts/run_release_gates.py`

## Verification behavior

`python scripts/verify_release_signing.py` fails closed when any of the following are true:

- a required bundle is missing
- a required artifact attestation is missing
- an artifact digest does not match the attested digest
- the release-attestation signature fails validation
- multiple signing identities are mixed within the same bundle

## CI integration

The runtime-foundation checkpoint2 gate is installed as `gate-60-release-signing` and is executed as part of the release-gate pipeline.

The release-bundle workflow now:

1. builds the bundles
2. signs the bundles
3. verifies the signed bundles
4. uploads the resulting artifacts

## Current checkpoint limitation

The bundle signatures are now asymmetric and externally verifiable, but this checkpoint still does not claim full certification closure because Tier 4 independent peer evidence remains absent and some retained targets remain below full certification-grade maturity.