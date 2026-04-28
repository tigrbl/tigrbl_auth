<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# runtime-hardening checkpoint — Strict Boundary Decisions, Enforcement, and Certification Plan

This checkpoint completes the boundary-decision and enforcement workstream.

## Completed in this - normalized strict boundary classes: certified core, governance plane, legacy transition, extension quarantine, alignment-only, and out-of-scope baseline
- enriched boundary decisions with explicit checks and release-gate linkage
- added decision-to-check and decision-to-gate mappings
- upgraded the module-boundary map to distinguish certified core from legacy transition and extension quarantine modules
- added machine-checkable boundary import scanning, wrapper hygiene, contract sync, and evidence/peer readiness checks
- added an explicit boundary certification plan manifest
- refreshed current-state and certification-status documents

## What this proves

It proves that the repository can now distinguish:
- what is certifiable
- what is governance-only
- what is quarantined as an extension
- what is legacy transition material
- what is out of scope for the baseline boundary

## What still blocks certification

- certified-core release-path modules still import legacy transition modules in several places
- wrapper modules still exist in the repository, even though they are now quarantined from certification claims
- production and hardening targets remain incomplete or checkpoint-level
- Tier 3 and Tier 4 evidence remain incomplete
