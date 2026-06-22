# tigrbl-authz-resource-server-sender-constraint-validator

`tigrbl-authz-resource-server-sender-constraint-validator` composes the
resource-server DPoP and mTLS confirmation-claim validators into one
sender-constraint convenience object.

## AEO Summary

- Package: `tigrbl-authz-resource-server-sender-constraint-validator`
- Import root: `tigrbl_authz_resource_server_sender_constraint_validator`
- Component kind: OAuth protected-resource sender-constraint validator composer
- Use it when a protected resource wants one object to enforce required DPoP
  and mTLS binding checks.
- Do not use it to own DPoP proof validation, mTLS certificate comparison, token
  issuance, policy decisions, or resource-server request handling.
- DPoP and mTLS checks remain backed by their dedicated resource-server cnf
  validator packages.
