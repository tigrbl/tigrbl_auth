> [!WARNING]
> Non-authoritative active document.
> Use this as a composition and packaging note, not as certification or release truth.
> For current executable and release truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and the generated reference surfaces.

# Tigrbl App Dependency Matrices

This note expands the composed app set into per-app dependency matrices.

The app names here match the target composition set in
`docs/architecture/EDGE_APP_UIX_COMPOSITION_MATRICES.md`.

## Dependency legend

| Dependency class | Meaning |
|---|---|
| Runtime package dependencies | Python or TypeScript packages that the app is primarily built from. |
| Surface dependencies | Public or admin API lanes the app consumes or exposes. |
| UIX dependencies | User-facing surfaces that must exist alongside the app. |
| Data and state dependencies | Durable stores, tenant records, sessions, keys, and registration state required by the app. |
| External infrastructure dependencies | Infrastructure or deployment concerns outside the package graph. |

## App inventory matrix

| App | Current repo basis | Primary role |
|---|---|---|
| `tba-auth-idp` | `tba_auth` backend deployment | Shared multi-tenant identity provider and control plane |
| `tba-auth-public-portal` | `pkgs/105-ui/tba-ui-public` | Tenant human-user public auth UX |
| `tba-auth-platform-admin-console` | split from `pkgs/105-ui/tba-ui-administration` | Platform-wide tenant and authority administration |
| `tba-auth-tenant-admin-console` | split from `pkgs/105-ui/tba-ui-administration` | Tenant-scoped identity, key, and local configuration administration |
| `tba-auth-developer-portal` | not fully shipped; partial client-management code exists | Tenant app and OIDC client self-service |
| `tba-auth-service-admin-surface` | not fully shipped; backend capability is partial | Machine/service/workload identity administration |

---

## `tba-auth-idp`

| Dependency class | Dependencies |
|---|---|
| Runtime package dependencies | `tba-auth`, `tba-server-identity`, `tba-runtime-identity`, `tba-runtime-identity-administration`, `tba-protocol-oauth`, `tba-protocol-oidc`, `tba-credentials`, `tba-runtime-authorization-policy`, `tba-concrete-identity-principals`, `tba-provider-identity-jose`, `tba-contracts-identity`, `tba-storage-core`, `tba-primitives-identity`, `tba-operator-identity` |
| Surface dependencies | public REST/OIDC lane, admin REST lane, admin RPC/OpenRPC lane, discovery documents, tenant discovery routes, JWKS publication routes |
| UIX dependencies | supports `tba-auth-public-portal`, `tba-auth-platform-admin-console`, `tba-auth-tenant-admin-console`, `tba-auth-developer-portal`, and optionally `tba-auth-service-admin-surface` |
| Data and state dependencies | tenant records, user identities, auth sessions, auth codes, token records, client registrations, service keys, API keys, consent, audit events, key rotation events, JWKS artifacts |
| External infrastructure dependencies | ASGI runner (`uvicorn`, `hypercorn`, or `tigrcorn`), SQL database (`sqlite` or `postgres`), TLS termination, environment/profile configuration, static hosting or reverse proxy for UIX apps |
| Notes | This is the only mandatory backend app. All other composed apps depend on it. |

---

## `tba-auth-public-portal`

| Dependency class | Dependencies |
|---|---|
| Runtime package dependencies | `@tba/ui-public`, React, React DOM, Vite, TypeScript |
| Surface dependencies | OIDC discovery, `/authorize`, `/token`, `/userinfo`, `/logout`, `/register`, tenant-scoped `/.well-known/openid-configuration`, tenant-scoped JWKS URI discovery |
| UIX dependencies | `public-uix` |
| Data and state dependencies | browser session state, public session cookie, end-user profile state, consent context, callback state, PKCE or browser RP flow state |
| External infrastructure dependencies | static asset hosting, browser runtime, reverse proxy or same-origin route forwarding to the backend identity deployment |
| Notes | This app depends on the backend public lane only. It should not require admin RPC or tenant-management surfaces. |

---

## `tba-auth-platform-admin-console`

| Dependency class | Dependencies |
|---|---|
| Runtime package dependencies | split subset of `@tba/ui-administration`, React, React DOM, Vite, TypeScript; backend support from `tba-runtime-identity-administration`, `tba-operator-identity`, `tba-contracts-identity`, `tba-runtime-authorization-policy` |
| Surface dependencies | `/admin/auth/*`, `/admin/tenants`, `/admin/identities`, `/rpc` methods for directory, profile, governance, keys, and operator status |
| UIX dependencies | `platform-admin-uix` |
| Data and state dependencies | admin session state, tenant records, platform-wide user records, admin authority flags, delegated-admin policy summaries, audit and governance state |
| External infrastructure dependencies | static hosting, authenticated admin browser session, access to the shared backend identity deployment |
| Notes | This app is the control surface for superuser operations like tenant creation and assignment of tenant admins. It should not expose tenant-local end-user flows. |

---

## `tba-auth-tenant-admin-console`

