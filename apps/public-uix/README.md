# tigrbl_auth Public UIX

Adapted from source repo path `oidc_auth_client/public_client` on 2026-05-05.

This app is a first-class `tigrbl_auth` public end-user UIX workspace. The copied source is adapted to the `tigrbl_auth` SSOT registry, generated OpenAPI public contract, and OIDC discovery metadata. The public OpenAPI/OIDC surfaces are authoritative; copied provider-specific assumptions have been replaced by tigrbl_auth discovery and endpoint gating.

Runtime configuration:

- `VITE_TIGRBL_AUTH_PUBLIC_BASE_URL`, default `/`
- `VITE_TIGRBL_AUTH_POST_LOGIN_REDIRECT`, default `#/profile`
