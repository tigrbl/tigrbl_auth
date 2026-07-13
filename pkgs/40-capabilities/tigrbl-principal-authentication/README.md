# tigrbl-principal-authentication

Composable record-backed authentication capabilities. Durable lookup operations
are injected from layer 30 and secret verification is delegated to layer-20
authenticator providers. The package does not own tables, routers, or protocol
authentication-method selection.

Operations:

- `authenticate_password`
- `authenticate_client_secret`
- `verify_client_record`
