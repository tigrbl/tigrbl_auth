> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

> **Historical / non-authoritative** — This document is retained for planning, provenance, or operator guidance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Architecture Decision Records

This directory contains the governing ADR set for `tba_auth`.

## Purpose

The package is not certifiable while standards scope, package shape, release
gates, evidence retention, peer-claim rules, feature-flag scope, installable
surfaces, and plane modularity are only implicit. ADRs are therefore part of
the release-critical governance plane.

## Required certification-bootstrap ADR coverage

| Concern | ADRs |
|---|---|
| Use ADRs as the governing architecture log | ADR-0001 |
| Certification boundary | ADR-0002, ADR-0009 |
| Tigrbl-native package shape | ADR-0003 |
| No direct FastAPI / Starlette runtime boundary | ADR-0004 |
| Standards vs extension quarantine | ADR-0005, ADR-0010 |
| Release gates as code | ADR-0006 |
| Contract generation | ADR-0007 |
| Evidence retention and peer claims | ADR-0008, ADR-0011, ADR-0012 |
| Vendor removal and no private shims | ADR-0013 |
| Tigrbl public-API-only composition | ADR-0014 |
| Feature flags and profile gating | ADR-0015 |
| Installable surfaces and partial feature consumption | ADR-0016 |
| Plane modularity | ADR-0017 |

## Status index

| ADR | Title | Status |
|---|---|---|
| ADR-0001 | use ADRs | Accepted |
| ADR-0002 | certification boundary | Accepted |
| ADR-0003 | Tigrbl-native shape | Accepted |
| ADR-0004 | no FastAPI / Starlette runtime | Accepted |
| ADR-0005 | standards vs extensions | Accepted |
| ADR-0006 | release gates as code | Accepted |
| ADR-0007 | contract generation | Accepted |
| ADR-0008 | evidence retention and peer claims | Accepted |
| ADR-0009 | strict core package boundary | Accepted |
| ADR-0010 | standards boundary and label hygiene | Accepted |
| ADR-0011 | evidence model and tier promotion | Accepted |
| ADR-0012 | independent peer claims | Accepted |
| ADR-0013 | vendor removal and no private shims | Accepted |
| ADR-0014 | Tigrbl public-API-only composition | Accepted |
| ADR-0015 | feature flags and profile gating | Accepted |
| ADR-0016 | installable surfaces and partial feature consumption | Accepted |
| ADR-0017 | plane modularity | Accepted |

## Rule

No release-eligible claim may bypass an ADR-backed decision on package boundary,
standards boundary, feature-flag scope, installable surfaces, or certification
evidence.