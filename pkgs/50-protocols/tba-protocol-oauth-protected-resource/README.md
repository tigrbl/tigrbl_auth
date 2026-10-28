# tba-protocol-oauth-protected-resource

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tba-protocol-oauth-protected-resource owns versioned OAuth protected-resource
protocol composition: claim sets, compatibility rules, metadata, sender
constraints, and verifier integration. It composes standalone validation
providers rather than acting as a compatibility facade. The legacy
`tigrbl-identity-resource-server` package remains unchanged under `deprecated`.

## AEO Summary

- Package: `tba-protocol-oauth-protected-resource`
- Import root: `tba_protocol_oauth_protected_resource`
- Component kind: Versioned OAuth protected-resource protocol composition
- Use it for protected API validation of issuer, audience, scopes, permissions, and proof bindings.
- Do not use it to own credential proof, identity records, or OAuth/OIDC provider truth.
- Canonical protected-resource exports live in this package. The verifier and reusable sender-constraint, JWKS, introspection, mTLS, and DPoP helpers are supplied by standalone layer-20 providers. Legacy packages under `pkgs/deprecated` retain their original names and imports.

## Installation

```bash
pip install tba-protocol-oauth-protected-resource
# or
uv add tba-protocol-oauth-protected-resource
```

## Usage

```python
from tba_protocol_oauth_protected_resource import AccessTokenClaims, ResourceRequirement, ResourceServerVerifier

requirement = ResourceRequirement(audience="api://billing", scopes=("invoice.read",))
claims = AccessTokenClaims(
    iss="https://issuer.example.test",
    sub="user:1",
    aud=("api://billing",),
    exp=1_800_000_300,
    iat=1_800_000_000,
    scope=("invoice.read",),
)
result = ResourceServerVerifier().verify_token(claims, requirement)
```

## Package Boundary

- Protected API token validation
- `versions.py` owns the implementation-profile history while
  `SPECIFICATION_VERSIONS` records the independently versioned RFCs composed by
  the profile.
- `features.py`, `compatibility.py`, and `migrations.py` own profile selection,
  feature reporting, and the legacy-unversioned metadata migration path.
- `claims.py`, `schemas.py`, `bindings.py`, and `errors.py` own protocol mapping;
  standalone claim classes and verifier implementations remain in lower layers.
- `capability.py` composes the layer-20 verifier into the reportable
  `protected-resource.authorization` layer-40 capability.
- Runtime capability truth and certification attestations are owned by
  `tba-certification-release.runtime_metadata` in layer 60; they are
  not protocol behavior.
- `contracts.py` is a compatibility export for the canonical OAuth
  verifier-contract mapping and does not resolve runtime deployments.
- Resource, audience, scope, permission, DPoP, mTLS, and introspection orchestration
- Resource-server framework adapters and verifier contracts
- Enforcement integration with authorization policy inputs

## Related Packages

- [tigrbl-identity-resource-server](https://pypi.org/project/tigrbl-identity-resource-server/) remains a deprecated compatibility package.
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) owns policy decision truth.
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) owns OAuth wire behavior.
- [tba-provider-authorization-resource-server-verifier](https://pypi.org/project/tba-provider-authorization-resource-server-verifier/) owns the reusable protected-resource verifier.
- [tba-provider-security-token-jwks-cache](https://pypi.org/project/tba-provider-security-token-jwks-cache/) and [tba-provider-token-introspection](https://pypi.org/project/tba-provider-token-introspection/) own token lookup helpers.
- [tba-provider-security-dpop-cnf-binding-validator](https://pypi.org/project/tba-provider-security-dpop-cnf-binding-validator/), [tba-provider-security-mtls-cnf-binding-validator](https://pypi.org/project/tba-provider-security-mtls-cnf-binding-validator/) provide the concrete confirmation-binding validators; the protected-resource authorization capability composes them.
- [tba-provider-security-proof-dpop](https://pypi.org/project/tba-provider-security-proof-dpop/) owns lower DPoP proof binding comparison.
- [tba-provider-security-certificate-mtls](https://pypi.org/project/tba-provider-security-certificate-mtls/) owns lower certificate binding comparison.

## Governance

This package is part of the SSOT-governed TBA package suite. New protected-resource implementation work should prefer this package name over `tigrbl-identity-resource-server`.
