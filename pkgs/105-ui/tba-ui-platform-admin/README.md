# @tba/ui-platform-admin

Platform owner and operator UIX for tenant lifecycle, tenant creation, and platform-level authority assignment.

## API Boundary

- Consumes `tba-app-backend-platform-admin`.
- Uses exactly one configured base URL: `VITE_TBA_AUTH_PLATFORM_ADMIN_BACKEND_APP_BASE_URL`.
- Blocks public login/consent/register paths from its backend client.
- `pkgs/105-ui/tba-ui-admin` remains the temporary extraction source until parity is proven.
