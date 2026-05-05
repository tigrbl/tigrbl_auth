> [!WARNING] Proposal only. `.ssot/` remains authoritative. This document proposes SPEC work to close or normalize governance gaps. The target matrix is informative only and is not a normative design source.

# SPEC Gap Coverage Proposal

## Purpose

This proposal translates the ADR gap proposal into a concrete SPEC set. The intent is to define executable requirements for the missing or under-normalized governed surfaces.

Informative inputs:

- [ADR_GAP_COVERAGE_PROPOSAL.md](./docs/compliance/ADR_GAP_COVERAGE_PROPOSAL.md)
- [target_cell_ssot_entity_matrix.json](./docs/compliance/target_cell_ssot_entity_matrix.json)
- [final_target_decision_matrix.json](./docs/compliance/final_target_decision_matrix.json)

## Required Boundary SPEC Coverage

The proposal set shall include explicit SPECs for all four governed surfaces:

- admin UIX boundary
- public UIX boundary
- admin API boundary
- public API boundary

## Proposed SPEC Set

### Proposed `SPEC-1074` Admin UIX Boundary Requirements

Parent ADR:

- proposed `ADR-1054`

What this SPEC should define:

- admin UIX scope
- admin UIX route/screen classes
- required admin session gate behavior
- readiness/config/resource/policy/mutation surface membership
- explicit exclusions and redaction rules
- required separation from public UIX and public API concerns

Primary governed surface addressed:

- admin UIX

### Proposed `SPEC-1075` Public UIX Boundary Requirements

Parent ADR:

- proposed `ADR-1055`

What this SPEC should define:

- public UIX scope
- public UIX route/screen classes
- required user journeys
- required separation from admin UIX
- minimum supported feature bundle for:
  - login
  - logout
  - registration
  - session continuity
  - optional consent and recovery surfaces

Primary governed surface addressed:

- public UIX

Expected downstream features:

- `feat:uix-public-shell`
- `feat:uix-public-auth-session`
- `feat:uix-public-login-view`
- `feat:uix-public-logout-view`
- `feat:uix-public-registration-view`

### Proposed `SPEC-1076` Admin API Boundary Requirements

Parent ADR:

- proposed `ADR-1056`

What this SPEC should define:

- admin API scope
- authenticated/authorized control-plane requirements
- resource management scope
- policy administration API scope
- required separation from public API, public UIX, and CLI-only concerns
- contract expectations for admin API publication

Primary governed surface addressed:

- admin API

### Proposed `SPEC-1077` Public API Boundary Requirements

Parent ADR:

- proposed `ADR-1057`

What this SPEC should define:

- public API scope
- public OAuth/OIDC/discovery route requirements
- public registration/logout scope where applicable
- explicit exclusion of admin/control-plane operations
- required separation from public UIX presentation concerns
- contract expectations for public API publication

Primary governed surface addressed:

- public API

### Proposed `SPEC-1078` Surface Applicability and Scope Classification Requirements

Parent ADR:

- proposed `ADR-1058`

What this SPEC should define:

- canonical scope-classification vocabulary
- allowed evidence for each classification
- rules for how authoritative scope is declared in SSOT
- projection requirements for informative reports that summarize scope or coverage

Primary normative problems normalized:

- admin-only concerns being misread as public gaps
- public-only concerns being misread as admin gaps
- adjacent surfaces being misreported as uncovered

### Proposed `SPEC-1079` Public UIX Contract, Browser Security, and Error Handling

Parent ADR:

- proposed `ADR-1059`

What this SPEC should define:

- public UIX contract consumption rules
- cookie/session model
- CSRF requirements
- origin/redirect constraints
- browser-facing token handling rules
- problem-details rendering and disclosure rules

Primary governed surface addressed:

- public UIX

### Proposed `SPEC-1080` Transport Protocol Support and Applicability Requirements

Parent ADR:

- proposed `ADR-1060`

What this SPEC should define:

