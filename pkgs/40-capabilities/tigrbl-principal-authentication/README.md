# tigrbl-principal-authentication

Composable record-backed authentication capabilities. Durable lookup operations
are injected from layer 30 and secret verification is delegated to layer-20
authenticator providers. The package does not own tables, routers, or protocol
authentication-method selection.

Operations:

- `authenticate_password`
- `authenticate_client_secret`
- `verify_client_record`
- `authenticate_api_key`

`authenticate_api_key` receives digest, API-key lookup, service-key lookup,
principal resolution, and last-used mutation callables from layer 30. It does
not import mapped tables or own an in-memory credential store.
