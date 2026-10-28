<!-- NON_AUTHORITATIVE_HISTORICAL -->
> [!WARNING]
> Historical / non-authoritative checkpoint document.
> Do **not** use this file to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Target Reality Matrix

This matrix reconciles declared scope, current claims, owner modules, public surface state, test planning, and evidence planning.

## baseline-certifiable-now

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| RFC 6749 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/rfc6749.py<br>tba_auth/standards/oauth2/rfc6749_token.py | current: /authorize, /token<br>target: /authorize, /token | conformance, integration, interop | compliance/evidence/tier3/oauth2-core/ | none |
| RFC 6750 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/rfc6750.py | current: ∅<br>target: /token, /userinfo, /introspect | conformance, integration, interop | compliance/evidence/tier3/bearer/ | surface-drift |
| RFC 7636 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/rfc7636_pkce.py | current: ∅<br>target: /authorize, /token | conformance, integration, unit, interop | compliance/evidence/tier3/pkce/ | surface-drift |
| RFC 8414 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/rfc8414.py<br>tba_auth/standards/oauth2/rfc8414_metadata.py | current: /.well-known/oauth-authorization-server<br>target: /.well-known/oauth-authorization-server | conformance, integration | compliance/evidence/tier3/discovery/ | none |
| RFC 8615 | tier 3 / evidenced-release-gated | tba_auth/standards/http/well_known.py | current: /.well-known/openid-configuration, /.well-known/oauth-authorization-server, /.well-known/jwks.json, /.well-known/oauth-protected-resource<br>target: /.well-known/openid-configuration, /.well-known/oauth-authorization-server, /.well-known/jwks.json, /.well-known/oauth-protected-resource | integration, unit | compliance/evidence/tier3/well-known/ | none |
| RFC 7515 | tier 3 / evidenced-release-gated | tba_auth/standards/jose/rfc7515.py | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jose/ | none |
| RFC 7517 | tier 3 / evidenced-release-gated | tba_auth/standards/jose/rfc7517.py | current: /.well-known/jwks.json<br>target: /.well-known/jwks.json | conformance, unit | compliance/evidence/tier3/jwks/ | none |
| RFC 7518 | tier 3 / evidenced-release-gated | tba_auth/standards/jose/rfc7518.py | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jose/ | none |
| RFC 7519 | tier 3 / evidenced-release-gated | tba_auth/standards/jose/rfc7519.py | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jwt/ | none |
| OIDC Core 1.0 | tier 3 / evidenced-release-gated | tba_auth/standards/oidc/core.py<br>tba_auth/standards/oidc/id_token.py | current: ∅<br>target: ∅ | conformance, integration | compliance/evidence/tier3/oidc-core/ | none |
| OIDC Discovery 1.0 | tier 3 / evidenced-release-gated | tba_auth/standards/oidc/discovery.py | current: /.well-known/openid-configuration<br>target: /.well-known/openid-configuration | conformance, integration, interop | compliance/evidence/tier3/discovery/ | none |
| OpenAPI 3.1 / 3.2 compatible public contract | tier 3 / evidenced-release-gated | tba_auth/api/rest<br>tba_auth/api/surfaces.py | current: ∅<br>target: ∅ | e2e, integration, unit | compliance/evidence/tier3/contracts/openapi/ | none |

