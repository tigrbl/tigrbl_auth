# ADR-1012: Remove vendor directories and forbid private framework shims

> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Remove vendor directories and forbid private framework shims

- Status: Accepted
- Date: 2026-03-19
- Supersedes: none

## Context

The repository is being refactored into a Tigrbl-native package. Certifiable
releases must not depend on copied `vendor/` trees, shadow framework modules, or
private compatibility shims that obscure the real dependency and runtime
boundary.

## Decision

Release-eligible paths in `tigrbl_auth` must not introduce:
- a `vendor/` directory,
- copied framework code,
- private routing or lifecycle shims that impersonate Tigrbl public APIs,
- boundary-blurring re-export modules that hide the real implementation source.

The supported composition surface is:
- `tigrbl_auth.plugin`
- `tigrbl_auth.gateway`
- other package modules that use declared Tigrbl public APIs directly.

## Consequences

- Dependency provenance remains explicit and reviewable.
- Boundary scans can fail closed on any reintroduced `vendor/` tree or private
  framework shim.
- Future migration work must move or rewrite code instead of wrapping it behind
  hidden compatibility layers.
