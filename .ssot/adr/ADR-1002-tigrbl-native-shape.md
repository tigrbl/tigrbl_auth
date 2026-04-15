# ADR-1002: Adopt the Tigrbl-native package shape

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Adopt the Tigrbl-native package shape

- Status: Accepted
- Date: 2026-03-19

## Context

Runtime code is organized around `api`, `tables`, `ops`, `services`,
`standards`, `security`, `config`, `cli`, `plugin`, and `gateway`. The
package is Tigrbl-native and avoids ad-hoc framework routing.

## Decision

This ADR is accepted for the current repository checkpoint.

## Consequences

- Architectural traceability is required.
- Standards claims must map to code, tests, and evidence.