## production-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| RFC 7516 | tier 3 / evidenced-release-gated | tba_auth/standards/jose/rfc7516.py<br>tba_auth/standards/oidc/id_token.py | current: ∅<br>target: ∅ | unit | compliance/evidence/tier3/jwe/ | active-without-effective-claim:baseline |
| RFC 7009 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/revocation.py<br>tba_auth/api/rest/routers/revoke.py | current: /revoke<br>target: /revoke | conformance, integration, unit | compliance/evidence/tier3/revocation/ | none |
| RFC 7591 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/dynamic_client_registration.py<br>tba_auth/api/rest/routers/register.py | current: /register<br>target: /register | conformance, integration, unit | compliance/evidence/tier3/client-registration/ | none |
| RFC 7662 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/introspection.py<br>tba_auth/services/persistence.py | current: /introspect<br>target: /introspect | conformance, integration, unit | compliance/evidence/tier3/introspection/ | none |
| RFC 8252 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/native_apps.py<br>tba_auth/tables/client.py | current: /authorize, /token, /register, /register/{client_id}<br>target: /authorize, /token, /register, /register/{client_id} | unit, conformance, interop | compliance/evidence/tier3/native-apps/ | none |
| RFC 9068 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/jwt_access_tokens.py<br>tba_auth/services/token_service.py | current: /login, /token, /token/exchange<br>target: /login, /token, /token/exchange | conformance, integration, unit, interop | compliance/evidence/tier3/jwt-access-token-profile/ | none |
| RFC 6265 | tier 3 / evidenced-release-gated | tba_auth/standards/http/cookies.py<br>tba_auth/standards/oidc/session_mgmt.py | current: /login, /authorize, /logout<br>target: /login, /authorize, /logout | conformance, integration, negative | compliance/evidence/tier3/cookies/ | none |
| RFC 7521 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/assertion_framework.py<br>tba_auth/ops/token.py | current: /token<br>target: /token | unit | compliance/evidence/tier3/assertion-framework/ | none |
| RFC 7523 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/jwt_client_auth.py<br>tba_auth/ops/token.py | current: /token, /register, /register/{client_id}<br>target: /token, /register, /register/{client_id} | unit | compliance/evidence/tier3/jwt-client-auth/ | none |
| RFC 9728 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/rfc9728.py | current: /.well-known/oauth-protected-resource<br>target: /.well-known/oauth-protected-resource | integration, unit, interop | compliance/evidence/tier3/protected-resource-metadata/ | none |
| OIDC UserInfo | tier 3 / evidenced-release-gated | tba_auth/standards/oidc/userinfo.py | current: /userinfo<br>target: /userinfo | conformance, integration, unit | compliance/evidence/tier3/oidc-userinfo/ | none |
| OIDC Session Management | tier 3 / evidenced-release-gated | tba_auth/standards/oidc/session_mgmt.py<br>tba_auth/standards/http/cookies.py | current: /login, /authorize, /logout<br>target: /login, /authorize, /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-session-management/ | none |
| OIDC RP-Initiated Logout | tier 3 / evidenced-release-gated | tba_auth/standards/oidc/rp_initiated_logout.py<br>tba_auth/api/rest/routers/logout.py | current: /logout<br>target: /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-rp-initiated-logout/ | none |
| OpenRPC 1.4.x admin/control-plane contract | tier 3 / evidenced-release-gated | tba_auth/api/rpc/__init__.py<br>tba_auth/api/rpc/registry.py | current: /rpc<br>target: /rpc | e2e, unit | compliance/evidence/tier3/contracts/openrpc/ | active-without-effective-claim:baseline |

## hardening-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| RFC 7592 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/client_registration_management.py<br>tba_auth/tables/client_registration.py | current: /register/{client_id}<br>target: /register/{client_id} | unit, conformance, integration | compliance/evidence/tier3/client-registration-management/ | active-without-effective-claim:production |
| RFC 8628 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/device_authorization.py<br>tba_auth/api/rest/routers/device_authorization.py | current: /device_authorization<br>target: /device_authorization | unit, conformance, integration, interop | compliance/evidence/tier3/device-flow/ | none |
| RFC 8693 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/token_exchange.py<br>tba_auth/ops/token.py | current: /token/exchange<br>target: /token/exchange | unit, conformance, integration, interop | compliance/evidence/tier3/token-exchange/ | none |
| RFC 8705 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/mtls.py<br>tba_auth/standards/oauth2/rfc9700.py | current: /token, /token/exchange<br>target: /token, /token/exchange | conformance, integration, unit, interop | compliance/evidence/tier3/mtls/ | none |
| RFC 8707 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/resource_indicators.py<br>tba_auth/ops/authorize.py | current: /authorize, /token, /device_authorization, /par, /token/exchange<br>target: /authorize, /token, /device_authorization, /par, /token/exchange | unit, conformance, integration | compliance/evidence/tier3/resource-indicators/ | none |
| RFC 9101 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/jar.py<br>tba_auth/ops/authorize.py | current: /authorize, /par<br>target: /authorize, /par | conformance, integration, unit, interop | compliance/evidence/tier3/jar/ | none |
| RFC 9126 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/par.py<br>tba_auth/api/rest/routers/par.py | current: /par<br>target: /par | conformance, integration, unit, interop | compliance/evidence/tier3/par/ | none |
| RFC 9207 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/issuer_identification.py<br>tba_auth/config/deployment.py | current: /authorize, /.well-known/openid-configuration<br>target: /authorize, /.well-known/openid-configuration | conformance, integration, unit | compliance/evidence/tier3/issuer-identification/ | active-without-effective-claim:production |
| RFC 9396 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/rar.py<br>tba_auth/ops/authorize.py | current: /authorize, /par<br>target: /authorize, /par | conformance, integration, unit, interop | compliance/evidence/tier3/rar/ | none |
| RFC 9449 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/dpop.py<br>tba_auth/standards/oauth2/rfc9700.py | current: /token, /token/exchange<br>target: /token, /token/exchange | conformance, integration, unit, interop | compliance/evidence/tier3/dpop/ | none |
| RFC 9700 | tier 3 / evidenced-release-gated | tba_auth/standards/oauth2/rfc9700.py<br>tba_auth/ops/authorize.py | current: /authorize, /token, /.well-known/openid-configuration<br>target: /authorize, /token, /.well-known/openid-configuration | integration, negative, unit | compliance/evidence/tier3/security-bcp/ | none |
| OIDC Front-Channel Logout | tier 3 / evidenced-release-gated | tba_auth/standards/oidc/frontchannel_logout.py<br>tba_auth/standards/oidc/rp_initiated_logout.py | current: /logout<br>target: /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-frontchannel-logout/ | none |
| OIDC Back-Channel Logout | tier 3 / evidenced-release-gated | tba_auth/standards/oidc/backchannel_logout.py<br>tba_auth/standards/oidc/rp_initiated_logout.py | current: /logout<br>target: /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-backchannel-logout/ | none |

