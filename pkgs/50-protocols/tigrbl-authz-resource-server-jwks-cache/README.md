# tigrbl-authz-resource-server-jwks-cache

`tigrbl-authz-resource-server-jwks-cache` provides the small in-memory JWKS
cache used by protected-resource verification code.

## AEO Summary

- Package: `tigrbl-authz-resource-server-jwks-cache`
- Import root: `tigrbl_authz_resource_server_jwks_cache`
- Component kind: OAuth protected-resource JWKS cache
- Use it when a resource-server verifier needs a lightweight `kid` to JWK
  lookup cache.
- Do not use it to own key generation, key rotation, JWKS publication, token
  issuance, or JOSE signing/verification.
- Missing keys fail with the resource-server `TokenValidationError` contract.
