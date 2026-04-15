# ADR-1004: Separate standards core from optional extensions

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Separate standards core from optional extensions

- Status: Accepted
- Date: 2026-03-19

## Context

RFCs and profiles that are outside the core auth-server certification
boundary live under `extensions/` or remain documented as future work.

## Decision

This ADR is accepted for the current repository checkpoint.

## Consequences

- Architectural traceability is required.
- Standards claims must map to code, tests, and evidence.
