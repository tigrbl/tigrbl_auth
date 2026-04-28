<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# RFC_FAMILY_RUNTIME_RFC_FAMILY_COMPLETION

## Summary

This checkpoint completes the planned RFC-family runtime checkpoint workstreams for the repository release path by replacing several previously helper-only or partial advanced RFC slices with live, mounted, contract-visible runtime behavior. The result is a substantially more complete production and hardening surface, but not a final certification-grade claim that the package is fully featured or fully RFC/spec compliant across the entire declared boundary.

## Workstream 7A — Token and client lifecycle

Completed in the active release path:

- RFC 7009 revocation remains mounted on the canonical `/revoke` surface
- RFC 7591 dynamic client registration remains mounted on `/register`
- RFC 7592 dynamic client management is now mounted on `/register/{client_id}` with GET, PUT, and DELETE operations bound to durable registration metadata and audit events
- RFC 7662 introspection remains persistence-backed in the persistence-domain checkpoint lifecycle model
- RFC 9068 JWT access token profile is now applied through the token service and issuance paths rather than remaining a helper-only slice

## Workstream 7B — Advanced authorization request surface

Completed in the active release path:

- RFC 9126 PAR remains mounted and now normalizes request-object, resource, and authorization-details inputs before persistence
- RFC 9101 request objects are now parsed and merged into the `/authorize` and `/par` flows
- RFC 9396 authorization details are now normalized in both `/authorize` and `/par`
- RFC 8707 resource indicators are now enforced across `/authorize`, `/token`, `/device_authorization`, `/par`, and `/token/exchange`

## Workstream 7C — Sender-constrained and delegated token hardening

Completed in the active release path:

- RFC 8705 certificate-bound token semantics are now enforced in the package as a gateway-mediated certificate-thumbprint binding profile
- RFC 9449 DPoP proof validation remains active and is now coupled to the hardening runtime and contract generation
- RFC 8693 token exchange is now audience/resource-aware and aligned with sender-constrained issuance

## Workstream 7D — Native, device, and browser specialization

Completed in the active release path:

- RFC 8252 native application redirect and PKCE guardrails are now enforced during registration and authorization
- RFC 8628 device authorization is now resource-aware and persistence-backed
- RFC 9728 protected-resource metadata remains active in production and hardening profiles

## Key files changed in this checkpoint

- `tigrbl_auth/ops/register.py`
- `tigrbl_auth/api/rest/routers/register.py`
- `tigrbl_auth/ops/authorize.py`
- `tigrbl_auth/ops/par.py`
- `tigrbl_auth/ops/device_authorization.py`
- `tigrbl_auth/ops/token.py`
- `tigrbl_auth/ops/login.py`
- `tigrbl_auth/standards/oauth2/token_exchange.py`
- `tigrbl_auth/services/token_service.py`
- `tigrbl_auth/standards/oauth2/rfc9700.py`
- `tigrbl_auth/cli/artifacts.py`
- `compliance/mappings/target-to-module.yaml`
- `compliance/mappings/target-to-endpoint.yaml`
- `compliance/mappings/target-to-test.yaml`

## Exit criteria assessment

### Retained target RFCs now live in the release path

The retained RFC-family runtime checkpoint RFC family members now have owned runtime modules, endpoint mappings where applicable, profile gating, test mapping, and evidence references.

### What still prevents a final certification-grade claim

This checkpoint still does **not** truthfully support a final claim that the package is certifiably fully featured or certifiably fully RFC/spec compliant across the full declared boundary. The remaining blockers are now dominated by certification maturity rather than basic surface absence:

- Tier 3 evidence bundles are not yet promoted across the full retained boundary
- Tier 4 independent peer validation is still absent
- release signing and attestation are still checkpoint-grade
- assertion-based and sender-constrained features still need broader certification-grade interop breadth, especially for gateway-mediated mTLS and limited-signing-profile JAR support
- RFC 7516, RFC 7521, and RFC 7523 remain helper-bounded and not promoted into a certification-grade fully implemented state
