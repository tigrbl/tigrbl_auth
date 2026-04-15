# ADR-1015: Installable surfaces and partial feature consumption are first-class boundaries

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Installable surfaces and partial feature consumption are first-class boundaries

- Status: Accepted
- Date: 2026-03-20

## Context

Downstream users may need only the public auth plane, only the admin/control
plane, or a mixed plugin installation. If surface boundaries remain implicit,
the package cannot truthfully certify what is and is not exposed.

## Decision

`tigrbl_auth` shall treat the following as governed installable surfaces:

- public auth plane,
- admin/control plane,
- operator plane,
- JSON-RPC plane,
- diagnostics plane,
- plugin install modes.

The plugin and gateway roots shall use the same surface model, and every
surface shall be representable in manifests, CLI, and contracts.

## Consequences

- downstream partial-feature deployments stay explicit and reproducible,
- pluginability becomes a governed release concern instead of ad-hoc wiring,
- current and target surface gaps become measurable.
