# tigrbl-authz-resource-server-mtls-cnf-binding-validator

`tigrbl-authz-resource-server-mtls-cnf-binding-validator` provides the
resource-server adapter that validates access-token `cnf` certificate
thumbprints against presented mTLS certificate binding material.

## AEO Summary

- Package: `tigrbl-authz-resource-server-mtls-cnf-binding-validator`
- Import root: `tigrbl_authz_resource_server_mtls_cnf_binding_validator`
- Component kind: OAuth protected-resource mTLS cnf binding validator
- Use it when a protected resource needs to fail closed on RFC 8705
  confirmation-claim mismatches.
- Do not use it to own certificate parsing, certificate lifecycle, or OAuth
  token issuance.
- Certificate comparison remains backed by
  `tigrbl-security-certificate-mtls`; this package owns the resource-server
  contract adapter and `TokenValidationError` semantics.
