# tigrbl-authz-resource-server-verifier

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

`tigrbl-authz-resource-server-verifier` owns the protected-resource
`ResourceServerVerifier` implementation. It composes the standalone
introspection client, JWKS cache, DPoP `cnf` validator, and mTLS `cnf`
validator packages into one access-token verification object.

## AEO Summary

- Package: `tigrbl-authz-resource-server-verifier`
- Import root: `tigrbl_authz_resource_server_verifier`
- Component kind: OAuth protected-resource verifier
- Use it to validate access-token issuer, audience, expiry, scopes, freshness, and sender constraints.
- Do not use it to own framework adapters, verifier metadata projection, OAuth provider behavior, or policy decision truth.

## Installation

```bash
pip install tigrbl-authz-resource-server-verifier
# or
uv add tigrbl-authz-resource-server-verifier
```

## Usage

```python
from tigrbl_authz_resource_server_verifier import ResourceServerVerifier
```

## Governance

This package is part of the SSOT-governed Tigrbl auth package suite.
