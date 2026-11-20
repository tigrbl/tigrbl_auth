# tba-credentials

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-credentials%3D%3D0.4.0.dev3/pkgs/070-facade/tba-credentials/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-credentials%3D%3D0.4.0.dev3/pkgs/070-facade/tba-credentials/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/070-facade"><img alt="Layer: 070 facade" src="https://img.shields.io/badge/Layer-070%20facade-0a7f5a"></a>
<a href="https://pypi.org/project/tba-credentials/"><img alt="PyPI version for tba-credentials" src="https://img.shields.io/pypi/v/tba-credentials?label=tba-credentials%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-credentials"><img alt="Monthly PyPI downloads for tba-credentials" src="https://static.pepy.tech/badge/tba-credentials/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/README.md"><img alt="README hits for tba-credentials" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

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

## When to use it

Choose `tba-credentials` for this responsibility: Credential facade for authentication, digital, and workload credential domains in the TBA package suite. Its `070-facade` placement keeps curated public entry points separate from moving implementation ownership out of focused packages.

## Installation

```bash
pip install tba-credentials
# or
uv add tba-credentials
```

Install the current `tba-credentials` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/070-facade/tba-credentials
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_credentials import Credential

assert callable(Credential)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-credentials==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the Credential entry point is available.

## Usage

```python
from tba_credentials import CredentialKind, create_password_credential, verify_credential
from tba_credentials import digital, workload

credential = create_password_credential("subject:alice", "correct horse battery staple")
assert credential.kind is CredentialKind.PASSWORD
assert verify_credential(credential, "correct horse battery staple")
```

## Package Boundary

- Authentication credential construction, verification, rotation, and revocation helpers
- Representation-neutral digital credential contracts under `tba_credentials.digital`
- Protocol-neutral workload credential contracts under `tba_credentials.workload`
- Curated imports only; concrete, provider, capability, storage, and protocol packages retain ownership

This facade does not define a secret-hash encoding or provide durable credential
storage. Shared-secret hashing is delegated to the bcrypt provider; durable
credential and audit state belongs to layers 01 and 30.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-credentials`:

- `issue_shared_secret` construction inputs: `secret`, `public_id`, `ttl`, `metadata`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_password_reset_credential` construction inputs: `ttl`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_api_key_credential` construction inputs: `public_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_service_key_credential` construction inputs: `public_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_client_secret_credential` construction inputs: `public_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_mfa_factor_credential` construction inputs: `factor_type`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_passkey_credential` construction inputs: `credential_id`, `public_key`, `sign_count`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `verify_credential` construction inputs: `now`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-credentials` exposes curated public entry points. Public operations found in its source:

- `new_credential_id` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `utc_now` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `hash_secret` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `verify_secret` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `issue_shared_secret` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_password_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_password_reset_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_api_key_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_service_key_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_client_secret_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_mfa_factor_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).
- `create_passkey_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/lifecycle.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-credentials`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md).

## Non-goals

`tba-credentials` does not take ownership of moving implementation ownership out of focused packages.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tigrbl-authn-credentials](https://pypi.org/project/tigrbl-authn-credentials/) remains a deprecated compatibility package.
- [tigrbl-identity-credentials](https://pypi.org/project/tigrbl-identity-credentials/) remains a deprecated compatibility package.
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) owns OAuth wire behavior.
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) owns authorization decisions.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/070-facade/tba-credentials)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-credentials/)

## Governance

This package is part of the SSOT-governed TBA package suite. New facade-level credential imports should prefer `tba_credentials`; implementation work should continue in the specialized owner package.

`tba-credentials` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `070-facade` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/src/tba_credentials/__init__.py).
