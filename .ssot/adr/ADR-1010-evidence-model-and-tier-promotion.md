# ADR-1010: Evidence bundles are required for tier promotion

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Evidence bundles are required for tier promotion

- Status: Accepted
- Date: 2026-03-19
- Supersedes: none

## Context

A standards target is not certifiable merely because code exists. Promotion from
intent to implementation to certification requires preserved evidence with clear
traceability.

## Decision

Tier promotion is governed as follows:
- Tier 1: target declared
- Tier 2: target implemented and internally asserted
- Tier 3: target evidenced, mapped, and release-gated
- Tier 4: target independently peer-supported

Every target promoted beyond Tier 1 must map to:
- code modules
- operator surface
- tests
- contracts where applicable
- evidence artifacts

## Consequences

- No Tier 3 promotion without preserved evidence bundles.
- Release automation must fail closed when evidence is missing.
