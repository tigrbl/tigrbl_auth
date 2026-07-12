> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

# Target Reality Matrix

This matrix reconciles declared scope, current claims, owner modules, public surface state, test planning, and evidence planning.

## baseline-certifiable-now

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| RFC 6749 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rfc6749.py<br>tigrbl_auth/standards/oauth2/rfc6749_token.py | current: /authorize, /token<br>target: /authorize, /token | conformance, integration, interop | compliance/evidence/tier3/oauth2-core/ | owner-module-path-missing |
| RFC 6750 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rfc6750.py | current: /token, /userinfo, /introspect<br>target: /token, /userinfo, /introspect | conformance, integration, interop | compliance/evidence/tier3/bearer/ | owner-module-path-missing |
| RFC 7636 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rfc7636_pkce.py | current: /authorize, /token<br>target: /authorize, /token | conformance, integration, unit, interop | compliance/evidence/tier3/pkce/ | owner-module-path-missing |
| RFC 8414 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rfc8414.py<br>tigrbl_auth/standards/oauth2/rfc8414_metadata.py | current: /.well-known/oauth-authorization-server<br>target: /.well-known/oauth-authorization-server | conformance, integration | compliance/evidence/tier3/discovery/ | owner-module-path-missing |
| RFC 8615 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/http/well_known.py | current: /.well-known/openid-configuration, /.well-known/oauth-authorization-server, /.well-known/jwks.json, /.well-known/oauth-protected-resource<br>target: /.well-known/openid-configuration, /.well-known/oauth-authorization-server, /.well-known/jwks.json, /.well-known/oauth-protected-resource | conformance, integration, unit | compliance/evidence/tier3/well-known/ | owner-module-path-missing |
| RFC 7515 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/jose/rfc7515.py | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jose/ | owner-module-path-missing |
| RFC 7516 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/jose/rfc7516.py<br>tigrbl_auth/standards/oidc/id_token.py | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jwe/ | owner-module-path-missing |
| RFC 7517 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/jose/rfc7517.py | current: /.well-known/jwks.json<br>target: /.well-known/jwks.json | conformance, unit | compliance/evidence/tier3/jwks/ | owner-module-path-missing |
| RFC 7518 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/jose/rfc7518.py | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jose/ | owner-module-path-missing |
| RFC 7519 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/jose/rfc7519.py | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jwt/ | owner-module-path-missing |
| RFC 6265 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/http/cookies.py<br>tigrbl_auth/standards/oidc/session_mgmt.py | current: /login, /authorize, /logout<br>target: /login, /authorize, /logout | conformance, integration, negative | compliance/evidence/tier3/cookies/ | owner-module-path-missing |
| OIDC Core 1.0 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/core.py<br>tigrbl_auth/standards/oidc/id_token.py | current: ∅<br>target: ∅ | conformance, integration | compliance/evidence/tier3/oidc-core/ | owner-module-path-missing |
| OIDC Discovery 1.0 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/discovery.py | current: /.well-known/openid-configuration<br>target: /.well-known/openid-configuration | conformance, integration, interop | compliance/evidence/tier3/discovery/ | owner-module-path-missing |
| OIDC Session Management | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/session_mgmt.py<br>tigrbl_auth/standards/http/cookies.py | current: /login, /authorize, /logout<br>target: /login, /authorize, /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-session-management/ | owner-module-path-missing |
| OpenAPI 3.1 / 3.2 compatible public contract | tier 3 / generated-live-from-deployment-metadata | tigrbl_auth/api/rest<br>tigrbl_auth/api/surfaces.py | current: ∅<br>target: ∅ | e2e, integration, unit | compliance/evidence/tier3/contracts/openapi/ | owner-module-path-missing |

