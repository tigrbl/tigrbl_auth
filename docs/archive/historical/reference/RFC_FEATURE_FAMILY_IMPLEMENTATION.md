> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# RFC_FEATURE_FAMILY_IMPLEMENTATION

This document records the RFC-family runtime checkpoint implementation state for the retained production and hardening RFC families. Each section identifies the implementation note, owned runtime modules, endpoint/schema mapping, profile gating, test mapping, and evidence recipe.

## RFC 7009 — Token Revocation

- Implementation note: canonical revocation surface remains `/revoke` with durable revocation records and audit events
- Owned runtime modules: `tigrbl_auth/api/rest/routers/revoke.py`, `tigrbl_auth/ops/revoke.py`, `tigrbl_auth/tables/revoked_token.py`, `tigrbl_auth/services/persistence.py`
- Endpoint and schema mapping: `POST /revoke`; response schema `RevocationOut`
- Profile gating: production, hardening
- Tests: `tests/conformance/production/test_rfc7009_revocation.py`, `tests/unit/test_3_public_route_contracts.py`
- Evidence recipe: `compliance/evidence/tier3/revocation/`

## RFC 7591 — Dynamic Client Registration

- Implementation note: live client creation with durable registration metadata and logout metadata capture
- Owned runtime modules: `tigrbl_auth/api/rest/routers/register.py`, `tigrbl_auth/ops/register.py`, `tigrbl_auth/tables/client.py`, `tigrbl_auth/tables/client_registration.py`
- Endpoint and schema mapping: `POST /register`; request `DynamicClientRegistrationIn`; response `DynamicClientRegistrationOut`
- Profile gating: production, hardening
- Tests: `tests/conformance/production/test_rfc7591_dynamic_client_registration.py`, `tests/unit/test_3_public_route_contracts.py`
- Evidence recipe: `compliance/evidence/tier3/client-registration/`

## RFC 7592 — Dynamic Client Management

- Implementation note: management plane moved from planned to live with authenticated GET/PUT/DELETE semantics
- Owned runtime modules: `tigrbl_auth/standards/oauth2/client_registration_management.py`, `tigrbl_auth/api/rest/routers/register.py`, `tigrbl_auth/ops/register.py`, `tigrbl_auth/tables/client_registration.py`
- Endpoint and schema mapping: `GET|PUT|DELETE /register/{client_id}`; request `DynamicClientRegistrationManagementIn`; response `DynamicClientRegistrationOut` or delete status payload
- Profile gating: hardening, peer-claim; visible in production contracts where hardening-capable management is enabled by deployment
- Tests: `tests/conformance/hardening/test_rfc7592_client_registration_management.py`, `tests/unit/test_RFC_FAMILY_RUNTIME_advanced_surface_contracts.py`
- Evidence recipe: `compliance/evidence/tier3/client-registration-management/`

## RFC 7662 — Token Introspection

- Implementation note: durable token-record-backed introspection remains active
- Owned runtime modules: `tigrbl_auth/standards/oauth2/introspection.py`, `tigrbl_auth/tables/token_record.py`, `tigrbl_auth/services/persistence.py`
- Endpoint and schema mapping: `POST /introspect`; response `IntrospectOut`
- Profile gating: production, hardening
- Tests: `tests/conformance/production/test_rfc7662_token_introspection.py`
- Evidence recipe: `compliance/evidence/tier3/introspection/`

## RFC 9068 — JWT Access Token Profile

- Implementation note: the token service now injects and validates JWT access-token profile claims during issuance and decode paths
- Owned runtime modules: `tigrbl_auth/standards/oauth2/jwt_access_tokens.py`, `tigrbl_auth/services/token_service.py`, `tigrbl_auth/ops/login.py`, `tigrbl_auth/ops/token.py`, `tigrbl_auth/standards/oauth2/token_exchange.py`
- Endpoint and schema mapping: access-token issuance on `/login`, `/token`, and `/token/exchange`; no new public path
- Profile gating: production, hardening, peer-claim
- Tests: `tests/conformance/production/test_rfc9068_jwt_profile.py`, `tests/unit/test_RFC_FAMILY_RUNTIME_advanced_surface_contracts.py`
- Evidence recipe: `compliance/evidence/tier3/jwt-access-token-profile/`

