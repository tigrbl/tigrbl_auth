> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

# Target Reality Matrix

This matrix reconciles declared scope, current claims, owner modules, public surface state, test planning, and evidence planning.

## Target x Cell SSOT Entity Matrix

This compatibility projection maps each target row to the strongest current SSOT entities for each surface cell.

- authority: `.ssot/registry.json`, `.ssot/adr`, `.ssot/specs`
- machine_readable_companion: `docs/compliance/target_cell_ssot_entity_matrix.json`
- public_api_cell_projection: `docs/compliance/public_api_target_ssot_matrix.json`
- public_uix_cell_projection: `docs/compliance/public_uix_target_ssot_matrix.json`
- cell contents: strongest direct or adjacent current ADR, SPEC, and feature entities
- notation: `none` means no direct current SSOT entity was found for that exact cell

| Target | Admin API | Public API | Admin UIX | Public UIX |
|---|---|---|---|---|
| RFC 9110 HTTP Semantics | `spc:1060`, `spc:1061`, `feat:secure-default-baseline-admin-gate`, `feat:runtime-profile-configuration-contract` | `spc:1034-1043`, `spc:1060`, `spc:1061`, `feat:runtime-profile-configuration-contract` | `adr:1038`, `adr:1040`, `spc:1055`, `spc:1057`, `feat:uix-admin-console-shell` | `none` |
| RFC 9112 HTTP/1.1 | `none` | `none` | `none` | `none` |
| RFC 9113 HTTP/2 | `feat:cli-flag-hypercorn-http2` | `feat:cli-flag-hypercorn-http2` | `none` | `none` |
| RFC 9114 HTTP/3 | `none` | `none` | `none` | `none` |
| RFC 9000 QUIC | `none` | `none` | `none` | `none` |
| RFC 8446 TLS 1.3 | `spc:1060`, `spc:1061`, `feat:secure-default-baseline-admin-gate` | `spc:1034-1043`, `spc:1060`, `spc:1061` | `adr:1040`, `spc:1055`, `feat:uix-admin-auth-session` | `none` |
| OpenAPI 3.1 | `adr:1006`, `spc:1060`, `spc:1061`, `spc:1063`, `spc:1065`, `feat:target-openapi-3-1-3-2-compatible-public-contract`, `feat:openapi-contract-always-valid`, `feat:openapi-runtime-payload-deferred-to-tigrbl`, `feat:admin-gate-does-not-mutate-openapi-json` | `adr:1006`, `spc:1034-1043`, `spc:1061`, `spc:1063`, `spc:1065`, `feat:target-openapi-3-1-3-2-compatible-public-contract`, `feat:openapi-contract-always-valid`, `feat:openapi-runtime-payload-deferred-to-tigrbl` | `spc:1056`, `feat:uix-enterprise-readiness-dashboard`, `feat:uix-redacted-config-viewer` | `none` |
| JSON Schema 2020-12 | `spc:1063`, `spc:1065` | `spc:1034-1043`, `spc:1063`, `spc:1065` | `none` | `none` |
| RFC 9457 Problem Details | `spc:1060`, `spc:1061` | `spc:1034-1043`, `spc:1060`, `spc:1061` | `adr:1040`, `spc:1055`, `spc:1057`, `feat:uix-admin-console-shell` | `none` |
| JSON-RPC 2.0 | `spc:1060`, `spc:1061`, `feat:cli-flag-rpc`, `feat:secure-default-baseline-admin-gate` | `spc:1060`, `feat:cli-flag-rpc` | `adr:1039`, `spc:1057`, `spc:1058`, `spc:1059` | `none` |
| OpenRPC | `adr:1006`, `spc:1024`, `spc:1044-1049`, `spc:1064`, `spc:1065`, `feat:target-openrpc-1-4-x-admin-control-plane-contract`, `feat:openrpc-contract-always-valid`, `feat:openrpc-runtime-payload-deferred-to-tigrbl`, `feat:admin-gate-does-not-mutate-openrpc-json` | `adr:1006`, `spc:1064`, `spc:1065` | `adr:1039`, `spc:1055`, `spc:1056`, `spc:1057`, `spc:1058`, `spc:1059`, `feat:uix-admin-console-shell` | `none` |
| RFC 6749 OAuth 2.0 | `feat:target-rfc-6749`, `feat:flag-enable-rfc6749` | `feat:target-rfc-6749`, `feat:flag-enable-rfc6749`, `spc:1034-1043` | `spc:1055`, `spc:1056`, `feat:uix-admin-auth-session` | `none` |
| RFC 6750 Bearer Tokens | `feat:target-rfc-6750`, `feat:flag-enable-rfc6750`, `feat:flag-enable-rfc6750-form`, `feat:flag-enable-rfc6750-query` | `feat:target-rfc-6750`, `feat:flag-enable-rfc6750`, `feat:flag-enable-rfc6750-form`, `feat:flag-enable-rfc6750-query`, `spc:1034-1043` | `spc:1055`, `spc:1057`, `feat:uix-admin-auth-session`, `feat:uix-token-admin-view` | `none` |
| RFC 9700 OAuth Security BCP | `feat:target-rfc-9700`, `feat:flag-enable-rfc9700` | `feat:target-rfc-9700`, `feat:flag-enable-rfc9700`, `spc:1034`, `spc:1035` | `adr:1040`, `spc:1055` | `none` |
| RFC 7009 Token Revocation | `feat:target-rfc-7009`, `feat:route-revoke`, `feat:flag-enable-rfc7009` | `feat:target-rfc-7009`, `feat:route-revoke`, `feat:flag-enable-rfc7009`, `spc:1039-1043` | `spc:1057`, `spc:1058`, `feat:uix-token-admin-view`, `feat:uix-safe-mutation-revoke-token`, `feat:uix-safe-mutation-revoke-session`, `feat:uix-safe-mutation-revoke-consent` | `none` |
| RFC 7662 Token Introspection | `feat:target-rfc-7662`, `feat:route-introspect`, `feat:flag-enable-rfc7662` | `feat:target-rfc-7662`, `feat:route-introspect`, `feat:flag-enable-rfc7662`, `spc:1039-1043` | `spc:1056`, `spc:1057`, `feat:uix-token-admin-view` | `none` |
| RFC 8414 OAuth Metadata | `feat:target-rfc-8414`, `feat:route-well-known-oauth-authorization-server`, `feat:flag-enable-rfc8414` | `feat:target-rfc-8414`, `feat:route-well-known-oauth-authorization-server`, `feat:flag-enable-rfc8414`, `spc:1034-1043` | `spc:1056`, `feat:uix-enterprise-readiness-dashboard`, `feat:uix-redacted-config-viewer` | `none` |
| RFC 9207 Issuer Identification | `feat:target-rfc-9207`, `feat:flag-enable-rfc9207` | `feat:target-rfc-9207`, `feat:flag-enable-rfc9207`, `spc:1034-1043` | `spc:1056`, `feat:uix-enterprise-readiness-dashboard`, `feat:uix-redacted-config-viewer` | `none` |
| RFC 8705 OAuth mTLS | `feat:target-rfc-8705`, `feat:slice-mtls`, `feat:flag-enable-rfc8705`, `feat:cli-flag-enable-mtls` | `feat:target-rfc-8705`, `feat:slice-mtls`, `feat:flag-enable-rfc8705`, `spc:1034`, `spc:1039`, `spc:1040`, `spc:1042`, `spc:1043` | `adr:1040`, `spc:1055`, `spc:1056` | `none` |
| RFC 9449 DPoP | `feat:target-rfc-9449`, `feat:slice-dpop`, `feat:flag-enable-rfc9449` | `feat:target-rfc-9449`, `feat:slice-dpop`, `feat:flag-enable-rfc9449`, `spc:1036`, `spc:1037`, `spc:1042`, `spc:1043` | `adr:1040`, `spc:1055`, `spc:1056` | `none` |
| RFC 7515 JWS | `feat:target-rfc-7515`, `feat:flag-enable-rfc7515` | `feat:target-rfc-7515`, `feat:flag-enable-rfc7515` | `none` | `none` |
| RFC 7516 JWE | `feat:target-rfc-7516`, `feat:flag-enable-rfc7516` | `feat:target-rfc-7516`, `feat:flag-enable-rfc7516` | `none` | `none` |
| RFC 7517 JWK / JWKS | `spc:1002`, `spc:1005`, `spc:1009`, `spc:1013`, `spc:1017`, `feat:target-rfc-7517`, `feat:target-key-lifecycle-and-jwks-publication`, `feat:route-well-known-jwks-json`, `feat:rpc-jwks-show`, `feat:cli-verb-keys-publish-jwks`, `feat:cli-verb-keys-generate` | `spc:1002`, `spc:1005`, `spc:1009`, `spc:1013`, `spc:1017`, `feat:target-rfc-7517`, `feat:route-well-known-jwks-json` | `spc:1057`, `spc:1058`, `feat:uix-keys-jwks-admin-view`, `feat:uix-safe-mutation-publish-jwks`, `feat:uix-safe-mutation-rotate-key` | `none` |
| RFC 7518 JWA | `feat:target-rfc-7518`, `feat:flag-enable-rfc7518` | `feat:target-rfc-7518`, `feat:flag-enable-rfc7518` | `spc:1057`, `spc:1058`, `feat:uix-keys-jwks-admin-view`, `feat:uix-safe-mutation-rotate-key` | `none` |
| RFC 7519 JWT | `feat:target-rfc-7519`, `feat:flag-enable-rfc7519` | `feat:target-rfc-7519`, `feat:flag-enable-rfc7519` | `spc:1057`, `spc:1059`, `feat:uix-token-admin-view`, `feat:uix-policy-simulation` | `none` |
| RFC 9068 JWT Access Token Profile | `feat:target-rfc-9068`, `feat:flag-enable-rfc9068` | `feat:target-rfc-9068`, `feat:flag-enable-rfc9068` | `spc:1057`, `feat:uix-token-admin-view` | `none` |
| RFC 7591 Dynamic Client Registration | `feat:target-rfc-7591`, `feat:flag-enable-rfc7591` | `feat:target-rfc-7591`, `feat:flag-enable-rfc7591`, `spc:1034-1043` | `spc:1057`, `spc:1058`, `feat:uix-client-admin-view`, `feat:uix-safe-mutation-update-client-registration` | `none` |
| RFC 7592 Client Registration Management | `feat:target-rfc-7592`, `feat:flag-enable-rfc7592` | `feat:target-rfc-7592`, `feat:flag-enable-rfc7592` | `spc:1057`, `spc:1058`, `feat:uix-client-admin-view`, `feat:uix-safe-mutation-update-client-registration` | `none` |
| OIDC Discovery 1.0 | `feat:target-oidc-discovery-1-0` | `feat:target-oidc-discovery-1-0`, `spc:1034-1043` | `spc:1056`, `feat:uix-enterprise-readiness-dashboard`, `feat:uix-redacted-config-viewer` | `none` |
| OIDC Dynamic Client Registration 1.0 | `feat:target-rfc-7591`, `feat:target-rfc-7592` | `feat:target-rfc-7591`, `feat:target-rfc-7592` | `spc:1057`, `spc:1058`, `feat:uix-client-admin-view`, `feat:uix-safe-mutation-update-client-registration` | `none` |
| RFC 7643 SCIM Core Schema | `adr:1052`, `spc:1068`, `spc:1072`, `feat:f33-scim-provisioning` | `none` | `adr:1052`, `spc:1072` | `none` |
| RFC 7644 SCIM Protocol | `adr:1052`, `spc:1068`, `spc:1072`, `feat:f33-scim-provisioning` | `none` | `adr:1052`, `spc:1072` | `none` |
| OIDC RP-Initiated Logout 1.0 | `feat:target-oidc-rp-initiated-logout`, `feat:route-logout` | `feat:target-oidc-rp-initiated-logout`, `feat:route-logout`, `spc:1034`, `spc:1036`, `spc:1037`, `spc:1039`, `spc:1040` | `spc:1055`, `spc:1057`, `feat:uix-admin-auth-session`, `feat:uix-session-admin-view` | `none` |
| OIDC Front-Channel Logout 1.0 | `feat:target-oidc-front-channel-logout` | `feat:target-oidc-front-channel-logout`, `spc:1034`, `spc:1036`, `spc:1037` | `spc:1055`, `spc:1057`, `feat:uix-admin-auth-session`, `feat:uix-session-admin-view` | `none` |
| OIDC Back-Channel Logout 1.0 | `feat:target-oidc-back-channel-logout` | `feat:target-oidc-back-channel-logout`, `spc:1034`, `spc:1036`, `spc:1037` | `spc:1055`, `spc:1057`, `feat:uix-admin-auth-session`, `feat:uix-session-admin-view` | `none` |
| NIST SP 800-53 | `adr:1051`, `adr:1052`, `spc:1070`, `spc:1071`, `spc:1072` | `adr:1051`, `spc:1070`, `spc:1071` | `adr:1040`, `adr:1051`, `adr:1052` | `none` |
| NIST SP 800-63 | `spc:1066`, `spc:1067`, `feat:target-nist-sp-800-63b-4-profile`, `feat:target-nist-sp-800-63c-4-profile`, `feat:profile-nist-sp-800-63b-4`, `feat:profile-nist-sp-800-63c-4` | `spc:1066`, `spc:1067`, `feat:target-nist-sp-800-63b-4-profile`, `feat:target-nist-sp-800-63c-4-profile` | `adr:1051`, `adr:1052` | `none` |
| NIST SP 800-218 SSDF | `none` | `none` | `none` | `none` |
| SLSA | `none` | `none` | `none` | `none` |
| in-toto | `none` | `none` | `none` | `none` |
| Sigstore | `none` | `none` | `none` | `none` |
| SPDX | `none` | `none` | `none` | `none` |
| CycloneDX | `none` | `none` | `none` | `none` |
| Admin API Profile Spec | `spc:1060`, `spc:1061`, `spc:1064`, `feat:target-openrpc-1-4-x-admin-control-plane-contract`, `feat:secure-default-baseline-admin-gate`, `feat:runtime-profile-configuration-contract` | `none` | `adr:1038`, `spc:1055`, `spc:1057`, `spc:1058`, `spc:1059`, all `feat:uix-*` admin rows | `none` |
| Deployment Profile Spec | `spc:1061`, `feat:runtime-profile-configuration-contract`, `feat:profile-baseline-development` | `spc:1061`, `feat:runtime-profile-configuration-contract`, `feat:profile-baseline-development` | `spc:1055`, `spc:1056`, `feat:uix-admin-console-shell`, `feat:uix-enterprise-readiness-dashboard`, `feat:uix-redacted-config-viewer`, `feat:uix-tenant-profile-selector` | `none` |
| Tenant Isolation Spec | `none` | `none` | `spc:1055`, `spc:1057`, `feat:uix-tenant-profile-selector`, `feat:uix-tenant-admin-view` | `none` |
| Policy Administration Spec | `spc:1059`, `spc:1070` | `none` | `spc:1059`, `feat:uix-rbac-administration`, `feat:uix-abac-administration`, `feat:uix-policy-simulation` | `none` |
| Key Lifecycle Spec | `spc:1002`, `spc:1005`, `spc:1009`, `spc:1013`, `spc:1017`, `feat:target-key-lifecycle-and-jwks-publication` | `spc:1002`, `spc:1005`, `spc:1009`, `spc:1013`, `spc:1017`, `feat:target-key-lifecycle-and-jwks-publication` | `spc:1057`, `spc:1058`, `feat:uix-keys-jwks-admin-view`, `feat:uix-safe-mutation-rotate-key`, `feat:uix-safe-mutation-publish-jwks` | `none` |
| Audit Event Schema | `feat:rpc-audit-list`, `feat:rpc-audit-export` | `none` | `adr:1040`, `spc:1057`, `feat:uix-audit-admin-view` | `none` |
| Client Policy Spec | `none` | `none` | `spc:1057`, `spc:1058`, `feat:uix-client-admin-view`, `feat:uix-safe-mutation-update-client-registration`, `feat:uix-safe-mutation-toggle-client` | `none` |
| Resource Contract Spec | `adr:1006`, `spc:1061`, `spc:1064`, `spc:1065`, `feat:target-openrpc-1-4-x-admin-control-plane-contract`, `feat:openrpc-contract-always-valid`, `feat:openrpc-runtime-payload-deferred-to-tigrbl` | `adr:1006`, `spc:1034-1043`, `spc:1063`, `spc:1065`, `feat:target-openapi-3-1-3-2-compatible-public-contract`, `feat:openapi-contract-always-valid` | `adr:1039`, `spc:1057`, all `feat:uix-*-admin-view` rows | `none` |

