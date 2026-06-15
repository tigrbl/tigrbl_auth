> [!WARNING]
> Non-authoritative active document.
> Use this as a composition note for app and UIX boundaries, not as certification or release truth.
> For current executable and release truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and the generated reference surfaces.

# Edge App and UIX Composition Matrices

This note turns the current repo discussion into explicit composition matrices.

See also `docs/architecture/TIGRBL_APP_DEPENDENCY_MATRICES.md` for per-app dependency matrices over the same composed app set.
See also `docs/architecture/TIGRBL_UIX_DEPENDENCY_MATRICES.md` for per-UIX dependency matrices over the proposed UIX split.
See also `docs/architecture/FUTURE_STATE_APP_DEPLOYMENT_MATRICES.md` and `docs/architecture/FUTURE_STATE_UIX_DEPLOYMENT_MATRICES.md` for the target deployment/path/view matrices.

The key distinction is:

- An **app** is a deployable or composable runtime surface.
- A **UIX** is a user-facing experience surface for a specific operator or user role.

In the current checkout, the backend is shared and multi-tenant, `public-uix` is a distinct UIX, and `admin-uix` currently carries both platform-admin and tenant-admin responsibilities.

## Current app matrix

| App / surface | Kind | Primary users | Backend lane | Current repo state | Notes |
|---|---|---|---|---|---|
| `tigrbl_auth` identity deployment | backend app | platform, tenants, tenant apps, end users | public REST/OIDC and admin REST/RPC | shipped | Shared multi-tenant backend deployment. |
| `admin-uix` | frontend app / UIX | platform admins, tenant admins | `/admin/*` and `/rpc` | shipped | Currently combines platform-admin and tenant-admin responsibilities. |
| `public-uix` | frontend app / UIX | tenant human users | public REST/OIDC | shipped | Covers login, registration, consent, callback, logout, and profile flows. |
| `@tigrbl-auth/rp` | browser client package | browser application developers | public REST/OIDC | shipped | Browser-safe RP SDK, not an operator console. |
| `tigrbl-auth-protocol-rp` | Python client package | backend application developers | public REST/OIDC | shipped | Server-side RP helper library, not a deployable portal. |
| `tigrbl-authz-resource-server` | API integration package | protected API developers | JWKS and introspection | shipped | Validation helper for downstream protected APIs. |
| `acme-notes-cli` | example client app | CLI users / integrators | device authorization and token | shipped example | Example consumer, not a platform control-plane app. |

## Target app composition matrix

| Target app | Kind | Primary users | Backend lane | Why it should exist | Current status |
|---|---|---|---|---|---|
| `tigrbl-auth-idp` | backend app | all external surfaces | public REST/OIDC and admin REST/RPC | Shared multi-tenant identity provider and control plane. | exists today as `tigrbl_auth` deployment |
| `tigrbl-auth-public-portal` | frontend app / UIX | tenant human users | public REST/OIDC | End-user login and consent should stay separate from admin operations. | exists today as `public-uix` |
| `tigrbl-auth-platform-admin-console` | frontend app / UIX | platform superusers | admin REST/RPC | Platform-wide tenant creation and authority assignment need their own surface. | folded into `admin-uix` today |
| `tigrbl-auth-tenant-admin-console` | frontend app / UIX | tenant admins | admin REST/RPC | Tenant-scoped identity, key, and app administration should be isolated from platform actions. | folded into `admin-uix` today |
| `tigrbl-auth-developer-portal` | frontend app / UIX | tenant app developers | public registration plus admin/client control plane | App/client registration and integration settings are a distinct workflow from user admin. | backend support exists; UIX not fully shipped |
| `tigrbl-auth-service-admin-surface` | app or focused UIX | workload and service operators | admin/control plane plus token surfaces | Machine identities, service keys, workload identities, and automation posture are distinct from human admin UX. | partial backend capability; no dedicated shipped UIX |

## Current UIX matrix

| UIX | Role served | Scope | Current capabilities in repo | Missing or overloaded areas |
|---|---|---|---|---|
| `public-uix` | tenant human user | tenant public auth UX | login, registration, consent, callback, logout, profile, email verification, password reset | does not provide tenant administration or developer self-service |
| `admin-uix` | platform admin and tenant admin | shared control plane | tenant list/create/delete, identity CRUD, tenant JWKS management, admin session flows | mixes platform-admin and tenant-admin roles; client/developer workflows are not fully surfaced in shipped navigation |

## Target UIX matrix

