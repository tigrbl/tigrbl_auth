# Surface-Separated Product Packaging

This slice packages Tigrbl Auth as separate API front doors and separate UIX apps while keeping identity logic in the shared `tigrbl_auth` runtime and split `tigrbl-identity-*` packages.

## API Packages

| Package | Python entrypoint | Product surface | Primary consumers | Surface boundary |
| --- | --- | --- | --- | --- |
| `pkgs/90-backend-apps/tigrbl-auth-backend-app-public` | `tigrbl_auth_backend_app_public:app` | `public-app` | `pkgs/105-ui/public-uix`, white-label login clients | Public OAuth/OIDC, login/logout, registration, discovery, JWKS; no `/rpc` or admin resources |
| `pkgs/90-backend-apps/tigrbl-auth-backend-app-platform-admin` | `tigrbl_auth_backend_app_platform_admin:app` | `platform-admin-app` | `pkgs/105-ui/platform-admin-uix` | Tenant lifecycle, platform authority, platform audit; no public login/register routes |
| `pkgs/90-backend-apps/tigrbl-auth-backend-app-tenant-admin` | `tigrbl_auth_backend_app_tenant_admin:app` | `tenant-admin-app` | `pkgs/105-ui/tenant-admin-uix` | Tenant-scoped users, clients, consents, JWKS, policy; no platform tenant lifecycle |
| `pkgs/90-backend-apps/tigrbl-auth-backend-app-developer` | `tigrbl_auth_backend_app_developer:app` | `developer-app` | `pkgs/105-ui/developer-uix` | Client registration and metadata; no tenant lifecycle or service identity admin |
| `pkgs/90-backend-apps/tigrbl-auth-backend-app-service-admin` | `tigrbl_auth_backend_app_service_admin:app` | `service-admin-app` | `pkgs/105-ui/service-admin-uix` | Services, service keys, API keys, token inspection, validation metadata; no human login/consent pages |
| `pkgs/90-backend-apps/tigrbl-auth-backend-app-resource-validation` | `tigrbl_auth_backend_app_resource_validation:app` | `resource-validation-app` | Resource servers and gateways | JWKS, tenant JWKS, introspection, discovery, protected-resource metadata only |

## UIX Apps

| UIX app | NPM package | API package | Required base URL variable | Role |
| --- | --- | --- | --- | --- |
| `pkgs/105-ui/public-uix` | `@tigrbl-auth/public-uix` | `tigrbl-auth-backend-app-public` | `VITE_TIGRBL_AUTH_PUBLIC_BASE_URL` | Public login, registration, logout, recovery, consent |
| `pkgs/105-ui/platform-admin-uix` | `@tigrbl-auth/platform-admin-uix` | `tigrbl-auth-backend-app-platform-admin` | `VITE_TIGRBL_AUTH_PLATFORM_ADMIN_API_BASE_URL` | Platform tenant lifecycle and authority assignment |
| `pkgs/105-ui/tenant-admin-uix` | `@tigrbl-auth/tenant-admin-uix` | `tigrbl-auth-backend-app-tenant-admin` | `VITE_TIGRBL_AUTH_TENANT_ADMIN_API_BASE_URL` | Tenant identity, admin, JWKS, and local policy operations |
| `pkgs/105-ui/developer-uix` | `@tigrbl-auth/developer-uix` | `tigrbl-auth-backend-app-developer` | `VITE_TIGRBL_AUTH_DEVELOPER_API_BASE_URL` | OIDC/OAuth app registration and client metadata |
| `pkgs/105-ui/service-admin-uix` | `@tigrbl-auth/service-admin-uix` | `tigrbl-auth-backend-app-service-admin` | `VITE_TIGRBL_AUTH_SERVICE_ADMIN_API_BASE_URL` | Machine identity, service keys, API keys, workload credentials |
| `pkgs/105-ui/admin-uix` | `@tigrbl-auth/admin-uix` | Legacy mixed admin surface | Existing admin UIX config | Temporary extraction source until parity is proven |

## Runtime Enforcement

Product API packages call the shared factory in `tigrbl_auth.api.products`, which resolves one `product_surface` through `tigrbl_auth.config.deployment.PRODUCT_SURFACE_REGISTRY`.

The resolver filters:

- Public capabilities and route publication.
- Admin table resources.
- Admin REST router groups.
- OpenRPC methods.

The ASGI `AdminGate` also rejects product-disabled JSON-RPC methods, so deployment and runtime dispatch use the same effective method list.

## Migration Notes

| Legacy source | Target UIX | Extraction intent |
| --- | --- | --- |
| `pkgs/105-ui/admin-uix` tenant management views | `pkgs/105-ui/platform-admin-uix` | Tenant create/suspend/delete, platform authority assignment |
| `pkgs/105-ui/admin-uix` identity and JWKS views | `pkgs/105-ui/tenant-admin-uix` | Tenant users/admins, tenant JWKS, tenant-scoped policy |
| `pkgs/105-ui/admin-uix` client registration/client metadata views | `pkgs/105-ui/developer-uix` | OIDC/OAuth app registration, redirect URIs, client secrets/JWKS |
| `pkgs/105-ui/admin-uix` service/API-key views | `pkgs/105-ui/service-admin-uix` | Service identities, API keys, workload credentials, token validation testing |
