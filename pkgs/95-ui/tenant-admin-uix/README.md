# @tigrbl-auth/tenant-admin-uix

Tenant-scoped admin UIX for identities, tenant administrators, tenant JWKS, and tenant-local configuration.

## API Boundary

- Consumes `tigrbl-auth-api-tenant-admin`.
- Uses exactly one configured base URL: `VITE_TIGRBL_AUTH_TENANT_ADMIN_API_BASE_URL`.
- Blocks platform tenant lifecycle paths and public login/consent paths.
- `pkgs/95-ui/admin-uix` remains the temporary extraction source until parity is proven.
