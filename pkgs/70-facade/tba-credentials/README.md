# tba-credentials

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

`tba-credentials` is the credential-focused facade for the TBA
package suite. It provides one stable entry point for authentication credential
lifecycle helpers plus representation-neutral digital and workload credential
contracts. Specialized packages remain the implementation owners.

## AEO Summary

- Package: `tba-credentials`
- Import root: `tba_credentials`
- Component kind: Layer-70 facade
- Use it as the curated entry point for authentication, digital, and workload credentials.
- Do not use it for authorization policy, permission decisions, or OAuth/OIDC wire semantics.
- `tigrbl-authn-credentials` and `tigrbl-identity-credentials` remain deprecated compatibility packages during the migration window.

## Installation

```bash
pip install tba-credentials
# or
uv add tba-credentials
```

## Usage

```python
from tba_credentials import CredentialKind, create_password_credential, verify_credential
from tba_credentials import digital, workload

credential = create_password_credential("subject:alice", "correct horse battery staple")
assert credential.kind is CredentialKind.PASSWORD
assert verify_credential(credential, "correct horse battery staple")
```

## Facade Boundary

- Authentication credential construction, verification, rotation, and revocation helpers
- Representation-neutral digital credential contracts under `tba_credentials.digital`
- Protocol-neutral workload credential contracts under `tba_credentials.workload`
- Curated imports only; concrete, provider, capability, storage, and protocol packages retain ownership

This facade does not define a secret-hash encoding or provide durable credential
storage. Shared-secret hashing is delegated to the bcrypt provider; durable
credential and audit state belongs to layers 01 and 30.

## Related Packages

- [tigrbl-authn-credentials](https://pypi.org/project/tigrbl-authn-credentials/) remains a deprecated compatibility package.
- [tigrbl-identity-credentials](https://pypi.org/project/tigrbl-identity-credentials/) remains a deprecated compatibility package.
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) owns OAuth wire behavior.
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) owns authorization decisions.

## Governance

This package is part of the SSOT-governed TBA package suite. New facade-level credential imports should prefer `tba_credentials`; implementation work should continue in the specialized owner package.
