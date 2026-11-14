# tba-credentials

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-credentials/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-credentials/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-credentials/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/70-facade"><img alt="Layer: 70 facade" src="https://img.shields.io/badge/Layer-70%20facade-0a7f5a"></a>
<a href="https://pypi.org/project/tba-credentials/"><img alt="PyPI version for tba-credentials" src="https://img.shields.io/pypi/v/tba-credentials?label=tba-credentials%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-credentials"><img alt="Monthly PyPI downloads for tba-credentials" src="https://static.pepy.tech/badge/tba-credentials/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-credentials/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

`tba-credentials` is the credential-focused facade for the TBA
package suite. It provides one stable entry point for authentication credential
lifecycle helpers plus representation-neutral digital and workload credential
contracts. Specialized packages remain the implementation owners.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_credentials import Credential

assert callable(Credential)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-credentials==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the Credential entry point is available.

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

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-credentials/src/tba_credentials/__init__.py).
