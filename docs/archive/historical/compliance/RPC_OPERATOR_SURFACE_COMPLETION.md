<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# operator-service checkpoint RPC Operator Surface Completion

## Objective

Replace the catalog-only OpenRPC posture with an implementation-backed
operator/admin surface whose contract is generated from executable method
registration.

## Completed in this checkpoint

- implemented `tigrbl_auth/api/rpc/__init__.py` as the public entrypoint for the implementation-backed RPC plane
- added `tigrbl_auth/api/rpc/registry.py` to own method registration, filtering, and invocation helpers
- implemented executable method modules in `tigrbl_auth/api/rpc/methods/`
- implemented request/response schema modules in `tigrbl_auth/api/rpc/schemas/`
- replaced detached OpenRPC generation with contract generation derived from `iter_active_rpc_methods(deployment)`
- added method-level owner metadata, required flags, surface-set metadata, and provenance into the OpenRPC artifact
- strengthened contract validation so committed OpenRPC artifacts must match the implementation-backed registry exactly
- updated certification-scope target metadata, endpoint mappings, module mappings, and test mappings for the OpenRPC control plane
- added live unit coverage for the registry-backed OpenRPC generation path

## Operator/admin capabilities now surfaced

This checkpoint provides first-class implementation-backed RPC methods for:

- client registration management
- session inspection and administrative termination
- token inspection and introspection posture lookup
- consent inspection and revocation
- audit lookup and export
- key listing, JWKS inspection, and key rotation
- profile and certification-target introspection
- governance/release discovery and gate execution

## Honest limits that still remain

This checkpoint materially improves truthfulness of the admin plane, but it is
not the final certification state.

Remaining later-work still includes:

- full runtime hardening enforcement across the hardening boundary
- broader advanced RFC surface completion where still partial or deferred
- preserved Tier 3 evidence promotion across the full retained boundary
- independent Tier 4 peer validation
- stronger release signing and attestation

## Validation posture

The operator-service checkpoint checkpoint now expects contract validation and contract-sync checks
to fail closed if the implementation-backed registry and the committed OpenRPC
artifact drift apart.
