# tigrbl_auth Public UIX

Adapted from source repo path `oidc_auth_client/public_client` on 2026-05-05.

This app is a first-class `tigrbl_auth` public end-user UIX workspace. The copied source is adapted to the `tigrbl_auth` SSOT registry, generated OpenAPI public contract, and OIDC discovery metadata. The public OpenAPI/OIDC surfaces are authoritative; provider-specific source assumptions are only retained where they can be gated by discovered endpoint support.

Runtime configuration:

- `VITE_TIGRBL_AUTH_PUBLIC_BASE_URL`, default `/`
- `VITE_TIGRBL_AUTH_POST_LOGIN_REDIRECT`, default `#/profile`
