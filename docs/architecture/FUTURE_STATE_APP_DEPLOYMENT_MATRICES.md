> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state deployment composition note, not as certification or release truth.
> For current executable and release truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and the generated reference surfaces.

# Future-State App Deployment Matrices

This note describes the target deployment shape for the composed `tigrbl` app surfaces.

The model here is:

- one shared multi-tenant backend identity plane
- multiple edge apps mounted around that plane
- each app owning a distinct operational role and route space

See also `docs/architecture/EDGE_APP_UIX_COMPOSITION_MATRICES.md` for the role split, `docs/architecture/TIGRBL_APP_DEPENDENCY_MATRICES.md` for package-level dependency detail, and `docs/architecture/apps/README.md` for one note per target app.

## Future-state app set

| Target app | Kind | Primary persona | Deployment role | Current implementation basis |
|---|---|---|---|---|
| `tigrbl-auth-idp` | backend app | platform, tenants, apps, users, services | shared multi-tenant identity and control plane | current `tigrbl_auth` backend |
| `tigrbl-auth-public-portal` | edge app | tenant human users | public browser auth entrypoint | current `public-uix` |
| `tigrbl-auth-platform-admin-console` | edge app | platform superusers | deployment-wide control-plane console | split from current `admin-uix` |
| `tigrbl-auth-tenant-admin-console` | edge app | tenant admins | tenant-scoped admin console | split from current `admin-uix` |
| `tigrbl-auth-developer-portal` | edge app | tenant app developers | app registration and integration console | partly present in backend and dormant UI components |
| `tigrbl-auth-service-admin-surface` | edge app | workload and service operators | machine identity and service access console | future composition over partial backend capability |

## `tigrbl-auth-idp` matrix

| Dimension | Future-state value |
|---|---|
| App kind | shared backend identity provider |
| Primary role | source of truth for public auth, tenant discovery, token issuance, admin control, and signing material publication |
| Suggested origin | `https://id.example.com` |
| Primary mounted paths | `/authorize`, `/token`, `/userinfo`, `/introspect`, `/register`, `/logout`, `/.well-known/*`, `/tenants/{tenant_slug}/.well-known/*`, `/admin/*`, `/rpc` |
| Functional blocks exposed | public auth lane, tenant discovery lane, admin REST lane, admin RPC lane, tenant JWKS publication lane |
| Upstream dependencies | persistence, key material storage, email/provider integrations, policy/config, auth/session services |
| Downstream dependents | all edge apps, RP SDKs, resource-server verifiers, CLI/device clients, tenant applications |
| Boundary rule | no tenant-specific bespoke UI should live here; this app exposes APIs and protocol surfaces |
| Current repo basis | `tigrbl_auth.app`, `tigrbl_auth.gateway`, REST routers, RPC methods, discovery and JWKS services |
| Main gap | app exists, but future-state deployment should be described and branded as the stable shared IDP plane |

## `tigrbl-auth-public-portal` matrix

| Dimension | Future-state value |
|---|---|
| App kind | public browser edge app |
| Primary role | human-user login, registration, consent, callback completion, recovery, and profile entrypoint |
| Suggested origin | `https://login.example.com` or tenant-branded login origin |
| Suggested mounted path | `/` |
| Backend paths consumed | `/authorize`, `/token`, `/userinfo`, `/logout`, `/register`, tenant discovery and JWKS metadata, recovery and verification endpoints |
| Primary views owned | login, register, consent, callback, profile, forgot password, reset password, verify email, terms |
| Functional block placement | public auth experience layer |
| Talks to | `tigrbl-auth-idp` public lane only |
| Should not talk to | `/admin/*`, `/rpc` |
| Current repo basis | `pkgs/95-ui/public-uix` plus its nginx route allowlist |
| Main gap | future-state deployment may need tenant branding, tenant selection, and per-tenant host/path strategy |

## `tigrbl-auth-platform-admin-console` matrix

| Dimension | Future-state value |
|---|---|
| App kind | privileged control-plane edge app |
| Primary role | deployment-wide administration across all tenants |
| Suggested origin | `https://platform-auth-admin.example.com` |
| Suggested mounted path | `/` |
| Backend paths consumed | `/admin/auth/*`, `/admin/tenants`, `/admin/identities`, `/rpc` |
| Primary views owned | platform dashboard, tenant list, tenant create, tenant delete, tenant detail, tenant admin assignment, platform identity administration, audit overview |
| Functional block placement | platform operations layer |
| Talks to | `tigrbl-auth-idp` admin REST and admin RPC lanes |
| Should not own | tenant-local day-to-day user admin, end-user login, app developer self-service |
| Current repo basis | platform-relevant parts of `pkgs/95-ui/admin-uix` |
| Main gap | current `admin-uix` mixes deployment-wide and tenant-local actions |

## `tigrbl-auth-tenant-admin-console` matrix

