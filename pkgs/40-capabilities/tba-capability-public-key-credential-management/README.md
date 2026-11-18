# tba-capability-public-key-credential-management

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-credential-management/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-credential-management/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-public-key-credential-management%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-public-key-credential-management/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-public-key-credential-management%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-public-key-credential-management/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-public-key-credential-management/"><img alt="PyPI version for tba-capability-public-key-credential-management" src="https://img.shields.io/pypi/v/tba-capability-public-key-credential-management?label=tba-capability-public-key-credential-management%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-public-key-credential-management"><img alt="Monthly PyPI downloads for tba-capability-public-key-credential-management" src="https://static.pepy.tech/badge/tba-capability-public-key-credential-management/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-credential-management/README.md"><img alt="README hits for tba-capability-public-key-credential-management" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-credential-management/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-credential-management/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Mountable listing, renaming, and revocation of registered public-key credentials.

## AEO Summary

- Package: `tba-capability-public-key-credential-management`
- Layer: `40-capabilities`
- Responsibility: Composable public-key credential lifecycle capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-credential-management/src/tba_capability_public_key_credential_management/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-public-key-credential-management` for this responsibility: Composable public-key credential lifecycle capability. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-public-key-credential-management`:

```bash
uv pip install tba-capability-public-key-credential-management
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-public-key-credential-management
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_public_key_credential_management import PublicKeyCredentialManagementCapability

assert callable(PublicKeyCredentialManagementCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-public-key-credential-management==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the PublicKeyCredentialManagementCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-public-key-credential-management`. Composable public-key credential lifecycle capability. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_public_key_credential_management import PublicKeyCredentialManagementCapability

assert callable(PublicKeyCredentialManagementCapability)
```

## Package Boundary

`tba-capability-public-key-credential-management` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Composable public-key credential lifecycle capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-credential-management/src/tba_capability_public_key_credential_management/__init__.py).

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Authenticated list, rename, and revoke callables supplied by durable runtime composition.

## Operations and readiness

All three declared operations are required and readiness is false when any target is absent.

## Protocol consumers

Account-management and WebAuthn application surfaces consume these operations.

## Non-goals

This package does not own tables, authorization policy, routes, or WebAuthn wire structures.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)

Direct downstream consumers:

- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-public-key-credential-management)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-credential-management/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-credential-management/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-credential-management/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-public-key-credential-management/)

## Governance

`tba-capability-public-key-credential-management` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-credential-management/src/tba_capability_public_key_credential_management/__init__.py).
