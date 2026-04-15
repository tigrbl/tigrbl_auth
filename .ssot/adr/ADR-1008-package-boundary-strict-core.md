# ADR-1008: Define the strict package boundary

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Define the strict package boundary

- Status: Accepted
- Date: 2026-03-19
- Supersedes: none

## Context

The repository contains both a target auth-core and adjacent security / identity work.
Without a strict package boundary, the package can overclaim standards coverage,
blend extension work into the certified surface, and produce ambiguous release
artifacts.

## Decision

`tigrbl_auth` is certified only as a **Tigrbl-native OAuth 2.0 Authorization
Server + OpenID Connect Provider + discovery / trust plane**. The public auth
plane, admin/control plane, contract plane, and governance plane are all within
scope when they are declared, mapped, and release-gated.

Everything else is either:
- extension-quarantined, or
- alignment-only.

## Consequences

- Claims are permitted only for declared core targets.
- Partial feature enablement must not leak disabled or quarantined claims into
  metadata, generated contracts, or evidence bundles.
- Out-of-scope work may exist in the repository, but it is not certifiable by
  default.