| Target UIX | Role served | Scope | Expected primary capabilities | Current status |
|---|---|---|---|---|
| `public-uix` | tenant human user | tenant public auth UX | login, consent, registration, callback, logout, profile | shipped |
| `platform-admin-uix` | platform superuser | deployment-wide | create tenants, delete tenants, assign tenant admins, bootstrap tenant control | needed split from `admin-uix` |
| `tenant-admin-uix` | tenant admin | tenant-scoped admin | manage tenant identities, tenant signing keys, tenant-local clients, tenant-local policy | needed split from `admin-uix` |
| `developer-uix` | tenant developer / app owner | tenant application integration | register OIDC apps, manage redirect URIs, auth methods, client secrets/JWKS metadata, discovery references | backend mostly supports this; dedicated shipped UIX missing |
| `service-admin-uix` | service or workload operator | machine identity administration | service identities, API keys, client credentials, workload identity, machine-to-machine setup | optional but likely needed if non-human identities are first-class |

## Workflow matrix

| Workflow | Primary actor | Backend lane | Best-fit app | Best-fit UIX | Current repo reality |
|---|---|---|---|---|---|
| Create tenant | platform superuser | admin REST | platform admin console | `platform-admin-uix` | currently done in `admin-uix` |
| Grant tenant admin authority | platform superuser | admin REST | platform admin console | `platform-admin-uix` | currently done in `admin-uix` identities flow |
| Manage tenant users | tenant admin | admin REST | tenant admin console | `tenant-admin-uix` | currently done in `admin-uix` |
| Manage tenant JWKS | tenant admin | admin RPC plus public tenant discovery parity | tenant admin console | `tenant-admin-uix` | currently done in `admin-uix` |
| Human user login | tenant human user | public REST/OIDC | public portal | `public-uix` | already aligned |
| CLI device login | CLI user | device authorization and token | consumer CLI | not a UIX | example exists as `acme-notes-cli` |
| Browser app login integration | tenant app developer | authorize and token | browser app using RP SDK | not a UIX | package exists as `@tigrbl-auth/rp` |
| Backend app login integration | backend app developer | discovery, authorize, token, userinfo | backend app using RP helpers | not a UIX | package exists as `tigrbl-auth-protocol-rp` |
| Protected API token validation | API developer | JWKS and introspection | protected API using verifier package | not a UIX | package exists as `tigrbl-authz-resource-server` |
| Register OIDC application | tenant developer or tenant admin | `/register` or client control plane | developer portal | `developer-uix` | backend supported; shipped UIX incomplete |
| Rotate client credentials or metadata | tenant developer or tenant admin | client control plane | developer portal | `developer-uix` | backend/client component exists; not fully exposed in shipped admin nav |
| Manage machine identities | service operator | token, service-key, operator plane | service admin surface | `service-admin-uix` | partial backend support; no dedicated UIX |

## Composition recommendation matrix

| Composition level | Include | Result |
|---|---|---|
| Minimum deployable | `tigrbl_auth` backend + `public-uix` + `admin-uix` | Works today, but admin responsibilities are overloaded. |
| Recommended near-term split | `tigrbl_auth` backend + `public-uix` + `platform-admin-uix` + `tenant-admin-uix` | Clean separation between deployment-wide and tenant-scoped administration. |
| Recommended product split | `tigrbl_auth` backend + `public-uix` + `platform-admin-uix` + `tenant-admin-uix` + `developer-uix` | Adds a proper self-service application registration surface. |
| Full role-complete split | previous set + `service-admin-uix` | Adds a dedicated non-human identity and workload-operator surface. |

## Honest gap matrix

| Gap | Why it matters | Current state |
|---|---|---|
| Platform admin and tenant admin are combined | Cross-tenant and tenant-local actions should not share the same UIX by default. | combined in `admin-uix` |
| Developer self-service is not a first-class shipped portal | OIDC app registration and client lifecycle are distinct from user administration. | backend support exists; shipped UX incomplete |
| Machine/service identity administration lacks a dedicated UIX | Machine actors need separate workflows from human tenant admins. | backend capability is partial; no dedicated UIX |
| Tenant self-service currently rides the admin plane | A separate tenant portal may still be desirable even if the backend lane remains the same. | tenant admins currently use `admin-uix` |

## Recommended named composition set

### Apps

- `tigrbl-auth-idp`
- `tigrbl-auth-public-portal`
- `tigrbl-auth-platform-admin-console`
- `tigrbl-auth-tenant-admin-console`
- `tigrbl-auth-developer-portal`
- `tigrbl-auth-service-admin-surface` optional

### UIXs

- `public-uix`
- `platform-admin-uix`
- `tenant-admin-uix`
- `developer-uix`
- `service-admin-uix` optional
