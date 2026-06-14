# tigrbl_auth Package Graph Brief

This brief grounds the architecture image in the live package inventory in this checkout.

## Package inventory

### Runtime and compatibility shell

- `tigrbl-auth`: compatibility facade preserving legacy `app`, `gateway`, `plugin`, CLI, and RFC import paths over the split package suite.
- `tigrbl-identity-server`: ASGI composition layer that builds public REST and admin RPC surfaces.
- `tigrbl-identity-runtime`: runtime planning, profile resolution, feature flags, deployment resolution, and runner adapters.
- `tigrbl-identity-operator`: operator CLI, repo truth, evidence workflows, and admin console helpers.

### Domain, protocol, and control-plane packages

- `tigrbl-identity-admin`: tenant, user, client, key, session, token, consent, audit, profile, and governance control-plane operations.
- `tigrbl-auth-protocol-oauth`: OAuth 2.x protocol flows including device authorization, PAR, token exchange, DPoP, and related RFC helpers.
- `tigrbl-auth-protocol-oidc`: OIDC discovery, ID token, userinfo, logout, session, and OIDC standards helpers.
- `tigrbl-authn-credentials`: password, API key, auth context, session, and token lifecycle helpers.
- `tigrbl-authz-policy`: RBAC, ABAC, delegated administration, provenance, and governance policy controls.
- `tigrbl-identity-principals`: tenant, principal, subject context, and trust-domain discovery helpers.
- `tigrbl-identity-jose`: JOSE, JWT, JWS, JWE, JWK, JWKS, key rotation, and signing helpers.
- `tigrbl-identity-contracts`: Pydantic REST and JSON-RPC contracts for public and admin APIs.

### Foundation and persistence packages

- `tigrbl-identity-storage`: SQLAlchemy tables, ORM models, migrations, persistence helpers, and operator state storage.
- `tigrbl-identity-core`: dependency-light primitives, typed helpers, path safety, and RFC 8785 canonicalization.

### Consumer and verification packages

- `tigrbl-auth-protocol-rp`: Python relying-party helpers for discovery, userinfo, logout, and RP integration.
- `tigrbl-authz-resource-server`: protected API token-validation and resource-server contracts.
- `tigrbl-identity-testkit`: fake identity components, vectors, fixtures, and integration harnesses.
- `acme-notes-cli`: example consumer showing device-login usage.

### UI and browser packages

- `@tigrbl-auth/public-uix`: public end-user UI built against generated OpenAPI and OIDC discovery surfaces.
- `@tigrbl-auth/admin-uix`: admin UI built against generated OpenRPC admin/control-plane surfaces.
- `@tigrbl-auth/rp`: browser-safe TypeScript relying-party SDK.

## Production block model

### Edge and consumer block

- Public UI, admin UI, browser RP SDK, Python RP helpers, resource-server helpers, and the example CLI live at the edge of production systems.
- These packages either call public REST and OIDC discovery endpoints or the admin RPC/OpenRPC surface.

### Runtime composition block

- `tigrbl-identity-server` is the main composition package for the running identity provider.
- `tigrbl-identity-runtime` resolves profiles, surfaces, flags, deployment style, and runner choice before the server is started.
- `tigrbl-auth` remains the compatibility shell that preserves older import and entrypoint paths across the split architecture.

### Domain services block

- OAuth, OIDC, admin, credential, policy, principal, JOSE, and contract packages provide the operational logic and protocol surface definitions used by the server.
- The operator package sits adjacent to this block because it uses the same runtime truth to generate evidence, surface reports, and installation artifacts.

### Data and foundation block

- Storage anchors persistence, migrations, and the state tables consumed by the runtime.
- Core provides low-level primitives and helper types that support the rest of the graph.

### Verification and governance sidecar block

- Testkit validates cross-cutting flows, conformance vectors, and fake peers.
- Operator workflows and SSOT artifacts support release governance and certification evidence.

## High-level flow edges

1. Public users and consumer apps enter through `@tigrbl-auth/public-uix`, `@tigrbl-auth/rp`, `tigrbl-auth-protocol-rp`, or the example CLI.
2. Administrative operators enter through `@tigrbl-auth/admin-uix` and `tigrbl-identity-operator`.
3. Those clients call the `tigrbl-identity-server` public REST or admin RPC surfaces.
4. The server delegates protocol and domain work to OAuth, OIDC, admin, credentials, policy, principals, JOSE, and contracts packages.
5. Domain logic persists and reads state through `tigrbl-identity-storage`.
6. Runtime startup and deployment behavior are resolved by `tigrbl-identity-runtime`.
7. Legacy consumers can still enter through `tigrbl-auth`, which forwards to the split runtime and server entrypoints.
