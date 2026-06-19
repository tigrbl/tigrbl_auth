> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state UIX composition note, not as certification or release truth.
> For current executable and release truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and the generated reference surfaces.

# Future-State UIX Deployment Matrices

This note describes the target user-experience surfaces that should sit on top of the composed `tigrbl_auth` deployment.

The model here is:

- each UIX serves one dominant operator or user role
- each UIX owns a coherent set of pages and workflows
- each UIX maps onto a narrow backend lane instead of one overloaded console

See also `docs/architecture/EDGE_APP_UIX_COMPOSITION_MATRICES.md` for the role split, `docs/architecture/TIGRBL_UIX_DEPENDENCY_MATRICES.md` for package-level dependency detail, and `docs/architecture/uix/README.md` for one note per target UIX.

## Future-state UIX set

| UIX | Primary actor | Main job | Current implementation basis |
|---|---|---|---|
| `public-uix` | tenant human user | login and end-user auth experience | current `pkgs/95-ui/public-uix` |
| `platform-admin-uix` | platform superuser | deployment-wide control-plane administration | split from current `pkgs/95-ui/admin-uix` |
| `tenant-admin-uix` | tenant admin | tenant-scoped administration | split from current `pkgs/95-ui/admin-uix` |
| `developer-uix` | tenant app developer | app registration and federation integration management | future extraction over partial current basis |
| `service-admin-uix` | service or workload operator | machine identity and service-access administration | future UIX over partial backend basis |

## `public-uix` matrix

| Dimension | Future-state value |
|---|---|
| UIX kind | public end-user SPA |
| Primary persona | tenant human user |
| Suggested mount | `https://login.example.com/` |
| Pages/views | `#/login`, `#/register`, `#/callback`, `#/profile`, `#/forgot-password`, `#/reset-password`, `#/verify-email`, `#/terms`, `#/consent` |
| Main workflows | browser login, registration, consent, logout, recovery, email verification, authenticated profile |
| Backend surfaces consumed | public auth routes and tenant discovery documents |
| Navigation scope | end-user only |
| Explicit exclusions | no tenant admin, no platform admin, no client management |
| Current repo basis | `pkgs/95-ui/public-uix/App.tsx`, discovery service, nginx allowlist |
| Main future-state gap | tenant branding and namespace entry model may need to be hardened |

## `platform-admin-uix` matrix

| Dimension | Future-state value |
|---|---|
| UIX kind | privileged operator SPA |
| Primary persona | platform superuser |
| Suggested mount | `https://platform-auth-admin.example.com/` |
| Pages/views | login, forgot password, reset password, change password, platform dashboard, tenant list, create tenant, tenant detail, assign tenant admin, platform identity administration, audit/health overview |
| Main workflows | create tenant, delete tenant, bootstrap tenant admins, inspect cross-tenant state, manage platform authorities |
| Backend surfaces consumed | `/admin/auth/*`, `/admin/tenants`, `/admin/identities`, `/rpc` |
| Navigation scope | deployment-wide only |
| Explicit exclusions | no tenant end-user auth, no tenant app self-service, no tenant-local day-to-day operations |
| Current repo basis | `pkgs/95-ui/admin-uix` auth shell plus tenant and identity management slices |
| Main future-state gap | current component tree needs separation between platform-only and tenant-local views |

## `tenant-admin-uix` matrix

| Dimension | Future-state value |
|---|---|
| UIX kind | tenant-scoped operator SPA |
| Primary persona | tenant administrator |
| Suggested mount | `https://tenant-auth-admin.example.com/` or tenant-scoped path mount |
| Pages/views | login, forgot password, reset password, change password, tenant dashboard, identity list, principal detail, create principal, credential issuance, signing keys, JWKS publication, tenant config/policy |
| Main workflows | create tenant principals, issue credentials, manage tenant admins, rotate signing keys, review tenant discovery posture |
| Backend surfaces consumed | `/admin/auth/*`, `/admin/identities`, `/rpc`, tenant discovery and tenant JWKS endpoints for parity/reference |
| Navigation scope | one tenant at a time |
| Explicit exclusions | no cross-tenant tenant creation, no platform-wide authority assignment |
| Current repo basis | `IdentityManagement.tsx`, `TenantJwksPublicationView.tsx`, portions of current `admin-uix` |
| Main future-state gap | tenant scoping and privilege boundaries need to be first-class in the UIX shell |