- per-surface meaning of:
  - `RFC 9112 HTTP/1.1`
  - `RFC 9113 HTTP/2`
  - `RFC 9114 HTTP/3`
  - `RFC 9000 QUIC`
- distinction between:
  - backend support
  - runtime enablement
  - contract visibility
  - browser/UIX dependency
  - certification claimability

Primary governed surfaces addressed:

- runtime
- admin API
- public API
- admin UIX
- public UIX

### Proposed `SPEC-1081` Supply Chain, Provenance, and Release Artifact Requirements

Parent ADR:

- proposed `ADR-1061`

What this SPEC should define:

- requirement mapping for:
  - `NIST SP 800-218 SSDF`
  - `SLSA`
  - `in-toto`
  - `Sigstore`
  - `SPDX`
  - `CycloneDX`
- required artifacts
- generated projections
- release-gate obligations
- disclosure obligations

Primary governed surfaces addressed:

- release and build provenance
- package and artifact publication
- API and UIX disclosure where relevant

### Proposed `SPEC-1082` Tenant Isolation and Client Policy Cross-Plane Requirements

Parent ADR:

- proposed `ADR-1062`

What this SPEC should define:

- tenant scoping rules across planes
- client policy visibility rules
- mutation and read-model constraints
- public-facing versus admin-only exposure
- cross-surface projection requirements for tenant/client policy concerns

Primary governed surfaces addressed:

- admin API
- public API
- admin UIX
- selected public UIX surfaces

### Proposed `SPEC-1083` UIX Schema, JOSE, and Safe Disclosure Requirements

Parent ADR:

- proposed `ADR-1063`

What this SPEC should define:

- UIX-safe disclosure model for:
  - `JSON Schema 2020-12`
  - `RFC 7515 JWS`
  - `RFC 7516 JWE`
  - selected JWT and JWKS presentation
- admin diagnostics versus public explanations
- redaction rules
- present-but-non-disclosing patterns

Primary governed surfaces addressed:

- admin UIX
- public UIX

## Recommended Authoring Order

1. `SPEC-1074` Admin UIX Boundary Requirements
2. `SPEC-1075` Public UIX Boundary Requirements
3. `SPEC-1076` Admin API Boundary Requirements
4. `SPEC-1077` Public API Boundary Requirements
5. `SPEC-1078` Surface Applicability and Scope Classification Requirements
6. `SPEC-1079` Public UIX Contract, Browser Security, and Error Handling
7. `SPEC-1080` Transport Protocol Support and Applicability Requirements
8. `SPEC-1081` Supply Chain, Provenance, and Release Artifact Requirements
9. `SPEC-1082` Tenant Isolation and Client Policy Cross-Plane Requirements
10. `SPEC-1083` UIX Schema, JOSE, and Safe Disclosure Requirements

## Recommended ADR-to-SPEC Mapping

| Proposed ADR | Proposed SPECs |
|---|---|
| `ADR-1054` | `SPEC-1074` |
| `ADR-1055` | `SPEC-1075` |
| `ADR-1056` | `SPEC-1076` |
| `ADR-1057` | `SPEC-1077` |
| `ADR-1058` | `SPEC-1078` |
| `ADR-1059` | `SPEC-1079` |
| `ADR-1060` | `SPEC-1080` |
| `ADR-1061` | `SPEC-1081` |
| `ADR-1062` | `SPEC-1082` |
| `ADR-1063` | `SPEC-1083` |

## What This Proposal Does Not Recommend

- it does not recommend one SPEC per RFC row
- it does not recommend using SPECs to hide applicability mistakes that should first be fixed in normative scope rules
- it does not recommend treating informative report symptoms as normative design requirements

## Next Step

If you want this promoted into SSOT work, the next concrete move is:

1. reserve SPEC numbers
2. author the four boundary SPECs first
3. author the scope-classification SPEC next
4. continue with contract/security, transport, provenance, tenant/client, and UIX disclosure requirements