## RFC 9126 — Pushed Authorization Requests

- Implementation note: PAR now persists normalized request-object, authorization-details, and resource inputs
- Owned runtime modules: `tigrbl_auth/standards/oauth2/par.py`, `tigrbl_auth/api/rest/routers/par.py`, `tigrbl_auth/ops/par.py`, `tigrbl_auth/tables/pushed_authorization_request.py`
- Endpoint and schema mapping: `POST /par`; request `PushedAuthorizationRequestIn`; response `PushedAuthorizationResponse`
- Profile gating: hardening, peer-claim
- Tests: `tests/conformance/hardening/test_rfc9126_par.py`, `tests/unit/test_3_public_route_contracts.py`
- Evidence recipe: `compliance/evidence/tier3/par/`

## RFC 9101 — JWT Secured Authorization Requests

- Implementation note: signed request objects are now parsed in `/authorize` and `/par` using the supported signing profile for this checkpoint
- Owned runtime modules: `tigrbl_auth/standards/oauth2/jar.py`, `tigrbl_auth/ops/authorize.py`, `tigrbl_auth/ops/par.py`
- Endpoint and schema mapping: request-object support on `/authorize` and `/par`; OpenAPI documents the `request` parameter
- Profile gating: hardening, peer-claim
- Tests: `tests/conformance/hardening/test_rfc9101_jar.py`, `tests/unit/test_RFC_FAMILY_RUNTIME_advanced_surface_contracts.py`
- Evidence recipe: `compliance/evidence/tier3/jar/`

## RFC 9396 — Rich Authorization Requests

- Implementation note: `authorization_details` is normalized across direct and pushed authorization request paths
- Owned runtime modules: `tigrbl_auth/standards/oauth2/rar.py`, `tigrbl_auth/ops/authorize.py`, `tigrbl_auth/ops/par.py`
- Endpoint and schema mapping: `/authorize` and `/par`; OpenAPI documents `authorization_details`
- Profile gating: hardening, peer-claim
- Tests: `tests/conformance/hardening/test_rfc9396_rar.py`, `tests/unit/test_RFC_FAMILY_RUNTIME_advanced_surface_contracts.py`
- Evidence recipe: `compliance/evidence/tier3/rar/`

## RFC 8707 — Resource Indicators

- Implementation note: resource indicators now propagate through authorization, device, token, PAR, and token-exchange flows and influence resulting audience selection
- Owned runtime modules: `tigrbl_auth/standards/oauth2/resource_indicators.py`, `tigrbl_auth/ops/authorize.py`, `tigrbl_auth/ops/token.py`, `tigrbl_auth/ops/device_authorization.py`, `tigrbl_auth/ops/par.py`, `tigrbl_auth/standards/oauth2/token_exchange.py`
- Endpoint and schema mapping: `/authorize`, `/token`, `/device_authorization`, `/par`, `/token/exchange`
- Profile gating: hardening, peer-claim
- Tests: `tests/conformance/hardening/test_rfc8707_resource_indicators.py`, `tests/unit/test_RFC_FAMILY_RUNTIME_advanced_surface_contracts.py`
- Evidence recipe: `compliance/evidence/tier3/resource-indicators/`

## RFC 8705 — OAuth mTLS

- Implementation note: this checkpoint implements gateway-mediated certificate-thumbprint binding and validation rather than an all-in-one socket-terminating TLS stack inside the package
- Owned runtime modules: `tigrbl_auth/standards/oauth2/mtls.py`, `tigrbl_auth/standards/oauth2/rfc9700.py`, `tigrbl_auth/ops/token.py`, `tigrbl_auth/standards/oauth2/token_exchange.py`, `tigrbl_auth/services/token_service.py`
- Endpoint and schema mapping: `/token`, `/token/exchange`; OpenAPI documents `X-Client-Cert-SHA256` for the supported deployment profile
- Profile gating: hardening, peer-claim
- Tests: `tests/conformance/hardening/test_rfc8705_mtls.py`, `tests/unit/test_RFC_FAMILY_RUNTIME_advanced_surface_contracts.py`
- Evidence recipe: `compliance/evidence/tier3/mtls/`

