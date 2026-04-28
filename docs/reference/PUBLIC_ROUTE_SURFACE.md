# PUBLIC_ROUTE_SURFACE

## Summary

This checkpoint completes the missing canonical public auth routes required by
Phase 3 for the authoritative release path.

The public route plane is now owned by explicit route modules under
`tigrbl_auth/api/rest/routers/`, with corresponding operation modules under
`tigrbl_auth/ops/`, schema ownership in `tigrbl_auth/api/rest/schemas.py`,
durable persistence under `tigrbl_auth/tables/*` and
`tigrbl_auth/services/persistence.py`, and contract publication through the
OpenAPI generation pipeline.

## Canonical route ownership

| Route | Profiles | Router | Operation | Primary schema(s) | Persistence / owner targets |
|---|---|---|---|---|---|
| `/login` | baseline, production, hardening | `tigrbl_auth/api/rest/routers/login.py` | `tigrbl_auth/ops/login.py` | `CredsIn`, `TokenPair` | `AuthSession`, `TokenRecord` |
| `/authorize` | baseline, production, hardening | `tigrbl_auth/api/rest/routers/authorize.py` | `tigrbl_auth/ops/authorize.py` | query surface | `AuthCode`, `AuthSession`, `Consent` |
| `/token` | baseline, production, hardening | `tigrbl_auth/api/rest/routers/token.py` | `tigrbl_auth/ops/token.py` | `TokenPair`, grant forms | `TokenRecord`, `AuthCode`, `DeviceCode` |
| `/userinfo` | production, hardening | standards include | OIDC owner surface | OIDC userinfo schemas | token/introspection backing |
| `/register` | production, hardening | `tigrbl_auth/api/rest/routers/register.py` | `tigrbl_auth/ops/register.py` | `DynamicClientRegistrationIn`, `DynamicClientRegistrationOut` | `Client`, `ClientRegistration`, `AuditEvent` |
| `/register/{client_id}` | production, hardening | `tigrbl_auth/api/rest/routers/register.py` | `tigrbl_auth/ops/register.py` | `DynamicClientRegistrationManagementIn`, `DynamicClientRegistrationOut`, delete status payload | `Client`, `ClientRegistration`, `AuditEvent` |
| `/revoke` | production, hardening | `tigrbl_auth/api/rest/routers/revoke.py` | `tigrbl_auth/ops/revoke.py` | `RevocationOut` | `RevokedToken`, `TokenRecord`, `AuditEvent` |
| `/logout` | production, hardening | `tigrbl_auth/api/rest/routers/logout.py` | `tigrbl_auth/ops/logout.py` | `LogoutIn`, `LogoutOut` | `AuthSession`, `LogoutState`, `AuditEvent` |
| `/introspect` | production, hardening | standards include | RFC 7662 owner surface | `IntrospectOut` | `TokenRecord`, `RevokedToken` |
| `/device_authorization` | hardening | `tigrbl_auth/api/rest/routers/device_authorization.py` | `tigrbl_auth/ops/device_authorization.py` | `DeviceAuthorizationIn`, `DeviceAuthorizationOut` | `DeviceCode`, `AuditEvent` |
| `/par` | hardening | `tigrbl_auth/api/rest/routers/par.py` | `tigrbl_auth/ops/par.py` | `PushedAuthorizationRequestIn`, `PushedAuthorizationResponse` | `PushedAuthorizationRequest`, `AuditEvent` |
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

Phase 3 adds contract-visible checks for the canonical route set:

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

The public-route plane now includes the Phase 3 canonical route inventory together with the Phase 7 advanced authorization and management surfaces required by the retained production and hardening RFC families.

It still does **not** by itself make the repository certifiably fully featured or certifiably fully RFC/spec compliant across the full declared certification boundary. Remaining blockers are now concentrated in evidence promotion, peer validation, release attestation, and broader certification-grade interop breadth.


## Phase 4 browser/logout semantics layered onto the public route plane

The Phase 4 checkpoint keeps the Phase 3 route inventory intact and deepens the browser-facing semantics behind those routes:

- `/login` now establishes a durable browser session and issues an opaque RFC 6265 cookie
- `/authorize` resolves browser sessions through the domain-owned cookie subsystem and emits `session_state`
- `/logout` now validates registered post-logout redirect URIs, clears the opaque cookie, and returns or persists logout fanout metadata
- `/register` now accepts `post_logout_redirect_uris`, `frontchannel_logout_uri`, and `backchannel_logout_uri` metadata used by logout planning

This still does not make the package fully certifiable, but it makes the browser/logout behavior materially more implementation-backed and observable.


## Phase 8 executable surface registry

The route inventory above is now driven by a single capability registry in
` tigrbl_auth/config/surfaces.py ` and mounted through
` tigrbl_auth.api.surfaces.attach_runtime_surfaces `.

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