## `developer-uix` matrix

| Dimension | Future-state value |
|---|---|
| UIX kind | developer/integration SPA |
| Primary persona | tenant app developer or delegated app owner |
| Suggested mount | `https://developer-auth.example.com/` |
| Pages/views | developer dashboard, app catalog, create OIDC app, app detail, redirect URI management, grant/auth method config, client secret rotation, JWKS metadata management, discovery reference, integration examples |
| Main workflows | register app, update client metadata, rotate secrets, inspect discovery metadata, prepare integration settings |
| Backend surfaces consumed | `/register`, `/register/{client_id}`, `/rpc` client and client-registration methods, tenant discovery docs |
| Navigation scope | tenant application integration only |
| Explicit exclusions | no platform tenant lifecycle, no general end-user profile UX |
| Current repo basis | `ClientManagement.tsx`, client registration APIs, dynamic registration routes |
| Main future-state gap | current shipped navigation does not expose this as a first-class portal |

## `service-admin-uix` matrix

| Dimension | Future-state value |
|---|---|
| UIX kind | machine/workload operator SPA |
| Primary persona | service owner, platform integration operator, workload operator |
| Suggested mount | `https://service-auth.example.com/` |
| Pages/views | service dashboard, machine principals, API keys, client credentials, workload trust setup, token inspection, introspection test, access posture, secret rotation |
| Main workflows | onboard machine principals, issue service credentials, validate token behavior, manage non-human trust relationships |
| Backend surfaces consumed | `/token`, `/introspect`, JWKS endpoints, machine/service auth surfaces, future workload identity methods |
| Navigation scope | non-human access management only |
| Explicit exclusions | no human login UX, no platform tenant creation |
| Current repo basis | token plane, auth backends, API-key and service-key capability, introspection support |
| Main future-state gap | dedicated UIX and stable service-operator API surface do not yet exist |

## Future-state UIX route ownership matrix

| UIX | Route or view ownership | Backend lane used |
|---|---|---|
| `public-uix` | public auth pages and consent flow | public auth lane |
| `platform-admin-uix` | platform control pages | admin REST and RPC |
| `tenant-admin-uix` | tenant admin pages | admin REST, admin RPC, tenant discovery parity |
| `developer-uix` | client/app registration pages | registration plus client control plane |
| `service-admin-uix` | machine/service access pages | token, introspection, JWKS, service control plane |

## Future-state UIX split matrix

| Current UIX/component basis | Future-state UIX | Split action |
|---|---|---|
| `pkgs/95-ui/public-uix` | `public-uix` | preserve as the end-user auth UIX |
| `admin-uix` tenant creation and global authority controls | `platform-admin-uix` | extract into superuser-only console |
| `admin-uix` identities and JWKS management | `tenant-admin-uix` | extract into tenant-admin console |
| `ClientManagement.tsx` and client APIs | `developer-uix` | promote into a dedicated developer-facing UIX |
| no current dedicated service operator UI | `service-admin-uix` | compose a new machine-access UIX around existing backend capabilities |

## Future-state UIX transition matrix

| UIX | Near-term delivery path | Why this sequencing makes sense |
|---|---|---|
| `public-uix` | retain and refine | already aligned with future-state role boundaries |
| `platform-admin-uix` | first extraction from `admin-uix` | tenant creation and authority assignment are the highest-risk overloaded flows |
| `tenant-admin-uix` | second extraction from `admin-uix` | tenant-local identity and key administration need cleaner scoping |
| `developer-uix` | third extraction or net-new app | client/app workflows are present but not first-class in the current UI |
| `service-admin-uix` | later composition | best deferred until service identity becomes a first-class product surface |