## RFC 9449 — DPoP

- Implementation note: DPoP proof verification is active in token and token-exchange flows and is reflected in hardening discovery metadata and contracts
- Owned runtime modules: `tigrbl_auth/standards/oauth2/dpop.py`, `tigrbl_auth/standards/oauth2/rfc9700.py`, `tigrbl_auth/ops/token.py`, `tigrbl_auth/standards/oauth2/token_exchange.py`
- Endpoint and schema mapping: `/token`, `/token/exchange`; OpenAPI documents `DPoP` request headers
- Profile gating: hardening, peer-claim
- Tests: `tests/conformance/hardening/test_rfc9449_dpop.py`, `tests/unit/test_RFC_FAMILY_RUNTIME_advanced_surface_contracts.py`
- Evidence recipe: `compliance/evidence/tier3/dpop/`

## RFC 8693 — Token Exchange

- Implementation note: exchanged access tokens now honor resource/audience selection and sender-constrained issuance
- Owned runtime modules: `tigrbl_auth/standards/oauth2/token_exchange.py`, `tigrbl_auth/services/token_service.py`
- Endpoint and schema mapping: `POST /token/exchange`; token-exchange form schema documented in OpenAPI
- Profile gating: hardening, peer-claim
- Tests: `tests/conformance/hardening/test_rfc8693_token_exchange.py`, `tests/unit/test_3_public_route_contracts.py`
- Evidence recipe: `compliance/evidence/tier3/token-exchange/`

## RFC 8252 — Native Apps

- Implementation note: native redirect URIs and PKCE guardrails are enforced during registration and authorization
- Owned runtime modules: `tigrbl_auth/standards/oauth2/native_apps.py`, `tigrbl_auth/tables/client.py`, `tigrbl_auth/ops/register.py`, `tigrbl_auth/ops/authorize.py`
- Endpoint and schema mapping: `/register`, `/register/{client_id}`, `/authorize`, `/token`; validation occurs within existing request models and query/form inputs
- Profile gating: production, hardening, peer-claim
- Tests: `tests/conformance/production/test_rfc8252_native_apps.py`
- Evidence recipe: `compliance/evidence/tier3/native-apps/`

## RFC 8628 — Device Authorization

- Implementation note: device authorization remains mounted and now participates in resource-indicator-aware audience selection
- Owned runtime modules: `tigrbl_auth/standards/oauth2/device_authorization.py`, `tigrbl_auth/api/rest/routers/device_authorization.py`, `tigrbl_auth/ops/device_authorization.py`, `tigrbl_auth/tables/device_code.py`
- Endpoint and schema mapping: `POST /device_authorization`; request `DeviceAuthorizationIn`; response `DeviceAuthorizationOut`
- Profile gating: hardening, peer-claim
- Tests: `tests/conformance/hardening/test_rfc8628_device_authorization.py`, `tests/unit/test_3_public_route_contracts.py`
- Evidence recipe: `compliance/evidence/tier3/device-flow/`

## RFC 9728 — Protected Resource Metadata

- Implementation note: protected-resource metadata remains active and aligned to deployment profiles
- Owned runtime modules: `tigrbl_auth/standards/oauth2/protected_resource_metadata.py`, `tigrbl_auth/standards/oidc/discovery_metadata.py`, `tigrbl_auth/cli/artifacts.py`
- Endpoint and schema mapping: `GET /.well-known/oauth-protected-resource`
- Profile gating: production, hardening, peer-claim
- Tests: `tests/conformance/production/test_rfc9728_protected_resource_metadata.py`
- Evidence recipe: `compliance/evidence/tier3/protected-resource-metadata/`

## Current honest status

This RFC-family runtime checkpoint implementation matrix records that the retained RFC families are now implementation-backed and mapped through routes, contracts, tests, and evidence placeholders. It does **not** claim that all of them are already Tier 3/Tier 4 promoted or certification-grade complete across every deployment mode.
