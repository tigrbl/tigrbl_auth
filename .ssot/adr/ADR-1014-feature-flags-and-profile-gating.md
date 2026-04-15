# ADR-1014: Feature flags and profile gating are release-governed surfaces

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Feature flags and profile gating are release-governed surfaces

- Status: Accepted
- Date: 2026-03-20

## Context

`tigrbl_auth` needs two explicit flag surfaces: environment-backed standards and
surface flags inside the runtime, and operator-facing CLI flags for serving,
governance, and control-plane administration. Without a governed registry,
downstream partial feature adoption becomes ambiguous and non-certifiable.

## Decision

- Standards targets shall be grouped into baseline, production, hardening,
  alignment-only, operational, surface, and extension-quarantine flag groups.
- Profiles shall gate which targets are mounted, emitted in discovery,
  represented in contracts, and claimable in the compliance plane.
- Legacy flag labels may remain only as migration history and may not drive new
  certification claims.
- A disabled feature must disappear from mounted surfaces, contracts, manifests,
  and release evidence.

## Consequences

- downstream users can adopt partial features without inheriting undeclared
  surfaces,
- operator UX becomes explicit and scriptable,
- governance tooling can fail closed when targets and flags diverge.
