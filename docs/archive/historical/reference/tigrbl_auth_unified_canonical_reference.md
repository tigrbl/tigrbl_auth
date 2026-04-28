> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# tigrbl_auth — Unified Canonical Markdown Reference
This document consolidates the available markdown artifacts for `tigrbl_auth` into one canonical reference. It preserves the revised certification tier model, brings forward unique material that only existed in the earlier matrix, deduplicates identical copies, and normalizes the project-tree, CLI, and usage content into a single architecture and compliance guide.
## Consolidation notes
- Canonical standards matrix source: `tigrbl_auth_standards_compliance_matrix_v2.md`
- Earlier matrix source: `tigrbl_auth_standards_compliance_matrix.md`; unique sections retained where they added coverage not present in the revised matrix
- Duplicate files deduplicated: `tigrbl_auth_project_tree_recommendation (1).md` and `tigrbl_auth_standards_compliance_matrix_v2 (1).md`
- Canonical architectural sources: `tigrbl_auth_project_tree_recommendation.md`, `tigrbl_auth_full_module_tree.md`, `tigrbl_auth_cli_flags.md`, and `tigrbl_auth_usage_examples.md`

## Table of contents
- [Standards and compliance](#standards-and-compliance)
- [Project tree layout](#project-tree-layout)
- [Exhaustive module tree](#exhaustive-module-tree)
- [Proposed CLI surface](#proposed-cli-surface)
- [Usage examples](#usage-examples)
- [Source handling appendix](#source-handling-appendix)

## Standards and compliance

### Provenance and scope

This document consolidates the standards, interoperability, and compliance target analysis discussed for `tigrbl_auth`.

Accessible repository surface did **not** expose a declared RFC or standards matrix. The only readable top-level package documentation visible during review was a title-only README:

> `# swarmauri-auth`

Accordingly, the matrices below represent the **recommended target boundary and implementation plan**, not a verified claim that the current package already satisfies these standards.

---

### Certification tier model (revised)

The previous version was missing an explicit tier for **independent peer claims**. That is a material gap because self-attested implementation maturity is not equivalent to externally reviewed conformance.

This revised model separates:
- implementation maturity,
- self-attested conformance,
- evidence-backed internal certification, and
- independent peer-reviewed claims.

| Tier | Name | Meaning |
|---|---|---|
| Tier 0 | Internal / Experimental | Prototype or private feature. No public conformance claim. |
| Tier 1 | Implemented | Feature exists and is usable, but no formal interoperability or conformance claim is made. |
| Tier 2 | Self-Asserted Interoperable | Team claims standards alignment and basic interop coverage through internal tests and docs. |
| Tier 3 | Evidence-Backed Certified | Preserved artifacts, conformance suites, negative tests, and release-gate evidence support the claim. |
| Tier 4 | Independent Peer Claim | Claim has external review, peer validation, independent interoperability confirmation, or equivalent third-party evidence. |

### Implementation model

| | Meaning |
|---|---|
| foundation-boundary | Foundation / boundary definition |
| baseline-interoperability | Interoperable baseline |
| production-readiness | Production completion |
| hardening-interop | Hardening / advanced interop |

---

### Consolidated standards / compliance matrix

| Feature | Target / Standard | Certification Tier | Implementation |
|---|---|---:|---:|
| HTTP auth framework semantics | RFC 9110 / HTTP Semantics; RFC 7235 legacy auth framework context | 2 | foundation-boundary |
| TLS-only auth transport boundary | TLS operational requirement across OAuth/OIDC endpoints | 2 | foundation-boundary |
| Authorization server core | RFC 6749 OAuth 2.0 Authorization Framework | 2 | baseline-interoperability |
| Bearer token usage | RFC 6750 Bearer Token Usage | 2 | baseline-interoperability |
| PKCE for public clients | RFC 7636 | 2 | baseline-interoperability |
| Authorization server metadata | RFC 8414 | 2 | baseline-interoperability |
| `.well-known` path conventions | RFC 5785 | 2 | baseline-interoperability |
| JWT token envelope | RFC 7519 JWT | 2 | baseline-interoperability |
| Signed token objects | RFC 7515 JWS | 2 | baseline-interoperability |
| Encrypted token objects | RFC 7516 JWE | 3 | production-readiness |
| JSON Web Keys | RFC 7517 JWK | 2 | baseline-interoperability |
| JOSE algorithm registry | RFC 7518 JWA | 2 | baseline-interoperability |
| JWT access token profile | RFC 9068 | 3 | production-readiness |
| Token revocation | RFC 7009 | 3 | production-readiness |
| Token introspection | RFC 7662 | 3 | production-readiness |
| Resource indicators / audience partitioning | RFC 8707 | 3 | production-readiness |
| Token exchange / delegation | RFC 8693 | 3 | hardening-interop |
| Device authorization flow | RFC 8628 | 3 | hardening-interop |
| Native app login profile | RFC 8252 | 3 | production-readiness |
| Dynamic client registration | RFC 7591 | 3 | production-readiness |
| Dynamic client registration management | RFC 7592 | 3 | hardening-interop |
| OAuth request object signing | RFC 9101 JAR | 3 | hardening-interop |
| Pushed authorization requests | RFC 9126 PAR | 3 | hardening-interop |
| Rich authorization requests | RFC 9396 RAR | 3 | hardening-interop |
| Sender-constrained tokens via mTLS | RFC 8705 | 4 | hardening-interop |
| Sender-constrained tokens via DPoP | RFC 9449 | 4 | hardening-interop |
| OAuth threat guidance baseline | RFC 6819 historical threat model guidance | 3 | production-readiness |
| OAuth modern hardening profile | OAuth 2.0 Security BCP alignment | 4 | hardening-interop |
| OIDC identity/authentication layer | OpenID Connect Core 1.0 | 2 | baseline-interoperability |
| OIDC discovery | OpenID Connect Discovery 1.0 | 2 | baseline-interoperability |
| OIDC userinfo | OpenID Connect Core 1.0 UserInfo surface | 3 | production-readiness |
| OIDC ID token validation | OIDC Core 1.0 | 2 | baseline-interoperability |
| OIDC session management | OpenID Connect Session Management 1.0 | 3 | production-readiness |
| OIDC RP-initiated logout | OpenID Connect RP-Initiated Logout 1.0 | 3 | production-readiness |
| OIDC front-channel logout | OpenID Connect Front-Channel Logout 1.0 | 4 | hardening-interop |
| OIDC back-channel logout | OpenID Connect Back-Channel Logout 1.0 | 4 | hardening-interop |
| Browser cookie sessions | RFC 6265 | 3 | production-readiness |
| Cookie security policy | RFC 6265 + Secure/HttpOnly/SameSite implementation policy | 3 | production-readiness |
| CSRF protection on browser auth flows | Web security hardening requirement, not a single RFC target here | 3 | production-readiness |
| State/nonce replay defense | OIDC Core + OAuth hardening profile | 3 | baseline-interoperability |
| Redirect URI strict validation | OAuth 2.0 / Security BCP / native app profile | 3 | baseline-interoperability |
| Refresh token rotation | Security BCP alignment | 4 | hardening-interop |
| Key rotation / JWKS rollover | JWK/JWS operational compliance | 3 | production-readiness |
| Issuer / audience / subject validation rules | JWT + OIDC validation profile | 3 | baseline-interoperability |
| Multi-tenant issuer partitioning | deployment/interoperability profile, not single RFC | 3 | production-readiness |
| Local account login | product feature; not standardized by one core RFC | 1 | production-readiness |
| End-user registration / signup | product feature; not standardized by one core RFC | 1 | production-readiness |
| Password-based local auth | implementation feature; standards-adjacent only | 1 | production-readiness |
| WebAuthn / passkeys | WebAuthn / FIDO2 family, outside RFC-only core set | 4 | hardening-interop |
| HTTP authorization endpoint | RFC 6749 / OIDC Core | 2 | baseline-interoperability |
| HTTP token endpoint | RFC 6749 / RFC 6750 / RFC 7636 | 2 | baseline-interoperability |
| HTTP revocation endpoint | RFC 7009 | 3 | production-readiness |
| HTTP introspection endpoint | RFC 7662 | 3 | production-readiness |
| HTTP JWKS endpoint | RFC 7517 / OIDC Discovery / RFC 8414 metadata linkage | 2 | baseline-interoperability |
| HTTP metadata endpoint | RFC 8414 | 2 | baseline-interoperability |
| OIDC discovery endpoint | OIDC Discovery 1.0 | 2 | baseline-interoperability |
| OIDC userinfo endpoint | OIDC Core 1.0 | 3 | production-readiness |
| OIDC logout endpoint | OIDC logout specs | 3 | production-readiness |
| Device authorization endpoint | RFC 8628 | 3 | hardening-interop |
| Client registration endpoint | RFC 7591 / 7592 | 3 | production-readiness |
| Access token validation for resource servers | RFC 6750 / RFC 7662 / RFC 9068 | 3 | production-readiness |
| Scope semantics | RFC 6749 / application profile | 2 | baseline-interoperability |
| Claims-based authorization | JWT / OIDC / application policy layer | 3 | production-readiness |
| RBAC / ABAC / ReBAC policy engine | product/policy feature, not governed by a single core RFC | 1 | production-readiness |
| OpenAPI HTTP contract | OpenAPI 3.1 | 2 | baseline-interoperability |
| OpenAPI bearer security scheme | OpenAPI 3.1 `http` bearer scheme | 2 | baseline-interoperability |
| OpenAPI OAuth2 scheme declaration | OpenAPI 3.1 `oauth2` security scheme | 2 | baseline-interoperability |
| OpenAPI OpenID Connect scheme | OpenAPI 3.1 `openIdConnect` security scheme | 2 | baseline-interoperability |
| OpenAPI standard error schemas | OpenAPI 3.1 implementation target for OAuth/OIDC errors | 3 | production-readiness |
| OpenAPI callback / redirect documentation | OpenAPI 3.1 documentation target | 3 | production-readiness |
| OpenRPC control-plane surface | OpenRPC 1.x for internal/admin RPC only | 2 | production-readiness |
| OpenRPC token/session admin methods | OpenRPC internal control-plane documentation target | 2 | production-readiness |
| OAuth/OIDC over JSON-RPC | Not a normative interop target; should not be claimed as standards-equivalent | 0 | foundation-boundary |
| JSON-RPC auth for internal admin | JSON-RPC / OpenRPC internal feature only | 2 | production-readiness |
| Audit event logging | production hardening / compliance feature | 3 | production-readiness |
| Security event logging | production hardening / compliance feature | 4 | hardening-interop |
| Deterministic config / metadata emission | production interop / operability target | 3 | production-readiness |
| Conformance / interoperability test suite | certification evidence requirement | 3 | hardening-interop |
| RFC-targeted negative tests | certification evidence requirement | 3 | hardening-interop |
| Cryptographic algorithm allowlists | JOSE hardening / Security BCP alignment | 4 | hardening-interop |
| Algorithm confusion resistance | JOSE hardening | 4 | hardening-interop |
| Clock skew tolerance rules | JWT/OIDC operational profile | 3 | production-readiness |
| Tenant-scoped key material isolation | production hardening target | 4 | hardening-interop |
| Back-channel service-to-service interop | OAuth token exchange / mTLS / JWT profiles | 4 | hardening-interop |
| CLI login interop | RFC 8628 device flow | 3 | hardening-interop |
| SPA login interop | OIDC Core + Auth Code + PKCE + Security BCP direction | 3 | production-readiness |
| Confidential web app interop | OAuth 2.0 + OIDC Core + cookie/session profile | 3 | production-readiness |
| Resource server interop | RFC 6750 + RFC 7662 and/or RFC 9068 | 3 | production-readiness |
| Gateway / proxy interop | metadata/JWKS/introspection/revocation exposure | 3 | production-readiness |
| OAuth 2.1 alignment | draft-era profile direction: PKCE-by-default, no implicit, hardened redirects | 3 | production-readiness |
| OAuth 2.1 formal RFC claim | Do not claim unless a final RFC is verified | 0 | foundation-boundary |

---

### Claim discipline for independent peer claims

A feature should not be placed in **Tier 4** merely because it is difficult or security-sensitive. Tier 4 should be reserved for features whose claim is supported by one or more of the following:

| Evidence class | Examples |
|---|---|
| Independent interoperability validation | Interop testing against third-party IdPs, RPs, gateways, SDKs, or resource servers |
| External conformance review | Independent protocol review, peer-reviewed implementation assessment, or recognized external audit |
| Reproducible public evidence | Public fixtures, wire captures, preserved artifacts, independently repeatable conformance cases |
| Cross-implementation verification | Same feature validated against multiple independent stacks |

#### Practical interpretation

| Tier | Claim posture |
|---|---|
| Tier 1 | “Implemented.” |
| Tier 2 | “We assert standards alignment.” |
| Tier 3 | “We have preserved evidence and internal certification artifacts.” |
| Tier 4 | “The claim has independent peer or third-party support.” |

---

### Recommended implementation ordering

| | Objective | Core targets |
|---|---|---|
| foundation-boundary | Foundation / boundary definition | HTTP semantics, TLS-only boundary, accurate standards claims, no false OpenRPC-over-OAuth claim |
| baseline-interoperability | Minimum interoperable identity server | RFC 6749, RFC 6750, RFC 7636, RFC 8414, RFC 7515/7517/7518/7519, OIDC Core, OIDC Discovery, authorization/token/JWKS/metadata |
| production-readiness | Production-grade auth platform | RFC 7009, RFC 7662, RFC 9068, RFC 7591, RFC 6265, OIDC userinfo/session/logout, OpenAPI 3.1 complete contract, RFC 8252 |
| hardening-interop | Hardened / enterprise | RFC 8705 or RFC 9449, RFC 8693, RFC 8628, RFC 9101, RFC 9126, RFC 9396, RFC 7592, front/back-channel logout, conformance evidence, independent interop validation preparation |

---

### Minimal certifiable claim set

| Feature cluster | Targets | Minimum tier |
|---|---|---:|
| OAuth core | RFC 6749, RFC 6750 | 2 |
| Modern login | RFC 7636, RFC 8414, OIDC Core, OIDC Discovery | 2 |
| Token format | RFC 7515, RFC 7517, RFC 7518, RFC 7519 | 2 |
| Required endpoints | Authorization, token, metadata, discovery, JWKS | 2 |
| API documentation | OpenAPI 3.1 with bearer / oauth2 / openIdConnect schemes | 2 |
| Internal certification evidence | Conformance tests, preserved artifacts, negative cases | 3 |
| Independent peer claim | External interop validation and peer-reviewed evidence | 4 |

---

### Critical missing targets to treat as non-optional after baseline

| Feature | Missing target / requirement | Recommended target tier |
|---|---|---:|
| Token lifecycle | RFC 7009, RFC 7662 | 3 |
| Browser sessions | RFC 6265 + OIDC session/logout specs | 3 |
| JWT access-token interoperability | RFC 9068 | 3 |
| Client ecosystem | RFC 7591 | 3 |
| Hardening | OAuth 2.0 Security BCP alignment | 4 |
| Sender-constrained tokens | RFC 9449 or RFC 8705 | 4 |
| Hardened authorization request channel | RFC 9126, RFC 9101 | 4 |
| Enterprise delegation | RFC 8693 | 4 |
| CLI/device login | RFC 8628 | 3 |
| Independent claimability | third-party interop validation and peer evidence | 4 |

---

### Summary

A credible `tigrbl_auth` standards boundary should be built in layers:

1. **Implemented foundation**: accurate protocol boundary, endpoint surface, and no overstated claims.
2. **Self-asserted interoperability**: OAuth 2.0 core, bearer, PKCE, discovery/metadata, JOSE/JWT, OIDC Core.
3. **Evidence-backed certification**: revocation, introspection, JWT access-token profile, browser sessions, logout, client registration, OpenAPI 3.1 completeness, negative and preserved conformance artifacts.
4. **Independent peer claims**: sender-constrained tokens, hardening profiles, cross-stack interop, externally reviewable and reproducible evidence.

### Additional standards breakdown retained from the earlier matrix

### Functional standards breakdown by concern

#### Authentication (AuthN)

| Feature cluster | Primary targets |
|---|---|
| Core login / identity | OpenID Connect Core 1.0 |
| Authorization framework substrate | RFC 6749, RFC 6750 |
| Token format and validation | RFC 7515, RFC 7517, RFC 7518, RFC 7519 |
| Discovery / machine-readable metadata | RFC 8414, OIDC Discovery 1.0, RFC 5785 |
| Public client hardening | RFC 7636 |
| Native app login | RFC 8252 |
| Proof-of-possession hardening | RFC 8705, RFC 9449 |

#### Authorization (AuthZ)

| Feature cluster | Primary targets |
|---|---|
| Delegated authorization core | RFC 6749 |
| Protected resource access | RFC 6750 |
| Token validation | RFC 7662, RFC 9068 |
| Resource targeting | RFC 8707 |
| Delegation / impersonation / exchange | RFC 8693 |
| Rich authorization semantics | RFC 9396 |

#### Registration

| Feature cluster | Primary targets |
|---|---|
| Dynamic client registration | RFC 7591 |
| Client registration management | RFC 7592 |
| End-user signup | Product-specific, not governed by one core RFC |

#### Login / sessions / logout

| Feature cluster | Primary targets |
|---|---|
| Browser / federated login | OIDC Core 1.0 |
| Session cookies | RFC 6265 |
| Session management | OIDC Session Management 1.0 |
| RP logout | OIDC RP-Initiated Logout 1.0 |
| Front-channel logout | OIDC Front-Channel Logout 1.0 |
| Back-channel logout | OIDC Back-Channel Logout 1.0 |
| Token revocation | RFC 7009 |

#### Well-knowns and discovery

| Feature cluster | Primary targets |
|---|---|
| Well-known path conventions | RFC 5785 |
| OAuth metadata endpoint | RFC 8414 |
| OIDC discovery endpoint | OpenID Connect Discovery 1.0 |
| JWKS publication | RFC 7517 + metadata/discovery linkage |

---

### OpenAPI targets

| Feature | Target / requirement | Tier | |
|---|---|---:|---:|
| HTTP API contract | OpenAPI 3.1 | 2 | baseline-interoperability |
| Bearer auth scheme | OpenAPI 3.1 `http` bearer | 2 | baseline-interoperability |
| OAuth flow docs | OpenAPI 3.1 `oauth2` scheme | 2 | baseline-interoperability |
| OIDC discovery binding | OpenAPI 3.1 `openIdConnect` scheme | 2 | baseline-interoperability |
| Standardized error schemas | OAuth/OIDC error modeling in OpenAPI | 2 | production-readiness |
| Redirect / callback docs | Explicit documentation of redirect semantics | 2 | production-readiness |
| Full endpoint contract coverage | Authorization, token, introspection, revocation, userinfo, JWKS, metadata, logout, registration, device flow | 2 | production-readiness |

---

### OpenRPC targets

| Feature | Target / requirement | Tier | |
|---|---|---:|---:|
| Internal admin/control-plane RPC documentation | OpenRPC 1.x | 1 | production-readiness |
| Token/session/admin methods over RPC | OpenRPC internal surface only | 1 | production-readiness |
| OAuth/OIDC interoperability over JSON-RPC | Not a normative target; should not be claimed | 0 | foundation-boundary |

---

### Recommended claim language discipline

| Claim area | Guidance |
|---|---|
| OAuth 2.1 | Align to OAuth 2.1 direction operationally, but do not claim a final RFC unless verified |
| OpenRPC | Use only for internal/admin/control-plane methods, not as a replacement for OAuth/OIDC HTTP interop |
| Registration | Distinguish client registration standards from end-user signup |
| Sessions | Distinguish browser cookie sessions from OAuth token semantics |
| AuthZ policy | Do not imply that RBAC/ABAC/ReBAC are standardized by one of the OAuth/OIDC RFCs |

---

## Project tree layout

### Decision

Build `tigrbl_auth` as a **standards package under the Tigrbl/Swarmauri monorepo** with a **Tigrbl-native shape**:

- keep the package under `pkgs/standards/tigrbl_auth/`
- keep the Python import root as `tigrbl_auth/` (no `src/` split)
- model runtime code around **`api` / `tables` / `ops` / `plugin` / `gateway`**
- separate **normative standards claims** from **optional extensions**
- add **ADRs**, **machine-readable compliance targets**, **release gates**, and **evidence bundles**
- keep GitHub workflows at the **monorepo root**, while storing package-local gate manifests under `compliance/gates/`

This layout is designed to support:

1. strict Tigrbl framework alignment,
2. certifiable RFC claim discipline,
3. OpenAPI / OpenRPC contract generation,
4. reproducible release gating,
5. independent peer-review evidence.

---

### Recommended tree

```text
pkgs/standards/tigrbl_auth/
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── LICENSE
├── .env.example
├── examples/
│   ├── standalone_app.py
│   ├── install_plugin.py
│   ├── oauth_authorization_code_pkce.py
│   ├── device_flow.py
│   └── service_to_service_token_exchange.py
├── scripts/
│   ├── generate_openapi.py
│   ├── generate_openrpc.py
│   ├── build_evidence_bundle.py
│   ├── verify_release_gates.py
│   ├── verify_claims.py
│   └── validate_well_known.py
├── specs/
│   ├── openapi/
│   │   ├── openapi.json
│   │   ├── openapi.yaml
│   │   └── overlays/
│   └── openrpc/
│       └── openrpc.json
├── docs/
│   ├── adr/
│   │   ├── 0001-use-adrs.md
│   │   ├── 0002-package-boundary.md
│   │   ├── 0003-claim-discipline.md
│   │   ├── 0004-standards-target-boundary.md
│   │   ├── 0005-tigrbl-surface-shape.md
│   │   ├── 0006-release-gates.md
│   │   └── template.md
│   ├── standards/
│   │   ├── targets.md
│   │   ├── oauth2.md
│   │   ├── oidc.md
│   │   ├── jose.md
│   │   ├── openapi.md
│   │   ├── openrpc.md
│   │   └── well_known.md
│   ├── compliance/
│   │   ├── target-matrix.md
│   │   ├── claim-tiers.md
│   │   ├── release-gates.md
│   │   ├── evidence-policy.md
│   │   ├── peer-claim-policy.md
│   │   └── threat-model.md
│   ├── runbooks/
│   │   ├── key-rotation.md
│   │   ├── incident-response.md
│   │   ├── release.md
│   │   └── interoperability.md
│   └── diagrams/
├── compliance/
│   ├── targets/
│   │   ├── rfc-targets.yaml
│   │   ├── oidc-targets.yaml
│   │   ├── openapi-targets.yaml
│   │   ├── openrpc-targets.yaml
│   │   └── profiles.yaml
│   ├── gates/
│   │   ├── gate-00-structure.yaml
│   │   ├── gate-10-unit.yaml
│   │   ├── gate-20-conformance.yaml
│   │   ├── gate-30-interop.yaml
│   │   ├── gate-40-security.yaml
│   │   ├── gate-50-specs.yaml
│   │   ├── gate-60-evidence.yaml
│   │   └── gate-70-release.yaml
│   ├── claims/
│   │   ├── self-asserted.yaml
│   │   ├── certified.yaml
│   │   └── peer-reviewed.yaml
│   ├── evidence/
│   │   ├── internal/
│   │   ├── peer/
│   │   ├── attestations/
│   │   ├── reports/
│   │   └── sbom/
│   └── waivers/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── conformance/
│   │   ├── oauth2/
│   │   │   ├── rfc6749/
│   │   │   ├── rfc6750/
│   │   │   ├── rfc7009/
│   │   │   ├── rfc7591/
│   │   │   ├── rfc7592/
│   │   │   ├── rfc7636/
│   │   │   ├── rfc7662/
│   │   │   ├── rfc8252/
│   │   │   ├── rfc8414/
│   │   │   ├── rfc8628/
│   │   │   ├── rfc8693/
│   │   │   ├── rfc8705/
│   │   │   ├── rfc8707/
│   │   │   ├── rfc9068/
│   │   │   ├── rfc9101/
│   │   │   ├── rfc9126/
│   │   │   ├── rfc9207/
│   │   │   ├── rfc9396/
│   │   │   └── rfc9449/
│   │   ├── jose/
│   │   │   ├── rfc7515/
│   │   │   ├── rfc7516/
│   │   │   ├── rfc7517/
│   │   │   ├── rfc7518/
│   │   │   ├── rfc7519/
│   │   │   ├── rfc7638/
│   │   │   ├── rfc7800/
│   │   │   ├── rfc8037/
│   │   │   └── rfc8725/
│   │   ├── oidc/
│   │   │   ├── core/
│   │   │   ├── discovery/
│   │   │   ├── session/
│   │   │   └── logout/
│   │   └── http/
│   │       ├── rfc5785/
│   │       └── rfc6265/
│   ├── interop/
│   │   ├── keycloak/
│   │   ├── okta/
│   │   ├── azure/
│   │   ├── generic_oidc_rp/
│   │   └── generic_resource_server/
│   ├── negative/
│   ├── e2e/
│   ├── perf/
│   ├── security/
│   └── fixtures/
└── tigrbl_auth/
    ├── __init__.py
    ├── plugin.py
    ├── gateway.py
    ├── api/
    │   ├── __init__.py
    │   ├── app.py
    │   ├── surfaces.py
    │   ├── rest/
    │   │   ├── __init__.py
    │   │   ├── deps/
    │   │   ├── schemas/
    │   │   ├── errors.py
    │   │   └── routers/
    │   │       ├── authorize.py
    │   │       ├── token.py
    │   │       ├── revocation.py
    │   │       ├── introspection.py
    │   │       ├── registration.py
    │   │       ├── userinfo.py
    │   │       ├── jwks.py
    │   │       ├── discovery.py
    │   │       ├── logout.py
    │   │       ├── device.py
    │   │       ├── par.py
    │   │       └── token_exchange.py
    │   └── rpc/
    │       ├── __init__.py
    │       ├── schemas/
    │       └── methods/
    │           ├── discovery.py
    │           ├── tenants.py
    │           ├── users.py
    │           ├── clients.py
    │           ├── sessions.py
    │           └── keys.py
    ├── tables/
    │   ├── __init__.py
    │   ├── tenant.py
    │   ├── user.py
    │   ├── client.py
    │   ├── auth_session.py
    │   ├── auth_code.py
    │   ├── device_code.py
    │   ├── pushed_authorization_request.py
    │   ├── revoked_token.py
    │   ├── service.py
    │   ├── service_key.py
    │   └── api_key.py
    ├── ops/
    │   ├── __init__.py
    │   ├── authenticate.py
    │   ├── authorize.py
    │   ├── token.py
    │   ├── register_client.py
    │   ├── manage_client.py
    │   ├── introspect_token.py
    │   ├── revoke_token.py
    │   ├── exchange_token.py
    │   ├── issue_access_token.py
    │   ├── issue_id_token.py
    │   ├── userinfo.py
    │   ├── login.py
    │   ├── logout.py
    │   └── sessions.py
    ├── services/
    │   ├── __init__.py
    │   ├── key_management.py
    │   ├── token_service.py
    │   ├── cookie_service.py
    │   ├── nonce_service.py
    │   ├── consent_service.py
    │   ├── replay_protection.py
    │   ├── capability_matrix.py
    │   └── evidence_bundle.py
    ├── standards/
    │   ├── __init__.py
    │   ├── jose/
    │   │   ├── jws.py
    │   │   ├── jwe.py
    │   │   ├── jwk.py
    │   │   ├── jwa.py
    │   │   ├── jwt.py
    │   │   ├── thumbprint.py
    │   │   └── bcp8725.py
    │   ├── oauth2/
    │   │   ├── core.py
    │   │   ├── bearer.py
    │   │   ├── revocation.py
    │   │   ├── introspection.py
    │   │   ├── pkce.py
    │   │   ├── dynamic_registration.py
    │   │   ├── client_mgmt.py
    │   │   ├── native_apps.py
    │   │   ├── metadata.py
    │   │   ├── jwt_access_tokens.py
    │   │   ├── jar.py
    │   │   ├── par.py
    │   │   ├── issuer_id.py
    │   │   ├── rar.py
    │   │   ├── dpop.py
    │   │   ├── mtls.py
    │   │   ├── resource_indicators.py
    │   │   ├── token_exchange.py
    │   │   ├── device_authorization.py
    │   │   └── profiles/
    │   │       └── oauth2_1_alignment.py
    │   ├── oidc/
    │   │   ├── core.py
    │   │   ├── discovery.py
    │   │   ├── id_token.py
    │   │   ├── userinfo.py
    │   │   ├── session_mgmt.py
    │   │   ├── rp_initiated_logout.py
    │   │   ├── frontchannel_logout.py
    │   │   ├── backchannel_logout.py
    │   │   └── amr.py
    │   └── http/
    │       ├── well_known.py
    │       ├── cookies.py
    │       └── tls.py
    ├── extensions/
    │   ├── __init__.py
    │   ├── webauthn/
    │   ├── webpush/
    │   ├── security_event_tokens/
    │   └── experimental/
    ├── security/
    │   ├── __init__.py
    │   ├── deps.py
    │   ├── csrf.py
    │   ├── headers.py
    │   ├── session_policy.py
    │   ├── algorithm_policy.py
    │   ├── key_rotation.py
    │   ├── proof_of_possession.py
    │   └── validators.py
    ├── config/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── feature_flags.py
    │   ├── claim_matrix.py
    │   └── release_profile.py
    ├── adapters/
    │   ├── __init__.py
    │   ├── local.py
    │   ├── remote.py
    │   ├── jwks_remote.py
    │   └── context.py
    ├── schemas/
    │   ├── json/
    │   └── examples/
    └── migrations/
        ├── env.py
        └── versions/
```

---

### Required structural rules

#### 1. Monorepo rule

Keep package-local code in `pkgs/standards/tigrbl_auth/`, but keep CI workflows at the repository root.

Package-local compliance policy belongs under:

- `compliance/gates/`
- `compliance/targets/`
- `compliance/claims/`

Root workflows should load those manifests and enforce them.

#### 2. Tigrbl-native module rule

Use Tigrbl-oriented names:

- `tables/` instead of `orm/`
- `api/` instead of generic `routers/`
- `ops/` for operation logic
- `plugin.py` for installation into an existing `TigrblApp`
- `gateway.py` or `api/app.py` for standalone app assembly

#### 3. Claim-discipline rule

Do **not** keep all RFC code under one flat `rfc/` directory.

Split into:

- `standards/` for **claimed normative targets**
- `extensions/` for adjacent or optional features that are not part of the default certification boundary

#### 4. No vendor shim rule

Delete the package-local `vendor/` re-export layer.

Import directly from:

- `tigrbl`
- `fastapi`
- `pydantic`
- `sqlalchemy`
- first-party Swarmauri packages

This reduces indirection, improves auditability, and makes standards tracing easier.

#### 5. Evidence-first rule

Every standards claim must map to:

- a target manifest in `compliance/targets/`
- tests in `tests/conformance/`
- evidence in `compliance/evidence/`
- a release gate in `compliance/gates/`

---

### Current → target mapping

| Current | Target |
|---|---|
| `tigrbl_auth/orm/*` | `tigrbl_auth/tables/*` |
| `tigrbl_auth/routers/*` | `tigrbl_auth/api/rest/*` and `tigrbl_auth/api/rpc/*` |
| `tigrbl_auth/backends.py` | `tigrbl_auth/ops/authenticate.py` + `tigrbl_auth/security/deps.py` |
| `tigrbl_auth/app.py` | `tigrbl_auth/api/app.py` + `tigrbl_auth/gateway.py` |
| `tigrbl_auth/rfc/*` | `tigrbl_auth/standards/{oauth2,oidc,jose,http}/*` |
| out-of-scope or optional RFC helpers | `tigrbl_auth/extensions/*` |
| `tigrbl_auth/runtime_cfg.py` | `tigrbl_auth/config/settings.py` |
| `tigrbl_auth/vendor/*` | **delete** |
| flat `tests/unit/test_rfc*.py` | `tests/conformance/<domain>/<rfc>/...` |
| no ADRs | `docs/adr/*` |
| no machine-readable claim manifests | `compliance/targets/*.yaml`, `compliance/claims/*.yaml` |
| no package-local gate manifests | `compliance/gates/*.yaml` |

---

### Release gates to implement

#### Gate 00 — structure
- package path correct under `pkgs/standards/`
- no `vendor/` shim
- ADR index present
- target manifests present
- generated specs build cleanly

#### Gate 10 — quality
- formatting, lint, type checks
- import graph checks
- unit tests pass
- migration drift check passes

#### Gate 20 — conformance
- every claimed RFC target has tests
- negative tests exist for every security-sensitive RFC target
- well-known endpoints and metadata validate

#### Gate 30 — interoperability
- interop suites pass against at least one generic RP and one generic RS
- Tier 4 claims require independent peer evidence material

#### Gate 40 — security
- JWT BCP checks
- algorithm allowlist checks
- key rotation simulation
- replay protection tests
- SBOM + dependency scan + secret scan

#### Gate 50 — contract
- OpenAPI artifact generated and validated
- OpenRPC artifact generated and validated
- REST and RPC discovery documents match runtime surface

#### Gate 60 — evidence
- evidence bundle assembled
- claim matrix synchronized with tests
- waivers reviewed
- certification artifact retained

#### Gate 70 — release
- changelog updated
- semver policy satisfied
- attestations generated
- package publish allowed

---

### First ADRs to write

1. **ADR-0001** — adopt ADRs and numbering scheme
2. **ADR-0002** — define certification boundary and claimed standards scope
3. **ADR-0003** — adopt Tigrbl-native package shape (`api/tables/ops/plugin`)
4. **ADR-0004** — remove vendor shim and use direct imports
5. **ADR-0005** — separate standards from extensions
6. **ADR-0006** — release gate policy and evidence retention model
7. **ADR-0007** — OpenAPI / OpenRPC generation strategy
8. **ADR-0008** — peer-claim evidence policy for Tier 4 claims

---

### Non-negotiable implementation choices

- **Keep** the package import root as `tigrbl_auth/`.
- **Rename** `orm/` to `tables/`.
- **Replace** flat `rfc/` with domain-grouped `standards/`.
- **Move** non-core or optional standards under `extensions/`.
- **Delete** `vendor/`.
- **Add** `plugin.py` and `gateway.py`.
- **Generate** OpenAPI and OpenRPC into `specs/`.
- **Add** `docs/adr/` and `compliance/` immediately.
- **Convert** RFC tests into domain-scoped conformance suites.
- **Treat release gates as code**, not prose.

---

### Bottom line

The correct target is **not** a slightly cleaner version of the current flat package.

The correct target is a **Tigrbl-native, evidence-first, standards-scoped package** whose runtime tree matches Tigrbl conventions and whose certification surface is explicit, testable, and gateable.

## Exhaustive module tree

This is the **target** tree for the new `tigrbl_auth` package, derived from:

- the revised standards/compliance matrix,
- the requirement to stay strictly Tigrbl-native,
- the requirement to adopt ADRs,
- the requirement to codify release gates,
- the current uploaded package state.

The target intentionally **removes** these current-package shapes from the certification boundary:

- `tigrbl_auth/vendor/`
- flat `tigrbl_auth/rfc/`
- flat `tigrbl_auth/routers/`
- flat runtime modules such as `backends.py`, `runtime_cfg.py`, `security.deps.py`, `db.py`

Their responsibilities are redistributed into `api/`, `tables/`, `ops/`, `services/`, `security/`, `config/`, and `standards/`.

```text
pkgs/standards/tigrbl_auth/
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── LICENSE
├── .env.example
├── examples/
│   ├── standalone_app.py
│   ├── install_plugin.py
│   ├── oauth_authorization_code_pkce.py
│   ├── oauth_client_credentials.py
│   ├── oidc_rp_login.py
│   ├── device_flow.py
│   ├── token_exchange.py
│   └── service_to_service_token_exchange.py
├── scripts/
│   ├── generate_openapi.py
│   ├── generate_openrpc.py
│   ├── run_conformance.py
│   ├── validate_well_known.py
│   ├── verify_claims.py
│   ├── verify_release_gates.py
│   └── build_evidence_bundle.py
├── specs/
│   ├── openapi/
│   │   ├── openapi.yaml
│   │   ├── openapi.json
│   │   └── overlays/
│   │       ├── auth-core.yaml
│   │       ├── oidc.yaml
│   │       └── admin-control-plane.yaml
│   └── openrpc/
│       └── openrpc.json
├── docs/
│   ├── adr/
│   │   ├── README.md
│   │   ├── template.md
│   │   ├── 0001-use-adrs.md
│   │   ├── 0002-certification-boundary.md
│   │   ├── 0003-tigrbl-native-package-shape.md
│   │   ├── 0004-remove-vendor-shims.md
│   │   ├── 0005-separate-standards-from-extensions.md
│   │   ├── 0006-release-gates-as-code.md
│   │   ├── 0007-openapi-openrpc-generation.md
│   │   ├── 0008-evidence-retention-policy.md
│   │   └── 0009-peer-claim-policy.md
│   ├── standards/
│   │   ├── targets.md
│   │   ├── oauth2.md
│   │   ├── oidc.md
│   │   ├── jose.md
│   │   ├── http.md
│   │   ├── openapi.md
│   │   ├── openrpc.md
│   │   └── well_known.md
│   ├── compliance/
│   │   ├── target-matrix.md
│   │   ├── claim-tiers.md
│   │   ├── release-gates.md
│   │   ├── evidence-policy.md
│   │   ├── peer-claim-policy.md
│   │   └── threat-model.md
│   ├── runbooks/
│   │   ├── key-rotation.md
│   │   ├── incident-response.md
│   │   ├── release.md
│   │   └── interoperability.md
│   └── diagrams/
│       ├── auth-surface-context.md
│       ├── token-lifecycle.md
│       ├── browser-session-flow.md
│       └── service-to-service-flow.md
├── compliance/
│   ├── targets/
│   │   ├── rfc-targets.yaml
│   │   ├── oidc-targets.yaml
│   │   ├── openapi-targets.yaml
│   │   ├── openrpc-targets.yaml
│   │   ├── endpoint-targets.yaml
│   │   └── profiles.yaml
│   ├── gates/
│   │   ├── gate-00-structure.yaml
│   │   ├── gate-10-format-lint-types.yaml
│   │   ├── gate-20-unit.yaml
│   │   ├── gate-30-integration.yaml
│   │   ├── gate-40-conformance.yaml
│   │   ├── gate-50-interop.yaml
│   │   ├── gate-60-security.yaml
│   │   ├── gate-70-contracts.yaml
│   │   ├── gate-80-evidence.yaml
│   │   └── gate-90-release.yaml
│   ├── claims/
│   │   ├── tier-1-implemented.yaml
│   │   ├── tier-2-self-asserted.yaml
│   │   ├── tier-3-evidence-backed.yaml
│   │   └── tier-4-peer-reviewed.yaml
│   ├── evidence/
│   │   ├── internal/
│   │   │   └── README.md
│   │   ├── peer/
│   │   │   └── README.md
│   │   ├── attestations/
│   │   │   └── README.md
│   │   ├── reports/
│   │   │   └── README.md
│   │   └── sbom/
│   │       └── README.md
│   └── waivers/
│       └── README.md
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── jwks/
│   │   │   ├── rsa_public_jwks.json
│   │   │   ├── ec_public_jwks.json
│   │   │   └── okp_public_jwks.json
│   │   ├── clients/
│   │   │   ├── public_client.json
│   │   │   ├── confidential_client.json
│   │   │   └── mtls_client.json
│   │   └── tenants/
│   │       ├── single_tenant.json
│   │       └── multi_tenant.json
│   ├── unit/
│   │   ├── test_plugin.py
│   │   ├── test_gateway.py
│   │   ├── test_settings.py
│   │   ├── test_feature_flags.py
│   │   ├── test_claim_matrix.py
│   │   ├── test_adapters.py
│   │   ├── test_tables.py
│   │   ├── test_key_management.py
│   │   ├── test_token_service.py
│   │   ├── test_session_service.py
│   │   ├── test_cookie_service.py
│   │   ├── test_nonce_service.py
│   │   ├── test_consent_service.py
│   │   ├── test_algorithm_policy.py
│   │   ├── test_session_policy.py
│   │   ├── test_security_deps.py
│   │   └── test_release_profile.py
│   ├── integration/
│   │   ├── test_rest_surface.py
│   │   ├── test_rpc_surface.py
│   │   ├── test_migrations.py
│   │   ├── test_openapi_generation.py
│   │   ├── test_openrpc_generation.py
│   │   └── test_plugin_installation.py
│   ├── conformance/
│   │   ├── oauth2/
│   │   │   ├── rfc6749/
│   │   │   │   ├── test_authorize.py
│   │   │   │   ├── test_token.py
│   │   │   │   ├── test_errors.py
│   │   │   │   └── test_grants.py
│   │   │   ├── rfc6750/
│   │   │   │   └── test_bearer_usage.py
│   │   │   ├── rfc7009/
│   │   │   │   └── test_revocation_endpoint.py
│   │   │   ├── rfc7591/
│   │   │   │   └── test_dynamic_client_registration.py
│   │   │   ├── rfc7592/
│   │   │   │   └── test_client_management.py
│   │   │   ├── rfc7636/
│   │   │   │   └── test_pkce.py
│   │   │   ├── rfc7662/
│   │   │   │   └── test_introspection.py
│   │   │   ├── rfc8252/
│   │   │   │   └── test_native_apps.py
│   │   │   ├── rfc8414/
│   │   │   │   └── test_authorization_server_metadata.py
│   │   │   ├── rfc8628/
│   │   │   │   └── test_device_authorization.py
│   │   │   ├── rfc8693/
│   │   │   │   └── test_token_exchange.py
│   │   │   ├── rfc8705/
│   │   │   │   └── test_mtls_sender_constrained_tokens.py
│   │   │   ├── rfc8707/
│   │   │   │   └── test_resource_indicators.py
│   │   │   ├── rfc9068/
│   │   │   │   └── test_jwt_access_token_profile.py
│   │   │   ├── rfc9101/
│   │   │   │   └── test_jar.py
│   │   │   ├── rfc9126/
│   │   │   │   └── test_par.py
│   │   │   ├── rfc9207/
│   │   │   │   └── test_issuer_identifier.py
│   │   │   ├── rfc9396/
│   │   │   │   └── test_rar.py
│   │   │   └── rfc9449/
│   │   │       └── test_dpop.py
│   │   ├── jose/
│   │   │   ├── rfc7515/
│   │   │   │   └── test_jws.py
│   │   │   ├── rfc7516/
│   │   │   │   └── test_jwe.py
│   │   │   ├── rfc7517/
│   │   │   │   └── test_jwk.py
│   │   │   ├── rfc7518/
│   │   │   │   └── test_jwa.py
│   │   │   ├── rfc7519/
│   │   │   │   └── test_jwt.py
│   │   │   ├── rfc7638/
│   │   │   │   └── test_jwk_thumbprint.py
│   │   │   ├── rfc7800/
│   │   │   │   └── test_proof_of_possession.py
│   │   │   ├── rfc8037/
│   │   │   │   └── test_okp_and_eddsa.py
│   │   │   └── rfc8725/
│   │   │       └── test_jwt_bcp.py
│   │   ├── oidc/
│   │   │   ├── core/
│   │   │   │   ├── test_authorize.py
│   │   │   │   ├── test_id_token.py
│   │   │   │   └── test_nonce_and_amr.py
│   │   │   ├── discovery/
│   │   │   │   ├── test_openid_configuration.py
│   │   │   │   └── test_jwks_uri.py
│   │   │   ├── session/
│   │   │   │   └── test_browser_session_management.py
│   │   │   └── logout/
│   │   │       ├── test_rp_initiated_logout.py
│   │   │       ├── test_frontchannel_logout.py
│   │   │       └── test_backchannel_logout.py
│   │   └── http/
│   │       ├── rfc5785/
│   │       │   └── test_well_known_endpoints.py
│   │       └── rfc6265/
│   │           └── test_cookie_policies.py
│   ├── interop/
│   │   ├── generic_oidc_rp/
│   │   │   ├── test_basic_login.py
│   │   │   └── test_logout.py
│   │   ├── generic_resource_server/
│   │   │   ├── test_jwt_validation.py
│   │   │   └── test_introspection_validation.py
│   │   ├── keycloak/
│   │   │   ├── test_login.py
│   │   │   └── test_token_exchange.py
│   │   ├── okta/
│   │   │   └── test_metadata_and_jwks.py
│   │   └── azure/
│   │       └── test_oidc_discovery.py
│   ├── negative/
│   │   ├── test_alg_none_rejected.py
│   │   ├── test_bad_redirect_uri_rejected.py
│   │   ├── test_pkce_verifier_mismatch.py
│   │   ├── test_replayed_nonce_rejected.py
│   │   ├── test_replayed_dpop_proof_rejected.py
│   │   ├── test_invalid_client_metadata_rejected.py
│   │   └── test_invalid_request_object_rejected.py
│   ├── e2e/
│   │   ├── test_browser_auth_code_pkce.py
│   │   ├── test_service_to_service_exchange.py
│   │   ├── test_device_flow.py
│   │   └── test_revocation_and_introspection.py
│   ├── security/
│   │   ├── test_key_rotation.py
│   │   ├── test_jwks_rollover.py
│   │   ├── test_refresh_token_rotation.py
│   │   ├── test_replay_protection.py
│   │   └── test_csrf_and_session_fixation.py
│   └── perf/
│       ├── test_token_issue_latency.py
│       └── test_introspection_throughput.py
└── tigrbl_auth/
    ├── __init__.py
    ├── plugin.py
    ├── gateway.py
    ├── api/
    │   ├── __init__.py
    │   ├── app.py
    │   ├── lifecycle.py
    │   ├── surfaces.py
    │   ├── rest/
    │   │   ├── __init__.py
    │   │   ├── errors.py
    │   │   ├── openapi.py
    │   │   ├── deps/
    │   │   │   ├── __init__.py
    │   │   │   ├── auth.py
    │   │   │   ├── clients.py
    │   │   │   ├── tenants.py
    │   │   │   ├── sessions.py
    │   │   │   ├── security.py
    │   │   │   └── rate_limits.py
    │   │   ├── schemas/
    │   │   │   ├── __init__.py
    │   │   │   ├── common.py
    │   │   │   ├── authorize.py
    │   │   │   ├── token.py
    │   │   │   ├── registration.py
    │   │   │   ├── client_management.py
    │   │   │   ├── introspection.py
    │   │   │   ├── revocation.py
    │   │   │   ├── userinfo.py
    │   │   │   ├── logout.py
    │   │   │   ├── device.py
    │   │   │   ├── par.py
    │   │   │   ├── token_exchange.py
    │   │   │   ├── keys.py
    │   │   │   ├── metadata.py
    │   │   │   └── errors.py
    │   │   └── routers/
    │   │       ├── __init__.py
    │   │       ├── authorize.py
    │   │       ├── token.py
    │   │       ├── revocation.py
    │   │       ├── introspection.py
    │   │       ├── registration.py
    │   │       ├── client_management.py
    │   │       ├── userinfo.py
    │   │       ├── jwks.py
    │   │       ├── oauth_metadata.py
    │   │       ├── openid_configuration.py
    │   │       ├── logout.py
    │   │       ├── device_authorization.py
    │   │       ├── pushed_authorization.py
    │   │       ├── token_exchange.py
    │   │       └── health.py
    │   └── rpc/
    │       ├── __init__.py
    │       ├── openrpc.py
    │       ├── registry.py
    │       ├── schemas/
    │       │   ├── __init__.py
    │       │   ├── common.py
    │       │   ├── tenants.py
    │       │   ├── users.py
    │       │   ├── clients.py
    │       │   ├── services.py
    │       │   ├── service_keys.py
    │       │   ├── api_keys.py
    │       │   ├── sessions.py
    │       │   ├── keys.py
    │       │   ├── discovery.py
    │       │   ├── claims.py
    │       │   └── gates.py
    │       └── methods/
    │           ├── __init__.py
    │           ├── discover.py
    │           ├── tenants.py
    │           ├── users.py
    │           ├── clients.py
    │           ├── services.py
    │           ├── service_keys.py
    │           ├── api_keys.py
    │           ├── sessions.py
    │           ├── keys.py
    │           ├── claims.py
    │           └── gates.py
    ├── tables/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── engine.py
    │   ├── mixins.py
    │   ├── tenant.py
    │   ├── user.py
    │   ├── client.py
    │   ├── service.py
    │   ├── service_key.py
    │   ├── api_key.py
    │   ├── auth_session.py
    │   ├── auth_code.py
    │   ├── device_code.py
    │   ├── pushed_authorization_request.py
    │   ├── revoked_token.py
    │   ├── consent.py
    │   └── audit_event.py
    ├── ops/
    │   ├── __init__.py
    │   ├── tenants.py
    │   ├── users.py
    │   ├── clients.py
    │   ├── services.py
    │   ├── service_keys.py
    │   ├── api_keys.py
    │   ├── authenticate.py
    │   ├── authorize.py
    │   ├── login.py
    │   ├── logout.py
    │   ├── consent.py
    │   ├── sessions.py
    │   ├── register_client.py
    │   ├── manage_client.py
    │   ├── issue_access_token.py
    │   ├── issue_id_token.py
    │   ├── introspect_token.py
    │   ├── revoke_token.py
    │   ├── exchange_token.py
    │   ├── device_authorization.py
    │   ├── pushed_authorization.py
    │   ├── userinfo.py
    │   └── rotate_keys.py
    ├── services/
    │   ├── __init__.py
    │   ├── key_management.py
    │   ├── jwks_service.py
    │   ├── token_service.py
    │   ├── session_service.py
    │   ├── cookie_service.py
    │   ├── nonce_service.py
    │   ├── consent_service.py
    │   ├── principal_service.py
    │   ├── audit_service.py
    │   ├── evidence_bundle.py
    │   ├── spec_generation.py
    │   └── release_gate_service.py
    ├── standards/
    │   ├── __init__.py
    │   ├── jose/
    │   │   ├── __init__.py
    │   │   ├── jws.py
    │   │   ├── jwe.py
    │   │   ├── jwk.py
    │   │   ├── jwa.py
    │   │   ├── jwt.py
    │   │   ├── thumbprint.py
    │   │   ├── proof_of_possession.py
    │   │   └── bcp8725.py
    │   ├── oauth2/
    │   │   ├── __init__.py
    │   │   ├── core.py
    │   │   ├── bearer.py
    │   │   ├── revocation.py
    │   │   ├── introspection.py
    │   │   ├── pkce.py
    │   │   ├── dynamic_registration.py
    │   │   ├── client_management.py
    │   │   ├── native_apps.py
    │   │   ├── metadata.py
    │   │   ├── jwt_access_tokens.py
    │   │   ├── jar.py
    │   │   ├── par.py
    │   │   ├── issuer_id.py
    │   │   ├── rar.py
    │   │   ├── dpop.py
    │   │   ├── mtls.py
    │   │   ├── resource_indicators.py
    │   │   ├── token_exchange.py
    │   │   ├── device_authorization.py
    │   │   └── profiles/
    │   │       ├── __init__.py
    │   │       └── oauth2_1_alignment.py
    │   ├── oidc/
    │   │   ├── __init__.py
    │   │   ├── core.py
    │   │   ├── discovery.py
    │   │   ├── id_token.py
    │   │   ├── userinfo.py
    │   │   ├── session_mgmt.py
    │   │   ├── rp_initiated_logout.py
    │   │   ├── frontchannel_logout.py
    │   │   ├── backchannel_logout.py
    │   │   └── amr.py
    │   └── http/
    │       ├── __init__.py
    │       ├── auth_framework.py
    │       ├── well_known.py
    │       ├── cookies.py
    │       └── tls.py
    ├── extensions/
    │   ├── __init__.py
    │   ├── webauthn/
    │   │   ├── __init__.py
    │   │   ├── registration.py
    │   │   ├── authentication.py
    │   │   ├── attestation.py
    │   │   ├── assertion.py
    │   │   └── metadata.py
    │   ├── webpush/
    │   │   ├── __init__.py
    │   │   └── encryption.py
    │   ├── security_event_tokens/
    │   │   ├── __init__.py
    │   │   └── set.py
    │   └── experimental/
    │       ├── __init__.py
    │       └── future_profiles.py
    ├── security/
    │   ├── __init__.py
    │   ├── deps.py
    │   ├── csrf.py
    │   ├── headers.py
    │   ├── session_policy.py
    │   ├── algorithm_policy.py
    │   ├── key_rotation.py
    │   ├── proof_of_possession.py
    │   ├── rate_limits.py
    │   ├── validators.py
    │   └── threat_model.py
    ├── config/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── feature_flags.py
    │   ├── claim_matrix.py
    │   ├── release_profile.py
    │   └── logging.py
    ├── adapters/
    │   ├── __init__.py
    │   ├── context.py
    │   ├── local.py
    │   ├── remote.py
    │   ├── jwks_remote.py
    │   └── subjects.py
    ├── schemas/
    │   ├── json/
    │   │   ├── openid_configuration.schema.json
    │   │   ├── authorization_server_metadata.schema.json
    │   │   ├── jwks.schema.json
    │   │   ├── client_registration.schema.json
    │   │   └── openrpc_discovery.schema.json
    │   └── examples/
    │       ├── authorization_code_token_response.json
    │       ├── openid_configuration.json
    │       └── registration_request.json
    └── migrations/
        ├── env.py
        └── versions/
            ├── 0001_initial_identity_tables.py
            ├── 0002_client_and_service_tables.py
            ├── 0003_authorization_runtime_tables.py
            ├── 0004_device_par_revocation_tables.py
            ├── 0005_session_logout_tables.py
            └── 0006_key_rotation_and_audit_tables.py
```

### Explicit replacements from current package

```text
current                                  -> target
---------------------------------------- -> --------------------------------------------
tigrbl_auth/app.py                       -> tigrbl_auth/api/app.py + tigrbl_auth/gateway.py
tigrbl_auth/backends.py                  -> tigrbl_auth/ops/authenticate.py
tigrbl_auth/crypto.py                    -> tigrbl_auth/services/key_management.py + standards/jose/*
tigrbl_auth/db.py                        -> tigrbl_auth/tables/engine.py
tigrbl_auth/security.deps.py              -> tigrbl_auth/security/deps.py + api/rest/deps/*
tigrbl_auth/jwtoken.py                   -> tigrbl_auth/standards/jose/jwt.py + services/token_service.py
tigrbl_auth/oidc_discovery.py            -> tigrbl_auth/standards/oidc/discovery.py + api/rest/routers/openid_configuration.py
tigrbl_auth/oidc_id_token.py             -> tigrbl_auth/standards/oidc/id_token.py
tigrbl_auth/oidc_userinfo.py             -> tigrbl_auth/standards/oidc/userinfo.py + ops/userinfo.py
tigrbl_auth/runtime_cfg.py               -> tigrbl_auth/config/settings.py
tigrbl_auth/principal_ctx.py             -> tigrbl_auth/adapters/context.py
tigrbl_auth/orm/*                        -> tigrbl_auth/tables/*
tigrbl_auth/routers/*                    -> tigrbl_auth/api/rest/* and tigrbl_auth/api/rpc/*
tigrbl_auth/rfc/*                        -> tigrbl_auth/standards/{oauth2,oidc,jose,http}/*
tigrbl_auth/vendor/*                     -> deleted
tests/unit/test_rfc*.py                  -> tests/conformance/<domain>/<target>/*
```

## Proposed CLI surface

### Current package state

From the uploaded package as inspected locally:

- there is **no active CLI implementation** in the current package,
- there is **no live `project.scripts` entry point** in `pyproject.toml`, and
- the only CLI hint is a **commented** script line for a future Typer app.

So, today, the current package effectively exposes **no supported CLI flags**.

This document defines the **authoritative CLI surface that should exist in the new package** based on:

- the revised standards / compliance matrix,
- the required ADR and release-gate model,
- strict Tigrbl framework adherence,
- the need for certifiable RFC/OIDC/OAuth/OpenAPI/OpenRPC evidence.

---

### Root executable

```bash
tigrbl-auth [GLOBAL FLAGS] <COMMAND> [SUBCOMMAND] [FLAGS]
```

### Command groups

- `serve`
- `migrate`
- `spec`
- `verify`
- `gate`
- `evidence`
- `claims`
- `adr`
- `doctor`
- `keys`

---

### Global flags

| Flag | Short | Type | Default | Purpose |
|---|---|---:|---|---|
| `--config` | `-c` | path | none | Load package config file |
| `--env-file` | `-e` | path | none | Load environment overrides |
| `--profile` | `-p` | string | `default` | Named runtime/compliance profile |
| `--workspace-root` |  | path | repo root | Monorepo root override |
| `--tenant` | `-t` | string | none | Tenant context for tenant-scoped operations |
| `--issuer` |  | string | config | Override issuer URL |
| `--strict` / `--no-strict` |  | bool | `--strict` | Fail on warnings or incomplete evidence |
| `--offline` |  | bool | false | Disable network-dependent validations |
| `--format` | `-f` | enum | `table` | Output format: `table`, `json`, `yaml` |
| `--output` | `-o` | path | stdout | Output file path |
| `--verbose` | `-v` | count | 0 | Increase verbosity |
| `--quiet` | `-q` | bool | false | Suppress non-essential output |
| `--trace` |  | bool | false | Emit tracebacks and debugging detail |
| `--color` / `--no-color` |  | bool | `--color` | ANSI color control |
| `--fail-fast` / `--no-fail-fast` |  | bool | `--fail-fast` | Stop on first fatal failure |
| `--experimental` |  | bool | false | Enable experimental command paths |
| `--version` | `-V` | bool | false | Print CLI version |
| `--help` | `-h` | bool | false | Show help |

---

### `serve`

Run the Tigrbl/FastAPI auth service.

```bash
tigrbl-auth serve [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--host` | string | `127.0.0.1` | Bind host |
| `--port` | int | `8000` | Bind port |
| `--workers` | int | `1` | Worker count |
| `--reload` / `--no-reload` | bool | `--no-reload` | Auto-reload for development |
| `--uds` | path | none | UNIX domain socket |
| `--root-path` | string | none | ASGI root path |
| `--mount-prefix` | string | `/` | Mount prefix for Tigrbl surface |
| `--database-url` | string | config | DB override |
| `--public-base-url` | string | config | Public-facing base URL |
| `--issuer` | string | config | Issuer URL override |
| `--enable-rest` / `--disable-rest` | bool | `--enable-rest` | Mount REST routes |
| `--enable-rpc` / `--disable-rpc` | bool | `--enable-rpc` | Mount JSON-RPC routes |
| `--readiness-path` | string | `/health/ready` | Readiness path |
| `--liveness-path` | string | `/health/live` | Liveness path |
| `--metrics-path` | string | `/metrics` | Metrics path |
| `--access-log` / `--no-access-log` | bool | `--access-log` | Uvicorn access log control |
| `--proxy-headers` / `--no-proxy-headers` | bool | `--proxy-headers` | Respect proxy headers |
| `--forwarded-allow-ips` | string | config | Trusted proxy list |
| `--log-level` | enum | `info` | `critical`, `error`, `warning`, `info`, `debug`, `trace` |
| `--auto-migrate` / `--no-auto-migrate` | bool | `--no-auto-migrate` | Apply startup migrations |
| `--dev-seed-keys` / `--no-dev-seed-keys` | bool | `--no-dev-seed-keys` | Seed local dev keys |

---

### `migrate`

Schema migration and migration introspection.

#### `migrate plan`

```bash
tigrbl-auth migrate plan [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--database-url` | string | config | DB override |
| `--from-revision` | string | current | Starting revision |
| `--to-revision` | string | `head` | Target revision |
| `--tenant` | string | none | Tenant scope |
| `--sql` | bool | false | Emit SQL only |
| `--tag` | string | none | Migration tag |
| `--format` | enum | `table` | Output format |

#### `migrate upgrade`

```bash
tigrbl-auth migrate upgrade [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--revision` | string | `head` | Target revision |
| `--database-url` | string | config | DB override |
| `--tenant` | string | none | Tenant scope |
| `--sql` | bool | false | Dry-run SQL output |
| `--tag` | string | none | Migration tag |
| `--dry-run` | bool | false | Validate without applying |

#### `migrate downgrade`

```bash
tigrbl-auth migrate downgrade [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--revision` | string | required | Target lower revision |
| `--database-url` | string | config | DB override |
| `--tenant` | string | none | Tenant scope |
| `--sql` | bool | false | Dry-run SQL output |
| `--tag` | string | none | Migration tag |
| `--dry-run` | bool | false | Validate without applying |

#### `migrate revision`

```bash
tigrbl-auth migrate revision [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--message` | string | required | Migration message |
| `--autogenerate` / `--no-autogenerate` | bool | `--autogenerate` | Generate from model diff |
| `--head` | string | `head` | Parent revision |
| `--splice` | bool | false | Create splice revision |
| `--branch-label` | string | none | Branch label |
| `--depends-on` | string | none | Dependency revision |
| `--tenant-aware` / `--no-tenant-aware` | bool | `--tenant-aware` | Mark tenant-aware migration |

#### `migrate current`

```bash
tigrbl-auth migrate current [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--database-url` | string | config | DB override |
| `--tenant` | string | none | Tenant scope |
| `--verbose` | count | 0 | Include detailed state |

#### `migrate history`

```bash
tigrbl-auth migrate history [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--database-url` | string | config | DB override |
| `--tenant` | string | none | Tenant scope |
| `--from-revision` | string | base | Start revision |
| `--to-revision` | string | head | End revision |
| `--verbose` | count | 0 | Include migration body |

---

### `spec`

Build, validate, diff, and publish OpenAPI/OpenRPC artifacts.

#### `spec build`

```bash
tigrbl-auth spec build [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--target` | enum | `all` | `public`, `admin`, `resource-server`, `internal`, `all` |
| `--kind` | enum | `all` | `openapi`, `openrpc`, `all` |
| `--format` | enum | `yaml` | `yaml`, `json` |
| `--out-dir` | path | `specs/` | Output directory |
| `--canonical-server-url` | string | config | Canonical server URL |
| `--include-examples` / `--no-include-examples` | bool | `--include-examples` | Include examples |
| `--include-internal` / `--exclude-internal` | bool | `--exclude-internal` | Include internal-only surfaces |
| `--fail-on-warning` / `--no-fail-on-warning` | bool | `--fail-on-warning` | Treat warnings as failures |
| `--stamp-version` / `--no-stamp-version` | bool | `--stamp-version` | Stamp package version into spec |

#### `spec validate`

```bash
tigrbl-auth spec validate [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--input` | path | required | Spec file or directory |
| `--kind` | enum | infer | `openapi`, `openrpc` |
| `--lint-profile` | enum | `strict` | `relaxed`, `strict`, `release` |
| `--schema` | path | built-in | Override validation schema |
| `--fail-on-warning` / `--no-fail-on-warning` | bool | `--fail-on-warning` | Warning policy |
| `--offline` | bool | false | Disable remote reference resolution |

#### `spec diff`

```bash
tigrbl-auth spec diff [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--base` | path | required | Baseline spec |
| `--head` | path | required | Proposed spec |
| `--kind` | enum | infer | `openapi`, `openrpc` |
| `--breaking-only` / `--no-breaking-only` | bool | `--no-breaking-only` | Show only breaking changes |
| `--fail-on-breaking` / `--no-fail-on-breaking` | bool | `--fail-on-breaking` | Release-breaking policy |
| `--format` | enum | `table` | Output format |

#### `spec publish`

```bash
tigrbl-auth spec publish [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--source` | path | `specs/` | Spec source directory |
| `--target` | enum | `all` | Publish target surface |
| `--registry` | string | required | Destination registry or bucket |
| `--version-tag` | string | required | Version tag |
| `--sign` / `--no-sign` | bool | `--sign` | Sign published artifacts |
| `--attestation` | path | none | Attach release attestation |

---

### `verify`

Verify standards targets, contracts, conformance, interop, and security.

#### Common verify flags

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--target` | string | `all` | Standards target selector |
| `--` | enum | all | `foundation-boundary`, `baseline-interoperability`, `production-readiness`, `hardening-interop` |
| `--tier` | enum | all | `0`, `1`, `2`, `3`, `4` |
| `--matrix` | path | `compliance/targets/standards-matrix.yaml` | Standards matrix |
| `--evidence-dir` | path | `compliance/evidence/` | Evidence root |
| `--junit` | path | none | JUnit XML output |
| `--json-report` | path | none | JSON report output |
| `--max-failures` | int | unlimited | Stop after N failures |
| `--marker` | string | none | Test marker selector |
| `--pytest-args` | string | none | Pass-through pytest args |

#### `verify targets`

```bash
tigrbl-auth verify targets [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--require-adrs` / `--no-require-adrs` | bool | `--require-adrs` | Target must link ADRs |
| `--require-tests` / `--no-require-tests` | bool | `--require-tests` | Target must link tests |
| `--require-evidence` / `--no-require-evidence` | bool | `--require-evidence` | Target must link evidence |
| `--require-specs` / `--no-require-specs` | bool | `--require-specs` | Target must link contract artifacts |
| `--fail-unmapped` / `--no-fail-unmapped` | bool | `--fail-unmapped` | Reject unmapped targets |

#### `verify contracts`

```bash
tigrbl-auth verify contracts [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--openapi` | path | `specs/openapi/` | OpenAPI path |
| `--openrpc` | path | `specs/openrpc/` | OpenRPC path |
| `--fail-on-breaking` / `--no-fail-on-breaking` | bool | `--fail-on-breaking` | Breaking-change policy |
| `--require-generated` / `--no-require-generated` | bool | `--require-generated` | Ensure generated artifacts exist |

#### `verify conformance`

```bash
tigrbl-auth verify conformance [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--suite` | string | `all` | Conformance suite selector |
| `--rfc` | string | none | RFC-specific selector |
| `--oidc-profile` | string | none | OIDC profile selector |
| `--record-evidence` / `--no-record-evidence` | bool | `--record-evidence` | Save evidence artifacts |
| `--negative-only` / `--no-negative-only` | bool | `--no-negative-only` | Run only negative tests |

#### `verify interop`

```bash
tigrbl-auth verify interop [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--profile` | enum | `all` | `spa`, `confidential`, `native`, `device`, `resource-server`, `gateway`, `all` |
| `--peer` | string | none | Named peer implementation |
| `--peer-config` | path | none | Peer config file |
| `--record-wire` / `--no-record-wire` | bool | `--record-wire` | Save wire captures |
| `--publish-report` / `--no-publish-report` | bool | `--no-publish-report` | Publish interop report |

#### `verify security`

```bash
tigrbl-auth verify security [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--profile` | enum | `baseline` | `baseline`, `production`, `hardening` |
| `--check-dpop` / `--no-check-dpop` | bool | `--check-dpop` | Verify DPoP profile |
| `--check-mtls` / `--no-check-mtls` | bool | `--check-mtls` | Verify mTLS profile |
| `--check-par` / `--no-check-par` | bool | `--check-par` | Verify PAR |
| `--check-jar` / `--no-check-jar` | bool | `--check-jar` | Verify JAR |
| `--check-rar` / `--no-check-rar` | bool | `--check-rar` | Verify RAR |
| `--check-rotation` / `--no-check-rotation` | bool | `--check-rotation` | Verify key rotation |
| `--check-replay` / `--no-check-replay` | bool | `--check-replay` | Verify replay defenses |

#### `verify all`

```bash
tigrbl-auth verify all [FLAGS]
```

Uses the common verify flags and runs targets, contracts, conformance, interop, and security in the required order.

---

### `gate`

Release-gate evaluation and attestation.

#### `gate run`

```bash
tigrbl-auth gate run [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--gate-file` | path | auto | Specific gate manifest |
| `--` | enum | required | `foundation-boundary`, `baseline-interoperability`, `production-readiness`, `hardening-interop` |
| `--tier` | enum | all applicable | `1`, `2`, `3`, `4` |
| `--release` | string | current | Release identifier |
| `--blocking` / `--advisory` | bool | `--blocking` | Gate severity |
| `--waiver-file` | path | none | Approved waiver manifest |
| `--evidence-dir` | path | `compliance/evidence/` | Evidence root |
| `--attest-out` | path | none | Write attestation file |
| `--dry-run` | bool | false | Evaluate without status change |

#### `gate explain`

```bash
tigrbl-auth gate explain [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--` | enum | required | `foundation-boundary`, `baseline-interoperability`, `production-readiness`, `hardening-interop` |
| `--tier` | enum | none | Restrict to tier |
| `--format` | enum | `table` | Output format |

#### `gate status`

```bash
tigrbl-auth gate status [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--release` | string | current | Release identifier |
| `--history` / `--no-history` | bool | `--no-history` | Include prior evaluations |
| `--format` | enum | `table` | Output format |

#### `gate attest`

```bash
tigrbl-auth gate attest [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--release` | string | required | Release identifier |
| `--bundle` | path | required | Evidence bundle |
| `--sign` / `--no-sign` | bool | `--sign` | Sign attestation |
| `--signing-key` | string | config | Signing key reference |
| `--output` | path | required | Attestation output path |

---

### `evidence`

Evidence collection, packaging, verification, and publication.

#### `evidence collect`

```bash
tigrbl-auth evidence collect [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--source` | enum | `all` | `tests`, `interop`, `wire`, `logs`, `jwks`, `contracts`, `all` |
| `--run-id` | string | current run | CI or local run identifier |
| `--out-dir` | path | `compliance/evidence/` | Output directory |
| `--compress` / `--no-compress` | bool | `--compress` | Compress evidence |
| `--redact-secrets` / `--no-redact-secrets` | bool | `--redact-secrets` | Secret redaction |
| `--include-large-artifacts` / `--exclude-large-artifacts` | bool | `--exclude-large-artifacts` | Large-artifact policy |

#### `evidence verify`

```bash
tigrbl-auth evidence verify [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--bundle` | path | required | Evidence bundle or directory |
| `--checksums` | path | auto | Checksum file |
| `--manifest` | path | auto | Evidence manifest |
| `--strict` / `--no-strict` | bool | `--strict` | Fail on missing or mismatched artifacts |

#### `evidence bundle`

```bash
tigrbl-auth evidence bundle [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--input-dir` | path | `compliance/evidence/` | Evidence root |
| `--output` | path | required | Bundle path |
| `--format` | enum | `tar.gz` | `tar.gz`, `zip`, `dir` |
| `--sign` / `--no-sign` | bool | `--sign` | Sign bundle |
| `--sbom` / `--no-sbom` | bool | `--sbom` | Attach SBOM |
| `--provenance` / `--no-provenance` | bool | `--provenance` | Attach provenance |

#### `evidence publish`

```bash
tigrbl-auth evidence publish [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--bundle` | path | required | Bundle to publish |
| `--dest` | string | required | Destination registry/bucket |
| `--index` / `--no-index` | bool | `--index` | Update evidence index |
| `--visibility` | enum | `internal` | `private`, `internal`, `public` |

---

### `claims`

Standards-claim inspection and promotion control.

#### `claims list`

```bash
tigrbl-auth claims list [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--tier` | enum | all | Filter by tier |
| `--` | enum | all | Filter by |
| `--status` | enum | all | `planned`, `implemented`, `asserted`, `certified`, `peer-reviewed` |
| `--target` | string | all | Standards target selector |
| `--format` | enum | `table` | Output format |

#### `claims show`

```bash
tigrbl-auth claims show [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--claim-id` | string | required | Claim identifier |
| `--evidence` / `--no-evidence` | bool | `--evidence` | Show evidence links |
| `--tests` / `--no-tests` | bool | `--tests` | Show linked tests |
| `--adrs` / `--no-adrs` | bool | `--adrs` | Show linked ADRs |

#### `claims check`

```bash
tigrbl-auth claims check [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--claim-id` | string | required | Claim identifier |
| `--require-tier` | enum | none | Minimum tier required |
| `--require-peer` / `--no-require-peer` | bool | `--no-require-peer` | Require tier-4 evidence |
| `--format` | enum | `table` | Output format |

#### `claims lock`

```bash
tigrbl-auth claims lock [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--release` | string | required | Release identifier |
| `--output` | path | required | Locked claims manifest |
| `--sign` / `--no-sign` | bool | `--sign` | Sign locked claim manifest |

#### `claims promote`

```bash
tigrbl-auth claims promote [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--claim-id` | string | required | Claim identifier |
| `--to-tier` | enum | required | Target tier |
| `--peer-report` | path | none | Required for tier-4 promotion |
| `--waiver-file` | path | none | Waiver or exception manifest |

---

### `adr`

Architecture Decision Record management.

#### `adr new`

```bash
tigrbl-auth adr new [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--id` | string | auto | ADR number |
| `--title` | string | required | ADR title |
| `--status` | enum | `proposed` | `proposed`, `accepted`, `superseded`, `deprecated` |
| `--supersedes` | string | none | Prior ADR |
| `--owners` | string | none | Comma-separated owners |
| `--template` | string | `default` | ADR template |
| `--target` | string | none | Linked standards target |
| `--` | enum | none | Linked |
| `--tier` | enum | none | Linked tier |

#### `adr list`

```bash
tigrbl-auth adr list [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--status` | enum | all | Status filter |
| `--target` | string | none | Linked target filter |
| `--format` | enum | `table` | Output format |

#### `adr show`

```bash
tigrbl-auth adr show [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--id` | string | required | ADR number |
| `--render` | enum | `markdown` | `markdown`, `json` |

#### `adr check`

```bash
tigrbl-auth adr check [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--required` / `--no-required` | bool | `--required` | Treat missing ADRs as failure |
| `--changed-path` | path | none | Check ADR requirements for changed paths |
| `--fail-missing` / `--no-fail-missing` | bool | `--fail-missing` | Failure policy |
| `--enforce-target-links` / `--no-enforce-target-links` | bool | `--enforce-target-links` | Require standards links |

#### `adr index`

```bash
tigrbl-auth adr index [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--output` | path | `docs/adr/index.md` | Generated index path |
| `--format` | enum | `markdown` | `markdown`, `json` |

---

### `doctor`

Runtime and repository health inspection.

```bash
tigrbl-auth doctor [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--check` | enum | `all` | `config`, `db`, `keys`, `routes`, `specs`, `gates`, `all` |
| `--fix` / `--no-fix` | bool | `--no-fix` | Apply safe local fixes |
| `--database-url` | string | config | DB override |
| `--issuer` | string | config | Issuer override |
| `--format` | enum | `table` | Output format |

---

### `keys`

Signing and JWKS operational controls.

#### `keys rotate`

```bash
tigrbl-auth keys rotate [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--provider` | string | config | Key provider name |
| `--kid` | string | auto | Key identifier |
| `--alg` | string | config | Signing/encryption algorithm |
| `--use` | enum | `sig` | `sig`, `enc` |
| `--activation-time` | datetime | now | Activation time |
| `--retire-after` | duration | policy | Retirement interval |
| `--publish-jwks` / `--no-publish-jwks` | bool | `--publish-jwks` | Publish new JWKS |
| `--dry-run` | bool | false | Preview rotation only |

#### `keys jwks`

```bash
tigrbl-auth keys jwks [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--public-only` / `--no-public-only` | bool | `--public-only` | Emit public JWKS only |
| `--issuer` | string | config | Issuer for metadata links |
| `--output` | path | stdout | JWKS output path |
| `--format` | enum | `json` | `json`, `yaml` |

#### `keys verify`

```bash
tigrbl-auth keys verify [FLAGS]
```

| Flag | Type | Default | Purpose |
|---|---:|---|---|
| `--token` | string | required | JWT or detached proof |
| `--jwks-uri` | string | config | JWKS endpoint or file |
| `--alg-allow` | string | policy | Allowed algorithms |
| `--aud` | string | none | Audience override |
| `--iss` | string | none | Issuer override |
| `--now` | datetime | system time | Validation time override |

---

### Entry-point recommendation

The current package should promote this CLI via a real script entry in `pyproject.toml`:

```toml
[project.scripts]
tigrbl-auth = "tigrbl_auth.cli:app"
```

The implementation should use a single command app with subcommand modules:

- `tigrbl_auth/cli/__init__.py`
- `tigrbl_auth/cli/serve.py`
- `tigrbl_auth/cli/migrate.py`
- `tigrbl_auth/cli/spec.py`
- `tigrbl_auth/cli/verify.py`
- `tigrbl_auth/cli/gate.py`
- `tigrbl_auth/cli/evidence.py`
- `tigrbl_auth/cli/claims.py`
- `tigrbl_auth/cli/adr.py`
- `tigrbl_auth/cli/doctor.py`
- `tigrbl_auth/cli/keys.py`

---

### Bottom line

- **Current package**: no supported CLI flags yet.
- **Required new package CLI**: one root `tigrbl-auth` command with governance, conformance, evidence, ADR, spec, migration, and runtime command groups.
- **Most important commands for certification**: `verify`, `gate`, `evidence`, `claims`, and `adr`.

## Usage examples

These examples are split between:

- **Current-surface compatible examples**: grounded in the uploaded package's existing `surface_api`, discovery, token, introspection, device-flow, and token-exchange surfaces.
- **Target-tree examples**: aligned to the proposed Tigrbl-native tree with `plugin.py`, `api/`, `specs/`, `compliance/`, `gates/`, and `docs/adr/`.

---

### 1. Mount the auth package into a Tigrbl app

```python
from tigrbl.engine import engine
from tigrbl import TigrblApp
from tigrbl_auth.db import dsn
from tigrbl_auth.routers.surface import surface_api

app = TigrblApp(engine=engine(dsn))
surface_api.mount_jsonrpc(prefix="/rpc")
surface_api.attach_diagnostics(prefix="/system")
app.include_router(surface_api)
```

---

### 2. Run the app locally and inspect the REST docs

```bash
uvicorn tigrbl_auth.app:app --reload
open http://localhost:8000/docs
```

---

### 3. Read OIDC discovery metadata

```bash
curl http://localhost:8000/.well-known/openid-configuration | jq
```

Typical use:
- verify `issuer`
- verify `jwks_uri`
- verify `authorization_endpoint`, `token_endpoint`, and supported scopes

---

### 4. Read the JWKS document for token validation

```bash
curl http://localhost:8000/.well-known/jwks.json | jq
```

Typical use:
- hand the JWK set to a resource server
- validate `kid` rotation behavior
- verify signing keys published by the issuer

---

### 5. Use PKCE helpers for an authorization-code client

```python
from tigrbl_auth import create_code_verifier, create_code_challenge

verifier = create_code_verifier()
challenge = create_code_challenge(verifier)

print({
    "code_verifier": verifier,
    "code_challenge": challenge,
    "code_challenge_method": "S256",
})
```

Typical use:
- SPA
- native app
- confidential client using hardened auth-code flow

---

### 6. Introspect an access token or API key

```bash
curl -X POST http://localhost:8000/introspect \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'token=YOUR_ACCESS_TOKEN'
```

Typical use:
- API gateway asks whether token is active
- resource server checks validity and claims
- compliance tests verify RFC 7662 behavior

---

### 7. Run the device-code flow

```bash
# Device-code request item: request a device code
curl -X POST http://localhost:8000/device_codes/device_authorization \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'client_id=test-client&scope=openid'

# Device-code polling item: poll the token endpoint after approval
curl -X POST http://localhost:8000/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=DEVICE_CODE&client_id=test-client'
```

Typical use:
- CLI login
- TV/device activation
- headless fleet onboarding

---

### 8. Exchange a subject token for a narrower audience token

```bash
curl -X POST http://localhost:8000/token/exchange \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=urn:ietf:params:oauth:grant-type:token-exchange' \
  -d 'subject_token=SUBJECT_TOKEN' \
  -d 'subject_token_type=urn:ietf:params:oauth:token-type:access_token' \
  -d 'audience=https://api.example.com' \
  -d 'scope=read'
```

Typical use:
- service-to-service delegation
- audience reduction
- tenant-scoped downstream calls

---

### 9. Target-tree install pattern using the proposed plugin layout

```python
from tigrbl import TigrblApp
from tigrbl.engine import engine
from tigrbl_auth.plugin import install
from tigrbl_auth.config.settings import Settings

settings = Settings.from_env()
app = TigrblApp(engine=engine(settings.database_dsn))
install(app, settings=settings)
```

Target behavior:
- installs REST routes from `tigrbl_auth/api/rest/`
- installs JSON-RPC methods from `tigrbl_auth/api/rpc/`
- registers tables from `tigrbl_auth/tables/`
- loads standards features from `tigrbl_auth/standards/`

---

### 10. Enforce ADRs and release gates before cutting a release

```bash
# verify required ADRs exist for the claimed features
python scripts/verify_claims.py \
  --targets compliance/targets/standards-matrix.yaml \
  --adr-map compliance/mappings/target-to-adr.yaml

# run the release gate for a production claim
python scripts/run_release_gates.py \
  --gate gates/release/production-readiness-production.yaml \
  --claims compliance/targets/release-claims.yaml \
  --evidence compliance/evidence/
```

Target behavior:
- blocks release if required ADRs are missing
- blocks release if OpenAPI/OpenRPC artifacts are stale
- blocks release if evidence for Tier 3/Tier 4 claims is incomplete
- produces an auditable certification bundle

---

### Notes

- Examples **1–8** are grounded in the current package surface and tests.
- Examples **9–10** are **target-state** examples for the proposed tree and governance model.
- For a certifiable package, runtime usage alone is not enough; ADR, evidence, and release-gate workflows must be part of normal package operation.

## Source handling appendix

| Source file | Handling | Notes |
|---|---|---|
| `tigrbl_auth_standards_compliance_matrix_v2.md` | Included as canonical | Revised tier model with explicit Tier 4 independent peer claims |
| `tigrbl_auth_standards_compliance_matrix.md` | Partially merged | Unique sections retained: functional breakdown, OpenAPI targets, OpenRPC targets, claim-language discipline |
| `tigrbl_auth_project_tree_recommendation.md` | Included as canonical | Macro project layout, structural rules, release gates, ADRs |
| `tigrbl_auth_project_tree_recommendation (1).md` | Deduplicated | Identical to canonical project-tree recommendation file |
| `tigrbl_auth_full_module_tree.md` | Included as canonical | Exhaustive runtime and project tree plus replacement map |
| `tigrbl_auth_cli_flags.md` | Included as canonical | Root executable, commands, flags, and entry-point recommendation |
| `tigrbl_auth_usage_examples.md` | Included as canonical | Current-surface and target-state usage examples |
| `tigrbl_auth_standards_compliance_matrix_v2 (1).md` | Deduplicated | Identical to canonical revised matrix file |

### Canonical intent

Use this unified reference as the single planning artifact for the new `tigrbl_auth` package: standards target definition, certification tiering, implementation s, project structure, exhaustive runtime module tree, CLI governance surface, and operational usage patterns.
