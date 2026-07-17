> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

# Target Reality Matrix

This matrix reconciles declared scope, current claims, owner modules, public surface state, test planning, and evidence planning.

## baseline-certifiable-now

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| RFC 6749 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/authorization_framework.py | current: /authorize, /token<br>target: /authorize, /token | conformance, integration, interop | compliance/evidence/tier3/oauth2-core/ | none |
| RFC 6750 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/bearer_token_usage.py | current: /token, /userinfo, /introspect<br>target: /token, /userinfo, /introspect | conformance, integration, interop | compliance/evidence/tier3/bearer/ | none |
| RFC 7636 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/proof_key_for_code_exchange.py | current: /authorize, /token<br>target: /authorize, /token | conformance, integration, unit, interop | compliance/evidence/tier3/pkce/ | none |
| RFC 8414 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/authorization_server_metadata.py | current: /.well-known/oauth-authorization-server<br>target: /.well-known/oauth-authorization-server | conformance, integration | compliance/evidence/tier3/discovery/ | none |
| RFC 8615 | tier 3 / evidenced-release-gated | pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/http_standards/well_known.py | current: /.well-known/openid-configuration, /.well-known/oauth-authorization-server, /.well-known/jwks.json, /.well-known/oauth-protected-resource<br>target: /.well-known/openid-configuration, /.well-known/oauth-authorization-server, /.well-known/jwks.json, /.well-known/oauth-protected-resource | conformance, integration, unit | compliance/evidence/tier3/well-known/ | none |
| RFC 7515 | tier 3 / evidenced-release-gated | pkgs/20-providers/tigrbl-identity-jose/src/tigrbl_identity_jose | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jose/ | none |
| RFC 7516 | tier 3 / evidenced-release-gated | pkgs/20-providers/tigrbl-identity-jose/src/tigrbl_identity_jose | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jwe/ | none |
| RFC 7517 | tier 3 / evidenced-release-gated | pkgs/20-providers/tigrbl-identity-jose/src/tigrbl_identity_jose | current: /.well-known/jwks.json<br>target: /.well-known/jwks.json | conformance, unit | compliance/evidence/tier3/jwks/ | none |
| RFC 7518 | tier 3 / evidenced-release-gated | pkgs/20-providers/tigrbl-identity-jose/src/tigrbl_identity_jose | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jose/ | none |
| RFC 7519 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-jwt/src/tigrbl_auth_protocol_jwt | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jwt/ | none |
| RFC 6265 | tier 3 / evidenced-release-gated | pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/http_standards/cookies.py | current: /login, /authorize, /logout<br>target: /login, /authorize, /logout | conformance, integration, negative | compliance/evidence/tier3/cookies/ | none |
| OIDC Core 1.0 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/standards/core.py | current: ∅<br>target: ∅ | conformance, integration | compliance/evidence/tier3/oidc-core/ | none |
| OIDC Discovery 1.0 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/standards/discovery.py | current: /.well-known/openid-configuration<br>target: /.well-known/openid-configuration | conformance, integration, interop | compliance/evidence/tier3/discovery/ | none |
| OIDC Session Management | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/standards/session_mgmt.py | current: /login, /authorize, /logout<br>target: /login, /authorize, /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-session-management/ | none |
| OpenAPI 3.1 / 3.2 compatible public contract | tier 3 / generated-live-from-deployment-metadata | pkgs/90-backend-apps/tigrbl-auth-backend-app-public/src/tigrbl_auth_backend_app_public/openapi.py | current: ∅<br>target: ∅ | e2e, integration, unit | compliance/evidence/tier3/contracts/openapi/ | none |

## production-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| RFC 7009 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/revocation.py | current: /revoke<br>target: /revoke | conformance, integration, unit | compliance/evidence/tier3/revocation/ | none |
| RFC 7591 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/dynamic_client_registration.py | current: /register<br>target: /register | conformance, integration, unit | compliance/evidence/tier3/client-registration/ | none |
| RFC 7592 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/client_registration_management.py | current: /register/{client_id}<br>target: /register/{client_id} | unit, conformance, integration | compliance/evidence/tier3/client-registration-management/ | none |
| RFC 7662 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/introspection.py | current: /introspect<br>target: /introspect | conformance, integration, unit | compliance/evidence/tier3/introspection/ | none |
| RFC 8252 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/native_apps.py | current: /authorize, /token, /register, /register/{client_id}<br>target: /authorize, /token, /register, /register/{client_id} | unit, conformance, interop | compliance/evidence/tier3/native-apps/ | none |
| RFC 9068 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/jwt_access_tokens.py | current: /login, /token, /token/exchange<br>target: /login, /token, /token/exchange | conformance, integration, unit, interop | compliance/evidence/tier3/jwt-access-token-profile/ | none |
| RFC 9207 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/issuer_identification.py | current: /authorize, /.well-known/openid-configuration<br>target: /authorize, /.well-known/openid-configuration | conformance, integration, unit | compliance/evidence/tier3/issuer-identification/ | none |
| RFC 7521 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/assertion_framework.py | current: /token<br>target: /token | conformance, unit | compliance/evidence/tier3/assertion-framework/ | none |
| RFC 7523 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/jwt_client_auth.py | current: /token, /register, /register/{client_id}<br>target: /token, /register, /register/{client_id} | conformance, unit | compliance/evidence/tier3/jwt-client-auth/ | none |
| RFC 9728 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/protected_resource_metadata.py | current: /.well-known/oauth-protected-resource<br>target: /.well-known/oauth-protected-resource | conformance, integration, unit, interop | compliance/evidence/tier3/protected-resource-metadata/ | none |
| OIDC UserInfo | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/standards/userinfo.py | current: /userinfo<br>target: /userinfo | conformance, integration, unit | compliance/evidence/tier3/oidc-userinfo/ | none |
| OIDC RP-Initiated Logout | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/standards/rp_initiated_logout.py | current: /logout<br>target: /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-rp-initiated-logout/ | none |
| OpenRPC 1.4.x admin/control-plane contract | tier 3 / implementation-backed-generated-from-rpc-registry | pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/api | current: /rpc<br>target: /rpc | e2e, unit | compliance/evidence/tier3/contracts/openrpc/ | none |