## baseline-certifiable-now

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| RFC 6749 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rfc6749.py<br>tigrbl_auth/standards/oauth2/rfc6749_token.py | current: /authorize, /token<br>target: /authorize, /token | conformance, integration, interop | compliance/evidence/tier3/oauth2-core/ | none |
| RFC 6750 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rfc6750.py | current: /token, /userinfo, /introspect<br>target: /token, /userinfo, /introspect | conformance, integration, interop | compliance/evidence/tier3/bearer/ | none |
| RFC 7636 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rfc7636_pkce.py | current: /authorize, /token<br>target: /authorize, /token | conformance, integration, unit, interop | compliance/evidence/tier3/pkce/ | none |
| RFC 8414 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rfc8414.py<br>tigrbl_auth/standards/oauth2/rfc8414_metadata.py | current: /.well-known/oauth-authorization-server<br>target: /.well-known/oauth-authorization-server | conformance, integration | compliance/evidence/tier3/discovery/ | none |
| RFC 8615 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/http/well_known.py | current: /.well-known/openid-configuration, /.well-known/oauth-authorization-server, /.well-known/jwks.json, /.well-known/oauth-protected-resource<br>target: /.well-known/openid-configuration, /.well-known/oauth-authorization-server, /.well-known/jwks.json, /.well-known/oauth-protected-resource | conformance, integration, unit | compliance/evidence/tier3/well-known/ | none |
| RFC 7515 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/jose/rfc7515.py | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jose/ | none |
| RFC 7516 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/jose/rfc7516.py<br>tigrbl_auth/standards/oidc/id_token.py | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jwe/ | none |
| RFC 7517 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/jose/rfc7517.py | current: /.well-known/jwks.json<br>target: /.well-known/jwks.json | conformance, unit | compliance/evidence/tier3/jwks/ | none |
| RFC 7518 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/jose/rfc7518.py | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jose/ | none |
| RFC 7519 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/jose/rfc7519.py | current: ∅<br>target: ∅ | conformance, unit | compliance/evidence/tier3/jwt/ | none |
| RFC 6265 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/http/cookies.py<br>tigrbl_auth/standards/oidc/session_mgmt.py | current: /login, /authorize, /logout<br>target: /login, /authorize, /logout | conformance, integration, negative | compliance/evidence/tier3/cookies/ | none |
| OIDC Core 1.0 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/core.py<br>tigrbl_auth/standards/oidc/id_token.py | current: ∅<br>target: ∅ | conformance, integration | compliance/evidence/tier3/oidc-core/ | none |
| OIDC Discovery 1.0 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/discovery.py | current: /.well-known/openid-configuration<br>target: /.well-known/openid-configuration | conformance, integration, interop | compliance/evidence/tier3/discovery/ | none |
| OIDC Session Management | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/session_mgmt.py<br>tigrbl_auth/standards/http/cookies.py | current: /login, /authorize, /logout<br>target: /login, /authorize, /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-session-management/ | none |
| OpenAPI 3.1 / 3.2 compatible public contract | tier 3 / generated-live-from-deployment-metadata | tigrbl_auth/api/rest<br>tigrbl_auth/api/surfaces.py | current: ∅<br>target: ∅ | e2e, integration, unit | compliance/evidence/tier3/contracts/openapi/ | none |