| Dimension | Future-state value |
|---|---|
| App kind | tenant-scoped control-plane edge app |
| Primary role | self-service administration inside one tenant boundary |
| Suggested origin | `https://tenant-auth-admin.example.com` or `https://admin.example.com/tenants/{tenant_slug}` |
| Suggested mounted path | `/` |
| Backend paths consumed | `/admin/auth/*`, `/admin/identities`, `/rpc`, tenant discovery and tenant JWKS publication endpoints for parity/reference |
| Primary views owned | tenant dashboard, tenant identities, principal detail, credential issuance flows, tenant signing keys, tenant JWKS publication, tenant policy/config |
| Functional block placement | tenant administration layer |
| Talks to | `tigrbl-auth-idp` admin REST, admin RPC, tenant discovery/JWKS surfaces |
| Should not own | platform-wide tenant lifecycle, cross-tenant authority assignment |
| Current repo basis | tenant-relevant parts of `pkgs/95-ui/admin-uix` |
| Main gap | tenant-scoped authority and navigation need to be separated cleanly from platform authority |

## `tigrbl-auth-developer-portal` matrix

| Dimension | Future-state value |
|---|---|
| App kind | tenant developer edge app |
| Primary role | self-service app registration and federation integration management |
| Suggested origin | `https://developer-auth.example.com` |
| Suggested mounted path | `/` |
| Backend paths consumed | `/register`, `/register/{client_id}`, `/rpc` client and client-registration methods, tenant discovery documents |
| Primary views owned | app catalog, app create, OIDC client registration, redirect URI management, client auth method config, secret/JWKS rotation, discovery reference, integration docs |
| Functional block placement | application integration layer |
| Talks to | `tigrbl-auth-idp` public registration lane plus admin/client control plane |
| Should not own | human-user login UX, cross-tenant platform administration |
| Current repo basis | `ClientManagement.tsx`, client registration RPC methods, dynamic registration endpoints |
| Main gap | backend capability exists, but the dedicated portal and route model are not shipped yet |

## `tigrbl-auth-service-admin-surface` matrix

| Dimension | Future-state value |
|---|---|
| App kind | service and workload operator edge app |
| Primary role | non-human identity onboarding and service access administration |
| Suggested origin | `https://service-auth.example.com` |
| Suggested mounted path | `/` |
| Backend paths consumed | `/token`, `/introspect`, JWKS endpoints, service-key and machine-principal control surfaces, future workload identity methods |
| Primary views owned | service identities, machine principals, API keys, client credentials, workload federation setup, token inspection/testing, trust posture |
| Functional block placement | machine access layer |
| Talks to | `tigrbl-auth-idp` token, introspection, JWKS, and operator/control surfaces |
| Should not own | human-user profile and consent, platform tenant creation |
| Current repo basis | auth backends, token plane, API-key/service-key capabilities, remote introspection support |
| Main gap | no dedicated shipped UIX or stable operator surface exists yet |

## Future-state app routing matrix

| App | External origin/path | Consumes from IDP | Main role boundary |
|---|---|---|---|
| `tigrbl-auth-idp` | `id.example.com/*` | n/a | protocol and control-plane backend |
| `tigrbl-auth-public-portal` | `login.example.com/` | public lane only | tenant end-user auth UX |
| `tigrbl-auth-platform-admin-console` | `platform-auth-admin.example.com/` | admin REST and RPC | platform-wide administration |
| `tigrbl-auth-tenant-admin-console` | `tenant-auth-admin.example.com/` | admin REST, RPC, tenant discovery parity | tenant-local administration |
| `tigrbl-auth-developer-portal` | `developer-auth.example.com/` | registration, client control, discovery | app/developer integration |
| `tigrbl-auth-service-admin-surface` | `service-auth.example.com/` | token, introspection, JWKS, machine control | machine/service administration |

## Future-state app call-flow matrix

| From app | To app/surface | Why the relationship exists |
|---|---|---|
| `tigrbl-auth-public-portal` | `tigrbl-auth-idp` public lane | executes browser auth flows and end-user recovery flows |
| `tigrbl-auth-platform-admin-console` | `tigrbl-auth-idp` admin lane | creates tenants and assigns high-privilege authority |
| `tigrbl-auth-tenant-admin-console` | `tigrbl-auth-idp` admin lane | manages tenant identities, credentials, and keys |
| `tigrbl-auth-developer-portal` | `tigrbl-auth-idp` registration and client plane | creates and manages OIDC/OAuth applications |
| `tigrbl-auth-service-admin-surface` | `tigrbl-auth-idp` token and machine plane | provisions and validates service access patterns |
| Tenant applications | `tigrbl-auth-idp` plus `tigrbl-auth-public-portal` | rely on IDP protocols and optionally redirect humans into the public portal |

## Future-state app split matrix

| Current repo surface | Future-state target app | Split action |
|---|---|---|
| `tigrbl_auth` backend | `tigrbl-auth-idp` | rename/brand as the stable shared IDP plane |
| `pkgs/95-ui/public-uix` | `tigrbl-auth-public-portal` | preserve and tenant-brand |
| `pkgs/95-ui/admin-uix` tenant creation and cross-tenant control | `tigrbl-auth-platform-admin-console` | extract into platform-only console |
| `pkgs/95-ui/admin-uix` identities and JWKS tenant operations | `tigrbl-auth-tenant-admin-console` | extract into tenant-admin console |
| dormant client-management UI and client APIs | `tigrbl-auth-developer-portal` | surface as first-class developer portal |
| machine/service operator workflows not yet surfaced | `tigrbl-auth-service-admin-surface` | compose new focused app when service identity becomes first-class |
