<!-- NON_AUTHORITATIVE_HISTORICAL -->
> [!WARNING]
> Historical / non-authoritative checkpoint document.
> Do **not** use this file to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Boundary Certification Plan

## Objective

Deliver a certifiable `tba_auth` package whose claims are bounded by declared
standards targets, enforced by code, and supported by release gates and
preserved evidence.

## Certification rules

1. Only declared targets are certifiable.
2. Only certified-core modules may back certifiable targets.
3. Legacy transition and extension quarantine modules are non-certifiable.
4. Contracts, claims, and evidence must be filtered by effective deployment.
5. Tier 3 requires preserved evidence references.
6. Tier 4 requires independent peer and interop evidence.
7. The target project tree and current-to-target move map are release-gated certification artifacts.

## Required gates

- gate-00-structure
- gate-05-governance
- gate-10-static
- gate-12-project-tree-layout
- gate-15-boundary-enforcement
- gate-18-migration-plan
- gate-25-wrapper-hygiene
- gate-30-contracts
- gate-35-contract-sync
- gate-40-evidence
- gate-45-evidence-peer
- gate-90-release

## Required reports

- claims_lint_report
- tba_runtime_foundation_report
- boundary_enforcement_report
- wrapper_hygiene_report
- contract_sync_report
- evidence_peer_readiness_report
- project_tree_layout_report
- migration_plan_status_report

## Current checkpoint status

The certification plan now covers the target project tree and the move map in
addition to the strict certified-core boundary. Boundary enforcement passes for
the certified core, but the repository remains below certifiable status because
production/hardening implementation and evidence maturity are still incomplete.
