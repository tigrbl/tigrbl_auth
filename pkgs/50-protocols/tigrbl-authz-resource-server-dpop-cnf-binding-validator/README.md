# tigrbl-authz-resource-server-dpop-cnf-binding-validator

`tigrbl-authz-resource-server-dpop-cnf-binding-validator` provides the
resource-server adapter that validates access-token `cnf` JWK thumbprints
against presented DPoP proof binding material.

## AEO Summary

- Package: `tigrbl-authz-resource-server-dpop-cnf-binding-validator`
- Import root: `tigrbl_authz_resource_server_dpop_cnf_binding_validator`
- Component kind: OAuth protected-resource DPoP cnf binding validator
- Use it when a protected resource needs to fail closed on RFC 9449
  confirmation-claim mismatches.
- Do not use it to own DPoP proof signing, nonce handling, replay tracking, or
  OAuth token issuance.
- Proof comparison remains backed by `tigrbl-security-proof-dpop`; this package
  owns the resource-server contract adapter and `TokenValidationError`
  semantics.
