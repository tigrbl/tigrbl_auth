# RPC Operator Surface

## Summary

The operator/admin control plane is now implementation-backed.

The authoritative RPC surface is owned by `tigrbl_auth/api/rpc/`:

- `registry.py` owns method registration and deployment filtering
- `methods/` owns executable operator/admin handlers
- `schemas/` owns request/response models used by both handlers and OpenRPC
- `pkgs/60-runtime/tigrbl-identity-cli/src/tigrbl_identity_cli/cli/artifacts/` generates OpenRPC directly from the live registry
- `pkgs/60-runtime/tigrbl-identity-cli/src/tigrbl_identity_cli/cli/reports/` validates that committed OpenRPC methods match the implementation-backed registry exactly

## Contract generation model

OpenRPC generation now runs in **implementation-backed-rpc-registry** mode.
The contract is derived from `iter_active_rpc_methods(deployment)` and carries
per-method metadata identifying:

- owner module
- required flags
- surface set
- chronology provenance

This removes the prior detached catalog-only posture.

## Method families

### Governance and release-plane methods

- `rpc.discover`
- `flow.list`
- `discovery.show`
- `claims.lint`
- `claims.show`
- `gate.run`
- `evidence.status`
- `release.bundle`

### Directory and entity lookup methods

- `tenant.list`
- `tenant.show`
- `client.list`
- `client.show`
- `identity.list`
- `identity.show`

### Client-registration management methods

- `client.registration.list`
- `client.registration.show`
- `client.registration.upsert`

### Session and token inspection methods

- `session.list`
- `session.show`
- `session.terminate`
- `token.list`
- `token.inspect`

### Consent and audit methods

- `consent.list`
- `consent.show`
- `consent.revoke`
- `audit.list`
- `audit.export`

### Key and JWKS methods

- `keys.list`
- `jwks.show`
- `keys.rotate`

### Profile and certification introspection methods

- `profile.show`
- `target.list`
- `target.show`

## Ownership model

Every OpenRPC method must map to:

- an executable handler under `tigrbl_auth/api/rpc/methods/`
- a request model and result model under `tigrbl_auth/api/rpc/schemas/`
- an owner-module path embedded in the committed OpenRPC artifact
- an active method entry in the deployment-resolved registry

## Sync enforcement

The repository now fails contract validation when:

- a committed OpenRPC method is missing from the implementation registry
- an implementation-backed method is absent from the committed OpenRPC artifact
- an OpenRPC method omits `x-tigrbl-auth.owner_module`
- an owner-module path in the committed OpenRPC artifact does not exist
- admin-rpc is active but the contract has no methods or no schema components

## Current honest status

This checkpoint completes the operator-service checkpoint objective of replacing the catalog-only
OpenRPC surface with an implementation-backed operator/admin plane.

It does **not** mean the repository is already certifiably fully featured or
certifiably fully RFC/spec compliant across the full declared boundary.
Later hardening, evidence, peer-validation, and release-attestation work still
remains.