## production-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| RFC 7009 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/revocation.py<br>tigrbl_auth/api/rest/routers/revoke.py | current: /revoke<br>target: /revoke | conformance, integration, unit | compliance/evidence/tier3/revocation/ | none |
| RFC 7591 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/dynamic_client_registration.py<br>tigrbl_auth/api/rest/routers/register.py | current: /register<br>target: /register | conformance, integration, unit | compliance/evidence/tier3/client-registration/ | none |
| RFC 7592 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/client_registration_management.py<br>tigrbl_auth/tables/client_registration.py | current: /register/{client_id}<br>target: /register/{client_id} | unit, conformance, integration | compliance/evidence/tier3/client-registration-management/ | none |
| RFC 7662 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/introspection.py<br>tigrbl_auth/services/persistence.py | current: /introspect<br>target: /introspect | conformance, integration, unit | compliance/evidence/tier3/introspection/ | none |
| RFC 8252 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/native_apps.py<br>tigrbl_auth/tables/client.py | current: /authorize, /token, /register, /register/{client_id}<br>target: /authorize, /token, /register, /register/{client_id} | unit, conformance, interop | compliance/evidence/tier3/native-apps/ | none |
| RFC 9068 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/jwt_access_tokens.py<br>tigrbl_auth/services/token_service.py | current: /login, /token, /token/exchange<br>target: /login, /token, /token/exchange | conformance, integration, unit, interop | compliance/evidence/tier3/jwt-access-token-profile/ | none |
| RFC 9207 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/issuer_identification.py<br>tigrbl_auth/config/deployment.py | current: /authorize, /.well-known/openid-configuration<br>target: /authorize, /.well-known/openid-configuration | conformance, integration, unit | compliance/evidence/tier3/issuer-identification/ | none |
| RFC 7521 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/assertion_framework.py<br>tigrbl_auth/ops/token.py | current: /token<br>target: /token | conformance, unit | compliance/evidence/tier3/assertion-framework/ | none |
| RFC 7523 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/jwt_client_auth.py<br>tigrbl_auth/ops/token.py | current: /token, /register, /register/{client_id}<br>target: /token, /register, /register/{client_id} | conformance, unit | compliance/evidence/tier3/jwt-client-auth/ | none |
| RFC 9728 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rfc9728.py | current: /.well-known/oauth-protected-resource<br>target: /.well-known/oauth-protected-resource | conformance, integration, unit, interop | compliance/evidence/tier3/protected-resource-metadata/ | none |
| OIDC UserInfo | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/userinfo.py | current: /userinfo<br>target: /userinfo | conformance, integration, unit | compliance/evidence/tier3/oidc-userinfo/ | none |
| OIDC RP-Initiated Logout | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/rp_initiated_logout.py<br>tigrbl_auth/api/rest/routers/logout.py | current: /logout<br>target: /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-rp-initiated-logout/ | none |
| OpenRPC 1.4.x admin/control-plane contract | tier 3 / implementation-backed-generated-from-rpc-registry | tigrbl_auth/api/rpc/__init__.py<br>tigrbl_auth/api/rpc/registry.py | current: /rpc<br>target: /rpc | e2e, unit | compliance/evidence/tier3/contracts/openrpc/ | none |

