# @tigrbl-auth/service-admin-uix

Service, machine, API-key, workload identity, and validation-testing UIX.

## API Boundary

- Consumes `tigrbl-auth-backend-app-service-admin`.
- Uses exactly one configured base URL: `VITE_TIGRBL_AUTH_SERVICE_ADMIN_BACKEND_APP_BASE_URL`.
- Allows service identity, service key, API key, token inspection, and validation metadata paths.
- Blocks tenant lifecycle and human login/consent paths.
