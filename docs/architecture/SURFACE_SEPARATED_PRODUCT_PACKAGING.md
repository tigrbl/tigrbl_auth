# Surface-Separated Product Packaging

This slice packages Tigrbl Auth as separate API front doors and separate UIX apps while keeping identity logic in the shared `tigrbl_auth` runtime and split `tigrbl-identity-*` packages.

## API Packages

| Package | Python entrypoint | Product surface | Primary consumers | Surface boundary |
| --- | --- | --- | --- | --- |
| `pkgs/80-apis/tigrbl-auth-api-public` | `tigrbl_auth_api_public:app` | `public-api` | `pkgs/90-apps/public-uix`, white-label login clients | Public OAuth/OIDC, login/logout, registration, discovery, JWKS; no `/rpc` or admin resources |
| `pkgs/80-apis/tigrbl-auth-api-platform-admin` | `tigrbl_auth_api_platform_admin:app` | `platform-admin-api` | `pkgs/90-apps/platform-admin-uix` | Tenant lifecycle, platform authority, platform audit; no public login/register routes |
| `pkgs/80-apis/tigrbl-auth-api-tenant-admin` | `tigrbl_auth_api_tenant_admin:app` | `tenant-admin-api` | `pkgs/90-apps/tenant-admin-uix` | Tenant-scoped users, clients, consents, JWKS, policy; no platform tenant lifecycle |
| `pkgs/80-apis/tigrbl-auth-api-developer` | `tigrbl_auth_api_developer:app` | `developer-api` | `pkgs/90-apps/developer-uix` | Client registration and metadata; no tenant lifecycle or service identity admin |
| `pkgs/80-apis/tigrbl-auth-api-service-admin` | `tigrbl_auth_api_service_admin:app` | `service-admin-api` | `pkgs/90-apps/service-admin-uix` | Services, service keys, API keys, token inspection, validation metadata; no human login/consent pages |
| `pkgs/80-apis/tigrbl-auth-api-resource-validation` | `tigrbl_auth_api_resource_validation:app` | `resource-validation-api` | Resource servers and gateways | JWKS, tenant JWKS, introspection, discovery, protected-resource metadata only |

## UIX Apps

| UIX app | NPM package | API package | Required base URL variable | Role |
| --- | --- | --- | --- | --- |
| `pkgs/90-apps/public-uix` | `@tigrbl-auth/public-uix` | `tigrbl-auth-api-public` | `VITE_TIGRBL_AUTH_PUBLIC_BASE_URL` | Public login, registration, logout, recovery, consent |
| `pkgs/90-apps/platform-admin-uix` | `@tigrbl-auth/platform-admin-uix` | `tigrbl-auth-api-platform-admin` | `VITE_TIGRBL_AUTH_PLATFORM_ADMIN_API_BASE_URL` | Platform tenant lifecycle and authority assignment |
| `pkgs/90-apps/tenant-admin-uix` | `@tigrbl-auth/tenant-admin-uix` | `tigrbl-auth-api-tenant-admin` | `VITE_TIGRBL_AUTH_TENANT_ADMIN_API_BASE_URL` | Tenant identity, admin, JWKS, and local policy operations |
| `pkgs/90-apps/developer-uix` | `@tigrbl-auth/developer-uix` | `tigrbl-auth-api-developer` | `VITE_TIGRBL_AUTH_DEVELOPER_API_BASE_URL` | OIDC/OAuth app registration and client metadata |
| `pkgs/90-apps/service-admin-uix` | `@tigrbl-auth/service-admin-uix` | `tigrbl-auth-api-service-admin` | `VITE_TIGRBL_AUTH_SERVICE_ADMIN_API_BASE_URL` | Machine identity, service keys, API keys, workload credentials |
| `pkgs/90-apps/admin-uix` | `@tigrbl-auth/admin-uix` | Legacy mixed admin surface | Existing admin UIX config | Temporary extraction source until parity is proven |

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
| `pkgs/90-apps/admin-uix` tenant management views | `pkgs/90-apps/platform-admin-uix` | Tenant create/suspend/delete, platform authority assignment |
| `pkgs/90-apps/admin-uix` identity and JWKS views | `pkgs/90-apps/tenant-admin-uix` | Tenant users/admins, tenant JWKS, tenant-scoped policy |
| `pkgs/90-apps/admin-uix` client registration/client metadata views | `pkgs/90-apps/developer-uix` | OIDC/OAuth app registration, redirect URIs, client secrets/JWKS |
| `pkgs/90-apps/admin-uix` service/API-key views | `pkgs/90-apps/service-admin-uix` | Service identities, API keys, workload credentials, token validation testing |
