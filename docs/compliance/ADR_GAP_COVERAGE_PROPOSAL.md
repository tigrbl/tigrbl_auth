> [!WARNING] Proposal only. `.ssot/` remains authoritative. This document proposes ADR work to close or normalize governance gaps. The target matrix is informative only and is not a normative design source.

# ADR Gap Coverage Proposal

## Purpose

This proposal turns the currently observed governance gaps into a small set of ADR candidates focused on real repository surfaces and boundary decisions.

Informative inputs:

- [target_cell_ssot_entity_matrix.json](./docs/compliance/target_cell_ssot_entity_matrix.json)
- [final_target_decision_matrix.json](./docs/compliance/final_target_decision_matrix.json)
- [TARGET_REALITY_MATRIX.md](./docs/compliance/TARGET_REALITY_MATRIX.md)

## Boundary Requirement

The proposal set shall explicitly include boundary ADRs for all four governed surfaces:

- admin UIX boundary
- public UIX boundary
- admin API boundary
- public API boundary

That requirement stands even where there is already partial or adjacent governance.

## Existing Relevant Coverage

The most relevant current ADRs already in the repo are:

- admin UIX:
  - `ADR-1038`
  - `ADR-1039`
  - `ADR-1040`
- public API:
  - `ADR-1006`
  - `ADR-1013`
  - `ADR-1041`
  - `ADR-1045`
- package / certification / boundary context:
  - `ADR-1001`
  - `ADR-1008`
  - `ADR-1016`
  - `ADR-1018`

Those are useful context, but the proposal still needs explicit boundary ADRs in the forward gap-closure set.

## Observed Gap Clusters

| Gap cluster | Current signal |
|---|---|
| Public UIX governance is missing as a first-class surface | `public_uix` is `none` for all tracked targets |
| API surface boundaries are not proposed explicitly in the current gap plan | public/admin API behavior exists, but the proposal set did not previously treat each as its own boundary ADR |
| Current reporting semantics conflate true gaps with intentional non-applicability | some report cells likely reflect scope boundaries rather than missing design |
| Transport protocol posture is uneven | `RFC 9112`, `RFC 9113`, `RFC 9114`, `RFC 9000` are sparse or absent across multiple surfaces |
| Supply chain / provenance governance is absent in the matrix | `NIST SP 800-218 SSDF`, `SLSA`, `in-toto`, `Sigstore`, `SPDX`, and `CycloneDX` are `none` across most cells |
| Tenant isolation and client policy are not normalized across surfaces | `Tenant Isolation Spec` and `Client Policy Spec` remain sparse outside admin UIX and adjacent API coverage |
| UIX-specific schema / JOSE handling is under-governed | `JSON Schema 2020-12`, `RFC 7515`, and `RFC 7516` have weak or absent UIX coverage |

## Proposed ADR Set

### Proposed `ADR-1054` Admin UIX Boundary

Current context:

- admin UIX already has meaningful governance in `ADR-1038`, `ADR-1039`, and `ADR-1040`

Problem:

- the forward proposal set should still include an explicit admin UIX boundary ADR so the surface is treated as a first-class boundary artifact rather than only a cluster of adjacent decisions

Proposed decision:

- define the admin UIX boundary explicitly
- state what is in scope:
  - shell
  - auth session gate
  - readiness/config
  - resource views
  - policy administration
  - safe mutations
- state what is out of scope:
  - backend-only internals
  - direct secret exposure
  - public end-user UX concerns

Primary governed surface addressed:

- admin UIX

### Proposed `ADR-1055` Public UIX Boundary

Problem:

- public end-user UIX is not currently governed as a first-class surface

Proposed decision:

- define the public UIX boundary explicitly
- establish scope for:
  - login
  - logout
  - registration
  - session continuation
  - consent / account-facing UX where applicable
  - recovery / challenge / public-facing identity UX where applicable
- separate public UIX from admin UIX and from backend-only API concerns

Primary governed surface addressed:

- public UIX

### Proposed `ADR-1056` Admin API Boundary

Problem:

- admin API behavior and contracts exist, but the proposal set should define the admin API boundary as its own governed surface

Proposed decision:

- define the admin API boundary explicitly
- state what is in scope:
  - OpenRPC-backed control-plane scope
  - authenticated and authorized admin actions
  - resource management
  - policy operations
  - operator-visible admin control-plane behavior
- state what is out of scope:
  - public auth routes
  - public browser UX
  - CLI-only concerns that are not part of the API boundary

Primary governed surface addressed:

- admin API

### Proposed `ADR-1057` Public API Boundary

Problem:

- public API behavior is governed through generated public contracts and profile artifacts, but the proposal set should define the public API boundary as its own surface

Proposed decision:

