# ADR-1005: Release gates are defined as code

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Release gates are defined as code

- Status: Accepted
- Date: 2026-03-19

## Context

Structure, lint, tests, conformance, contracts, evidence, and release
promotion are evaluated through declarative gate manifests.

## Decision

This ADR is accepted for the current repository checkpoint.

## Consequences

- Architectural traceability is required.
- Standards claims must map to code, tests, and evidence.