## production-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| RFC 7009 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/revocation.py<br>tigrbl_auth/api/rest/routers/revoke.py | current: /revoke<br>target: /revoke | conformance, integration, unit | compliance/evidence/tier3/revocation/ | owner-module-path-missing |
| RFC 7591 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/dynamic_client_registration.py<br>tigrbl_auth/api/rest/routers/register.py | current: /register<br>target: /register | conformance, integration, unit | compliance/evidence/tier3/client-registration/ | owner-module-path-missing |
| RFC 7592 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/client_registration_management.py<br>tigrbl_auth/tables/client_registration.py | current: /register/{client_id}<br>target: /register/{client_id} | unit, conformance, integration | compliance/evidence/tier3/client-registration-management/ | owner-module-path-missing |
| RFC 7662 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/introspection.py<br>tigrbl_auth/services/persistence.py | current: /introspect<br>target: /introspect | conformance, integration, unit | compliance/evidence/tier3/introspection/ | owner-module-path-missing |
| RFC 8252 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/native_apps.py<br>tigrbl_auth/tables/client.py | current: /authorize, /token, /register, /register/{client_id}<br>target: /authorize, /token, /register, /register/{client_id} | unit, conformance, interop | compliance/evidence/tier3/native-apps/ | owner-module-path-missing |
| RFC 9068 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/jwt_access_tokens.py<br>tigrbl_auth/services/token_service.py | current: /login, /token, /token/exchange<br>target: /login, /token, /token/exchange | conformance, integration, unit, interop | compliance/evidence/tier3/jwt-access-token-profile/ | owner-module-path-missing |
| RFC 9207 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/issuer_identification.py<br>tigrbl_auth/config/deployment.py | current: /authorize, /.well-known/openid-configuration<br>target: /authorize, /.well-known/openid-configuration | conformance, integration, unit | compliance/evidence/tier3/issuer-identification/ | owner-module-path-missing |
| RFC 7521 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/assertion_framework.py<br>tigrbl_auth/ops/token.py | current: /token<br>target: /token | conformance, unit | compliance/evidence/tier3/assertion-framework/ | owner-module-path-missing |
| RFC 7523 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/jwt_client_auth.py<br>tigrbl_auth/ops/token.py | current: /token, /register, /register/{client_id}<br>target: /token, /register, /register/{client_id} | conformance, unit | compliance/evidence/tier3/jwt-client-auth/ | owner-module-path-missing |
| RFC 9728 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rfc9728.py | current: /.well-known/oauth-protected-resource<br>target: /.well-known/oauth-protected-resource | conformance, integration, unit, interop | compliance/evidence/tier3/protected-resource-metadata/ | owner-module-path-missing |
| OIDC UserInfo | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/userinfo.py | current: /userinfo<br>target: /userinfo | conformance, integration, unit | compliance/evidence/tier3/oidc-userinfo/ | owner-module-path-missing |
| OIDC RP-Initiated Logout | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/rp_initiated_logout.py<br>tigrbl_auth/api/rest/routers/logout.py | current: /logout<br>target: /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-rp-initiated-logout/ | owner-module-path-missing |
| OpenRPC 1.4.x admin/control-plane contract | tier 3 / implementation-backed-generated-from-rpc-registry | tigrbl_auth/api/rpc/__init__.py<br>tigrbl_auth/api/rpc/registry.py | current: /rpc<br>target: /rpc | e2e, unit | compliance/evidence/tier3/contracts/openrpc/ | owner-module-path-missing |