| Dependency class | Dependencies |
|---|---|
| Runtime package dependencies | split subset of `@tba/ui-administration`, React, React DOM, Vite, TypeScript; backend support from `tba-runtime-identity-administration`, `tba-operator-identity`, `tba-runtime-authorization-policy`, `tba-contracts-identity` |
| Surface dependencies | `/admin/auth/*`, `/admin/identities`, tenant discovery routes, `/rpc` directory methods, `tenant.keys.*`, `keys.list`, `jwks.show`, client and policy control-plane methods |
| UIX dependencies | `tenant-admin-uix` |
| Data and state dependencies | tenant-scoped admin session, tenant visibility filters, tenant identities, tenant JWKS inventory and publication state, tenant client records, tenant policy state |
| External infrastructure dependencies | static hosting, authenticated admin browser session, access to the shared backend identity deployment |
| Notes | This app is tenant-scoped even though it still rides the admin/control-plane backend lane. It should exclude platform-only actions like arbitrary tenant creation or global authority assignment. |

---

## `tba-auth-developer-portal`

| Dependency class | Dependencies |
|---|---|
| Runtime package dependencies | future dedicated portal UIX, plus existing backend support from `tba-protocol-oauth`, `tba-runtime-identity-administration`, `tba-contracts-identity`, `tba-runtime-authorization-policy`; existing partial frontend basis in `pkgs/105-ui/tba-ui-administration/components/ClientManagement.tsx` |
| Surface dependencies | `/register`, `/register/{client_id}`, OIDC discovery metadata, tenant discovery metadata, client control-plane methods (`client.list`, `client.show`, `client.registration.*`, and any future `client.create/update/delete` RPC methods that are formally shipped) |
| UIX dependencies | `developer-uix` |
| Data and state dependencies | client registration records, redirect URIs, grant types, token endpoint auth methods, client secrets or client JWKS metadata, software metadata, tenant ownership and delegated admin policy |
| External infrastructure dependencies | static hosting, developer browser session, access to discovery and registration endpoints, documentation/examples for app integrators |
| Notes | The backend support is largely present, but the shipped frontend is incomplete. This app depends on both public registration surfaces and tenant-scoped administrative control over client records. |

---

## `tba-auth-service-admin-surface`

| Dependency class | Dependencies |
|---|---|
| Runtime package dependencies | future dedicated UIX or automation surface; backend support from `tba-credentials`, `tba-runtime-authorization-policy`, `tba-concrete-identity-principals`, `tba-protocol-oauth`, `tba-protocol-oauth-protected-resource`, and operator/service-key workflows |
| Surface dependencies | token endpoint, introspection endpoint, JWKS publication, service-key and API-key administration surfaces, workload-identity and advanced-identity control surfaces where promoted into the release path |
| UIX dependencies | `service-admin-uix` if browser-based; may also depend on CLI or automation surfaces rather than a browser UI alone |
| Data and state dependencies | service identities, service keys, API keys, workload identity records, token introspection state, machine principal metadata, trust-domain and scope policy |
| External infrastructure dependencies | automation clients, CI/CD secret handling, machine-to-machine trust posture, protected API deployment integration |
| Notes | This surface is optional in the near term but becomes necessary once non-human identities are a first-class operator concern rather than an internal backend capability only. |

---

## Shared dependency overlap matrix

| Dependency | `idp` | `public-portal` | `platform-admin-console` | `tenant-admin-console` | `developer-portal` | `service-admin-surface` |
|---|---|---|---|---|---|---|
| public REST/OIDC lane | yes | yes | no | partial | yes | yes |
| admin REST lane | yes | no | yes | yes | partial | partial |
| admin RPC/OpenRPC lane | yes | no | yes | yes | partial | partial |
| tenant records | yes | indirect | yes | yes | yes | indirect |
| identity records | yes | indirect | yes | yes | indirect | indirect |
| client registration state | yes | indirect | partial | partial | yes | indirect |
| JWKS and key state | yes | indirect | partial | yes | indirect | yes |
| machine/service identity state | yes | no | indirect | indirect | indirect | yes |

## Current-to-target implementation basis matrix

| Target app | Current concrete basis in this repo | Main dependency gap |
|---|---|---|
| `tba-auth-idp` | `tba_auth` backend package and split Python packages | already concrete |
| `tba-auth-public-portal` | `pkgs/105-ui/tba-ui-public` | tenant-branded composition and deployment wiring |
| `tba-auth-platform-admin-console` | platform subset of `pkgs/105-ui/tba-ui-administration` | explicit split from tenant-admin concerns |
| `tba-auth-tenant-admin-console` | tenant subset of `pkgs/105-ui/tba-ui-administration` | explicit split from platform-admin concerns |
| `tba-auth-developer-portal` | partial `ClientManagement` component plus backend registration/control-plane support | dedicated UIX, formal routing, and tighter client-management contract surface |
| `tba-auth-service-admin-surface` | partial backend service/workload capability only | dedicated surface definition, promoted workflows, and possibly a non-browser-first operator experience |

## Recommended packaging implication matrix

| Target app | Recommended packaging direction |
|---|---|
| `tba-auth-idp` | keep as shared backend deployment over the existing split Python packages |
| `tba-auth-public-portal` | keep as dedicated frontend app package |
| `tba-auth-platform-admin-console` | split from `admin-uix` into a separate frontend app package |
| `tba-auth-tenant-admin-console` | split from `admin-uix` into a separate frontend app package |
| `tba-auth-developer-portal` | create a dedicated frontend app package; reuse client-management logic and public discovery helpers |
| `tba-auth-service-admin-surface` | decide whether this is a frontend app, a CLI-first operator app, or both before packaging |