## hardening-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| RFC 8628 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/device_authorization.py<br>tigrbl_auth/api/rest/routers/device_authorization.py | current: /device_authorization<br>target: /device_authorization | unit, conformance, integration, interop | compliance/evidence/tier3/device-flow/ | none |
| RFC 8693 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/token_exchange.py<br>tigrbl_auth/ops/token.py | current: /token/exchange<br>target: /token/exchange | unit, conformance, integration, interop | compliance/evidence/tier3/token-exchange/ | none |
| RFC 8705 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/mtls.py<br>tigrbl_auth/standards/oauth2/rfc9700.py | current: /token, /token/exchange<br>target: /token, /token/exchange | conformance, integration, unit, interop | compliance/evidence/tier3/mtls/ | none |
| RFC 8707 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/resource_indicators.py<br>tigrbl_auth/ops/authorize.py | current: /authorize, /token, /device_authorization, /par, /token/exchange<br>target: /authorize, /token, /device_authorization, /par, /token/exchange | unit, conformance, integration | compliance/evidence/tier3/resource-indicators/ | none |
| RFC 9101 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/jar.py<br>tigrbl_auth/ops/authorize.py | current: /authorize, /par<br>target: /authorize, /par | conformance, integration, unit, interop | compliance/evidence/tier3/jar/ | none |
| RFC 9126 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/par.py<br>tigrbl_auth/api/rest/routers/par.py | current: /par<br>target: /par | conformance, integration, unit, interop | compliance/evidence/tier3/par/ | none |
| RFC 9396 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rar.py<br>tigrbl_auth/ops/authorize.py | current: /authorize, /par<br>target: /authorize, /par | conformance, integration, unit, interop | compliance/evidence/tier3/rar/ | none |
| RFC 9449 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/dpop.py<br>tigrbl_auth/standards/oauth2/rfc9700.py | current: /token, /token/exchange<br>target: /token, /token/exchange | conformance, integration, unit, interop | compliance/evidence/tier3/dpop/ | none |
| RFC 9700 | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oauth2/rfc9700.py<br>tigrbl_auth/ops/authorize.py | current: /authorize, /token, /.well-known/openid-configuration<br>target: /authorize, /token, /.well-known/openid-configuration | conformance, integration, negative, unit | compliance/evidence/tier3/security-bcp/ | none |
| OIDC Front-Channel Logout | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/frontchannel_logout.py<br>tigrbl_auth/standards/oidc/rp_initiated_logout.py | current: /logout<br>target: /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-frontchannel-logout/ | none |
| OIDC Back-Channel Logout | tier 3 / evidenced-release-gated | tigrbl_auth/standards/oidc/backchannel_logout.py<br>tigrbl_auth/standards/oidc/rp_initiated_logout.py | current: /logout<br>target: /logout | conformance, integration, negative, unit | compliance/evidence/tier3/oidc-backchannel-logout/ | none |