## hardening-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| RFC 8628 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/device_authorization.py<br>tigrbl_auth/api/rest/routers/device_authorization.py | current: /device_authorization<br>target: /device_authorization | unit, conformance, integration, interop | compliance/evidence/tier3/device-flow/ | owner-module-path-missing |
| RFC 8693 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/token_exchange.py<br>tigrbl_auth/ops/token.py | current: /token/exchange<br>target: /token/exchange | unit, conformance, integration, interop | compliance/evidence/tier3/token-exchange/ | owner-module-path-missing |
| RFC 8705 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/mtls.py<br>tigrbl_auth/standards/oauth2/rfc9700.py | current: /token, /token/exchange<br>target: /token, /token/exchange | conformance, integration, unit, interop | compliance/evidence/tier3/mtls/ | owner-module-path-missing |
| RFC 8707 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/resource_indicators.py<br>tigrbl_auth/ops/authorize.py | current: /authorize, /token, /device_authorization, /par, /token/exchange<br>target: /authorize, /token, /device_authorization, /par, /token/exchange | unit, conformance, integration | compliance/evidence/tier3/resource-indicators/ | owner-module-path-missing |
| RFC 9101 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/jar.py<br>tigrbl_auth/ops/authorize.py | current: /authorize, /par<br>target: /authorize, /par | conformance, integration, unit, interop | compliance/evidence/tier3/jar/ | owner-module-path-missing |
| RFC 9126 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/par.py<br>tigrbl_auth/api/rest/routers/par.py | current: /par<br>target: /par | conformance, integration, unit, interop | compliance/evidence/tier3/par/ | owner-module-path-missing |
| RFC 9396 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rar.py<br>tigrbl_auth/ops/authorize.py | current: /authorize, /par<br>target: /authorize, /par | conformance, integration, unit, interop | compliance/evidence/tier3/rar/ | owner-module-path-missing |
| RFC 9449 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/dpop.py<br>tigrbl_auth/standards/oauth2/rfc9700.py | current: /token, /token/exchange<br>target: /token, /token/exchange | conformance, integration, unit, interop | compliance/evidence/tier3/dpop/ | owner-module-path-missing |
| RFC 9700 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rfc9700.py<br>tigrbl_auth/ops/authorize.py | current: /authorize, /token, /.well-known/openid-configuration<br>target: /authorize, /token, /.well-known/openid-configuration | conformance, integration, negative, unit | compliance/evidence/tier3/security-bcp/ | owner-module-path-missing |
| OIDC Front-Channel Logout | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/frontchannel_logout.py<br>tigrbl_auth/standards/oidc/rp_initiated_logout.py | current: /logout<br>target: /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-frontchannel-logout/ | owner-module-path-missing |
| OIDC Back-Channel Logout | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/backchannel_logout.py<br>tigrbl_auth/standards/oidc/rp_initiated_logout.py | current: /logout<br>target: /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-backchannel-logout/ | owner-module-path-missing |

## runtime-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| ASGI 3 application package | tier 3 / evidenced-release-gated | tigrbl_auth/api/app.py<br>tigrbl_auth/app.py | current: ∅<br>target: ∅ | integration, unit, conformance | compliance/evidence/tier3/asgi-application/ | owner-module-path-missing |
| Runner profile: Uvicorn | tier 3 / evidenced-release-gated | tigrbl_auth/api/app.py<br>tigrbl_auth/gateway.py | current: ∅<br>target: ∅ | unit, integration, conformance | compliance/evidence/tier3/runner-uvicorn/ | owner-module-path-missing |
| Runner profile: Hypercorn | tier 3 / evidenced-release-gated | tigrbl_auth/api/app.py<br>tigrbl_auth/gateway.py | current: ∅<br>target: ∅ | unit, integration, conformance | compliance/evidence/tier3/runner-hypercorn/ | owner-module-path-missing |
| Runner profile: Tigrcorn | tier 3 / evidenced-release-gated | tigrbl_auth/api/app.py<br>tigrbl_auth/gateway.py | current: ∅<br>target: ∅ | unit, integration, conformance | compliance/evidence/tier3/runner-tigrcorn/ | owner-module-path-missing |

