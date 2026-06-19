# PUBLIC_ROUTE_SURFACE

## Summary

This checkpoint completes the missing canonical public auth routes required by
public-route checkpoint for the authoritative release path.

The public route plane is now owned by explicit route modules under
`pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/rest/routers/`, with
protocol operation logic in the split OAuth/OIDC packages, table-backed schema
ownership in `pkgs/20-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/`,
and contract publication through the OpenAPI generation pipeline.

## Canonical route ownership

| Route | Profiles | Router | Operation | Primary schema(s) | Persistence / owner targets |
|---|---|---|---|---|---|
| `/login` | baseline, production, hardening | `pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/rest/routers/login.py` | `pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/ops/login.py` | `CredsIn`, `TokenPair` | `AuthSession`, `TokenRecord` |
| `/authorize` | baseline, production, hardening | `pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/rest/routers/authorize.py` | `pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/ops/authorize.py` | query surface | `AuthCode`, `AuthSession`, `Consent` |
| `/token` | baseline, production, hardening | `pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/rest/routers/token.py` | `pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/ops/token.py` | `TokenPair`, grant forms | `TokenRecord`, `AuthCode`, `DeviceCode` |
| `/userinfo` | production, hardening | standards include | OIDC owner surface | OIDC userinfo schemas | token/introspection backing |
| `/register` | production, hardening | `pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/rest/routers/register.py` | `pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/ops/registration_runtime.py` | `DynamicClientRegistrationIn`, `DynamicClientRegistrationOut` | `Client`, `ClientRegistration`, `AuditEvent` |
| `/register/{client_id}` | production, hardening | `pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/rest/routers/register.py` | `pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/ops/registration_runtime.py` | `DynamicClientRegistrationManagementIn`, `DynamicClientRegistrationOut`, delete status payload | `Client`, `ClientRegistration`, `AuditEvent` |
| `/revoke` | production, hardening | `pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/rest/routers/revoke.py` | `pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/ops/revoke.py` | `RevocationOut` | `RevokedToken`, `TokenRecord`, `AuditEvent` |
| `/logout` | production, hardening | `pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/rest/routers/logout.py` | `pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/ops/logout.py` | `LogoutIn`, `LogoutOut` | `AuthSession`, `LogoutState`, `AuditEvent` |
| `/introspect` | production, hardening | standards include | RFC 7662 owner surface | `IntrospectOut` | `TokenRecord`, `RevokedToken` |
| `/device_authorization` | hardening | `pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/rest/routers/device_authorization.py` | `pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/ops/device_authorization.py` | `DeviceAuthorizationIn`, `DeviceAuthorizationOut` | `DeviceCode`, `AuditEvent` |
| `/par` | hardening | `pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/rest/routers/par.py` | `pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/ops/par.py` | `PushedAuthorizationRequestIn`, `PushedAuthorizationResponse` | `PushedAuthorizationRequest`, `AuditEvent` |
| `/token/exchange` | hardening | standards include | RFC 8693 owner surface | form surface | token service / token lifecycle |
| discovery + JWKS | baseline, production, hardening | standards includes | OIDC / RFC 8414 / RFC 9728 owner surfaces | discovery docs | deployment-aware metadata |

## Canonical route policy

- `/revoke` is the canonical RFC 7009 revocation path for the certified release
  path.
- `/revoked_tokens/revoke` is retained only as a legacy compatibility alias
  outside the canonical certification surface.
- `/register`, `/register/{client_id}`, `/revoke`, and `/logout` are production-visible.
- `/device_authorization`, `/par`, and `/token/exchange` are hardening-visible.
- Discovery metadata and OpenAPI generation must only publish routes active in
  the effective deployment profile.

## Profile-effective route sets

### Baseline

- `/login`
- `/authorize`
- `/token`
- `/.well-known/openid-configuration`
- `/.well-known/oauth-authorization-server`
- `/.well-known/jwks.json`

### Production

- baseline routes
- `/userinfo`
- `/register`
- `/register/{client_id}`
- `/revoke`
- `/logout`
- `/introspect`
- `/.well-known/oauth-protected-resource`

### Hardening

- production routes
- `/device_authorization`
- `/par`
- `/token/exchange`

## Test and contract mapping

public-route checkpoint adds contract-visible checks for the canonical route set:

- `tests/unit/test_public_route_contracts.py`
- `tests/conformance/production/test_oidc_rp_initiated_logout.py`

Expanded RFC-targeted conformance coverage is now mapped for:

- RFC 7009
- RFC 7591
- RFC 7592
- RFC 8252
- RFC 8707
- RFC 9068
- RFC 9101
- RFC 9396
- RFC 9449
- RFC 7662
- RFC 8628
- RFC 8693
- RFC 9126
- OIDC RP-Initiated Logout

## Honest status

The public-route plane now includes the public-route checkpoint canonical route inventory together with the RFC-family runtime checkpoint advanced authorization and management surfaces required by the retained production and hardening RFC families.

It still does **not** by itself make the repository certifiably fully featured or certifiably fully RFC/spec compliant across the full declared certification boundary. Remaining blockers are now concentrated in evidence promotion, peer validation, release attestation, and broader certification-grade interop breadth.


## browser-session checkpoint browser/logout semantics layered onto the public route plane

The browser-session checkpoint checkpoint keeps the public-route checkpoint route inventory intact and deepens the browser-facing semantics behind those routes:

- `/login` now establishes a durable browser session and issues an opaque RFC 6265 cookie
- `/authorize` resolves browser sessions through the domain-owned cookie subsystem and emits `session_state`
- `/logout` now validates registered post-logout redirect URIs, clears the opaque cookie, and returns or persists logout fanout metadata
- `/register` now accepts `post_logout_redirect_uris`, `frontchannel_logout_uri`, and `backchannel_logout_uri` metadata used by logout planning

This still does not make the package fully certifiable, but it makes the browser/logout behavior materially more implementation-backed and observable.


## capability-wiring checkpoint executable surface registry

The route inventory above is now driven by the split-package deployment and
surface registries in
`pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/` and mounted through
`pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/api/surfaces.py`.

That registry is the authoritative source for:

- profile-specific mounted routes
- profile-specific OpenAPI paths
- discovery snapshot publication
- contract-sync and modularity verification

The practical effect is that public route enablement is no longer split between
a hand-maintained contract list and separate plugin/app conditional mounting
logic. The same capability identifiers now drive both.


## Target/profile truth addendum — 2026-03-27

The retained target/profile truth for the three previously mismatched RFCs is now normalized across the deployment resolver, declared claims, target buckets, and surface manifests:

- `RFC 7516` is treated as a **baseline+** target. It has **no standalone public route**; instead it is activated as JOSE/JWE helper support in the baseline, production, and hardening profiles. Discovery encryption metadata is still conditional on `enable_id_token_encryption`.
- `RFC 7592` is treated as a **production+** target and is surfaced by `GET/PUT/DELETE /register/{client_id}`.
- `RFC 9207` is treated as a **production+** target and is surfaced through shared authorization/discovery semantics on `/authorize` and `/.well-known/openid-configuration`.

This target/profile normalization is an alignment-only truth update. It does not by itself close the remaining runtime, validated-evidence, migration-portability, or Tier 4 peer-validation blockers.
