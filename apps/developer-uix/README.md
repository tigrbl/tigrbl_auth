# @tigrbl-auth/developer-uix

Developer UIX for OIDC/OAuth client registration, redirect URI management, client metadata, secrets, and client JWKS.

## API Boundary

- Consumes `tigrbl-auth-api-developer`.
- Uses exactly one configured base URL: `VITE_TIGRBL_AUTH_DEVELOPER_API_BASE_URL`.
- Allows client registration and developer-scoped RPC paths.
- Blocks tenant lifecycle and service identity administration.