## hardening-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| RFC 8628 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/device_authorization.py | current: /device_authorization<br>target: /device_authorization | unit, conformance, integration, interop | compliance/evidence/tier3/device-flow/ | none |
| RFC 8693 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/token_exchange.py | current: /token/exchange<br>target: /token/exchange | unit, conformance, integration, interop | compliance/evidence/tier3/token-exchange/ | none |
| RFC 8705 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/mutual_tls_client_authentication.py | current: /token, /token/exchange<br>target: /token, /token/exchange | conformance, integration, unit, interop | compliance/evidence/tier3/mtls/ | none |
| RFC 8707 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/resource_indicators.py | current: /authorize, /token, /device_authorization, /par, /token/exchange<br>target: /authorize, /token, /device_authorization, /par, /token/exchange | unit, conformance, integration | compliance/evidence/tier3/resource-indicators/ | none |
| RFC 9101 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/jwt_secured_authorization_requests.py | current: /authorize, /par<br>target: /authorize, /par | conformance, integration, unit, interop | compliance/evidence/tier3/jar/ | none |
| RFC 9126 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/pushed_authorization_requests.py | current: /par<br>target: /par | conformance, integration, unit, interop | compliance/evidence/tier3/par/ | none |
| RFC 9396 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/rich_authorization_requests.py | current: /authorize, /par<br>target: /authorize, /par | conformance, integration, unit, interop | compliance/evidence/tier3/rar/ | none |
| RFC 9449 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/dpop.py | current: /token, /token/exchange<br>target: /token, /token/exchange | conformance, integration, unit, interop | compliance/evidence/tier3/dpop/ | none |
| RFC 9700 | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/oauth_security_bcp.py | current: /authorize, /token, /.well-known/openid-configuration<br>target: /authorize, /token, /.well-known/openid-configuration | conformance, integration, negative, unit | compliance/evidence/tier3/security-bcp/ | none |
| OIDC Front-Channel Logout | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/standards/frontchannel_logout.py | current: /logout<br>target: /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-frontchannel-logout/ | none |
| OIDC Back-Channel Logout | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/standards/backchannel_logout.py | current: /logout<br>target: /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-backchannel-logout/ | none |

## runtime-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| ASGI 3 application package | tier 3 / evidenced-release-gated | pkgs/90-backend-apps/tigrbl-auth-backend-app-public/src/tigrbl_auth_backend_app_public/app.py | current: ∅<br>target: ∅ | integration, unit, conformance | compliance/evidence/tier3/asgi-application/ | none |
| Runner profile: Uvicorn | tier 3 / evidenced-release-gated | pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/uvicorn.py | current: ∅<br>target: ∅ | unit, integration, conformance | compliance/evidence/tier3/runner-uvicorn/ | none |
| Runner profile: Hypercorn | tier 3 / evidenced-release-gated | pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/hypercorn.py | current: ∅<br>target: ∅ | unit, integration, conformance | compliance/evidence/tier3/runner-hypercorn/ | none |
| Runner profile: Tigrcorn | tier 3 / evidenced-release-gated | pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/tigrcorn.py | current: ∅<br>target: ∅ | unit, integration, conformance | compliance/evidence/tier3/runner-tigrcorn/ | none |

## operator-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| CLI operator surface | tier 3 / evidenced-release-gated | pkgs/60-runtime/tigrbl-identity-cli/src/tigrbl_identity_cli/cli | current: ∅<br>target: ∅ | unit, conformance | compliance/evidence/tier3/cli-operator-surface/ | none |
| Bootstrap and migration lifecycle | tier 3 / evidenced-release-gated | pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/migrations | current: ∅<br>target: ∅ | unit, e2e, conformance | compliance/evidence/tier3/bootstrap-migration/ | none |
| Key lifecycle and JWKS publication | tier 3 / evidenced-release-gated | pkgs/50-protocols/tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/jwks_service.py | current: ∅<br>target: ∅ | unit, conformance | compliance/evidence/tier3/key-lifecycle-jwks/ | none |
| Import/export portability | tier 3 / evidenced-release-gated | pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/portability.py | current: ∅<br>target: ∅ | unit, conformance | compliance/evidence/tier3/import-export-portability/ | none |
| Release bundle and signature verification | tier 3 / evidenced-release-gated | pkgs/60-runtime/tigrbl-auth-release-certification/src/tigrbl_auth_release_certification | current: ∅<br>target: ∅ | unit, security | compliance/evidence/tier3/release-bundle-signing/ | none |

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

