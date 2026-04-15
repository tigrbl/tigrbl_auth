# ADR-1009: Normalize standards labels and quarantine mis-scoped targets

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Normalize standards labels and quarantine mis-scoped targets

- Status: Accepted
- Date: 2026-03-19
- Supersedes: none

## Context

The repository inherited stale or wrong standards labels, including a legacy
`RFC 8523` label where the relevant OAuth JWT client-auth claim belongs to
RFC 7523, and repository material that treated RFC 8932 as if it were part of
authorization-server metadata rather than a quarantined non-auth-core target.

## Decision

The certification plane uses normalized labels only:
- `.well-known` claims use **RFC 8615**.
- JWT client-auth and authorization-grant claims use **RFC 7523**.
- RFC 8932 remains extension-quarantined and is not part of the auth-core claim
  boundary.
- Extension RFCs are documented under `compliance/targets/extension-targets.yaml`
  and are excluded from core certification manifests.

## Consequences

- Legacy labels may remain in repository history or non-certified files, but
  they cannot be emitted as current certification claims.
- Claims linting fails if corrected labels regress.