- define the public API boundary explicitly
- state what is in scope:
  - public OAuth/OIDC/discovery routes
  - public registration and logout surfaces where in scope
  - public metadata and discovery contracts
- state what is out of scope:
  - admin/control-plane operations
  - admin UIX concerns
  - CLI/operator-only flows

Primary governed surface addressed:

- public API

### Proposed `ADR-1058` Surface Applicability and Scope Classification

Problem:

- current reporting collapses "missing governance" and "intentionally not applicable" into the same symptom

Proposed decision:

- define a normative classification model for repository surfaces and targets:
  - in scope
  - out of scope
  - not applicable
  - planned
  - implemented
  - adjacent but non-authoritative
- require informative reports to project those normative classifications instead of ambiguous placeholders

Primary scope problems normalized:

- admin-only surfaces being shown as public gaps
- public-only surfaces being shown as admin gaps
- adjacent surfaces being misread as uncovered

### Proposed `ADR-1059` Public UIX Contract and Security Model

Problem:

- once public UIX exists as a first-class surface, the repo still needs a decision for how it consumes backend contracts and how browser security is governed

Proposed decision:

- public UIX consumes public HTTP/OpenAPI surfaces, not admin OpenRPC surfaces
- govern:
  - cookies
  - CSRF
  - redirect URI handling
  - same-site and origin model
  - browser-facing token handling
  - public error and problem-details rendering

Primary governed surface addressed:

- public UIX

### Proposed `ADR-1060` Transport Protocol Posture Across API and UIX

Problem:

- transport support is tracked unevenly across runtime, API, and UIX surfaces

Proposed decision:

- define support, exposure, and certification expectations for:
  - HTTP/1.1
  - HTTP/2
  - HTTP/3
  - QUIC
- separate:
  - backend/runtime support
  - operator/runtime enablement
  - browser/UIX dependence
  - certification claims

Primary governed surfaces addressed:

- runtime
- admin API
- public API
- admin UIX
- public UIX

### Proposed `ADR-1061` Supply Chain and Provenance Governance Boundary

Problem:

- supply-chain governance is not yet translated into explicit repo-level decisions even though it matters for certifiability and release posture

Proposed decision:

- govern how repo truth maps to:
  - `NIST SP 800-218 SSDF`
  - `SLSA`
  - `in-toto`
  - `Sigstore`
  - `SPDX`
  - `CycloneDX`
- decide which are:
  - certifiable release requirements
  - generated evidence/reporting artifacts
  - packaging metadata obligations
  - disclosure obligations

Primary governed surfaces addressed:

- release and build provenance
- package and artifact publication
- API/UIX disclosure only where relevant

### Proposed `ADR-1062` Tenant Isolation and Client Policy Plane Normalization

Problem:

- tenant isolation and client policy are not consistently governed across public/admin/API/UIX surfaces

Proposed decision:

- normalize how tenant scoping and client policy appear across:
  - admin control plane
  - public authorization plane
  - admin UIX
  - public UIX where tenant/client choices are user-visible

Primary governed surfaces addressed:

- admin API
- public API
- admin UIX
- selected public UIX surfaces

### Proposed `ADR-1063` UIX Data, Schema, and JOSE Disclosure Boundary

Problem:

- UIX surfaces still lack clear governance for how schema-driven or cryptographic artifacts are exposed, explained, or suppressed

Proposed decision:

- define UIX-facing handling for:
  - `JSON Schema 2020-12`
  - `RFC 7515 JWS`
  - `RFC 7516 JWE`
  - selected JWT/JWKS presentation and debugging surfaces
- separate:
  - operational admin views
  - end-user public views
  - hidden implementation details
  - safe redaction and explanation surfaces

Primary governed surfaces addressed:

- admin UIX
- public UIX

## Recommended Authoring Order

1. `ADR-1054` Admin UIX Boundary
2. `ADR-1055` Public UIX Boundary
3. `ADR-1056` Admin API Boundary
4. `ADR-1057` Public API Boundary
5. `ADR-1058` Surface Applicability and Scope Classification
6. `ADR-1059` Public UIX Contract and Security Model
7. `ADR-1060` Transport Protocol Posture Across API and UIX
8. `ADR-1061` Supply Chain and Provenance Governance Boundary
9. `ADR-1062` Tenant Isolation and Client Policy Plane Normalization
10. `ADR-1063` UIX Data, Schema, and JOSE Disclosure Boundary

## What This Proposal Does Not Recommend

- it does not recommend one ADR per RFC row
- it does not recommend filling every empty report entry with forced coverage
- it does not recommend treating informative report symptoms as normative design requirements

## Next Step

If you want this promoted into SSOT work, the next concrete move is:

1. reserve ADR numbers
2. author the four surface-boundary ADRs first
3. add companion SPEC proposals under each ADR
4. update informative reports so they project the normative scope model instead of ambiguous empty states
