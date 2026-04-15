# ADR-1011: Independent peer claims are a separate certification boundary

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Independent peer claims are a separate certification boundary

- Status: Accepted
- Date: 2026-03-19
- Supersedes: none

## Context

Independent peer claims require a stricter standard than internally generated
reports. They must be reproducible and attributable to external interop or peer
review material.

## Decision

Tier 4 claims require all of the following:
- a Tier 3 evidence bundle
- an identified peer or interop profile
- preserved peer artifacts
- reproducible execution instructions
- explicit promotion approval captured in the compliance plane

Peer claims are additive. They do not relax Tier 3 evidence requirements.

## Consequences

- A release may be fully functional without Tier 4 claims.
- No target may be described as independently supported unless the peer pack is
  present and the claim manifest is promoted.
