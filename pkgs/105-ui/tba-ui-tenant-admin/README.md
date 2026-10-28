# @tba/ui-tenant-admin

Tenant-scoped admin UIX for identities, tenant administrators, tenant JWKS, and tenant-local configuration.

## API Boundary

- Consumes `tba-app-backend-tenant-admin`.
- Uses exactly one configured base URL: `VITE_TBA_AUTH_TENANT_ADMIN_BACKEND_APP_BASE_URL`.
- Blocks platform tenant lifecycle paths and public login/consent paths.
- `pkgs/105-ui/tba-ui-admin` remains the temporary extraction source until parity is proven.