## runtime-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| ASGI 3 application package | tier 3 / evidenced-release-gated | tigrbl_auth/api/app.py<br>tigrbl_auth/app.py | current: ∅<br>target: ∅ | integration, unit, conformance | compliance/evidence/tier3/asgi-application/ | none |
| Runner profile: Uvicorn | tier 3 / evidenced-release-gated | tigrbl_auth/api/app.py<br>tigrbl_auth/gateway.py | current: ∅<br>target: ∅ | unit, integration, conformance | compliance/evidence/tier3/runner-uvicorn/ | none |
| Runner profile: Hypercorn | tier 3 / evidenced-release-gated | tigrbl_auth/api/app.py<br>tigrbl_auth/gateway.py | current: ∅<br>target: ∅ | unit, integration, conformance | compliance/evidence/tier3/runner-hypercorn/ | none |
| Runner profile: Tigrcorn | tier 3 / evidenced-release-gated | tigrbl_auth/api/app.py<br>tigrbl_auth/gateway.py | current: ∅<br>target: ∅ | unit, integration, conformance | compliance/evidence/tier3/runner-tigrcorn/ | none |

## operator-completion-required

| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |
|---|---|---|---|---|---|---|
| CLI operator surface | tier 3 / evidenced-release-gated | tigrbl_auth/cli/main.py<br>tigrbl_auth/cli/metadata.py | current: ∅<br>target: ∅ | unit, conformance | compliance/evidence/tier3/cli-operator-surface/ | none |
| Bootstrap and migration lifecycle | tier 3 / evidenced-release-gated | tigrbl_auth/cli/main.py<br>tigrbl_auth/cli/metadata.py | current: ∅<br>target: ∅ | unit, e2e, conformance | compliance/evidence/tier3/bootstrap-migration/ | none |
| Key lifecycle and JWKS publication | tier 3 / evidenced-release-gated | tigrbl_auth/cli/metadata.py<br>tigrbl_auth/cli/handlers.py | current: ∅<br>target: ∅ | unit, conformance | compliance/evidence/tier3/key-lifecycle-jwks/ | none |
| Import/export portability | tier 3 / evidenced-release-gated | tigrbl_auth/cli/metadata.py<br>tigrbl_auth/cli/handlers.py | current: ∅<br>target: ∅ | unit, conformance | compliance/evidence/tier3/import-export-portability/ | none |
| Release bundle and signature verification | tier 3 / evidenced-release-gated | tigrbl_auth/cli/reports.py<br>tigrbl_auth/cli/handlers.py | current: ∅<br>target: ∅ | unit, security | compliance/evidence/tier3/release-bundle-signing/ | none |

## out-of-scope/deferred

| Target | Kind | Reason |
|---|---|---|
| RFC 7800 | extension-quarantine | Optional hardening extension not yet promoted into the certified core boundary. |
| RFC 7952 | extension-quarantine | Outside the default OAuth 2.0 / OIDC auth-server certification boundary. |
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

