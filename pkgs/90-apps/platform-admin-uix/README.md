# @tigrbl-auth/platform-admin-uix

Platform owner and operator UIX for tenant lifecycle, tenant creation, and platform-level authority assignment.

## API Boundary

- Consumes `tigrbl-auth-api-platform-admin`.
- Uses exactly one configured base URL: `VITE_TIGRBL_AUTH_PLATFORM_ADMIN_API_BASE_URL`.
- Blocks public login/consent/register paths from its backend client.
- `pkgs/90-apps/admin-uix` remains the temporary extraction source until parity is proven.
