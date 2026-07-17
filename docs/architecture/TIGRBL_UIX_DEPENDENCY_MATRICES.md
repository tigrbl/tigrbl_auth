> [!WARNING]
> Non-authoritative active document.
> Use this as a composition and packaging note, not as certification or release truth.
> For current executable and release truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and the generated reference surfaces.

# Tigrbl UIX Dependency Matrices

This note expands the proposed UIX set into per-UIX dependency matrices.

The proposed UIXs are:

- `public-uix`
- `platform-admin-uix`
- `tenant-admin-uix`
- `developer-uix`
- `service-admin-uix` optional

These UIX names match the target UIX composition in
`docs/architecture/EDGE_APP_UIX_COMPOSITION_MATRICES.md`.

## Dependency legend

| Dependency class | Meaning |
|---|---|
| Frontend package dependencies | UI runtime, shared frontend modules, and local component/service modules. |
| Backend surface dependencies | Backend routes, RPC methods, discovery docs, or contract surfaces the UIX consumes. |
| Identity and session dependencies | Session state, actor identity, tenant scope, cookies, delegated scope, or browser storage requirements. |
| Domain data dependencies | The business objects or records the UIX must read or mutate. |
| External infrastructure dependencies | Static hosting, reverse proxying, browser context, and deployment prerequisites. |

## UIX inventory matrix

| UIX | Current repo basis | Primary role |
|---|---|---|
| `public-uix` | `pkgs/105-ui/public-uix` | Tenant human-user authentication and consent UX |
| `platform-admin-uix` | split from `pkgs/105-ui/admin-uix` | Platform superuser administration UX |
| `tenant-admin-uix` | split from `pkgs/105-ui/admin-uix` | Tenant-scoped administration UX |
| `developer-uix` | not fully shipped; partial basis in `ClientManagement` and discovery helpers | Tenant app developer and OIDC client self-service UX |
| `service-admin-uix` | not fully shipped; backend-only partial basis today | Service/workload/machine identity administration UX |

---

## `public-uix`

| Dependency class | Dependencies |
|---|---|
| Frontend package dependencies | `@tigrbl-auth/public-uix`, React, React DOM, Vite, TypeScript, `useAuth`, `useAuthSession`, `useLogin`, `useRegister`, `useOidcActions`, `tigrblAuthDiscovery`, OIDC adapter modules, public UX policy helpers |
| Backend surface dependencies | `/.well-known/openid-configuration`, tenant-scoped `/.well-known/openid-configuration`, `/authorize`, `/token`, `/userinfo`, `/logout`, `/register`, discovery-advertised registration endpoint, tenant-scoped JWKS URI |
| Identity and session dependencies | public session cookie, browser-local user/session storage, callback state, post-login redirect target, optional MFA and email-verification state |
| Domain data dependencies | end-user identity profile, consent view model, login request context, registration payloads, logout redirect state |
| External infrastructure dependencies | static asset hosting, browser runtime, reverse proxy or same-origin path routing to the shared identity deployment |
| Notes | This UIX should remain isolated from admin/control-plane responsibilities. It depends on the public lane only. |

---

## `platform-admin-uix`

| Dependency class | Dependencies |
|---|---|
| Frontend package dependencies | split subset of `@tigrbl-auth/admin-uix`, React, React DOM, Vite, TypeScript, `adminAuthService`, `backendService`, `jsonRpcService`, `governancePolicy`, tenant-management and identity-management components, platform-only navigation shell |
| Backend surface dependencies | `/admin/auth/login`, `/admin/auth/session`, `/admin/auth/logout`, `/admin/auth/forgot-password`, `/admin/auth/reset-password`, `/admin/auth/change-password`, `/admin/tenants`, `/admin/identities`, `/rpc` directory/profile/governance surfaces as needed for platform context |
| Identity and session dependencies | authenticated admin browser session, superuser flag, platform actor identity, delegated-admin policy awareness where platform users can grant or inspect scopes |
| Domain data dependencies | tenant records, platform-visible user records, admin authority flags, tenant provisioning payloads, bootstrap/deletion decisions, audit and governance summaries |
| External infrastructure dependencies | static hosting, browser runtime, reverse proxying to admin surfaces, stricter operator authentication posture than public UX |
| Notes | This UIX should contain only deployment-wide authority flows. It should not be the place for tenant-local day-to-day application management. |

---

## `tenant-admin-uix`

| Dependency class | Dependencies |
|---|---|
| Frontend package dependencies | split subset of `@tigrbl-auth/admin-uix`, React, React DOM, Vite, TypeScript, `adminAuthService`, `backendService`, `jsonRpcService`, `governancePolicy`, `IdentityManagement`, `TenantJwksPublicationView`, tenant-scoped navigation shell |
| Backend surface dependencies | `/admin/auth/*`, `/admin/identities`, tenant-scoped discovery routes, `tenant.keys.seed`, `tenant.keys.create`, `tenant.keys.update`, `tenant.keys.delete`, `keys.list`, `jwks.show`, tenant directory and policy RPC methods |
| Identity and session dependencies | authenticated admin browser session, tenant selection state, delegated tenant scope, tenant visibility filtering, tenant-scoped mutation authorization |
| Domain data dependencies | tenant identity records, tenant admin privileges, tenant JWKS lifecycle state, tenant client inventory, tenant-local policy summaries |
| External infrastructure dependencies | static hosting, browser runtime, reverse proxying to admin/control-plane surfaces, access to tenant discovery parity routes |
| Notes | This UIX still rides the admin/control-plane backend lane, but its actor and data scope should be limited to one tenant at a time. |