## operator-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| CLI operator surface | tier 3 / evidenced-release-gated | tigrbl_auth/cli<br>tigrbl_auth/services/operator_service.py | current: ∅<br>target: ∅ | unit, conformance | compliance/evidence/tier3/cli-operator-surface/ | owner-module-path-missing |
| Bootstrap and migration lifecycle | tier 3 / evidenced-release-gated | tigrbl_auth/cli<br>tigrbl_auth/services/persistence.py | current: ∅<br>target: ∅ | unit, e2e, conformance | compliance/evidence/tier3/bootstrap-migration/ | owner-module-path-missing |
| Key lifecycle and JWKS publication | tier 3 / evidenced-release-gated | tigrbl_auth/cli<br>tigrbl_auth/api/rpc/methods/keys.py | current: ∅<br>target: ∅ | unit, conformance | compliance/evidence/tier3/key-lifecycle-jwks/ | owner-module-path-missing |
| Import/export portability | tier 3 / evidenced-release-gated | tigrbl_auth/cli<br>tigrbl_auth/services/import_export_service.py | current: ∅<br>target: ∅ | unit, conformance | compliance/evidence/tier3/import-export-portability/ | owner-module-path-missing |
| Release bundle and signature verification | tier 3 / evidenced-release-gated | tigrbl_auth/cli | current: ∅<br>target: ∅ | unit, security | compliance/evidence/tier3/release-bundle-signing/ | owner-module-path-missing |

## out-of-scope/deferred

| Target | Kind | Reason |
|---|---|---|
| RFC 7800 | extension-quarantine | Optional hardening extension not yet promoted into the certified core boundary. |
| RFC 8417 | extension-quarantine | Outside the default OAuth 2.0 / OIDC auth-server certification boundary. |
| RFC 8291 | extension-quarantine | Web Push is not part of the certified auth-core boundary. |
| RFC 8812 | extension-quarantine | WebAuthn is extension work and not part of the default certified boundary. |
| RFC 8932 | extension-quarantine | RFC 8932 is not an OAuth/OIDC auth-core target and remains quarantined from certification claims. |
| OAuth 2.1 alignment profile | alignment-only | Track draft-era alignment only. Do not emit as a final RFC compliance claim. |
| FAPI 2.0 Message Signing profile | alignment-only | Track external sector profile coverage only. Do not emit as a retained core certification claim. |
| SMART App Launch profile | alignment-only | Track external healthcare profile coverage only. Do not emit as a retained core certification claim. |
| SMART Backend Services profile | alignment-only | Track external healthcare backend profile coverage only. Do not emit as a retained core certification claim. |
| FAST / UDAP Security profile | alignment-only | Track external trust-community profile coverage only. Do not emit as a retained core certification claim. |
| IHE IUA profile | alignment-only | Track external healthcare authorization profile coverage only. Do not emit as a retained core certification claim. |
| NIST SP 800-63B-4 profile | alignment-only | Track external assurance profile coverage only. Do not emit as a retained core certification claim. |
| NIST SP 800-63C-4 profile | alignment-only | Track external federation assurance profile coverage only. Do not emit as a retained core certification claim. |
| CAMARA Security and Interoperability profile | alignment-only | Track external telecom profile coverage only. Do not emit as a retained core certification claim. |
| FDX CSDF Security Model and Profile | alignment-only | Track external financial-data profile coverage only. Do not emit as a retained core certification claim. |
| GNAP Core + Resource Server profile | alignment-only | Track adjacent authorization profile coverage only. Do not emit as a retained core certification claim. |
| WebAuthn and passkey-bound OAuth patterns | alignment-only | Track external pattern coverage only. Do not emit as a retained core certification claim. |
| Confidential SPA profile pattern | alignment-only | Track external browser-architecture pattern coverage only. Do not emit as a retained core certification claim. |
| SAML IdP/SP | out-of-scope-baseline | explicitly excluded from the default certification boundary |
| LDAP/AD federation | out-of-scope-baseline | explicitly excluded from the default certification boundary |
| SCIM | out-of-scope-baseline | explicitly excluded from the default certification boundary |
| full authorization-policy platform | out-of-scope-baseline | explicitly excluded from the default certification boundary |
| Supabase-style data-plane authorization | out-of-scope-baseline | explicitly excluded from the default certification boundary |
| framework-local auth subsystem | out-of-scope-baseline | explicitly excluded from the default certification boundary |
| Keycloak-scale federation breadth | out-of-scope-baseline | explicitly excluded from the default certification boundary |

