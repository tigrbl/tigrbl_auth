# @tigrbl-auth/tenant-admin-uix

Tenant-scoped admin UIX for identities, tenant administrators, tenant JWKS, and tenant-local configuration.

## API Boundary

- Consumes `tigrbl-auth-backend-app-tenant-admin`.
- Uses exactly one configured base URL: `VITE_TIGRBL_AUTH_TENANT_ADMIN_BACKEND_APP_BASE_URL`.
- Blocks platform tenant lifecycle paths and public login/consent paths.
- `pkgs/105-ui/admin-uix` remains the temporary extraction source until parity is proven.
