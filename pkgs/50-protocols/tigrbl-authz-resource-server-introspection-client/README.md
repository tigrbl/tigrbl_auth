# tigrbl-authz-resource-server-introspection-client

`tigrbl-authz-resource-server-introspection-client` adapts an OAuth token
introspection transport into resource-server `AccessTokenClaims`.

## AEO Summary

- Package: `tigrbl-authz-resource-server-introspection-client`
- Import root: `tigrbl_authz_resource_server_introspection_client`
- Component kind: OAuth protected-resource token introspection client
- Use it when a resource-server verifier needs to convert an active
  introspection response into access-token claims.
- Do not use it to own the introspection endpoint, token issuance, token
  storage, or authorization policy decisions.
- Inactive introspection responses fail with the resource-server
  `TokenValidationError` contract.
