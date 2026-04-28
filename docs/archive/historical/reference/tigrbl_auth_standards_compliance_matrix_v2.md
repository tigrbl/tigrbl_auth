> [!WARNING]
> Archived historical reference. This document is retained for audit history only and is **not** an authoritative current-state artifact.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` for the current source of truth.

# Tigrbl Auth — Standards / Compliance Target Matrix (Revised Tier Model)

## Provenance and scope

This document consolidates the standards, interoperability, and compliance target analysis discussed for `tigrbl_auth`.

Accessible repository surface did **not** expose a declared RFC or standards matrix. The only readable top-level package documentation visible during review was a title-only README:

> `# swarmauri-auth`

Accordingly, the matrices below represent the **recommended target boundary and implementation plan**, not a verified claim that the current package already satisfies these standards.

---

## Certification tier model (revised)

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

## Implementation model

| | Meaning |
|---|---|
| foundation-boundary | Foundation / boundary definition |
| baseline-interoperability | Interoperable baseline |
| production-readiness | Production completion |
| hardening-interop | Hardening / advanced interop |

---

## Consolidated standards / compliance matrix

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

## Claim discipline for independent peer claims

A feature should not be placed in **Tier 4** merely because it is difficult or security-sensitive. Tier 4 should be reserved for features whose claim is supported by one or more of the following:

| Evidence class | Examples |
|---|---|
| Independent interoperability validation | Interop testing against third-party IdPs, RPs, gateways, SDKs, or resource servers |
| External conformance review | Independent protocol review, peer-reviewed implementation assessment, or recognized external audit |
| Reproducible public evidence | Public fixtures, wire captures, preserved artifacts, independently repeatable conformance cases |
| Cross-implementation verification | Same feature validated against multiple independent stacks |

### Practical interpretation

| Tier | Claim posture |
|---|---|
| Tier 1 | “Implemented.” |
| Tier 2 | “We assert standards alignment.” |
| Tier 3 | “We have preserved evidence and internal certification artifacts.” |
| Tier 4 | “The claim has independent peer or third-party support.” |

---

## Recommended implementation ordering

| | Objective | Core targets |
|---|---|---|
| foundation-boundary | Foundation / boundary definition | HTTP semantics, TLS-only boundary, accurate standards claims, no false OpenRPC-over-OAuth claim |
| baseline-interoperability | Minimum interoperable identity server | RFC 6749, RFC 6750, RFC 7636, RFC 8414, RFC 7515/7517/7518/7519, OIDC Core, OIDC Discovery, authorization/token/JWKS/metadata |
| production-readiness | Production-grade auth platform | RFC 7009, RFC 7662, RFC 9068, RFC 7591, RFC 6265, OIDC userinfo/session/logout, OpenAPI 3.1 complete contract, RFC 8252 |
| hardening-interop | Hardened / enterprise | RFC 8705 or RFC 9449, RFC 8693, RFC 8628, RFC 9101, RFC 9126, RFC 9396, RFC 7592, front/back-channel logout, conformance evidence, independent interop validation preparation |

---

## Minimal certifiable claim set

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

## Critical missing targets to treat as non-optional after baseline

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

## Summary

A credible `tigrbl_auth` standards boundary should be built in layers:

1. **Implemented foundation**: accurate protocol boundary, endpoint surface, and no overstated claims.
2. **Self-asserted interoperability**: OAuth 2.0 core, bearer, PKCE, discovery/metadata, JOSE/JWT, OIDC Core.
3. **Evidence-backed certification**: revocation, introspection, JWT access-token profile, browser sessions, logout, client registration, OpenAPI 3.1 completeness, negative and preserved conformance artifacts.
4. **Independent peer claims**: sender-constrained tokens, hardening profiles, cross-stack interop, externally reviewable and reproducible evidence.