---

## `developer-uix`

| Dependency class | Dependencies |
|---|---|
| Frontend package dependencies | future dedicated frontend package; current likely reuse sources are `ClientManagement.tsx`, `backendService`, `jsonRpcService`, `governancePolicy`, `tigrblAuthDiscovery`, possibly shared RP/discovery helpers |
| Backend surface dependencies | `/.well-known/openid-configuration`, tenant-scoped discovery docs, `/register`, `/register/{client_id}`, `client.list`, `client.show`, `client.registration.list`, `client.registration.show`, `client.registration.upsert`, `client.registration.delete`, and any formalized future client CRUD/admin RPC methods |
| Identity and session dependencies | tenant developer browser session or delegated tenant-admin scope, tenant ownership context, client mutation authorization checks, possible app-owner scope model if introduced |
| Domain data dependencies | OIDC client registrations, redirect URIs, grant types, auth method metadata, software metadata, client secrets or client JWKS metadata, discovery references, application ownership records |
| External infrastructure dependencies | static hosting, browser runtime, reverse proxying to both public registration and admin/client control-plane surfaces, developer-facing documentation/examples |
| Notes | This UIX depends on both public registration semantics and tenant-scoped administrative ownership. It is a distinct dependency profile from general tenant-user or tenant-admin UX. |

---

## `service-admin-uix`

| Dependency class | Dependencies |
|---|---|
| Frontend package dependencies | future dedicated frontend package or mixed browser/CLI surface; likely shared modules would include admin auth, backend service adapters, machine-identity or service-key focused components, and possibly verifier/introspection helpers |
| Backend surface dependencies | token endpoint, introspection endpoint, JWKS publication, service-key/API-key administration surfaces, workload identity and advanced identity control surfaces when promoted into the shipped boundary |
| Identity and session dependencies | operator or service-admin session, machine-identity scope, automation-safe credential handling, service/workload ownership context |
| Domain data dependencies | service identities, service keys, API keys, client-credentials registrations, workload identities, token introspection state, machine-principal policy and trust-domain metadata |
| External infrastructure dependencies | browser or CLI operator runtime, CI/CD or automation integration, secret-handling policy, protected API deployment coordination |
| Notes | This UIX is optional in the near term. It becomes necessary once machine actors are treated as first-class administered subjects instead of backend-only implementation details. |

---

## Shared dependency overlap matrix

| Dependency | `public-uix` | `platform-admin-uix` | `tenant-admin-uix` | `developer-uix` | `service-admin-uix` |
|---|---|---|---|---|---|
| React/Vite/TypeScript frontend stack | yes | yes | yes | yes | likely |
| public discovery documents | yes | no | partial | yes | partial |
| public REST/OIDC lane | yes | no | partial | yes | yes |
| admin REST lane | no | yes | yes | partial | partial |
| admin RPC/OpenRPC lane | no | partial | yes | yes | partial |
| browser session cookie | yes | no | no | possible | possible |
| admin authenticated session | no | yes | yes | possible | possible |
| tenant scoping and delegated scope | no | partial | yes | yes | yes |
| client registration state | no | no | partial | yes | partial |
| JWKS/key lifecycle state | indirect | partial | yes | indirect | yes |
| machine/service identity state | no | no | indirect | indirect | yes |

## Current-to-target implementation basis matrix

| Target UIX | Current concrete basis in this repo | Main dependency gap |
|---|---|---|
| `public-uix` | `pkgs/105-ui/public-uix` | tenant-branded composition and deployment wiring only |
| `platform-admin-uix` | platform subset of `pkgs/105-ui/admin-uix` | explicit removal of tenant-local workflows and a dedicated platform nav/state model |
| `tenant-admin-uix` | tenant subset of `pkgs/105-ui/admin-uix` | explicit removal of platform-global workflows and tenant-local client/policy completion |
| `developer-uix` | `ClientManagement.tsx` plus discovery/client backend support | dedicated UI shell, formal route model, stronger app-owner workflow model |
| `service-admin-uix` | partial backend-only service/workload capability | dedicated UI model, promoted service identity workflows, and possibly CLI-first rather than browser-first delivery |

## Packaging implication matrix

| Target UIX | Recommended packaging direction |
|---|---|
| `public-uix` | keep as dedicated frontend app package |
| `platform-admin-uix` | split from `admin-uix` into its own frontend app package |
| `tenant-admin-uix` | split from `admin-uix` into its own frontend app package |
| `developer-uix` | create a dedicated frontend app package and reuse client-management plus discovery helpers |
| `service-admin-uix` | decide whether to package as a dedicated frontend app, an operator CLI UI layer, or both |
