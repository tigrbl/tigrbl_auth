<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# runtime-hardening checkpoint Hardening Runtime Enforcement

## Objective

Convert hardening posture from declarative policy into executable runtime behavior.

## Completed in this checkpoint

- enforced RFC 9700-aligned authorization-request policy in `tigrbl_auth/ops/authorize.py`
- enforced runtime grant-type policy in `tigrbl_auth/ops/token.py`
- disabled the password grant in hardening and peer-claim profiles
- disabled implicit and hybrid response types in hardening and peer-claim profiles
- made PAR mandatory in hardening and peer-claim profiles when RFC 9126 is active
- enforced sender-constrained token issuance in hardening and peer-claim profiles when DPoP or mTLS support is active
- updated discovery metadata so advertised response/grant types match the active runtime policy
- updated OpenAPI contract generation so hardening and peer-claim contracts reflect the executable policy surface
- aligned the peer-claim profile flag set with the hardening boundary for executable runtime posture
- added profile-aware discovery snapshot artifacts and runtime-hardening checkpoint test mappings

## Required outputs delivered

- `docs/reference/HARDENING_RUNTIME_ENFORCEMENT_MATRIX.md`
- `tests/negative/test_6_hardening_runtime_enforcement.py`
- `tests/unit/test_6_profile_discovery_runtime.py`
- `specs/discovery/profiles/*/openid-configuration.json`
- updated profile-specific OpenAPI artifacts, including `specs/openapi/profiles/peer-claim/`

## Honest limits that remain

This checkpoint materially improves hardening truthfulness for the core authorization, token, discovery, and contract paths, but it does not by itself make the repository certifiably fully featured or certifiably fully RFC/spec compliant across the entire declared boundary.

Remaining later-work still includes broader advanced-flow completion, preserved evidence promotion, Tier 4 peer validation, and stronger release attestation.