## runtime-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| ASGI 3 application package | tier 3 / evidenced-release-gated | tba_auth/api/app.py<br>tba_auth/app.py | current: ∅<br>target: ∅ | integration, unit, conformance | compliance/evidence/tier3/asgi-application/ | none |
| Runner profile: Uvicorn | tier 3 / evidenced-release-gated | tba_auth/api/app.py<br>tba_auth/gateway.py | current: ∅<br>target: ∅ | unit, integration, conformance | compliance/evidence/tier3/runner-uvicorn/ | none |
| Runner profile: Hypercorn | tier 3 / evidenced-release-gated | tba_auth/api/app.py<br>tba_auth/gateway.py | current: ∅<br>target: ∅ | unit, integration, conformance | compliance/evidence/tier3/runner-hypercorn/ | none |
| Runner profile: Tigrcorn | tier 3 / evidenced-release-gated | tba_auth/api/app.py<br>tba_auth/gateway.py | current: ∅<br>target: ∅ | unit, integration, conformance | compliance/evidence/tier3/runner-tigrcorn/ | none |

## operator-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| CLI operator surface | tier 3 / evidenced-release-gated | tba_auth/cli/main.py<br>tba_auth/cli/metadata.py | current: ∅<br>target: ∅ | unit, conformance | compliance/evidence/tier3/cli-operator-surface/ | none |
| Bootstrap and migration lifecycle | tier 3 / evidenced-release-gated | tba_auth/cli/main.py<br>tba_auth/cli/metadata.py | current: ∅<br>target: ∅ | unit, e2e, conformance | compliance/evidence/tier3/bootstrap-migration/ | none |
| Key lifecycle and JWKS publication | tier 3 / evidenced-release-gated | tba_auth/cli/metadata.py<br>tba_auth/cli/handlers.py | current: ∅<br>target: ∅ | unit, conformance | compliance/evidence/tier3/key-lifecycle-jwks/ | none |
| Import/export portability | tier 3 / evidenced-release-gated | tba_auth/cli/metadata.py<br>tba_auth/cli/handlers.py | current: ∅<br>target: ∅ | unit, conformance | compliance/evidence/tier3/import-export-portability/ | none |
| Release bundle and signature verification | tier 3 / evidenced-release-gated | tba_auth/cli/reports.py<br>tba_auth/cli/handlers.py | current: ∅<br>target: ∅ | unit, security | compliance/evidence/tier3/release-bundle-signing/ | none |

## out-of-scope/deferred

| Target | Kind | Reason |
|---|---|---|
| RFC 7800 | extension-quarantine | Optional hardening extension not yet promoted into the certified core boundary. |
| RFC 7952 | extension-quarantine | Outside the default OAuth 2.0 / OIDC auth-server certification boundary. |
| RFC 8291 | extension-quarantine | Web Push is not part of the certified auth-core boundary. |
| RFC 8812 | extension-quarantine | WebAuthn is extension work and not part of the default certified boundary. |
| RFC 8932 | extension-quarantine | RFC 8932 is not an OAuth/OIDC auth-core target and remains quarantined from certification claims. |
| OAuth 2.1 alignment profile | alignment-only | Track draft-era alignment only. Do not emit as a final RFC compliance claim. |
| SAML IdP/SP | out-of-scope-baseline | explicitly excluded from the default certification boundary |
| LDAP/AD federation | out-of-scope-baseline | explicitly excluded from the default certification boundary |
| SCIM | out-of-scope-baseline | explicitly excluded from the default certification boundary |
| full authorization-policy platform | out-of-scope-baseline | explicitly excluded from the default certification boundary |
| Supabase-style data-plane authorization | out-of-scope-baseline | explicitly excluded from the default certification boundary |
| framework-local auth subsystem | out-of-scope-baseline | explicitly excluded from the default certification boundary |
| Keycloak-scale federation breadth | out-of-scope-baseline | explicitly excluded from the default certification boundary |

