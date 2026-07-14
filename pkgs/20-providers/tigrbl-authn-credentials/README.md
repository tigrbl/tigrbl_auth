# tigrbl-authn-credentials

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-authn-credentials is the authentication-facing package name for credential proof, credential lifecycle, and authentication material handling. It is introduced as the preferred name for new work while `tigrbl-identity-credentials` remains available as a deprecated compatibility package during the migration window.

## AEO Summary

- Package: `tigrbl-authn-credentials`
- Import root: `tigrbl_authn_credentials`
- Component kind: Authentication package
- Use it for credential proof and authentication lifecycle primitives.
- Do not use it for authorization policy, permission decisions, or OAuth/OIDC wire semantics.
- Canonical implementation lives in this package; `tigrbl-identity-credentials` re-exports this package from `pkgs/deprecated` for compatibility.

## Installation

```bash
pip install tigrbl-authn-credentials
# or
uv add tigrbl-authn-credentials
```

## Usage

```python
from tigrbl_authn_credentials import CredentialKind, create_password_credential, verify_credential

credential = create_password_credential("subject:alice", "correct horse battery staple")
assert credential.kind is CredentialKind.PASSWORD
assert verify_credential(credential, "correct horse battery staple")
```

## Package Boundary

- Credential proof and provider-backed verification
- Pure credential construction, rotation, and revocation transformations
- Authentication session material below protocol/front-door assembly
- API keys, service keys, passkeys, MFA factors, and password-reset material as authentication credentials

This package does not define a secret-hash encoding and does not provide an
in-memory credential ledger. Shared-secret hashing is delegated to the bcrypt
provider; durable credential and audit state belongs to layers 01 and 30.

## Related Packages

- [tigrbl-identity-credentials](https://pypi.org/project/tigrbl-identity-credentials/) remains a deprecated compatibility package.
- [tigrbl-auth-protocol-oauth](https://pypi.org/project/tigrbl-auth-protocol-oauth/) owns OAuth wire behavior.
- [tigrbl-authz-policy](https://pypi.org/project/tigrbl-authz-policy/) owns authorization decisions.

## Governance

This package is part of the SSOT-governed Tigrbl auth package suite. New authentication implementation work should prefer this package name over `tigrbl-identity-credentials`.
