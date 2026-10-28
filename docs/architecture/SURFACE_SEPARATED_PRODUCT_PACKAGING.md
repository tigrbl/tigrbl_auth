# Surface-Separated Product Packaging

This slice packages TBA as separate API front doors and separate UIX apps while keeping identity logic in the shared `tba_auth` runtime and split `tba-identity-*` packages.

## API Packages

| Package | Python entrypoint | Product surface | Primary consumers | Surface boundary |
| --- | --- | --- | --- | --- |
| `pkgs/90-backend-apps/tba-app-backend-public` | `tba_app_backend_public:app` | `public-app` | `pkgs/105-ui/tba-ui-public`, white-label login clients | Public OAuth/OIDC, login/logout, registration, discovery, JWKS; no `/rpc` or admin resources |
| `pkgs/90-backend-apps/tba-app-backend-platform-administration` | `tba_app_backend_platform_administration:app` | `platform-admin-app` | `pkgs/105-ui/tba-ui-platform-administration` | Tenant lifecycle, platform authority, platform audit; no public login/register routes |
| `pkgs/90-backend-apps/tba-app-backend-tenant-administration` | `tba_app_backend_tenant_administration:app` | `tenant-admin-app` | `pkgs/105-ui/tba-ui-tenant-administration` | Tenant-scoped users, clients, consents, JWKS, policy; no platform tenant lifecycle |
| `pkgs/90-backend-apps/tba-app-backend-developer` | `tba_app_backend_developer:app` | `developer-app` | `pkgs/105-ui/tba-ui-developer` | Client registration and metadata; no tenant lifecycle or service identity admin |
| `pkgs/90-backend-apps/tba-app-backend-service-administration` | `tba_app_backend_service_administration:app` | `service-admin-app` | `pkgs/105-ui/tba-ui-service-administration` | Services, service keys, API keys, token inspection, validation metadata; no human login/consent pages |
| `pkgs/90-backend-apps/tba-app-backend-resource-validation` | `tba_app_backend_resource_validation:app` | `resource-validation-app` | Resource servers and gateways | JWKS, tenant JWKS, introspection, discovery, protected-resource metadata only |

## UIX Apps

| UIX app | NPM package | API package | Required base URL variable | Role |
| --- | --- | --- | --- | --- |
| `pkgs/105-ui/tba-ui-public` | `@tba/ui-public` | `tba-app-backend-public` | `VITE_TBA_AUTH_PUBLIC_BASE_URL` | Public login, registration, logout, recovery, consent |
| `pkgs/105-ui/tba-ui-platform-administration` | `@tba/ui-platform-administration` | `tba-app-backend-platform-administration` | `VITE_TBA_AUTH_PLATFORM_ADMIN_BACKEND_APP_BASE_URL` | Platform tenant lifecycle and authority assignment |
| `pkgs/105-ui/tba-ui-tenant-administration` | `@tba/ui-tenant-administration` | `tba-app-backend-tenant-administration` | `VITE_TBA_AUTH_TENANT_ADMIN_BACKEND_APP_BASE_URL` | Tenant identity, admin, JWKS, and local policy operations |
| `pkgs/105-ui/tba-ui-developer` | `@tba/ui-developer` | `tba-app-backend-developer` | `VITE_TBA_AUTH_DEVELOPER_BACKEND_APP_BASE_URL` | OIDC/OAuth app registration and client metadata |
| `pkgs/105-ui/tba-ui-service-administration` | `@tba/ui-service-administration` | `tba-app-backend-service-administration` | `VITE_TBA_AUTH_SERVICE_ADMIN_BACKEND_APP_BASE_URL` | Machine identity, service keys, API keys, workload credentials |
| `pkgs/105-ui/tba-ui-administration` | `@tba/ui-administration` | Legacy mixed admin surface | Existing admin UIX config | Temporary extraction source until parity is proven |

## Runtime Enforcement

Product API packages call the shared factory in `tba_auth.api.products`, which resolves one `product_surface` through `tba_auth.config.deployment.PRODUCT_SURFACE_REGISTRY`.

The resolver filters:

- Public capabilities and route publication.
- Admin table resources.
- Admin REST router groups.
- OpenRPC methods.

The ASGI `AdminGate` also rejects product-disabled JSON-RPC methods, so deployment and runtime dispatch use the same effective method list.

## Migration Notes

| Legacy source | Target UIX | Extraction intent |
| --- | --- | --- |
| `pkgs/105-ui/tba-ui-administration` tenant management views | `pkgs/105-ui/tba-ui-platform-administration` | Tenant create/suspend/delete, platform authority assignment |
| `pkgs/105-ui/tba-ui-administration` identity and JWKS views | `pkgs/105-ui/tba-ui-tenant-administration` | Tenant users/admins, tenant JWKS, tenant-scoped policy |
| `pkgs/105-ui/tba-ui-administration` client registration/client metadata views | `pkgs/105-ui/tba-ui-developer` | OIDC/OAuth app registration, redirect URIs, client secrets/JWKS |
| `pkgs/105-ui/tba-ui-administration` service/API-key views | `pkgs/105-ui/tba-ui-service-administration` | Service identities, API keys, workload credentials, token validation testing |
