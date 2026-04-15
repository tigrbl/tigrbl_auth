# ADR-1003: Direct FastAPI and Starlette imports are forbidden

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Direct FastAPI and Starlette imports are forbidden

- Status: Accepted
- Date: 2026-03-19

## Context

The active runtime package must not directly import FastAPI or Starlette.
Tigrbl and Tigrbl type exports are the framework boundary.

## Decision

This ADR is accepted for the current repository checkpoint.

## Consequences

- Architectural traceability is required.
- Standards claims must map to code, tests, and evidence.
