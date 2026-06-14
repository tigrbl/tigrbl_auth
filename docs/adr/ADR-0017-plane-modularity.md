> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Runtime planes own one concern each

- Status: Accepted
- Date: 2026-03-20

## Context

The package is certifiable only if boundaries stay strict. The runtime must be
modular by plane rather than by incidental file history.

## Decision

The release path is organized into these planes:

- `api/` for transport,
- `tables/` for persistence,
- `ops/` for transaction-owning orchestration,
- `services/` for reusable domain services,
- `standards/` for protocol-specific behavior,
- `security/` for cross-cutting hardening,
- `config/` for profile and feature resolution,
- `adapters/` for provider and trust seams,
- `cli/` for operator and certification UX,
- `plugin.py` and `gateway.py` for Tigrbl-native composition.

Package prefixes follow the same single-concern rule:

- `tigrbl-identity-*` owns neutral identity records and operational support,
- `tigrbl-authn-*` owns credential proof and authentication lifecycle,
- `tigrbl-authz-*` owns authority, policy, grants, permissions, decisions, and enforcement,
- `tigrbl-auth-protocol-*` owns OAuth/OIDC/RP wire behavior,
- `tigrbl-auth*` owns composed products and front doors.

## Consequences

- downstream extension work can be quarantined cleanly,
- traceability from standards target to owning plane becomes machine-checkable,
- the package tree becomes easier to certify and to refactor.
